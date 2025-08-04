import numpy as np

def shen_modularity(G, communities):
    """
    Normalized Shen modularity.
    Suitable for overlapping communities and weighted, undirected graphs.

    Q = (1 / 2m) * sum_i sum_{v,w in C_i} [ (1 / (O_v * O_w)) * (A_vw - (k_v * k_w)/(2m)) ]
    """
    m = G.size(weight='weight')
    degrees = dict(G.degree(weight='weight'))

    # Calculate the number of communities each node belongs to
    node_membership_count = {}
    for community in communities:
        for node in community:
            node_membership_count[node] = node_membership_count.get(node, 0) + 1

    Q = 0.0
    for community in communities:
        for v in community:
            for w in community:
                if v not in node_membership_count or w not in node_membership_count:
                    continue

                O_v = node_membership_count[v]
                O_w = node_membership_count[w]

                A_vw = G[v][w]['weight'] if G.has_edge(v, w) else 0.0
                k_v = degrees[v]
                k_w = degrees[w]

                Q += (1 / (O_v * O_w)) * (A_vw - (k_v * k_w) / (2 * m))

    return Q / (2 * m)


def compute_fuzzy_membership(communities):
    """
    communities: List[Set[int]]
    Output: {node: {community_id: membership_value}}
    """
    membership = {}
    node_community_counts = {}

    # Step 1: Calculate the number of communities each node belongs to
    for cid, comm in enumerate(communities):
        for node in comm:
            node_community_counts[node] = node_community_counts.get(node, 0) + 1

    # Assign a membership value of 1 / total communities of the node (assuming equal membership)
    for cid, comm in enumerate(communities):
        for node in comm:
            if node not in membership:
                membership[node] = {}
            membership[node][cid] = 1.0 / node_community_counts[node]

    return membership


def qoc(nxG, communities):
    """
    communities: List[Set[int]]
    G: a NetworkX graph (can be weighted or unweighted)

    Automatically extracts fuzzy memberships and calculates the fuzzy Q_oc modularity.
    """
    m = nxG.size(weight='weight')
    degrees = dict(nxG.degree(weight='weight'))
    fuzzy_membership = compute_fuzzy_membership(communities)

    Qoc = 0.0
    for i in nxG.nodes():
        for j in nxG.nodes():
            if i == j:
                continue

            A_ij = nxG[i][j]['weight'] if nxG.has_edge(i, j) else 0.0
            expected = degrees[i] * degrees[j] / (2 * m)

            mu_i = fuzzy_membership.get(i, {})
            mu_j = fuzzy_membership.get(j, {})

            # select the maximum of sqrt(min(μ)) according to common communities
            max_term = 0.0
            for c in set(mu_i) & set(mu_j):
                val = np.sqrt(min(mu_i[c], mu_j[c]))
                max_term = max(max_term, val)

            Qoc += (A_ij - expected) * max_term

    Qoc /= (2 * m)
    return Qoc