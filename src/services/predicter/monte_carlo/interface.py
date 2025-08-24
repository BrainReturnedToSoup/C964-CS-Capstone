from typing import List, TypedDict
from abc import ABC, abstractmethod
from ..interface import Prediction_Input, Prediction_Output

class Monte_Carlo_Output(TypedDict):
    price_predictions: List[Prediction_Output]

class Monte_Carlo(ABC):
    @abstractmethod    
    def predict(input: Prediction_Input, num_of_samples) -> Monte_Carlo_Output:
        pass