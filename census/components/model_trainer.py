from census.exception import CensusException
from census.logger import logging
import pandas as pd
import numpy as np
from census.entity import configuration_entity
from census.entity import artifact_entity
from census import utils
import os
import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

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
            model=RandomForestClassifier()
            model.fit(x,y)
            return model
        except Exception as e:
            raise CensusException(e,sys)

    def initiate_model_training(self,):
        try:
            logging.info("Loading training and test array after transformation")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.trained_file_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.test_file_path)

            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Training the model")
            model=self.train_model(x=x_train, y=y_train)

            logging.info("f1 trained data set score")
            yhat_train=model.predict(x_train).round()
            f1_train_score=f1_score(y_train,yhat_train)

            logging.info("f1 test data set score")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_test,yhat_test)
            logging.info(f"Checking if our model is underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception("model accuracy is not good as it is not able to give good accuracy as \
                expected: {self.model_trainer_config.expected_score} model accuracy is {f1_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff=abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")
            
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            model_trainer_artifact=artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_Score=f1_test_score)

            return model_trainer_artifact

        except Exception as e:
            raise CensusException(e,sys)
