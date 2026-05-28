import os
import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Digit Recognizer AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

* { font-family: 'Space Grotesk', sans-serif !important; }

.stApp { background: #000000 !important; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 3px; }

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 2.2rem 0 0.8rem;
    position: relative;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 500px; height: 160px;
    background: radial-gradient(ellipse, rgba(0,245,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #00f5ff, #00ff88, #00f5ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    margin: 0;
}
@keyframes shimmer { 0% { background-position: 0% } 100% { background-position: 200% } }
.hero-sub {
    color: #2d3748;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.hero-divider {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, #00f5ff, #00ff88);
    margin: 0.8rem auto 0;
    border-radius: 2px;
    box-shadow: 0 0 10px rgba(0,245,255,0.5);
}

/* ── Model toggle switch ── */
div[data-testid="column"]:has(.sw-active),
div[data-testid="column"]:has(.sw-inactive) {
    padding: 4px !important;
}

/* ACTIVE — solid filled, unmissable */
.sw-active .stButton > button {
    background: linear-gradient(135deg, rgba(0,245,255,0.22), rgba(0,255,136,0.12)) !important;
    border: 2px solid #00f5ff !important;
    color: #00f5ff !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    border-radius: 12px !important;
    box-shadow: 0 0 28px rgba(0,245,255,0.45), 0 0 8px rgba(0,245,255,0.2) inset !important;
    padding: 0.65rem 1rem !important;
    text-shadow: 0 0 12px rgba(0,245,255,0.8) !important;
}
.sw-active .stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,255,0.3), rgba(0,255,136,0.18)) !important;
    box-shadow: 0 0 40px rgba(0,245,255,0.6) !important;
}

/* INACTIVE — clearly dimmed */
.sw-inactive .stButton > button {
    background: #0a0a0a !important;
    border: 2px solid rgba(255,255,255,0.07) !important;
    color: #374151 !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    padding: 0.65rem 1rem !important;
}
.sw-inactive .stButton > button:hover {
    border-color: rgba(0,245,255,0.2) !important;
    color: #6b7280 !important;
}

/* ── Neon card ── */
.neon-card {
    background: #0a0a0a;
    border: 1px solid rgba(0,245,255,0.12);
    border-radius: 20px;
    padding: 1.6rem;
    position: relative;
    overflow: hidden;
}
.neon-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.5), transparent);
}

/* ── Section label ── */
.sec-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00f5ff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.sec-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(0,245,255,0.2), transparent);
}

/* ── Canvas hint ── */
.canvas-hint {
    color: #1e293b;
    font-size: 0.72rem;
    text-align: center;
    margin-top: 0.5rem;
    letter-spacing: 1px;
}

/* ── Predict button ── */
.stButton > button {
    background: transparent !important;
    border: 1.5px solid #00f5ff !important;
    color: #00f5ff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    margin-top: 0.8rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 10px rgba(0,245,255,0.15) !important;
}
.stButton > button:hover {
    background: rgba(0,245,255,0.07) !important;
    box-shadow: 0 0 28px rgba(0,245,255,0.4) !important;
    transform: translateY(-2px) !important;
}

