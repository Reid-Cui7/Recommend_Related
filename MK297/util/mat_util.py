import sys
sys.path.append("./")
import read
import numpy as np
from scipy.sparse import coo_matrix

def graph_to_m(graph):
    vertex = list(graph.keys())
    address_dict = {}
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index
    row = []
    col = []
    data = []
    for element_i in graph:
        weight = round(1 / len(graph[element_i]), 3)
        row_index = address_dict[element_i]
        for element_j in graph[element_i]:
            col_index = address_dict[element_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    m = coo_matrix((data, (row, col)), shape=(len(vertex), len(vertex)))
    return m, vertex, address_dict


def mat_all_point(m_mat, vertex, alpha):
    total_len = len(vertex)
    row = []
    col = []
    data = []
    for index in range(total_len):
        row.append(index)
        col.append(index)
        data.append(1)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data, (row, col)), shape=(total_len, total_len))
    return eye_t.tocsr() - alpha * m_mat.tocsr().transpose()


if __name__ == "__main__":
    graph = read.get_graph_from_data(r"C:/Users/Bean1777/Documents/Codes/Daily/Data/ratings.csv", 4.0)
    m, vertex, address_dict = graph_to_m(graph)
    print(address_dict)
    print(m.todense())
    print(mat_all_point(m, vertex, 0.8))