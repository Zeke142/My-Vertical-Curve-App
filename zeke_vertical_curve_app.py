import streamlit as st

st.set_page_config(page_title="Zeke’s Vertical Curve App", layout="centered")

st.title("Zeke’s Vertical Curve App")
st.caption("“Ten toes down!”")

# Sidebar for mode selection
st.sidebar.title("Curve Mode")
input_mode = st.sidebar.radio("Choose Input Method:", ("Elevation-Based", "Grade-Based"))

# Helper: Retrieve session state or default
def get_state(key, default=0.0):
    return st.session_state.get(key, default)

# Elevation-Based Mode
if input_mode == "Elevation-Based":
    st.subheader("Elevation-Based Inputs")
    bvc_station = st.number_input("BVC Station", step=1.0, key="bvc_station")
    bvc_elevation = st.number_input("BVC Elevation", step=0.01, key="bvc_elevation")
    evc_station = st.number_input("EVC Station", step=1.0, key="evc_station")
    evc_elevation = st.number_input("EVC Elevation", step=0.01, key="evc_elevation")

    try:
        L = evc_station - bvc_station
        pvi_station = (bvc_station + evc_station) / 2
        pvi_elevation = (bvc_elevation + evc_elevation) / 2
        g1 = (pvi_elevation - bvc_elevation) / (pvi_station - bvc_station) * 100
        g2 = (evc_elevation - pvi_elevation) / (evc_station - pvi_station) * 100

        st.write(f"PVI Station (calculated): {pvi_station}")
        st.write(f"PVI Elevation (calculated): {pvi_elevation}")
        st.write(f"Grade In (g₁): {g1:.4f}%")
        st.write(f"Grade Out (g₂): {g2:.4f}%")
    except ZeroDivisionError:
        st.error("Curve length (L) or station difference cannot be zero.")

# Grade-Based Mode
elif input_mode == "Grade-Based":
    st.subheader("Grade-Based Inputs")
    bvc_station = st.number_input("BVC Station", step=1.0, key="bvc_station")
    evc_station = st.number_input("EVC Station", step=1.0, key="evc_station")
    bvc_elevation = st.number_input("BVC Elevation", step=0.01, key="bvc_elevation")
    g1 = st.number_input("Grade In (g₁) [%]", step=0.01, key="g1")
    g2 = st.number_input("Grade Out (g₂) [%]", step=0.01, key="g2")

    try:
        L = evc_station - bvc_station
        pvi_station = (bvc_station + evc_station) / 2
        pvi_elevation = bvc_elevation + (g1 / 100) * (pvi_station - bvc_station)

        st.write(f"PVI Station (calculated): {pvi_station}")
        st.write(f"PVI Elevation (calculated): {pvi_elevation}")
    except ZeroDivisionError:
        st.error("Curve length (L) cannot be zero.")

# Station Evaluation
st.subheader("Evaluate Elevation and Grade at a Station")
station = st.number_input("Enter Station to Evaluate", step=1.0, key="eval_station")

try:
    x = station - bvc_station
    a = (g2 - g1) / (2 * L)
    elevation = bvc_elevation + (g1 / 100) * x + a * x ** 2
    grade = g1 + (2 * a * x)

    st.success(f"Elevation at station {station}: {elevation:.4f}")
    st.success(f"Grade at station {station}: {grade:.4f}%")
except ZeroDivisionError:
    st.error("Invalid input: Division by zero. Check station inputs.")
except Exception as e:
    st.error(f"An error occurred: {e}")