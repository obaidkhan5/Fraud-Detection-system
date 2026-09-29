import streamlit as st
import joblib
import numpy as np
import random
import os
import time

st.set_page_config(
    page_title="SecurePay AI",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
    <style>
    /* Overall Background and Text */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: white !important;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #1e40af !important;
        font-family: 'Inter', sans-serif;
    }

    /* Professional Result Boxes */
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin: 20px 0;
    }
    .fraud-box {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 2px solid #ef4444;
    }
    .safe-box {
        background-color: #dcfce7;
        color: #15803d;
        border: 2px solid #22c55e;
    }

    /* Cards for Layout */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* Button Customization */
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def load_model_file():
    paths = [
        os.path.join(os.path.dirname(__file__), 'securepay_model.pkl'),
        r"D:\Fraud Detection system\trained model .pkl"
    ]
    for path in paths:
        if os.path.exists(path):
            return joblib.load(path)
    return None

model = load_model_file()

if 'captcha' not in st.session_state:
    st.session_state.captcha = str(random.randint(1000, 9999))

with st.sidebar:
    st.title("🛡️ SecurePay AI")
    st.subheader("Admin")
    st.divider()
    
    if model:
        st.success("System: Online")
    else:
        st.error("System: Offline")
    
    if st.button("Regenerate Security Code"):
        st.session_state.captcha = str(random.randint(1000, 9999))
        st.rerun()

st.title("Credit Card Fraud Analysis")
st.write("Enterprise-grade transaction monitoring and risk assessment.")

if model is None:
    st.error("🚨 Model file not found! Please ensure 'securepay_model.pkl' is in the folder.")
else:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="card"><h3>Transaction Details</h3>', unsafe_allow_html=True)
        amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0)
        tr_time = st.number_input("Time (Seconds)", min_value=0.0, value=0.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>Security Check</h3>', unsafe_allow_html=True)
        st.info(f"Security Code: **{st.session_state.captcha}**")
        captcha_input = st.text_input("Enter Code", placeholder="Type code here")
        analyze_btn = st.button("Analyze Transaction")
        st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if captcha_input != st.session_state.captcha:
            st.warning("Verification failed: Incorrect security code.")
        elif amount <= 0:
            st.warning("Please enter a valid amount.")
        else:
            with st.spinner("Processing..."):
                time.sleep(1)
                input_data = np.zeros(30)
                input_data[28] = amount
                input_data[29] = tr_time
                
                prediction = model.predict([input_data])
                is_fraud = True if (prediction[0] == 1 or amount > 15000) else False
                
                if is_fraud:
                    st.markdown('<div class="result-box fraud-box">🚨 FRAUDULENT TRANSACTION DETECTED</div>', unsafe_allow_html=True)
                    st.error(f"High risk detected for transaction of ${amount:,.2f}. The system has blocked this request.")
                else:
                    st.markdown('<div class="result-box safe-box">✅ TRANSACTION IS SECURE</div>', unsafe_allow_html=True)
                    st.success(f"Transaction of ${amount:,.2f} has been approved successfully.")
                
                st.session_state.captcha = str(random.randint(1000, 9999))

st.divider()
st.caption("© 2026 SecurePay Technologies | Secure Data Processing")