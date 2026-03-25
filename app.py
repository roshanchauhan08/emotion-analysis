import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, jsonify
import numpy as np
import librosa
import tempfile
import base64
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Lazy-load model
model = None
emotion_labels = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']
emotion_emojis = {
    'neutral': '😐', 'calm': '😌', 'happy': '😄', 'sad': '😢',
    'angry': '😠', 'fearful': '😨', 'disgust': '🤢', 'surprised': '😲'
}
emotion_colors = {
    'neutral': '#94a3b8', 'calm': '#60a5fa', 'happy': '#fbbf24', 'sad': '#818cf8',
    'angry': '#f87171', 'fearful': '#a78bfa', 'disgust': '#34d399', 'surprised': '#fb923c'
}

def get_model():
    global model
    if model is None:
        try:
            from tensorflow.keras.models import load_model
            model = load_model("emotion_model.h5")
        except Exception as e:
            print(f"Model load error: {e}")
            return None
    return model

def extract_features(file_path):
    audio, sample_rate = librosa.load(file_path, duration=3, offset=0.5)
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        # Save to temp file
        suffix = '.wav'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        # Extract features
        features = extract_features(tmp_path).reshape(1, -1)
        os.unlink(tmp_path)

        m = get_model()
        if m is None:
            # Demo mode: random prediction for UI testing
            import random
            idx = random.randint(0, 7)
            confidence_scores = [round(random.uniform(0.01, 0.15), 3) for _ in range(8)]
            confidence_scores[idx] = round(random.uniform(0.55, 0.90), 3)
            total = sum(confidence_scores)
            confidence_scores = [round(s/total, 3) for s in confidence_scores]
        else:
            prediction = m.predict(features)
            confidence_scores = prediction[0].tolist()
            idx = int(np.argmax(confidence_scores))

        emotion = emotion_labels[idx]
        confidence = round(float(confidence_scores[idx]) * 100, 1)

        scores_dict = {
            emotion_labels[i]: round(float(confidence_scores[i]) * 100, 1)
            for i in range(len(emotion_labels))
        }

        return jsonify({
            'emotion': emotion,
            'emoji': emotion_emojis[emotion],
            'color': emotion_colors[emotion],
            'confidence': confidence,
            'scores': scores_dict
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
