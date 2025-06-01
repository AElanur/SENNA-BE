from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def get_tokenizer(model_name="t5-small"):
    return AutoTokenizer.from_pretrained(model_name)

def get_model(model_name="t5-small"):
    return AutoModelForSeq2SeqLM.from_pretrained(model_name)
