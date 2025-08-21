import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from logging.logger_instance import logger
from services.predict.impl import Predicter

pretrained_model=joblib.load("../../static/model.pkl")
prefit_scaler=joblib.load("../../static/scaler.pkl")
columns=pd.read_csv("../../static/housing_price_dataset.csv").columns

predicter=Predicter(logger=logger, pretrained_model=pretrained_model, prefit_scaler=prefit_scaler, column_order=columns)