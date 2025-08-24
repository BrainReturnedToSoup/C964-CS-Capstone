import pytest
from marshmallow import ValidationError
from .impl import MonteCarlo
from custom_logging.instance import logger

@pytest.mark.order(11)
def test_validate_constructor_args():
    valid_noise_std=50
    valid_num_of_samples_min=5
    valid_num_of_samples_max=1000
    
    # should not raise an exception
    MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
    invalid_noise_std=-1
    invalid_num_of_samples_min=0
    invalid_num_of_samples_max=0
    
    # invalid noise_std
    with pytest.raises(ValidationError) as e:
        MonteCarlo(logger=logger, noise_std=invalid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    
    # invalid num_of_samples_min
    with pytest.raises(ValidationError) as e:
        MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=invalid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)

    # invalid num_of_samples_max due to out-of-range (min==1)
    with pytest.raises(ValidationError) as e:
        MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=invalid_num_of_samples_max)   
            
    # invalid num_of_samples_max due to out-of-range (max<min) ()
    with pytest.raises(ValidationError) as e:
        MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=5, num_of_samples_max=3)
        
@pytest.mark.order(12)
def test_validate_input():
    pass

@pytest.mark.order(13)
def test_create_noisy_input():
    pass

@pytest.mark.order(14)
def test_predict():
    pass