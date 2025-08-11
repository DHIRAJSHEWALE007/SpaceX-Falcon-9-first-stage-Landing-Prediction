from SpaceXF9LandingPred.config.configuration import ConfigurationManager
from SpaceXF9LandingPred.components.data_preprocessing import DataPreprocessing
from SpaceXF9LandingPred.logging import logger


class DataPreprocessingTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        config=ConfigurationManager()
        data_preprocessing_config=config.get_data_preprocessing_config()
        data_preprocessing=DataPreprocessing(config=data_preprocessing_config)
        data_preprocessing.process_data()
