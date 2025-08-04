import networkx as nx
import igraph as ig
from enum import Enum

# Define all algorithms and selected algorithms
ALL_ALGORITHMS = {
    "ego_networks": "Ego Networks",
    "lpanni": "LPANNI",
    "core_expansion": "Core Expansion",
    "my": "Proposed",
    "my_disjoint": "Proposed Disjoint"
}
SELECTED_ALGORITHMS = {}
SELECTED_DATASET_TYPE = None
MAXIMUM_GRAPH_SIZE = 200

class Dataset:
    def __init__(self):
        self.name = ""
        self.directory = ""
        self.nx_graph = nx.Graph()
        self.ig_graph = ig.Graph()
        self.layout = ig.Layout()
        self.real_communities = []            
        
class Result:
    def __init__(self):
        self.dataset_name = ""
        self.ig_graph = ig.Graph()
        self.layout = ig.Layout()
        self.real_communities = []
        self.number_of_real_communities = 0
        self.algorithm_name = ""
        self.predicted_communities = []
        self.number_of_pred_communities = 0
        self.runtime = 0.0
        self.shen_modularity = 0.0
        self.nmi_lfk = 0.0
        self.f_score = 0.0
        self.omega = 0.0
        self.qoc = 0.0
        # self.updated_F_Score = 0.0

    def __copy__(self):
        return Result()

    def set_dataset(self, dataset):
        self.dataset_name = dataset.name
        self.ig_graph = dataset.ig_graph
        self.layout = dataset.layout
        self.real_communities = dataset.real_communities

   
    def print_result(self):
        include_comparison_metrics = self.number_of_real_communities != 0
    
        data = [
            self.dataset_name,
            self.algorithm_name,
            self.number_of_pred_communities,
            f"{self.runtime:.3f}",
            f"{self.shen_modularity:.2f}",
            f"{self.qoc:.2f}",
        ]
        column_widths = [15, 12, 16, 10, 15, 15]
    
        if include_comparison_metrics:
            data += [
                self.number_of_real_communities,
                f"{self.nmi_lfk:.2f}",
                f"{self.omega:.2f}",
                f"{self.f_score:.2f}",
            ]
            column_widths += [16, 10, 10, 10]
    
        print("".join(f"{d:<{w}}" for d, w in zip(data, column_widths)))

def print_header(include_comparison_metrics=True):
    headers = [
        "dataset", "algorithm", "pred_coms", "runtime", "Q_shen", "Q_oc"
    ]
    column_widths = [15, 12, 16, 10, 15, 15]

    if include_comparison_metrics:
        headers += ["real_coms", "nmi_lfk", "omega", "f1_score"]
        column_widths += [16, 10, 10, 10]

    print("".join(f"{h:<{w}}" for h, w in zip(headers, column_widths)))



def select_algorithms(algorithm_keys): 
    for key in algorithm_keys: 
        if key in ALL_ALGORITHMS: 
            SELECTED_ALGORITHMS[key] = ALL_ALGORITHMS[key] 
        else:
            print(f"Algorithm key '{key}' not found in ALL_ALGORITHMS")
            
def select_all_algorithms():
    global SELECTED_ALGORITHMS
    SELECTED_ALGORITHMS = ALL_ALGORITHMS.copy()
    
class DatasetType(Enum):
    GROUND_TRUTH = "GroundTruth"
    WITHOUT_GROUND_TRUTH = "WithoutGroundTruth"
    LFR_BENCHMARK = "LFRbenchmark"

dataset_type_to_string = {
    DatasetType.GROUND_TRUTH: "GroundTruth",
    DatasetType.WITHOUT_GROUND_TRUTH: "WithoutGroundTruth",
    DatasetType.LFR_BENCHMARK: "LFRbenchmark"
}

def select_dataset_type(dataset_type):
    global SELECTED_DATASET_TYPE
    SELECTED_DATASET_TYPE = dataset_type

def get_selected_dataset_type():
    return dataset_type_to_string[SELECTED_DATASET_TYPE]
