import os

def get_item_info(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    item_info = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            elif len(item) == 3:
                itemid, title, genre = item[0], item[1], item[2]
            elif len(item) > 3:
                itemid, genre = item[0], item[-1]
                title = ','.join(item[1:-1])
            item_info[itemid] = [title, genre]
    return item_info


def get_ave_score(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating = item[0], item[1], item[2]
            if itemid not in record_dict:
                record_dict[itemid] = [0, 0.0]
            record_dict[itemid][0] += 1
            record_dict[itemid][1] += float(rating)
    for itemid in record_dict.keys():
        score_dict[itemid] = round(record_dict[itemid][1] / record_dict[itemid][0], 3)
    return score_dict


def get_train_data(input_file, score_thr):
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    linenum = 0
    neg_dict = {}
    pos_dict = {}
    train_data = []
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid, itemid, rating = item[0], item[1], float(item[2])
            if userid not in pos_dict:
                pos_dict[userid] = []
            if userid not in neg_dict:
                neg_dict[userid] = []
            if rating >= score_thr:
                pos_dict[userid].append((itemid, 1))
            else:
                score = score_dict.get(itemid, 0.0)
                neg_dict[userid].append((itemid, score))
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num > 0:
            train_data += [(userid, x[0], x[1]) for x in pos_dict[userid]][:data_num]
        else:
            continue
        sorted_neg_list = sorted(neg_dict[userid], key=lambda x: x[1], reverse=True)[:data_num]
        train_data += [(userid, x[0], 0) for x in sorted_neg_list]
        # if userid == '1':
        #     print(len(pos_dict['1']))
        #     print(len(neg_dict['1']))
        #     print(sorted_neg_list)
    return train_data


def get_graph_from_data(input_file, score_thr):
    """
    Return: {userA: {itemb:1, itemc:1}, itemb: {userA:1, userB:1}, ...}
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    graph = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            userid, itemid, rating = item[0], "item_" + item[1], item[2]
            if float(rating) < score_thr:
                continue
            if userid not in graph:
                graph[userid] = {}
            graph[userid][itemid] = 1
            if itemid not in graph:
                graph[itemid] = {}
            graph[itemid][userid] = 1
    return graph



if __name__ == '__main__':
    # item_dict = get_item_info("/Users/mac/Codes/Projects/Dataset/mksz297/movies.csv")
    # print(len(item_dict))
    # print(item_dict['1'])
    # print(item_dict['11'])

    # score_dict = get_ave_score("/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv")
    # print(len(score_dict))
    # print(score_dict['31'])

    # train_data = get_train_data("/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv", 4.0)
    # print(len(train_data))
    # print(train_data[:50])

    graph = get_graph_from_data(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/ratings.csv", 4.0)
    print(graph['1'])