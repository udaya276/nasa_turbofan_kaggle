from nasa.exception import SensorException
from nasa.logger import logging
import sys
from nasa.entity.config_entity import TrainingPipelineConfig, DatabaseInsertionConfig, DataIngestionConfig, DataValidationConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from nasa.entity.artifact_entity import DataValidationArtifact, DatabaseInsertionArtifact, DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from nasa.componenets.data_validation import DataValidation
from nasa.componenets.database_insertion import DatabaseInsetion
from nasa.componenets.data_ingestion import DataIngestion
from nasa.componenets.data_validation import DataValidation
from nasa.componenets.data_transformation import DataTransformation
from nasa.componenets.model_trainer import ModelTrainer
from nasa.componenets.model_evaluation import ModelEvaluation
from nasa.componenets.model_pusher import ModelPusher
from nasa.cloud_storage.s3_syncer import S3Sync
from nasa.constant.s3_bucket import TRAINING_BUCKET_NAME
from nasa.constant.training_pipeline import SAVED_MODEL_DIR


class TrainPipeline:
    is_pipeline_running = False
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            self.s3_sync = S3Sync()
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_data_validation(self)->DataValidationArtifact:
        try:
            data_validate_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"Start data validation")
            data_validation = DataValidation(data_validate_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"End data validation")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_database_insertion(self, data_validation_artifact:DataValidationArtifact)->DatabaseInsertionArtifact:
        try:
            database_insertion_config = DatabaseInsertionConfig(training_pipeline_config = self.training_pipeline_config)
            logging.info(f"Start of databse insertion")
            database_insertion = DatabaseInsetion(database_insertion_config, data_validation_artifact)
            database_insertion.initiate_database_insertion()
            logging.info(f"End of databse insertion")
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            if DatabaseInsetion.database_insertion_status:
                data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
                logging.info(f"start of data ingestion")
                data_ingestion = DataIngestion(data_ingestion_config)
                data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
                logging.info(f"End of Data ingestion")
                return data_ingestion_artifact
            else:
                logging.info("Database insertion not complete")
        except Exception as e:
            raise SensorException(e, sys)
    """
    def start_data_validation(self, data_ingestion_artifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
    """
    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            data_transformation = DataTransformation(data_ingestion_artifact = data_ingestion_artifact, data_transformation_config = data_transformation_config)
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

    def start_model_evaluation(self,data_transformation_artifact:DataTransformationArtifact, model_trainer_artifact:ModelTrainerArtifact):
        try:
            model_eval_config = ModelEvaluationConfig(training_pipeline_config = self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config, data_transformation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_model_pusher(self, model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config = self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
    
    
    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True
            data_validation_artifact = self.start_data_validation()
            self.start_database_insertion(data_validation_artifact)
            data_ingestion_artifact = self.start_data_ingestion()
           # data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            logging.info("bypass start")
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact, model_trainer_artifact)
            logging.info("bypass end")
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)
            logging.info("run pipeline competed")
            TrainPipeline.is_pipeline_running = False
            logging.info("check s3 before")
            self.sync_artifact_dir_to_s3()
            logging.info("check s3 after")
            self.sync_saved_model_dir_to_s3()
            logging.info("check s3 completed")
        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainPipeline.is_pipeline_running = False
            raise SensorException(e, sys)

