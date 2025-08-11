from SpaceXF9LandingPred.config.configuration import ConfigurationManager
import pandas as pd
import joblib

class PredictionPipeline:
    def __init__(self):
        self.trainer_config, _ = ConfigurationManager().get_model_trainer_config()
        self.preprocessing_config = ConfigurationManager().get_data_preprocessing_config()
        self.encoder = joblib.load(self.preprocessing_config.encoder_ckpt)
        self.scaler=joblib.load(self.trainer_config.scaler_ckpt)
        self.model=joblib.load(self.trainer_config.model_ckpt)

    def predict(self,X):

        features = X[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 
                 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 
                 'Serial']]
        
        categorical_cols = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial', 
                            'GridFins', 'Reused', 'Legs']
        
        numerical_cols = ['FlightNumber', 'PayloadMass', 'Flights', 'Block', 'ReusedCount']
        
        encoded_cats = self.encoder.transform(features[categorical_cols])

        encoded_cat_cols = self.encoder.get_feature_names_out(categorical_cols)
        
        encoded_df = pd.DataFrame(encoded_cats, columns=encoded_cat_cols, index=features.index)

        X = pd.concat([features[numerical_cols], encoded_df], axis=1)

        X.astype(float)
        

        X = self.scaler.transform(X)

        output = self.model.predict(X)

        return output
        