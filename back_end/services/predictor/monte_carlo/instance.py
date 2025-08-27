from .impl import MonteCarlo 
from custom_logging.instance import logger
from ..instance import predictor

seed=18759127513

monte_carlo_predictor=MonteCarlo(logger=logger, predictor=predictor, seed=seed, noise_std=50, num_of_samples_min=1, num_of_samples_max=1000)