import numpy as np
from .interface import NEIGHBORHOOD
from .static import model_assets
from .preprocessor import Preprocessor
from back_end.custom_logging.instance import logger

def test_convert_to_ordered_df():
    preprocesser=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    
    # grab the first sample, get rid of the price column while preserving the intrinsic order of the columns
    initial_sample=model_assets.trainX_transformed_df.iloc[[0]]
    
    # pull only the fields that the "Prediction_Input" type has
    unordered_columns=["Neighborhood", "Bedrooms", "Bathrooms", "SquareFeet"]
    
    # ensure the out-of-order list of the columns is actually out-of-order in relation to the dataset, while containing all the same elements
    assert unordered_columns != list(model_assets.pretrained_gradient_boosted_regressor.feature_names_in_) and set(model_assets.pretrained_gradient_boosted_regressor.feature_names_in_) == set(unordered_columns)
    
    # create a mock input that is out of order compared to the raw column order in the underlying dataset.
    mock_prediction_input={}
    
    for key in unordered_columns:
        mock_prediction_input[key]=initial_sample[key].iloc[0] # get the val from the head, since its a one sample df

    ordered_df=preprocesser._convert_to_ordered_df(mock_prediction_input)
    
    # go element by element between the two lists representing columns, check if they are the same (they should be)
    assert all(a == b for a, b in zip(ordered_df.columns, model_assets.pretrained_gradient_boosted_regressor.feature_names_in_))

# comparing the conversion by the method to a conversion made in the 
# Google Collab repo the ML model was created in
def test_convert_neighborhoods():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    
    valid_input={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }
    
    prev_val=valid_input["Neighborhood"]
    
    converted_input=preprocessor._convert_neighborhoods(valid_input)

    assert converted_input["Neighborhood"] == NEIGHBORHOOD[prev_val]

def test_scaler_transform_input():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    
    # sample order should be the same
    unscaled_val=model_assets.trainX_raw_df["SquareFeet"].iloc[0]
    already_scaled_val=model_assets.trainX_transformed_df["SquareFeet"].iloc[0]
    
    mock_input={
        "Bathrooms": 2,
        "SquareFeet": unscaled_val,
        "Bedrooms": 4,
        "Neighborhood": "Rural"   
    }
    
    # the other portions of the mock input don't matter that much, we just need an input that 
    # meets "Prediction_Input". Will modify in place.
    transformed_input=preprocessor._scaler_transform_input(mock_input)
    
    # the transformed value should be the same as what alerady exists in the truncated and scaled df,
    # since the scaler was fit to the entire original dataset. Using a sample from that original dataset
    # should mean the transformation is deterministic given the dataset.
    assert np.isclose(already_scaled_val, transformed_input["SquareFeet"])