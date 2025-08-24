import pytest
from .impl import MonteCarlo
from src.custom_logging.instance import logger

def test_validate_constructor_args():
    valid_noise_std=50
    valid_num_of_samples_min=5
    valid_num_of_samples_max=1000
    
    # shoud not raise an exception
    monte_carlo_predicter=MonteCarlo(logger=logger, noise_std=valid_noise_std, num_of_samples_min=valid_num_of_samples_min, num_of_samples_max=valid_num_of_samples_max)
    

def test_validate_input():
    pass

def test_create_noisy_input():
    pass

def test_predict():
    pass