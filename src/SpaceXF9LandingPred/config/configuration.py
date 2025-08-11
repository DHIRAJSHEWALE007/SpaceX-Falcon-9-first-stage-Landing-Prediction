from SpaceXF9LandingPred.constants import *
from SpaceXF9LandingPred.utils.common import read_yaml, create_directories
from SpaceXF9LandingPred.entity import DataIngestionConfig, DataPreprocessingConfig, ModelEvaluationConfig, ModelTrainerConfig

class ConfigurationManager:
    def __init__(self, 
                config_filepath=CONFIG_FILE_PATH, 
                params_filepath=PARAMS_FILE_PATH):
        
        self.config_file=read_yaml(config_filepath)
        self.params_file=read_yaml(params_filepath)

        create_directories([self.config_file.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        
        config=self.config_file.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            data_url=config.data_url,
            data_path=config.data_path
        )

        return data_ingestion_config
    
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        
        config=self.config_file.data_preprocessing
        create_directories([config.root_dir])

        data_preprocessing_config=DataPreprocessingConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            encoder_ckpt=config.encoder_ckpt,
            processed_data_path=config.processed_data_path
        )

        return data_preprocessing_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        
        config=self.config_file.model_evaluation
        params=self.params_file.evaluation_params
        create_directories([config.root_dir])

        model_evaluation_config=ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            evaluation_result_path=config.evaluation_result_path
        )

        return model_evaluation_config, params
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        
        config=self.config_file.model_trainer
        params=self.params_file.training_params
        create_directories([config.root_dir])

        model_trainer_config=ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            scaler_ckpt=config.scaler_ckpt,
            model_ckpt=config.model_ckpt
        )

        return model_trainer_config, params