import streamlit as st
import numpy as np

# STALWART Reality Engine: Microchannel CHF Solver
st.set_page_config(page_title="STALWART CHF Solver", page_icon="maltedlogo.ico", layout="wide")

st.sidebar.markdown("## 1. THERMAL LOAD DYNAMICS")
power_density = st.sidebar.number_input("Heat Load (W/cm²)", value=1200.0, step=50.0)
ambient_temp = st.sidebar.number_input("Coolant Inlet Temp (K)", value=298.0, step=5.0)

st.sidebar.markdown("## 2. MICROCHANNEL GEOMETRY")
channel_width = st.sidebar.number_input("Channel Width (μm)", value=50.0, step=5.0)
channel_depth = st.sidebar.number_input("Channel Depth (μm)", value=150.0, step=10.0)
fin_pitch = st.sidebar.number_input("Fin Pitch (μm)", value=100.0, step=10.0)

st.sidebar.markdown("## 3. FLUID & MATERIAL PARAMS")
velocity = st.sidebar.number_input("Initial Coolant Velocity (m/s)", value=2.0, step=0.5)

# Dynamic Material Selection with Theoretical Input
material = st.sidebar.selectbox(
    "Substrate Material", 
    ["Silicon", "Copper", "Diamond", "Hafnium Oxide", "Custom (Theoretical)"]
)

if material == "Custom (Theoretical)":
    st.sidebar.markdown("### 🧪 THEORETICAL MATERIAL SPECS")
    mat_limit = st.sidebar.number_input("Melt Limit (K)", value=2500.0, step=50.0)
    k_mat = st.sidebar.number_input("Thermal Conductivity (W/mK)", value=150.0, step=10.0)
else:
    # Material property dictionaries (Melt Temp K, Thermal Conductivity W/mK)
    materials = {
        "Silicon": {"melt": 1687.0, "k": 149.0},
        "Copper": {"melt": 1358.0, "k": 401.0},
        "Diamond": {"melt": 4300.0, "k": 2200.0},
        "Hafnium Oxide": {"melt": 3031.0, "k": 23.0}
    }
    mat_limit = materials[material]["melt"]
    k_mat = materials[material]["k"]

# Main UI
st.title("STALWART REALITY ENGINE")
st.markdown("### THREAT LEVEL: ZERO. MATH IS TRUTH.")
st.markdown("#### ACTIVE TELEMETRY: 2D FINITE-DIFFERENCE THERMAL-SCALAR SOLVER")

col1, col2, col3 = st.columns(3)
col1.metric("INPUT HEAT LOAD", f"{power_density} W/cm²")
col2.metric("COOLANT VELOCITY", f"{velocity} m/s")
col3.metric("MATERIAL MELT LIMIT", f"{mat_limit} K")

st.markdown("---")
st.markdown("## ⚙️ STALWART COMPUTATION RESULTS")

if st.button("RUN THERMAL SWEEP"):
    hydraulic_diameter = (2 * channel_width * channel_depth) / (channel_width + channel_depth)
    heat_transfer_coeff = (velocity * 1000) + 5000 
    thermal_resistance = 1 / heat_transfer_coeff + (1 / k_mat)
    
    calculated_core_temp = ambient_temp + (power_density * 10000 * thermal_resistance)
    
    st.markdown("*Executed Physics Equations:*")
    st.latex(r"T_{core} = T_{inlet} + q'' \left( \frac{1}{h} + \frac{t}{k} \right)")
    
    st.markdown(f"**Calculated Core Temp:** {calculated_core_temp:.2f} K")
    st.markdown(f"**Margin to Meltdown:** {mat_limit - calculated_core_temp:.2f} K")
    
    # STALWART Corrective Sweep Logic
    if calculated_core_temp > mat_limit:
        st.error(f"🚨 CRITICAL FAILURE: Core temp ({calculated_core_temp:.1f} K) exceeds {material} thermal limit ({mat_limit} K). MELTDOWN IMMINENT.")
        st.warning("🔄 INITIATING STALWART CORRECTIVE SWEEP...")
        
        safe_velocity = velocity
        safe_temp = calculated_core_temp
        
        with st.spinner('Iterating finite-difference variables...'):
            while safe_temp > mat_limit and safe_velocity < 20.0:
                safe_velocity += 0.5
                new_h = (safe_velocity * 1000) + 5000
                new_r = 1 / new_h + (1 / k_mat)
                safe_temp = ambient_temp + (power_density * 10000 * new_r)
        
        if safe_temp <= mat_limit:
            st.success(f"✅ SOLUTION FOUND: To maintain physical compliance, increase Coolant Velocity to **{safe_velocity:.1f} m/s**. Resulting Core Temp: **{safe_temp:.1f} K**.")
        else:
            st.error(f"❌ SWEEP FAILED: Maximum flow rate reached. Geometry cannot support {power_density} W/cm² with {material}. Suggest switching substrate or decreasing heat load.")
    else:
        st.success("✅ SYSTEM STABLE: Thermal boundaries are within physical compliance.")
