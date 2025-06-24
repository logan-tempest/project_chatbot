 # train.py

import os
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from dotenv import load_dotenv

load_dotenv()
CSV_FILE = os.getenv("CSV_PATH", "ilr_conversational_500.csv")

df = pd.read_csv(CSV_FILE)
questions = df['Question'].astype(str).tolist()
tags = df['Tag'].astype(str).tolist()
answers = df['Answer'].astype(str).tolist()
qa_pairs = list(zip(questions, tags, answers))

# Encode tags
lbl_encoder = LabelEncoder()
encoded_tags = lbl_encoder.fit_transform(tags)
num_classes = len(lbl_encoder.classes_)

# Tokenize
vocab_size = 3000
max_len = 40
tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(questions)
sequences = tokenizer.texts_to_sequences(questions)
padded = pad_sequences(sequences, padding='post', maxlen=max_len)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 64, input_length=max_len),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.fit(
    padded,
    np.array(encoded_tags),
    epochs=300,
    batch_size=8,
    validation_split=0.15,
    verbose=1
)

# Save to backend/models/
os.makedirs("backend/models", exist_ok=True)
model.save("backend/models/legal_rights_chat_model.h5")
pickle.dump(tokenizer, open("backend/models/legal_tokenizer.pkl", "wb"))
pickle.dump(lbl_encoder, open("backend/models/legal_encoder.pkl", "wb"))

print("✅ Training complete. Model and tools saved.")
#         return answer
#     else: