import argparse
import os
from typing import Callable
import warnings
import numpy as np

import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings(action='ignore', category=DataConversionWarning)


def load_dataset(input_data_path) -> pd.DataFrame:
    print('Carregando dataset {}'.format(input_data_path))
    df = pd.read_csv(input_data_path)
    return df


def clear_fn(df: pd.DataFrame) -> pd.DataFrame:
    print('Selecionando colunas que serão utilizadas {}')
    df = df[["target_fg","target_og","ebc","srm","ph","ibu"]]

    print('Removendo dados ausentes e duplicados')
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def save_dataset_processed(X_train, X_test, y_train, y_test):
    print('Shape do dataset de treino após do preprocessamento: {}'.format(X_train.shape))
    print('Shape do dataset de teste após do preprocessamento: {}'.format(X_test.shape))

    train_features_output_path = os.path.join(f'{base_dir}/train', 'train_features.csv')
    train_labels_output_path = os.path.join(f'{base_dir}/train', 'train_labels.csv')

    test_features_output_path = os.path.join(f'{base_dir}/test', 'test_features.csv')
    test_labels_output_path = os.path.join(f'{base_dir}/test', 'test_labels.csv')

    print('Salvando features de treino em {}'.format(train_features_output_path))
    pd.DataFrame(X_train).to_csv(train_features_output_path, header=False, index=False)

    print('Salvando features de teste em {}'.format(test_features_output_path))
    pd.DataFrame(X_test).to_csv(test_features_output_path, header=False, index=False)

    print('Salvando labels de treino em {}'.format(train_labels_output_path))
    y_train.to_csv(train_labels_output_path, header=False, index=False)

    print('Salvando labels de treino em {}'.format(test_labels_output_path))
    y_test.to_csv(test_labels_output_path, header=False, index=False)



def preprocess_fn(df: pd.DataFrame,split_ratio: float) -> tuple[np.array, np.array, np.array, np.array]:
    print('Separando dados em treino e test em {}'.format(split_ratio))
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('ibu', axis=1),
        df['ibu'],
        test_size=split_ratio)

    print('Realializando preprocessamento e feature engineering')
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return (X_train, X_test, y_train, y_test)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-test-split-ratio', type=float, default=0.3)

    args, _ = parser.parse_known_args()
    print('Recebendo paramêtros {}'.format(args))

    base_dir='/opt/ml/processing'
    df: pd.DataFrame = load_dataset(
            path=os.path.join(f'{base_dir}/input', 'dataset.csv')
        ).pipe(clear_fn)

    X_train, X_test, y_train, y_test = preprocess_fn(df, split_ratio=args.train_test_split_ratio)

    save_dataset_processed(
        X_train = X_train,
        X_test = X_train, 
        y_train = y_train, 
        y_test = y_test
    )
