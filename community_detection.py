import math

__all__ = ['my_algorithm_overlapping_communities']

def calculate_gravitational_weights(G):
    k = 1  # Sabit bir çarpan (gerekirse ayarlanabilir)
    for u, v in G.edges():
        edge_weight = G[u][v]['weight']
        G[u][v]['weight'] = (k * G.degree(u) * G.degree(v)) / (edge_weight ** 2)
        

def calculate_weights(G):   
    for u,v in G.edges():                    
        uNeighbors = frozenset(G.neighbors(u)).union({u})
        vNeighbors = frozenset(G.neighbors(v)).union({v})
        commonNeighbors = uNeighbors.intersection(vNeighbors)
        
        G[u][v]['weight'] = len(commonNeighbors) / (math.sqrt(len(uNeighbors) * len(vNeighbors)))
        print(f"Edge ({u}, {v}) weight: {G[u][v]['weight']}")

def add_node_to_community(communities, index, node):        
    communities[index] = communities[index].union({node})

    if {node} in communities:
        communities.remove({node})

def calculate_CN(communities, communities_of_node, neighbors_of_node):
    return max(
        ((len(communities[index].intersection(neighbors_of_node)), index) for index in communities_of_node),
        default=(-1, 0)
    )

def select_community_using_my_metric(G, u, v, communities, communities_of_node_1, communities_of_node_2):
    neighbors_v = set(G.neighbors(v))
    neighbors_u = set(G.neighbors(u))

    metric_1, index_1 = calculate_CN(communities, communities_of_node_1, neighbors_v)
    metric_2, index_2 = calculate_CN(communities, communities_of_node_2, neighbors_u)

    if metric_1 > metric_2:
        add_node_to_community(communities, index_1, v)
    elif metric_2 > metric_1:
        add_node_to_community(communities, index_2, u)
    else:
        if G.degree(u) < G.degree(v):
            add_node_to_community(communities, index_2, u)
        else:
            add_node_to_community(communities, index_1, v)

def calculate_CNW(G, node_1, communities, communities_of_node_2, neighbors_of_node_2):
    return max(
        ((sum(G[node_1][i].get('weight', 0) for i in communities[index].intersection(neighbors_of_node_2)), index)
         for index in communities_of_node_2),
        default=(-1, 0)
    )

def select_community_using_CNW(G, u, v, communities, communities_of_node_1, communities_of_node_2):
    neighbors_u = set(G.neighbors(u))
    neighbors_v = set(G.neighbors(v))

    metric_1, index_2 = calculate_CNW(G, u, communities, communities_of_node_2, neighbors_u)
    metric_2, index_1 = calculate_CNW(G, v, communities, communities_of_node_1, neighbors_v)

    if metric_1 < metric_2:
        add_node_to_community(communities, index_1, v)
    elif metric_2 < metric_1:
        add_node_to_community(communities, index_2, u)
    else:
        if G.degree(u) < G.degree(v):
            add_node_to_community(communities, index_2, u)
        else:
            add_node_to_community(communities, index_1, v)

    #print(u, v, round(G[u][v].get('w', 0), 2), round(metric_1, 2), round(metric_2, 2), communities)
    
def find_all_communities_of_node(communities, node):
    community_list = list()
    index = 0
    for community in communities:
        if node in community:
            community_list.append(index)
        index = index + 1
    return community_list
    #print(u, v, round(G[u][v].get('w', 0), 2), round(metric_1, 2), round(metric_2, 2), communities)

