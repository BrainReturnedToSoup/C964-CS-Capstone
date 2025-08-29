import pytest
from marshmallow import ValidationError
import numpy as np
from back_end.custom_logging.instance import logger
from ..static import model_assets
from ..interface import PredictionInput
from ..impl import Predictor
from ..preprocessor import Preprocessor
from .impl import MonteCarlo
from .interface import MonteCarloOutput

def test_validate_constructor_args():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    valid_seed=18759127513
    valid_noise_std=50
    valid_num_of_samples_min=5
    valid_num_of_samples_max=1000
    
    # should not raise an exception
    mcp=MonteCarlo(logger=logger, predictor=predictor, seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
    invalid_seed=-1
    invalid_noise_std=-1
    invalid_num_of_samples_min=0
    invalid_num_of_samples_max=0
    
    # invalid seed
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(seed=invalid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid noise_std
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(seed=valid_seed, noise_std=invalid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples_min
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=invalid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples_max due to out-of-range (min==1)
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=invalid_num_of_samples_max)   
    assert "monte-carlo-predicter-service" in str(e.value)
       
    # invalid num_of_samples_max due to out-of-range (max<min) ()
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=5, num_of_samples_max=3)
    assert "monte-carlo-predicter-service" in str(e.value)
    
def test_validate_input():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    valid_seed=18759127513
    valid_noise_std=50
    valid_num_of_samples_min=2
    valid_num_of_samples_max=1000
    
    mcp=MonteCarlo(logger=logger, predictor=predictor, seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
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
    mcp._validate_input(input=valid_but_out_of_order_input, num_of_samples=6)
    
    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(invalid_input_1, num_of_samples=2)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(invalid_input_2, num_of_samples=2)
    assert "monte-carlo-predicter-service" in str(e.value)

    # invalid input given the mock
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(invalid_input_3, num_of_samples=2)
    assert "monte-carlo-predicter-service" in str(e.value)


    # invalid num_of_samples given the mock, num_of_samples == 0
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(valid_but_out_of_order_input, num_of_samples=0)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples given the mock, num_of_samples < min
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(valid_but_out_of_order_input, num_of_samples=1)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples given the mock, num_of_samples > max
    with pytest.raises(ValidationError) as e:
        mcp._validate_input(valid_but_out_of_order_input, num_of_samples=1001)
    assert "monte-carlo-predicter-service" in str(e.value)
    

def test_create_noisy_input():
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    valid_seed=18759127513
    valid_noise_std=50
    valid_num_of_samples_min=1
    num_of_samples:int=100000

    mcp=MonteCarlo(logger=logger, predictor=predictor, seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=num_of_samples)
    
    mock_input:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }
    
    noisy_inputs_squarefeet=[]
    
    for _ in range(num_of_samples):
        noisy_inputs_squarefeet.append(mcp._create_noisy_input(mock_input)["SquareFeet"]) 
        
    observed_mean=np.array(noisy_inputs_squarefeet).mean()
    
    # Values are close with a margin of ±2, which is sufficient given the number of samples.
    # This works because the noise follows a normal distribution, where the original
    # SquareFeet value is both the mean and median (approximately, since the implementation
    # casts to an int)
    assert np.isclose(mock_input["SquareFeet"], observed_mean, atol=2, rtol=0)

def test_predict():
    num_of_samples=999
    
    preprocessor=Preprocessor(logger=logger, prefit_scaler=model_assets.prefit_scaler, columns=model_assets.pretrained_gradient_boosted_regressor.feature_names_in_)
    predictor=Predictor(logger=logger, pretrained_model=model_assets.pretrained_gradient_boosted_regressor, preprocessor=preprocessor)
    valid_seed=18759127513
    valid_noise_std=50
    valid_num_of_samples_min=5
    valid_num_of_samples_max=1000
    
    mcp=MonteCarlo(logger=logger, predictor=predictor, seed=valid_seed, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
    mock_input:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }
    
    monte_carlo_output:MonteCarloOutput=mcp.predict(input=mock_input, num_of_samples=num_of_samples)
    
    assert len(monte_carlo_output["price_predictions"]) == num_of_samples
    assert len(monte_carlo_output["gaussian_noisy_square_feet"]) == num_of_samples