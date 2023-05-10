from nasa.exception import SensorException 
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import sys
from nasa.entity.artifact_entity import RegressionEvaluationArtifact


def get_evaluation_score(y_true, y_pred)->RegressionEvaluationArtifact:
    try:
        mse = mean_squared_error(y_true,y_pred)
        rmse = np.sqrt(mse)
        r2score = r2_score(y_true, y_pred)

        regression_score = RegressionEvaluationArtifact(rmse = rmse, r2score = r2score)
        return regression_score
    except Exception as e:
        raise SensorException(e, sys)