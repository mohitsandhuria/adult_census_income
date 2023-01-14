from census.exception import CensusException
from census.logger import logging
import os,sys
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census.config import DATABASE_NAME,COLLECTION_NAME
from census import utils
from sklearn.model_selection import train_test_split
import os
import sys

class DataIngestion:

    def __init__(self,data_ingestion_config:configuration_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CensusException(e, sys)
    
    def initiate_data_ingestion(self):
        try:    
            logging.info("importing data from mongodb to Dataframe")
            df=utils.get_collection_dataframe(database_name=self.data_ingestion_config.database_name, 
            collection_name=self.data_ingestion_config.collection_name)
            cat_cols=[var for var in df.columns if df[var].dtype=='O']
            num_cols=[var for var in df.columns if df[var].dtype!='O']
            for i in cat_cols:
                df[i]=df[i].str.strip().map(lambda x: np.nan if x=="?" else x)
            
            logging.info("Create feature store folder if not available")

            feature_store=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store,exist_ok=True)
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            
            logging.info("split dataset into train and test set")
            
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            logging.info("Create dataset directory if not exist")

            dataset_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            logging.info("Save df to train and test file in dataset folder")

            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            data_ingestion_artifact=artifact_entity.DataIngestionArtifact(feature_store_file_path=self.data_ingestion_config.feature_store_file_path, 
            train_file_path=self.data_ingestion_config.train_file_path, 
            test_file_path=self.data_ingestion_config.test_file_path)

            return data_ingestion_artifact
        except Exception as e:
            raise CensusException(e, sys)

        