import os
import sys
sys.path.append("/Users/mac/Codes/Projects/Recommend_Related/MK297/util")
import read


def get_up(item_cate, input_file, score_thr=4.0, topk=2):
    if not os.path.exists(input_file):
        return {}
    record = {}
    up = {}
    linenum = 0
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating, timestamp = item[0], item[1], float(item[2]), int(item[3])
            if rating < score_thr:
                continue
            if itemid not in item_cate:
                continue
            time_score = get_time_score(timestamp)
            if userid not in record:
                record[userid] = {}
            for cate in item_cate[itemid]:
                if cate not in record[userid]:
                    record[userid][cate] = 0
                record[userid][cate] += rating * time_score * item_cate[itemid][cate]
    for userid in record:
        if userid not in up:
            up[userid] = []
        total_score = 0
        for pair in sorted(record[userid].items(), key=lambda x: x[1], reverse=True)[:topk]:
            up[userid].append((pair[0], pair[1]))
            total_score += pair[1]
        for index in range(len(up[userid])):
            up[userid][index] = (up[userid][index][0], round(up[userid][index][1] / total_score, 3))
    return up


def get_time_score(timestamp):
    fix_time_stamp = 1476086345
    total_secs = 24 * 60 * 60
    delta = (fix_time_stamp - timestamp) / total_secs / 100
    return round(1 / (1 + delta), 3)


def recom(cate_item_sort, up, userid, topk=10):
    if userid not in up:
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for pair in up[userid]:
        cate = pair[0]
        ratio = pair[1]
        num = int(topk * ratio) + 1
        if cate not in cate_item_sort:
            continue
        recom_list = cate_item_sort[cate][:num]
        recom_result[userid].extend(recom_list)
    return recom_result


def run_main(score_file_path, info_file_path, userid, topk=10):
    ave_score = read.get_ave_score(score_file_path)
    item_cate, cate_item_sort = read.get_item_cate(ave_score, info_file_path)
    up = get_up(item_cate, score_file_path)
    recom_result = recom(cate_item_sort, up, userid, topk)
    return recom_result


if __name__ == '__main__':
    score_file_path = '/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv'
    info_file_path = '/Users/mac/Codes/Projects/Dataset/mksz297/movies.csv'
    userid = '1'
    recom_result = run_main(score_file_path, info_file_path, userid, topk=10)
    print(recom_result)