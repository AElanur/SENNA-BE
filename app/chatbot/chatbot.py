import os
from sympy.printing.pytorch import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Chatbot:
    def __init__(self, model_path, max_length):
        abs_model_path = os.path.abspath(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(abs_model_path, local_files_only=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(abs_model_path, local_files_only=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_length = max_length

    @staticmethod
    def check_message_history(conversation_history):
        formatted_history = ""
        for turn in conversation_history:
            formatted_history += f"{turn['input']}\n"
        return formatted_history

    @staticmethod
    def format_conversation_natural(conversation_history):
        lines = []
        for idx, turn in enumerate(conversation_history):
            if 'input' in turn:
                lines.append(f"User: {turn['input'].strip()}")
            if 'target' in turn:
                lines.append(f"Bot: {turn['target'].strip()}")
        return "\n".join(lines)

    def generate_message(self, conversation_history, predicted_class=None):
        history_window = conversation_history[-4:]
        input_text = self.format_conversation_natural(history_window)
        # if predicted_class is not None:
        #     input_text = f"[CLASS_{predicted_class}]\n{input_text}"

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
                early_stopping=True,
                no_repeat_ngram_size=3,
                temperature=0.8,
                top_p=0.9,
                do_sample=True
            )
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

