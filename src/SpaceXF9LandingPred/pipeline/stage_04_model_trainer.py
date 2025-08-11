from SpaceXF9LandingPred.config.configuration import ConfigurationManager
from SpaceXF9LandingPred.components.model_trainer import ModelTrainer
from SpaceXF9LandingPred.logging import logger


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_trainer_config, params = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config, params=params)
        model_trainer.train()