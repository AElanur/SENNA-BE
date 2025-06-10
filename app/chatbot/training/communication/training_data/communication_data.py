from torch.utils.data import Dataset

class CommunicationData(Dataset):
    def __init__(self, qa_pairs, tokenizer, max_length=64):
        self.qa_pairs = qa_pairs
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        print("Sample:", self.qa_pairs[:3])
        print("Total samples:", len(self.qa_pairs))
        return len(self.qa_pairs)

    def __getitem__(self, idx):
        item = self.qa_pairs[idx]
        input_text = item["input"]
        target_text = item["target"]

        input_enc = self.tokenizer(
            input_text, padding="max_length", truncation=True,
            max_length=self.max_length, return_tensors="pt"
        )
        target_enc = self.tokenizer(
            target_text, padding="max_length", truncation=True,
            max_length=self.max_length, return_tensors="pt"
        )
        return {
            "input_ids": input_enc["input_ids"].squeeze(0),
            "attention_mask": input_enc["attention_mask"].squeeze(0),
            "labels": target_enc["input_ids"].squeeze(0)
        }
