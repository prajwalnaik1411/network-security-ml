import os  # Used to interact with environment variables (like getting values from .env)
import sys  # Helps in error handling (used in custom exception)
import json  # Used to convert data into JSON format


from dotenv import load_dotenv

# Loads variables from a .env file into the OS environment

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# Fetch MongoDB connection URL from environment variables

print(MONGO_DB_URL)  # (For debugging only — avoid printing in real projects)


import certifi

ca = certifi.where()
# 'ca' is a file path containing trusted SSL certificates


import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# networksecurity → main project folder
# exception → subfolder
# exception.py → file
# NetworkSecurityException → class inside that file


class NetworkDataExtract:

    def __init__(self):
        try:
            pass
            # Placeholder constructor (used for future initialization if needed)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
            # e → original error
            # sys → gives detailed traceback info

    def csv_to_json_convertor(self, file_path):
        # Converts CSV data into JSON (key–value format)
        try:
            data = pd.read_csv(file_path)
            # Reads CSV into a pandas DataFrame

            data.reset_index(drop=True, inplace=True)
            # drop=True → removes old index
            # inplace=True → modifies original data

            records = list(json.loads(data.T.to_json()).values())
            # data.T → transpose (rows ↔ columns)
            # to_json() → converts DataFrame to JSON string
            # json.loads(...) → converts JSON string → Python dictionary
            # .values() → extracts only values (removes keys)
            # list(...) → converts into list of records

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        # Inserts JSON records into MongoDB
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            # Connects to MongoDB using connection URL

            self.database = self.mongo_client[self.database]
            # Selects database

            self.collection = self.database[self.collection]
            # Selects collection (similar to table)

            self.collection.insert_many(self.records)
            # Inserts all records at once

            return len(self.records)
            # Returns number of inserted records

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"F:\CYBER_security_project\network_data\phisingData.csv"
    # Path to your dataset

    DATABASE = "Prajwal_naik"
    Collection = "NetworkData"

    networkobj = NetworkDataExtract()
    # Create object of class

    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    # Convert CSV → JSON

    print(records)

    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    # Insert JSON data into MongoDB

    print(no_of_records)


#  FLOW:
# CSV → Pandas → JSON → MongoDB
