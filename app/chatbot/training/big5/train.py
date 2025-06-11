import os

import torch
import torch.nn as nn
import torch.optim as optim
from .personality_dataset import dataset, dataloader
from .text_cnn import TextCNN
from .tokenizer import vocab

embed_dim = 100
num_classes = 5
num_epochs = 10
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = TextCNN(vocab_size=len(vocab), embed_dim=embed_dim, num_classes=num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in dataloader:
        inputs = batch["input_ids"].to(device)
        labels = batch["labels"].to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")


save_dir = "app/chatbot/training/big5/data/"
os.makedirs(save_dir, exist_ok=True)
torch.save(model.state_dict(), os.path.join(save_dir, "big5_dataset.pt"))
