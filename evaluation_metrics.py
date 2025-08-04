from cdlib import NodeClustering
import numpy as np

def my_modularity(graph, communities):
    """
    Klasik modülerlik (disjoint, yönsüz, ağırlıksız).
    Formül: Q = (m + in_edge - out_edge) / (2m)
    Sadece ayrık topluluklar için uygundur.
    """
    communities = NodeClustering(communities, graph=graph)
    if len(communities.communities) == 1:
        return 0

    communities = communities.to_node_community_map()

    edge_list = graph.edges()
    m = len(edge_list)

    in_edge = 0
    out_edge = 0

    for (u, v) in edge_list:
        if len(set(communities[v]).intersection(set(communities[u]))) > 0:
            in_edge = in_edge + 1
        else:
            out_edge = out_edge + 1

    my_modularity_score = (m + in_edge - out_edge)/(2*m)

    return my_modularity_score


# Modularity (ağırlıklı)
def modularity_weighted(G, communities):
    """
    Weighted Modularity (ağırlıklı, yönsüz, ayrık).
    Formül: Q = sum(A_uv - (k_u*k_v)/(2m)) / (2m)
    Sadece ayrık topluluklar için uygundur.
    """
    m = G.size(weight="weight")
    degrees = dict(G.degree(weight="weight"))
    Q = 0.0
    for community in communities:
        for u in community:
            for v in community:
                if u == v:
                    continue
                # A_uv = G[u][v]['weight'] if G.has_edge(u, v) else 0
                A_uv = G[u][v].get('weight', 1.0) if G.has_edge(u, v) else 0

                Q += A_uv - (degrees[u] * degrees[v]) / (2 * m)
    return Q / (2 * m) if m > 0 else 0

def shen_modularity(G, communities):
    """
    Normalize edilmiş Shen modularity.
    Overlapping topluluklar ve ağırlıklı, yönsüz graf için uygundur.

    Q = (1 / 2m) * sum_i sum_{v,w in C_i} [ (1 / (O_v * O_w)) * (A_vw - (k_v * k_w)/(2m)) ]
    """
    m = G.size(weight='weight')
    degrees = dict(G.degree(weight='weight'))

    # Her düğümün kaç topluluğa ait olduğunu hesapla
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

    # Adım 1: Hangi düğüm kaç topluluğa ait?
    for cid, comm in enumerate(communities):
        for node in comm:
            node_community_counts[node] = node_community_counts.get(node, 0) + 1

    # Adım 2: Üyelik değeri = 1 / toplam topluluk sayısı (eşit böl)
    for cid, comm in enumerate(communities):
        for node in comm:
            if node not in membership:
                membership[node] = {}
            membership[node][cid] = 1.0 / node_community_counts[node]

    return membership


def qoc(nxG, communities):
    """
    communities: List[Set[int]]
    G: networkx ağı (ağırlıklı veya ağırlıksız)

    Otomatik fuzzy membership çıkarır ve Q_oc fuzzy hesaplar
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

            # Ortak topluluklara göre min(μ)^0.5 içinden maksimumu bul
            max_term = 0.0
            for c in set(mu_i) & set(mu_j):
                val = np.sqrt(min(mu_i[c], mu_j[c]))
                max_term = max(max_term, val)

            Qoc += (A_ij - expected) * max_term

    Qoc /= (2 * m)
    return Qoc



# #----------------metrics için kullanılacak-------------------------

# # Inclusion Rate hesaplama
# def inclusion_rate(true_partition, pred_partition):
#     """
#     Inclusion Rate (overlapping, ağırlıksız, yönsüz).
#     Formül: max_precision * |Ri| / toplam |Ri|
#     Hem ayrık hem örtüşen topluluklar için uygundur.
#     """
#     inclusion_rates = []
#     for Ri in pred_partition:
#         max_precision = max(len(set(Ri).intersection(set(Gj))) / len(Ri) for Gj in true_partition)
#         inclusion_rates.append(max_precision * len(Ri))
#     return sum(inclusion_rates) / sum(len(Ri) for Ri in pred_partition)

# # Coverage Rate hesaplama
# def coverage_rate(true_partition, pred_partition):
#     """
#     Coverage Rate (overlapping, ağırlıksız, yönsüz).
#     Formül: max_recall * |Gj| / toplam |Gj|
#     Hem ayrık hem örtüşen topluluklar için uygundur.
#     """
#     coverage_rates = []
#     for Gj in true_partition:
#         max_recall = max(len(set(Ri).intersection(set(Gj))) / len(Gj) for Ri in pred_partition)
#         coverage_rates.append(max_recall * len(Gj))
#     return sum(coverage_rates) / sum(len(Gj) for Gj in true_partition)


# # Güncellenmiş F Updated hesaplama
# def f_updated(true_partition, pred_partition):
#     """
#     F-updated (overlapping, ağırlıksız, yönsüz).
#     Formül: 2 * inclusion * coverage / (inclusion + coverage)
#     Hem ayrık hem örtüşen topluluklar için uygundur.
#     """
#     inclusion = inclusion_rate(true_partition, pred_partition)
#     coverage = coverage_rate(true_partition, pred_partition)
#     return (2 * inclusion * coverage) / (inclusion + coverage) if inclusion > 0 and coverage > 0 else 0


