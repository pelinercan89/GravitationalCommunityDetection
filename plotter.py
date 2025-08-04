import my_globals, directory_manager
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import igraph as ig
import numpy as np

visual_style = {
    "bbox": (500, 500),
    "vertex_size": 50,
    "vertex_label_size": 35,
    "margin": 50,
    "vertex_color": "light blue"
}

def save_predicted_networks(results):
    for result in results.values():
        output_file = f"{directory_manager.OUTPUT_DIRECTORY}/{result.algorithm_name}/predicted/{result.algorithm_name}_{result.dataset_name}.png"
        clusters = ig.VertexCover(result.ig_graph, clusters=result.predicted_communities)
        
        vertex_labels = result.ig_graph.vs["label"] if "label" in result.ig_graph.vs.attributes() else result.ig_graph.vs["_nx_name"]
        edge_labels = result.ig_graph.es["weight"] if "weight" in result.ig_graph.es.attributes() else None
        ig.plot(clusters, output_file, **visual_style, mark_groups=True, inline=True, vertex_label=vertex_labels, layout=result.layout,edge_label=edge_labels)

               
def save_original_networks(datasets):
    for dataset in datasets:
        output_file = f"{directory_manager.OUTPUT_DIRECTORY}/original/{dataset.name}.png"
        clusters = ig.VertexCover(dataset.ig_graph, clusters=dataset.real_communities)
        
        vertex_labels = dataset.ig_graph.vs["label"] if "label" in dataset.ig_graph.vs.attributes() else dataset.ig_graph.vs["_nx_name"]
        edge_labels = dataset.ig_graph.es["weight"] if "w" in dataset.ig_graph.es.attributes() else None
        ig.plot(clusters, output_file, **visual_style, mark_groups=True, inline=True, vertex_label=vertex_labels, layout=dataset.layout, edge_label=edge_labels)

def plot_bar_chart(ax, X, data, colors, x_labels, y_label, file_name):
    gap = -0.20
    num_algorithms = len(my_globals.SELECTED_ALGORITHMS)
    
    if len(colors) < num_algorithms:
        raise ValueError("Not enough colors provided for the number of algorithms.")
    
    bars = []
    for i, (algorithm_name, color) in enumerate(zip(my_globals.SELECTED_ALGORITHMS.keys(), colors)):
        if len(X) != len(data[algorithm_name]):
            raise ValueError(f"Length of X ({len(X)}) does not match length of data for {algorithm_name} ({len(data[algorithm_name])}).")
        
        bar = ax.bar(X + gap, data[algorithm_name], color=color, width=0.20, label=algorithm_name) 
        bars.append(bar)
        gap += 0.20
    
    ax.set_xticks(X)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel(y_label)
    ax.legend()
    plt.savefig(file_name, bbox_inches='tight')
    plt.show()

def plot_data(results, datasets):
    metrics = ['qoc_modularity', 'mgh_nmi', 'f_score', 'my_modularity', 'runtime']
    y_labels = ['Modülarite', 'NMI', 'F-Skor', 'Kapsama', 'Çalışma Zamanı (ms)']
    file_names = ['modularity_results.png', 'NMI_results.png', 'f_score_results.png', 'my_modularity_results.png', 'runtime_results.png']
    
    my_dict = {algorithm_name: {metric: [] for metric in metrics} for algorithm_name in my_globals.SELECTED_ALGORITHMS.keys()}
    
    for algorithm_name in my_globals.SELECTED_ALGORITHMS.keys():
        for dataset in datasets:
            for metric in metrics:
                my_dict[algorithm_name][metric].append(getattr(results[(dataset.name, algorithm_name)], metric))
    
    X = np.arange(len(datasets))
    x_labels = [f'Network {i+1}' for i in range(len(datasets))]
    colors = ['purple', 'limegreen', 'blue', 'red', 'orange', 'cyan', 'magenta', 'yellow', 'black', 'brown']
    
    for metric, y_label, file_name in zip(metrics, y_labels, file_names):
        fig, ax = plt.subplots(figsize=(12, len(datasets)))
        output_file = f"{directory_manager.OUTPUT_DIRECTORY}/bar_charts/{file_name}"
        plot_bar_chart(ax, X, {algo: my_dict[algo][metric] for algo in my_globals.SELECTED_ALGORITHMS.keys()}, colors, x_labels, y_label, output_file)
  
