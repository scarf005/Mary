import os
import yaml

def open_yaml(file):
    def set_file_path(file):
        FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(FILE_PATH, file)

    with open(set_file_path(file), 'r') as file:
        try:
            info = yaml.load(file, Loader=yaml.FullLoader)
            print(info)
            print(info['crawling_intestine'])
        except yaml.YAMLError as exc:
            print(exc)
