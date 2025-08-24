from typing import List
import numpy as np
from marshmallow import ValidationError
from ..interface import Prediction_Input, Prediction_Output
from ..interface import Predicter as Predicter_Interface
from ..instance import predicter
from .interface import Monte_Carlo as Monte_Carlo_Interface, Monte_Carlo_Output

# no point in injecting the predicter
# the methods in the class are way too coupled to the particular ML model for that to matter.
# plus, python doesn't really have any real encapsulation.

class Monte_Carlo(Monte_Carlo_Interface):
    def __init__(self, logger, noise_std: float=0.01, num_of_samples_min: int=1, num_of_samples_max: int=1000):
        self._validate_constructor_args(noise_std=noise_std, num_of_samples_min=num_of_samples_min, num_of_samples_max=num_of_samples_max)
        
        self.logger=logger
        self.predicter:Predicter_Interface=predicter
        self.noise_std=noise_std
        self.num_of_samples_min=num_of_samples_min
        self.num_of_samples_max=num_of_samples_max
    
    def _validate_constructor_args(noise_std: float, num_of_samples_min: int, num_of_samples_max: int) -> None:
        
        return
    
    def _create_noisy_input(self, input: Prediction_Input) -> Prediction_Input:
        input["SquareFeet"]=np.random.normal(0, self.noise_std, [[input["SquareFeet"]]])
        
        return input

    # will throw an error if input fails to match the Prediction_Input schema.
    # Python's type hints are so weak, that I am validating manually to reduce the amount of tests I have to make
    # to ensure proper behavior. This is especially important, considering potential nightmare bugs due to invalid model input data
    # because someone messed up up the stream (me)
    def _validate_input(self, input: Prediction_Input, num_of_samples: int) -> None:
        try:
            Prediction_Input().load(input)
            
            if not isinstance(num_of_samples, int):
                e=ValidationError(f"Supplied 'num_of_samples' is of invalid type:expected={int}:received={type(num_of_samples)}")
                raise e
            
            if (num_of_samples <= 0) or num_of_samples > self.num_of_samples_max:
                e=ValidationError(f"Supplied 'num_of_samples' invalid input:min={self.num_of_samples_min}:max={self.num_of_samples_max}:received{num_of_samples}")
                raise e
            
        except ValidationError as e:
            e.messages["origin"]="monte-carlo-service"
            raise e
        
    def predict(self, input: Prediction_Input, num_of_samples: int) -> Monte_Carlo_Output:
        self._validate_input(input=input, num_of_samples=num_of_samples)
        
        noisy_prediction_outputs:List[Prediction_Output]=[]
        
        for _ in range(self.num_of_samples_min, num_of_samples):
            noisy_input=self._create_noisy_input(input=input)
            noisy_prediction_output=self.predicter.predict(input=noisy_input)
            noisy_prediction_outputs.append(noisy_prediction_output)
            
        return { "prediction_outputs": noisy_prediction_outputs }
        