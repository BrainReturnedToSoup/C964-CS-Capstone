import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

from logging.log_factory.interface import Log_Factory as Log_Factory_Interface
from services.predict.interface import Predicter as Predicter_Interface
from services.predict.interface import Prediction_Input, Prediction_Output
from services.predict.interface import Neighborhood

class Predicter(Predicter_Interface):
    def __init__(self, logger: Log_Factory_Interface, pretrained_model: GradientBoostingRegressor, prefit_scaler: StandardScaler, column_order):
        self.logger=logger
        self.pretrained_model=pretrained_model
        self.prefit_scaler=prefit_scaler
        self.column_order=column_order
    
    # convert the string-based labels of neighborhoods to distinct integers
    def convert_neighborhoods(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe["Neighborhood"] = dataframe["Neighborhood"].map(Neighborhood)
            
        return dataframe
    
    # Mainly to order the inputs based on the columns in the dataset. Safety net for if the dataset columns
    # or even the input data type change in order. 
    def order_input(self, input: Prediction_Input) -> pd.DataFrame:
        # ensure the order of the received input matches that of the columns
        ordered_data = [input[key] for key in self.column_order]
        
        df = pd.DataFrame(ordered_data, columns=self.column_order)
        
        return df

    # will transform the input to be on the scale of what the scaler has fit to the original 
    # train-and-test dataset. The model was trained on scaled data, which means inputs for production inference must 
    # match the same scale. 
    def transform_input(self, input: Prediction_Input) -> pd.DataFrame:
        df = self.order_input(input)
        
        X = df["SquareFeet"]
        
        # Extract columns to keep as is
        diff = df[df.columns.difference(["SquareFeet"])]

        # different from fit_transform, in that it doesn't change the scaler ratios, it 
        transformed_X_val = self.prefit_scaler.transform(X.values)

        # Combine scaled 'SquareFeet' with other columns
        recombined_data= np.hstack((transformed_X_val, diff.values))

        # Create a new DataFrame from the combined data
        # Need to make sure column order and names are correct
        transformed_df = pd.DataFrame(recombined_data, columns=self.column_order)
        
        return transformed_df
    
    def predict(self, input: Prediction_Input) -> Prediction_Output:
        transformed_input = self.transform_input(input)
        transformed_and_converted_input = self.convert_neighborhoods(transformed_input)
        prediction = self.pretrained_model.predict(transformed_and_converted_input)
        price = prediction[0]
        
        return { "Price": price }
    