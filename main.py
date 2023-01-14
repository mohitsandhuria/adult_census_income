from census.exception import CensusException
from census.logger import logging
import sys,os
from census import utils
from census.entity import configuration_entity
from census.components.data_ingestion import DataIngestion


class start_training_pipeline:
     try:
          #Data Ingestion
          training_pipeline_config=configuration_entity.TrainingPipelineConfig()
          data_ingestion_config=configuration_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
     except Exception as e:
          raise CensusException(e,sys)