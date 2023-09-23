from nasa.entity.artifact_entity import DataValidationArtifact, DatabaseInsertionArtifact
from nasa.entity.config_entity import DatabaseInsertionConfig
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from nasa.logger import logging
from nasa.exception import SensorException
from nasa.data_access.nasa_data import Nasadata
import os, sys
import numpy as np
import shutil


class DatabaseInsetion:
    database_insertion_status = False

    def __init__(self, database_insertion_config:DatabaseInsertionConfig, data_validation_artifact:DataValidationArtifact):
        self.database_insertion_config = database_insertion_config
        self.data_validation_artifact = data_validation_artifact


    def database_connect(self):
        try:
            nasadata = Nasadata()
            session = nasadata.database_connect()
            return session
        except Exception as e:
            raise SensorException(e, sys)

    def insert_data_into_database(self, session, file_path):
        try:
            nasadata = Nasadata()
            file_data_insertion_status = nasadata.insertion_data_into_database(session, file_path)
            return file_data_insertion_status              
        except Exception as e:
            raise SensorException(e, sys)
        

    def initiate_database_insertion(self):
        try:
            nasadata = Nasadata()
            DatabaseInsetion.database_insertion_status = False
            session = self.database_connect()
            processed_data_dir= self.database_insertion_config.data_processed_dir
            os.makedirs(processed_data_dir)
            accepted_dir_path = self.data_validation_artifact.accepted_dir_path
            accepted_dir_files_list = os.listdir(accepted_dir_path)
            logging.info("Juste before accepted dir check")
            if accepted_dir_files_list==None:
                DatabaseInsetion.database_insertion_status = False
                logging.info("No new file added in accepted dir list or accepted directory is empty")
            else:

                for file in accepted_dir_files_list:
                    file_path = os.path.join(self.data_validation_artifact.accepted_dir_path, file)
                    self.insert_data_into_database(session, file_path)
                    if nasadata.file_data_insertion_status:
                        shutil.move(file_path, processed_data_dir)
                DatabaseInsetion.database_insertion_status = True
                logging.info("file data added in database")

        except Exception as e:
            DatabaseInsetion.database_insertion_status = False
            raise SensorException(e, sys)       
