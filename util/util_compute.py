import torch
import numpy as np



def softmax(x):
    z = x - max(x)
    numerator = np.exp(z)
    denominator = np.sum(numerator)
    softmax = numerator/denominator
    return softmax


def predict_classification_causal(model, tokenizer, input_text, num_option, device):
    choices = ['A', 'B', 'C', 'D', 'E'][:num_option]
    choice_ids = [tokenizer.encode(choice)[-1] for choice in choices]
    with torch.no_grad():
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        input_ids = inputs["input_ids"]
        if model.config._name_or_path in ['aisingapore/sea-lion-7b-instruct', 'aisingapore/gemma2-9b-cpt-sea-lionv3-base'] :
            inputs.pop("token_type_ids")
        outputs = model(**inputs, labels=input_ids)
        last_token_logits = outputs.logits[:, -1, :]
        choice_logits = last_token_logits[:, choice_ids].detach().cpu().numpy()
        conf = softmax(choice_logits[0])
        pred = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}[np.argmax(choice_logits[0])]
    return conf, pred


def predict_classification_mt0(model, tokenizer, input_text, num_option, device):
    choices = ['A', 'B', 'C', 'D', 'E'][:num_option]
    choice_ids = [tokenizer.encode(choice)[0] for choice in choices]
    with torch.no_grad():
        start_token = tokenizer('<pad>', return_tensors="pt").to(device)
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        outputs = model(**inputs, decoder_input_ids=start_token['input_ids'])
        last_token_logits = outputs.logits[:, -1, :]
        choice_logits = last_token_logits[:, choice_ids].detach().cpu().numpy()
        conf = softmax(choice_logits[0])
        pred = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}[np.argmax(choice_logits[0])]
    return conf, pred

