from .impl import MonteCarlo 
from custom_logging.instance import logger
from ..instance import predicter

seed=18759127513

monte_carlo_predicter=MonteCarlo(logger=logger, predicter=predicter, seed=seed, noise_std=50, num_of_samples_min=1, num_of_samples_max=1000)