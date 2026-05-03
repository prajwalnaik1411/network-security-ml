from datetime import (
    datetime,
)  # Helps create unique folder names (super important in pipelines)
import os  # file paths

# directory creation
# #Example: os.path.join()
from networksecurity.constant import training_pipeline  # Imports constants like:

# folder names
# file names
# DB configs

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:  # This is the main controller config
    def __init__(self, timestamp=datetime.now()):  # Default timestamp = current time
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")  # Converts time → string
        # Example: 05_02_2026_18_30_45
        self.pipeline_name = training_pipeline.PIPELINE_NAME  # Name of pipeline
        self.artifact_name = (
            training_pipeline.ARTIFACT_DIR
        )  # Base folder name (like "artifacts")
        self.artifact_dir = os.path.join(
            self.artifact_name, timestamp
        )  # artifacts/05_02_2026_18_30_45/
        self.model_dir = os.path.join(
            "final_model"
        )  # Folder where final model is stored
        self.timestamp: str = timestamp  # Store timestamp for reuse


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )
        self.feature_store_file_path: str = os.path.join(  # Stores raw collected data
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME,
        )
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME,
        )
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME,
        )
        self.train_test_split_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )
        self.collection_name: str = (
            training_pipeline.DATA_INGESTION_COLLECTION_NAME
        )  # MongoDB config
        # Where data is coming from
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:  # Config for validation stage
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = (
            os.path.join(  # Creates validation folder:artifacts/<timestamp>/data_validation/
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_VALIDATION_DIR_NAME,
            )
        )
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir: str = os.path.join(  # Folder for bad/invalid data
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path: str = (
            os.path.join(  # Path for validated training data
                self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME
            )
        )
        self.valid_test_file_path: str = os.path.join(  # Path for validated test data
            self.valid_data_dir, training_pipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path: str = os.path.join(  # Path for bad training data
            self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path: str = os.path.join(  # Path for bad test data
            self.invalid_data_dir, training_pipeline.TEST_FILE_NAME
        )
        self.drift_report_file_path: str = os.path.join(  # Path for data drift report
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )
        """data_validation/
                        ├── valid/
                        │     ├── train.csv
                        │     └── test.csv
                        ├── invalid/
                        │     ├── train.csv
                        │     └── test.csv
                        └── drift/
                                └── report.yaml
                                """


class DataTransformationConfig:  # Config for data preprocessing stage
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
        )
        self.transformed_train_file_path: str = os.path.join(  # train.csv → train.npy
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_object_file_path: str = (
            os.path.join(  # Stores preprocessing object:
                self.data_transformation_dir,
                training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
            )
        )
        """data_transformation/
                ├── transformed_data/
                │     ├── train.npy
                │     └── test.npy
                └── transformed_object/
                        └── preprocessor.pkl
        """


class ModelTrainerConfig:  # Config for model training stage
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = (
            os.path.join(  # Creates folder for training outputs,This folder will store:trained model,evaluation results,reports.
                training_pipeline_config.artifact_dir,
                training_pipeline.MODEL_TRAINER_DIR_NAME,
            )
        )
        self.trained_model_file_path: str = (
            os.path.join(  # Full path where model is saved
                self.model_trainer_dir,
                training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                training_pipeline.MODEL_FILE_NAME,
            )
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = (
            training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        )
        """model_trainer/
                    ├── trained_model/
                    │     └── model.pkl"""

        """
        Train model → Evaluate → Check accuracy & overfitting →
        ✔ Good → Save model
        ❌ Bad → Reject model
        """
