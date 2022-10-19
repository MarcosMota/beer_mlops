
import json
import os
import tarfile
from typing import Any, Dict
import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def load_model(path: str = "/opt/ml/processing/model") -> Any:
    model_path = os.path.join(path, "model.tar.gz")

    print("Extraindo do modelo de : {}".format(model_path))
    with tarfile.open(model_path) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=".")
    print("Carregando modelo")
    model = joblib.load("model.joblib")
    return model

def load_dataset_test(path: str = "/opt/ml/processing/test") -> tuple[pd.DataFrame, pd.DataFrame]:
    print("Carregando dataset de teste")
    test_features_data = os.path.join("/opt/ml/processing/test", "test_features.csv")
    test_labels_data = os.path.join("/opt/ml/processing/test", "test_labels.csv")

    X_test = pd.read_csv(test_features_data, header=None)
    y_test = pd.read_csv(test_labels_data, header=None)
    return (X_test, y_test)

def save_report(report: dict, path_output: str):
    evaluation_output_path = os.path.join(path_output, "evaluation.json")
    print("Salvando avaliação em {}".format(evaluation_output_path))

    with open(evaluation_output_path, "w") as f:
        f.write(json.dumps(report))

def evaluate(y_test: np.array, predictions: np.array) -> Dict:
    print("Avaliando modelo")
    report_dict = {}
    report_dict["mse"] = mean_squared_error(y_test, predictions)
    report_dict["r2"] = r2_score(y_test, predictions)
    
    print(f"MSE: {report_dict['mse']} R2: {report_dict['r2']}")

    return report_dict 

if __name__ == "__main__":
    
    path_model = "/opt/ml/processing/model"
    path_test = "/opt/ml/processing/test"
    path_output = "/opt/ml/processing/evaluation"
    
    model = load_model(path_model)

    X_test, y_test = load_dataset_test(path_test)
    predictions = model.predict(X_test)

    report = evaluate(y_test = y_test, predictions = predictions)

    save_report(report=report, path_output=path_output)
