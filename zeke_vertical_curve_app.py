import streamlit as st

st.set_page_config(page_title="Zeke's Vertical Curve App", layout="centered")

st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

st.header("Vertical Curve Inputs")

# BVC and EVC station & elevation inputs
bvc_station = st.number_input("Begin Vertical Curve (BVC) Station", step=1.0)
bvc_elevation = st.number_input("BVC Elevation", step=0.01)

evc_station = st.number_input("End Vertical Curve (EVC) Station", step=1.0)
evc_elevation = st.number_input("EVC Elevation", step=0.01)

# PVI station input (optional override)
pvi_station = st.number_input("Point of Vertical Intersection (PVI) Station", value=(bvc_station + evc_station) / 2, step=1.0)
pvi_elevation = st.number_input("PVI Elevation", step=0.01)

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
k_value = None
if use_custom_k:
    k_value = st.number_input("K-value (optional)", step=0.01)

# Compute curve geometry
curve_length = evc_station - bvc_station
grade_in = (pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100 if pvi_station != bvc_station else 0
grade_out = (evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100 if evc_station != pvi_station else 0
a_value = grade_out - grade_in

if not use_custom_k:
    if a_value != 0:
        k_value = curve_length / abs(a_value)
    else:
        k_value = "Undefined (A = 0)"

# Output results
st.header("Results")
st.markdown(f"**Curve Length:** {curve_length:.2f} units")
st.markdown(f"**Grade In (g₁):** {grade_in:.3f} %")
st.markdown(f"**Grade Out (g₂):** {grade_out:.3f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.3f} %")
st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.2f}'}")