def my_algorithm_overlapping_communities(G):
    # print(f"Number of nodes: {G.number_of_nodes()}")
    # print(f"Number of edges: {G.number_of_edges()}")
    #assign each node as a community
    communities = [set([n]) for n in G.nodes()]
    
    #find weights
    #calculate_weights(G)
    calculate_gravitational_weights(G)
    
    #sort edges according to their cosine similarities by decreasing order
    sorted_edge_list = sorted(G.edges(data=True), key=lambda t: t[2].get('weight'), reverse=True)

    # print("uv F(u,v) CNW(u,v) CNW(v,u) communities")
    #find communities
    for u, v, w in sorted_edge_list[:]:
        if u == v:
            continue
        if ({u} in communities) and ({v} in communities):
            communities.remove({u})
            communities.remove({v})
            communities.append({u, v})
            continue

        communities_of_node_1 = find_all_communities_of_node(communities, u)
        communities_of_node_2 = find_all_communities_of_node(communities, v)

        if len(set(communities_of_node_1).intersection(set(communities_of_node_2))) == 0:            
            # my_metric
            # select_community_using_my_metric(G, u, v, communities, communities_of_node_1, communities_of_node_2)
            
            # #new_metric
            select_community_using_CNW(G, u, v, communities, communities_of_node_1, communities_of_node_2)
            
    sorted_communities = sorted(communities, key=len, reverse=True)
    #print(f"number of communities: {len(sorted_communities)}")
    index1 = 1

    while index1 < len(sorted_communities):
        index2 = index1 - 1
        while index2 >= 0:
            if len(set(sorted_communities[index1]).intersection(set(sorted_communities[index2]))) > (1/2) * len(sorted_communities[index1]):
                sorted_communities[index1] = set(sorted_communities[index1]).union(set(sorted_communities[index2]))
                sorted_communities.remove(sorted_communities[index2])
                index1 = index1 - 1
            elif len(sorted_communities[index1]) == 2 and len(set(sorted_communities[index1]).intersection(set(sorted_communities[index2]))) == (1/2) * len(sorted_communities[index1]):
                sorted_communities[index1] = set(sorted_communities[index1]).union(set(sorted_communities[index2]))
                sorted_communities.remove(sorted_communities[index2])
                index1 = index1 - 1
            index2 = index2 - 1
        index1 = index1 + 1
    #print(f"Number of sorted communities: {len(sorted_communities)}")
    return sorted_communities

def find_overlapping_nodes(sorted_communities):
    overlapping_nodes = []  # Ortak düğümleri saklamak için bir liste
    for index1 in range(len(sorted_communities)):
        for index2 in range(index1 + 1, len(sorted_communities)):
            current = sorted_communities[index1]
            other = sorted_communities[index2]
            common_nodes = current & other  # Ortak düğümleri bul
            if common_nodes:
                overlapping_nodes.append((index1, index2, common_nodes))  # İndekslerle birlikte sakla
    return overlapping_nodes


def my_algorithm_disjoint_communities(G):
    # `sorted_communities` oluşturuluyor
    sorted_communities = my_algorithm_overlapping_communities(G)
    #print(f"Sorted communities: {sorted_communities}")

    # `sorted_communities`'nin değiştirilmemiş bir kopyasını oluştur
    original_sorted_communities = [community.copy() for community in sorted_communities]

    # Ortak düğümleri bul
    overlapping_nodes = find_overlapping_nodes(sorted_communities)
    #print(f"Overlapping nodes with indices: {overlapping_nodes}")

    # Ortak düğümler üzerinde işlem yap
    for index1, index2, common_nodes in overlapping_nodes:
        #print(f"Processing common nodes between community {index1} and {index2}: {common_nodes}")

        for node in common_nodes:
            # Güncel toplulukları her zaman `sorted_communities` üzerinden al
            current = sorted_communities[index1]
            other = sorted_communities[index2]

            # Düğümün hala topluluklarda mevcut olup olmadığını kontrol et
            if node not in current or node not in other:
                continue  # Eğer düğüm çıkarılmışsa, işlem yapma

            neighbors_of_node = set(G.neighbors(node))

            # `calculate_CNW` ile katkıyı hesapla (değiştirilmemiş topluluklar üzerinden)
            metric_current, _ = calculate_CNW(G, node, original_sorted_communities, [index1], neighbors_of_node)
            metric_other, _ = calculate_CNW(G, node, original_sorted_communities, [index2], neighbors_of_node)

            #print(f"Node {node}: Metric Current: {metric_current}, Metric Other: {metric_other}")

            # Daha büyük katkı sağlayan topluluğu seç
            if metric_current >= metric_other:
                #print(f"Node {node} stays in community {index1}.")
                # `sorted_communities` üzerinden düğümü çıkar
                sorted_communities[index2] = sorted_communities[index2] - {node}
            else:
                #print(f"Node {node} moves to community {index2}.")
                # `sorted_communities` üzerinden düğümü çıkar
                sorted_communities[index1] = sorted_communities[index1] - {node}

    # Boş toplulukları kaldır
    sorted_communities = [community for community in sorted_communities if community]
    # print(f"Number of sorted communities disjoint: {len(sorted_communities)}")

    # Tüm toplulukları birleştir
    return sorted_communities