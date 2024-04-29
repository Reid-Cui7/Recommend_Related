import os
import sys

def produce_train_data(input_file, out_file, score_thr=4.0):
    if not os.path.exists(input_file):
        return
    linenum = 0
    record = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            useid, itemid, rating = item[0], item[1], float(item[2])
            if rating < score_thr:
                continue
            if useid not in record:
                record[useid] = []
            record[useid].append(itemid)
    with open(out_file, 'w') as f:
        for userid in record:
            f.write(" ".join(record[userid]) + "\n")


if __name__ == '__main__':
    # input_file = '/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv'
    # out_file = '/Users/mac/Codes/Projects/Dataset/mksz297/train_data.txt'
    # produce_train_data(input_file, out_file)
    if len(sys.argv) < 3:
        print("Usage: python produce_train_data.py <input_file> <out_file>")
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        produce_train_data(input_file, output_file)