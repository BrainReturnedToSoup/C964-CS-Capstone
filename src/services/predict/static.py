import pandas as pd
from pathlib import Path
import joblib

# must be version 1.6.1 sklearn same as what the model was trained in
from sklearn.ensemble import GradientBoostingRegressor 
from sklearn.preprocessing import StandardScaler

# This module is for initializing some important static assets to be used within 
# the predicter. By initializing these assets here, the interface, implementation, and instance modules
# can import them, and thus depend on a shared "model". 

curr_file_path=Path(__file__).resolve()
src_path=curr_file_path.parent.parent.parent
static_path=src_path / "static"

# pull the base dataset, and the truncated and scaled df used to train the actual model. Sort them by the dependent var Y
# because some of the tests rely on picking the same semantic samples between these two dataframes. Sorting ensures consistency
housing_price_dataset_df=pd.read_csv(static_path / "housing_price_dataset.csv").sort_values(by="Price")
truncated_and_scaled_df:pd.DataFrame=pd.DataFrame(joblib.load(static_path / "truncated_and_scaled_df.pkl")).sort_values(by="Price")

pretrained_gbr_model:GradientBoostingRegressor=joblib.load(static_path / "model.pkl")
prefit_scaler:StandardScaler=joblib.load(static_path / "scaler.pkl")

testX=pd.DataFrame(joblib.load(static_path / "testX.pkl"))
testY=pd.DataFrame(joblib.load(static_path / "testY.pkl"))
deltasY=list(joblib.load(static_path / "deltasY.pkl"))