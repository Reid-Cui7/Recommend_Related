import sys
sys.path.append("../util")
import get_feature_num
import numpy as np
from sklearn.externals import joblib

def get_test_data(test_file, feature_num_file):
    total_feature_num = get_feature_num(feature_num_file)
    test_label = np.getfromtxt(test_file, delimiter=',', dtype=np.float32, usecols=-1)
    feature_list = range(total_feature_num)
    test_feature = np.getfromtxt(test_file, delimiter=',', dtype=np.float32, usecols=feature_list)
    return test_feature, test_label

def predict_by_lr_model(test_feature, lr_model):
    result_list = []
    prob_list = lr_model.predict_proba(test_feature)
    for index in range(prob_list):
        result_list.append(prob_list[index][1])
    return result_list

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def get_auc(predict_list, test_label):
    # auc = (sum(pos_index) - pos_num(pos_num + 1)/2)/pos_num * neg_num)
    total_list = []
    for index in range(len(predict_list)):
        predict_score = predict_list[index]
        label = test_label[index]
        total_list.append((label, predict_score))
    sorted_total_list = sorted(total_list, key=lambda ele: ele[1])
    neg_num = 0
    pos_num = 0
    count = 1
    total_pos_index = 0
    for pair in sorted_total_list:
        label, predict_score = pair[0], pair[1]
        if label == 0:
            neg_num += 1
        else:
            pos_num += 1
            total_pos_index += count
        count += 1
    auc_score = (total_pos_index - pos_num * (pos_num + 1) / 2) / (pos_num * neg_num)
    print(f"{auc_score:.5f}")

def get_accuarcy(predict_list, test_label):
    score_thr = 0.5
    right_num + 0
    for index in range(len(predict_list)):
        predict_score = predict_list[index]
        if predict_score >= score_thr:
            predict_label = 1
        else:
            predict_label = 0
        if predict_label == test_label[index]:
            right_num += 1
    accuracy = right_num / len(predict_list)
    print(f"{accuracy:.5f}")

def predict_by_lr_coef(test_feature, lr_coef):
    sigmoid_func = np.frompyfunc(sigmoid, 1, 1)
    return sigmoid_func(np.dot(test_feature, lr_coef))


def run_check_core(test_feature, test_label, model, score_func):
    predict_list = score_func(test_feature, model)
    get_auc(predict_list, test_label)
    get_accuarcy(predict_list, test_label)

def run_check(test_file, lr_coef_file, lr_model_file, feature_num_file):
    test_feature, test_label = get_test_data(test_file, feature_num_file)
    lr_coef = np.genfromtxt(lr_coef_file, delimiter=',', dtype=np.float32)
    lr_model = joblib.load(lr_model_file)
    run_check_core(test_feature, test_label, lr_model, predict_by_lr_model)
    run_check_core(test_feature, test_label, lr_coef, predict_by_lr_coef)