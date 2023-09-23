from nasa.logger import logging
from nasa.exception import SensorException
from nasa.entity.config_entity import DataValidationConfig
from nasa.entity.artifact_entity import DataValidationArtifact
from nasa.constant import training_pipeline
from nasa.constant.training_pipeline import SCHEMA_FILE_PATH
from nasa.utils.main_utils import read_yaml_file
import os, sys
import pandas as pd
import shutil

class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig):
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            logging.info(f"Start of validate number of columns")
            number_of_columns = len(self._schema_config["columns"])-1
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:            
                return True
            logging.info(f"End of validate number of columns")
            return False             
        except Exception as e:
            raise SensorException(e, sys) 

    def is_numerical_column_present(self, dataframe:pd.DataFrame)->bool:
        try:
            logging.info(f"Start of checking numerical columns")
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            logging.info(f"End of checking numerical columns")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e,sys) 
    
    def initiate_data_validation(self):
        try:
            logging.info(f"Initiation of data validation")
            raw_data_directory_name = training_pipeline.RAW_DATA_DIR_NAME
            raw_data_directory_files = os.listdir(raw_data_directory_name)
            accepted_dir = self.data_validation_config.accepted_dir
            os.makedirs(accepted_dir)
            rejected_dir = self.data_validation_config.rejected_dir
            os.makedirs(rejected_dir)
            logging.info("Check validation 1")
            for file_name in raw_data_directory_files:
                logging.info(f"Data validation started for file: {file_name}")
                file_path = os.path.join(raw_data_directory_name, file_name)
                dataframe = pd.read_csv(file_path, names=self._schema_config['dataframe_columns'])   
                result_validate_number_of_column = self.validate_number_of_columns(dataframe)
                if result_validate_number_of_column:         
                    result_is_numerical_column_present = self.is_numerical_column_present(dataframe)

                    if result_is_numerical_column_present:
                        #move file to good
                        shutil.copy(file_path, accepted_dir)  #move to be changed to copy later
                        logging.info(f"{file_name} file moved to accepted directory")
                    else:
                        #move file to bad
                        shutil.move(file_path, rejected_dir)
                        logging.info(f"{file_name} file moved to rejected directory")
                else:
                    #move file to bad
                    shutil.move(file_path, rejected_dir)
                    logging.info(f"{file_name} file moved to rejected directory")
            data_validation_artifact = DataValidationArtifact(accepted_dir, rejected_dir)
            logging.info(f"End of Data validation")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
 





