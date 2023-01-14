from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    pass

@dataclass
class ModelTrainerArtifact:
    pass

@dataclass
class ModelEvaluationArtifact:
    pass

@dataclass
class ModelPusherArtifact:
    pass