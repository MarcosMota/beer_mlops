import argparse
import os
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
import joblib



def load_data(training_dir: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_features_data = os.path.join(training_dir, "train_features.csv")
    train_labels_data = os.path.join(training_dir, "train_labels.csv")

    print("Carregando dados de treino e teste")
    X_train = pd.read_csv(train_features_data, header=None)
    y_train = pd.read_csv(train_labels_data, header=None)

    return (X_train, y_train)

def save_model(model_dir: str, model: BaseEstimator):

    model_output_directory = os.path.join(model_dir, "model.joblib")
    
    print("Salvando modelo em {}".format(model_output_directory))
    joblib.dump(model, model_output_directory)

def train_fn(X_train, y_train, hyperparameters:dict) -> BaseEstimator:
    model = RandomForestRegressor(
        max_depth=hyperparameters['max_depth'],
        n_estimators=hyperparameters['n_estimators'],
        random_state=hyperparameters['random_state']
    )

    print("Treinando modelo")
    model.fit(X_train, y_train)

    return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_depth', type=int, default=None)
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--random_state', type=int, default=None)
    
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--training', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    args, _ = parser.parse_known_args()
    print('Recebendo paramêtros {}'.format(args))
    hyperparameters = {
        'max_depth' : args.max_depth,
        'n_estimators' : args.n_estimators,
        'random_state' : args.random_state
    }

    X_train, y_train = load_data(args.training)

    model = train_fn(X_train, y_train, hyperparameters=hyperparameters)

    save_model(model_dir= args.model_dir, model=model)

