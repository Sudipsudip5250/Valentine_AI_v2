from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import numpy as np
import pickle
import json
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('punkt')  # Add this to force download the missing tokenizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load necessary files
lemmatizer = WordNetLemmatizer()
model = load_model("chatbot_model.h5")
intents = json.loads(open("AI_brain2.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.10
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints):
    if not ints:
        return "I'm sorry, I don't understand."

    tag = ints[0]['intent']
    for i in intents['intents']:
        if i['tag'] == tag:
            return np.random.choice(i['responses'])
    return "I'm sorry, I don't have a response for that."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    intents = predict_class(user_input)
    response = getResponse(intents)
    return jsonify({"response": response})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from Render, default 5000
    app.run(host="0.0.0.0", port=port, debug=True)

