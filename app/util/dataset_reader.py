import os
import configparser
import re
import json
from typing import List, Dict
from datasets import load_dataset

class DatasetReader:
    def __init__(self, dataset_path, recipe_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_path = dataset_path
        self.recipe_path = recipe_path or os.path.join(base_dir, "..", "config", "parsing_recipe.json")
        with open(self.recipe_path, "r") as f:
            self.parsing_recipes = json.load(f)

    def get_datasets_from_ini(self, section='training') -> List[Dict[str, str]]:
        config = configparser.ConfigParser()
        config.read(self.dataset_path)
        if section not in config:
            raise ValueError(f"Section [{section}] not found in {self.dataset_path}")
        datasets = []
        for k, v in config[section].items():
            dataset_url, parser_key = [x.strip() for x in v.split('|')]
            datasets.append({"url": dataset_url, "parser": parser_key})
        return datasets

    def parse_row(self, row, recipe) -> List[Dict[str, str]]:
        if recipe["type"] == "regex":
            text = row.get('text', '')
            match = re.match(recipe["pattern"], text, re.DOTALL)
            if match:
                return [{
                    recipe["fields"][0]: match.group(1).strip(),
                    recipe["fields"][1]: match.group(2).strip()
                }]
            return []
        elif recipe["type"] == "dialog_list":
            qa_pairs = []
            dialog_field = recipe.get("dialog_field", "dialog")
            dialog = row.get(dialog_field, [])
            if not dialog:
                return []
            utterances = [
                turn.get('content', '').strip() if isinstance(turn, dict) and 'content' in turn else str(turn).strip()
                for turn in dialog
            ]
            # Optionally, filter by role here if needed
            for i in range(len(utterances) - 1):
                qa_pairs.append({
                    "question": utterances[i],
                    "answer": utterances[i + 1]
                })
            return qa_pairs
        elif recipe["type"] in ["classification", "text_classification"]:
            fields = recipe.get("fields", [])
            if not all(field in row for field in fields):
                return []
            return [{
                "question": str(row[fields[0]]).strip(),
                "answer": str(row[fields[1]]).strip()
            }]
        else:
            raise ValueError(f"Unknown parsing type: {recipe['type']}")

    def load_and_prepare_all_datasets(self) -> List[Dict[str, str]]:
        datasets = self.get_datasets_from_ini()
        qa_pairs = []
        for ds in datasets:
            raw_dataset = load_dataset(ds["url"], split="train", trust_remote_code=True)
            recipe = self.parsing_recipes.get(ds["parser"])
            if recipe is None:
                raise ValueError(f"No parsing recipe found for parser key: {ds['parser']}")
            for row in raw_dataset:
                qa_pairs.extend(self.parse_row(row, recipe))
        return qa_pairs
