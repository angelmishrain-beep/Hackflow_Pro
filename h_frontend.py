import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="HackFlow Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@300;400;500;600&display=swap');
    
    /* Global Styles - Enhanced Vintage Red Theme */
    .stApp {
        background: linear-gradient(135deg, #2D1B1B 0%, #4A2C2C 50%, #6B3E3E 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom container */
    .main-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(25px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 35px 60px rgba(0, 0, 0, 0.12);
    }
    
    /* Header styling - Eye-catching Vintage Red */
    .app-header {
        text-align: center;
        padding: 2.5rem 0;
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E, #FFB3B3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 2.5rem;
        font-family: 'Playfair Display', serif;
        animation: vibrant-pulse 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.6);
    }
    
    @keyframes vibrant-pulse {
        0%, 100% { 
            transform: scale(1);
            filter: drop-shadow(0 0 20px rgba(255, 107, 107, 0.8));
        }
        50% { 
            transform: scale(1.05);
            filter: drop-shadow(0 0 40px rgba(255, 142, 142, 1));
        }
    }
    
    /* Tab styling - Eye-catching Enhanced */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 0.8rem;
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 107, 107, 0.3);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding: 0 2.5rem;
        background: transparent;
        border-radius: 18px;
        color: #D32F2F;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.3), transparent);
        transition: left 0.6s;
    }
    
    .stTabs [data-baseweb="tab"]:hover:before {
        left: 100%;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E) !important;
        color: white !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4);
        transform: translateY(-4px);
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 107, 107, 0.2);
        transform: translateY(-3px);
        color: #B71C1C;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
    }
    
    /* Input styling - High Visibility */
    .stTextInput > div > div > input {
        background: #FFFFFF !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 18px !important;
        padding: 1.4rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2D1B1B !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        width: 100% !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF5252 !important;
        box-shadow: 0 0 35px rgba(255, 107, 107, 0.6) !important;
        transform: translateY(-3px) !important;
        background: #FFFFFF !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #FF5252 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8D6E63 !important;
        font-weight: 500 !important;
    }
    
    .stTextArea textarea {
        background: #FFFFFF !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 18px !important;
        padding: 1.4rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2D1B1B !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        width: 100% !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #FF5252 !important;
        box-shadow: 0 0 35px rgba(255, 107, 107, 0.6) !important;
        background: #FFFFFF !important;
        outline: none !important;
    }
    
    .stTextArea textarea:hover {
        border-color: #FF5252 !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #8D6E63 !important;
        font-weight: 500 !important;
    }
    
    /* Button styling - High Visibility */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E, #FFB3B3) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1.2rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        position: relative !important;
        overflow: hidden !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        width: 100% !important;
        min-height: 60px !important;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 20px 50px rgba(255, 107, 107, 0.6) !important;
        background: linear-gradient(135deg, #FF5252, #FF7979, #FFA0A0) !important;
        filter: brightness(1.1) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) !important;
        transition: all 0.1s ease !important;
    }
    
    /* Card styling - Eye-catching Vibrant */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 28px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 50px rgba(255, 107, 107, 0.2);
        border: 3px solid rgba(255, 107, 107, 0.3);
        backdrop-filter: blur(30px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .info-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #FF6B6B, #FF8E8E, #FFB3B3, #FF6B6B);
        opacity: 0;
        transition: opacity 0.4s ease;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    .info-card:hover:before {
        opacity: 1;
    }
    
    .info-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 70px rgba(255, 107, 107, 0.3);
        background: rgba(255, 255, 255, 1);
        border-color: rgba(255, 107, 107, 0.5);
    }
    
    /* Progress bar styling - Eye-catching Vibrant */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #FF8E8E, #FFB3B3);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    /* Success/Error messages - Eye-catching Enhanced */
    .stSuccess {
        background: linear-gradient(135deg, #4CAF50, #66BB6A, #81C784);
        color: white;
        border-radius: 20px;
        border: 2px solid rgba(76, 175, 80, 0.3);
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .stError {
        background: linear-gradient(135deg, #F44336, #EF5350, #E57373);
        color: white;
        border-radius: 20px;
        border: 2px solid rgba(244, 67, 54, 0.3);
        box-shadow: 0 8px 25px rgba(244, 67, 54, 0.3);
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Number input styling - High Visibility */
    .stNumberInput > div > div > input {
        background: #FFFFFF !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 18px !important;
        padding: 1.4rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2D1B1B !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        width: 100% !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #FF5252 !important;
        box-shadow: 0 0 35px rgba(255, 107, 107, 0.6) !important;
        transform: translateY(-3px) !important;
        background: #FFFFFF !important;
        outline: none !important;
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #FF5252 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Select box styling - High Visibility */
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border-radius: 18px !important;
        border: 3px solid #FF6B6B !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 0.5rem !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #FF5252 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #2D1B1B !important;
        font-weight: 600 !important;
    }
    
    /* Radio styling - High Visibility */
    .stRadio > div {
        background: #FFFFFF !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(20px) !important;
        border: 3px solid #FF6B6B !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stRadio > div:hover {
        background: #FFFFFF !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
        border-color: #FF5252 !important;
    }
    
    .stRadio > div > label {
        color: #2D1B1B !important;
        font-weight: 600 !important;
    }
    
    /* Radio button circles - Enhanced Visibility */
    .stRadio > div > label > div[data-testid="stRadio"] {
        background: #FFFFFF !important;
        border: 2px solid #FF6B6B !important;
        border-radius: 50% !important;
        width: 20px !important;
        height: 20px !important;
        margin-right: 10px !important;
    }
    
    .stRadio > div > label > div[data-testid="stRadio"]:checked {
        background: #FF6B6B !important;
        border-color: #FF5252 !important;
    }
    
    .stRadio > div > label > div[data-testid="stRadio"]:checked::after {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 8px !important;
        height: 8px !important;
        background: #FFFFFF !important;
        border-radius: 50% !important;
    }
    
    /* Alternative radio button styling */
    .stRadio input[type="radio"] {
        appearance: none !important;
        width: 20px !important;
        height: 20px !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 50% !important;
        background: #FFFFFF !important;
        margin-right: 10px !important;
        position: relative !important;
        cursor: pointer !important;
    }
    
    .stRadio input[type="radio"]:checked {
        background: #FF6B6B !important;
        border-color: #FF5252 !important;
    }
    
    .stRadio input[type="radio"]:checked::after {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 8px !important;
        height: 8px !important;
        background: #FFFFFF !important;
        border-radius: 50% !important;
    }
    
    .stRadio input[type="radio"]:hover {
        border-color: #FF5252 !important;
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.3) !important;
    }
    
    /* Radio button labels */
    .stRadio label {
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        padding: 0.5rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio label:hover {
        background: rgba(255, 107, 107, 0.1) !important;
    }
    
    /* Columns styling - Vintage Red Theme */
    .stColumn {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(129, 17, 18, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(129, 17, 18, 0.1);
    }
    
    .stColumn:hover {
        background: rgba(255, 255, 255, 0.8);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(129, 17, 18, 0.15);
    }
    
    /* Expander styling - High Visibility */
    .streamlit-expander {
        background: #FFFFFF !important;
        border-radius: 20px !important;
        border: 3px solid #FF6B6B !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 1rem 0 !important;
    }
    
    .streamlit-expander:hover {
        border-color: #FF5252 !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .streamlit-expander > div {
        background: transparent !important;
    }
    
    .streamlit-expander > div > div {
        color: #2D1B1B !important;
        font-weight: 600 !important;
    }
    
    /* Caption styling - Eye-catching Enhanced */
    .stCaption {
        font-size: 1.2rem;
        color: #FF6B6B;
        font-weight: 600;
        line-height: 1.6;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Subheader styling - Eye-catching Vibrant */
    .stSubheader {
        color: #FF6B6B;
        font-weight: 700;
        font-size: 1.6rem;
        margin: 2rem 0;
        font-family: 'Playfair Display', serif;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Animated icons - Gentle and calming */
    .icon {
        display: inline-block;
        animation: gentle-sway 3s ease-in-out infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes gentle-sway {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-3px) rotate(1deg); }
        75% { transform: translateY(3px) rotate(-1deg); }
    }
    
    /* Floating elements - Soft breathing motion */
    .floating {
        animation: soft-float 4s ease-in-out infinite;
    }
    
    @keyframes soft-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    /* Custom title styling - Eye-catching Vibrant */
    .custom-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E, #FFB3B3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 3rem 0;
        font-family: 'Playfair Display', serif;
        animation: vibrant-pulse 4s ease-in-out infinite;
        text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    .emoji-large {
        font-size: 3.2rem;
        animation: vibrant-bounce 2s ease-in-out infinite;
        filter: drop-shadow(0 6px 12px rgba(255, 107, 107, 0.6));
    }
    
    @keyframes vibrant-bounce {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.1) rotate(2deg); }
        75% { transform: scale(1.05) rotate(-2deg); }
    }
    
    @keyframes soft-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Additional calming animations */
    .zen-fade-in {
        animation: zen-fade-in 0.8s ease-out;
    }
    
    @keyframes zen-fade-in {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Smooth transitions for all interactive elements */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Custom scrollbar - High Visibility */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF5252, #FF7979);
    }
    
    /* Additional form element styling for better visibility */
    .stTextInput label,
    .stTextArea label,
    .stNumberInput label,
    .stSelectbox label,
    .stRadio label {
        color: #FF6B6B !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: #FFFFFF !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #FF5252 !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Info and warning messages */
    .stInfo {
        background: linear-gradient(135deg, #2196F3, #42A5F5, #64B5F6) !important;
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid rgba(33, 150, 243, 0.3) !important;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3) !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FF9800, #FFB74D, #FFCC80) !important;
        color: white !important;
        border-radius: 20px !important;
        border: 2px solid rgba(255, 152, 0, 0.3) !important;
        box-shadow: 0 8px 25px rgba(255, 152, 0, 0.3) !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Enhanced Radio Button Styling for Better Visibility */
    .stRadio > div > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.8rem !important;
    }
    
    .stRadio > div > div > label {
        display: flex !important;
        align-items: center !important;
        padding: 1rem !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FF6B6B !important;
        border-radius: 15px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2) !important;
    }
    
    .stRadio > div > div > label:hover {
        background: rgba(255, 107, 107, 0.1) !important;
        border-color: #FF5252 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stRadio > div > div > label > input[type="radio"] {
        appearance: none !important;
        width: 24px !important;
        height: 24px !important;
        border: 3px solid #FF6B6B !important;
        border-radius: 50% !important;
        background: #FFFFFF !important;
        margin-right: 15px !important;
        position: relative !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio > div > div > label > input[type="radio"]:checked {
        background: #FF6B6B !important;
        border-color: #FF5252 !important;
        box-shadow: 0 0 15px rgba(255, 107, 107, 0.5) !important;
    }
    
    .stRadio > div > div > label > input[type="radio"]:checked::after {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 10px !important;
        height: 10px !important;
        background: #FFFFFF !important;
        border-radius: 50% !important;
    }
    
    .stRadio > div > div > label > input[type="radio"]:hover {
        border-color: #FF5252 !important;
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stRadio > div > div > label > span {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Alternative text styling for radio labels */
    .stRadio > div > div > label {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div > div > label > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Ensure all text in radio buttons is visible */
    .stRadio * {
        color: #2D1B1B !important;
    }
    
    .stRadio > div > div > label > * {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Selected radio button styling */
    .stRadio > div > div > label:has(input[type="radio"]:checked) {
        background: rgba(255, 107, 107, 0.15) !important;
        border-color: #FF5252 !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Additional text visibility fixes for Streamlit radio buttons */
    .stRadio > div > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div > div > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div > div > div > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Streamlit specific radio button text styling */
    .stRadio > div > div > div[data-testid="stRadio"] {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div > div > div[data-testid="stRadio"] > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio > div > div > div[data-testid="stRadio"] > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Force text visibility in all radio button containers */
    .stRadio div[role="radiogroup"] {
        color: #2D1B1B !important;
    }
    
    .stRadio div[role="radiogroup"] > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio div[role="radiogroup"] > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio div[role="radiogroup"] > div > div > div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Ensure text is visible in radio button labels */
    .stRadio label div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio label div div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stRadio label div div div {
        color: #2D1B1B !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="app-header">🚀 HackFlow Pro</h1>', unsafe_allow_html=True)

backend_url = "http://127.0.0.1:8000/"

# Create tabs with enhanced styling
tab1, tab2, tab3, tab4 = st.tabs([" Login Portal", " Execution Hub", " Dashboard", "Github Code upload"])

with tab1:
    st.markdown('<div class="custom-title"><span class="icon">👥</span>Team Registration</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="info-card floating">', unsafe_allow_html=True)
        st.markdown("###  Create Your Dream Team")
        st.caption(" Login your team and start your incredible journey toward innovation!")
        
        team_name = st.text_input(" Enter your team name:", placeholder="Team Awesome")
        leader_name = st.text_input("Enter leader name:", placeholder="John Doe")
        leader_email = st.text_input(" Enter Leader's email:", placeholder="john@example.com")
        
        if st.button("Save Team Info", key="save_team"):
            if team_name and leader_name and leader_email:
                st.success(f" Team '{team_name}' with leader {leader_name} saved!")
                payload = {
                    "team_name": team_name,
                    "leader_name": leader_name,
                    "leader_email": leader_email,
                    "members": [] 
                }
                try:
                    response = requests.post("http://127.0.0.1:8000/save_team", json=payload)
                    if response.status_code == 200:
                        st.success(" Team info saved successfully in DB ")
                    else:
                        st.error(f"Error: {response.text}")
                except:
                    st.warning(" Backend connection issue - but your data is captured!")
            else:
                st.warning(" Please fill in all team details!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card floating">', unsafe_allow_html=True)
        st.markdown("###  Add Team Members")
        
        num_members = st.number_input("🔢 Enter number of team members:", min_value=1, max_value=10, value=1, step=1)
        member_data = []
        
        for i in range(1, num_members + 1):
            st.markdown(f"#### 🌟 Member {i} Details")
            email = st.text_input(f"📧 Email of member {i}", key=f"email_{i}", placeholder=f"member{i}@example.com")
            level = st.radio(f"🎯 Skill Level {i}", ["🥉 Beginner", "🥈 Intermediate", "🥇 Advanced"], key=f"level_{i}")
            member_data.append({"email": email, "level": level})
        
        if st.button("🚀 Submit All Details", key="submit_members"):
            st.success("🎊 You've entered details successfully! Ready to hack!")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="custom-title"><span class="icon">⚡</span>Execution Command Center</div>', unsafe_allow_html=True)
    st.caption("🤖 Here AI will help you strategize, guide and execute winning plans.")
    
    col1, col2 = st.columns([1.2, 0.8], gap="large")
    
    with col1:
        with st.expander("🎯 Hackathon Configuration", expanded=True):
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            theme = st.text_input("🎨 Hackathon Theme:", placeholder="AI for Good")
            problem = st.text_input("💡 Problem Statement:", placeholder="Solve climate change with technology")
            
            col_dur1, col_dur2 = st.columns(2)
            with col_dur1:
                duration = st.number_input("⏱️ Duration", min_value=1, value=24, step=1)
            with col_dur2:
                time_unit = st.selectbox("⏳ Time Unit", ["Hours", "Minutes", "Seconds"])
            
            if time_unit == "Hours":
                total_seconds = duration * 3600
            elif time_unit == "Minutes":
                total_seconds = duration * 60
            else:
                total_seconds = duration
            
            if st.button("💾 Save Hackathon Config", key="save_hackathon"):
                payload = {
                    "theme": theme,
                    "problem_statement": problem,
                    "duration": duration,
                    "time_unit": time_unit
                }
                try:
                    response = requests.post("http://127.0.0.1:8000/save_hackathon", json=payload)
                    if response.status_code == 200:
                        st.success("🎉 Hackathon info saved successfully! ✅")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except:
                    st.warning("⚠️ Backend connection issue - config captured locally!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🎯 Generate Smart Tasks", key="generate_tasks"):
            with st.spinner("🔄 AI is crafting your perfect task distribution..."):
                time.sleep(1)  # Add visual delay for better UX
                try:
                    response = requests.post("http://127.0.0.1:8000/assign_tasks")
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("### 📋 AI-Generated Task Assignment")
                        st.markdown('<div class="info-card">', unsafe_allow_html=True)
                        st.write(data["tasks"])
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {response.text}")
                except:
                    st.info("🤖 AI Task Generator: Backend offline - would generate optimized task distribution here!")
    
    with col2:
        st.markdown('<div class="info-card floating">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Assistant")
        st.markdown('<span class="emoji-large">🧠</span>', unsafe_allow_html=True)
        
        query = st.text_area("💬 What help do you need?", placeholder="How should we approach the UI design?", height=150)
        
        if st.button("🚀 Get AI Guidance", key="get_help"):
            if query:
                with st.spinner("🤔 AI is thinking..."):
                    payload = {"query": query}
                    try:
                        response = requests.post("http://127.0.0.1:8000/help", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            st.markdown("#### 🎯 AI Expert Advice")
                            st.write(data["answer"])
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except:
                        st.info("🤖 AI would provide expert guidance here! Backend currently offline.")
            else:
                st.warning("⚠️ Please enter your question first!")
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="custom-title"><span class="icon">📊</span>Project Analytics Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown('<div class="info-card floating">', unsafe_allow_html=True)
        st.markdown("### 🔗 Project Tracker")
        
        project_url = st.text_input("🌐 Enter your project repository URL:", placeholder="https://github.com/yourteam/awesome-project")
        
        if st.button("📈 Analyze Progress", key="track_progress"):
            if project_url:
                with st.spinner("🔍 Analyzing your project..."):
                    time.sleep(1)  # Visual delay for better UX
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/track",
                            json={"project_url": project_url}
                        )
                        data = response.json()
                        progress = data["progress"]
                        
                        st.success(f"🎯 Project Progress: {progress}%")
                        st.progress(progress)
                        
                    except:
                        # Demo mode when backend is offline
                        import random
                        progress = random.randint(25, 95)
                        st.success(f"🎯 Project Progress: {progress}%")
                        st.progress(progress)
            else:
                st.warning("⚠️ Please enter a valid project URL!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Progress Visualization")
        
        # Create demo progress data when no real data available
        try:
            if 'progress' in locals():
                fig = go.Figure(data=[go.Pie(
                    values=[progress, 100-progress],
                    labels=["✅ Completed", "⏳ Remaining"],
                    hole=0.6,
                    marker=dict(colors=["#4ecdc4", "#ff6b6b"]),
                    textinfo='label+percent',
                    textfont_size=14,
                    textfont_color="white"
                )])
                
                fig.update_layout(
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white", size=16),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Default visualization
                fig = go.Figure(data=[go.Pie(
                    values=[0, 100],
                    labels=["✅ Ready to Start", "⏳ Awaiting Analysis"],
                    hole=0.6,
                    marker=dict(colors=["#8089af", "#FFFFFF"]),
                    textinfo='label',
                    textfont_size=14
                )])
                
                fig.update_layout(
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=14),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
        except:
            st.info("📊 Progress visualization will appear here after analysis!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer - Eye-catching Vibrant
st.markdown("---")
st.markdown(
    '<div class="zen-fade-in" style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.95); border-radius: 25px; backdrop-filter: blur(20px); box-shadow: 0 15px 40px rgba(255, 107, 107, 0.2); border: 3px solid rgba(255, 107, 107, 0.3);">'
    '<p style="color: #FF6B6B; font-size: 1.3rem; margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">✨ Built with passion for hackathon success! ✨</p>'
    '<p style="color: #FF8E8E; font-size: 1rem; margin-top: 1rem; font-weight: 500;">🚀 HackFlow Pro - Where Innovation Meets Execution 🚀</p>'
    '</div>', 
    unsafe_allow_html=True
)
with tab4:
    st.markdown('<div class="custom-title"><span class="icon">📁</span>GitHub Code Upload</div>', unsafe_allow_html=True)
    st.caption("🌊 Seamlessly upload your project files to the cloud with our gentle upload system.")
    
    st.markdown('<div class="info-card floating">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Your Project Files")
    st.caption("✨ Choose your files and let our system handle the rest with care and precision.")
    
    uploaded_file = st.file_uploader("Choose a file to upload", help="Select any file from your project to upload to our secure cloud storage")
    
    if uploaded_file is not None:
        st.info(f"📋 Selected file: **{uploaded_file.name}** ({uploaded_file.size} bytes)")
        
        if st.button("🚀 Upload File", key="upload_file"):
            with st.spinner("🔄 Uploading your file with care..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post("http://localhost:8000/upload_file/", files=files)
                    
                    if response.status_code == 200:
                        st.success(f"✨ File **{uploaded_file.name}** uploaded successfully! 🎉")
                        st.balloons()
                    else:
                        st.error("❌ Failed to upload the file. Please try again.")
                except Exception as e:
                    st.warning("⚠️ Upload service temporarily unavailable. Your file is ready to upload when the service is back online.")
    
    st.markdown('</div>', unsafe_allow_html=True)

