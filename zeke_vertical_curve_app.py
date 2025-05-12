import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Page config
st.set_page_config(page_title="Zeke’s Vertical Curve App", layout="centered")

# Title
st.title("Zeke’s Vertical Curve App")

# Sidebar Theme Selector
with st.sidebar:
    st.header("Theme Selector")
    theme = st.selectbox("Choose a theme", options=["HP Green", "Solarized Light", "Solarized Dark", "Classic Blue"])

    theme_colors = {
        "HP Green": {"bg": "#101010", "line": "#39FF14", "text": "#39FF14"},
        "Solarized Light": {"bg": "#fdf6e3", "line": "#268bd2", "text": "#657b83"},
        "Solarized Dark": {"bg": "#002b36", "line": "#2aa198", "text": "#93a1a1"},
        "Classic Blue": {"bg": "#ffffff", "line": "#1f77b4", "text": "#000000"},
    }

    colors = theme_colors[theme]

# Input Form
with st.form("curve_form"):
    st.subheader("Input Vertical Curve Parameters")

    x_pvi = st.number_input("Station of PVI", value=1000.0, format="%.6f")
    y_pvi = st.number_input("Elevation at PVI", value=500.0, format="%.6f")
    g1 = st.number_input("Initial Grade (in decimal, e.g., 0.03 for 3%)", value=0.03, format="%.6f")
    g2 = st.number_input("Final Grade (in decimal)", value=-0.02, format="%.6f")
    L = st.number_input("Length of Vertical Curve", value=200.0, format="%.6f")
    x = st.number_input("Station to Evaluate", value=1025.0, format="%.6f")
    show_plot = st.checkbox("Show Elevation Plot")

    submitted = st.form_submit_button("Calculate")

# Calculation
if submitted:
    A = g2 - g1
    dx = x - x_pvi
    y = y_pvi + g1 * dx + (A * dx**2) / (2 * L)

    st.success(f"Elevation at station {x} is {y}")

    if show_plot:
        st.subheader("Curve Profile")
        x_vals = np.linspace(x_pvi - L/2, x_pvi + L/2, 200)
        y_vals = y_pvi + g1*(x_vals - x_pvi) + (A/2)*((x_vals - x_pvi)**2) / L

        fig, ax = plt.subplots(facecolor=colors["bg"])
        fig.patch.set_facecolor(colors["bg"])
        ax.set_facecolor(colors["bg"])

        ax.plot(x_vals, y_vals, label="Vertical Curve", color=colors["line"])
        ax.axvline(x, color='red', linestyle='--', label=f"Station {x}")
        ax.plot(x, y, 'ro')
        ax.set_xlabel("Station", color=colors["text"])
        ax.set_ylabel("Elevation", color=colors["text"])
        ax.tick_params(colors=colors["text"])
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.3)

        st.pyplot(fig)

# Footer Tagline
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
    "<span style='font-size:1.2em;'>🛣️</span> "
    "<strong>Zeke’s Vertical Curve App</strong> "
    "<span style='font-size:1.2em;'>🧮</span><br>"
    "“Ten toes down!”"
    "</div>",
    unsafe_allow_html=True,
)
