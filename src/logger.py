import json
import os

class Logger(object):
    def __init__(self, dir : str = './', logs_file_name : str = 'logs.json', saving_step : int = 50, safe_mode : bool = False):
        if (saving_step <= 0):
            raise Exception("Saving step value is negative: " + str(saving_step))

        self.__counter = 0
        self.__saving_step = saving_step
        self.__file_path = dir + '/' + logs_file_name
        self.__safe_mode = safe_mode

        if os.path.isfile(self.__file_path):
            self.__logs = self.__parse_from_file()
        else:
            self.__logs = {}

    
    def __del__(self):
        try:
            self.dump()
        except NameError:
            pass


    def is_empty(self) -> bool:
        return len(self.__logs) == 0


    def dump(self) -> None:
        if (self.__safe_mode):
            return
        with open(self.__file_path, 'w+') as file:
            json.dump(self.__logs, file)


    def get_pairs(self) -> list:
        result = []
        for key, value in self.__logs.items():
            pair = self.__pair_from_key(key)
            pair.append(value[0])
            result.append(pair)
        return result
    

    def get_features(self) -> list:
        result = []
        for features in self.__logs.values():
            result.append(features)
        return result


    def log(self, vertex_id_1 : int, vertex_id_2 : int, features : list) -> None:
        key = self.__key(vertex_id_1, vertex_id_2)
        if (key in self.__logs):
            raise Exception("Such data is already stored:\n " + key + " : " + str(self.__logs[key]))

        self.__logs[key] = features
        self.__counter += 1

        if (self.__counter % self.__saving_step == 0):
            self.dump()

    
    def remove(self, vertex_id_1 : int, vertex_id_2 : int) -> None:
        key = self.__key(vertex_id_1, vertex_id_2)
        if (key not in self.__logs):
            return
        
        del self.__logs[key] 
        self.__counter += 1

        if (self.__counter % self.__saving_step == 0):
            self.dump()

    
    def contains(self, vertex_id_1 : int, vertex_id_2 : int) -> bool:
        key = self.__key(vertex_id_1, vertex_id_2)
        return (key in self.__logs)


    def __parse_from_file(self) -> dict:
        try:
            with open(self.__file_path, 'r') as file:
                return json.load(file)
        except OSError:
            print("Could not open/read file: ", self.__file_path)
        except Exception:
            print("Could not parse json: ", self.__file_path)


    def __key(self, vertex_id_1 : int, vertex_id_2 : int) -> str:
        return str(min(vertex_id_1, vertex_id_2)) + '-' + str(max(vertex_id_1, vertex_id_2))
    

    def __pair_from_key(self, key : str) -> list:
        tokens = key.split('-')
        return [int(tokens[0]), int(tokens[1])]
    