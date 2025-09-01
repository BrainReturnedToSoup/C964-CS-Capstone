from .impl import MonteCarlo 
from back_end.custom_logging.instance import logger
from ..instance import predictor

seed=18759127513 # an arbitrary seed, but nonetheless a constant to refer to for the sake of this project.

# a reasonable amount of noise, small enough that variations in square footage aren't mismatched to the categorical features.
# It wouldn't make sense for a 1000 square foot house to have 5 bed 3 bath now would it, and for that example to occur a non-trivial amount of times.
noise_std=50  

monte_carlo_predictor=MonteCarlo(logger=logger, predictor=predictor, seed=seed, noise_std=noise_std, num_of_samples_min=1, num_of_samples_max=1000)