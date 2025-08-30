import pytest
import numpy as np
from marshmallow import ValidationError
from back_end.custom_logging.instance import logger
from .interface import PredictionInput
from .static import model_assets
from .impl import Predictor
from .preprocessor import Preprocessor

def test_validate_input():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    
    valid_but_out_of_order_input:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }

    invalid_input_1:PredictionInput={
        "Bathrooms": 0, # the invalid field
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }

    invalid_input_2:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 0, # the invalid field
        "Neighborhood": "Rural"    
    }

    invalid_input_3:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "invalid" # the invalid field 
    }
    
    # should not throw an exception
    predictor._validate_input(input=valid_but_out_of_order_input)
    
    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        predictor._validate_input(invalid_input_1)
    assert "predictor-service" in str(e.value)
    
    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        predictor._validate_input(invalid_input_2)
    assert "predictor-service" in str(e.value)

    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        predictor._validate_input(invalid_input_3)
    assert "predictor-service" in str(e.value)

def test_predict():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    
    testX_subset=model_assets.testX_raw_df.iloc[0:50]
    testY_subset=model_assets.testY_df.iloc[0:50]
    deltasY_subset=list(model_assets.deltasY)[0:50]

    # now, grab each sample, and make a mock input from such sample. The predictor then predicts on these mock inputs
    # and the predictions are consolidated back to then be compared to deltas already made in Google Collab.
    for i in range(0,50):
        sample=testX_subset.iloc[i]
        
        print(sample["Neighborhood"])
        
        input={
            "Bathrooms": sample["Bathrooms"],
            "SquareFeet": sample["SquareFeet"],
            "Bedrooms": sample["Bedrooms"],
            "Neighborhood": sample["Neighborhood"]
        }
        
        prediction=predictor.predict(input)
        delta=testY_subset.iloc[i].values[0]-prediction["price_prediction"]
        assert np.isclose(delta, deltasY_subset[i])
    
    