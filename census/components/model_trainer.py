from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from sklearn.ensemble import RandomForestRegressor

class ModelTrainer:
    def __init__(self,model_trainer_config:configuration_entity.ModelTrainerConfig,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CensusException(e,sys)

    def train_model(self,x,y):
        try:
            random_forest=RandomForestRegressor()
            random_forest.fit(x,y)
            return random_forest
        except Exception as e:
            raise CensusException(e,sys)

    def initiate_model_training(self,):
        try:
            pass
        except Exception as e:
            raise CensusException(e,sys)
