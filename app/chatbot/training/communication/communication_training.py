import os
from .training_data.communication_data import CommunicationData
from app.util.dataset_reader import DatasetReader
from app.chatbot.training.model.model import get_tokenizer, get_model
from app.util.training_script import get_training_script
from ..config.dataset_type import DatasetType
from ..train_model import TrainModel


script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'training_data', 'communication_data')
os.makedirs(save_dir, exist_ok=True)

dataset_ini_path = get_training_script(DatasetType.COMMUNICATION_DATASET)
reader = DatasetReader(dataset_ini_path)
qa_pairs = reader.load_and_prepare_all_datasets()
tokenizer = get_tokenizer("t5-small")
model = get_model("t5-small")
dataset = CommunicationData(qa_pairs, tokenizer, max_length=64)

trainer = TrainModel(model, dataset, save_dir)
trainer.train()
trainer.save(tokenizer)
