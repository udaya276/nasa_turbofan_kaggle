from nasa.logger import logging
from nasa.exception import SensorException
from nasa.entity.config_entity import ModelEvaluationConfig
from nasa.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, DataTransformationArtifact, ModelEvaluationArtifact
import sys
import pandas as pd
from nasa.constant.training_pipeline import TARGET_COLUMN
from nasa.ml.estimator import ModelResolver
from nasa.utils.main_utils import load_object, write_yaml_file
from nasa.ml.regression_metric import get_evaluation_score
#from nasa.ml.estimator import predict_df
class ModelEvaluation:
    def __init__(self, model_eval_config:ModelEvaluationConfig, data_transformation_artifact:DataTransformationArtifact,model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact            
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_evaluation(self):
        try:
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #valid train and test file dataframe
            train_df = pd.read_csv(transformed_train_file_path)
            test_df = pd.read_csv(transformed_test_file_path)

            df = pd.concat([train_df, test_df])
            y_true = df[TARGET_COLUMN]
            df.drop(TARGET_COLUMN, axis=1, inplace=True)
            logging.info("check eval 1")
            train_model_file_path = self.model_trainer_artifact.trained_model_file_path 
            logging.info(train_model_file_path)          
            #train_model_file_path = 'artifact\\04_26_2023_22_20_38\\model_trainer\\trained_model\\model.pkl'
            logging.info("check eval 2")
            model_resolver = ModelResolver()

            is_model_accepted = True
            
            logging.info("check eval_3")
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=None, 
                    best_model_path=None, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact, 
                    best_model_metric_artifact=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            logging.info("Check eval_4")
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path = latest_model_path)

            #latest_model = load_object(file_path = train_model_file_path)
            train_model = load_object(file_path = train_model_file_path)

            logging.info("check eval_5")
            y_trained_pred = train_model.predict(df)
            logging.info("check eval 5_1")
            y_latest_pred = latest_model.predict(df)
            #y_latest_pred = train_model.predict(df)

            logging.info("check eval 6")
            trained_metric = get_evaluation_score(y_true, y_trained_pred)
            latest_metric = get_evaluation_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.r2score-latest_metric.r2score
            if self.model_eval_config.change_threshold < improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted = False
            
            logging.info("check eval 7")
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path = latest_model_path,
                trained_model_path = train_model_file_path,
                train_model_metric_artifact = trained_metric,
                best_model_metric_artifact = latest_metric
            )
            model_eval_report = model_evaluation_artifact.__dict__

            #save the report
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        