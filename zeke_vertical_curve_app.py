import streamlit as st

st.set_page_config(page_title="Zeke's Vertical Curve App", layout="centered")
st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

# Utility function to convert text to float safely
def to_float(value):
    try:
        return float(value)
    except:
        return None

# Input Mode Selection
input_mode = st.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

# Elevation-Based Input Mode
if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")

    bvc_station = to_float(st.text_input("BVC Station", value="", placeholder="e.g. 1000.00", type="number"))
    bvc_elevation = to_float(st.text_input("BVC Elevation", value="", placeholder="e.g. 500.00", type="number"))

    evc_station = to_float(st.text_input("EVC Station", value="", placeholder="e.g. 1100.00", type="number"))
    evc_elevation = to_float(st.text_input("EVC Elevation", value="", placeholder="e.g. 510.00", type="number"))

    pvi_station = to_float(st.text_input("PVI Station", value="", placeholder="e.g. 1050.00", type="number"))
    pvi_elevation = to_float(st.text_input("PVI Elevation", value="", placeholder="e.g. 505.00", type="number"))

    if None not in [bvc_station, evc_station, bvc_elevation, evc_elevation, pvi_station, pvi_elevation]:
        curve_length = evc_station - bvc_station
        g1 = ((pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100) if pvi_station != bvc_station else 0.0
        g2 = ((evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100) if evc_station != pvi_station else 0.0
    else:
        curve_length = g1 = g2 = None

else:
    st.subheader("Grade-Based Inputs")

    bvc_station = to_float(st.text_input("BVC Station", value="", placeholder="e.g. 1000.00", type="number"))
    evc_station = to_float(st.text_input("EVC Station", value="", placeholder="e.g. 1100.00", type="number"))
    bvc_elevation = to_float(st.text_input("BVC Elevation", value="", placeholder="e.g. 500.00", type="number"))
    g1 = to_float(st.text_input("Grade In (g₁) [%]", value="", placeholder="e.g. 1.25", type="number"))
    g2 = to_float(st.text_input("Grade Out (g₂) [%]", value="", placeholder="e.g. -0.75", type="number"))

    if None not in [bvc_station, evc_station]:
        curve_length = evc_station - bvc_station
    else:
        curve_length = None

# Common Calculations
a_value = (g2 - g1) if None not in [g1, g2] else None

# Optional K-value
use_custom_k = st.checkbox("Enter custom K-value?")
if use_custom_k:
    k_value = to_float(st.text_input("K-value", value="", placeholder="e.g. 200.00", type="number"))
else:
    if a_value is not None and curve_length not in [None, 0]:
        k_value = curve_length / abs(a_value) if a_value != 0 else "Undefined (A = 0)"
    else:
        k_value = "Undefined (check inputs)"

# Display Summary
if None not in [curve_length, g1, g2, a_value]:
    st.header("Results")
    st.markdown(f"**Curve Length (L):** {curve_length:.4f} ft")
    st.markdown(f"**Grade In (g₁):** {g1:.4f} %")
    st.markdown(f"**Grade Out (g₂):** {g2:.4f} %")
    st.markdown(f"**A = g₂ - g₁:** {a_value:.4f} %")
    st.markdown(f"**K-value:** {k_value if isinstance(k_value, str) else f'{k_value:.4f}'}")

# Elevation and Grade at Any Station
st.subheader("Elevation at Any Station")
station_input = to_float(st.text_input("Enter Station", value="", placeholder="e.g. 1045.00", type="number"))

if None not in [bvc_station, evc_station, station_input, bvc_elevation, g1, a_value, curve_length]:
    if bvc_station <= station_input <= evc_station:
        x = station_input - bvc_station  # horizontal distance from BVC
        g1_decimal = g1 / 100

        if curve_length != 0:
            elevation = bvc_elevation + g1_decimal * x + (a_value / 100) * x**2 / (2 * curve_length)
            grade_at_x = g1 + (a_value * x / curve_length)
        else:
            elevation = bvc_elevation
            grade_at_x = g1

        st.markdown(f"**Elevation at station {station_input:.2f}:** {elevation:.4f} ft")
        st.markdown(f"**Grade at station {station_input:.2f}:** {grade_at_x:.4f} %")
    else:
        st.warning("Station is outside the limits of the vertical curve.")
elif station_input is not None:
    st.warning("Please complete all required inputs before calculating elevation.")