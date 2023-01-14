from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
import sys
import os
from census.config import mongo_client

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
