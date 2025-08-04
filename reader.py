import os
import networkx as nx
import igraph as ig

import my_globals
import directory_manager

def read_gml_graph(file_name):
    G = nx.read_gml(file_name, label="id")
    for u, v in G.edges():
        weight = G[u][v].get("weight", 1.0)
        G[u][v]["weight"] = weight
    return G

def read_edgelist(file_name):
    nxG = nx.read_edgelist(file_name, nodetype=int, data=(("weight", float),))
    for u, v, data in nxG.edges(data=True):
        if "weight" not in data:
            data["weight"] = 1.0
    return nxG

def read_graph(file_name):
    file_type = file_name.split(".")[-1]

    if file_type == "gml":
        nxG = read_gml_graph(file_name)
    elif file_type == "edgelist":
        nxG = read_edgelist(file_name)

    # mapping işlemi kaldırıldı, orijinal node ID'ler kullanılıyor
    for node in nxG.nodes():
        nxG.nodes[node]["label"] = node  # node ID'yi label olarak sakla

    edge_list = [(u, v, d.get("weight", 1.0)) for u, v, d in nxG.edges(data=True)]
    igG = ig.Graph.TupleList(edge_list, directed=False, weights=True)

    # mapping yine oluşturulabilir ama artık kullanılmayacak
    mapping = {node: idx for idx, node in enumerate(nxG.nodes())}

    return nxG, igG, mapping


def read_graph_and_layout(file_path):
    nx_graph, ig_graph, mapping = read_graph(file_path)
    layout = ig_graph.layout("kk")
    return nx_graph, ig_graph, layout, mapping

def read_communities(file_path, mapping=None):
    with open(file_path, "r") as file:
        lines = file.readlines()
    communities = eval(lines[0])

    if mapping is None:
        return communities

    new_communities = []
    for community in communities:
        new_community = []
        for node in community:
            if node in mapping:
                new_community.append(node)  # mapping iptal edildi, orijinal ID ile kullan
        new_communities.append(new_community)

    return new_communities


def read_datasets():
    directory = f"{directory_manager.PROJECT_DIRECTORY}/Data/{my_globals.dataset_type_to_string[my_globals.SELECTED_DATASET_TYPE]}"
    datasets = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path) and (file_name.endswith(".edgelist") or file_name.endswith(".gml")):
            dataset = my_globals.Dataset()
            dataset.directory = file_path
            dataset.name, _ = os.path.splitext(file_name)

            dataset.nx_graph, dataset.ig_graph, mapping = read_graph(file_path)
            # dataset.layout = dataset.ig_graph.layout("kk")

            communities_file_path = os.path.splitext(file_path)[0] + ".dat"
            if os.path.exists(communities_file_path):
                dataset.real_communities = read_communities(communities_file_path, None)  # mapping kullanma

            datasets.append(dataset)

    return datasets