/* ── Result card ── */
.result-card {
    background: #070707;
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 20px;
    padding: 2.5rem 1.5rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,136,0.5), transparent);
}
.result-pre {
    font-size: 0.6rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #2d3748;
    margin-bottom: 0.4rem;
}
.result-digit {
    font-size: 9rem;
    font-weight: 800;
    line-height: 1;
    color: #00ff88;
    text-shadow: 0 0 50px rgba(0,255,136,0.5), 0 0 100px rgba(0,255,136,0.15);
}
.result-conf-label {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2d3748;
    margin: 1rem 0 0.2rem;
}
.result-conf {
    font-size: 2.2rem;
    font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 20px rgba(0,245,255,0.5);
}
.cbar-wrap {
    width: 80%;
    background: #111;
    border-radius: 50px;
    height: 5px;
    margin: 0.8rem auto 0;
    overflow: hidden;
}
.cbar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #00ff88, #00f5ff);
    box-shadow: 0 0 8px rgba(0,245,255,0.6);
}
.mbadge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.8rem;
    border-radius: 50px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 1.2rem;
}
.mbadge-ann { color: #00f5ff; border: 1px solid rgba(0,245,255,0.3); background: rgba(0,245,255,0.05); }
.mbadge-cnn { color: #00ff88; border: 1px solid rgba(0,255,136,0.3); background: rgba(0,255,136,0.05); }

/* ── Empty state ── */
.empty-state {
    border: 1px dashed #111;
    border-radius: 20px;
    padding: 4rem 2rem;
    text-align: center;
    background: #050505;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 420px;
}
.empty-icon { font-size: 3.5rem; opacity: 0.15; }
.empty-text { color: #1a202c; font-size: 0.82rem; margin-top: 1rem; letter-spacing: 1px; line-height: 1.8; }

/* ── Alerts ── */
.stAlert { background: #0a0a0a !important; border-radius: 10px !important; border-left-color: #00f5ff !important; }
</style>
""", unsafe_allow_html=True)


# ─── ONNX model loading — works on any Python version ─────────────────────────
@st.cache_resource(show_spinner=False)
def load_models():
    import onnxruntime as ort
    models = {}
    for name, path in [("ANN", "ann_model.onnx"), ("CNN", "cnn_model.onnx")]:
        try:
            sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
            models[name] = sess
        except Exception as e:
            st.error(f"{name} load failed: {e}")
    return models

def predict(session, arr):
    input_name = session.get_inputs()[0].name
    probs = session.run(None, {input_name: arr})[0][0]
    digit = int(np.argmax(probs))
    conf  = float(probs[digit]) * 100
    return digit, conf, probs


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">Digit Recognizer</div>
    <div class="hero-sub">Deep Learning &nbsp;·&nbsp; ANN &amp; CNN &nbsp;·&nbsp; MNIST</div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─── Load models ──────────────────────────────────────────────────────────────
models = load_models()
if not models:
    st.error("No models found. Place ann_model.h5 and cnn_model.keras in the same folder.")
    st.stop()

# ─── Model toggle switch ──────────────────────────────────────────────────────
if "model_choice" not in st.session_state:
    st.session_state.model_choice = list(models.keys())[0]

# Render the switch bar with invisible Streamlit buttons overlaid via columns
_, sw_col, _ = st.columns([1, 1.4, 1])
with sw_col:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        ann_cls = "sw-active" if st.session_state.model_choice == "ANN" else "sw-inactive"
        st.markdown(f'<div class="{ann_cls}">', unsafe_allow_html=True)
        if st.button("ANN", key="sw_ann", use_container_width=True):
            st.session_state.model_choice = "ANN"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        cnn_cls = "sw-active" if st.session_state.model_choice == "CNN" else "sw-inactive"
        st.markdown(f'<div class="{cnn_cls}">', unsafe_allow_html=True)
        if st.button("CNN", key="sw_cnn", use_container_width=True):
            st.session_state.model_choice = "CNN"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

model_choice = st.session_state.model_choice

# ─── Main layout — 50 / 50 ────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ── LEFT: Canvas ──────────────────────────────────────────────────────────────
with col_left:
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">✦ Draw a Digit</div>', unsafe_allow_html=True)

    try:
        from streamlit_drawable_canvas import st_canvas
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=24,
            stroke_color="#FFFFFF",
            background_color="#000000",
            height=400,
            width=400,
            drawing_mode="freedraw",
            key="digit_canvas",
        )
        st.markdown('<div class="canvas-hint">— draw with mouse or touch —</div>', unsafe_allow_html=True)
        predict_btn = st.button("⬡  PREDICT", key="predict_draw")

    except ImportError:
        st.error("Run: pip install streamlit-drawable-canvas")
        canvas_result = None
        predict_btn   = False

    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Result ─────────────────────────────────────────────────────────────
with col_right:
    if predict_btn and canvas_result is not None:
        img_data = canvas_result.image_data
        if img_data is not None:
            rgba       = img_data.astype(np.uint8)
            brightness = rgba[:, :, :3].max()

            if brightness < 30:
                st.markdown("""
                <div class="empty-state">
                    <div class="empty-icon">✏️</div>
                    <div class="empty-text">Canvas is empty<br>draw a digit first</div>
                </div>""", unsafe_allow_html=True)
            else:
                # ── MNIST-faithful preprocessing ──────────────────────────────
                rgb  = rgba[:, :, :3].astype("float32")
                gray = 0.299*rgb[:,:,0] + 0.587*rgb[:,:,1] + 0.114*rgb[:,:,2]

                mask = (gray > 30).astype("float32")
                rows = np.any(mask > 0, axis=1)
                cols = np.any(mask > 0, axis=0)
                r0, r1 = np.where(rows)[0][[0, -1]]
                c0, c1 = np.where(cols)[0][[0, -1]]
                cropped = gray[r0:r1+1, c0:c1+1]

                h, w = cropped.shape
                diff = abs(h - w)
                if h > w:
                    cropped = np.pad(cropped, ((0,0),(diff//2, diff-diff//2)), constant_values=0)
                elif w > h:
                    cropped = np.pad(cropped, ((diff//2, diff-diff//2),(0,0)), constant_values=0)

                pad = int(cropped.shape[0] * 0.2)
                cropped = np.pad(cropped, pad, constant_values=0)

                pil_gray = Image.fromarray(cropped.astype("uint8"))
                pil_gray = pil_gray.resize((28, 28), Image.LANCZOS)

                arr       = np.array(pil_gray, dtype="float32") / 255.0
                arr_input = arr.reshape(1, 28, 28).astype("float32") if model_choice == "ANN" else arr.reshape(1, 28, 28, 1).astype("float32")

                digit, conf, probs = predict(models[model_choice], arr_input)

                badge_cls = "mbadge-ann" if model_choice == "ANN" else "mbadge-cnn"
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-pre">Predicted Digit</div>
                    <div class="result-digit">{digit}</div>
                    <div class="result-conf-label">Confidence</div>
                    <div class="result-conf">{conf:.2f}%</div>
                    <div class="cbar-wrap">
                        <div class="cbar-fill" style="width:{min(conf,100):.1f}%"></div>
                    </div>
                    <span class="mbadge {badge_cls}">⬡ {model_choice}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🎯</div>
                <div class="empty-text">Draw something and hit Predict</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🧠</div>
            <div class="empty-text">Draw a digit on the left<br>then press PREDICT</div>
        </div>
        """, unsafe_allow_html=True)
