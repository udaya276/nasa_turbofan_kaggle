from nasa.exception import SensorException
from nasa.logger import logging
import sys
from nasa.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from nasa.entity.artifact_entity import DataIngestionArtifact
from nasa.componenets.data_ingestion import DataIngestion
from nasa.componenets.data_validation import DataValidation




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

    
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_ingestion()
        data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
