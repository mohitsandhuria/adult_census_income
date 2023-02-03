from census.exception import CensusException
import os,sys
from datetime import datetime

FILE_NAME = "census.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
TRANSFORMER_FILE_PATH="transformer.pkl"
ENCODER_OBJECT_FILE_PATH="encoder.pkl"
MODEL_FILE_NAME="model_trainer.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise CensusException(e, sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="census"
            self.collection_name="income"
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size=0.3
        except Exception as e:
            raise CensusException(e, sys)
        
    def to_dict(self,):
        try:
            return self.__dict__
        except Exception as e:
            raise CensusException(e, sys)

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path=os.path.join(self.data_validation_dir,"report.yaml")
            self.missing_threshold:float=0.2
            self.base_file_path="adult_census.csv"
        except Exception as e:
            raise CensusException(e, sys)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
            self.transform_object_path=os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_FILE_PATH)
            self.trained_file_path=os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace(".csv", ".npz"))
            self.test_file_path=os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace(".csv", ".npz"))
            self.encoder_path=os.path.join(self.data_transformation_dir,"encoder",ENCODER_OBJECT_FILE_PATH)
        except Exception as e:
            raise CensusException(e, sys)


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
            self.model_path=os.path.join(self.model_trainer_dir,"model_path",MODEL_FILE_NAME)
            self.expected_score=0.7
            self.overfitting_threshold = 0.2
        except Exception as e:
            raise CensusException(e, sys)
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold=0.01

class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_pusher_dir=os.path.join(training_pipeline_config.artifact_dir,"model_pusher")
            self.saved_model_dir=os.path.join("saved_models")
            self.pusher_model_dir=os.path.join(self.model_pusher_dir,"saved_models")
            self.pusher_model_path=os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
            self.pusher_transformer_path=os.path.join(self.pusher_model_dir,TRANSFORMER_FILE_PATH)
            self.pusher_targer_encoder_path=os.path.join(self.pusher_model_dir,ENCODER_OBJECT_FILE_PATH)
        except Exception as e:
            raise CensusException(e,sys)
            