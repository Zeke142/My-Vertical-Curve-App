import streamlit as st

st.set_page_config(page_title="Zeke's Vertical Curve App", layout="centered")

st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

# Input Mode Selection
input_mode = st.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

# Elevation-Based Input Mode
if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")

    bvc_station = st.number_input("BVC Station", step=1.0, format="%.2f")
    bvc_elevation = st.number_input("BVC Elevation", step=0.01)

    evc_station = st.number_input("EVC Station", step=1.0, format="%.2f")
    evc_elevation = st.number_input("EVC Elevation", step=0.01)

    pvi_station = st.number_input("PVI Station", value=(bvc_station + evc_station) / 2, step=1.0, format="%.2f")
    pvi_elevation = st.number_input("PVI Elevation", step=0.01)

    curve_length = evc_station - bvc_station
    g1 = (pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100 if pvi_station != bvc_station else 0
    g2 = (evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100 if evc_station != pvi_station else 0

# Grade-Based Input Mode
else:
    st.subheader("Grade-Based Inputs")

    bvc_station = st.number_input("BVC Station", step=1.0, format="%.2f")
    evc_station = st.number_input("EVC Station", step=1.0, format="%.2f")
    curve_length = evc_station - bvc_station

    bvc_elevation = st.number_input("BVC Elevation", step=0.01)
    g1 = st.number_input("Grade In (g₁) [%]", step=0.01, format="%.2f")
    g2 = st.number_input("Grade Out (g₂) [%]", step=0.01, format="%.2f")

# Calculated values
a_value = g2 - g1

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
if use_custom_k:
    k_value = st.number_input("K-value", step=0.01)
else:
    if a_value == 0:
        k_value = "Undefined (g₁ = g₂)"
    else:
        k_value = curve_length / abs(a_value)

# Results Display
st.header("Results")
st.markdown(f"**Curve Length (L):** {curve_length:.4f} ft")
st.markdown(f"**Grade In (g₁):** {g1:.4f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.4f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.4f} %")
st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.4f}'}")

# Elevation & Grade at Any Station
st.subheader("Elevation at Any Station")

station_input = st.number_input("Enter Station", step=1.0, format="%.2f")

if bvc_station <= station_input <= evc_station:
    x = station_input - bvc_station  # horizontal distance from BVC
    g1_decimal = g1 / 100
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length) if curve_length != 0 else bvc_elevation
    grade_at_x = g1 + (a_value * x / curve_length) if curve_length != 0 else g1

    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {station_input:.2f}:** {grade_at_x:.4f} %")
else:
    st.warning("Station is outside the limits of the vertical curve.")