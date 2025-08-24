from .impl import Monte_Carlo 
from custom_logging.logger_instance import logger

monte_carlo_predicter=Monte_Carlo(logger=logger, noise_std=0.01, num_of_samples_min=1, num_of_samples_max=1000)