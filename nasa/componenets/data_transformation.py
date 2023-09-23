from nasa.logger import logging
from nasa.exception import SensorException
import os, sys
import pandas as pd
from nasa.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from nasa.entity.config_entity import DataTransformationConfig
from nasa.utils.main_utils import save_dataframe_to_csv, save_object
class DataTransformation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            logging.info("Start of reading from file")
            index_names = ['unit_number', 'time_cycles']
            setting_names = ['setting_1', 'setting_2', 'setting_3']
            sensor_names = ['Fan inlet temperature', 'LPC outlet temperature', 'HPC outlet temperature', 'LPT outlet temperature', 
            'Fan inlet Pressure', 'bypass-duct pressure', 'HPC outlet pressure', 'Physical fan speed', 'Physical core speed', 'Engine pressure ratio', 'HPC outlet Static pressure',
            'Ratio of fuel flow to Ps30', 'Corrected fan speed', 'Corrected core speed', 'Bypass Ratio', 'Burner fuel-air ratio', 'Bleed Enthalpy', 'Required fan speed', 'Required fan conversion speed',
            'High-pressure turbines Cool air flow', 'Low-pressure turbines Cool air flow' ]
            col_names = index_names + setting_names + sensor_names          
            df = pd.read_csv(file_path, header=0,names=col_names)

            #Add RUL column
            train_grouped_by_unit = df.groupby(by='unit_number') 
            max_time_cycles = train_grouped_by_unit['time_cycles'].max() 
            merged = df.merge(max_time_cycles.to_frame(name='max_time_cycle'), left_on='unit_number',right_index=True)
            merged["RUL"] = merged["max_time_cycle"] - merged['time_cycles']
            merged = merged.drop("max_time_cycle", axis=1) 
            logging.info("End of reading from file")
            return merged
            
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            pass
            #minmaxscaler = MinMaxScaler()
            #preprocessor = Pipeline(steps=[("MinMaxScaler",minmaxscaler)])
            #return minmaxscaler
        except Exception as e:
            raise SensorException(e, sys)

    def inititate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = DataTransformation.read_data(self.data_ingestion_artifact.test_file_path)
            preprocessor = self.get_data_transformer_object()

            #training dataframe
            logging.info("Check1")
            input_feature_train_df = train_df.drop(columns = ["RUL"], axis=1)
            target_feature_train_df = train_df["RUL"]
            target_feature_train_df = target_feature_train_df.to_frame()
            logging.info("Check2")
            
            #testing dataframe
            logging.info("Check3")
            input_feature_test_df = test_df.drop(columns=["RUL"], axis=1)
            target_feature_test_df = test_df["RUL"]
            target_feature_test_df = target_feature_test_df.to_frame()
            logging.info("Check4")

            minmaxscaler = MinMaxScaler()
            preprocessor_object = minmaxscaler.fit(input_feature_train_df)
            logging.info("Check4_1")
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_train_feature = pd.DataFrame(transformed_input_train_feature)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            transformed_input_test_feature = pd.DataFrame(transformed_input_test_feature)
            logging.info("Check5")

            #concat input and target data
            index_names = ['unit_number', 'time_cycles']
            setting_names = ['setting_1', 'setting_2', 'setting_3']
            sensor_names = ['Fan inlet temperature', 'LPC outlet temperature', 'HPC outlet temperature', 'LPT outlet temperature', 
            'Fan inlet Pressure', 'bypass-duct pressure', 'HPC outlet pressure', 'Physical fan speed', 'Physical core speed', 'Engine pressure ratio', 'HPC outlet Static pressure',
            'Ratio of fuel flow to Ps30', 'Corrected fan speed', 'Corrected core speed', 'Bypass Ratio', 'Burner fuel-air ratio', 'Bleed Enthalpy', 'Required fan speed', 'Required fan conversion speed',
            'High-pressure turbines Cool air flow', 'Low-pressure turbines Cool air flow', 'RUL']
            col_names = index_names + setting_names + sensor_names 
            final_train_df = pd.concat([transformed_input_train_feature, target_feature_train_df], axis=1, names=col_names)
            final_test_df = pd.concat([transformed_input_test_feature, target_feature_test_df], axis=1, names=col_names)
            #logging.info(final_train_df.head(2))
            logging.info("Check6")

            #save train and test dataframe to csv files  
            save_dataframe_to_csv( self.data_transformation_config.transformed_train_file_path, df=final_train_df)
            save_dataframe_to_csv( self.data_transformation_config.transformed_test_file_path, df=final_test_df)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            logging.info("Check7")

            #preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)
