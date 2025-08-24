from .impl import MonteCarlo 
from src.custom_logging.instance import logger

monte_carlo_predicter=MonteCarlo(logger=logger, noise_std=50, num_of_samples_min=1, num_of_samples_max=1000)