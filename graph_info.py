import sys
import os
from pathlib import Path

DATA_SUFFIX = ".txt"
RESULTS_SUFIX = ".csv"

PROJECT_PATH = Path("")
RESULTS_PATH = PROJECT_PATH.joinpath("results")
GRAPH_PATH = PROJECT_PATH.joinpath("graph")
DATA_PATH = PROJECT_PATH.joinpath("data")
FILE_PREF = "GRAPH-INFO-"
EXE_FILE_NAME = "part1"


def calc_all(dir_path: Path = DATA_PATH):
    for file_path in dir_path.rglob("*"):
        if file_path.suffix == DATA_SUFFIX:
            get_info(file_path)


def get_info(file_path: Path):
    file_name = file_path.parts[-1][:-len(DATA_SUFFIX)]
    result_data = RESULTS_PATH.joinpath(FILE_PREF + file_name + RESULTS_SUFIX)
    
    res = os.system(f"{GRAPH_PATH.joinpath(EXE_FILE_NAME)} {file_path} {result_data}")
    
    if (res != 0):
        raise Exception(f"graph error code: {res}")
        exit()
        
    print("\n==| Successful |==\n")


if __name__ == '__main__':
    args = sys.argv
    
    calc_all()
