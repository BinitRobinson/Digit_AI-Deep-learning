import streamlit as st
import numpy as np
from PIL import Image
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

st.set_page_config(
    page_title="Digit Recognizer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

* {
    font-family: 'Space Grotesk', sans-serif !important;
}

.stApp {
    background: black;
    color: white;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.hero {
    text-align: center;
    padding-top: 20px;
    padding-bottom: 10px;
}

.hero h1 {
    font-size: 4rem;
    color: #00f5ff;
}

.hero p {
    color: #777;
    letter-spacing: 3px;
}

.result-box {
    background: #0a0a0a;
    border: 1px solid #00f5ff33;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
}

.digit {
    font-size: 120px;
    font-weight: bold;
    color: #00ff88;
}

.conf {
    font-size: 30px;
    color: #00f5ff;
}

.empty-box {
    height: 420px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px dashed #222;
    border-radius: 20px;
    color: #555;
    font-size: 20px;
}

.stButton > button {
    width: 100%;
    background: transparent !important;
    border: 1px solid #00f5ff !important;
    color: #00f5ff !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    import tensorflow as tf

    models = {}

    # ANN MODEL
    try:
        models["ANN"] = tf.keras.models.load_model(
            "ann_model.h5",
            compile=False
        )
        st.success("ANN model loaded")
    except Exception as e:
        st.error(f"ANN load failed: {e}")

    # CNN MODEL
    try:
        models["CNN"] = tf.keras.models.load_model(
            "cnn_model.keras",
            compile=False
        )
        st.success("CNN model loaded")
    except Exception as e:
        st.error(f"CNN load failed: {e}")

    return models

models = load_models()

if not models:
    st.error("No models loaded.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# PREDICTION FUNCTION
# ─────────────────────────────────────────────────────────────
def predict(model, arr):
    probs = model.predict(arr, verbose=0)[0]
    digit = int(np.argmax(probs))
    conf = float(probs[digit]) * 100
    return digit, conf

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Digit Recognizer AI</h1>
    <p>ANN · CNN · MNIST</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# MODEL SELECT
# ─────────────────────────────────────────────────────────────
model_choice = st.radio(
    "Select Model",
    list(models.keys()),
    horizontal=True
)

# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────────────────────
left, right = st.columns(2)

# ─────────────────────────────────────────────────────────────
# LEFT SIDE
# ─────────────────────────────────────────────────────────────
with left:

    try:
        from streamlit_drawable_canvas import st_canvas

        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=24,
            stroke_color="#FFFFFF",
            background_color="#000000",
            width=400,
            height=400,
            drawing_mode="freedraw",
            key="canvas",
        )

        predict_btn = st.button("PREDICT")

    except ImportError:
        st.error("Install streamlit-drawable-canvas")
        st.stop()

# ─────────────────────────────────────────────────────────────
# RIGHT SIDE
# ─────────────────────────────────────────────────────────────
with right:

    if predict_btn and canvas_result.image_data is not None:

        rgba = canvas_result.image_data.astype(np.uint8)

        rgb = rgba[:, :, :3].astype("float32")

        gray = (
            0.299 * rgb[:, :, 0]
            + 0.587 * rgb[:, :, 1]
            + 0.114 * rgb[:, :, 2]
        )

        mask = (gray > 20).astype("float32")

        if mask.sum() == 0:

            st.markdown("""
            <div class="empty-box">
                Draw a digit first
            </div>
            """, unsafe_allow_html=True)

        else:

            rows = np.any(mask > 0, axis=1)
            cols = np.any(mask > 0, axis=0)

            r0, r1 = np.where(rows)[0][[0, -1]]
            c0, c1 = np.where(cols)[0][[0, -1]]

            cropped = gray[r0:r1+1, c0:c1+1]

            h, w = cropped.shape

            diff = abs(h - w)

            if h > w:
                cropped = np.pad(
                    cropped,
                    ((0, 0), (diff//2, diff - diff//2)),
                    constant_values=0
                )
            elif w > h:
                cropped = np.pad(
                    cropped,
                    ((diff//2, diff - diff//2), (0, 0)),
                    constant_values=0
                )

            pad = int(cropped.shape[0] * 0.2)

            cropped = np.pad(
                cropped,
                pad,
                constant_values=0
            )

            img = Image.fromarray(cropped.astype("uint8"))

            img = img.resize((28, 28))

            arr = np.array(img).astype("float32") / 255.0

            if model_choice == "ANN":
                arr = arr.reshape(1, 28, 28)
            else:
                arr = arr.reshape(1, 28, 28, 1)

            digit, conf = predict(
                models[model_choice],
                arr
            )

            st.markdown(f"""
            <div class="result-box">
                <h3>Prediction</h3>
                <div class="digit">{digit}</div>
                <div class="conf">{conf:.2f}% Confidence</div>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="empty-box">
            Draw a digit and click Predict
        </div>
        """, unsafe_allow_html=True)