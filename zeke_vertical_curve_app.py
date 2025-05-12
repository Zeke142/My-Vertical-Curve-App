import streamlit as st

st.set_page_config(page_title="Zeke's Vertical Curve App", layout="centered")

st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

# Initialize session state defaults
defaults = {
    "bvc_station": 0.0,
    "bvc_elevation": 0.0,
    "evc_station": 0.0,
    "evc_elevation": 0.0,
    "pvi_station": 0.0,
    "pvi_elevation": 0.0,
    "g1": 0.0,
    "g2": 0.0,
    "k_value": 0.0,
    "station_input": 0.0
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Input Mode Selection
input_mode = st.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

# Elevation-Based Input Mode
if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")

    st.session_state.bvc_station = st.number_input("BVC Station", value=st.session_state.bvc_station, step=1.0, format="%.2f", key="bvc_station")
    st.session_state.bvc_elevation = st.number_input("BVC Elevation", value=st.session_state.bvc_elevation, step=0.01, key="bvc_elevation")

    st.session_state.evc_station = st.number_input("EVC Station", value=st.session_state.evc_station, step=1.0, format="%.2f", key="evc_station")
    st.session_state.evc_elevation = st.number_input("EVC Elevation", value=st.session_state.evc_elevation, step=0.01, key="evc_elevation")

    default_pvi = (st.session_state.bvc_station + st.session_state.evc_station) / 2
    st.session_state.pvi_station = st.number_input("PVI Station", value=st.session_state.pvi_station or default_pvi, step=1.0, format="%.2f", key="pvi_station")
    st.session_state.pvi_elevation = st.number_input("PVI Elevation", value=st.session_state.pvi_elevation, step=0.01, key="pvi_elevation")

    curve_length = st.session_state.evc_station - st.session_state.bvc_station
    g1 = ((st.session_state.pvi_elevation - st.session_state.bvc_elevation) / (st.session_state.pvi_station - st.session_state.bvc_station) * 100) if st.session_state.pvi_station != st.session_state.bvc_station else 0.0
    g2 = ((st.session_state.evc_elevation - st.session_state.pvi_elevation) / (st.session_state.evc_station - st.session_state.pvi_station) * 100) if st.session_state.evc_station != st.session_state.pvi_station else 0.0

else:
    st.subheader("Grade-Based Inputs")

    st.session_state.bvc_station = st.number_input("BVC Station", value=st.session_state.bvc_station, step=1.0, format="%.2f", key="bvc_station")
    st.session_state.evc_station = st.number_input("EVC Station", value=st.session_state.evc_station, step=1.0, format="%.2f", key="evc_station")
    curve_length = st.session_state.evc_station - st.session_state.bvc_station

    st.session_state.bvc_elevation = st.number_input("BVC Elevation", value=st.session_state.bvc_elevation, step=0.01, key="bvc_elevation")
    g1 = st.number_input("Grade In (g₁) [%]", value=st.session_state.g1, step=0.01, format="%.2f", key="g1")
    g2 = st.number_input("Grade Out (g₂) [%]", value=st.session_state.g2, step=0.01, format="%.2f", key="g2")

# Common Calculations
a_value = g2 - g1

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
if use_custom_k:
    st.session_state.k_value = st.number_input("K-value", value=st.session_state.k_value, step=0.01, key="k_value")
else:
    if a_value == 0 or curve_length == 0:
        k_value = "Undefined (check inputs)"
    else:
        k_value = curve_length / abs(a_value)

# Display Summary
st.header("Results")
st.markdown(f"**Curve Length (L):** {curve_length:.4f} ft")
st.markdown(f"**Grade In (g₁):** {g1:.4f} %")
st.markdown(f"**Grade Out (g₂):** {g2:.4f} %")
st.markdown(f"**A = g₂ - g₁:** {a_value:.4f} %")
st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.4f}'}")

# Elevation and Grade at Any Station
st.subheader("Elevation at Any Station")
st.session_state.station_input = st.number_input("Enter Station", value=st.session_state.station_input, step=1.0, format="%.2f", key="station_input")

if st.session_state.bvc_station <= st.session_state.station_input <= st.session_state.evc_station:
    x = st.session_state.station_input - st.session_state.bvc_station
    g1_decimal = g1 / 100

    if curve_length != 0:
        elevation = st.session_state.bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
        grade_at_x = g1 + (a_value * x / curve_length)
    else:
        elevation = st.session_state.bvc_elevation
        grade_at_x = g1

    st.markdown(f"**Elevation at station {st.session_state.station_input:.2f}:** {elevation:.4f} ft")
    st.markdown(f"**Grade at station {st.session_state.station_input:.2f}:** {grade_at_x:.4f} %")
else:
    st.warning("Station is outside the limits of the vertical curve.")