from torch.utils.data import Dataset
import torch

class CommunicationData(Dataset):
    def __init__(self, qa_pairs, tokenizer, max_length=256):
        self.qa_pairs = qa_pairs
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.qa_pairs)

    def __getitem__(self, idx):
        item = self.qa_pairs[idx]
        input_text = item["input"]
        target_text = item["target"]

        prompt = input_text.strip()
        answer = target_text.strip()
        full_text = f"{prompt}\n{answer}"

        encodings = self.tokenizer(
            full_text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )

        input_ids = encodings["input_ids"].squeeze(0)
        attention_mask = encodings["attention_mask"].squeeze(0)

        prompt_enc = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        prompt_len = prompt_enc["input_ids"].squeeze(0).ne(self.tokenizer.pad_token_id).sum().item()

        labels = input_ids.clone()
        labels[:prompt_len] = -100

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }
