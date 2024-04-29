import numpy as np
from sklearn.externals import joblib

def get_test_data(test_file):
    total_feature_num = 118
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

def predict_by_lr_coef(test_feature, lr_coef):
    sigmoid_func = np.frompyfunc(sigmoid, 1, 1)
    return sigmoid_func(np.dot(test_feature, lr_coef))


def run_check_core(test_feature, test_label, model, score_func):
    predict_list = score_func(test_feature, model)
    get_auc(predict_list, test_label)
    get_accuarcy(predict_list, test_label)

def run_check(test_file, lr_coef_file, lr_model_file):
    test_feature, test_label = get_test_data(test_file)
    lr_coef = np.genfromtxt(lr_coef_file, delimiter=',', dtype=np.float32)
    lr_model = joblib.load(lr_model_file)
    run_check_core(test_feature, test_label, lr_model, predict_by_lr_model)
    run_check_core(test_feature, test_label, lr_coef, predict_by_lr_coef)