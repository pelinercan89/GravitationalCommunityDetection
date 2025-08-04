import time
import my_globals
import evaluation_metrics
import cdlib.evaluation as eval
import community_detection as gravitational
import copy

from cdlib import algorithms, NodeClustering

# Initialize result object
result = my_globals.Result()

# Define algorithm functions
algorithm_functions = {
    "core_expansion": algorithms.core_expansion,
    "ego_networks": algorithms.ego_networks,
    "lpanni": algorithms.lpanni,
    "percomvc": algorithms.percomvc,
    "girvan_newman": lambda nxG: algorithms.girvan_newman(nxG, 1),
    "greedy_modularity": algorithms.greedy_modularity,
    "louvain": algorithms.louvain,
    "k_clique": lambda nxG: algorithms.kclique(nxG, 3),
    "fluid_communities": lambda nxG: algorithms.async_fluid(nxG, k=4),
    "walktrap": algorithms.walktrap,
    "label_propagation": algorithms.label_propagation
}

# Run algorithms and return a list of communities
def run_algorithm(nxG, algorithm_name, real_communities=None):
    
    originalG = copy.deepcopy(nxG)
    
    if algorithm_name == "gravitational":
        start_time = time.perf_counter()
        predicted_communities = gravitational.overlapping_community_detection(nxG)
        end_time = time.perf_counter()
        predicted_clusters = NodeClustering(predicted_communities, graph=None)
    elif algorithm_name == "gravitational_disjoint":
        start_time = time.perf_counter()
        predicted_communities = gravitational.disjoint_community_detection(nxG)
        end_time = time.perf_counter()
        predicted_clusters = NodeClustering(predicted_communities, graph=None)
    else:
        start_time = time.perf_counter()
        predicted_clusters = algorithm_functions[algorithm_name](nxG)
        end_time = time.perf_counter()
        predicted_communities = list(map(set, set(map(frozenset, predicted_clusters.communities))))

    result = my_globals.Result()
    
    # Set communities
    result.predicted_communities = predicted_communities

    # Set time
    result.runtime = round((end_time - start_time), 4)

    # Set number of communities    
    result.number_of_pred_communities = len(predicted_communities)

    # Set modularities
    result.shen_modularity = evaluation_metrics.shen_modularity(originalG, predicted_communities)
    result.qoc = evaluation_metrics.qoc(originalG, predicted_communities)
             
    # Set NMI, Omega and F-score
    if real_communities:
        result.real_communities = real_communities
        real_clusters = NodeClustering(real_communities, graph=None)
        result.real_clusters = real_clusters        
        result.number_of_real_communities = len(real_communities)
              
        true_nc = NodeClustering(real_communities, graph=nxG, method_name="ground_truth", overlap=True)
        pred_nc = NodeClustering(predicted_communities, graph=nxG, method_name="predicted", overlap=True)
  
        result.nmi_lfk = eval.overlapping_normalized_mutual_information_LFK(true_nc, pred_nc).score
        result.omega = eval.omega(true_nc, pred_nc).score
        result.f_score = eval.f1(true_nc, pred_nc).score     
                
    return result

def run_algorithms_on_datasets(datasets):
    results = {}
    
    if my_globals.get_selected_dataset_type() == 'WithoutGroundTruth':
        my_globals.print_header(False)
    else:
        my_globals.print_header(True)
    
    for dataset in datasets:
        for algo_name in my_globals.SELECTED_ALGORITHMS.keys():
            result = copy.deepcopy(run_algorithm(dataset.nx_graph, algo_name, dataset.real_communities))
            result.set_dataset(dataset)
            result.algorithm_name = algo_name
            
            results[(dataset.name, algo_name)] = result   
            result.print_result()
    return results
