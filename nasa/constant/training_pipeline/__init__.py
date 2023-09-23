import os

ARTIFACT_DIR: str = "artifact"
PIPELINE_NAME: str = "nasa"
RAW_DATA_DIR_NAME: str = 'raw_data'
"""
Data validation related constant start with DATA_VALIDATION_LOAD VAR NAME
"""
DATA_VALIDATED_DIR_NAME: str = "data_validation"
ACCEPTED_DATA_DIR_NAME: str = "accepted"
REJECTED_DATA_DIR_NAME:str = "rejected"
"""
Database related constant start with DATA_VALIDATION_LOAD VAR NAME
"""
DATA_PROCESSED_DIR_NAME: str = "data_processed"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
FILE_NAME: str = "nasa.csv"

DATA_INGESTION_INGESTED_DIR: str = "ingested"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

DATA_INGESTION_COLLECTION_NAME: str = "car"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
#PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.joblib"

"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_FILE_NAME:str = "model.pkl"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
#MODEL_FILE_NAME:str = "model.joblib"
#MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.joblib"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.10

"""
Model Evaluation ralated constant start with MODE TRAINER VAR NAME
"""
TARGET_COLUMN = "RUL"
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME= "report.yaml" 


"""
Model Pusher ralated constant
"""
SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR