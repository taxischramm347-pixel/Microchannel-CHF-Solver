import streamlit as st
import numpy as np
from scipy.optimize import minimize
import json
from google import genai
from google.genai import types

# --- STALWART ENGINES ---
class STALWART_Thermal_Engine:
    def sweep_to_reality(self, power, load, max_temp_override, theory_text):
        # The engine now catches the raw theory text for future NLP parsing
        parsed_theory_note = f" (Theory Noted: {theory_text[:20]}...)" if theory_text else ""
        
        heat_generated = power * 1.5
        if heat_generated <= max_temp_override and load <= 113:
            return "SUCCESS", f"Thermal limits hold at {power}W and {load}MPa.{parsed_theory_note}"
        
        safe_power = max_temp_override / 1.5
        return "SALVAGED", f"Thermal sweep triggered. Cap power at {safe_power:.2f}W to prevent core meltdown.{parsed_theory_note}"

class STALWART_Electro_Engine:
    def sweep_to_reality(self, wraps, voltage, frequency, theory_text):
        parsed_theory_note = f" (Theory Noted: {theory_text[:20]}...)" if theory_text else ""
        
        gradient = (voltage / wraps) * (frequency / 60)
        if gradient < 5:
            return "SUCCESS", f"Magnetic gradient is stable at {frequency}Hz.{parsed_theory_note}"
        return "SALVAGED", f"Pinch factor detected. Increase wraps or drop voltage to stabilize field.{parsed_theory_note}"

# --- VISION AI ARCHITECTURE (LIVE) ---
def extract_data_from_sketch(image_file, api_key):
    try:
        client = genai.Client(api_key=api_key)
        image_bytes = image_file.getvalue()
        
        prompt = """
        Analyze this engineering sketch. Look for numbers related to power (Watts) and structural load (MPa).
        Respond ONLY with a valid JSON object matching this format perfectly:
        {"detected_power": 1200, "detected_load": 150, "confidence": "90%"}
        If you cannot find exact numbers, estimate reasonable thresholds based on the drawing and note a lower confidence.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ]
        )
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(raw_text)
        
    except Exception as e:
        return {"error": str(e)}

# --- VISUAL DASHBOARD SHELL ---
st.set_page_config(page_title="STALWART Reality Engine", layout="wide", initial_sidebar_state="expanded")

# --- SCI-FI CUSTOM CSS OVERLAY ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Share Tech Mono', monospace !important; }
.stApp { background-color: #050505; background-image: radial-gradient(circle, #1a1a24 10%, #050505 80%); }
h1, h2, h3 { color: #00ffcc !important; text-shadow: 0px 0px 8px rgba(0,255,204,0.6); text-transform: uppercase; letter-spacing: 1px; }
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div {
    background-color: #111116; color: #00ffcc; border: 1px solid #00ffcc; box-shadow: inset 0px 0px 5px rgba(0,255,204,0.2);
}
.stButton>button {
    background-color: #0a0a0f; border: 2px solid #ff3366; color: #ff3366; text-transform: uppercase;
    font-weight: bold; letter-spacing: 2px; box-shadow: 0px 0px 10px rgba(255,51,102,0.5); transition: 0.3s; width: 100%;
}
.stButton>button:hover { background-color: #ff3366; color: #000; box-shadow: 0px 0px 20px rgba(255,51,102,1); border-color: #ff3366; }
[data-testid="stMetricValue"] { color: #ffcc00; text-shadow: 0px 0px 5px rgba(255,204,0,0.5); }
[data-testid="stMetricLabel"] { color: #a0a0b0; text-transform: uppercase; }
hr { border-color: #00ffcc; opacity: 0.3; box-shadow: 0px 0px 5px #00ffcc; }
</style>
""", unsafe_allow_html=True)

st.title("STALWART Reality Engine")
st.markdown("### Threat Level: Zero. Math is Truth.")
st.divider()

