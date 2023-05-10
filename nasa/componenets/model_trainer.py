from nasa.logger import logging
from nasa.exception import SensorException
import os, sys
from nasa.entity.config_entity import ModelTrainerConfig
from nasa.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact 
import pandas as pd
from sklearn.svm import SVR
from nasa.utils.main_utils import load_object, save_object
from nasa.ml.estimator import NasaModel
from nasa.ml.regression_metric import get_evaluation_score


class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)
        
    def train_model(self, x_train, y_train):
        try:
            svr = SVR(kernel = 'rbf')
            svr.fit(x_train, y_train)
            return svr
            
        except Exception as e:
            raise e
    
    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            df_train = self.read_data(train_file_path)
            df_test = self.read_data(test_file_path)
            
            x_train, y_train, x_test, y_test = df_train.iloc[:, :-1], df_train.iloc[:, -1], df_test.iloc[:,:-1], df_test.iloc[:, -1]
            
            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            regression_train_metric = get_evaluation_score(y_true = y_train, y_pred = y_train_pred)

            y_test_pred = model.predict(x_test)
            regression_test_metric = get_evaluation_score(y_true = y_test, y_pred = y_test_pred)

            #overfitting and underfitting
            diff_rmse = abs(regression_train_metric.rmse - regression_test_metric.rmse)
            diff_r2 = abs(regression_train_metric.r2score - regression_test_metric.r2score)

            #if diff_rmse > self.model_trainer_config.overfitting_underfitting_threshold or diff_r2 > self.model_trainer_config.overfitting_underfitting_threshold:
             #   raise Exception('Model is not good try to do more experimentation')


            preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok = True)
            nasa_model = NasaModel(preprocessor = preprocessor, model = model)
            save_object(self.model_trainer_config.trained_model_file_path, obj = nasa_model)

            #model trainer artifact
            model_trainer_artifact =  ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
            train_metric_artifact = regression_train_metric,
            test_metric_artifact = regression_test_metric)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)