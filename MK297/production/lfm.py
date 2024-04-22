import sys
sys.path.append("../util")
import read
import numpy as np


def init_model(vector_len):
    return np.random.randn(vector_len)

def model_predict(user_vec, item_vec):
    return np.dot(user_vec, item_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(item_vec))

def lfm_train(train_data, F, alpha, beta, step):
    """
    :param train_data: 训练数据集
    :param F: 隐特征维度
    :param alpha: 正则化参数
    :param beta: 学习率
    :param step: 迭代次数
    :return: dict: key itemid, value:np.ndarray
    :return: dict: key userid, value:np.ndarray
    """
    user_vec, item_vec = {}, {}
    for step_index in range(step):
        for data_instance in train_data:
            userid, itemid, label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F)
        delta = label - model_predict(user_vec[userid], item_vec[itemid])
        for index in range(F):
            user_vec[userid][index] += beta * (delta * item_vec[itemid][index] - alpha * user_vec[userid][index])
            item_vec[itemid][index] += beta * (delta * user_vec[userid][index] - alpha * item_vec[itemid][index])
        beta *= 0.9
    return user_vec, item_vec

def model_train_process():
    train_data = read.get_train_data("/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv", 4.0)
    user_vec, item_vec = lfm_train(train_data, F=50, alpha=0.01, beta=0.1, step=50)
    return user_vec, item_vec

def give_recom_result(user_vec, item_vec, userid, fix_num):
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = model_predict(user_vector, item_vector)
        record[itemid] = res
    for pair in sorted(record.items(), key=lambda x: x[1], reverse=True)[:fix_num]:
        itemid = pair[0]
        score = round(pair[1], 3)
        recom_list.append((itemid, score))
    return recom_list


def ana_recom_result(train_data, userid, recom_list):
    item_info = read.get_item_info("/Users/mac/Codes/Projects/Dataset/mksz297/movies.csv")
    for data_instance in train_data:
        uid, itemid, label = data_instance
        if label == 1 and userid == uid:
            print(item_info[itemid])
    print("=" * 50)
    for pair in recom_list:
        print(item_info[pair[0]])

if __name__ == '__main__':
    user_vec, item_vec = model_train_process()
    recom_list = give_recom_result(user_vec, item_vec, "24", 10)
    train_data = read.get_train_data("/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv", 4.0)
    ana_recom_result(train_data, "24", recom_list)