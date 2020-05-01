import os
import yaml
from pprint import pprint as pp

def open_yaml(file, print_info=False):
    def set_file_path(file):
        FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(FILE_PATH, file)

    with open(set_file_path(file), 'r') as file:
        try:
            info = yaml.load(file, Loader=yaml.FullLoader)
            if print_info: pp(info)
            return info
        except yaml.YAMLError as exc:
            return exc
