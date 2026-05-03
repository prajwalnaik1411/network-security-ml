from dataclasses import dataclass   # Automatically creates:
                                    # __init__
                                    # __repr__
                                    # cleaner objects


@dataclass
class DataIngestionArtifact:        # Stores output of Data Ingestion step:
    trained_file_path: str          # Path to training data
    test_file_path: str             # Path to testing data


@dataclass
class DataValidationArtifact:       # Output of Data Validation step
    validation_status: bool         # Whether validation passed or not
                                    # True  → good data
                                    # False → issue found
    valid_train_file_path: str      # Path to clean/valid training data
    valid_test_file_path: str       # Path to clean/valid testing data
    invalid_train_file_path: str    # Path to bad training data
    invalid_test_file_path: str     # Path to bad testing data
    drift_report_file_path: str     # Path to data drift report


@dataclass
class DataTransformationArtifact:  # Output of Data Transformation step
    transformed_object_file_path: str   # Path to preprocessing object (scaler, encoder, etc.)
    transformed_train_file_path: str    # Path to transformed training data (usually .npy)
    transformed_test_file_path: str     # Path to transformed testing data


@dataclass
class ClassificationMetricArtifact:    # Stores model performance metrics
    f1_score: float                   # Balance between precision & recall
    precision_score: float            # How many predicted positives are correct
    recall_score: float               # How many actual positives are captured


@dataclass
class ModelTrainerArtifact:           # Output of Model Training step
    trained_model_file_path: str      # Path to saved model (model.pkl)
    train_metric_artifact: ClassificationMetricArtifact  # Metrics on training data
    test_metric_artifact: ClassificationMetricArtifact   # Metrics on test data