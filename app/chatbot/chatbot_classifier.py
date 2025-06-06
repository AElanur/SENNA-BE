import os
from sympy.printing.pytorch import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ChatbotClassifier:
    def __init__(self, model_path, max_length):
        abs_classifier_path = os.path.abspath(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(abs_classifier_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(abs_classifier_path, local_files_only=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_length = max_length

    def classify_message(self, user_message):
        inputs = self.tokenizer(
            user_message,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=self.max_length
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        with torch.no_grad():
            logits = self.model(input_ids=input_ids, attention_mask=attention_mask).logits
            probs = torch.nn.functional.softmax(logits, dim=1)
            predicted_class = torch.argmax(probs, dim=1).item()
        return predicted_class, probs.cpu().numpy().tolist()[0]
