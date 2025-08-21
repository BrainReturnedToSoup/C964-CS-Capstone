from typing import TypedDict
from abc import ABC, abstractmethod

# inputs, REQUIRES MANUAL VALUE CHECKS WITHIN IMPLs
Square_Feet = [1000, 2999] # min & max
Bedrooms = set([2,3,4,5])
Bathrooms = set([1,2,3])
Neighborhood = {"Rural": 0, "Suburb": 1, "Urban": 2}

class Prediction_Input(TypedDict):
    SquareFeet: int
    Bathrooms: int
    Bedrooms: int
    Neighborhood: str

# outputs
class Prediction_Output(TypedDict):
    Price: float

class Predicter(ABC):
    @abstractmethod
    def predict(input: Prediction_Input) -> Prediction_Output:
        pass