from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
import sys
import os
from census.config import mongo_client
import yaml
import dill

def get_collection_dataframe(database_name,collection_name):

    try:
        logging.info(f"Reading Data from Database- {database_name} and Collection- {collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Columns in Database {df.columns}")
        if '_id' in df.columns:
            logging.info(f"deleting _id from dataframe columns")
            df.drop('_id',axis=1,inplace=True)
        logging.info(f"Number of rows and columns in dataframe {df.shape}")
        return df
    except Exception as e:
        raise CensusException(e, sys)

def write_to_yaml(file_path,data):
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)

        with open(file_path,'w') as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise CensusException(e, sys)

def convert_column_to_float(df,exclude_column):
    try:
        for column in df.columns:
            if column not in exclude_column:
                df[column]=df[column].astype('float')
        return df

    except Exception as e:
        raise CensusException(e, sys)

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CensusException(e,sys)

def save_object(file_path: str, obj: object):
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise CensusException(e, sys) from e