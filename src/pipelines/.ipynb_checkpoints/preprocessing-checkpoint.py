import argparse
import os
import warnings

import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings(action='ignore', category=DataConversionWarning)


def preprocess_fn(split_ratio: float, base_dir='/opt/ml/processing') -> None:
    input_data_path = os.path.join(f'{base_dir}/input', 'dataset.csv')
    print('Carregando dataset {}'.format(input_data_path))
    df = pd.read_csv(input_data_path)

    print('Selecionando colunas que serão utilizadas {}')
    df = df[["target_fg","target_og","ebc","srm","ph","ibu"]]

    print('Removendo dados ausentes e duplicados')
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    print('Separando dados em treino e test em {}'.format(split_ratio))
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('ibu', axis=1),
        df['ibu'],
        test_size=split_ratio)

    

    print('Realializando preprocessamento e feature engineering')
    scaler = StandardScaler()
    train_features = scaler.fit_transform(X_train)
    test_features = scaler.transform(X_test)
    
    

    print('Shape do dataset de treino após do preprocessamento: {}'.format(train_features.shape))
    print('Shape do dataset de teste após do preprocessamento: {}'.format(test_features.shape))

    train_features_output_path = os.path.join(f'{base_dir}/train', 'train_features.csv')
    train_labels_output_path = os.path.join(f'{base_dir}/train', 'train_labels.csv')

    test_features_output_path = os.path.join(f'{base_dir}/test', 'test_features.csv')
    test_labels_output_path = os.path.join(f'{base_dir}/test', 'test_labels.csv')

    print('Salvando features de treino em {}'.format(train_features_output_path))
    pd.DataFrame(train_features).to_csv(train_features_output_path, header=False, index=False)

    print('Salvando features de teste em {}'.format(test_features_output_path))
    pd.DataFrame(test_features).to_csv(test_features_output_path, header=False, index=False)

    print('Salvando labels de treino em {}'.format(train_labels_output_path))
    y_train.to_csv(train_labels_output_path, header=False, index=False)

    print('Salvando labels de treino em {}'.format(test_labels_output_path))
    y_test.to_csv(test_labels_output_path, header=False, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-test-split-ratio', type=float, default=0.3)

    args, _ = parser.parse_known_args()
    print('Recebendo paramêtros {}'.format(args))
    preprocess_fn(split_ratio=args.train_test_split_ratio)
