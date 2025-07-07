# chatbot_nlp.py

import nltk
import random
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK packages
nltk.download('punkt')     # Tokenizer
nltk.download('wordnet')   # Lemmatizer
nltk.download('omw-1.4')

# Sample corpus (You can expand this with more knowledge)
corpus = """
Hello! I'm your AI assistant. I can answer your questions.
What is your name?
My name is PyBot.
How can I help you?
I can help you with basic information.
Tell me about Python.
Python is a high-level, interpreted programming language.
Who developed Python?
Python was developed by Guido van Rossum.
What is machine learning?
Machine learning is a field of artificial intelligence that uses statistical techniques.
Bye
Goodbye! Have a nice day.
"""

# Text preprocessing
sent_tokens = nltk.sent_tokenize(corpus.lower())  # Sentence Tokenization
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greeting responses
GREETING_INPUTS = ["hi", "hello", "hey", "greetings"]
GREETING_RESPONSES = ["hi", "hello", "hey there", "hi, how can I help you?"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generate response using TF-IDF
def generate_response(user_input):
    user_input = user_input.lower()
    sent_tokens.append(user_input)

    vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = vectorizer.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    score = flat[-1]

    if score == 0:
        response = "I'm sorry, I didn't understand that."
    else:
        response = sent_tokens[idx]

    sent_tokens.pop()  # Remove last input
    return response

# Main Chat Loop
def chatbot():
    print("PyBot: Hello! I am PyBot. Ask me anything or type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("PyBot: Goodbye! Have a great day.")
            break
        elif greet(user_input) is not None:
            print("PyBot:", greet(user_input))
        else:
            print("PyBot:", generate_response(user_input))

# Run chatbot
if __name__ == "__main__":
    chatbot()