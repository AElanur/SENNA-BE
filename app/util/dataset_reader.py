import os
import configparser
import re
import json
from typing import List, Dict

from datasets import load_dataset
from ..util.data_parser import parse_regex, parse_dialog_list, parse_classification


class DatasetReader:
    def __init__(self, dataset_path, recipe_path=None, trained_file="trained.txt"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dataset_path = dataset_path
        self.recipe_path = recipe_path or os.path.join(base_dir, "..", "config", "parsing_recipe.json")
        self.trained_file = trained_file
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

    def load_trained_list(self) -> set:
        if not os.path.exists(self.trained_file):
            return set()
        with open(self.trained_file, "r") as f:
            return set(line.strip() for line in f if line.strip())

    def save_trained_list(self, trained: set):
        with open(self.trained_file, "w") as f:
            for name in sorted(trained):
                f.write(f"{name}\n")

    @staticmethod
    def parse_row(row, recipe) -> List[Dict[str, str]]:
        if recipe["type"] == "regex":
            return parse_regex(row, recipe)
        elif recipe["type"] == "dialog_list":
            return parse_dialog_list(row, recipe)
        elif recipe["type"] in ["classification", "text_classification"]:
            return parse_classification(row, recipe)
        else:
            raise ValueError(f"Unknown parsing type: {recipe['type']}")

    def load_and_prepare_all_datasets(self) -> List[Dict[str, str]]:
        training_datasets = self.get_datasets_from_ini()
        qa_pairs = []
        for ds in training_datasets:
            raw_dataset = load_dataset(ds["url"], split="train", trust_remote_code=True)
            print(f"Loaded dataset {ds['url']} with {len(raw_dataset)} samples")
            recipe = self.parsing_recipes.get(ds["parser"])
            if recipe is None:
                raise ValueError(f"No parsing recipe found for parser key: {ds['parser']}")
            for row in raw_dataset:
                qa_pairs.extend(self.parse_row(row, recipe))
        return qa_pairs
