from census.exception import CensusException
from census.logger import logging
import sys,os
from census import utils
from census.entity import configuration_entity
from census.components.data_ingestion import DataIngestion
from census.components.data_validation import DataValidation
from census.components.data_transformation import DataTransformation
from census.components.model_trainer import ModelTrainer
from census.components.model_evaluation import ModelEvaluation

class start_training_pipeline:
     try:
          #Data Ingestion
          training_pipeline_config=configuration_entity.TrainingPipelineConfig()
          data_ingestion_config=configuration_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
          

          #Data Validation
          data_validation_config=configuration_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
          data_validation_artifact=data_validation.initiate_data_validation()

          #Data Transformation
          data_transformation_config=configuration_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact, data_transformation_config=data_transformation_config)
          data_transformation_artifact=data_transformation.initiate_data_transformation()

          #Model Trainer
          model_trainer_config=configuration_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer=ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact=model_trainer.initiate_model_training()
          
          #model evaluation
          model_evaluation_config=configuration_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_evaluation=ModelEvaluation(model_eval_config=model_evaluation_config, data_ingestion_artifact=data_ingestion_artifact, 
          data_transformation_artifact=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)
          model_evaluation_artifact=model_evaluation.initiate_model_evaluation()

     except Exception as e:
          raise CensusException(e,sys)