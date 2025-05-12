import streamlit as st

st.set_page_config(page_title="Zeke's Vertical Curve App", layout="centered")

st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

st.header("Vertical Curve Inputs")

# Begin and End Points
bvc_station = st.number_input("Begin Vertical Curve (BVC) Station", step=1.0)
bvc_elevation = st.number_input("BVC Elevation", step=0.01)

evc_station = st.number_input("End Vertical Curve (EVC) Station", step=1.0)
evc_elevation = st.number_input("EVC Elevation", step=0.01)

# PVI Info
pvi_station = st.number_input("PVI Station", value=(bvc_station + evc_station) / 2, step=1.0)
pvi_elevation = st.number_input("PVI Elevation", step=0.01)

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
k_value = None
if use_custom_k:
    k_value = st.number_input("K-value (optional)", step=0.01)

# Derived values
curve_length = evc_station - bvc_station
g1 = (pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100 if pvi_station != bvc_station else 0
g2 = (evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100 if evc_station != pvi_station else 0
a_value = g2 - g1

if not use_custom_k:
    if a_value != 0:
        k_value = curve_length / abs(a_value)
    else:
        k_value = "Undefined (A = 0)"

# Output results
st.header("Results")
st.markdown(f"**Curve Length (L):** {curve_length:.2f} units")
st.markdown(f"**Grade In (g₁):** {g1:.3f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.3f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.3f} %")
st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.2f}'}")

# Elevation at any station
st.subheader("Elevation at a Station")

station_input = st.number_input("Enter station to compute elevation:", step=1.0)

if bvc_station <= station_input <= evc_station:
    x = station_input - bvc_station  # distance from BVC
    g1_decimal = g1 / 100
    elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
    st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.3f}")
else:
    st.warning("Station is outside the limits of the vertical curve.")