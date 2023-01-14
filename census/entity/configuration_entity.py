from census.exception import CensusException
import os,sys
from datetime import datetime

FILE_NAME = "census.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"


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
    pass

class DataTransformationConfig:
    pass

class ModelTrainerConfig:
    pass

class ModelEvaluationConfig:
    pass

class ModelPusherConfig:
    pass