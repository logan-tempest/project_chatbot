# chat.py

import os
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

from tensorflow.keras.preprocessing.sequence import pad_sequences
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv()

# Paths from .env
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "legal_rights_chat_model.h5"))
TOKENIZER_PATH = str(BASE_DIR / "models" / "legal_tokenizer.pkl")
ENCODER_PATH = str(BASE_DIR / "models" / "legal_encoder.pkl")
CSV_FILE = os.getenv("CSV_PATH", "ilr_conversational_500.csv")
 

# Load data and tools
df = pd.read_csv(CSV_FILE)
questions = df['Question'].astype(str).tolist()
answers = df['Answer'].astype(str).tolist()
tags = df['Tag'].astype(str).tolist()
qa_pairs = list(zip(questions, tags, answers))

model = tf.keras.models.load_model(MODEL_PATH)
tokenizer = pickle.load(open(TOKENIZER_PATH, "rb"))
lbl_encoder = pickle.load(open(ENCODER_PATH, "rb"))
semantic_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
question_embeddings = semantic_model.encode(questions, convert_to_tensor=True)

vocab_size = 3000
max_len = 40

def get_response(user_input):
    seq = tokenizer.texts_to_sequences([user_input])
    padded = pad_sequences(seq, maxlen=max_len, padding='post')
    prediction = model.predict(padded, verbose=0)
    prob = np.max(prediction)
    tag = lbl_encoder.inverse_transform([np.argmax(prediction)])[0]

    if prob > 0.6:
        filtered = [(q, a) for (q, t, a) in qa_pairs if t == tag]
        if filtered:
            f_qs = [q for (q, _) in filtered]
            f_as = [a for (_, a) in filtered]
            f_embeds = semantic_model.encode(f_qs, convert_to_tensor=True)
            user_embed = semantic_model.encode(user_input, convert_to_tensor=True)
            sims = util.pytorch_cos_sim(user_embed, f_embeds)[0]
            best = int(sims.argmax())
            return f_as[best], prob

    return "I'm not confident about that. Try rephrasing.", prob
