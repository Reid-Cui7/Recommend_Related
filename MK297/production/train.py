import numpy as np
from sklearn.linear_model import LogisticRegressionCV as LRCV
from sklearn.externals import joblib

def train_lr_model(train_file, model_coef, model_file):
    total_feature_num = 118
    train_label = np.genfromtxt(train_file, delimiter=',', dtype=np.int32, usecols=-1)
    feature_list = range(total_feature_num)
    train_feature = np.genfromtxt(train_file, delimiter=',', dtype=np.float32, usecols=feature_list)
    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5).fit(train_feature, train_label)
    scores = lr_cf.scores_.values()[0]
    print(f'diff: {",".join([str(score) for score in scores.mean(axis=0)])}')
    print(f'acc: {scores.mean()}')
    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5, scoring="roc_auc").fit(train_feature, train_label)
    print(f"auc: {scores.mean()}")
    coef = lr_cf.coef_[0]
    with open(model_coef, "w+") as f:
        f.write(",".join([str(c) for c in coef]))
    joblib.dump(lr_cf, model_file)
