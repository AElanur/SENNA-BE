import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW

class TrainModel:
    def __init__(self, model, dataset, save_dir, batch_size=8, lr=5e-5, epochs=3):
        self.dataset = dataset
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.save_dir = save_dir
        self.batch_size = batch_size
        self.lr = lr
        self.epochs = epochs
        self.optimizer = AdamW(self.model.parameters(), lr=self.lr)
        self.dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)

    def train(self):
        self.print_device_usage()
        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            for batch in self.dataloader:
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["labels"].to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                loss = outputs.loss
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            avg_loss = total_loss / len(self.dataloader)
            print(f"Epoch {epoch+1} complete. Avg Loss: {avg_loss:.4f}")

    def save(self, tokenizer=None):
        self.model.save_pretrained(self.save_dir)
        if tokenizer:
            tokenizer.save_pretrained(self.save_dir)

    @staticmethod
    def print_device_usage():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", device)