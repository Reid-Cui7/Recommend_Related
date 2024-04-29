import os
import sys
import numpy as np

def load_item_vec(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    item_vec = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split()
            if len(item) < 129:
                continue
            itemid = item[0]
            if itemid == "</s>":
                continue
            item_vec[itemid] = np.asarray([float(x) for x in item[1:]])
    return item_vec


def cal_item_sim(item_vec_dict, itemid, output_file, top_k=10):
    if itemid not in item_vec_dict:
        return
    score = {}
    item_vec = item_vec_dict[itemid]
    for other_itemid in item_vec_dict.keys():
        if other_itemid == itemid:
            continue
        other_item_vec = item_vec_dict[other_itemid]
        dnum = np.linalg.norm(item_vec) / np.linalg.norm(other_item_vec)
        if dnum == 0:
            score[other_itemid] = 0
        else:
            score[other_itemid] = round(np.dot(item_vec, other_item_vec) / dnum, 3)
    with open(output_file, 'a') as f:
        tmp_list = []
        out_str = itemid + "\t"
        for pair in sorted(score.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            tmp_list.append(pair[0] + "_" + str(pair[1]))
        out_str += ";".join(tmp_list)
        f.write(out_str + "\n")


def run_main(input_file, output_file, top_k=10):
    item_vec_dict = load_item_vec(input_file)
    for itemid in item_vec_dict.keys():
        cal_item_sim(item_vec_dict, itemid, output_file, top_k)


if __name__ == "__main__":
    # item_vec = load_item_vec("./item_vec.txt")
    # print(len(item_vec))
    # run_main("./item_vec.txt", "./item_sim.txt")
    if len(sys.argv) < 3:
        print("Usage: python produce_item_sim.py input_file output_file")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        run_main(input_file, output_file)
