import pandas as pd
from pathlib import Path
import joblib

# must be version 1.6.1 sklearn same as what the model was trained in
from sklearn.ensemble import GradientBoostingRegressor 
from sklearn.preprocessing import StandardScaler

# This module is for initializing some important static assets to be used within 
# the predicter. By initializing these assets here, the interface, implementation, and instance modules
# can import them, and thus depend on a shared "model". 

curr_file_path=Path(__file__).resolve().parent.parent

class ModelAssets:
    def __init__(self):
        self.pretrained_gradient_boosted_regressor:GradientBoostingRegressor=joblib.load(curr_file_path / "model.pkl")
        self.prefit_scaler:StandardScaler=joblib.load(curr_file_path / "scaler.pkl")
        
        self.dataset_df=pd.read_csv(curr_file_path / "housing_price_dataset.csv")
        
        self.trainX_raw_df=pd.DataFrame(joblib.load(curr_file_path / "trainX.pkl"))
        self.trainX_transformed_df=pd.DataFrame(joblib.load(curr_file_path / "trainX_renamed_scaled_ordered.pkl"))
        self.trainY_df=pd.DataFrame(joblib.load(curr_file_path / "trainY.pkl")).loc[self.trainX_raw_df.index]
        
        self.testX_raw_df=pd.DataFrame(joblib.load(curr_file_path / "testX.pkl"))
        self.testX_transformed_df=pd.DataFrame(joblib.load(curr_file_path / "testX_renamed_scaled_ordered.pkl"))
        self.testY_df=pd.DataFrame(joblib.load(curr_file_path / "testY.pkl")).loc[self.testX_raw_df.index]
    
        self.deltasY=pd.Series(joblib.load(curr_file_path / "deltasY.pkl"), index=self.testX_raw_df.index)
        
        self.trainX_raw_df=self.trainX_raw_df.sort_values(by="SquareFeet", inplace=False)
        self.trainX_transformed_df=self.trainX_transformed_df.sort_values(by="SquareFeet", inplace=False)
        self.trainY_df=self.trainY_df.loc[self.trainX_raw_df.index]

        self.testX_raw_df=self.testX_raw_df.sort_values(by="SquareFeet", inplace=False)
        self.testX_transformed_df=self.testX_transformed_df.sort_values(by="SquareFeet", inplace=False)
        self.testY_df=self.testY_df.loc[self.testX_raw_df.index]
        
        self.deltasY=self.deltasY[self.testX_raw_df.index]
        
        # trainX.reset_index(drop=True, inplace=True)
        # trainX_renamed_scaled_ordered.reset_index(drop=True, inplace=True)
        # trainY.reset_index(drop=True, inplace=True)
        # testX.reset_index(drop=True, inplace=True)
        # testX_renamed_scaled_ordered.reset_index(drop=True, inplace=True)
        # testY.reset_index(drop=True, inplace=True)