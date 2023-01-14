from census.exception import CensusException
from census.logger import logging
import os,sys
from dataclasses import dataclass
import pymongo

@dataclass
class environment_variables:
    mongo_db_url=os.getenv("MONGO_DB_URL")


env_var=environment_variables()
mongo_client=pymongo.MongoClient(env_var.mongo_db_url)

DATABASE_NAME="census"
COLLECTION_NAME="income"