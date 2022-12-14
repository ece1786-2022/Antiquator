# -*- coding: utf-8 -*-
"""GPT2 Shakespeare

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X7VfxnO5FQXpSZe1ru2lAGlsPrqfiC4I
"""

!pip install transformers

from transformers import AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, GPT2LMHeadModel, AdamW

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import random

from tqdm.auto import tqdm

input_data = pd.read_csv('/content/data_f.txt', sep='\n', names=['Input'])

output_data = pd.read_csv('/content/label_f.txt', sep='\n', names=['Output'])

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

#input_data['Input'][0]
#output_data['Output'][0]

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id).to(device)

tokenizer.pad_token = tokenizer.eos_token

input_dataset = []
output_dataset = []

for row in input_data['Input']:
    input_dataset.append(row)

for row in output_data['Output']:
    output_dataset.append(row)

print(len(input_dataset))
print(len(output_dataset))

input_dataset[:5]

output_dataset[:5]

class ShakespeareDataset(Dataset):

    def __init__(self, input_encodings, output_encodings):
        self.input_encodings = input_encodings
        self.output_encodings = output_encodings
        #self.max_length = max(len(self.input_encodings['input_ids']) , len(self.output_encodings['input_ids']))

    def __getitem__(self, index):
        
        x = {key: torch.tensor(val[index]) for key,val in self.input_encodings.items()}
        y = {key: torch.tensor(val[index]) for key,val in self.output_encodings.items()}
        return x,y

    def __len__(self):
        return len(self.input_encodings['input_ids'])
        #return self.max_length

train_dataset = ShakespeareDataset(tokenizer(input_dataset[:5000], truncation=True, padding=True) , tokenizer(output_dataset[:5000], truncation=True, padding=True))
val_dataset = ShakespeareDataset(tokenizer(input_dataset[:5000], truncation=True, padding=True) , tokenizer(output_dataset[:5000], truncation=True, padding=True))

len(train_dataset)

train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True)

val_dataloader = DataLoader(val_dataset, batch_size=1, shuffle=True)

len(train_dataloader)

optimizer = AdamW(model.parameters(), lr=2e-5)

loss = 0
epochs = 5

for epoch in range(epochs):

    print(f"Training epoch {epoch}")
    print(loss)

    for batch in tqdm(train_dataloader):
        x,y = batch
        input_ids = x['input_ids'].to(device)
        attention_mask = x['attention_mask'].to(device)
        labels= y['input_ids'].to(device)
        #print(labels.shape)
        #print(batch)
        labels = labels[:,:input_ids.shape[-1]]
        outputs = model(input_ids=input_ids, labels=labels)
        #outputs = model(x['input_ids'],y['input_ids'])
        loss = outputs.loss
        loss.backward()

        optimizer.step()

        optimizer.zero_grad()



