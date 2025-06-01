from data.data_set import load_and_prepare_dataset
from data.qa_dataset import QADataset
from model import get_tokenizer, get_model
from torch.utils.data import DataLoader
from torch.optim import AdamW

qa_pairs = load_and_prepare_dataset()
tokenizer = get_tokenizer()
model = get_model()

dataset = QADataset(qa_pairs, tokenizer)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
optimizer = AdamW(model.parameters(), lr=5e-5)
model.train()
for epoch in range(3):
    for questions, answers in dataloader:
        input_ids = questions['input_ids'].squeeze(1)
        attention_mask = questions['attention_mask'].squeeze(1)
        labels = answers['input_ids'].squeeze(1)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print(f"Epoch {epoch+1} complete. Loss: {loss.item()}")




