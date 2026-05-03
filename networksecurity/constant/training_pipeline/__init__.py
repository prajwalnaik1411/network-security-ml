# Central control room for the pipeline
# All constants are defined here to keep the pipeline clean and configurable

import os      # For file path handling (os.path.join)
import sys     # For exception handling (traceback info)
import numpy as np  # Numerical operations (used in imputer configs)
import pandas as pd  # Data handling (not directly used here, but fine to keep)



# GENERAL PIPELINE CONSTANTS
TARGET_COLUMN = "Result"              # Target variable for model
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"       # Root folder for all pipeline outputs
FILE_NAME: str = "phishingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")  # Schema definition file

SAVED_MODEL_DIR = os.path.join("saved_models")  # Final saved models directory
MODEL_FILE_NAME = "model.pkl"


# DATA INGESTION CONSTANTS

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"   # MongoDB collection name
DATA_INGESTION_DATABASE_NAME: str = "Prajwal_naik"    # MongoDB database name

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Raw data storage
DATA_INGESTION_INGESTED_DIR: str = "ingested"            # Train/test split storage

DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2       # 80% train, 20% test


# DATA VALIDATION CONSTANTS

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"    # Clean data
DATA_VALIDATION_INVALID_DIR: str = "invalid"    # Rejected data

DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"  # Used later in transformation


# DATA TRANSFORMATION CONSTANTS

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"          # .npy files
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object" # preprocessor.pkl

# KNN Imputer configuration
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,   # Value to replace
    "n_neighbors": 3,           # Number of neighbors
    "weights": "uniform",       # Equal weight for neighbors
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"


# MODEL TRAINER CONSTANTS

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"

MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"  # Saved model name

MODEL_TRAINER_EXPECTED_SCORE: float = 0.6            # Minimum acceptable accuracy
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05  # Acceptable gap


# CLOUD / STORAGE

TRAINING_BUCKET_NAME = "networksecurity"  # Bucket for storing artifacts/models