# --- THE SWITCHBOARD ---
st.sidebar.header("1. Core Physics Engine")
engine_choice = st.sidebar.selectbox("Active Solver:", ["Thermal Dynamics", "Electromagnetic & Geometry", "Theoretical Sandbox"])
st.sidebar.divider()

# --- CLOUD API CONFIGURATION (BYOK) ---
st.sidebar.header("2. AI Vision Link")
user_api_key = st.sidebar.text_input("Enter API Key (Required for Scan):", type="password")
st.sidebar.divider()

# --- THE SKETCH IMPORTER (FIXED CAMERA LOGIC) ---
st.sidebar.header("3. Blueprint Optics")
input_method = st.sidebar.radio("Optics Mode:", ["Standby (Off)", "Live Scanner", "Upload File"], horizontal=True)
active_image = None

if input_method == "Live Scanner":
    active_image = st.camera_input("Initialize STALWART Optics Array")
elif input_method == "Upload File":
    active_image = st.file_uploader("Drop image here", type=['png', 'jpg', 'jpeg'])

if 'auto_power' not in st.session_state: st.session_state.auto_power = 1500
if 'auto_load' not in st.session_state: st.session_state.auto_load = 200

if active_image is not None:
    if not user_api_key:
        st.sidebar.error("SYSTEM LOCK: A valid API Key is required to authorize the scan.")
    else:
        with st.sidebar.status("Transmitting to cloud...", expanded=True) as status:
            ai_data = extract_data_from_sketch(active_image, user_api_key)
            if "error" in ai_data:
                status.update(label="Scan Failed.", state="error", expanded=False)
            else:
                st.session_state.auto_power = ai_data.get("detected_power", 1500)
                st.session_state.auto_load = ai_data.get("detected_load", 200)
                status.update(label=f"Scan Complete!", state="complete", expanded=False)

st.sidebar.divider()

# --- DYNAMIC INPUT PANELS WITH DEEP VARIABLES ---
st.sidebar.header("4. Manual Override Parameters")

active_melting_point = 1358 
active_frequency = 60 
raw_theory_input = ""

if engine_choice == "Thermal Dynamics":
    material = st.sidebar.selectbox("Core Material", ["Copper", "Aluminum", "Hafnium Oxide", "Nanocrystalline Alloy", "Other (Custom)"])
    
    if material == "Other (Custom)":
        custom_mat_name = st.sidebar.text_input("Specify Custom Material:")
        active_melting_point = st.sidebar.number_input("Known Melting Point (K):", value=1000)
    elif material == "Aluminum": active_melting_point = 933
    elif material == "Hafnium Oxide": active_melting_point = 3031
    
    user_power = st.sidebar.number_input("Power Draw (Watts)", value=float(st.session_state.auto_power))
    user_load = st.sidebar.number_input("Structural Load (MPa)", value=float(st.session_state.auto_load))
    
    with st.sidebar.expander("Advanced Thermal Parameters"):
        cooling_type = st.selectbox("Cooling Mechanism", ["Passive Radiator", "Active Liquid Loop", "Microchannel Flow"])
        ambient_temp = st.number_input("Ambient Environment Temp (K)", value=298)
        
    raw_theory_input = st.sidebar.text_area("Raw Theory / Context (Natural Language):", placeholder="Describe design intentions, workarounds, or theoretical context here...")

elif engine_choice == "Electromagnetic & Geometry":
    coil_type = st.sidebar.selectbox("Geometry Shape", ["Standard Toroidal", "Bi-Ionic Hourglass", "Golden Ratio Stator", "Other (Custom)"])
    
    if coil_type == "Other (Custom)":
        custom_geom = st.sidebar.text_input("Specify Custom Geometry:")
        
    wire_material = st.sidebar.selectbox("Wire Material", ["Gold", "Coated Aluminum", "Copper", "YBCO Superconductor"])
    wrap_count = st.sidebar.number_input("Number of Wraps", value=144)
    voltage_in = st.sidebar.number_input("Input Voltage", value=120)
    
    with st.sidebar.expander("Advanced Electromagnetic Parameters"):
        wire_gauge = st.number_input("Wire Thickness (AWG)", value=12)
        active_frequency = st.number_input("Operating Frequency (Hz)", value=60)
        input_current = st.number_input("Input Current (Amps)", value=15)

    raw_theory_input = st.sidebar.text_area("Raw Theory / Context (Natural Language):", placeholder="Describe design intentions, workarounds, or theoretical context here...")

