import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pyttsx3
import time
from tensorflow.keras.models import load_model
import numpy as np
from utils import extract_features
from record import record_audio

engine = pyttsx3.init()
engine.setProperty('rate', 140)

engine.say("Recording will start in a few seconds")
engine.runAndWait()
time.sleep(1)

record_audio("test.wav")

model = load_model("emotion_model.h5")
features = extract_features("test.wav").reshape(1, -1)
prediction = model.predict(features)
predicted_label = np.argmax(prediction)

emotion_map = {
    1: "neutral", 2: "calm", 3: "happy", 4: "sad",
    5: "angry", 6: "fearful", 7: "disgust", 8: "surprised"
}

emotion = emotion_map.get(predicted_label + 1, 'Unknown')
print(f"Predicted Emotion: {emotion}")

engine.say(f"You sound {emotion}")
engine.runAndWait()
