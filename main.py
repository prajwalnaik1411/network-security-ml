from networksecurity.components.data_ingestion import DataIngestion#This class is responsible for collecting data
from networksecurity.components.data_validation import DataValidation#Used to check data quality (missing values, schema, etc.)
from networksecurity.components.data_transformation import DataTransformation#Used to clean + preprocess data (scaling, encoding, etc.)
from networksecurity.exception.exception import NetworkSecurityException#Used to handle errors in a clean structured way
from networksecurity.logging.logger import logging  #Used instead of print → better for debugging & tracking pipeline
from networksecurity.entity.config_entity import (  #They store settings like:
                                                    #file paths
                                                    #DB URLs
                                                    #parameter
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.components.model_trainer import ModelTrainer  # Trains ML model
from networksecurity.entity.config_entity import ModelTrainerConfig#


import sys  # Used for exception handling (debugging info)

if __name__ == "__main__":  #This ensures the script runs only when executed directly
                            # (not when imported)
    try:
        # STEP 1: CONFIGURATION
        trainingpipelineconfig = TrainingPipelineConfig()#Creates global configuration object

        # STEP 2: DATA INGESTION
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)   #Create ingestion config using pipeline config
        data_ingestion = DataIngestion(dataingestionconfig)                 # Create ingestion object
        logging.info("Initiate the data ingestion")                         # Log message (instead of print)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()    #Runs ingestion process,Returns artifact (output info like file paths)
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        # STEP 3: DATA VALIDATION
        data_validation_config = DataValidationConfig(trainingpipelineconfig)#Create validation config
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()#Validates data,Returns validation result
        logging.info("data Validation Completed")
        print(data_validation_artifact)

        # STEP 4: DATA TRANSFORMATION
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)#Create transformation config
        logging.info("data Transformation started")
        data_transformation = DataTransformation(  # Uses validated data
            data_validation_artifact, data_transformation_config
        )
        data_transformation_artifact = (#Cleans + transforms data,Returns transformed dataset
            data_transformation.initiate_data_transformation()
        )
        print(data_transformation_artifact)
        logging.info("data Transformation completed")

        # STEP 5: MODEL TRAINING
        logging.info("Model Training sstared")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)#Create training config
        model_trainer = ModelTrainer(   #Pass:
                                        #config
                                        #transformed data
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()#Train model
        # Returns trained model + metrics

        logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e, sys)


# FLOW:
# Config → Ingestion → Validation → Transformation → Training