def plot_image_subplot(ax, img_path, title=None, texts=None):
    img = mpimg.imread(img_path)
    ax.imshow(img)
    if title:
        ax.set_title(title)
    ax.axis('off')  # Hide the axis

    if texts:
        text_str = '\n'.join([f'{k}: {v:.2f}' for k, v in texts.items()])
        ax.text(1.05, 0.5, text_str, transform=ax.transAxes, fontsize=12, verticalalignment='center')

def plot_images_table(results):
    plt.rcParams["font.size"] = "15"  # Set the font size
    
    algorithms = set(algorithm for _, algorithm in results.keys())
    datasets = set(dataset for dataset, _ in results.keys())
    num_datasets = len(datasets)
    num_algorithms = len(algorithms)
    
    fig, axes = plt.subplots(num_datasets, num_algorithms + 1, figsize=(25, 25))  # Create a grid figure
    
    for i, dataset_name in enumerate(sorted(datasets)):
        # Plot the original graph
        ax = axes[i, 0]
        original_img_path = f"{directory_manager.OUTPUT_DIRECTORY}/original/{dataset_name}.png"
        plot_image_subplot(ax, original_img_path, title="Original")
        
        for j, algorithm_name in enumerate(sorted(algorithms)):
            ax = axes[i, j + 1]
            predicted_img_path = f"{directory_manager.OUTPUT_DIRECTORY}/{algorithm_name}/predicted/{algorithm_name}_{dataset_name}.png"
            texts = {
                'Modularity': results[(dataset_name, algorithm_name)].shen_modularity,
                'NMI': results[(dataset_name, algorithm_name)].mgh_nmi,
                'F-Score': results[(dataset_name, algorithm_name)].f_score,
                'Coverage': results[(dataset_name, algorithm_name)].my_modularity
            }
            plot_image_subplot(ax, predicted_img_path, title=algorithm_name, texts=texts)
    
    plt.tight_layout()
    output_file = f"{directory_manager.OUTPUT_DIRECTORY}/results.png"
    plt.savefig(output_file)
    plt.show()

def plot_original_and_predicted_networks(results, datasets, algorithm_name):
    for dataset in datasets:
        fig, axs = plt.subplots(1, 2, figsize=(14.5, 10.5))
        
        original_img_path = f"{directory_manager.OUTPUT_DIRECTORY}/original/{dataset.name}.png"
        predicted_img_path = f"{directory_manager.OUTPUT_DIRECTORY}/{algorithm_name}/predicted/{algorithm_name}_{dataset.name}.png"
        
        plot_image_subplot(axs[0], original_img_path, "Original")
        plot_image_subplot(axs[1], predicted_img_path, "Predicted")
        
        output_file = f"{directory_manager.OUTPUT_DIRECTORY}/{algorithm_name}/results/{algorithm_name}_{dataset.name}.png"
        plt.savefig(output_file)
        plt.show()
                
def plot_graphs(datasets, results):    
    # Only works if the graphs are of a size that can be visually examined
    for dataset in datasets:
        if len(dataset.nx_graph.nodes) > my_globals.MAXIMUM_GRAPH_SIZE:
            print(f"Graphs for dataset {dataset.name} are too big to plot.")
            return
    
    save_original_networks(datasets)
    for algo_name in my_globals.SELECTED_ALGORITHMS.keys(): 
        save_predicted_networks(results)       
        plot_original_and_predicted_networks(results, datasets, algo_name)
    plot_images_table(results)
