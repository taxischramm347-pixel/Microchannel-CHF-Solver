import streamlit as st

st.set_page_config(page_title="STALWART Reality Engine", layout="wide")

# --- CUSTOM SCI-FI CSS ---
st.markdown("""
<style>
    h1, h2, h3, .stMetric label { color: #00ffcc !important; font-family: 'Courier New', monospace; }
    .stMetric [data-testid="stMetricValue"] { color: #ffcc00 !important; }
    div[data-testid="stAlert"] { border: 1px solid #00ffcc; background-color: rgba(0, 255, 204, 0.05); }
    div[data-testid="stException"] { font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- MATERIAL PHYSICS CONSTANTS ---
# Dictionary format: { "Material": (Melting Point K, Yield Strength MPa) }
MATERIAL_DATA = {
    "Hafnium Oxide": (3031, 400.0),      # High heat, high strength ceramic
    "Yttrium Barium Copper Oxide": (1273, 50.0), # Superconductor ceramic, brittle
    "Bismuth": (544, 15.0)               # Low melting point, highly brittle metal
}

COOLING_DATA = {
    "Passive Radiator": 0.85, # K/W thermal resistance
    "Microchannel Array": 0.25,
    "Active Cryo": 0.05
}

# --- SIDEBAR INPUTS ---
st.sidebar.title("4. MANUAL OVERRIDE PARAMETERS")
core_material = st.sidebar.selectbox("Core Material", list(MATERIAL_DATA.keys()))
power_draw = st.sidebar.number_input("Power Draw (Watts)", value=150.00, min_value=0.0)
system_voltage = st.sidebar.number_input("System Voltage (Volts)", value=12.00, min_value=0.1)
struct_load = st.sidebar.number_input("Structural Load (MPa)", value=20.00, min_value=0.0)

st.sidebar.markdown("### Advanced Thermal Parameters")
cooling_mech = st.sidebar.selectbox("Cooling Mechanism", list(COOLING_DATA.keys()))
ambient_temp = st.sidebar.number_input("Ambient Temp (K)", value=298.0, min_value=0.0)

raw_theory = st.sidebar.text_area("Raw Theory / Context Log:")

# --- FETCH REAL-WORLD CONSTANTS ---
melt_limit, yield_limit = MATERIAL_DATA[core_material]
thermal_res = COOLING_DATA[cooling_mech]

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
    colA.metric("POWER INPUT", f"{power_draw:.2f} W")
    colB.metric("COOLING RESISTANCE", f"{thermal_res} K/W")
    colC.metric("MATERIAL MELT LIMIT", f"{melt_limit} K") 

    if st.button("RUN THERMAL SWEEP", key="btn_thermal"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        # Math Execution
        calc_temp = ambient_temp + (power_draw * thermal_res)
        
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$T_{core}=T_{ambient}+(P\\times R_{th})$$")
        
        st.markdown("**Output Metrics:**")
        out_col1, out_col2, out_col3 = st.columns(3)
        out_col1.metric(label="Calculated Core Temp", value=f"{calc_temp:.2f} K")
        out_col2.metric(label="Margin to Meltdown", value=f"{melt_limit - calc_temp:.2f} K") 
        out_col3.metric(label="Ambient Baseline", value=f"{ambient_temp:.1f} K") 
        
        st.markdown("**System Analysis Log:**")
        if calc_temp >= melt_limit:
            st.error(f"🚨 CRITICAL FAILURE: Core temp ({calc_temp:.1f} K) exceeds {core_material} thermal limit ({melt_limit} K). MELTDOWN IMMINENT.")
        else:
            st.success(f"✅ SYSTEM STABLE: Core temp ({calc_temp:.1f} K) is within the {core_material} safe zone ({melt_limit} K).")
        
        if raw_theory:
            st.info(f"**Context Logged:** {raw_theory}")

# --- TAB 2: POWER MATRIX ---
with tab2:
    st.subheader("ACTIVE TELEMETRY: POWER MATRIX")
    colA, colB, colC = st.columns(3)
    colA.metric("POWER INPUT", f"{power_draw:.2f} W")
    colB.metric("SYSTEM VOLTAGE", f"{system_voltage:.2f} V")
    colC.metric("EXPECTED AMPERAGE", f"{(power_draw/system_voltage):.2f} A") 

    if st.button("RUN POWER SWEEP", key="btn_power"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        # Math Execution
        current = power_draw / system_voltage
        resistance = system_voltage / current if current > 0 else float('inf')
        
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$I=\\frac{P}{V}$$")
        st.markdown("$$R=\\frac{V}{I}$$")
        
        st.markdown("**Output Metrics:**")
        out_col1, out_col2, out_col3 = st.columns(3)
        out_col1.metric(label="Total Power (Watts)", value=f"{power_draw:.2f} W")
        out_col2.metric(label="Current (Amps)", value=f"{current:.2f} A") 
        out_col3.metric(label="Circuit Resistance", value=f"{resistance:.4f} Ω" if current > 0 else "Infinite") 
        
        st.markdown("**System Analysis Log:**")
        if current > 50.0:
            st.warning(f"⚠️ HIGH CURRENT WARNING: {current:.1f} A exceeds standard limits. Risk of plasma arcing unless operating within a superconducting matrix.")
        else:
            st.success(f"✅ ELECTRICAL STABLE: {current:.1f} A flows safely through the circuit matrix.")
        
        if raw_theory:
            st.info(f"**Context Logged:** {raw_theory}")

# --- TAB 3: STRUCTURAL LIMITS ---
with tab3:
    st.subheader("ACTIVE TELEMETRY: STRUCTURAL LIMITS")
    colA, colB = st.columns(2)
    colA.metric("APPLIED LOAD", f"{struct_load:.2f} MPa")
    colB.metric("MATERIAL YIELD STRENGTH", f"{yield_limit:.2f} MPa") 
    
    if st.button("RUN STRUCTURAL SWEEP", key="btn_struct"):
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        
        # Math Execution
        safety_factor = yield_limit / struct_load if struct_load > 0 else float('inf')
        
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$\\sigma_{load}\\le\\sigma_{yield}$$")
        st.markdown("$$Safety\\ Factor=\\frac{\\sigma_{yield}}{\\sigma_{load}}$$")
        
        st.markdown("**Output Metrics:**")
        out_col1, out_col2, out_col3 = st.columns(3)
        out_col1.metric(label="Structural Load", value=f"{struct_load:.2f} MPa")
        out_col2.metric(label="Material Yield", value=f"{yield_limit:.2f} MPa") 
        out_col3.metric(label="Safety Factor", value=f"{safety_factor:.2f}") 
        
        st.markdown("**System Analysis Log:**")
        if struct_load >= yield_limit:
            st.error(f"🚨 CRITICAL FAILURE: Applied load ({struct_load:.1f} MPa) exceeds {core_material} yield strength ({yield_limit:.1f} MPa). FRACTURE IMMINENT.")
        elif safety_factor < 1.5:
            st.warning(f"⚠️ CAUTION: Safety factor is {safety_factor:.2f}. Structural integrity is holding, but margin is extremely thin. Microfractures possible.")
        else:
            st.success(f"✅ STRUCTURAL STABLE: Shielding matrix and core geometry easily withstand {struct_load:.1f} MPa.")
            
        if raw_theory:
            st.info(f"**Context Logged:** {raw_theory}")
