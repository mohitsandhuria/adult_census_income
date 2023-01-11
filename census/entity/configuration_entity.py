from census.exception import SensorException
import os,sys


class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            SensorException(e, sys)

class DataIngestionConfig:
    pass

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