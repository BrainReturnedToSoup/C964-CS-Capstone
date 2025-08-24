import pytest
from marshmallow import ValidationError
import numpy as np
from .impl import MonteCarlo
from ..interface import PredictionInput
from .interface import MonteCarloOutput
from custom_logging.instance import logger

@pytest.mark.order(11)
def test_validate_constructor_args():
    valid_noise_std=50
    valid_num_of_samples_min=5
    valid_num_of_samples_max=1000
    
    # should not raise an exception
    mcp=MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
    invalid_noise_std=-1
    invalid_num_of_samples_min=0
    invalid_num_of_samples_max=0
    
    # invalid noise_std
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(noise_std=invalid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples_min
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(noise_std=valid_noise_std, num_of_samples_min=invalid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    assert "monte-carlo-predicter-service" in str(e.value)
    
    # invalid num_of_samples_max due to out-of-range (min==1)
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=invalid_num_of_samples_max)   
    assert "monte-carlo-predicter-service" in str(e.value)
       
    # invalid num_of_samples_max due to out-of-range (max<min) ()
    with pytest.raises(ValidationError) as e:
        mcp._validate_constructor_args(noise_std=valid_noise_std, num_of_samples_min=5, num_of_samples_max=3)
    assert "monte-carlo-predicter-service" in str(e.value)
    
@pytest.mark.order(12)
def test_validate_input():
    mcp=MonteCarlo(logger=logger, noise_std=1, num_of_samples_min=2, num_of_samples_max=5)
    
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
    mcp._validate_input(input=valid_but_out_of_order_input, num_of_samples=2)
    
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
        mcp._validate_input(valid_but_out_of_order_input, num_of_samples=6)
    assert "monte-carlo-predicter-service" in str(e.value)
    

@pytest.mark.order(12)
def test_create_noisy_input():
    num_of_samples:int=100000

    mcp=MonteCarlo(logger=logger, noise_std=50, num_of_samples_min=1, num_of_samples_max=num_of_samples)
    
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

@pytest.mark.order(13)
def test_predict():
    num_of_samples=1000
    
    mcp=MonteCarlo(logger=logger,noise_std=50, num_of_samples_min=1, num_of_samples_max=num_of_samples)
    
    mock_input:PredictionInput={
        "Bathrooms": 2,
        "SquareFeet": 2187,
        "Bedrooms": 4,
        "Neighborhood": "Rural"    
    }
    
    monte_carlo_output:MonteCarloOutput=mcp.predict(input=mock_input, num_of_samples=num_of_samples)
    
    assert len(monte_carlo_output["price_predictions"]) == num_of_samples