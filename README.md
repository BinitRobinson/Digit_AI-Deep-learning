# 🧠 Digit Recognizer AI

A deep learning web app that recognizes handwritten digits in real time — built with **Streamlit**, **TensorFlow**, and trained on the **MNIST** dataset.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-orange?style=flat-square&logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- ✏️ **Draw a digit** on an interactive canvas using your mouse or touch
- 🤖 **Switch between two models** — ANN and CNN — with a neon toggle bar
- 🎯 **Instant prediction** with digit display and confidence percentage
- 🌑 **Dark mode UI** — pure black background with neon cyan/green accents
- ⚡ **MNIST-faithful preprocessing** — tight crop, centering, and normalization

---

## 🖼️ Preview

```
┌─────────────────────────────────────────────────┐
│            🧠 Digit Recognizer                  │
│       DEEP LEARNING · ANN & CNN · MNIST         │
├──────────────────┬──────────────────────────────┤
│  [ ANN ]  [ CNN ]│                              │
│                  │         Predicted             │
│  ┌────────────┐  │              7               │
│  │            │  │                              │
│  │  canvas    │  │         Confidence           │
│  │            │  │          98.24%              │
│  └────────────┘  │       ████████████░          │
│  [ ⬡ PREDICT ]  │          ⬡ CNN               │
└──────────────────┴──────────────────────────────┘
```

---

## 🗂️ Project Structure

```
digit-recognizer/
│
├── app.py                  # Main Streamlit application
├── ann_model.h5            # Trained ANN model (~97% accuracy)
├── cnn_model.keras         # Trained CNN model (~99% accuracy)
├── digit_recognition.ipynb # Training notebook
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🧬 Models

| Model | Architecture | Parameters | Test Accuracy |
|-------|-------------|------------|---------------|
| **ANN** | Flatten → Dense(128) → Dense(64) → Dense(10) | ~109K | ~97% |
| **CNN** | Conv2D(32) → Pool → Conv2D(64) → Pool → Dense(128) → Dense(10) | ~203K | ~99% |

Both models trained on the MNIST dataset (60,000 training images, 10,000 test images).

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/your-username/digit-recognizer.git
cd digit-recognizer
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

Opens at `http://localhost:8501` 🎉

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub (make sure model files are included)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** ✅

> First deployment may take 3–5 minutes while TensorFlow installs.

---

## 📦 Requirements

```
streamlit==1.57.0
tensorflow==2.21.0
numpy==2.4.4
Pillow==12.1.1
plotly==6.7.0
streamlit-drawable-canvas==0.9.3
```

---

## 🔧 How the Preprocessing Works

Raw canvas drawings go through an MNIST-faithful pipeline before prediction:

```
RGBA canvas (400×400)
  │
  ├─ Extract RGB brightness (ignore alpha — always 255)
  ├─ Threshold > 30 to isolate stroke pixels
  ├─ Tight bounding box crop
  ├─ Pad to square
  ├─ Add 20% border padding (MNIST-style centering)
  ├─ Resize to 28×28 with LANCZOS
  └─ Normalize to [0, 1]
```

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ using Streamlit & TensorFlow
</div>
