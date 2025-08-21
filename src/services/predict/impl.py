import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

from logging.log_factory.interface import Log_Factory as Log_Factory_Interface
from services.predict.interface import Predicter as Predicter_Interface
from services.predict.interface import Prediction_Input, Prediction_Output
from services.predict.interface import Square_Feet, Bedrooms, Bathrooms, Neighborhood

class Predicter(Predicter_Interface):
    def __init__(self, logger: Log_Factory_Interface, model: GradientBoostingRegressor, dataset: pd.DataFrame, scaler: StandardScaler):
        self.logger=logger
        self.model=model
        self.dataset=dataset
        self.scaler=scaler
        
        self.dataset=self.fit_transform_dataset(self.dataset)
        self.dataset=self.convert_neighborhoods(self.dataset)
    
    def convert_neighborhoods(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # convert the string rep of neighborhoods to number values, completing the conversion
        dataframe["Neighborhood"] = dataframe["Neighborhood"].map(Neighborhood)
            
        return dataframe
    
    # will scale square feet and convert neighborhood types to numbers
    def fit_transform_dataset(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        X = dataframe[["SquareFeet"]]
        Y = dataframe["Price"]

        # Extract columns to keep as is
        diff = dataframe[dataframe.columns.difference(["SquareFeet", "Price"])]

        scaled_X_vals = self.scaler.fit_transform(X.values)

        # Combine scaled 'SquareFeet' with other columns
        # Ensure 'Price' is included if needed later
        data = np.hstack((scaled_X_vals, diff.values))
        data = np.hstack((data, np.reshape(Y.values, (-1, 1))))

        # Create a new DataFrame from the combined data
        # Need to make sure column order and names are correct
        scaled_df = pd.DataFrame(data, columns=["SquareFeet", "Bathrooms", "Bedrooms", "Neighborhood", "Price"])
        
        return scaled_df
    
    def order_input(self, input: Prediction_Input) -> pd.DataFrame:
        # ensure the order of the received input matches that of the columns
        column_order = self.dataset.columns
        
        ordered_data = [input[key] for key in column_order]
        
        df = pd.DataFrame(ordered_data, columns=column_order.keys())
        
        return df

    # will scale square feet and convert neighborhood types to numbers, utilizing the original scaler
    def transform_input(self, input: Prediction_Input) -> pd.DataFrame:
        df = self.order_input(input)
        
        X = df["SquareFeet"]
        
        # Extract columns to keep as is
        diff = df[df.columns.difference(["SquareFeet"])]

        # different from fit_transform, in that it doesn't change the scaler ratios, it 
        transformed_X_val = self.scaler.transform(X.values)

        # Combine scaled 'SquareFeet' with other columns
        recombined_data= np.hstack((transformed_X_val, diff.values))

        # Create a new DataFrame from the combined data
        # Need to make sure column order and names are correct
        transformed_df = pd.DataFrame(recombined_data, columns=["SquareFeet", "Bathrooms", "Bedrooms", "Neighborhood"])
        
        return transformed_df
    
    def validate_inputs(self, input: Prediction_Input) -> None:
        input_keys = input.keys()
        expected_keys = Prediction_Input.keys()
        
        missing_keys = input_keys - expected_keys
        extra_keys = expected_keys - input_keys
        
        if missing_keys:
            raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):input missing keys:expected={Prediction_Input.keys()}:received={input.keys()}")
        if extra_keys:
            raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):input has extra keys:expected={Prediction_Input.keys()}:received={input.keys()}")
        
        for key in input:
            if key == "SquareFeet" and (input[key] < Square_Feet[0] or input[key] > Square_Feet[1]):
                raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):invalid input for 'SquareFeet':expected={Square_Feet[0]}-{Square_Feet[1]}:received={input[key]}")
            
            if key == "Bedrooms" and not (input[key] in Bedrooms):
                raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):invalid input for 'Bathrooms':expected=(one of the following){Bedrooms}:received={input[key]}")
            
            if key == "Bathrooms" and not (input[key] in Bathrooms):
                raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):invalid input for 'Bedrooms':expected=(one of the following){Bathrooms}:received={input[key]}")
            
            if key == "Neighborhood" and not (input[key] in Neighborhood):
                raise Exception(f"services.predict.impl.Predicter.validate_inputs(self, input):invalid input for 'Neighborhood':expected=(one of the following){Bedrooms}:received={input[key]}")
            
        
    
    def predict(self, input: Prediction_Input) -> Prediction_Output:
        self.validate_inputs(input)
        
        transformed_input = self.transform_input(input)
        transformed_and_converted_input = self.convert_neighborhoods(transformed_input)
        prediction = self.model.predict(transformed_and_converted_input)
        price = prediction[0]
        
        return {"Price": price}
    