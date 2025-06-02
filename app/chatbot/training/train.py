import torch
from data.data_set import load_and_prepare_dataset
from data.qa_dataset import QADataset
from model import get_tokenizer, get_model
from torch.utils.data import DataLoader
from torch.optim import AdamW

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
qa_pairs = load_and_prepare_dataset()
tokenizer = get_tokenizer("t5-small")
model = get_model("t5-small").to(device)

dataset = QADataset(qa_pairs, tokenizer, max_length=64)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
optimizer = AdamW(model.parameters(), lr=5e-5)

model.train()
for epoch in range(3):
    total_loss = 0
    for batch in dataloader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1} complete. Avg Loss: {avg_loss:.4f}")

model.save_pretrained("./finetuned-mental-health-chatbot")
tokenizer.save_pretrained("./finetuned-mental-health-chatbot")
