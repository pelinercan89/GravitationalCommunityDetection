import os, subprocess, shutil, psutil, sys
import math
import directory_manager

target = directory_manager.PROJECT_DIRECTORY + "/Data/LFRbenchmark/"

def terminate_process_by_name(exe_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == exe_name:
            process.terminate()
            process.wait()  # Ensure the process has terminated

def create_dataset_with_command(dataset_id, num_nodes, avg_degree, max_degree, mix_param, num_overlapped_nodes, membership_overlapped_nodes, timeout=60):
    command = (
        f"benchmark.exe -N {num_nodes} -k {avg_degree} -maxk {max_degree} "
        f"-muw {mix_param} -on {num_overlapped_nodes} -om {membership_overlapped_nodes}"
    )
    
    # Change directory
    os.chdir(directory_manager.PROJECT_DIRECTORY + "/LFRbenchmarks-main/weighted_undirected/")
    
    try:
        # Run command with timeout using Popen
        process = subprocess.Popen(command, shell=True)
        process.wait(timeout=timeout)
        
        # Copy the generated files
        src = directory_manager.PROJECT_DIRECTORY + "/LFRbenchmarks-main/weighted_undirected/"
        
        shutil.copy(f"{src}network.dat", f"{target}network{dataset_id}.edgelist")
        shutil.copy(f"{src}community.dat", f"{target}network{dataset_id}.dat")
        
        
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds.")
        # Terminate the process and its children
        terminate_process_by_name('benchmark.exe')
        sys.exit("Dataset cannot be generated.")

def convert_network_file_to_my_format(dataset_id):
    src_file_path = f"{target}network{dataset_id}.edgelist"
    
    with open(src_file_path, "r") as file:
        lines = file.readlines()
    
    with open(src_file_path, "w") as file:
        for line in lines:
            if line[0] == '#':
                continue
            words = line.split()
            if int(words[0]) < int(words[1]):
                # Ağırlık kontrolü yap ve 0'dan küçükse -1 ile çarp
                weight = math.ceil(float(words[2]))
                if weight < 0.1:
                    weight = 0.1  # Negatif ağırlığı pozitif yap
                file.write(f"{int(words[0])-1} {int(words[1])-1} {round(weight, 2)}\n")
 
def  convert_community_file_to_my_format(dataset_id):
    #convert to community list and starts from 0
    src_file_path = f"{target}network{dataset_id}.dat"
    
    with open(src_file_path, "r") as file:
        lines = file.readlines()
    
    community_size = max(int(com) for line in lines for com in line.split("\t")[1].split())
    community_list = [set() for _ in range(community_size)]
    
    for line in lines:
        words = line.split("\t")
        node = int(words[0]) - 1
        coms = words[1].split()
        for com in coms:
            community_list[int(com)-1].add(node)
    
    with open(src_file_path, "w") as file:
        file.write(str(community_list) + "\n")
    
def convert_generated_files_into_my_format(dataset_id):
    convert_network_file_to_my_format(dataset_id)
    convert_community_file_to_my_format(dataset_id)


def create_test_set(num_tests, num_nodes, avg_degree, max_degree, mix_param, num_overlapped_nodes, membership_overlapped_nodes):
    """
    num_tests: Kaç test seti oluşturulacak
    num_nodes: Düğüm sayısı
    avg_degree: Ortalama derece
    max_degree: Maksimum düğüm derecesi
    mix_param: Karışım parametresi
    num_overlapped_nodes: Örtüşen düğüm sayısı
    membership_overlapped_nodes: Örtüşen düğümlerin topluluk sayısı
    """
    
    for dataset_index in range(1, num_tests + 1):
        create_dataset_with_command(dataset_index, num_nodes, avg_degree, max_degree, mix_param, num_overlapped_nodes, membership_overlapped_nodes)
        convert_generated_files_into_my_format(dataset_index)
 
def generate_configured_datasets(enableOverlap):
    dataset_id = 1
    test_configs = []
    
    if enableOverlap:
        test_configs = [
            # (num_tests, num_nodes, avg_degree, max_degree, mix_param, on, om)
        
            (3, 500, 10, 30, 0.05, 30, 2),           
            (3, 1000, 10, 30, 0.1, 30, 2),         
        ]
    else:
        test_configs = [
            # (num_tests, num_nodes, avg_degree, max_degree, mix_param, on, om)
        
            (3, 500, 10, 30, 0.05, 0, 0),            
            (3, 1000, 10, 30, 0.1, 0, 0),          
        ]

    for (num_tests, num_nodes, avg_degree, max_degree, mu, on, om) in test_configs:
        for _ in range(num_tests):
            create_dataset_with_command(dataset_id, num_nodes, avg_degree, max_degree, mu, on, om)
            convert_generated_files_into_my_format(dataset_id)
            dataset_id += 1

    print("\nTüm veri setleri başarıyla üretildi ve kaydedildi.")




    
