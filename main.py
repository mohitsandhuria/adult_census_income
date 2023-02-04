from census.pipeline.batch_prediction import start_batch_prediction
from census.pipeline.training_pipeline import start_training_pipeline
import sys, os
from census.logger import logging
from census.exception import CensusException

file_path="/config/workspace/adult_census.csv"

if __name__=="__main__":
     try:
          logging.info("starting batch prediction")
          output_file_name=start_batch_prediction(input_file_path=file_path)
          print(output_file_name)
     except Exception as e:
          raise CensusException(e,sys)