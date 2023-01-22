from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from census.config import TARGET_COLUMN
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import LabelEncoder


class DataTransformation:
    def __init__(self,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,data_transformation_config:configuration_entity.DataTransformationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise CensusException(e, sys)

        except Exception as e:
            raise CensusException(e, sys)
    @classmethod
    def get_data_transformed(cls):
        try:
            simple_imputation=SimpleImputer(strategy='most_frequent')
            mode_pipeline = Pipeline(steps=[('imputer', simple_imputation)])
            return mode_pipeline
        except Exception as e:
            raise CensusException(e, sys)

    def initiate_data_transformation(self,):
        try:
            #import the data from data ingestion artifact
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)


            labler={}
            num_cols=[var for var in train_df.columns if train_df[var].dtype!='O']
            cat_cols=[var for var in train_df.columns if train_df[var].dtype=='O']
            for i in cat_cols:
                le=LabelEncoder()
                le=le.fit(train_df[i])
                train_df[i]=le.transform(train_df[i])
                test_df[i]=le.transform(test_df[i])
                labler[i]=le

            #selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            #selecting target feature for train and test dataframe
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_test_df=test_df[TARGET_COLUMN]

            rs=RobustScaler()
            rs.fit(input_feature_train_df[num_cols])
            input_feature_train_df[num_cols]=rs.transform(input_feature_train_df[num_cols])
            input_feature_test_df[num_cols]=rs.transform(input_feature_test_df[num_cols])

            transformation_pipeline = DataTransformation.get_data_transformed()
            transformation_pipeline.fit(input_feature_train_df)
            

            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            smt=SMOTETomek(random_state=42,sampling_strategy='minority')

            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_df.shape}")
            input_feature_train_arr, target_feature_train_df = smt.fit_resample(input_feature_train_arr, target_feature_train_df)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_df.shape}")

            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_df.shape}")
            input_feature_test_arr, target_feature_test_df = smt.fit_resample(input_feature_test_arr, target_feature_test_df)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_df.shape}")

            train_arr=np.c_[input_feature_train_arr, target_feature_train_df]
            test_arr=np.c_[input_feature_test_arr, target_feature_test_df]

            utils.save_numpy_array_data(file_path=self.data_transformation_config.trained_file_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.test_file_path, array=test_arr)

            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.encoder_path, obj=labler)

            data_transformation_artifact=artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.data_transformation_dir,
                trained_file_path=self.data_transformation_config.trained_file_path, 
                test_file_path=self.data_transformation_config.test_file_path, 
                encoder_path=self.data_transformation_config.encoder_path)

            return data_transformation_artifact
        except Exception as e:
            raise CensusException(e, sys)