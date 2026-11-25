"""Streamlit dashboard: streamlit run app.py"""
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from src.models import recommend_crops, predict_yield, CROPS
from src.advisor import (fertilizer_advice, irrigation_advice, disease_risk,
                         simulate_soil_moisture)
from src.leaf import analyze_leaf

st.set_page_config(page_title="AgriSense AI", page_icon="🌾", layout="wide")
st.title("🌾 AgriSense AI – Smart Agriculture using AI")
st.caption("Crop recommendation · Yield prediction · Fertilizer · Irrigation · Disease risk · Leaf analysis")

with st.sidebar:
    st.header("Soil & weather inputs")
    N = st.slider("Nitrogen (N) kg/ha", 0, 140, 80)
    P = st.slider("Phosphorus (P) kg/ha", 5, 145, 45)
    K = st.slider("Potassium (K) kg/ha", 5, 205, 40)
    ph = st.slider("Soil pH", 4.0, 9.0, 6.5, 0.1)
    temp = st.slider("Temperature °C", 8, 44, 25)
    hum = st.slider("Humidity %", 14, 100, 70)
    rain = st.slider("Rainfall mm", 20, 300, 100)
    area = st.number_input("Field area (hectares)", 0.1, 500.0, 2.0)

tabs = st.tabs(["🌱 Crop & Yield", "🧪 Fertilizer", "💧 Irrigation", "🍂 Disease Risk", "📷 Leaf Analysis"])

with tabs[0]:   
    recs = recommend_crops(N, P, K, ph, temp, hum, rain)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top recommended crops")
        for crop, p in recs:
            st.write(f"**{crop.title()}** – {p}% confidence")
            st.progress(min(int(p), 100))
    with c2:
        st.subheader("Yield estimate")
        crop = st.selectbox("Crop", CROPS, index=CROPS.index(recs[0][0]))
        per_ha, total = predict_yield(crop, N, P, K, ph, temp, hum, rain, area)
        st.metric("Expected yield", f"{per_ha} t/ha")
        st.metric(f"Total for {area} ha", f"{total} tonnes")
    st.session_state["crop"] = crop

crop = st.session_state.get("crop", recs[0][0])

with tabs[1]:
    st.subheader(f"Fertilizer plan for {crop.title()}")
    for t in fertilizer_advice(crop, N, P, K, ph):
        st.info(t)

with tabs[2]:
    st.subheader("Irrigation planner")
    c1, c2 = st.columns(2)
    sm = c1.slider("Current soil moisture %", 0, 100, 30)
    rc = c2.slider("Rain chance next 24h %", 0, 100, 20)
    action, mm, msg = irrigation_advice(crop, sm, temp, rc)
    st.success(f"**{action}**" + (f" – apply about {mm} mm" if mm else "") + f". {msg}")
    st.markdown("**7-day simulation** (automatic irrigation)")
    rain_days = [0, 0, 10, 0, 0, 20, 0]
    sim = pd.DataFrame(simulate_soil_moisture(sm, temp, rain_days, crop))
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(sim["day"], sim["soil_moisture"], marker="o", color="green", label="Soil moisture %")
    ax.bar(sim["day"], sim["irrigation_mm"], alpha=0.4, label="Irrigation mm")
    ax.set_xlabel("Day"); ax.legend(); st.pyplot(fig)
    st.dataframe(sim, use_container_width=True)

with tabs[3]:
    st.subheader("Fungal disease risk")
    lw = st.slider("Leaf wetness (hours/day)", 0, 24, 8)
    score, level = disease_risk(hum, temp, lw)
    st.metric("Risk score", f"{score}/100", level)
    st.progress(score)

with tabs[4]:
    st.subheader("Upload a leaf photo")
    up = st.file_uploader("Leaf image (plain background works best)", type=["jpg", "jpeg", "png"])
    if up:
        img = Image.open(up)
        status, pct, dx = analyze_leaf(img)
        c1, c2 = st.columns(2)
        c1.image(img, width=250)
        c2.metric("Status", status)
        c2.write(pct); c2.write(dx)
    else:
        st.caption("Try the images in the `sample_leaves` folder.")
