from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from census.predictor import ModelResolver
from census.config import TARGET_COLUMN
from datetime import datetime

PREDICTION_DIR="prediction"

def start_batch_prediction(input_file_path):
    try:
        logging.info("starting batch prediction")
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        model_resolver=ModelResolver(model_registry="saved_models")
        logging.info(f"Reading input file from {input_file_path}")
        df=pd.read_csv(input_file_path,names=['age',"workclass","fnlwgt","education",
        "education-num","marital-status","occupation","relationship","race","sex",
        "capital-gain","capital-loss","hours-per-week","native-country","salary"])
        cat_cols=[var for var in df.columns if df[var].dtype=='O']
        num_cols=[var for var in df.columns if df[var].dtype!='O']
        for i in cat_cols:
            df[i]=df[i].str.strip().map(lambda x: np.nan if x=="?" else x)

        logging.info(f"loading transformer from {model_resolver.get_latest_transformer_path()}")
        transformer=utils.load_objects(file_path=model_resolver.get_latest_transformer_path())
        logging.info(f"importing encoder from {model_resolver.get_latest_encoder_path()}")
        encoder=utils.load_objects(file_path=model_resolver.get_latest_encoder_path())
        for i in cat_cols:
            df[i]=encoder[i].transform(df[i])
        input_feature_name=list(transformer.feature_names_in_)
        input_arr=transformer.transform(df[input_feature_name])

        logging.info(f"loading model from {model_resolver.get_latest_model_path()}")
        model=utils.load_objects(file_path=model_resolver.get_latest_model_path())
        logging.info(f"input array {input_arr}")
        prediction=model.predict(input_arr)

        logging.info(f"Loading target encoder to convert predicted column to categorical")
        cat_prediction=encoder[TARGET_COLUMN].inverse_transform(prediction.astype(int))

        df['prediction']=prediction
        df['cat_prediction']=cat_prediction

        prediction_file_name=os.path.basename(input_file_path).replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        preddiction_file_path=os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(preddiction_file_path,index=False,header=True)
        return prediction_file_name
    except Exception as e:
        raise CensusException(e,sys)
