from SpaceXF9LandingPred.config.configuration import ConfigurationManager
from SpaceXF9LandingPred.components.model_evaluation import ModelEvaluation
from SpaceXF9LandingPred.logging import logger


class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_evaluation_config, params = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config, params=params)
        model_evaluation.evaluate_models()

