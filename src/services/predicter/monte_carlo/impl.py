from typing import List
import copy as cp
import numpy as np
from marshmallow import ValidationError
from ..interface import PredictionInput, PredictionOutput
from ..interface import Predicter as Predicter_Interface
from ..instance import predicter
from .interface import MonteCarlo as MonteCarlo_Interface, MonteCarloOutput, ConstructorArgs, PredictArgs


# no point in injecting the predicter
# the methods in the class are way too coupled to the particular ML model for that to matter.
# plus, python doesn't really have any real encapsulation.

class MonteCarlo(MonteCarlo_Interface):
    def __init__(self, logger, noise_std: int, num_of_samples_min: int=1, num_of_samples_max: int=1000):
        self._validate_constructor_args(noise_std=noise_std, num_of_samples_min=num_of_samples_min, num_of_samples_max=num_of_samples_max)
        
        # a Gradient Boosted Regressor
        self.predicter:Predicter_Interface=predicter
        self.rand_seed=1857295 # just something arbitrary to be used by the random generator for noise generation.
       
        # set the seed and immediately get the base state. From now on, the state will be reused in the given class instance
        np.random.seed(self.rand_seed) 
        self.np_random_state=np.random.get_state()
        
        self.logger=logger
        self.noise_std=noise_std # standard deviation based on raw += square feet. ex: noise_std=50 means +-50 squarefeet as the standard dev.
        self.num_of_samples_min=num_of_samples_min
        self.num_of_samples_max=num_of_samples_max

    def _validate_constructor_args(self, noise_std: int, num_of_samples_min: int, num_of_samples_max: int) -> None:
        constructor_args_schema=ConstructorArgs() # initialize it in-method, since you only really need to use it once on class instantiation
        
        try:
            constructor_args_schema.load({"noise_std": noise_std, "num_of_samples_min": num_of_samples_min, "num_of_samples_max": num_of_samples_max})
        except ValidationError as e:
            e.messages["origin"]="monte-carlo-predicter-service"
            raise e
        
    # treat the rand generation as a transaction. np.random is global, so the class instance needs to maintain 
    # state to get np.random back to the proper state for this given class. This means the method is deterministic
    # based on a seed, which is important for testing. Also, by holding the relevant state locally, other parts of the 
    # system can follow a similar pattern, and hold their own locally seeded state. Python is single-threaded so this works.
    def _create_noisy_input(self, input: PredictionInput) -> PredictionInput:
        copy=cp.deepcopy(input)
        current_square_feet = input["SquareFeet"]
        
        np.random.set_state(self.np_random_state)
        # Generate noise with mean=0, std=self.noise_std
        # This creates values that are symmetrically distributed around 0
        noise = np.random.normal(0, self.noise_std)
        
        copy["SquareFeet"]=max(int(current_square_feet+noise), 0) # needs to be whole ints as per the dataset. max(x, 0) is for the case that the final square feet value is negative (impossible irl)
        
        self.np_random_state=np.random.get_state()
        
        return copy

    # will throw an error if input fails to match the Prediction_Input schema.
    # Python's type hints are so weak, that I am validating manually to reduce the amount of tests I have to make
    # to ensure proper behavior. This is especially important, considering potential nightmare bugs due to invalid model input data
    # because someone messed up up the stream (me)
    def _validate_input(self, input: PredictionInput, num_of_samples: int) -> None:
        predict_args_schema=PredictArgs(num_of_samples_min=self.num_of_samples_min, num_of_samples_max=self.num_of_samples_max)
         
        try:
            predict_args_schema.load({"input": input, "num_of_samples": num_of_samples})
        except ValidationError as e:
            e.messages["origin"]="monte-carlo-predicter-service"
            raise e
        
    def predict(self, input: PredictionInput, num_of_samples: int) -> MonteCarloOutput:
        self._validate_input(input=input, num_of_samples=num_of_samples)
        
        # create a bunch of predictions with applied noise. 
        noisy_prediction_outputs:List[PredictionOutput]=[]
        
        for _ in range(num_of_samples):
            noisy_input=self._create_noisy_input(input=input)
            noisy_prediction_output=self.predicter.predict(input=noisy_input)
            noisy_prediction_outputs.append(noisy_prediction_output)
            
        return { "prediction_outputs": noisy_prediction_outputs }
        