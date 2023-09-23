from nasa.exception import SensorException
from nasa.logger import logging
import pandas as pd
import numpy as np
import sys
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from nasa.constant.database import SECURE_BUNDLE_FILE_LOCATION, CLIENT_ID, CLIENT_SECRET
from nasa.utils.main_utils import read_yaml_file
from nasa.constant.training_pipeline import SCHEMA_FILE_PATH

class Nasadata():
    """
    This class help to export entire cassandra db record as pandas dataframe
    """
    file_data_insertion_status = False


    def __init__(self):
        try:
            self.secure_bundle_file_location = SECURE_BUNDLE_FILE_LOCATION
            self.client_id = CLIENT_ID
            self.client_secret = CLIENT_SECRET
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)
        
    def database_connect(self):
        try:
            logging.info(f"Start of cassandra database connection")
            cloud_config= {'secure_connect_bundle': self.secure_bundle_file_location}
            logging.info(f"Check 1")
            auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
            logging.info(f"Check 2")
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            logging.info(f"Check 3")
            session = cluster.connect()
            logging.info("check 4")
            #row = session.execute("select release_version from system.local").one()
            #logging.info(f"Cassandra databse connected with Release version: ",{row[0]})
            return session
        except Exception as e:
            raise SensorException(e, sys)
        
    def export_raw_data_as_dataframe(self, session):
        logging.info(f"Start of reading from database and export as dataframe")
        df = pd.DataFrame(columns = self.schema_config['database_columns'])
        logging.info(f"Check 2_1")
        rows=session.execute("select * from test4.raw_data_with_uuid").all()
        logging.info(f"Check 2_2")
        for row in rows:
            df.loc[len(df)] = {'id':row[0], 'unit_number':row[1] ,'time_in_cycles':row[2] ,'set_1':row[3] ,'set_2':row[4] ,'set_3':row[5] ,'sen_1':row[6] ,'sen_2':row[7] ,'sen_3':row[8] ,'sen_4':row[9] ,'sen_5':row[10] ,'sen_6':row[11] ,'sen_7':row[12] ,'sen_8':row[13] ,'sen_9':row[14] ,'sen_10':row[15] ,'sen_11':row[16] ,'sen_12':row[17] ,'sen_13':row[18] ,'sen_14':row[19] ,'sen_15':row[20] ,'sen_16':row[21] ,'sen_17':row[22] ,'sen_18':row[23] ,'sen_19':row[24] ,'sen_20':row[25] ,'sen_21':row[26]}
        logging.info(f"Check 2_3")
        rslt_df = df.sort_values(by = ['unit_number', 'time_in_cycles'])
        logging.info(f"End of reading data from database")

        return rslt_df
  
    def insertion_data_into_database(self, session, file_path):            
        try:
            Nasadata.file_data_insertion_status =True              
            try:
                logging.info("inserts into existing database starts")
                with open(file_path, 'r') as f:
                    contents = f.readlines()
                    for content in contents:
                        new_cont = content.split()
                        new_array = np.array(new_cont, dtype=float)
                        nl = list(new_array)
                        session.execute(f"insert into test4.raw_data_with_uuid(id, unit_number ,time_in_cycles ,set_1 ,set_2 ,set_3 ,sen_1 ,sen_2 ,sen_3 ,sen_4 ,sen_5 ,sen_6 ,sen_7 ,sen_8 ,sen_9 ,sen_10 ,sen_11 ,sen_12 ,sen_13 ,sen_14 ,sen_15 ,sen_16 ,sen_17 ,sen_18 ,sen_19 ,sen_20 ,sen_21 ) values(uuid(),{nl[0]:.2f},{nl[1]:.2f},{nl[2]:.2f},{nl[3]:.2f},{nl[4]:.2f},{nl[5]:.2f},{nl[6]:.2f},{nl[7]:.2f},{nl[8]:.2f},{nl[9]:.2f},{nl[10]:.2f},{nl[11]:.2f},{nl[12]:.2f},{nl[13]:.2f},{nl[14]:.2f},{nl[15]:.2f},{nl[16]:.2f},{nl[17]:.2f},{nl[18]:.2f},{nl[19]:.2f},{nl[20]:.2f},{nl[21]:.2f},{nl[22]:.2f},{nl[23]:.2f},{nl[24]:.2f},{nl[25]:.2f})")
                logging.info(f"Database insertion complete to existing database table")
                Nasadata.file_data_insertion_status = True
                    
            except:
                session.execute("create table test4.raw_data_with_uuid(id uuid PRIMARY KEY, unit_number float,time_in_cycles float,set_1 float,set_2 float,set_3 float,sen_1 float,sen_2 float,sen_3 float,sen_4 float,sen_5 float,sen_6 float,sen_7 float,sen_8 float,sen_9 float,sen_10 float,sen_11 float,sen_12 float,sen_13 float,sen_14 float,sen_15 float,sen_16 float,sen_17 float,sen_18 float,sen_19 float,sen_20 float,sen_21 float)").one()
                logging.info("Cassandra database table created")
                with open(file_path, 'r') as f:
                    contents = f.readlines()
                    for content in contents:
                        new_cont = content.split()
                        new_array = np.array(new_cont, dtype=float)
                        nl = list(new_array)
                        session.execute(f"insert into test4.raw_data_with_uuid(id, unit_number ,time_in_cycles ,set_1 ,set_2 ,set_3 ,sen_1 ,sen_2 ,sen_3 ,sen_4 ,sen_5 ,sen_6 ,sen_7 ,sen_8 ,sen_9 ,sen_10 ,sen_11 ,sen_12 ,sen_13 ,sen_14 ,sen_15 ,sen_16 ,sen_17 ,sen_18 ,sen_19 ,sen_20 ,sen_21 ) values(uuid(),{nl[0]:.2f},{nl[1]:.2f},{nl[2]:.2f},{nl[3]:.2f},{nl[4]:.2f},{nl[5]:.2f},{nl[6]:.2f},{nl[7]:.2f},{nl[8]:.2f},{nl[9]:.2f},{nl[10]:.2f},{nl[11]:.2f},{nl[12]:.2f},{nl[13]:.2f},{nl[14]:.2f},{nl[15]:.2f},{nl[16]:.2f},{nl[17]:.2f},{nl[18]:.2f},{nl[19]:.2f},{nl[20]:.2f},{nl[21]:.2f},{nl[22]:.2f},{nl[23]:.2f},{nl[24]:.2f},{nl[25]:.2f})")
                logging.info("Database insertion complete after creating new database table")
                Nasadata.file_data_insertion_status = True   

        except Exception as e:
            Nasadata.file_data_insertion_status=False
            raise SensorException(e, sys)
