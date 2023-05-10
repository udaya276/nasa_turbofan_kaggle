from nasa.exception import SensorException
import os, sys
import yaml
import pandas as pd
from nasa.logger import logging
import dill
import pickle
import joblib


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)

def save_dataframe_to_csv(file_path: str, df:pd.DataFrame):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        df.to_csv(file_path, header=True, index=False)
    except Exception as e:
        raise SensorException(e, sys)

def save_object(file_path: str, obj:object)-> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            #pickle.dump(obj, file_obj)
            #joblib.dump(obj, file_obj)
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise SensorException(e, sys)
    
def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            #return pickle.load(file_obj)
            #return joblib.load(file_obj)
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys)
"""    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise SensorException(e, sys)
   
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
"""   
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)
