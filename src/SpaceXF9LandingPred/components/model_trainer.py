import pandas as pd
import numpy as np

from SpaceXF9LandingPred.logging import logger

from SpaceXF9LandingPred.entity import ModelTrainerConfig

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig, params):
        self.config=config
        self.params=params
        self.scaler=StandardScaler()

    def train(self):
        data = pd.read_csv(self.config.data_path)
        X = data.drop(columns=['Class'], axis=1)
        Y = data['Class'].to_numpy()

        X = self.scaler.fit_transform(X)
        
        joblib.dump(self.scaler, self.config.scaler_ckpt)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
        
        parameters=dict(self.params.svc)
        model=SVC(**parameters)
        model.fit(X_train, Y_train)
        accuracy=model.score(X_test, Y_test)

        logger.info(f"Model trained with accuracy score of {accuracy*100:.2f}% on test data.")

        joblib.dump(model, self.config.model_ckpt)

        logger.info("Model Checkpoint is created in artifacts")