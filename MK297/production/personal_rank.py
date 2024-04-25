import sys
sys.path.append("../util")
import read, mat_util
import numpy as np
from scipy.sparse.linalg import gmres

def personal_rank(graph, root, alpha, iter_num, recom_num=10):
    rank = {point: 0 for point in graph}
    rank[root] = 1
    recom_res = {}
    for iter_index in range(iter_num):
        tmp_rank = {point: 0 for point in graph}
        for out_point, out_dict in graph.items():
            for inner_point, value in out_dict.items():
                tmp_rank[inner_point] += round(alpha * rank[out_point] / len(out_dict), 4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1 - alpha, 4)
        if tmp_rank == rank:
            break
        rank = tmp_rank

    cnt = 1
    for pair in sorted(rank.items(), key=lambda x: x[1], reverse=True):
        point, pr = pair[0], pair[1]
        if len(point.split("_")) < 2:
            continue
        if point in graph[root]:
            continue
        recom_res[point] = pr
        cnt += 1
        if cnt > recom_num:
            break
    return recom_res
    

def personal_rank_mat(graph, root, alpha, recom_num=10):
    m, vertex, address_dict = mat_util.graph_to_m(graph)
    if root not in address_dict:
        return {}
    score_dict = {}
    recom_dict = {}
    mat_all = mat_util.mat_all_point(m, vertex, alpha)
    index = address_dict[root]
    initial_list = [[0] for _ in range(len(vertex))]
    initial_list[index] = [1]
    r_zero = np.array(initial_list)
    res = gmres(mat_all, r_zero, rtol=1e-8)[0]
    for index in range(len(res)):
        point = vertex[index]
        if len(point.split("_")) < 2:
            continue
        if point in graph[root]:
            continue
        score_dict[point] = round(res[index], 3)
    for pair in sorted(score_dict.items(), key=lambda x: x[1], reverse=True)[:recom_num]:
        point, pr = pair[0], pair[1]
        recom_dict[point] = pr
    return recom_dict
    

def get_one_user_recom():
    graph = read.get_graph_from_data(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/ratings.csv", 4.0)
    result = personal_rank(graph, "1", 0.8, 20, 100)
    # item_info = read.get_item_info(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/movies.csv")
    # for itemid in graph["1"]:
    #     _itemid = itemid.split("_")[1]
    #     print(item_info[_itemid])
    # print("*" * 50)
    # for itemid in result:
    #     _itemid = itemid.split("_")[1]
    #     print(item_info[_itemid], result[itemid])
    return result


def get_one_user_by_mat():
    graph = read.get_graph_from_data(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/ratings.csv", 4.0)
    result = personal_rank_mat(graph, "1", 0.8, 100)
    # item_info = read.get_item_info(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/movies.csv")
    # for itemid in graph["1"]:
    #     _itemid = itemid.split("_")[1]
    #     print(item_info[_itemid])
    # print("*" * 50)
    # for itemid in result:
    #     _itemid = itemid.split("_")[1]
    #     print(item_info[_itemid], result[itemid])
    return result

if __name__ == "__main__":
    recom_result_base = get_one_user_recom()
    recom_result_mat = get_one_user_by_mat()
    num = 0
    print(len(recom_result_base))
    for ele in recom_result_base:
        if ele in recom_result_mat:
            num += 1
    print(num)