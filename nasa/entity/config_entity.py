from datetime import datetime
import os
from nasa.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        #pipeline name
        self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp
        self.raw_data_dir_path = training_pipeline.RAW_DATA_DIR_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validated_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATED_DIR_NAME)
        self.accepted_dir = os.path.join(self.data_validated_dir, training_pipeline.ACCEPTED_DATA_DIR_NAME)
        self.rejected_dir = os.path.join(self.data_validated_dir, training_pipeline.REJECTED_DATA_DIR_NAME)

class DatabaseInsertionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_processed_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_PROCESSED_DIR_NAME)        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        self.training_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path:str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.raw_data_dir_path = "raw_data"
"""    
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)       
"""
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME)
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.PREPROCSSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_FILE_NAME)
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path: str = os.path.join(self.model_evaluation_dir, training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME)
        self.model_file_path: str = os.path.join(self.model_evaluation_dir, training_pipeline.MODEL_FILE_NAME)
        timestamp = round(datetime.now().timestamp())
        self.saved_model_path = os.path.join(training_pipeline.SAVED_MODEL_DIR, f"{timestamp}", training_pipeline.MODEL_FILE_NAME)


        