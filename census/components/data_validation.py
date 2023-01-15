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
            drift_report=dict()

            base_columns=base_df.columns
            current_columns=current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)
            
                if same_distribution.p_value>0.5:
                    drift_report




