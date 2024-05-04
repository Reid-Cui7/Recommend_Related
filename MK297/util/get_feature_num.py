import os

def get_feature_num(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as file:
        for line in file.readlines():
            item = line.strip().split('=')
            if item[0] == 'feature_num':
                return int(item[1])
    return 0