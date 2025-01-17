# -*- coding: utf-8 -*-
"""ELMO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1veJyKcDjNl9_OOmh1mvCGjOnYJ5QmqGt
"""

import tensorflow_hub as hub
import tensorflow as tf

import pandas as pd
import numpy as np

elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)

def Elmo_Embedding(text=[""]):
 
  embeddings = elmo(text, signature="default", as_dict=True)["elmo"]

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())
    
    return sess.run(tf.reduce_mean(embeddings,1))

def Calculate_Elmo_Embedding(Input_Data_filepath, colname="Caption_Tokens", Output_Data_filepath=""):
    
  Data = pd.read_csv(Input_Data_filepath)
  Data_Elmo_Embeddings = []

  for row in range(Data.shape[0]):
    Row_text = Data.iloc[row][colname]
    text = [Row_text]

    text_avg_Embedding = Elmo_Embedding(text)
    Data_Elmo_Embeddings.append(text_avg_Embedding)

  Data_Text = Data[[colname]]
  Data_Labels = Data[["Label"]]
  Data_Embeddings = pd.DataFrame(Data_Elmo_Embeddings)
  
  Text_Embedding_Map = pd.concat([Data_Text,Data_Embeddings,Data_Labels], axis=1)

  if Output_Data_filepath:
    Text_Embedding_Map.to_csv(Output_Data_filepath)
  
  return Text_Embedding_Map

Text_Embedding_Map = Calculate_Elmo_Embedding("/content/Final_Labeled_Data.csv", "Caption_Tokens", "/content/Data_Elmo_Embeddings.csv")
print(Text_Embedding_Map)