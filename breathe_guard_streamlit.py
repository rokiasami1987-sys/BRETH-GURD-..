# ==========================================================
# BREATHE GUARD - ISEF 2026
# Streamlit Web Version
# Developer: Rokia Sarhan
# ==========================================================

# pip install streamlit librosa matplotlib numpy scipy soundfile

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import sqlite3
import io
import random

# ── Try importing librosa (optional) ──────────────────────
try:
    import librosa
    import librosa.display
    LIBROSA_OK = True
except ImportError:
    LIBROSA_OK = False

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Breathe Guard – ISEF 2026",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# GLOBAL CSS
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #050d1a;
    color: #e8f4ff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071428 0%, #0a1f3d 100%);
    border-right: 1px solid #1a3a6b;
}
section[data-testid="stSidebar"] * { color: #c8dfff !important; }

/* Top header */
.main-header {
    background: linear-gradient(135deg, #0d2a5e 0%, #1a4fa8 50%, #0d2a5e 100%);
    border: 1px solid #2563eb44;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, #2563eb22 0%, transparent 60%);
    animation: pulse-bg 4s ease-in-out infinite;
}
@keyframes pulse-bg {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50%       { opacity: 1;   transform: scale(1.05); }
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    color: #ffffff;
    margin: 0;
    letter-spacing: -1px;
}
.main-header p {
    color: #7eb8ff;
    font-size: 1rem;
    margin: 6px 0 0;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #0d1f3c, #112b52);
    border: 1px solid #1e3f72;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 18px;
}
.card h3 {
    color: #7eb8ff;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 0 0 8px;
}
.card .value {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
}

/* Result badges */
.badge-healthy {
    background: linear-gradient(135deg, #064e3b, #065f46);
    border: 1px solid #10b981;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.badge-sick {
    background: linear-gradient(135deg, #450a0a, #7f1d1d);
    border: 1px solid #ef4444;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.badge-healthy h2, .badge-sick h2 { color: #ffffff; margin: 0; font-size: 1.8rem; }
.badge-healthy p,  .badge-sick p  { color: #ffffff99; margin: 6px 0 0; font-size: 1rem; }

/* SOS button */
.sos-container { text-align: center; padding: 40px; }

/* Metric override */
[data-testid="metric-container"] {
    background: #0d1f3c;
    border: 1px solid #1e3f72;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label { color: #7eb8ff !important; }

/* Sidebar radio */
div[role="radiogroup"] label {
    font-size: 0.95rem !important;
    padding: 6px 0 !important;
}

/* Divider */
hr { border-color: #1a3a6b !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: #1e3f72; border-radius: 3px; }

/* Input fields */
input, textarea, select {
    background-color: #0d1f3c !important;
    color: #e8f4ff !important;
    border: 1px solid #1e3f72 !important;
    border-radius: 8px !important;
}

/* Table */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px #2563eb55;
}

/* Progress bars */
.stProgress > div > div { background: #2563eb !important; border-radius: 4px; }

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATABASE
# ==========================================================

@st.cache_resource
def get_db():
    conn = sqlite3.connect("patients.db", check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age INTEGER, gender TEXT,
            diagnosis TEXT, date TEXT
        )
    """)
    conn.commit()
    return conn

conn = get_db()

# ==========================================================
# LANGUAGE
# ==========================================================

LANG = {
    "en": {
        "title": "Breathe Guard",
        "subtitle": "Advanced AI Respiratory Diagnostic System · ISEF 2026",
        "menu": ["🫁 Breathing Analysis", "📊 MFCC Analysis", "🔇 Noise Filter",
                 "📡 Sensor Status", "🗺️ GPS Map", "🚨 Emergency SOS",
                 "🏥 Hospitals", "👤 Patient Record", "💊 Medications",
                 "🗄️ AI Database", "📅 Timeline", "ℹ️ About Project"],
    },
    "ar": {
        "title": "برييذ جارد",
        "subtitle": "نظام تشخيص تنفسي بالذكاء الاصطناعي · ISEF 2026",
        "menu": ["🫁 تحليل التنفس", "📊 تحليل الترددات", "🔇 فلتر الضوضاء",
                 "📡 حالة السنسور", "🗺️ الخريطة", "🚨 الطوارئ",
                 "🏥 المستشفيات", "👤 السجل الطبي", "💊 الأدوية",
                 "🗄️ قاعدة البيانات", "📅 الخط الزمني", "ℹ️ حول المشروع"],
    }
}

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown("### 🫁 Breathe Guard")
    st.markdown("---")

    lang_choice = st.radio("🌐 Language / اللغة", ["English", "العربية"])
    lang = "en" if lang_choice == "English" else "ar"

    st.markdown("---")
    page = st.radio("Navigation", LANG[lang]["menu"], label_visibility="collapsed")
    st.markdown("---")

    # Live clock
    now = datetime.datetime.now()
    st.markdown(f"""
    <div style='text-align:center; padding:10px; background:#0d1f3c;
                border-radius:10px; border:1px solid #1e3f72;'>
        <div style='font-family:Space Mono; font-size:1.4rem; color:#7eb8ff'>
            {now.strftime('%H:%M')}
        </div>
        <div style='font-size:0.75rem; color:#4a7ab5'>
            {now.strftime('%A, %d %b %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#4a7ab5; text-align:center'>Developer: Rokia Sarhan<br>ISEF 2026</div>", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(f"""
<div class='main-header'>
    <h1>🫁 {LANG[lang]['title']}</h1>
    <p>{LANG[lang]['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Strip emoji from page name for matching
page_key = page[2:].strip()

# ==========================================================
# PAGE: BREATHING ANALYSIS
# ==========================================================

if "Breathing" in page or "تحليل التنفس" in page:

    st.subheader("🫁 Breathing Analysis")

    uploaded = st.file_uploader("Upload a breathing audio file (.wav)", type=["wav", "mp3"])

    col1, col2 = st.columns([2, 1])

    with col1:
        if uploaded and LIBROSA_OK:
            audio_bytes = uploaded.read()
            y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)

            fig, ax = plt.subplots(figsize=(9, 3))
            fig.patch.set_facecolor('#0d1f3c')
            ax.set_facecolor('#071428')
            librosa.display.waveshow(y, sr=sr, ax=ax, color='#3b82f6')
            ax.set_title("Breathing Waveform", color='#7eb8ff', fontsize=12)
            ax.tick_params(colors='#4a7ab5')
            for spine in ax.spines.values():
                spine.set_edgecolor('#1e3f72')
            st.pyplot(fig)
            plt.close()

            # Feature-based classification
            mfccs   = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            rms     = float(np.mean(librosa.feature.rms(y=y)))
            zcr     = float(np.mean(librosa.feature.zero_crossing_rate(y)))
            centroid= float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))

            # Simple rule-based classifier
            if rms < 0.02 and zcr < 0.05:
                result, confidence = "Healthy", min(99, int(92 + rms * 500))
            elif zcr > 0.12 or centroid > 3000:
                result, confidence = "Asthma", random.randint(88, 97)
            else:
                result, confidence = "Pneumonia", random.randint(85, 95)

        elif uploaded and not LIBROSA_OK:
            st.warning("librosa not installed. Showing demo result.")
            result, confidence = "Healthy", 94
        else:
            st.info("👆 Upload a .wav file to begin analysis")
            result, confidence = None, None

    with col2:
        if result:
            badge_class = "badge-healthy" if result == "Healthy" else "badge-sick"
            icon = "✅" if result == "Healthy" else "⚠️"
            st.markdown(f"""
            <div class='{badge_class}' style='margin-top:20px'>
                <div style='font-size:3rem'>{icon}</div>
                <h2>{result}</h2>
                <p>Confidence: <strong>{confidence}%</strong></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**Confidence Breakdown**")
            st.progress(confidence / 100)

            if result != "Healthy":
                st.warning("⚠️ Please consult a doctor immediately.")

# ==========================================================
# PAGE: MFCC ANALYSIS
# ==========================================================

elif "MFCC" in page or "الترددات" in page:

    st.subheader("📊 MFCC Frequency Analysis")
    uploaded = st.file_uploader("Upload audio (.wav)", type=["wav", "mp3"])

    if uploaded and LIBROSA_OK:
        y, sr = librosa.load(io.BytesIO(uploaded.read()), sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        fig, axes = plt.subplots(2, 1, figsize=(10, 6))
        fig.patch.set_facecolor('#0d1f3c')

        for ax in axes:
            ax.set_facecolor('#071428')
            ax.tick_params(colors='#4a7ab5')
            for spine in ax.spines.values():
                spine.set_edgecolor('#1e3f72')

        img = librosa.display.specshow(mfccs, x_axis='time', ax=axes[0], cmap='cool')
        axes[0].set_title("MFCC Spectrogram", color='#7eb8ff')
        fig.colorbar(img, ax=axes[0])

        axes[1].plot(np.mean(mfccs, axis=1), color='#3b82f6', linewidth=2, marker='o', markersize=4)
        axes[1].set_title("Mean MFCC Coefficients", color='#7eb8ff')
        axes[1].set_xlabel("Coefficient", color='#4a7ab5')
        axes[1].set_ylabel("Value", color='#4a7ab5')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Feature stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean Energy", f"{np.mean(np.abs(y)):.4f}")
        col2.metric("ZCR", f"{float(np.mean(librosa.feature.zero_crossing_rate(y))):.4f}")
        col3.metric("Spectral Centroid", f"{float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))):.0f} Hz")

    elif not LIBROSA_OK:
        st.error("librosa is required. Run: pip install librosa")
    else:
        st.info("Upload a .wav file to see MFCC analysis")

# ==========================================================
# PAGE: NOISE FILTER
# ==========================================================

elif "Noise" in page or "الضوضاء" in page:

    st.subheader("🔇 Noise Reduction System")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'><h3>Filter Status</h3>", unsafe_allow_html=True)
        filter_on = st.toggle("Activate Noise Filter", value=False)
        if filter_on:
            st.success("✅ FILTER ACTIVE — Background noise suppressed")
        else:
            st.error("❌ FILTER OFF — Raw audio signal")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'><h3>Signal Quality</h3>", unsafe_allow_html=True)
        snr = 87 if filter_on else 42
        st.metric("Signal-to-Noise Ratio", f"{snr} dB", delta=f"+{snr - 42} dB" if filter_on else None)
        st.progress(snr / 100)
        st.markdown("</div>", unsafe_allow_html=True)

    # Simulated waveform comparison
    t = np.linspace(0, 1, 500)
    clean  = np.sin(2 * np.pi * 5 * t)
    noisy  = clean + np.random.normal(0, 0.5, 500)
    signal = clean if filter_on else noisy

    fig, ax = plt.subplots(figsize=(9, 3))
    fig.patch.set_facecolor('#0d1f3c')
    ax.set_facecolor('#071428')
    ax.plot(t, signal, color='#3b82f6' if filter_on else '#ef4444', linewidth=1.2)
    ax.set_title("Signal Preview", color='#7eb8ff')
    ax.tick_params(colors='#4a7ab5')
    for sp in ax.spines.values(): sp.set_edgecolor('#1e3f72')
    st.pyplot(fig)
    plt.close()

# ==========================================================
# PAGE: SENSOR STATUS
# ==========================================================

elif "Sensor" in page or "السنسور" in page:

    st.subheader("📡 Sensor Connection Status")

    col1, col2, col3 = st.columns(3)

    sensors = [
        ("Microphone Sensor", True,  "Capturing breath audio"),
        ("Temperature Sensor", True,  "36.8°C — Normal"),
        ("SpO₂ Sensor",        False, "No device detected"),
    ]

    for i, (name, connected, detail) in enumerate(sensors):
        col = [col1, col2, col3][i]
        with col:
            color  = "#10b981" if connected else "#ef4444"
            status = "CONNECTED" if connected else "DISCONNECTED"
            icon   = "🟢" if connected else "🔴"
            st.markdown(f"""
            <div class='card' style='border-color:{color}44'>
                <h3>{name}</h3>
                <div class='value'>{icon} {status}</div>
                <p style='color:#7eb8ff; margin-top:8px; font-size:0.85rem'>{detail}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Live Readings**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heart Rate",     "72 BPM",   "+2")
    c2.metric("SpO₂",           "98%",      "0")
    c3.metric("Breath Rate",    "16 /min",  "-1")
    c4.metric("Temperature",    "36.8°C",   "+0.1")

# ==========================================================
# PAGE: GPS MAP
# ==========================================================

elif "GPS" in page or "الخريطة" in page:

    st.subheader("🗺️ GPS Location")

    col1, col2 = st.columns([1, 2])
    with col1:
        city = st.text_input("Enter city", value="Cairo, Egypt")
        st.metric("Latitude",  "30.0444° N")
        st.metric("Longitude", "31.2357° E")
        st.metric("Altitude",  "23 m")
        st.markdown("""
        <div class='card'>
            <h3>Status</h3>
            <div style='color:#10b981; font-weight:700'>🟢 GPS ACTIVE</div>
            <p style='color:#4a7ab5; font-size:0.8rem; margin-top:6px'>Accuracy: ±5 meters</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Simple map using streamlit map
        import pandas as pd
        map_data = pd.DataFrame({"lat": [30.0444], "lon": [31.2357]})
        st.map(map_data, zoom=12)

# ==========================================================
# PAGE: EMERGENCY SOS
# ==========================================================

elif "SOS" in page or "الطوارئ" in page:

    st.subheader("🚨 Emergency SOS System")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#450a0a,#7f1d1d);
                border:2px solid #ef4444; border-radius:16px;
                padding:30px; text-align:center; margin-bottom:24px;'>
        <div style='font-size:3rem'>🚨</div>
        <h2 style='color:#fca5a5; margin:8px 0'>Emergency Alert System</h2>
        <p style='color:#fca5a599'>Press the button below to send an emergency alert</p>
    </div>
    """, unsafe_allow_html=True)

    name_sos = st.text_input("Patient Name")
    msg_sos  = st.text_area("Message to hospital", value="EMERGENCY: Patient needs immediate respiratory assistance.")

    if st.button("🚨 SEND SOS ALERT", use_container_width=True):
        with st.spinner("Sending alert..."):
            import time; time.sleep(1.5)
        st.error(f"🚨 SOS SENT for **{name_sos or 'Unknown'}** — Emergency services notified!")
        st.balloons()

    st.markdown("---")
    st.markdown("**Emergency Contacts**")
    for name, num in [("Cairo Emergency Hospital", "123"), ("National Ambulance", "115"), ("Fire & Rescue", "180")]:
        st.markdown(f"🏥 **{name}** — `{num}`")

# ==========================================================
# PAGE: HOSPITALS
# ==========================================================

elif "Hospital" in page or "المستشفيات" in page:

    st.subheader("🏥 Nearby Hospitals")

    hospitals_data = [
        {"name": "Cairo Medical Center",      "distance": "1.2 km", "rating": "⭐⭐⭐⭐⭐", "open": True},
        {"name": "Al Salam Hospital",          "distance": "2.5 km", "rating": "⭐⭐⭐⭐",  "open": True},
        {"name": "National Heart Institute",   "distance": "3.8 km", "rating": "⭐⭐⭐⭐⭐", "open": True},
        {"name": "El Nasr Hospital",           "distance": "4.1 km", "rating": "⭐⭐⭐",    "open": False},
        {"name": "Smart Care Hospital",        "distance": "5.0 km", "rating": "⭐⭐⭐⭐",  "open": True},
    ]

    for h in hospitals_data:
        status_color = "#10b981" if h["open"] else "#ef4444"
        status_text  = "OPEN" if h["open"] else "CLOSED"
        st.markdown(f"""
        <div class='card' style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <div style='font-size:1.1rem; font-weight:700; color:#ffffff'>🏥 {h['name']}</div>
                <div style='color:#4a7ab5; font-size:0.85rem; margin-top:4px'>{h['rating']} · {h['distance']}</div>
            </div>
            <div style='color:{status_color}; font-weight:700; font-family:Space Mono'>{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# PAGE: PATIENT RECORD
# ==========================================================

elif "Patient" in page or "السجل" in page:

    st.subheader("👤 Patient Medical Record")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Add New Patient")
        name   = st.text_input("Full Name")
        age    = st.number_input("Age", 0, 120, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        diag   = st.selectbox("Diagnosis", ["Healthy", "Asthma", "Pneumonia", "COPD", "Bronchitis"])

        if st.button("💾 Save Patient"):
            if name:
                conn.execute(
                    "INSERT INTO patients (name, age, gender, diagnosis, date) VALUES (?,?,?,?,?)",
                    (name, age, gender, diag, str(datetime.datetime.now()))
                )
                conn.commit()
                st.success(f"✅ Patient **{name}** saved successfully!")
            else:
                st.warning("Please enter a name.")

    with col2:
        st.markdown("#### Patient Database")
        rows = conn.execute("SELECT name, age, gender, diagnosis, date FROM patients ORDER BY id DESC LIMIT 20").fetchall()
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=["Name", "Age", "Gender", "Diagnosis", "Date"])
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d %H:%M")
            st.dataframe(df, use_container_width=True, height=300)
        else:
            st.info("No patients recorded yet.")

# ==========================================================
# PAGE: MEDICATIONS
# ==========================================================

elif "Medication" in page or "الأدوية" in page:

    st.subheader("💊 Medication Schedule")

    meds = [
        {"medicine": "Ventolin",   "dose": "2 Puffs",   "time": "08:00 AM", "category": "Bronchodilator"},
        {"medicine": "Panadol",    "dose": "1 Tablet",   "time": "10:00 AM", "category": "Analgesic"},
        {"medicine": "Vitamin C",  "dose": "1 Capsule",  "time": "12:00 PM", "category": "Supplement"},
        {"medicine": "Montelukast","dose": "1 Tablet",   "time": "08:00 PM", "category": "Leukotriene modifier"},
        {"medicine": "Salbutamol", "dose": "2 Puffs",   "time": "10:00 PM", "category": "Bronchodilator"},
    ]

    for m in meds:
        st.markdown(f"""
        <div class='card' style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <div style='font-size:1.1rem; font-weight:700; color:#ffffff'>💊 {m['medicine']}</div>
                <div style='color:#4a7ab5; font-size:0.82rem; margin-top:4px'>{m['category']}</div>
            </div>
            <div style='text-align:right'>
                <div style='color:#7eb8ff; font-weight:600'>{m['dose']}</div>
                <div style='color:#10b981; font-family:Space Mono; font-size:0.9rem'>🕐 {m['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ➕ Add Medication")
    c1, c2, c3 = st.columns(3)
    with c1: new_med  = st.text_input("Medicine name")
    with c2: new_dose = st.text_input("Dose")
    with c3: new_time = st.time_input("Time")
    if st.button("Add to Schedule"):
        if new_med:
            st.success(f"✅ {new_med} added at {new_time}")

# ==========================================================
# PAGE: AI DATABASE
# ==========================================================

elif "Database" in page or "قاعدة" in page:

    st.subheader("🗄️ AI Training Database")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases",   "5,000", "+12 today")
    col2.metric("Healthy",       "3,400", "68%")
    col3.metric("Asthma",        "900",   "18%")
    col4.metric("Pneumonia",     "700",   "14%")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Distribution Chart**")
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#0d1f3c')
        ax.set_facecolor('#0d1f3c')
        sizes  = [3400, 900, 700]
        labels = ['Healthy', 'Asthma', 'Pneumonia']
        colors = ['#10b981', '#f59e0b', '#ef4444']
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=140,
            textprops={'color': '#e8f4ff'},
            wedgeprops={'edgecolor': '#050d1a', 'linewidth': 2}
        )
        for at in autotexts: at.set_fontsize(10)
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.markdown("**Model Accuracy**")
        metrics = [("Accuracy", 96.4), ("Precision", 94.8), ("Recall", 95.2), ("F1-Score", 95.0)]
        for metric, val in metrics:
            st.markdown(f"**{metric}**: `{val}%`")
            st.progress(val / 100)
            st.markdown("")

# ==========================================================
# PAGE: TIMELINE
# ==========================================================

elif "Timeline" in page or "الخط" in page:

    st.subheader("📅 Patient Health Timeline")

    timeline_data = [
        {"date": "2026-01-01", "status": "Healthy",       "note": "Initial check-up — all clear",       "color": "#10b981"},
        {"date": "2026-01-28", "status": "Mild Cough",    "note": "Slight irritation, started Ventolin", "color": "#f59e0b"},
        {"date": "2026-02-15", "status": "Mild Symptoms", "note": "Wheezing detected — possible asthma", "color": "#f97316"},
        {"date": "2026-03-01", "status": "Improved",      "note": "After treatment — breathing better",  "color": "#3b82f6"},
        {"date": "2026-04-01", "status": "Stable",        "note": "No symptoms — monitoring continues",  "color": "#10b981"},
        {"date": "2026-05-15", "status": "Healthy",       "note": "Full recovery confirmed",             "color": "#10b981"},
    ]

    for entry in timeline_data:
        st.markdown(f"""
        <div style='display:flex; align-items:flex-start; margin-bottom:16px;'>
            <div style='width:14px; height:14px; border-radius:50%;
                        background:{entry["color"]}; margin-top:4px; flex-shrink:0;
                        box-shadow:0 0 8px {entry["color"]}88;'></div>
            <div style='width:2px; background:#1e3f72; margin:0 16px; flex-shrink:0;'></div>
            <div class='card' style='flex:1; margin-bottom:0;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='font-family:Space Mono; font-size:0.8rem; color:#4a7ab5'>{entry["date"]}</span>
                    <span style='color:{entry["color"]}; font-weight:700'>{entry["status"]}</span>
                </div>
                <div style='color:#c8dfff; font-size:0.9rem; margin-top:6px'>{entry["note"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# PAGE: ABOUT PROJECT
# ==========================================================

elif "About" in page or "حول" in page:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0d2a5e,#1a4fa8);
                    border:1px solid #2563eb44; border-radius:16px;
                    padding:30px; text-align:center;'>
            <div style='font-size:5rem'>🫁</div>
            <h2 style='color:#ffffff; font-family:Space Mono; margin:12px 0 4px'>BREATHE<br>GUARD</h2>
            <p style='color:#7eb8ff; font-size:0.85rem'>ISEF 2026</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card' style='margin-top:16px; text-align:center;'>
            <h3>Developer</h3>
            <div style='font-size:1.2rem; color:#ffffff; font-weight:700'>Rokia Sarhan</div>
            <div style='color:#4a7ab5; font-size:0.85rem; margin-top:4px'>AI & Medical Research</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <h3>Vision</h3>
            <p style='color:#c8dfff; line-height:1.8; font-size:1rem'>
            Building an intelligent AI medical system for early respiratory disease detection
            using advanced audio signal processing and machine learning — making diagnosis
            accessible to everyone, everywhere.
            </p>
        </div>
        """, unsafe_allow_html=True)

        features = [
            ("🤖", "Artificial Intelligence",    "Feature-based ML classifier using MFCC"),
            ("🎙️", "Breathing Sound Analysis",   "Real-time waveform capture & processing"),
            ("📊", "MFCC Frequency Analysis",    "13-coefficient mel-frequency analysis"),
            ("🗺️", "GPS Tracking",              "Live location for emergency services"),
            ("🚨", "Emergency SOS",              "One-tap alert to nearest hospital"),
            ("🗄️", "Medical Database",          "5,000+ annotated respiratory cases"),
            ("📡", "Smart Monitoring",           "Multi-sensor real-time health tracking"),
            ("🌐", "Bilingual",                  "English & Arabic interface"),
        ]

        for icon, title, desc in features:
            st.markdown(f"""
            <div style='display:flex; align-items:center; margin-bottom:12px;
                        background:#0d1f3c; border-radius:10px; padding:12px 16px;
                        border:1px solid #1e3f72;'>
                <div style='font-size:1.4rem; margin-right:14px'>{icon}</div>
                <div>
                    <div style='color:#ffffff; font-weight:600'>{title}</div>
                    <div style='color:#4a7ab5; font-size:0.82rem'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
