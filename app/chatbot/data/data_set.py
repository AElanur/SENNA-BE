from datasets import load_dataset
import re

def load_and_prepare_dataset():
    raw_dataset = load_dataset("heliosbrahma/mental_health_chatbot_dataset", split="train")
    qa_pairs = []
    for row in raw_dataset:
        text = row['text']
        match = re.match(r"<HUMAN>:\s*(.*?)\n<ASSISTANT>:\s*(.*)", text, re.DOTALL)
        if match:
            qa_pairs.append({
                "question": match.group(1).strip(),
                "answer": match.group(2).strip()
            })
    return qa_pairs

