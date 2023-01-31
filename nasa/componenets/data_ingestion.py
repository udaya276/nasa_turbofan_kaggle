from nasa.exception import SensorException
from nasa.logger import logging
import sys, os
from nasa.entity.config_entity import DataIngestionConfig
from nasa.entity.artifact_entity import DataIngestionArtifact
from nasa.data_access.nasa_data import Nasadata
from pandas import DataFrame
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config= data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def move_files_to_respective_folder(self):
        pass

    def export_raw_data_into_feature_store(self):
        """
        Export raw data as data frame into feature
        """
        try:
            logging.info("Start of exporting raw data from data folder into feature store")
            nasadata = Nasadata()
            dataframe = nasadata.export_raw_data_as_dataframe(raw_data_dir = self.data_ingestion_config.raw_data_dir_path)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            #creating directory
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("End of exporting raw data from data folder into feature store")
            return dataframe
        except Exception as e:
            raise SensorException(e,sys)

    def split_data_as_train_test(self, dataframe:DataFrame) -> None:
        """
        Feture store dataset will be split into train and test file
        """
        try:
            logging.info("start of split_data_as_train_test operation")
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path")
        except Exception as e:
            return SensorException(e, sys)
            
    def export_validation_dependent_data(self):
        pass
    def export_validation_independent_data(self):
        pass
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_raw_data_into_feature_store()
            self.split_data_as_train_test(dataframe = dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            return SensorException(e, sys)
        
