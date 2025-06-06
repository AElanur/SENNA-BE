import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.util.dataset_reader import DatasetReader
from .training_data.classification_data import ClassificationData
from app.util.training_script import get_training_script
from ..config.dataset_type import DatasetType
from ..train_model import TrainModel

script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'training_data', 'classification_data')
os.makedirs(save_dir, exist_ok=True)

dataset_ini_path = get_training_script(DatasetType.CLASSIFIER_DATASET)
reader = DatasetReader(dataset_ini_path)
qa_pairs = reader.load_and_prepare_all_datasets()
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
dataset = ClassificationData(qa_pairs, tokenizer)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)

trainer = TrainModel(model, dataset, save_dir)
trainer.train()
trainer.save(tokenizer)
