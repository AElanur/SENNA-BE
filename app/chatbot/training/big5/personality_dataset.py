import torch
from torch.utils.data import Dataset, DataLoader
from .tokenizer import text_to_indices, texts, labels, vocab

max_len = 32

class PersonalityDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len):
        self.data = [text_to_indices(text, vocab, max_len) for text in texts]
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids": torch.tensor(self.data[idx], dtype=torch.long),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long)
        }

dataset = PersonalityDataset(texts, labels, vocab, max_len)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)