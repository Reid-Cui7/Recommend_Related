
import numpy as np
import pandas as pd

def get_input(input_train_data, input_test_data):
    dtype_dict = {
                    "age": np.int32,
                    "education-num": np.int32,
                    "capital-gain": np.int32,
                    "capital-loss": np.int32,
                    "hours-per-week": np.int32,
                }
    
    use_list = range(15)
    use_list.remove(2)
    train_data_df = pd.read_csv(input_train_data, sep=",", header=0, dtype=dtype_dict, na_values="?", usecols=use_list)
    train_data_df.dropna(axis=0, how="any")
    test_data_df = pd.read_csv(input_test_data, sep=",", header=0, dtype=dtype_dict, na_values="?", usecols=use_list)
    test_data_df.dropna(axis=0, how="any")
    return train_data_df, test_data_df

def label_trans(x):
    return "0" if x == " <=50K" else "1"


def process_label_feature(label_feature_str, df_in):
    df_in.loc[:,label_feature_str] = df_in.loc[:,label_feature_str].apply(label_trans)


def dict_trans(dict_in):
    output_dict = {}
    index = 0
    for pair in sorted(dict_in.items(), key=lambda x:x[1], reverse=True):
        output_dict[pair[0]] = index
        index += 1
    return output_dict


def dis_to_feature(x, feature_dict):
    output_list = [0] * len(feature_dict)
    if x not in feature_dict:
        return ",".join([str[ele] for ele in output_list])
    else:
        index = feature_dict[x]
        output_list[index] = 1
    return ",".join(str[ele] for ele in output_list)

def process_dis_feature(feature_str, df_train, df_test):
    origin_dict = df_train.loc[:,feature_str].value_counts().to_dict()
    feature_dict = dict_trans(origin_dict)
    df_train.loc[:,feature_str] = df_train.loc[:,feature_str].apply(dis_to_feature, args=(feature_dict,))
    df_test.loc[:,feature_str] = df_test.loc[:,feature_str].apply(dis_to_feature, args=(feature_dict,))
    return len(feature_dict)

def list_trans(input_dict):
    output_list = [0] * 5
    key_list = ["min", "25%", "50%", "75%", "max"]
    for index in range(len(key_list)):
        fix_key = key_list[index]
        if fix_key not in input_dict:
            raise ValueError("{} not in dict".format(fix_key))
            sys.exit()
        output_list[index] = input_dict[fix_key]
    return output_list
        

def con_to_feature(x, feature_list):
    feature_len = len(feature_list) - 1
    result = [0] * feature_len
    for index in range(feature_len):
        if x >= feature_list[index] and x <= feature_list[index+1]:
            result[index] = 1
            return ",".join(str[ele] for ele in result)
    return ",".join(str[ele] for ele in result)

def process_con_feature(feature_str, df_train, df_test):
    origin_dict = df_train.loc[:,feature_str].describe().to_dict()
    feature_list = list_trans(origin_dict)
    df_train.loc[:,feature_str] = df_train.loc[:,feature_str].apply(con_to_feature, args=(feature_list,))
    df_test.loc[:,feature_str] = df_test.loc[:,feature_str].apply(con_to_feature, args=(feature_list,))
    return len(feature_list) - 1

def output_file(df_in, out_file):
    with open(out_file, "w") as f:
        for index, row in df_in.iterrows():
            f.write("{}\n".format(row.to_csv(header=False, index=False)))

def add(str_one, str_two):
    list_one = str_one.split(",")
    list_two = str_two.split(",")
    list_one_len = len(list_one)
    list_two_len = len(list_two)
    return_list = [0] * (list_one_len * list_two_len)
    try:
        index_one = list_one.index('1')
    except:
        index_one = 0
    try:
        index_two = list_two.index('1')
    except:
        index_two = 0
    return_list[index_one * list_two_len + index_two] = 1
    return ",".join(str[ele] for ele in return_list)

def combine_feature(feature_one, feature_two, new_feature, train_data_df, test_data_df, feature_num_dict):
    train_data_df[new_feature].train_data_df.apply(lambda row: add(row[feature_one], row[feature_two]))
    test_data_df[new_feature].test_data_df.apply(lambda row: add(row[feature_one], row[feature_two]))
    if feature_one not in feature_num_dict:
        raise ValueError("{} not in dict".format(feature_one))
        sys.exit()
    return feature_num_dict[feature_one] * feature_num_dict[feature_two]

def ana_train_data(input_train_data, input_test_data, out_train_file, out_test_file, feature_num_file):
    train_data_df, test_data_df = get_input(input_train_data, input_test_data)
    label_feature_str = "label"
    dis_feature_list = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country"]
    con_feature_list = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
    process_label_feature(label_feature_str, train_data_df)
    process_label_feature(label_feature_str, test_data_df)
    index_list = ['age', 'workclass', 'education', 'education-num', 'marital-status', 'occupation', 'relationship', \
        'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country']
    dis_feature_num = 0
    con_feature_num = 0
    feature_num_dict = {}
    for dis_feature in dis_feature_list:
        tmp_feature_num += process_dis_feature(dis_feature, train_data_df, test_data_df)
        dis_feature_num += tmp_feature_num
        feature_num_dict[dis_feature] = tmp_feature_num
    for con_feature in con_feature_list:
        tmp_feature_num += process_con_feature(con_feature, train_data_df, test_data_df)
        con_feature_num += tmp_feature_num
        feature_num_dict[con_feature] = tmp_feature_num
    new_feature_len = combine_feature("age", "workclass", "age_workclass", train_data_df, test_data_df, feature_num_dict)
    new_feature_len_2 = combine_feature("capital-gain", "education", "cap_edu", train_data_df, test_data_df, feature_num_dict)
    train_data_df = train_data_df.reindex(columns=index_list + ["age_workclass", "cap_edu", "label"])
    test_data_df = test_data_df.reindex(columns=index_list + ["age_workclass", "cap_edu", "label"])
    output_file(train_data_df, out_train_file)
    output_file(test_data_df, out_test_file)
    with open(feature_num_file, "w") as f:
        f.write("feature_num=" + str(dis_feature_num + con_feature_num + new_feature_len))





if __name__ == "__main__":
    ...