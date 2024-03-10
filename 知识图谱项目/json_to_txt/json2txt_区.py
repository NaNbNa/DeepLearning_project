import pandas as pd
import json
import os


def json2txt(path_json, path_txt):
    # files是list类型
    files = os.listdir(path_json)
    txt = open(path_txt + "/" + 'quName.txt', 'w+')
    for file in files:  # 遍历文件夹内文件
        position = path_json + "/" + file
        with open(position, 'r', encoding='utf8') as f:
            line = f.read()
            data_json = json.loads(line)
            department_list = data_json['dataList']
            for list_dict in department_list:
                attribution = list_dict["attributes"]['xtBusinessType']
                name = attribution['quName']
                if isinstance(name, str):
                    txt.writelines(name + "\n")
    txt.close()


dir_json = '/Users/ctb/Downloads/PyProject/project/JsonFile'
dir_txt = '/Users/ctb/Downloads/PyProject/project/txtFile'
json2txt(dir_json, dir_txt)
print('ok')
