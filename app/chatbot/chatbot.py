import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

class Chatbot:
    def __init__(self, model_path="app/chatbot/finetuned-mental-health-chatbot", max_length=256):
        abs_model_path = os.path.abspath(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(abs_model_path, local_files_only=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(abs_model_path, local_files_only=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_length = max_length

    def send_message(self, user_message):
        input_text = f"question: {user_message}"
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=self.max_length
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)
        with torch.no_grad():
            output = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=self.max_length,
                num_beams=4,
                early_stopping=True
            )
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

