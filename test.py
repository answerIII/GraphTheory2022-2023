import os

from logistic_regression import logreg
from logistic_regression import preproc_data
from pathlib import Path

EXTRACTION_FILE_NAME = "PART3"
PREDICT_NAME = "soc-sign-bitcoinalpha"
EXTRACTION_FILE_NAME = "part2"

DATA_SUFFIX = ".txt"
FEATURE_SUFFIX = ".csv"
RESULT_SUFFIX = ".png"

PROJECT_PATH = Path("")
FEATURES_PATH = PROJECT_PATH.joinpath("features")
RESULTS_PATH = PROJECT_PATH.joinpath("results")
GRAPH_PATH = PROJECT_PATH.joinpath("graph")
DATA_PATH = PROJECT_PATH.joinpath("data")
FILE_PREF = "TEST-" + EXTRACTION_FILE_NAME + "-"


def predict(file_name: Path):
    train, test = preproc_data.load_data(FEATURES_PATH.joinpath(FILE_PREF + file_name).with_suffix(FEATURE_SUFFIX))
    train_X, train_y = preproc_data.split_data(train)
    test_X, test_y = preproc_data.split_data(test)
    
    log_reg = logreg.fit_logreg(train_X, train_y)
    curve = logreg.roc_auc_curve(log_reg, test_X, test_y)
    
    curve.savefig(RESULTS_PATH.joinpath(FILE_PREF + file_name).with_suffix(RESULT_SUFFIX))


def extract_features(file_path: Path = DATA_PATH.joinpath(PREDICT_NAME).with_suffix(DATA_SUFFIX), max_features: int = 20000, data_part: float = 0.6666):
    file_name = file_path.parts[-1][:-len(DATA_SUFFIX)]
    
    print(f"\n==| Static feature extraction \"{file_name}\" |==\n")
    
    command = f"{GRAPH_PATH.joinpath(EXTRACTION_FILE_NAME)} {file_path} {max_features//2} {data_part} {FEATURES_PATH.joinpath(FILE_PREF + file_name).with_suffix(FEATURE_SUFFIX)}"    
    
    print("\n","command:", command, "\n")
    
    res = os.system(command)
    
    if (res != 0):
        raise Exception(f"graph error code: {res}")
        exit()
        
    print("\n==| Successful extraction |==\n")
    
    return file_name

if __name__ == '__main__':
    predict(extract_features())