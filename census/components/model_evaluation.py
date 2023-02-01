from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from sklearn.metrics import f1_score
from census.config import TARGET_COLUMN


class ModelEvaluation:
    def __init__(self,model_eval_config:configuration_entity.ModelEvaluationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):

        self.model_eval_config=model_eval_config
        self.data_ingestion_artifact=data_ingestion_artifact
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_artifact=model_trainer_artifact

    def initiate_model_evaluation(self):
        try:
        #if saved model folder has model the we will compare 
            #which model is best trained or the model from saved model folder
            logging.info("if saved model folder has model the we will compare "
            "which model is best trained or the model from saved model folder")
        except Exception as e:
            raise CensusException(e, sys)