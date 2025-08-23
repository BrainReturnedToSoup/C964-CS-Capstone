import pytest
import numpy as np
import pandas as pd
from marshmallow import ValidationError
from custom_logging.logger_instance import logger
from .impl import Predicter
from .interface import Prediction_Input, NEIGHBORHOOD
from .static import housing_price_dataset_df, truncated_and_scaled_df, pretrained_gbr_model, prefit_scaler, input_columns, testX, testY, deltasY

# The trick for testing the predicter, is to test using the test set that was used in 
# the training of the model itself. The test set as well as the training deltas
# have already been generated, so assert that the model predicts these values and creates
# the same deltas. We must do this, because the implementation is highly opinionated to the
# structure of data used to train the model, so using the actual model as part of the test 
# is the way to ensure correctness.

predicter=Predicter(logger=logger) 

def test_predicter():
    assert predicter.logger == logger
    assert predicter.pretrained_model == pretrained_gbr_model
    assert predicter.prefit_scaler == prefit_scaler


def test_validate_input():
    # set of mocks, which combined should be good for testing validity of inputs across their permutations,
    # as well as the state machine of the predicter (potentially, it's stateful, so checking this is important)
    valid_but_out_of_order_input:Prediction_Input={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }

    invalid_input_1:Prediction_Input={
        "Bathrooms": 0, # the invalid field
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }

    invalid_input_2:Prediction_Input={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 0, # the invalid field
        "Neighborhood": "Rural"    
    }

    invalid_input_3:Prediction_Input={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "invalid" # the invalid field 
    }
        
    # should not raise an excception
    predicter.validate_input(valid_but_out_of_order_input)

    with pytest.raises(ValidationError) as e:
        predicter.validate_input(invalid_input_1)
    assert "predicter-service" in str(e.value)
    
    with pytest.raises(ValidationError) as e:
        predicter.validate_input(invalid_input_2)
    assert "predicter-service" in str(e.value)
    
    with pytest.raises(ValidationError) as e:
        predicter.validate_input(invalid_input_3)
    assert "predicter-service" in str(e.value)

# important to check whether supplied input data can be sorted to match the column order
# set. This is important, because the ML model is trained on a specific ordering of the 
# data, yet, Python will let you mess up the ordering. 
def test_convert_to_ordered_df():
    # grab the first sample, not including the price column, but preserving the intrinsic order of the columns
    initial_sample=truncated_and_scaled_df.loc[:, truncated_and_scaled_df.columns != "Price"].iloc[[0]]
    
    # pull only the fields that the "Prediction_Input" type has
    unordered_columns=["Neighborhood", "Bedrooms", "Bathrooms", "SquareFeet"]
    
    # ensure the out-of-order list of the columns is actually out-of-order in relation to the dataset, while containing all the same elements
    assert unordered_columns != list(pretrained_gbr_model.feature_names_in_) and set(pretrained_gbr_model.feature_names_in_) == set(unordered_columns)
    
    # create a mock input that is out of order compared to the raw column order in the underlying dataset.
    mock_prediction_input={}
    
    for key in unordered_columns:
        mock_prediction_input[key]=initial_sample[key].iloc[0] # get the val from the head, since its a one sample df

    ordered_df=predicter.convert_to_ordered_df(mock_prediction_input)
    
    assert all(a == b for a, b in zip(ordered_df.columns, pretrained_gbr_model.feature_names_in_))

# comparing the conversion by the method to a conversion made in the 
# Google Collab repo the ML model was created in
def test_convert_neighborhoods():
    valid_input={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }
    
    prev_val=valid_input["Neighborhood"]
    
    predicter.convert_neighborhoods(valid_input)

    assert valid_input["Neighborhood"] == NEIGHBORHOOD[prev_val]
    
def test_scaler_transform_input():
    # take the square feet from the first sample from the base dataset
    unscaled_val=housing_price_dataset_df["SquareFeet"].iloc[0]
    
    # take the square feet frmo the first sample of the truncated and scaled DF
    already_scaled_val=truncated_and_scaled_df["SquareFeet"].iloc[0]
    
    mock_input={
        "Bathrooms": 2,
        "SquareFeet": unscaled_val,
        "Bedrooms": 4,
        "Neighborhood": "Rural"   
    }
    
    # the other portions of the mock input don't matter that much, we just need an input that 
    # meets "Prediction_Input". Will modify in place.
    predicter.scaler_transform_input(mock_input)
    
    # the transformed value should be the same as what alerady exists in the truncated and scaled df,
    # since the scaler was fit to the entire original dataset. Using a sample from that original dataset
    # should mean the transformation is deterministic given the dataset.
    assert already_scaled_val == mock_input["SquareFeet"]
    
def test_predict():
    testX_subset=testX.iloc[0:50]
    testY_subset=testY.iloc[0:50]
    deltasY_subset=deltasY[0:50]

    # because testX is scaled and truncated, need to convert the values back since the predicter expects normal dataset-based vals
    testX_subset_reverted=testX_subset
    NEIGHBORHOOD_inverted = {v: k for k, v in NEIGHBORHOOD.items()}
    testX_subset_reverted["SquareFeet"] = prefit_scaler.inverse_transform(
        testX_subset_reverted[["SquareFeet"]].values
    ).flatten()
    
    for key in NEIGHBORHOOD_inverted:
        testX_subset_reverted["Neighborhood"] = testX_subset_reverted["Neighborhood"].replace(int(key), NEIGHBORHOOD_inverted[key])
        
    for i in range(0,50):
        sample=testX_subset_reverted.iloc[i]
        
        input={
            "Bathrooms": sample["Bathrooms"],
            "SquareFeet": sample["SquareFeet"],
            "Bedrooms": sample["Bedrooms"],
            "Neighborhood": sample["Neighborhood"]   
        }
        
        prediction=predicter.predict(input)
        delta=testY_subset.iloc[i].values[0]-prediction["PricePrediction"]
        assert delta == deltasY_subset[i]
    
    