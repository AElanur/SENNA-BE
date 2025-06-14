from transformers import AutoTokenizer, AutoModelForCausalLM


def get_tokenizer(model_name="distilbert/distilgpt2"):
    return AutoTokenizer.from_pretrained(model_name)

def get_model(model_name="distilbert/distilgpt2"):
    return AutoModelForCausalLM.from_pretrained(model_name)
