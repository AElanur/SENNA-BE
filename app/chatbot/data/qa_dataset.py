from torch.utils.data import Dataset

class QADataset(Dataset):
    def __init__(self, qa_pairs, tokenizer):
        self.qa_pairs = qa_pairs
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.qa_pairs)

    def __getitem__(self, idx):
        item = self.qa_pairs[idx]

        question = self.tokenizer(item["question"], return_tensors="pt", padding="max_length", truncation=True)
        answer = self.tokenizer(item["answer"], return_tensors="pt", padding="max_length", truncation=True)
        return question, answer