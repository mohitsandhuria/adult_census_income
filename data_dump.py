import pymongo
import pandas as pd
import json

DATA_FILE_PATH="adult_census.csv"
client=pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH="adult_census.csv"
DATABASE_NAME="census"
COLLECTION_NAME="income"

if __name__=='__main__':

    df=pd.read_csv(DATA_FILE_PATH,
    names=['age',"workclass","fnlwgt","education",
    "education-num","marital-status","occupation","relationship","race","sex",
    "capital-gain","capital-loss","hours-per-week","native-country","salary"])

    print("Rows and Columns: ",df.shape)
    # convert the records to json to dump the data in MongoDB

    df.reset_index(drop=True,inplace=True)

    json_records=list(json.loads(df.T.to_json()).values())
    print(json_records[0])

    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)

