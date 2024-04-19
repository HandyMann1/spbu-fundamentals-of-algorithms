import copy
from typing import Any

# from src.plotting import plot_graph
import networkx as nx
import numpy as np


def edge_tuple_creator(array):
    result = []
    for i in range(len(array) - 1):
        result.append((array[i], array[i + 1]))
    return result


def max_flow(G: nx.DiGraph, s: Any, t: Any) -> int:
    value: int = 0
    G_tmp = copy.deepcopy(G)

    while True:
        try:
            path = nx.shortest_path(G_tmp, s, t)
        except nx.NetworkXNoPath:
            break

        print(f'path = {path}')

        path_edges = edge_tuple_creator(path)
        min_flow_local = np.inf

        for i in range(len(path) - 1):
            weight_list = nx.get_edge_attributes(G_tmp, "weight")
            if weight_list[path_edges[i]] < min_flow_local:
                min_flow_local = weight_list[path_edges[i]]
        print(f'minimal flow = {min_flow_local}')
        value += min_flow_local

        for j in range(len(path) - 1):
            edge_tuple = path_edges[j]
            G_tmp.edges[edge_tuple]["weight"] -= min_flow_local

            if G_tmp.edges[edge_tuple]["weight"] == 0:
                G_tmp.remove_edge(edge_tuple[0], edge_tuple[1])

            if edge_tuple[::-1] not in G_tmp.edges:
                G_tmp.add_edge(edge_tuple[::-1][0], edge_tuple[::-1][1])
                G_tmp.edges[edge_tuple[::-1]]["weight"] = min_flow_local
            else:
                G_tmp.edges[edge_tuple[::-1]]["weight"] += min_flow_local
    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.DiGraph)

    # plot_graph(G)
    val = max_flow(G, s='0', t='5')
    print(f"Maximum flow is {val}. Should be 23")
