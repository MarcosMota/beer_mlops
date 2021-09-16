
import json
import os
import tarfile
import pandas as pd
import joblib

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

if __name__ == "__main__":
    model_path = os.path.join("/opt/ml/processing/model", "model.tar.gz")

    print("Extraindo do modelo de : {}".format(model_path))
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")
    print("Carregando modelo")
    model = joblib.load("model.joblib")

    print("Carregando dataset de teste")
    test_features_data = os.path.join("/opt/ml/processing/test", "test_features.csv")
    test_labels_data = os.path.join("/opt/ml/processing/test", "test_labels.csv")

    X_test = pd.read_csv(test_features_data, header=None)
    y_test = pd.read_csv(test_labels_data, header=None)
    predictions = model.predict(X_test)

    print("Avaliando modelo")
    report_dict = {}
    report_dict["mse"] = mean_squared_error(y_test, predictions)
    report_dict["r2"] = r2_score(y_test, predictions)
    
    print(f"MSE: {report_dict['mse']} R2: {report_dict['r2']}")

    evaluation_output_path = os.path.join("/opt/ml/processing/evaluation", "evaluation.json")
    print("Salvando avaliação em {}".format(evaluation_output_path))

    with open(evaluation_output_path, "w") as f:
        f.write(json.dumps(report_dict))