import json
import os
from collections import Counter

model_path = "app/chatbot/training/scripts/big5-personality.json"
path =  os.path.abspath(model_path)
with open(path, "r") as f:
    data = json.load(f)

texts = [item["input"] for item in data["data"]]
tokens = [ word.lower() for text in texts for word in text.split()]
vocab = { word: idx+1 for idx, (word, _ ) in enumerate(Counter(tokens).most_common())}

def text_to_indices(text, vocab, max_len=32):
    indices = [vocab.get(word.lower(), 0) for word in text.split()]

    return indices[:max_len] + [0]*(max_len - len(indices))

label_map = {"O": 0, "C": 1, "E": 2, "A": 3, "N": 4}
trait_to_personality = {item["trait_identifier"]: item["personality_id"] for item in data["traits"]}
trait_identifiers = sorted({item["trait_identifier"] for item in data["traits"]})
trait_label_map = {trait: idx for idx, trait in enumerate(trait_identifiers)}

texts = [item["input"] for item in data["data"]]
labels = [label_map[item["personality_id"]] for item in data["data"]]
identifiers = [trait_label_map[item["trait_identifier"]] for item in data["data"]]

