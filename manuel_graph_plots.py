import matplotlib.pyplot as plt
import igraph as ig
import numpy as np

# **Grafiği oluştur**
g = ig.Graph()
# #örnek 1 baş
# g.add_vertices(["A", "B", "C", "D", "E", "F", "G", "H"])
# g.add_edges([
#     ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("C", "E"), 
#     ("C", "F"), ("E", "G"), ("G", "F"), ("E", "H")
# ])

# **Kenar ağırlıkları**
# weights = [10, 2.5, 2.2, 2, 3, 1.6, 3.3, 1.5, 1.4]
# g.es["weight"] = weights

# **Düğümlerin konumlarını belirle**
# layout_dict = {
#     'A': (-2, 0),
#     'B': (-4, -1),
#     'C': (0, -1),
#     'D': (-4, 1),
#     'E': (0, 1),
#     'F': (4, -1),
#     'G': (4, 1),
#     'H': (1, 2)
# }
# layout = ig.Layout([layout_dict[v] for v in g.vs["name"]])

# **Örtüşen Toplulukları Belirleme**
# community_groups = [["A", "B", "C", "D", "E", "H"], ["C", "E", "F", "G"]]
# #örnek 1 son

# örnek 2 baş
g.add_vertices(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
g.add_edges([
    ("A", "B"), ("A", "E"), ("A", "H"), ("B", "C"), ("B", "E"), ("B", "F"), ("B", "I"), ("C", "D"), ("C", "F"),
    ("C", "G"), ("D", "G"), ("D", "K"), ("E", "H"), ("E", "I"), ("F", "I"), ("F", "J"), ("F", "G"), ("G", "J"),
    ("G", "K"), ("J", "I"), ("J", "K")
])

# **Kenar ağırlıkları**
weights = [2, 6, 5, 1, 5, 4, 3, 3, 3, 6, 4, 1, 1, 2, 6, 8, 2, 9, 3, 2, 4]
g.es["weight"] = weights

# **Düğüm konumları**
layout_dict = {
    "A": (-3, -2), "B": (-1, -2), "C": (1, -2), "D": (3, -2),
    "E": (-2, 0), "F": (0, 0), "G": (2, 0), "H": (-3, 2),
    "I": (-1, 2), "J": (1, 2), "K": (3, 2)
}
layout = ig.Layout([layout_dict[v] for v in g.vs["name"]])

# **Örtüşen Toplulukları Belirleme**
#community_groups = [["A", "B", "C", "E", "F", "H", "I", "J"], ["C", "D", "F", "G"],["D", "G", "J", "K"]]

# **Ayrık Toplulukları Belirleme**
community_groups = [["A", "B", "C", "E", "F", "H", "I", "J"], ["D", "G", "K"]]
# örnek 2 son

# **mark_groups için indeks listesi oluştur**
group_indices = [[g.vs.find(node).index for node in group] for group in community_groups]
clusters = ig.VertexCover(g, clusters=group_indices)

# **Grafiği kaydet**
output_file = "./Makale/Grafikler/new_plot.png"

ig.plot(
    g, #clusters,  # **Grafiği çiziyoruz**
    target=output_file,  
    layout=layout,
    mark_groups=True,  # **Çerçeveleri düzgün oluştur**
    edge_label=g.es['weight'],  # Kenar ağırlıklarını göster
    vertex_label=g.vs["name"],  # Düğüm etiketlerini göster
    vertex_size=50, 
    edge_label_size=20,
    vertex_label_size=20,
    vertex_color="lightblue",
    bbox=(600, 400),
    margin=100
)

# **Kaydedilen resmi göster**
img = plt.imread(output_file)
plt.figure(figsize=(6, 6))
plt.imshow(img)
plt.axis('off')  
plt.show()