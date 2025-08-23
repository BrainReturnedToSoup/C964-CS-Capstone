import pandas as pd
from pathlib import Path
import joblib

# must be version 1.6.1 sklearn same as what the model was trained in
from sklearn.ensemble import GradientBoostingRegressor 
from sklearn.preprocessing import StandardScaler

# This module is for initializing some important static assets to be used within 
# the predicter. By initializing these assets here, the interface, implementation, and instance modules
# can import them, and thus depend on a shared "model". 

curr_file_path=Path(__file__).resolve().parent

pretrained_gbr_model:GradientBoostingRegressor=joblib.load(curr_file_path / "model.pkl")
prefit_scaler:StandardScaler=joblib.load(curr_file_path / "scaler.pkl")

housing_price_dataset_df=pd.read_csv(curr_file_path / "housing_price_dataset.csv")

trainX=pd.DataFrame(joblib.load(curr_file_path / "trainX.pkl"))
trainX_renamed_scaled_ordered=pd.DataFrame(joblib.load(curr_file_path / "trainX_renamed_scaled_ordered.pkl"))
trainY=pd.DataFrame(joblib.load(curr_file_path / "trainY.pkl"))

testX=pd.DataFrame(joblib.load(curr_file_path / "testX.pkl"))
testX_renamed_scaled_ordered=pd.DataFrame(joblib.load(curr_file_path / "testX_renamed_scaled_ordered.pkl"))
testY=pd.DataFrame(joblib.load(curr_file_path / "testY.pkl"))

deltasY=pd.Series(joblib.load(curr_file_path / "deltasY.pkl"), index=testX.index)

trainX=trainX.sort_values(by="SquareFeet", inplace=False)
trainX_renamed_scaled_ordered=trainX_renamed_scaled_ordered.sort_values(by="SquareFeet", inplace=False)
trainY=trainY.loc[trainX.index]

testX=testX.sort_values(by="SquareFeet", inplace=False)
testX_renamed_scaled_ordered=testX_renamed_scaled_ordered.sort_values(by="SquareFeet", inplace=False)
testY=testY.loc[testX.index]

deltasY=list(deltasY.loc[testX.index])

trainX.reset_index(drop=True, inplace=True)
trainX_renamed_scaled_ordered.reset_index(drop=True, inplace=True)
trainY.reset_index(drop=True, inplace=True)
testX.reset_index(drop=True, inplace=True)
testX_renamed_scaled_ordered.reset_index(drop=True, inplace=True)
testY.reset_index(drop=True, inplace=True)
