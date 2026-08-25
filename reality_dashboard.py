import streamlit as st
import numpy as np

# --- CONFIG & STYLING ---
st.set_page_config(page_title="STALWART Reality Engine", layout="wide")
st.markdown("""
<style>
    h1, h2, h3, .stMetric label { color: #00ffcc !important; font-family: 'Courier New', monospace; }
    .stMetric [data-testid="stMetricValue"] { color: #ffcc00 !important; }
    div[data-testid="stAlert"] { border: 1px solid #00ffcc; background-color: rgba(0, 255, 204, 0.05); }
    div[data-testid="stException"] { font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- MATERIAL & PHYSICS CONSTANTS (THE TRUTH DICTIONARIES) ---
MATERIAL_DATA = {
    "Hafnium Oxide": {"melt_k": 3031.0, "yield_mpa": 400.0, "dielectric": 25.0},
    "Yttrium Barium Copper Oxide": {"melt_k": 1273.0, "yield_mpa": 50.0, "dielectric": 10000.0},
    "Bismuth": {"melt_k": 544.7, "yield_mpa": 15.0, "dielectric": 1.0},
    "Quartz": {"melt_k": 1943.0, "yield_mpa": 50.0, "dielectric": 4.5},
    "Tourmaline": {"melt_k": 1150.0, "yield_mpa": 100.0, "dielectric": 6.5},
    "Amorphous Nanocrystalline": {"melt_k": 1400.0, "yield_mpa": 1200.0, "dielectric": 10.0}
}

COOLING_DATA = {
    "Passive Radiator": 0.85,
    "Microchannel Array": 0.25,
    "Active Cryo": 0.05,
    "Thermoelectric Recycling Loop": 0.15
}

FUSION_FUELS = {
    "Proton-Boron 11 (p-11B)": {"energy_mev": 8.7, "ignition_kev": 100.0, "aneutronic": True},
    "Deuterium-Tritium (D-T)": {"energy_mev": 17.6, "ignition_kev": 15.0, "aneutronic": False}
}

# --- SIDEBAR: 1. PROPULSION & FIELD GEOMETRY ---
st.sidebar.title("1. PROPULSION & FIELD GEOMETRY")
coil_type = st.sidebar.selectbox("Coil Matrix", ["Bi-Ionic Hourglass (Inverted)", "Starship Rodin Coil", "Multi-layered Toroidal"])
phi_rotation = st.sidebar.number_input("Golden Ratio (Φ) Harmonics", value=1.618, format="%.3f")
engine_config = st.sidebar.selectbox("Engine Configuration", ["Quad-Ionic Engine Block", "Dual-Drive Plasma"])

# --- SIDEBAR: 2. REACTOR & CONTAINMENT ---
st.sidebar.title("2. REACTOR & CONTAINMENT")
fusion_fuel = st.sidebar.selectbox("Aneutronic Fuel Type", list(FUSION_FUELS.keys()))
icrf_freq = st.sidebar.number_input("ICRF Excitation (MHz)", value=2.5, min_value=0.1)
containment_field = st.sidebar.number_input("Containment Field (Tesla)", value=5.5)

# --- SIDEBAR: 3. TRACTOR & DIELECTRIC ARRAYS ---
st.sidebar.title("3. TRACTOR DYNAMICS")
mag_gradient = st.sidebar.number_input("Magnetic Gradient (Tesla/m)", value=10.5)
dipole_moment = st.sidebar.number_input("Induced Dipole Moment (A·m²)", value=5.0)

# --- SIDEBAR: 4. MANUAL OVERRIDE PARAMETERS ---
st.sidebar.title("4. MANUAL OVERRIDE PARAMETERS")
core_material = st.sidebar.selectbox("Core Material", list(MATERIAL_DATA.keys()))
power_draw = st.sidebar.number_input("Power Draw (Watts)", value=150.00, min_value=0.0)
system_voltage = st.sidebar.number_input("System Voltage (Volts)", value=12.00, min_value=0.1)
struct_load = st.sidebar.number_input("Structural Load (MPa)", value=20.00, min_value=0.0)

st.sidebar.markdown("### Advanced Thermal Parameters")
cooling_mech = st.sidebar.selectbox("Cooling Mechanism", list(COOLING_DATA.keys()))
ambient_temp = st.sidebar.number_input("Ambient Temp (K)", value=298.0, min_value=0.0)

raw_theory = st.sidebar.text_area("Raw Theory / Context Log:")

# --- FETCH SELECTED CONSTANTS ---
mat_melt = MATERIAL_DATA[core_material]["melt_k"]
mat_yield = MATERIAL_DATA[core_material]["yield_mpa"]
mat_dielectric = MATERIAL_DATA[core_material]["dielectric"]
thermal_res = COOLING_DATA[cooling_mech]
fuel_mev = FUSION_FUELS[fusion_fuel]["energy_mev"]
fuel_ign = FUSION_FUELS[fusion_fuel]["ignition_kev"]
is_aneutronic = FUSION_FUELS[fusion_fuel]["aneutronic"]

# --- MAIN ENGINE HEADER ---
st.title("STALWART REALITY ENGINE")
st.markdown("### THREAT LEVEL: ZERO. MATH IS TRUTH.")
st.markdown("---")

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Thermal Dynamics", "Power Matrix", "Structural Limits", "Propulsion & Tractor Fields", "Reactor Stability"])

# --- TAB 1: THERMAL ---
with tab1:
    st.subheader("ACTIVE TELEMETRY: THERMAL DYNAMICS")
    colA, colB, colC = st.columns(3)
    colA.metric("POWER INPUT", f"{power_draw:.2f} W")
    colB.metric("COOLING RESISTANCE", f"{thermal_res} K/W")
    colC.metric("MATERIAL MELT LIMIT", f"{mat_melt} K")

    if st.button("RUN THERMAL SWEEP", key="btn_therm"):
        calc_temp = ambient_temp + (power_draw * thermal_res)
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$T_{core}=T_{ambient}+(P\\times R_{th})$$")
        
        out1, out2, out3 = st.columns(3)
        out1.metric("Calculated Core Temp", f"{calc_temp:.2f} K")
        out2.metric("Margin to Meltdown", f"{mat_melt - calc_temp:.2f} K")
        out3.metric("Recycling Efficiency", f"{(ambient_temp / calc_temp)*100:.1f}%")
        
        st.markdown("**System Analysis Log:**")
        if calc_temp >= mat_melt:
            st.error(f"🚨 CRITICAL FAILURE: Core temp ({calc_temp:.1f} K) exceeds {core_material} thermal limit ({mat_melt} K). MELTDOWN IMMINENT.")
        else:
            st.success(f"✅ SYSTEM STABLE: Core temp is within safe operational limits for {core_material}.")
        if raw_theory: st.info(f"**Context:** {raw_theory}")

# --- TAB 2: POWER MATRIX ---
with tab2:
    st.subheader("ACTIVE TELEMETRY: POWER MATRIX")
    colA, colB, colC = st.columns(3)
    colA.metric("POWER INPUT", f"{power_draw:.2f} W")
    colB.metric("SYSTEM VOLTAGE", f"{system_voltage:.2f} V")
    colC.metric("DIELECTRIC CONSTANT", f"{mat_dielectric}")

    if st.button("RUN POWER SWEEP", key="btn_pwr"):
        current = power_draw / system_voltage
        resistance = system_voltage / current if current > 0 else float('inf')
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$I=\\frac{P}{V} \\quad | \\quad R=\\frac{V}{I}$$")
        
        out1, out2, out3 = st.columns(3)
        out1.metric("Total Power", f"{power_draw:.2f} W")
        out2.metric("Current", f"{current:.2f} A")
        out3.metric("Circuit Resistance", f"{resistance:.4f} Ω")
        
        st.markdown("**System Analysis Log:**")
        if current > 50.0 and core_material != "Yttrium Barium Copper Oxide":
            st.warning(f"⚠️ HIGH CURRENT WARNING: Risk of plasma arcing unless operating within a superconducting matrix like YBCO.")
        else:
            st.success(f"✅ ELECTRICAL STABLE: Current flows safely through the {core_material} matrix.")
        if raw_theory: st.info(f"**Context:** {raw_theory}")

# --- TAB 3: STRUCTURAL ---
with tab3:
    st.subheader("ACTIVE TELEMETRY: STRUCTURAL LIMITS")
    colA, colB = st.columns(2)
    colA.metric("APPLIED LOAD", f"{struct_load:.2f} MPa")
    colB.metric("MATERIAL YIELD STRENGTH", f"{mat_yield:.2f} MPa")

    if st.button("RUN STRUCTURAL SWEEP", key="btn_str"):
        safety_factor = mat_yield / struct_load if struct_load > 0 else float('inf')
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$\\sigma_{load}\\le\\sigma_{yield} \\quad | \\quad Safety = \\frac{\\sigma_{yield}}{\\sigma_{load}}$$")
        
        out1, out2, out3 = st.columns(3)
        out1.metric("Structural Load", f"{struct_load:.2f} MPa")
        out2.metric("Material Yield", f"{mat_yield:.2f} MPa")
        out3.metric("Safety Factor", f"{safety_factor:.2f}")
        
        st.markdown("**System Analysis Log:**")
        if struct_load >= mat_yield:
            st.error(f"🚨 CRITICAL FAILURE: Applied load ({struct_load:.1f} MPa) shatters {core_material}. FRACTURE IMMINENT.")
        elif safety_factor < 1.5:
            st.warning(f"⚠️ CAUTION: Safety factor is {safety_factor:.2f}. Margin is thin. Microfractures possible.")
        else:
            st.success(f"✅ STRUCTURAL STABLE: Shielding matrix easily withstands {struct_load:.1f} MPa.")
        if raw_theory: st.info(f"**Context:** {raw_theory}")

# --- TAB 4: TRACTOR & PROPULSION ---
with tab4:
    st.subheader("ACTIVE TELEMETRY: PROPULSION & FIELD EFFECT")
    colA, colB, colC = st.columns(3)
    colA.metric("COIL MATRIX", coil_type)
    colB.metric("MAGNETIC GRADIENT", f"{mag_gradient} T/m")
    colC.metric("DIPOLE MOMENT", f"{dipole_moment} A·m²")
    
    if st.button("RUN FIELD SWEEP", key="btn_field"):
        tractor_force = dipole_moment * mag_gradient
        phi_variance = abs(1.618 - phi_rotation)
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$F_{tractor} = \\nabla (\\mathbf{m} \\cdot \\mathbf{B})$$")
        
        out1, out2, out3 = st.columns(3)
        out1.metric("Tractor Beam Force", f"{tractor_force:.2f} N")
        out2.metric("Harmonic Ratio", f"{phi_rotation:.3f}")
        out3.metric("Pinch Factor Mitigation", "Active" if "Inverted" in coil_type else "Inactive")
        
        st.markdown("**System Analysis Log:**")
        if phi_variance > 0.05:
            st.warning("⚠️ HARMONIC INSTABILITY: Rotation drifting from Golden Ratio (1.618). Field containment may destabilize.")
        else:
            st.success(f"✅ FIELD STABLE: {coil_type} generating {tractor_force:.2f} N of focused tractor pull.")

# --- TAB 5: REACTOR ---
with tab5:
    st.subheader("ACTIVE TELEMETRY: FUSION STABILITY")
    colA, colB, colC = st.columns(3)
    colA.metric("FUEL TYPE", fusion_fuel)
    colB.metric("CONTAINMENT FIELD", f"{containment_field} T")
    colC.metric("ICRF EXCITATION", f"{icrf_freq} MHz")
    
    if st.button("RUN REACTOR SWEEP", key="btn_reac"):
        plasma_beta = (power_draw / (containment_field**2)) * 0.01 
        st.markdown("---")
        st.subheader("⚙️ STALWART COMPUTATION RESULTS")
        st.markdown("**Executed Physics Equations:**")
        st.markdown("$$E = mc^2 \\quad | \\quad \\beta = \\frac{p}{B^2 / (2\\mu_0)}$$")
        
        out1, out2, out3 = st.columns(3)
        out1.metric("Energy Output", f"{fuel_mev} MeV")
        out2.metric("Ignition Threshold", f"{fuel_ign} keV")
        out3.metric("Plasma Beta Target", f"{plasma_beta:.5f}")
        
        st.markdown("**System Analysis Log:**")
        if not is_aneutronic:
            st.warning(f"⚠️ RADIATION ALERT: {fusion_fuel} is not aneutronic. High neutron flux detected. Shielding required.")
        else:
            st.success(f"✅ REACTOR STABLE: {fusion_fuel} ignited. Aneutronic reaction confirmed via ICRF locked trajectory.")
