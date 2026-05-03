from networksecurity.exception.exception import NetworkSecurityException  # Custom exception for structured error handling
from networksecurity.logging.logger import logging  # Custom logging utility for tracking pipeline steps

# Configuration classes
from networksecurity.entity.config_entity import DataIngestionConfig  # Holds DB info, paths, split ratio
from networksecurity.entity.artifact_entity import DataIngestionArtifact  # Stores output paths (train/test)

import os        # File and directory operations
import sys       # Exception handling (traceback info)
import numpy as np   # Numerical operations (handling NaN)
import pandas as pd  # Data manipulation (DataFrame)
import pymongo       # MongoDB client
from typing import List  # Type hinting (optional here)
from sklearn.model_selection import train_test_split  # Train-test splitting
from dotenv import load_dotenv  # Load environment variables from .env

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # MongoDB connection string


class DataIngestion:  # Handles full data ingestion pipeline
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config  # Store config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB and return as DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name  # DB name
            collection_name = self.data_ingestion_config.collection_name  # Collection name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)  # Connect to MongoDB
            collection = self.mongo_client[database_name][collection_name]  # Access collection

            df = pd.DataFrame(list(collection.find()))  # Convert documents → DataFrame

            if "_id" in df.columns.to_list():  # Remove MongoDB default ID
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)  # Replace 'na' with NaN

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Proper exception propagation

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """
        Save raw data into feature store (CSV)
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)  # Get directory
            os.makedirs(dir_path, exist_ok=True)  # Create if not exists

            dataframe.to_csv(feature_store_file_path, index=False, header=True)  # Save CSV

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Split dataset into training and testing sets
        """
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train-test split on dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test files")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info("Train and test files exported successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """
        Execute full data ingestion pipeline
        """
        try:
            dataframe = self.export_collection_as_dataframe()  # Step 1: Load data
            dataframe = self.export_data_into_feature_store(dataframe)  # Step 2: Save raw data
            self.split_data_as_train_test(dataframe)  # Step 3: Split data

            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)