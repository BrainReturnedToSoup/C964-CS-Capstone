import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from logging.logger_instance import logger
from services.predict.impl import Predicter

model=joblib.load("../../static/model.pkl")
training_dataset=pd.read_csv("../../static/training_dataset.csv")
scaler=StandardScaler()

predicter = Predicter(logger=logger, model=model, dataset=training_dataset, scaler=scaler)