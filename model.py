import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from utils import extract_features

DATASET_PATH = "dataset"
features, labels = [], []

for file in os.listdir(DATASET_PATH):
    if file.endswith(".wav"):
        emotion = file.split("-")[2]
        path = os.path.join(DATASET_PATH, file)
        features.append(extract_features(path))
        labels.append(emotion)

df = pd.DataFrame(features)
df['label'] = labels
df.to_csv("emotion_dataset.csv", index=False)

X = df.iloc[:, :-1].values
y = LabelEncoder().fit_transform(df['label'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    Dense(256, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(len(set(y)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))
model.save("emotion_model.h5")
print("Model saved as emotion_model.h5")
