from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class RegressionEvaluationArtifact:
    rmse:float
    r2score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: RegressionEvaluationArtifact
    test_metric_artifact: RegressionEvaluationArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    train_model_metric_artifact: RegressionEvaluationArtifact
    best_model_metric_artifact: RegressionEvaluationArtifact

@dataclass
class ModelPusherArtifact:
    model_file_path: str
    saved_model_path: str
