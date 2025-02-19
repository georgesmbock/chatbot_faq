import json
from flask import Flask, request, jsonify
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model and tokenizer from file_nlp
model = BertForSequenceClassification.from_pretrained('../data/file_nlp')
tokenizer = BertTokenizer.from_pretrained('../data/file_nlp')


# Load the JSON file 
def loadJsonFile():
    with open('../data/dataset/faq_dataset.json', 'r') as file:
        return json.load(file)

# Call loadJsonFile function to loading JSON file
data = loadJsonFile()


# Similarity function
def similarite(query, corpus):
    Tf_vectorizer = TfidfVectorizer()
    matrix_Tf = Tf_vectorizer.fit_transform(corpus + query)
    similarity_query_and_corpus = cosine_similarity(matrix_Tf[-1], matrix_Tf[:-1])
    max_index = np.argmax(similarity_query_and_corpus)
    return max_index


# function to predict the category
def predict_question(quest):
    inputs = tokenizer(quest, return_tensors="pt", truncation=True, padding=True, max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class_idx = torch.argmax(logits, dim=1).item()

    # Labels of categories
    labels = ["shipping", "general", "produt", "return"]
    predicted_label = labels[predicted_class_idx]

    # Chech ID and answer for category predict
    document_data = [item for item in data if item['label'] == predicted_label]

    # List corpus of question of categority predicted
    corpus_question = [doc['question'] for doc in document_data]
    query = [quest]

    # Similarity
    index_of_similarity_question = similarite(query, corpus_question)

    # Return ID question and her reponse corresponding
    question_data = document_data[index_of_similarity_question]  
    return question_data['idQuestion'], question_data['answer'], predicted_label
