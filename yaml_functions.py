import os
import yaml
from pprint import pprint as pp

def init_language():
    """
    기본 언어 설정. 없으면 영어. 글-로벌
    """
    yaml_data = read_yaml("config.yaml", '!default')
    if yaml_data: return yaml_data.get('LANGUAGE') + "\\"
    else: return ""

def read_yaml(file, *args):
    """
    YAML 파일을 불러와 읽음. 번역 정보를 받음
    """

    print_info = True if 'info' in args else False # 활성화하면 로드한 파일 내용을 나열해줌
    default = False if '!default' in args else True # 기본값은 DEFAULT_FOLDER에서 염

    def set_file_path(file):
        FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(FILE_PATH, file)

    def open_file(file_path):
        with open(file_path, 'r', encoding='UTF8') as file:
            try:
                info = yaml.load(file, Loader=yaml.FullLoader)
                if print_info: pp(info)
                return info
            except yaml.YAMLError as exc:
                print(f'crashed while trying to load {file_path}')
                if hasattr(exc, 'problem_mark'):
                    mark = exc.problem_mark
                    print (f'Error position: {mark.line+1}:{mark.column+1}')
                return exc

    def update_dic(dic, updating):
        import collections.abc
        for k, v in updating.items():
            if isinstance(v, collections.abc.Mapping):
                dic[k] = update_dic(dic.get(k, {}), v)
            else:
                dic[k] = v
        return dic

    route = set_file_path(file)

    if default: # 번역 사용, 영어판 yaml 파일을 불러온 뒤 번역판을 덮어씌움.
        route = set_file_path(DEFAULT_FOLDER + file)
        Total_yaml = open_file(route)
        if LANG:
            tns_route = set_file_path(DEFAULT_FOLDER + LANG + file)
            Tns_yaml = open_file(tns_route)
            Total_yaml = update_dic(Total_yaml, Tns_yaml)

        return Total_yaml

    else: # Mary 폴더에서 직접 열 때
        return open_file(route)


def cout(searching_object, *args):
    """
    원하는 yaml에서 추출한 객체를 이용해 메세지를 만들때 씀.
    args 쓰는 순서는 영어순대로, 번역파일에서 알아서 순서를 바꾸니 다르게 할 필요는 없음
    """
    return searching_object['log_format'].format(*args)

DEFAULT_FOLDER = "translations\\"
LANG = init_language()
#SYS_LOG = read_yaml("system_log.yaml")

if __name__ == "__main__":
    #artifacts = read_yaml("artifacts.yaml")
    #talisman = artifacts['talisman']

    log = read_yaml('system_log.yaml')['character_info_log']
    pp(log)
