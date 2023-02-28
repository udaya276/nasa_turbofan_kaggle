from nasa.exception import SensorException
from nasa.logger import logging
import sys
from nasa.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from nasa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from nasa.componenets.data_ingestion import DataIngestion
from nasa.componenets.data_validation import DataValidation
from nasa.componenets.data_transformation import DataTransformation
from nasa.componenets.model_trainer import ModelTrainer




class TrainPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise SensorException(e, sys)
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"start of data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"End of Data ingestion")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_data_validation(self, data_ingestion_artifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact = data_validation_artifact, data_transformation_config = data_transformation_config)
            data_transformation_artifact = data_transformation.inititate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config = self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)


    
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_ingestion()
        data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
        data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
        model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
