from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.config import TARGET_COLUMN
import os,sys
from typing import Optional
import pandas as pd
import numpy as np
from sensor import utils
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler


class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                data_ingestion_artifect:artifact_entity.DataIngestionArtifact):
        
                try:
                    self.data_transformation_config=data_transformation_config
                    self.data_ingestion_artifect=data_ingestion_artifect

                except Exception as e:
                    raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler =  RobustScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return pipeline
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            train_df=pd.read_csv(self.data_ingestion_artifect.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifect.test_file_path)

            # Selecting Input feature for Training and Test Data
            input_features_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_features_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            # O/P or Target feature for Training and Test Data
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
             
            label_encoder = LabelEncoder() 
            label_encoder.fit(target_feature_train_df)

            # Transformation on target Column
            target_feature_train_array = label_encoder.transform(target_feature_train_df)
            target_feature_test_array = label_encoder.transform(target_feature_test_df)

            transformation_pipline = DataTransformation.get_data_transformer_object()
            transformation_pipline.fit(input_features_train_df)
            
            #transforming input features
            input_features_train_array = transformation_pipline.transform(input_features_train_df)
            input_features_test_array = transformation_pipline.transform(input_features_test_df)

            smt = SMOTETomek() # sampling_strategy="minority" showing error so make it auto
            logging.info(f"Before Resampling in training set input:{input_features_train_array.shape} Target:{target_feature_train_array.shape}")
            
            input_features_train_array,target_feature_train_array=smt.fit_resample(input_features_train_array,target_feature_train_array)
            
            logging.info(f"After Resampling in training set input:{input_features_train_array.shape} Target:{target_feature_train_array.shape}")
            logging.info(f"Before Resampling in training set input:{input_features_test_array.shape} Target{target_feature_test_array.shape}")
            input_features_test_array,target_feature_test_array=smt.fit_resample(input_features_test_array,target_feature_test_array)
            logging.info(f"After Resampling in training set input:{input_features_test_array.shape} Target{target_feature_test_array.shape}")

            # Target Encoder
            # Combine for train and test array
            train_arr = np.c_[input_features_train_array,target_feature_train_array]
            test_arr = np.c_[input_features_test_array,target_feature_test_array]

            # Save Numpy Array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_test_path, array=test_arr)

            # Save Tranformation object or Transformation Pipline
            utils.save_object(file_path=self.data_transformation_config.transformation_object_path, 
                                 obj=transformation_pipline)

            # Save target Encoder 
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, 
                                          obj=label_encoder)  

            data_transformation_artifect = artifact_entity.DataTransformationArtifact(
                transformation_object_path=self.data_transformation_config.transformation_object_path, 
                transform_train_path=self.data_transformation_config.transform_train_path, 
                transform_test_path=self.data_transformation_config.transform_test_path, 
                target_encoder_path=self.data_transformation_config.target_encoder_path)

            logging.info(f"Data Tranformation Object") 
            return data_transformation_artifect   

        except Exception as e:
            raise SensorException(e, sys)
        
        




