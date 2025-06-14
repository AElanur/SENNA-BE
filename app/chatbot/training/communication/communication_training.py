import os
from app.chatbot.training.communication.communication_data import CommunicationData
from app.util.dataset_reader import DatasetReader
from app.chatbot.training.communication.model import get_tokenizer, get_model
from app.util.training_script import get_training_script
from ..train_model import TrainModel

script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'training_data')
os.makedirs(save_dir, exist_ok=True)

dataset_ini_path = get_training_script("communication_dataset")
reader = DatasetReader(dataset_ini_path)
qa_pairs = reader.load_and_prepare_all_datasets()

model_name = "distilgpt2"

tokenizer = get_tokenizer(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = get_model(model_name)

dataset = CommunicationData(qa_pairs, tokenizer, max_length=256)

trainer = TrainModel(model, dataset, save_dir)
trainer.train()
trainer.save(tokenizer)
