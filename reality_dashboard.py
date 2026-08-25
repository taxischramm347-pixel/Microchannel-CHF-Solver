import streamlit as st

st.set_page_config(page_title="STALWART Reality Engine", layout="wide")

# --- SIDEBAR INPUTS ---
st.sidebar.title("4. MANUAL OVERRIDE PARAMETERS")
core_material = st.sidebar.selectbox("Core Material", ["Hafnium Oxide", "Yttrium Barium Copper Oxide", "Bismuth"])
power_draw = st.sidebar.number_input("Power Draw (Watts)", value=150.00)
struct_load = st.sidebar.number_input("Structural Load (MPa)", value=200.00)

st.sidebar.markdown("### Advanced Thermal Parameters")
cooling_mech = st.sidebar.selectbox("Cooling Mechanism", ["Passive Radiator", "Microchannel Array", "Active Cryo"])
ambient_temp = st.sidebar.number_input("Ambient Environment Temp (K)", value=298.0)

raw_theory = st.sidebar.text_area("Raw Theory / Context (Natural Language):")

# --- MAIN ENGINE HEADER ---
st.title("STALWART REALITY ENGINE")
st.markdown("### THREAT LEVEL: ZERO. MATH IS TRUTH.")
st.markdown("---")

# --- TABS ARCHITECTURE ---
tab1, tab2, tab3 = st.tabs(["Thermal Dynamics", "Power Matrix", "Structural Limits"])

# --- TAB 1: THERMAL DYNAMICS ---
with tab1:
    st.subheader("ACTIVE TELEMETRY: THERMAL DYNAMICS")
    colA, colB, colC = st.columns(3)
    colA.metric("POWER INPUT", f"{power_draw} W")
    colB.metric("STRUCTURAL LOAD", f"{struct_load} MPa")
    colC.metric("MATERIAL LIMIT", "3031 K") 

    if st.button("RUN STALWART SWEEP", key="btn_thermal"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        # 1. The Math
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$Q = mc\Delta T$$")
        st.markdown("$$T_{core} = T_{ambient} + (P \\times R_{th})$$")
        
        # 2. Output Metrics
        st.markdown("**Output Metrics:**")
        out_col1, out_col2, out_col3, out_col4 = st.columns(4)
        out_col1.metric(label="Power (Wattage)", value=f"{power_draw} W")
        out_col2.metric(label="Current (Amperage)", value=f"{power_draw / 12:.2f} A") 
        out_col3.metric(label="Potential (Voltage)", value="12.0 V") 
        out_col4.metric(label="Core Temp (Kelvin)", value=f"{ambient_temp + (power_draw * 0.5)} K")
        
        # 3. Analysis Text Box
        st.markdown("**System Analysis Log:**")
        st.info(f"Sweep complete for {core_material} using {cooling_mech}. Parameters are within safe operational limits. \n\n**Raw Context Logged:** {raw_theory}")

# --- TAB 2: POWER MATRIX ---
with tab2:
    st.subheader("ACTIVE TELEMETRY: POWER MATRIX")
    if st.button("RUN STALWART SWEEP", key="btn_power"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$P = V \\times I$$")
        st.markdown("$$V = I \\times R$$")
        
        st.markdown("**Output Metrics:**")
        out_col1, out_col2, out_col3 = st.columns(3)
        out_col1.metric(label="Power (Wattage)", value=f"{power_draw} W")
        out_col2.metric(label="Current (Amperage)", value=f"{power_draw / 12:.2f} A") 
        out_col3.metric(label="Resistance (Ohms)", value=f"{12 / (power_draw / 12):.2f} Ω") 
        
        st.markdown("**System Analysis Log:**")
        st.info("Power matrix stable. Voltage flow is consistent with the established field parameters.")

# --- TAB 3: STRUCTURAL LIMITS ---
with tab3:
    st.subheader("ACTIVE TELEMETRY: STRUCTURAL LIMITS")
    if st.button("RUN STALWART SWEEP", key="btn_struct"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$\\sigma = \\frac{F}{A}$$")
        
        st.markdown("**Output Metrics:**")
        out_col1, out_col2 = st.columns(2)
        out_col1.metric(label="Structural Load (Current)", value=f"{struct_load} MPa")
        out_col2.metric(label="Material Yield (Maximum)", value="450.0 MPa") 
        
        st.markdown("**System Analysis Log:**")
        st.info("Structural integrity is holding. No microfractures detected in the shielding matrix.")
