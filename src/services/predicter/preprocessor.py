import copy as cp
import pandas as pd
from typing import List
from sklearn.preprocessing import StandardScaler
from services.predicter.interface import Preprocessor as Preprocessor_Interface
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from services.predicter.interface import PredictionInput, NEIGHBORHOOD

class Preprocessor(Preprocessor_Interface):
    def __init__(self, logger: LogFactory_Interface, prefit_scaler: StandardScaler, columns: List[str]):
        self.logger=logger
        self.prefit_scaler=prefit_scaler
        self.columns=columns
        
    # convert the string-based labels of neighborhoods to distinct integers
    def _convert_neighborhoods(self, input: PredictionInput) -> PredictionInput:
        copy=cp.deepcopy(input)
        copy["Neighborhood"] = NEIGHBORHOOD[input["Neighborhood"]]
        return copy

    # will transform the input to be on the scale of what the scaler has fit to the original 
    # train-and-test dataset. Only scaled square feet, because the other features are categorical.
    def _scaler_transform_input(self, input: PredictionInput) -> PredictionInput:  
        copy=cp.deepcopy(input)
        copy["SquareFeet"] = self.prefit_scaler.transform([[input["SquareFeet"]]])[0][0]
        return copy
    
    # ensure the order of the received input matches that of the columns expected by the model
    def _convert_to_ordered_df(self, input: PredictionInput) -> pd.DataFrame:
        ordered_vals=[]
        
        for key in self.columns:
            ordered_vals.append(input[key])
        
        df = pd.DataFrame(data=[ordered_vals], columns=self.columns)
        
        return df
    
    def process(self, input: PredictionInput) -> pd.DataFrame:
        scaled_input=self._scaler_transform_input(input)
        scaled_converted_input=self._convert_neighborhoods(scaled_input)
        df=self._convert_to_ordered_df(scaled_converted_input)
        
        return df