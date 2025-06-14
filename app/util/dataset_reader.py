import os
import configparser
import json
from typing import List, Dict

from datasets import load_dataset
from ..util.data_parser import parse_dialog_list

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

    @staticmethod
    def parse_row(row, recipe) -> List[Dict[str, str]]:
        if recipe["type"] == "dialog_list":
            return parse_dialog_list(row, recipe)
        else:
            raise ValueError(f"Unknown parsing type: {recipe['type']}")

    def load_and_prepare_all_datasets(self) -> List[Dict[str, str]]:
        training_datasets = self.get_datasets_from_ini()
        qa_pairs = []
        for ds in training_datasets:
            raw_dataset = load_dataset(ds["url"], split="train", trust_remote_code=True)
            recipe = self.parsing_recipes.get(ds["parser"])
            if recipe is None:
                raise ValueError(f"No parsing recipe found for parser key: {ds['parser']}")
            for row in raw_dataset:
                qa_pairs.extend(self.parse_row(row, recipe))

        return self.remove_duplicate_pairs_from_dataset(qa_pairs)

    @staticmethod
    def remove_duplicate_pairs_from_dataset(qa_pairs):
        seen = set()
        unique_qa_pairs = []
        for pair in qa_pairs:
            key = (pair["input"].strip(), pair["target"].strip())
            if key not in seen:
                seen.add(key)
                unique_qa_pairs.append(pair)
            else:
                print(f"Duplicate pair found: {pair}")
        return unique_qa_pairs
