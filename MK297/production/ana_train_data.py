
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


def ana_train_data(input_train_data, input_test_data, out_train_data, out_test_data):
    train_data_df, test_data_df = get_input(input_train_data, input_test_data)
    process_label_feature("label", train_data_df)
    process_label_feature("label", test_data_df)


if __name__ == "__main__":
    ...