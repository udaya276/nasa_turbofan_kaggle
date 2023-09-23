from nasa.logger import logging
from nasa.exception import SensorException
import sys
from nasa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from nasa.entity.config_entity import DataValidationConfig
import pandas as pd
from nasa.utils.main_utils import read_yaml_file
from nasa.constant.training_pipeline import SCHEMA_FILE_PATH
import shutil


class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path):
        try:
            df = pd.read_csv(file_path)
            return df

        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])-1
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False 
        except Exception as e:
            raise SensorException(e, sys) 
         
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e,sys)         

    def initiate_data_validation(self):
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #validate number of columns
            status = self.validate_number_of_columns(dataframe = train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe doesnot contain all columns. \n"
            status = self.validate_number_of_columns(dataframe = test_dataframe)
            if not status:
                error_message = f"{error_message}test dataframe doesnot contain all columns. \n"

            #validate numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"
            
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"
            
            if len(error_message)>0:
                raise Exception(error_message)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)


