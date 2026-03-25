# 🎙️ VoiceMood — Speech Emotion Recognition System

> A real-time speech emotion recognition web app built with Python, TensorFlow, Flask, and librosa. Achieves **82.3% accuracy** detecting 8 human emotions from voice audio.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.x-green?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-82.3%25-brightgreen?style=flat-square)

---

## ✨ Features

- 🌐 **Web Interface** — Upload audio files or record directly from your browser
- 🎯 **8 Emotion Classes** — neutral, calm, happy, sad, angry, fearful, disgust, surprised
- 📊 **Confidence Scores** — Visual breakdown of all emotion probabilities
- 🎙️ **CLI Mode** — Run `main.py` for desktop voice recording + TTS feedback
- 🔁 **Batch Evaluation** — `predict_dataset.py` to score your entire dataset

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/Speech-Emotion-Recognition-System.git
cd Speech-Emotion-Recognition-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your trained model

Place `emotion_model.h5` in the root directory.  
(Or train a new one — see [Training](#training) below)

### 4. Run the web app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## 🏗️ Project Structure

```
Speech-Emotion-Recognition-System/
│
├── app.py                  ← Flask web server (main entry point)
├── main.py                 ← CLI mode with TTS feedback
├── model.py                ← Model training script
├── predict_dataset.py      ← Batch accuracy evaluation
├── utils.py                ← MFCC feature extraction
├── record.py               ← Microphone recording utility
│
├── templates/
│   └── index.html          ← Web frontend
├── static/
│   ├── css/style.css
│   └── js/main.js
│
├── emotion_model.h5        ← Trained Keras model
├── emotion_dataset.csv     ← Extracted features dataset
└── requirements.txt
```

---

## 🧠 How It Works

```
Audio Input  →  MFCC Extraction (40 features)  →  Dense Neural Network  →  Emotion Label
```

1. **Audio** — WAV/MP3/OGG, 3 seconds used (with 0.5s offset)
2. **Features** — 40 MFCC coefficients extracted via `librosa`
3. **Model** — 3-layer Dense network: `256 → 128 → 8 (softmax)`
4. **Output** — Emotion class + confidence scores for all 8 classes

---

## 🏋️ Training

To train your own model, download the [RAVDESS dataset](https://zenodo.org/record/1188976) and place WAV files in a `dataset/` folder:

```bash
python model.py
```

This will generate `emotion_dataset.csv` and `emotion_model.h5`.

---

## 📊 Evaluate on Dataset

```bash
python predict_dataset.py
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web server |
| `tensorflow` | Neural network model |
| `librosa` | Audio feature extraction |
| `numpy` | Numerical processing |
| `scikit-learn` | Label encoding, train/test split |
| `sounddevice` | Microphone recording |
| `wavio` | WAV file writing |
| `pyttsx3` | Text-to-speech (CLI mode) |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT License © 2024 rajritu77821
