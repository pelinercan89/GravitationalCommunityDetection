import my_globals,  reader, algorithm_executer, plotter, directory_manager,dataset_generator

def main():      
    
    # Select a dataset
    # Test on synthetic networks
    # Enter parameters manually: num_tests, num_nodes, avg_degree, max_degree, mix_param, num_overlapped_nodes, membership_overlapped_nodes):
    # dataset_generator.create_test_set(5, 500, 15, 50, 0.2, 30, 2)  
    # Enter parameters automatically:
    # dataset_generator.generate_configured_datasets(False)
    
    # Test on LFR networks
    my_globals.select_dataset_type(my_globals.DatasetType.LFR_BENCHMARK)   
    # Test on real networks
    # my_globals.select_dataset_type(my_globals.DatasetType.GROUND_TRUTH)
    # Test on datasets without ground truth
    # my_globals.select_dataset_type(my_globals.DatasetType.WITHOUT_GROUND_TRUTH)
    
    # get the dataset
    datasets = reader.read_datasets()    

    # Select algorithms
    # algorithm_keys_to_select = ["gravitational"]#"ego_networks"] 
    algorithm_keys_to_select = ["gravitational_disjoint"]#"ego_networks"] 
    
    my_globals.select_algorithms(algorithm_keys_to_select)
    #my_globals.select_all_algorithms()
    
    # Clean directory    
    directory_manager.clean_output_directory()
    # Create directory for results    
    directory_manager.create_directories()
    
    # Run algorşthm on datasets
    results = algorithm_executer.run_algorithms_on_datasets(datasets)
    
    # Plot graphs (Only call if the graphs are of a size that can be visually examined)
    # plotter.plot_graphs(datasets, results)
        
    # Plot bar charts
    # plotter.plot_data(results, datasets)
   
main()
