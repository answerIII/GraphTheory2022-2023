import pandas as pd
from sklearn import model_selection


def load_data(data_path: str) -> (pd.DataFrame, pd.DataFrame):
    df = pd.read_csv(data_path)
    
    true_df = df[df['predict'] == 1.]
    false_df = df[df['predict'] == 0.]
    
    train_true_df, test_true_df = model_selection.train_test_split(true_df, test_size=0.25, random_state=0)
    train_false_df, test_false_df = model_selection.train_test_split(false_df, test_size=0.25, random_state=0)
    
    train_df = pd.concat([train_true_df, train_false_df])
    test_df = pd.concat([test_true_df, test_false_df])
    
    return train_df, test_df


def split_data(df: pd.DataFrame) -> (pd.DataFrame, pd.Series):
    return df.drop(columns=['predict']), df['predict']


if __name__ == '__main__':
    train_df, test_dt = load_data('TEST.txt')
    train_X, train_y = split_data(train_df)
    test_X, test_y = split_data(test_dt)
    print(train_df)
    print(test_dt)
    
    print(train_X, train_y)
    print(test_X, test_y)