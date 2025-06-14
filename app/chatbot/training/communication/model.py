from transformers import AutoTokenizer, AutoModelForCausalLM


def get_tokenizer(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    return AutoTokenizer.from_pretrained(model_name)

def get_model(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    return AutoModelForCausalLM.from_pretrained(model_name)
