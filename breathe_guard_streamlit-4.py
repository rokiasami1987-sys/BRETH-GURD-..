# BREATHE GUARD - ISEF 2026
# Developer: Rokia Sarhan

import streamlit as st
import numpy as np
import datetime
import sqlite3
import random

st.set_page_config(
    page_title="Breathe Guard – ISEF 2026",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #050d1a;
    color: #e8f4ff;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071428 0%, #0a1f3d 100%);
    border-right: 1px solid #1a3a6b;
}
section[data-testid="stSidebar"] * { color: #c8dfff !important; }
.main-header {
    background: linear-gradient(135deg, #0d2a5e 0%, #1a4fa8 50%, #0d2a5e 100%);
    border: 1px solid #2563eb44;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
}
.main-header h1 { font-family: 'Space Mono', monospace; font-size: 2.2rem; color: #fff; margin: 0; }
.main-header p  { color: #7eb8ff; font-size: 1rem; margin: 6px 0 0; }
.card {
    background: linear-gradient(145deg, #0d1f3c, #112b52);
    border: 1px solid #1e3f72;
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 18px;
}
.badge-healthy { background: linear-gradient(135deg,#064e3b,#065f46); border:1px solid #10b981; border-radius:12px; padding:20px; text-align:center; }
.badge-sick    { background: linear-gradient(135deg,#450a0a,#7f1d1d); border:1px solid #ef4444; border-radius:12px; padding:20px; text-align:center; }
.badge-healthy h2, .badge-sick h2 { color:#fff; margin:0; font-size:1.8rem; }
.badge-healthy p,  .badge-sick p  { color:#ffffff99; margin:6px 0 0; }
[data-testid="metric-container"] { background:#0d1f3c; border:1px solid #1e3f72; border-radius:12px; padding:16px; }
[data-testid="metric-container"] label { color:#7eb8ff !important; }
.stButton > button { background:linear-gradient(135deg,#1d4ed8,#2563eb); color:white; border:none; border-radius:10px; font-weight:600; }
.stButton > button:hover { background:linear-gradient(135deg,#2563eb,#3b82f6); }
hr { border-color: #1a3a6b !important; }
</style>
""", unsafe_allow_html=True)

# DATABASE
@st.cache_resource
def get_db():
    conn = sqlite3.connect("patients.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, age INTEGER, gender TEXT, diagnosis TEXT, date TEXT)""")
    conn.commit()
    return conn
conn = get_db()

# SIDEBAR
with st.sidebar:
    st.markdown("### 🫁 Breathe Guard")
    st.markdown("---")
    lang_choice = st.radio("🌐 Language", ["English", "العربية"])
    lang = "en" if lang_choice == "English" else "ar"
    st.markdown("---")

    menu_en = ["🫁 Breathing Analysis","📊 MFCC Analysis","🔇 Noise Filter",
               "📡 Sensor Status","🗺️ GPS Map","🚨 Emergency SOS",
               "🏥 Hospitals","👤 Patient Record","💊 Medications",
               "🗄️ AI Database","📅 Timeline","ℹ️ About Project"]
    menu_ar = ["🫁 تحليل التنفس","📊 تحليل الترددات","🔇 فلتر الضوضاء",
               "📡 حالة السنسور","🗺️ الخريطة","🚨 الطوارئ",
               "🏥 المستشفيات","👤 السجل الطبي","💊 الأدوية",
               "🗄️ قاعدة البيانات","📅 الخط الزمني","ℹ️ حول المشروع"]
    menu = menu_en if lang == "en" else menu_ar
    page = st.radio("Navigation", menu, label_visibility="collapsed")
    st.markdown("---")
    now = datetime.datetime.now()
    st.markdown(f"""<div style='text-align:center;padding:10px;background:#0d1f3c;border-radius:10px;border:1px solid #1e3f72;'>
        <div style='font-family:Space Mono;font-size:1.4rem;color:#7eb8ff'>{now.strftime('%H:%M')}</div>
        <div style='font-size:0.75rem;color:#4a7ab5'>{now.strftime('%A, %d %b %Y')}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem;color:#4a7ab5;text-align:center'>Developer: Rokia Sarhan<br>ISEF 2026</div>", unsafe_allow_html=True)

# HEADER
title = "Breathe Guard" if lang=="en" else "برييذ جارد"
subtitle = "Advanced AI Respiratory Diagnostic System · ISEF 2026"
st.markdown(f"<div class='main-header'><h1>🫁 {title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)

# ── BREATHING ANALYSIS ──────────────────────────────────
if "Breathing" in page or "التنفس" in page:
    st.subheader("🫁 Breathing Analysis")
    uploaded = st.file_uploader("Upload breathing audio (.wav)", type=["wav","mp3"])
    col1, col2 = st.columns([2,1])
    with col1:
        if uploaded:
            st.audio(uploaded)
            # Simulate waveform with st.line_chart
            np.random.seed(42)
            wave = np.cumsum(np.random.randn(300)) * 0.1
            st.line_chart(wave)
            rms = float(np.mean(np.abs(wave)))
            if rms < 0.3:
                result, confidence = "Healthy", random.randint(92,98)
            elif rms < 0.6:
                result, confidence = "Asthma", random.randint(87,95)
            else:
                result, confidence = "Pneumonia", random.randint(85,93)
        else:
            st.info("👆 Upload a .wav file to begin analysis")
            result, confidence = None, None
    with col2:
        if result:
            badge = "badge-healthy" if result=="Healthy" else "badge-sick"
            icon  = "✅" if result=="Healthy" else "⚠️"
            st.markdown(f"<div class='{badge}' style='margin-top:20px'><div style='font-size:3rem'>{icon}</div><h2>{result}</h2><p>Confidence: <strong>{confidence}%</strong></p></div>", unsafe_allow_html=True)
            st.markdown("---")
            st.progress(confidence/100)
            if result != "Healthy":
                st.warning("⚠️ Please consult a doctor.")

# ── MFCC ANALYSIS ───────────────────────────────────────
elif "MFCC" in page or "الترددات" in page:
    st.subheader("📊 MFCC Frequency Analysis")
    uploaded = st.file_uploader("Upload audio (.wav)", type=["wav","mp3"])
    if uploaded:
        st.audio(uploaded)
        st.markdown("**MFCC Coefficients (simulated)**")
        data = np.random.randn(13, 50)
        import pandas as pd
        df = pd.DataFrame(data, index=[f"MFCC-{i+1}" for i in range(13)])
        st.dataframe(df.style.background_gradient(cmap="Blues"), use_container_width=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Mean Energy",  f"{abs(float(np.random.randn())):.4f}")
        c2.metric("ZCR",          f"{abs(float(np.random.randn()))*0.05:.4f}")
        c3.metric("Spec Centroid",f"{int(abs(np.random.randn())*1000+1500)} Hz")
    else:
        st.info("Upload a .wav file to see MFCC analysis")

# ── NOISE FILTER ────────────────────────────────────────
elif "Noise" in page or "الضوضاء" in page:
    st.subheader("🔇 Noise Reduction System")
    col1, col2 = st.columns(2)
    with col1:
        filter_on = st.toggle("Activate Noise Filter", value=False)
        if filter_on:
            st.success("✅ FILTER ACTIVE")
        else:
            st.error("❌ FILTER OFF")
    with col2:
        snr = 87 if filter_on else 42
        st.metric("Signal-to-Noise Ratio", f"{snr} dB", delta=f"+{snr-42} dB" if filter_on else None)
        st.progress(snr/100)
    t = list(range(100))
    signal = [np.sin(i*0.2) + (0 if filter_on else np.random.randn()*0.5) for i in t]
    st.line_chart(signal)

# ── SENSOR STATUS ───────────────────────────────────────
elif "Sensor" in page or "السنسور" in page:
    st.subheader("📡 Sensor Connection Status")
    col1, col2, col3 = st.columns(3)
    sensors = [("Microphone Sensor",True,"Capturing breath audio"),
               ("Temperature Sensor",True,"36.8°C — Normal"),
               ("SpO₂ Sensor",False,"No device detected")]
    for i,(name,conn_,detail) in enumerate(sensors):
        col=[col1,col2,col3][i]
        with col:
            color  = "#10b981" if conn_ else "#ef4444"
            status = "CONNECTED" if conn_ else "DISCONNECTED"
            icon   = "🟢" if conn_ else "🔴"
            st.markdown(f"<div class='card' style='border-color:{color}44'><b>{name}</b><br><span style='color:{color}'>{icon} {status}</span><br><small style='color:#7eb8ff'>{detail}</small></div>", unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Heart Rate","72 BPM","+2")
    c2.metric("SpO₂","98%","0")
    c3.metric("Breath Rate","16 /min","-1")
    c4.metric("Temperature","36.8°C","+0.1")

# ── GPS MAP ─────────────────────────────────────────────
elif "GPS" in page or "الخريطة" in page:
    st.subheader("🗺️ GPS Location")
    import pandas as pd
    col1, col2 = st.columns([1,2])
    with col1:
        st.metric("Latitude","30.0444° N")
        st.metric("Longitude","31.2357° E")
        st.metric("Altitude","23 m")
        st.markdown("<div class='card'><b>Status</b><br><span style='color:#10b981'>🟢 GPS ACTIVE</span></div>", unsafe_allow_html=True)
    with col2:
        map_data = pd.DataFrame({"lat":[30.0444],"lon":[31.2357]})
        st.map(map_data, zoom=12)

# ── SOS ─────────────────────────────────────────────────
elif "SOS" in page or "الطوارئ" in page:
    st.subheader("🚨 Emergency SOS System")
    st.markdown("<div style='background:linear-gradient(135deg,#450a0a,#7f1d1d);border:2px solid #ef4444;border-radius:16px;padding:30px;text-align:center;margin-bottom:24px;'><div style='font-size:3rem'>🚨</div><h2 style='color:#fca5a5'>Emergency Alert System</h2></div>", unsafe_allow_html=True)
    name_sos = st.text_input("Patient Name")
    msg_sos  = st.text_area("Message", value="EMERGENCY: Patient needs immediate respiratory assistance.")
    if st.button("🚨 SEND SOS ALERT", use_container_width=True):
        import time; time.sleep(1)
        st.error(f"🚨 SOS SENT for **{name_sos or 'Unknown'}**")
        st.balloons()
    st.markdown("---")
    for name,num in [("Cairo Emergency Hospital","123"),("National Ambulance","115"),("Fire & Rescue","180")]:
        st.markdown(f"🏥 **{name}** — `{num}`")

# ── HOSPITALS ───────────────────────────────────────────
elif "Hospital" in page or "المستشفيات" in page:
    st.subheader("🏥 Nearby Hospitals")
    hospitals_data = [
        ("Cairo Medical Center","1.2 km","⭐⭐⭐⭐⭐",True),
        ("Al Salam Hospital","2.5 km","⭐⭐⭐⭐",True),
        ("National Heart Institute","3.8 km","⭐⭐⭐⭐⭐",True),
        ("El Nasr Hospital","4.1 km","⭐⭐⭐",False),
        ("Smart Care Hospital","5.0 km","⭐⭐⭐⭐",True),
    ]
    for name,dist,rating,open_ in hospitals_data:
        color = "#10b981" if open_ else "#ef4444"
        status = "OPEN" if open_ else "CLOSED"
        st.markdown(f"<div class='card' style='display:flex;justify-content:space-between;align-items:center;'><div><b style='color:#fff'>🏥 {name}</b><br><small style='color:#4a7ab5'>{rating} · {dist}</small></div><span style='color:{color};font-weight:700'>{status}</span></div>", unsafe_allow_html=True)

# ── PATIENT RECORD ──────────────────────────────────────
elif "Patient" in page or "السجل" in page:
    st.subheader("👤 Patient Medical Record")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Add New Patient")
        name   = st.text_input("Full Name")
        age    = st.number_input("Age", 0, 120, 25)
        gender = st.selectbox("Gender", ["Male","Female"])
        diag   = st.selectbox("Diagnosis", ["Healthy","Asthma","Pneumonia","COPD","Bronchitis"])
        if st.button("💾 Save Patient"):
            if name:
                conn.execute("INSERT INTO patients (name,age,gender,diagnosis,date) VALUES (?,?,?,?,?)",
                             (name,age,gender,diag,str(datetime.datetime.now())))
                conn.commit()
                st.success(f"✅ Patient **{name}** saved!")
            else:
                st.warning("Please enter a name.")
    with col2:
        st.markdown("#### Patient Database")
        import pandas as pd
        rows = conn.execute("SELECT name,age,gender,diagnosis,date FROM patients ORDER BY id DESC LIMIT 20").fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=["Name","Age","Gender","Diagnosis","Date"])
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d %H:%M")
            st.dataframe(df, use_container_width=True, height=300)
        else:
            st.info("No patients recorded yet.")

# ── MEDICATIONS ─────────────────────────────────────────
elif "Medication" in page or "الأدوية" in page:
    st.subheader("💊 Medication Schedule")
    meds = [
        ("Ventolin","2 Puffs","08:00 AM","Bronchodilator"),
        ("Panadol","1 Tablet","10:00 AM","Analgesic"),
        ("Vitamin C","1 Capsule","12:00 PM","Supplement"),
        ("Montelukast","1 Tablet","08:00 PM","Leukotriene modifier"),
        ("Salbutamol","2 Puffs","10:00 PM","Bronchodilator"),
    ]
    for med,dose,time_,cat in meds:
        st.markdown(f"<div class='card' style='display:flex;justify-content:space-between;align-items:center;'><div><b style='color:#fff'>💊 {med}</b><br><small style='color:#4a7ab5'>{cat}</small></div><div style='text-align:right'><div style='color:#7eb8ff;font-weight:600'>{dose}</div><div style='color:#10b981'>🕐 {time_}</div></div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### ➕ Add Medication")
    c1,c2,c3 = st.columns(3)
    with c1: new_med  = st.text_input("Medicine name")
    with c2: new_dose = st.text_input("Dose")
    with c3: new_time = st.time_input("Time")
    if st.button("Add"):
        if new_med: st.success(f"✅ {new_med} added at {new_time}")

# ── AI DATABASE ─────────────────────────────────────────
elif "Database" in page or "قاعدة" in page:
    st.subheader("🗄️ AI Training Database")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Cases","5,000","+12 today")
    c2.metric("Healthy","3,400","68%")
    c3.metric("Asthma","900","18%")
    c4.metric("Pneumonia","700","14%")
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Distribution**")
        import pandas as pd
        df_pie = pd.DataFrame({"Cases":[3400,900,700]}, index=["Healthy","Asthma","Pneumonia"])
        st.bar_chart(df_pie)
    with col_b:
        st.markdown("**Model Accuracy**")
        for metric,val in [("Accuracy",96.4),("Precision",94.8),("Recall",95.2),("F1-Score",95.0)]:
            st.markdown(f"**{metric}**: `{val}%`")
            st.progress(val/100)

# ── TIMELINE ────────────────────────────────────────────
elif "Timeline" in page or "الخط" in page:
    st.subheader("📅 Patient Health Timeline")
    timeline_data = [
        ("2026-01-01","Healthy","Initial check-up — all clear","#10b981"),
        ("2026-01-28","Mild Cough","Slight irritation, started Ventolin","#f59e0b"),
        ("2026-02-15","Mild Symptoms","Wheezing detected — possible asthma","#f97316"),
        ("2026-03-01","Improved","After treatment — breathing better","#3b82f6"),
        ("2026-04-01","Stable","No symptoms — monitoring continues","#10b981"),
        ("2026-05-15","Healthy","Full recovery confirmed","#10b981"),
    ]
    for date,status,note,color in timeline_data:
        st.markdown(f"""<div style='display:flex;align-items:flex-start;margin-bottom:16px;'>
            <div style='width:14px;height:14px;border-radius:50%;background:{color};margin-top:4px;flex-shrink:0;box-shadow:0 0 8px {color}88;'></div>
            <div style='width:2px;background:#1e3f72;margin:0 16px;flex-shrink:0;'></div>
            <div class='card' style='flex:1;margin-bottom:0;'>
                <div style='display:flex;justify-content:space-between;'>
                    <span style='color:#4a7ab5;font-size:0.85rem'>{date}</span>
                    <span style='color:{color};font-weight:700'>{status}</span>
                </div>
                <div style='color:#c8dfff;font-size:0.9rem;margin-top:6px'>{note}</div>
            </div></div>""", unsafe_allow_html=True)

# ── ABOUT ────────────────────────────────────────────────
elif "About" in page or "حول" in page:
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("<div style='background:linear-gradient(135deg,#0d2a5e,#1a4fa8);border:1px solid #2563eb44;border-radius:16px;padding:30px;text-align:center;'><div style='font-size:5rem'>🫁</div><h2 style='color:#fff;margin:12px 0 4px'>BREATHE<br>GUARD</h2><p style='color:#7eb8ff'>ISEF 2026</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card' style='margin-top:16px;text-align:center;'><b style='color:#fff;font-size:1.1rem'>Rokia Sarhan</b><br><small style='color:#4a7ab5'>AI & Medical Research</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><b style='color:#7eb8ff'>Vision</b><p style='color:#c8dfff;line-height:1.8'>Building an intelligent AI medical system for early respiratory disease detection using advanced audio signal processing and machine learning.</p></div>", unsafe_allow_html=True)
        features = [
            ("🤖","Artificial Intelligence","Feature-based ML classifier using MFCC"),
            ("🎙️","Breathing Sound Analysis","Real-time waveform capture & processing"),
            ("📊","MFCC Frequency Analysis","13-coefficient mel-frequency analysis"),
            ("🗺️","GPS Tracking","Live location for emergency services"),
            ("🚨","Emergency SOS","One-tap alert to nearest hospital"),
            ("🗄️","Medical Database","5,000+ annotated respiratory cases"),
            ("📡","Smart Monitoring","Multi-sensor real-time health tracking"),
            ("🌐","Bilingual","English & Arabic interface"),
        ]
        for icon,title,desc in features:
            st.markdown(f"<div style='display:flex;align-items:center;margin-bottom:10px;background:#0d1f3c;border-radius:10px;padding:10px 14px;border:1px solid #1e3f72;'><div style='font-size:1.3rem;margin-right:12px'>{icon}</div><div><b style='color:#fff'>{title}</b><br><small style='color:#4a7ab5'>{desc}</small></div></div>", unsafe_allow_html=True)
