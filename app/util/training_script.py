import os
from app.chatbot.training.config.dataset_type import DatasetType

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_training_script(script: DatasetType):
    return os.path.join(base_dir, "..", "config", f'{script.value}.ini')


