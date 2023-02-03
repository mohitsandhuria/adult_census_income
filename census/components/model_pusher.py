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



class ModelPusher:
    def __init__(self,model_pusher_config:configuration_entity.ModelPusherConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise CensusException(e,sys)

    def initiate_model_pusher(self):
        try:
            logging.info("loading transformer model and encoder")
            transformer=utils.load_objects(file_path=self.data_transformation_artifact.transform_object_path)
            model=utils.load_objects(file_path=self.model_trainer_artifact.model_path)
            encoder=utils.load_objects(file_path=self.data_transformation_artifact.encoder_path)

            logging.info("saving model into model pusher dir")
            utils.save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            utils.save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            utils.save_object(file_path=self.model_pusher_config.pusher_targer_encoder_path, obj=encoder)

            logging.info("saving model into saved model dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            encoder_path=self.model_resolver.get_latest_save_encoder_path()
            model_path=self.model_resolver.get_latest_save_model_path()


            utils.save_object(file_path=transformer_path, obj=transformer)
            utils.save_object(file_path=encoder_path, obj=encoder)
            utils.save_object(file_path=model_path, obj=model)

            model_pusher_artifact=artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir, 
                                    saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise CensusException(e, sys)