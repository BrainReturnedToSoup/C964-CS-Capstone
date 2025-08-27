from marshmallow import ValidationError
from sklearn.ensemble import GradientBoostingRegressor
from custom_logging.log_factory.interface import LogFactory as LogFactory_Interface
from .interface import  PredictionInput, PredictionOutput, Predictor as Predictor_Interface, Preprocessor as Preprocessor_Interface

# no point in injecting the model, scaler, etc.
# the methods in the class are way too coupled to the particular ML model for that to matter.
# plus, python doesn't really have any real encapsulation.

# In the future, look into scikit-learn pipelines, instead of this more manual approach. 

class Predictor(Predictor_Interface):
    def __init__(self, logger: LogFactory_Interface, pretrained_model: GradientBoostingRegressor, preprocessor: Preprocessor_Interface):
        self.logger=logger
        self.pretrained_model=pretrained_model
        self.preprocessor=preprocessor
    
    # will throw an error if input fails to match the Prediction_Input schema.
    # Python's type hints are so weak, that I am validating manually to reduce the amount of tests I have to make
    # to ensure proper behavior. This is especially important, considering potential nightmare bugs due to invalid model input data
    # because someone messed up up the stream (me)
    def _validate_input(self, input: PredictionInput) -> None:
        try:
            PredictionInput().load(data=input)
        except ValidationError as e:
            e.messages["origin"]="predictor-service"
            raise e
            
    def predict(self, input: PredictionInput) -> PredictionOutput:
        self._validate_input(input)
        df=self.preprocessor.process(input)
        prediction=self.pretrained_model.predict(df)
        price=prediction[0]
        
        return { "price_prediction": price }
    