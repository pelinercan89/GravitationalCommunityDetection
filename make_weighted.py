import os
import networkx as nx
import random
import directory_manager
    
def give_weights():
    directory = f"{directory_manager.PROJECT_DIRECTORY}/Data/GiveWeights"
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
                    
            if file_name.endswith(".gml"): 
                G = nx.read_gml(f"{directory}/{file_name}", label=None)
                
                # assign random weight to each edge
                max_degree = max(dict(G.degree()).values())
                for u, v in G.edges():
                    G[u][v]['weight'] = random.randint(1, max_degree + 5)
                    
                output = f"{directory}/Weighted/"
                if not os.path.exists(output):  
                    os.makedirs(output)
                nx.write_gml(G, f"{output}/weighted_{file_name}")
              
give_weights()               
