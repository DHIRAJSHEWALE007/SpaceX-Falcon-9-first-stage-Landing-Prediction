import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import joblib

from SpaceXF9LandingPred.logging import logger

from SpaceXF9LandingPred.entity import DataPreprocessingConfig


class DataPreprocessing:
    def __init__(self, config:DataPreprocessingConfig):
        self.config=config

    def process_data(self):

        data = pd.read_csv(self.config.data_path)

        data['PayloadMass']=data['PayloadMass'].replace(np.nan, data['PayloadMass'].mean())
        data["Orbit"]=data["Orbit"].replace(np.nan, data["Orbit"].mode()[0])

        logger.info("Fixed Null/Missing Values")

        landing_outcomes = data['Outcome'].value_counts()
        bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])

        outcome_list = []
        for outcome in data['Outcome']:
            if outcome in bad_outcomes:
                outcome_list.append(0)
            else:
                outcome_list.append(1)

        data['Class']=outcome_list

        features = data[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 
                 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 
                 'Serial', 'Class']]

        categorical_cols = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial', 
                            'GridFins', 'Reused', 'Legs']
        numerical_cols = ['FlightNumber', 'PayloadMass', 'Flights', 'Block', 'ReusedCount', 'Class']

        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=float)

        encoded_cats = encoder.fit_transform(features[categorical_cols])

        joblib.dump(encoder, self.config.encoder_ckpt)

        encoded_cat_cols = encoder.get_feature_names_out(categorical_cols)
        
        encoded_df = pd.DataFrame(encoded_cats, columns=encoded_cat_cols, index=features.index)

        features_encoded = pd.concat([features[numerical_cols], encoded_df], axis=1)

        features_encoded.astype(float)

        logger.info("Features are Encoded Successfully")

        features_encoded.to_csv(self.config.processed_data_path, index=False)

        logger.info("Processed Data file has been created in artifacts")