import copy as cp
import pandas as pd
from marshmallow import ValidationError
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from .interface import Predicter as Predicter_Interface
from .interface import PredictionInput, PredictionOutput, NEIGHBORHOOD
from static.loader import pretrained_gbr_model, prefit_scaler

# no point in injecting the model, scaler, etc.
# the methods in the class are way too coupled to the particular ML model for that to matter.
# plus, python doesn't really have any real encapsulation.

# In the future, look into scikit-learn pipelines, instead of this more manual approach. 

class Predicter(Predicter_Interface):
    def __init__(self, logger: LogFactory_Interface):
        self.logger=logger
        self.pretrained_model=pretrained_gbr_model
        self.prefit_scaler=prefit_scaler
    
    # convert the string-based labels of neighborhoods to distinct integers
    def _convert_neighborhoods(self, input: PredictionInput) -> PredictionInput :
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
        
        for key in self.pretrained_model.feature_names_in_:
            ordered_vals.append(input[key])
        
        df = pd.DataFrame(data=[ordered_vals], columns=self.pretrained_model.feature_names_in_)
        
        return df
    
    # will throw an error if input fails to match the Prediction_Input schema.
    # Python's type hints are so weak, that I am validating manually to reduce the amount of tests I have to make
    # to ensure proper behavior. This is especially important, considering potential nightmare bugs due to invalid model input data
    # because someone messed up up the stream (me)
    def _validate_input(self, input: PredictionInput) -> None:
        try:
            PredictionInput().load(input)
        except ValidationError as e:
            e.messages["origin"]="predicter-service"
            raise e
            
    def predict(self, input: PredictionInput) -> PredictionOutput:
        self._validate_input(input)
        scaled_input=self._scaler_transform_input(input)
        scaled_converted_input=self._convert_neighborhoods(scaled_input)
        df=self._convert_to_ordered_df(scaled_converted_input)
        prediction=self.pretrained_model.predict(df)
        price=prediction[0]
        
        return { "price_prediction": price }
    