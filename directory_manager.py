import os
import shutil
import my_globals

# Define the directory
PROJECT_DIRECTORY = os.getcwd()
OUTPUT_DIRECTORY = None
DATASET_DIRECTORY = None

def set_output_directory(selected_dataset_type):
    global OUTPUT_DIRECTORY
    OUTPUT_DIRECTORY = f"{PROJECT_DIRECTORY}/Outputs/{my_globals.get_selected_dataset_type()}"

def set_dataset_directory(selected_dataset_type):
    global DATASET_DIRECTORY
    DATASET_DIRECTORY = f"{PROJECT_DIRECTORY}/Data/{my_globals.get_selected_dataset_type()}"

def create_result_directories(selected_algorithms):
    subdirectories = ["predicted", "results"]
    base_directories = ["original", "bar_charts"]
    
    # Create base directories
    for base_dir in base_directories:
        os.makedirs(os.path.join(OUTPUT_DIRECTORY, base_dir), exist_ok=True)
    
    # Create algorithm-specific subdirectories
    for algorithm_name in selected_algorithms.keys():
        for subdirectory in subdirectories:
            os.makedirs(os.path.join(OUTPUT_DIRECTORY, algorithm_name, subdirectory), exist_ok=True)

def create_directories():
    set_output_directory(my_globals.SELECTED_DATASET_TYPE)
    set_dataset_directory(my_globals.SELECTED_DATASET_TYPE)
    create_result_directories(my_globals.SELECTED_ALGORITHMS)
    
def clean_output_directory():
    output_directory = os.path.join(PROJECT_DIRECTORY, 'Outputs')
    
    # Check if the directory exists
    if os.path.exists(output_directory):
        # Iterate over all files and subdirectories in the directory
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            try:
                # Remove files and subdirectories
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f'The directory {output_directory} does not exist.')
