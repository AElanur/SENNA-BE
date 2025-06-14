import os

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_training_script(script):
    return os.path.join(base_dir, "..", "config", f'{script}.ini')

def get_trained_scripts():
    return os.path.join(base_dir, "..", "config", "trained_datasets.txt")