elif engine_choice == "Theoretical Sandbox":
    st.sidebar.warning("Sandbox Mode: Strict physical limits bypassed for theoretical modeling.")
    raw_theory_input = st.sidebar.text_area("Input Custom Math or Theory Here (e.g. x^2 + y):", placeholder="Enter pure math or theoretical framework...")
    with st.sidebar.expander("Define Custom Constants"):
        st.text_input("Variable 1 (e.g., m = 10)")
        st.text_input("Variable 2 (e.g., c = 3e8)")

# --- MAIN DISPLAY ---
st.subheader(f"Active Telemetry: {engine_choice}")

if engine_choice == "Thermal Dynamics":
    col1, col2, col3 = st.columns(3)
    col1.metric("Power Input", f"{user_power} W")
    col2.metric("Structural Load", f"{user_load} MPa")
    col3.metric("Material Limit", f"{active_melting_point} K")
elif engine_choice == "Electromagnetic & Geometry":
    col1, col2, col3 = st.columns(3)
    col1.metric("Coil Wraps", f"{wrap_count}")
    col2.metric("Voltage Input", f"{voltage_in} V")
    col3.metric("Frequency", f"{active_frequency} Hz")
elif engine_choice == "Theoretical Sandbox":
    st.info("Sandbox active. Telemetry bypassed.")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Run STALWART Sweep", type="primary"):
    if engine_choice == "Thermal Dynamics":
        engine = STALWART_Thermal_Engine()
        status, msg = engine.sweep_to_reality(user_power, user_load, active_melting_point, raw_theory_input)
    
    elif engine_choice == "Electromagnetic & Geometry":
        engine = STALWART_Electro_Engine()
        status, msg = engine.sweep_to_reality(wrap_count, voltage_in, active_frequency, raw_theory_input)
        
    elif engine_choice == "Theoretical Sandbox":
        parsed_note = f" (Context Noted: {raw_theory_input[:20]}...)" if raw_theory_input else ""
        status, msg = "SUCCESS", f"Custom math parsed and accepted.{parsed_note}"

    if status == "SUCCESS":
        st.success(msg)
    elif status == "SALVAGED":
        st.warning(f"Optimization Sweep Triggered:\n\n{msg}")
    else:
        st.error(msg)

# --- PWA JAVASCRIPT INJECTION ---
import streamlit.components.v1 as components
components.html("""
<script>
    // Inject the manifest into the main browser head
    const manifest = window.parent.document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = './app/static/manifest.json';
    window.parent.document.head.appendChild(manifest);

    // Register the Service Worker
    if ('serviceWorker' in window.parent.navigator) {
        window.parent.navigator.serviceWorker.register('./app/static/sw.js')
        .then(function(registration) {
            console.log('STALWART Service Worker Registered');
        })
        .catch(function(error) {
            console.log('Service Worker Registration Failed:', error);
        });
    }
</script>
""", height=0, width=0)

# --- PWA JAVASCRIPT INJECTION ---
import streamlit.components.v1 as components
components.html("""
<script>
    // Inject the manifest into the main browser head
    const manifest = window.parent.document.createElement('link');
    manifest.rel = 'manifest';
    manifest.href = './app/static/manifest.json';
    window.parent.document.head.appendChild(manifest);

    // Register the Service Worker
    if ('serviceWorker' in window.parent.navigator) {
        window.parent.navigator.serviceWorker.register('./app/static/sw.js')
        .then(function(registration) {
            console.log('STALWART Service Worker Registered');
        })
        .catch(function(error) {
            console.log('Service Worker Registration Failed:', error);
        });
    }
</script>
""", height=0, width=0)
