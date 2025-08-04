__all__ = ['overlapping_community_detection', 'disjoint_community_detection']

def calculate_gravitational_weights(G):
    for u, v in G.edges():
        edge_weight = G[u][v]['weight']
        G[u][v]['weight'] = (G.degree(u) * G.degree(v)) / (edge_weight ** 2)

def add_node_to_community(communities, index, node):        
    communities[index] = communities[index].union({node})

    if {node} in communities:
        communities.remove({node})

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
    
def find_all_communities_of_node(communities, node):
    community_list = list()
    index = 0
    for community in communities:
        if node in community:
            community_list.append(index)
        index = index + 1
    return community_list

def overlapping_community_detection(G):
    #assign each node as a community
    communities = [set([n]) for n in G.nodes()]
    
    #find weights
    calculate_gravitational_weights(G)
    
    #sort edges according to their cosine similarities by decreasing order
    sorted_edge_list = sorted(G.edges(data=True), key=lambda t: t[2].get('weight'), reverse=True)

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
            select_community_using_CNW(G, u, v, communities, communities_of_node_1, communities_of_node_2)
    
    # finetune communities to merge small communities
    sorted_communities = sorted(communities, key=len, reverse=True)
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
        
    return sorted_communities

def find_overlapping_nodes(sorted_communities):
    # finds overlapping nodes and their indexes in different communities
    overlapping_nodes = []  
    for index1 in range(len(sorted_communities)):
        for index2 in range(index1 + 1, len(sorted_communities)):
            current = sorted_communities[index1]
            other = sorted_communities[index2]
            common_nodes = current & other  
            if common_nodes:
                overlapping_nodes.append((index1, index2, common_nodes)) 
    return overlapping_nodes

def disjoint_community_detection(G):
    sorted_communities = overlapping_community_detection(G)
    original_sorted_communities = [community.copy() for community in sorted_communities]

    # find overlapping nodes 
    overlapping_nodes = find_overlapping_nodes(sorted_communities)

    # remove overlapping nodes from the community which has a lower CNW
    for index1, index2, common_nodes in overlapping_nodes:
        for node in common_nodes:
            current = sorted_communities[index1]
            other = sorted_communities[index2]

            # check the node in communities
            if node not in current or node not in other:
                continue

            neighbors_of_node = set(G.neighbors(node))

            # calculate_CNW values
            metric_current, _ = calculate_CNW(G, node, original_sorted_communities, [index1], neighbors_of_node)
            metric_other, _ = calculate_CNW(G, node, original_sorted_communities, [index2], neighbors_of_node)

            # select the community with a higher CNW and remove the node from the community with lower CNW
            if metric_current >= metric_other:
                sorted_communities[index2] = sorted_communities[index2] - {node}
            else:
                sorted_communities[index1] = sorted_communities[index1] - {node}

    # If there is a community with all nodes are removed then remove the empty communities
    sorted_communities = [community for community in sorted_communities if community]

    return sorted_communities