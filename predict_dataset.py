import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
from utils import extract_features
from keras.models import load_model

model = load_model("emotion_model.h5")
emotion_labels = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']

dataset_path = "dataset"
correct = 0
total = 0

for file in os.listdir(dataset_path):
    if file.endswith(".wav"):
        filepath = os.path.join(dataset_path, file)
        parts = file.split('-')
        if len(parts) > 2:
            emotion_code = int(parts[2])
            true_emotion = emotion_labels[emotion_code - 1]

            features = extract_features(filepath).reshape(1, -1)
            prediction = model.predict(features)
            predicted_index = np.argmax(prediction)
            predicted_emotion = emotion_labels[predicted_index]

            print(f"{file} => Predicted: {predicted_emotion}, Actual: {true_emotion}")

            if predicted_emotion.lower() == true_emotion.lower():
                correct += 1
            total += 1

accuracy = (correct / total) * 100 if total > 0 else 0
print(f"\nAccuracy: {accuracy:.2f}%")
