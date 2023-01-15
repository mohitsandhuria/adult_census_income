from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,data_validation_config:configuration_entity.DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} Data Validation {'>>'*20}")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.validation_error=dict()
        except Exception as e:
            raise CensusException(e,sys)
    
    def drop_missing_values_columns(self,df,report_key_name):
        '''This function will drop the column which contains missing values more than specified threshold
        df : pandas Accepts dataframe
        threshhold: percentage criteria to drop a column
        ===============================================================================================
        Returns pandas dataframe if atleast one column is having the 
        '''

        try:
            threshold=self.data_validation_config.missing_threshold
            null_report=df.isnull().sum()/df.shape[0]

            drop_column_names=null_report[null_report>threshold].index
            self.validation_error[report_key_name]=list(drop_column_names)
            logging.info(f"dropping column from dataframe having more null values with respect to threshold")
            logging.info(f"Number of columns to drop: {len(list(drop_column_names))} columns to drop {drop_column_names} ")
            df.drop(list(drop_column_names),axis=1,inplace=True)
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise CensusException(e, sys)

    def is_required_column_exists(self,base_df,current_df,report_key_name):
        try:
            missing_column=[]
            base_columns=base_df.columns
            current_columns=current_df.columns
            
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    missing_column.append(base_column)
            
            if len(missing_column)>0:
                self.validation_error[report_key_name]=missing_column
                return False
            return True

        except Exception as e:
            raise CensusException(e, sys)
        
    def data_drift(self,current_df,base_df,report_key_name):
        try:
            drift_report=dict()

            base_columns=base_df.columns
            current_columns=current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)
            
                if same_distribution.pvalue>0.05:
                    drift_report={"p_value":float(same_distribution.pvalue),"same_distribution":True}
                else:
                    drift_report={"p_value":float(same_distribution.pvalue),"same_distribution":False}
                self.validation_error=drift_report
        except Exception as e:
            raise CensusException(e,sys)


    def initiate_data_validation(self):
        try:
            logging.info(f"Reading base file to form data frame")
            base_df=pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)
            logging.info(f"Reading train and test file from artefacts")
            cat_cols=[var for var in base_df.columns if base_df[var].dtype=='O']
            num_cols=[var for var in base_df.columns if base_df[var].dtype!='O']
            for i in cat_cols:
                base_df[i]=base_df[i].str.strip().map(lambda x: np.nan if x=="?" else x)
            logging.info("dropping null values columns from base dataset")
            base_df=self.drop_missing_values_columns(df=base_df, report_key_name="missing_values_in_base_dataset")

            logging.info(f"Reading Train dataset")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading Train dataset")
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("dropping null values columns from train dataset")
            train_df=self.drop_missing_values_columns(df=train_df, report_key_name="missing_values_in_train_dataset")
            logging.info("dropping null values columns from test dataset")
            test_df=self.drop_missing_values_columns(df=test_df, report_key_name="missing_values_in_test_dataset")

            exclude_column=cat_cols
            base_df=utils.convert_column_to_float(df=base_df, exclude_column=exclude_column)
            train_df=utils.convert_column_to_float(df=train_df, exclude_column=exclude_column)
            test_df=utils.convert_column_to_float(df=test_df, exclude_column=exclude_column)

            base_df=base_df[num_cols]
            train_df=train_df[num_cols]
            test_df=test_df[num_cols]


            logging.info("Checking if required column exists in train and test df")

            train_df_column_status=self.is_required_column_exists(base_df=base_df, current_df=train_df, report_key_name="missing_columns_within_train_dataset")
            test_df_column_status=self.is_required_column_exists(base_df=base_df, current_df=test_df, report_key_name="missing_columns_within_train_dataset")

            if train_df_column_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(current_df=train_df, base_df=base_df, report_key_name="data_drift_within_train_dataset")
            if test_df_column_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(current_df=test_df, base_df=base_df, report_key_name="data_drift_within_test_dataset")
            
            logging.info("Writting report to yml")
            utils.write_to_yaml(file_path=self.data_validation_config.report_file_path, data=self.validation_error)

            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CensusException(e, sys)    



