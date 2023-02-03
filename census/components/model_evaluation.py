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
from census.predictor import ModelResolver


class ModelEvaluation:
    def __init__(self,model_eval_config:configuration_entity.ModelEvaluationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):

        self.model_eval_config=model_eval_config
        self.data_ingestion_artifact=data_ingestion_artifact
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_artifact=model_trainer_artifact
        self.model_resolver=ModelResolver()

    def initiate_model_evaluation(self):
        try:
        #if saved model folder has model the we will compare 
            #which model is best trained or the model from saved model folder
            logging.info("if saved model folder has model the we will compare "
            "which model is best trained or the model from saved model folder")
            latest_dir_path=self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
                return model_eval_artifact
            
            #finding location of transformer and target encoder
            logging.info(f"finding location of transformer and encoder path")
            transformer_path=self.model_resolver.get_latest_transformer_path()
            model_path=self.model_resolver.get_latest_model_path()
            encoder_path=self.model_resolver.get_latest_encoder_path()

            logging.info("previous trained tranformer and encoder")
            transformer=utils.load_objects(file_path=transformer_path)
            model=utils.load_objects(file_path=model_path)
            encoder=utils.load_objects(file_path=encoder_path)

            logging.info("currently trained model objects")
            current_transformer=utils.load_objects(file_path=self.data_transformation_artifact.transform_object_path)
            current_target_encoder=utils.load_objects(file_path=self.data_transformation_artifact.encoder_path)
            current_model=utils.load_objects(file_path=self.model_trainer_artifact.model_path)

            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df=test_df[TARGET_COLUMN]
            cat_cols=[var for var in test_df.columns if test_df[var].dtype=='O']
            for i in cat_cols:
                test_df[i]=encoder[i].transform(test_df[i])
            y_true=test_df[TARGET_COLUMN]


            input_feature_name=list(transformer.feature_names_in_)
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred=model.predict(input_arr)
            previous_model_score=f1_score(y_true,y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true =current_target_encoder[TARGET_COLUMN].transform(target_df)
            current_model_score=f1_score(y_true,y_pred)

            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")
                
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact

        except Exception as e:
            raise CensusException(e, sys)