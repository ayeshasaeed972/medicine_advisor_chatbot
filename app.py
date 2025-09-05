import streamlit as st
from datetime import datetime, timedelta
import random
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import requests
from geopy.geocoders import Nominatim
import geocoder
import pyttsx3
import speech_recognition as sr
import threading

# Clean Minimalist CSS with improved styling
st.markdown("""
<style>
    .main {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Arial', sans-serif;
    }
    
    .stButton>button {
        border-radius: 25px;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .stSuccess {
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .stInfo {
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #4facfe;
        padding: 12px;
        background: rgba(255, 255, 255, 0.9);
        color: #333;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 15px;
        border: 2px solid #4facfe;
        padding: 12px;
        background: rgba(255, 255, 255, 0.9);
        color: #333;
    }
    
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .emergency-contact {
        color: #ff6b6b;
        font-weight: bold;
        font-size: 16px;
        margin: 8px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .health-tip {
        background: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        margin: 25px 0;
        border: none;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: white;
        margin-top: 40px;
        opacity: 0.8;
    }
    
    .consultation-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .remedy-box {
        background: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        font-size: 16px;
    }
    
    .reminder-box {
        background: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        color: white;
    }
    
    .chat-message {
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
    }
    
    .user-message {
        background: rgba(79, 172, 254, 0.3);
        margin-left: 20%;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .doctor-message {
        background: rgba(102, 126, 234, 0.3);
        margin-right: 20%;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .white-text {
        color: white !important;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .medicine-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .symptom-tracker {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .dashboard-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        text-align: center;
    }
    
    .progress-bar {
        height: 10px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 5px;
    }
    
    .family-member {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .health-journal {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .mood-selector {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
    }
    
    .mood-option {
        text-align: center;
        cursor: pointer;
        padding: 10px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .mood-option:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .mood-option.selected {
        background: rgba(79, 172, 254, 0.3);
        transform: scale(1.1);
    }
    
    .profile-header {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .health-metric {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .emergency-guide {
        background: rgba(255, 100, 100, 0.2);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid rgba(255, 100, 100, 0.5);
    }
    
    .voice-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'history' not in st.session_state:
    st.session_state.history = []
if 'symptom_history' not in st.session_state:
    st.session_state.symptom_history = []
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"
if 'medicine_inventory' not in st.session_state:
    st.session_state.medicine_inventory = []
if 'symptom_logs' not in st.session_state:
    st.session_state.symptom_logs = []
if 'health_goals' not in st.session_state:
    st.session_state.health_goals = [
        {"goal": "Drink 8 glasses of water daily", "progress": 75, "target": 100},
        {"goal": "30 minutes of exercise", "progress": 60, "target": 100},
        {"goal": "7 hours of sleep", "progress": 85, "target": 100}
    ]
if 'family_members' not in st.session_state:
    st.session_state.family_members = [
        {"name": "Ali", "relation": "Son", "age": 12, "gender": "Male", "blood_type": "O+", 
         "allergies": "None", "conditions": "None", "medications": "None", "last_checkup": "2023-10-15"},
        {"name": "Fatima", "relation": "Daughter", "age": 8, "gender": "Female", "blood_type": "A+", 
         "allergies": "Dust", "conditions": "None", "medications": "None", "last_checkup": "2023-09-20"}
    ]
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []
if 'current_family_member' not in st.session_state:
    st.session_state.current_family_member = None
if 'family_health_data' not in st.session_state:
    st.session_state.family_health_data = {}
if 'voice_input' not in st.session_state:
    st.session_state.voice_input = ""
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False

# All health tips list
all_health_tips = [
    "💧 Drink 8-10 glasses of water daily for proper hydration",
    "🏃‍♂️ Exercise for 30 minutes daily to boost metabolism and mood", 
    "😴 Get 7-8 hours of quality sleep every night for better immunity",
    "🍎 Eat 5 servings of fruits and vegetables daily for vitamins",
    "🧘‍♀️ Practice 10-minute meditation daily to reduce stress by 40%"
]

# Doctor data
doctors = [
    {"name": "Dr. Ayesha Saeed", "specialty": "General Physician", "rating": 4.8, "fee": 1500, "experience": "10 years"},
    {"name": "Dr. Saeed", "specialty": "Ayurvedic Specialist", "rating": 4.9, "fee": 2000, "experience": "15 years"},
    {"name": "Dr. Haleema Saeed", "specialty": "Herbal Medicine", "rating": 4.7, "fee": 1200, "experience": "8 years"},
    {"name": "Dr. Shehryar Saeed", "specialty": "Homeopathy", "rating": 4.6, "fee": 1000, "experience": "12 years"}
]

# Clinic locations
clinics = [
    {"name": "Main City Clinic", "address": "123 Main Street, Karachi", "hours": "9AM-9PM", "phone": "021-1234567"},
    {"name": "Downtown Health Center", "address": "456 Downtown Ave, Lahore", "hours": "8AM-8PM", "phone": "042-7654321"},
    {"name": "Green Herbal Center", "address": "789 Garden Road, Islamabad", "hours": "10AM-6PM", "phone": "051-5551234"}
]

# Emergency guide data
emergency_guides = {
    "Heart Attack": {
        "steps": [
            "Call emergency services immediately",
            "Help the person sit down and rest",
            "Loosen tight clothing",
            "If prescribed, help them take their nitroglycerin",
            "Give aspirin if not allergic",
            "Perform CPR if trained and if person is unresponsive"
        ],
        "donot": [
            "Leave the person alone",
            "Allow the person to deny symptoms",
            "Wait to see if symptoms go away",
            "Give anything other than aspirin unless directed by medical professionals"
        ]
    },
    "Choking": {
        "steps": [
            "Ask 'Are you choking?'",
            "Perform 5 back blows between shoulder blades",
            "Perform 5 abdominal thrusts (Heimlich maneuver)",
            "Alternate between back blows and abdominal thrusts",
            "Call emergency services if object isn't dislodged"
        ],
        "donot": [
            "Perform abdominal thrusts on infants under 1 year",
            "Reach blindly into the mouth",
            "Slap on the back if person is coughing effectively"
        ]
    },
    "Burns": {
        "steps": [
            "Cool the burn under cool running water for 10-15 minutes",
            "Remove tight items before the area swells",
            "Cover the burn with sterile non-stick dressing",
            "Take pain relief if needed",
            "Seek medical attention for serious burns"
        ],
        "donot": [
            "Use ice or iced water",
            "Apply creams, ointments or fats",
            "Break blisters",
            "Remove clothing stuck to the burn"
        ]
    },
    "Stroke": {
        "steps": [
            "Call emergency services immediately",
            "Note the time when symptoms started",
            "Keep the person comfortable and supported",
            "If unconscious, place in recovery position",
            "Be prepared to perform CPR if breathing stops"
        ],
        "donot": [
            "Give food or drink",
            "Let the person drive themselves to hospital",
            "Wait to see if symptoms improve"
        ]
    }
}

# Medicine inventory data
if not st.session_state.medicine_inventory:
    st.session_state.medicine_inventory = [
        {"name": "Turmeric", "quantity": "100g", "expiry": "2024-12-01", "uses": "Anti-inflammatory, Antioxidant"},
        {"name": "Ginger", "quantity": "250g", "expiry": "2024-10-15", "uses": "Digestion, Nausea, Cold"},
        {"name": "Honey", "quantity": "500g", "expiry": "2025-05-20", "uses": "Cough, Sore throat, Energy"},
        {"name": "Peppermint Oil", "quantity": "30ml", "expiry": "2024-08-30", "uses": "Headache, Digestion"}
    ]

# Enhanced remedy function with AI-like suggestions
def get_remedy(symptoms):
    symptoms = symptoms.lower()
    remedies = {
        'head': {"remedy": "Headache: Apply peppermint oil to temples and forehead", "confidence": 85},
        'cold': {"remedy": "Common Cold: Drink ginger tea with honey, lemon, and turmeric", "confidence": 90},
        'fever': {"remedy": "Fever: Basil tea with honey and black pepper", "confidence": 80},
        'cough': {"remedy": "Cough: Turmeric milk with honey and ginger", "confidence": 88},
        'stomach': {"remedy": "Indigestion: Peppermint tea with fennel seeds after meals", "confidence": 82},
        'throat': {"remedy": "Sore Throat: Salt water gargle 3 times + honey lemon tea", "confidence": 87},
        'stress': {"remedy": "Stress: Chamomile tea + deep breathing exercises", "confidence": 84},
        'sleep': {"remedy": "Insomnia: Warm milk with turmeric + 1 tsp ghee", "confidence": 79},
        'skin': {"remedy": "Skin Issues: Aloe vera gel application + neem water", "confidence": 86},
        'allergy': {"remedy": "Allergy: Steam inhalation + turmeric honey water", "confidence": 83}
    }
    
    for key, data in remedies.items():
        if key in symptoms:
            return data
    
    return {"remedy": "Please consult a doctor for proper diagnosis and treatment", "confidence": 0}

# Function to simulate doctor response
def get_doctor_response(message):
    time.sleep(1)  # Simulate response time
    responses = [
        "I understand your concern. Let me suggest a natural remedy for that.",
        "Based on your symptoms, I recommend trying this traditional treatment.",
        "Many patients find relief with this approach. Give it a try.",
        "This remedy has been used for generations with good results."
    ]
    remedy_data = get_remedy(message)
    return random.choice(responses) + " " + remedy_data["remedy"]

# Function to get age-specific health tips
def get_age_specific_tips(age):
    if age < 1:
        return ["Breastfeeding is best for babies", "Regular vaccination is important", "Ensure proper sleep schedule"]
    elif age < 5:
        return ["Provide balanced nutrition", "Encourage physical activity", "Limit screen time"]
    elif age < 12:
        return ["Ensure calcium for growing bones", "Encourage outdoor play", "Establish healthy eating habits"]
    elif age < 18:
        return ["Focus on protein-rich diet", "Encourage sports participation", "Monitor mental health"]
    elif age < 40:
        return ["Regular exercise is crucial", "Maintain healthy weight", "Annual health checkups"]
    elif age < 60:
        return ["Monitor blood pressure regularly", "Heart-healthy diet", "Regular health screenings"]
    else:
        return ["Gentle exercises like walking", "Calcium and Vitamin D supplements", "Regular doctor visits"]

# Function to generate health report
def generate_health_report():
    report = f"HEALTH REPORT - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += "=== SYMPTOM HISTORY ===\n"
    for i, entry in enumerate(st.session_state.symptom_history[-10:]):
        report += f"{i+1}. {entry['timestamp']}: {entry['symptoms']}\n"
        if 'remedy' in entry:
            report += f"   Remedy: {entry['remedy']}\n"
        report += "\n"
    
    report += "=== MEDICINE INVENTORY ===\n"
    for med in st.session_state.medicine_inventory:
        report += f"- {med['name']} ({med['quantity']}) - Expires: {med['expiry']}\n"
    
    report += "\n=== FAMILY HEALTH SUMMARY ===\n"
    for member in st.session_state.family_members:
        report += f"- {member['name']} ({member['relation']}, {member['age']} years)\n"
    
    return report

# Function for voice input
def listen_to_voice():
    st.session_state.is_listening = True
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        with microphone as source:
            st.info("Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        text = recognizer.recognize_google(audio)
        st.session_state.voice_input = text
        st.success(f"Recognized: {text}")
    except sr.WaitTimeoutError:
        st.error("No speech detected within timeout")
    except sr.UnknownValueError:
        st.error("Could not understand the audio")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        st.session_state.is_listening = False

# Function for text-to-speech
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")

# Function to find nearby hospitals
def find_nearby_hospitals(location="Karachi"):
    # This is a simulation - in a real app, you would use Google Places API or similar
    hospitals = {
        "Karachi": [
            {"name": "Aga Khan University Hospital", "distance": "2.5 km", "phone": "021-111-911-911"},
            {"name": "Civil Hospital Karachi", "distance": "3.2 km", "phone": "021-99215700"},
            {"name": "Jinnah Postgraduate Medical Centre", "distance": "4.1 km", "phone": "021-99215700"}
        ],
        "Lahore": [
            {"name": "Shaukat Khanum Memorial Hospital", "distance": "1.8 km", "phone": "042-111-911-911"},
            {"name": "Services Hospital Lahore", "distance": "2.3 km", "phone": "042-99211111"},
            {"name": "Mayo Hospital Lahore", "distance": "3.5 km", "phone": "042-99211111"}
        ],
        "Islamabad": [
            {"name": "Pakistan Institute of Medical Sciences", "distance": "2.1 km", "phone": "051-9261170"},
            {"name": "Shifa International Hospital", "distance": "3.7 km", "phone": "051-8464646"},
            {"name": "Ali Medical Centre", "distance": "4.2 km", "phone": "051-8444444"}
        ]
    }
    
    return hospitals.get(location, hospitals["Karachi"])

# Navigation tabs - Updated with new features
tabs = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Health Dashboard", "💬 Live Chat", "🩺 Doctors", 
                                      "🗺️ Clinics", "📋 Health Reminder", "📜 History", "💊 Medicine Tracker", 
                                      "📊 Symptom Analysis", "👨‍👩‍👧‍👦 Family Health", "📓 Health Journal",
                                      "🚑 Emergency Guide", "📄 Health Reports", "🎤 Voice Assistant"])

if tabs == "🏠 Home":
    st.session_state.active_tab = "Home"
elif tabs == "📊 Health Dashboard":
    st.session_state.active_tab = "Health Dashboard"
elif tabs == "💬 Live Chat":
    st.session_state.active_tab = "Live Chat"
elif tabs == "🩺 Doctors":
    st.session_state.active_tab = "Doctors"
elif tabs == "🗺️ Clinics":
    st.session_state.active_tab = "Clinics"
elif tabs == "📋 Health Reminder":
    st.session_state.active_tab = "Health Reminder"
elif tabs == "📜 History":
    st.session_state.active_tab = "History"
elif tabs == "💊 Medicine Tracker":
    st.session_state.active_tab = "Medicine Tracker"
elif tabs == "📊 Symptom Analysis":
    st.session_state.active_tab = "Symptom Analysis"
elif tabs == "👨‍👩‍👧‍👦 Family Health":
    st.session_state.active_tab = "Family Health"
elif tabs == "📓 Health Journal":
    st.session_state.active_tab = "Health Journal"
elif tabs == "🚑 Emergency Guide":
    st.session_state.active_tab = "Emergency Guide"
elif tabs == "📄 Health Reports":
    st.session_state.active_tab = "Health Reports"
elif tabs == "🎤 Voice Assistant":
    st.session_state.active_tab = "Voice Assistant"

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("### 🚀 Quick Select")
    common_symptoms = st.selectbox(
        "Choose common symptoms:",
        ["Select", "Headache", "Cold", "Fever", "Cough", "Stomach Pain", 
         "Sore Throat", "Stress", "Insomnia", "Skin Issues", "Allergy"]
    )
    
    st.markdown("---")
    
    st.markdown("### 💡 Health Tips")
    # Show random tip by default
    if 'current_tip' not in st.session_state:
        st.session_state.current_tip = random.choice(all_health_tips)
    
    st.markdown(f"<div class='health-tip'>{st.session_state.current_tip}</div>", unsafe_allow_html=True)
    
    # Button to show all tips
    if st.button("📋 Show All Tips"):
        st.session_state.show_all_tips = not st.session_state.get('show_all_tips', False)
    
    if st.session_state.get('show_all_tips'):
        st.markdown("---")
        st.markdown("### 📝 All Health Tips")
        for i, tip in enumerate(all_health_tips, 1):
            st.write(f"{i}. {tip}")
    
    st.markdown("---")
    
    # ================== DOCTOR CONSULTATION ==================
    st.markdown("### 🩺 Book Doctor Consultation")
    
    with st.form("consultation_form"):
        st.write("**Fill the form to book appointment:**")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        symptoms = st.text_area("Describe Symptoms")
        preferred_date = st.date_input("Preferred Date")
        preferred_time = st.time_input("Preferred Time")
        
        submitted = st.form_submit_button("📅 Book Appointment Now")
        
        if submitted:
            if name and phone and symptoms:
                st.success("✅ Appointment Request Sent!")
                st.info(f"""
                **Appointment Details:**
                👤 Name: {name}
                📞 Phone: {phone}
                📅 Date: {preferred_date}
                ⏰ Time: {preferred_time}
                🏥 Doctor will contact you within 24 hours
                """)
                
                # Add to consultation history
                consultation = {
                    "name": name,
                    "phone": phone,
                    "symptoms": symptoms,
                    "date": str(preferred_date),
                    "time": str(preferred_time),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.symptom_history.append(consultation)
            else:
                st.error("⚠️ Please fill all fields")
    
    st.markdown("---")
    
    st.markdown("### 📞 Emergency Contacts")
    st.markdown("<p class='emergency-contact'>🚑 Ambulance: 102</p>", unsafe_allow_html=True)
    st.markdown("<p class='emergency-contact'>🆘 Emergency: 112</p>", unsafe_allow_html=True)
    st.markdown("<p class='emergency-contact'>👨‍⚕️ Doctor: 9876543210</p>", unsafe_allow_html=True)
    st.markdown("<p class='emergency-contact'>👮 Police: 100</p>", unsafe_allow_html=True)

# ================== MAIN CONTENT AREA ==================
if st.session_state.active_tab == "Home":
    st.markdown("# 🌿 Traditional Medicine Advisor")
    st.markdown("### Discover natural remedies for your health concerns")

    # Add a beautiful divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Input Section
    st.markdown("### 🤒 Describe Your Symptoms")

    # Use quick select from sidebar
    if common_symptoms != "Select":
        symptoms = common_symptoms
    else:
        symptoms = ""

    symptoms_input = st.text_input("Type your symptoms:", symptoms, 
                                  placeholder="e.g., headache, fever, cough...")

    if st.button("🔍 Find Natural Remedy", type="primary"):
        if symptoms_input:
            remedy_data = get_remedy(symptoms_input)
            st.session_state.current_remedy = remedy_data["remedy"]
            st.session_state.remedy_confidence = remedy_data["confidence"]
            st.session_state.show_results = True
            st.session_state.symptoms_input = symptoms_input
            
            # Add to symptom history
            st.session_state.symptom_history.append({
                "symptoms": symptoms_input,
                "remedy": remedy_data["remedy"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # Add to symptom logs for analysis
            st.session_state.symptom_logs.append({
                "symptom": symptoms_input,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "severity": "Moderate"  # Default value
            })
        else:
            st.error("⚠️ Please describe your symptoms first!")

    # Show Results
    if st.session_state.get('show_results') and st.session_state.get('symptoms_input'):
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.success("💊 **Remedy Found!**")
        
        remedy = st.session_state.current_remedy
        symptoms_input = st.session_state.symptoms_input
        confidence = st.session_state.remedy_confidence
        
        # Use the new remedy box with dark background
        st.markdown(f"<div class='remedy-box'><strong>{remedy}</strong></div>", unsafe_allow_html=True)
        
        # Show confidence level
        if confidence > 0:
            st.write(f"**Confidence Level:** {confidence}%")
        
        # Dosage Information
        st.markdown("**💊 Dosage:**")
        dosage_info = {
            'peppermint': "Apply 2-3 times daily for 5 days",
            'ginger': "Drink 3 times daily after meals for 1 week",
            'basil': "Drink 2 times daily (morning-evening) for 5 days",
            'turmeric': "Once daily at bedtime for 1 week",
            'chamomile': "2-3 times when feeling stressed",
            'salt water': "Gargle 3-4 times daily for 3 days"
        }
        
        for key, dosage in dosage_info.items():
            if key in remedy.lower():
                st.write(f"• {dosage}")
        
        # Preparation Steps
        st.markdown("**👩‍🍳 Preparation:**")
        if 'ginger tea' in remedy.lower():
            st.write("• Boil water with ginger slices")
            st.write("• Add honey and lemon")
            st.write("• Drink warm")
        elif 'basil tea' in remedy.lower():
            st.write("• Steep basil leaves in hot water")
            st.write("• Add honey")
            st.write("• Drink warm")
        else:
            st.write("• Follow standard preparation methods")
        
        # Medicine Cost in Pakistani Rupees
        st.markdown("**💰 Estimated Cost (Pakistani Rupees):**")
        cost_data = {
            'peppermint oil': "Rs. 150-200 (15ml)",
            'ginger': "Rs. 50-80 per kg", 
            'turmeric': "Rs. 80-120 per kg",
            'honey': "Rs. 200-500 per kg",
            'tulsi leaves': "Rs. 30-50 per bunch",
            'chamomile': "Rs. 100-150 per pack"
        }
        
        for item, cost in cost_data.items():
            if item in remedy.lower():
                st.write(f"• {item.title()}: {cost}")
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Remedy"):
                with open("remedy_history.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {symptoms_input} → {remedy}\n")
                st.success("Saved to file!")
        with col2:
            report_text = f"""MEDICINE ADVISOR REPORT
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    Symptoms: {symptoms_input}
    Remedy: {remedy}
    """
            st.download_button("📄 Export Report", report_text, "remedy_report.txt")
        with col3:
            if st.button("📅 Add Reminder"):
                # Pre-fill reminder form with remedy info
                st.session_state.reminder_prefill = f"Take {remedy.split(':')[0]} remedy"
                st.session_state.active_tab = "Health Reminder"
                st.rerun()
        
        # Add to history
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "symptoms": symptoms_input,
            "remedy": remedy
        })

    # Recent History
    if st.session_state.history:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### 📜 Recent History")
        for i, item in enumerate(reversed(st.session_state.history[-3:]), 1):
            st.write(f"{i}. **{item['symptoms']}** → {item['remedy']} (*{item['timestamp']}*)")

    # Quick Actions
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Health Tips")
        
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💧 Hydration"):
            st.info("Drink 8-10 glasses of water daily")
    with col2:
        if st.button("🏃 Fitness"):
            st.info("30 mins daily exercise")
    with col3:
        if st.button("😴 Sleep"):
            st.info("7-8 hours quality sleep")

    # WhatsApp Integration
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📱 WhatsApp Consultation")
    st.write("Click below to start a WhatsApp chat with our health advisor:")
    st.markdown("[💬 Start WhatsApp Chat](https://wa.me/1234567890?text=Hi%20I%20need%20health%20advice)")

elif st.session_state.active_tab == "Health Dashboard":
    st.markdown("# 📊 Health Dashboard")
    st.markdown("### Your personal health overview")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Health Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='dashboard-card'>" +
                   "<h3>🩺 Symptoms This Week</h3>" +
                   "<h2>3</h2>" +
                   "<p>2 less than last week</p>" +
                   "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='dashboard-card'>" +
                   "<h3>💊 Remedies Used</h3>" +
                   "<h2>7</h2>" +
                   "<p>Most used: Turmeric</p>" +
                   "</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='dashboard-card'>" +
                   "<h3>📅 Consultations</h3>" +
                   "<h2>2</h2>" +
                   "<p>Last: 3 days ago</p>" +
                   "</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Health Goals
    st.markdown("### 🎯 Health Goals")
    for goal in st.session_state.health_goals:
        st.write(f"**{goal['goal']}**")
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {goal['progress']}%"></div>
        </div>
        <p>{goal['progress']}% completed</p>
        """, unsafe_allow_html=True)
    
    # Add new goal
    with st.form("goal_form"):
        st.write("**Add New Goal:**")
        new_goal = st.text_input("Goal Description")
        goal_target = st.slider("Target (%)", 0, 100, 100)
        submitted = st.form_submit_button("➕ Add Goal")
        
        if submitted and new_goal:
            st.session_state.health_goals.append({
                "goal": new_goal,
                "progress": 0,
                "target": goal_target
            })
            st.success("Goal added successfully!")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Weekly Health Chart
    st.markdown("### 📈 Weekly Health Trend")
    
    # Sample data for chart
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    wellness_scores = [7, 8, 6, 9, 8, 9, 10]  # Out of 10
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, wellness_scores, marker='o', linewidth=2, markersize=8)
    ax.set_ylim(0, 10)
    ax.set_ylabel('Wellness Score')
    ax.set_title('Weekly Wellness Trend')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

elif st.session_state.active_tab == "Live Chat":
    st.markdown("# 💬 Live Chat with Doctor")
    st.markdown("### Real-time consultation with our health experts")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["sender"] == "user":
                st.markdown(f"<div class='chat-message user-message'><strong>You:</strong> {msg['message']}</div>", 
                           unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message doctor-message'><strong>Doctor:</strong> {msg['message']}</div>", 
                           unsafe_allow_html=True)
    
    # Chat input
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    chat_input = st.text_input("Type your message here...", key="chat_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send", key="send_chat"):
            if chat_input:
                # Add user message
                st.session_state.chat_messages.append({"sender": "user", "message": chat_input})
                
                # Get doctor response
                doctor_response = get_doctor_response(chat_input)
                
                # Add doctor message
                st.session_state.chat_messages.append({"sender": "doctor", "message": doctor_response})
                
                # Rerun to update chat
                st.rerun()
    with col2:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

elif st.session_state.active_tab == "Doctors":
    st.markdown("# 🩺 Our Doctors")
    st.markdown("### Consult with our certified traditional medicine experts")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    for i, doctor in enumerate(doctors):
        with st.expander(f"👨‍⚕️ {doctor['name']} - {doctor['specialty']}"):
            st.write(f"**Rating:** {doctor['rating']} ⭐")
            st.write(f"**Experience:** {doctor['experience']}")
            st.write(f"**Consultation Fee:** Rs. {doctor['fee']}")
            st.write("**Availability:** Monday to Saturday, 10AM-6PM")
            
            if st.button("Book Appointment", key=f"doc_{i}"):
                st.success(f"Appointment request sent to {doctor['name']}!")
                
    # Consultation Packages
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 💰 Consultation Packages")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='consultation-card'>" +
                   "<h3>Basic</h3>" +
                   "<h2>Rs. 1000</h2>" +
                   "<p>• 15 mins consultation</p>" +
                   "<p>• General advice</p>" +
                   "<p>• Basic remedy suggestion</p>" +
                   "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='consultation-card'>" +
                   "<h3>Standard</h3>" +
                   "<h2>Rs. 2000</h2>" +
                   "<p>• 30 mins consultation</p>" +
                   "<p>• Detailed analysis</p>" +
                   "<p>• Personalized treatment</p>" +
                   "</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='consultation-card'>" +
                   "<h3>Premium</h3>" +
                   "<h2>Rs. 3500</h2>" +
                   "<p>• 60 mins consultation</p>" +
                   "<p>• Follow-up sessions</p>" +
                   "<p>• Complete health plan</p>" +
                   "</div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "Clinics":
    st.markdown("# 🗺️ Clinic Locations")
    st.markdown("### Find our traditional medicine clinics near you")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    for clinic in clinics:
        st.markdown(f"### 🏥 {clinic['name']}")
        st.write(f"**Address:** {clinic['address']}")
        st.write(f"**Hours:** {clinic['hours']}")
        st.write(f"**Phone:** {clinic['phone']}")
        st.write("**Services:** Traditional consultation, herbal medicines, acupuncture")
        st.button("Get Directions", key=clinic['name'])
        st.markdown("---")
    
    # Map placeholder
    st.markdown("### 📍 Interactive Map")
    st.write("*Map integration would show here with clinic locations*")
    st.image("https://via.placeholder.com/600x300/667eea/ffffff?text=Clinic+Locations+Map", use_column_width=True)

elif st.session_state.active_tab == "Health Reminder":
    st.markdown("# 📋 Health Reminder")
    st.markdown("### Set reminders for your medications and health routines")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Add new reminder
    with st.form("reminder_form"):
        st.write("**Add New Reminder:**")
        reminder_text = st.text_input("Reminder Title", value=st.session_state.get('reminder_prefill', ''))
        reminder_time = st.time_input("Reminder Time")
        reminder_date = st.date_input("Reminder Date", datetime.now())
        repeat = st.selectbox("Repeat", ["Never", "Daily", "Weekly", "Monthly"])
        
        submitted = st.form_submit_button("➕ Add Reminder")
        
        if submitted:
            if reminder_text:
                new_reminder = {
                    "text": reminder_text,
                    "time": str(reminder_time),
                    "date": str(reminder_date),
                    "repeat": repeat,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.reminders.append(new_reminder)
                st.success("Reminder added successfully!")
                # Clear the prefill after use
                if 'reminder_prefill' in st.session_state:
                    del st.session_state.reminder_prefill
            else:
                st.error("Please enter reminder text")
    
    # Display reminders
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 🔔 Your Reminders")
    
    if st.session_state.reminders:
        for i, reminder in enumerate(st.session_state.reminders):
            st.markdown(f"<div class='reminder-box'>" +
                       f"<h4>{reminder['text']}</h4>" +
                       f"<p>⏰ {reminder['time']} on {reminder['date']}</p>" +
                       f"<p>🔁 Repeat: {reminder['repeat']}</p>" +
                       f"</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.reminders.pop(i)
                    st.rerun()
    else:
        st.info("No reminders set. Add one above!")

elif st.session_state.active_tab == "History":
    st.markdown("# 📜 Your Health History")
    st.markdown("### Review your symptom and consultation history")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Symptom History
    st.markdown("### 🤒 Symptom History")
    if st.session_state.symptom_history:
        for i, entry in enumerate(reversed(st.session_state.symptom_history)):
            with st.expander(f"{entry['timestamp']} - {entry['symptoms'][:30]}..."):
                st.write(f"**Symptoms:** {entry['symptoms']}")
                if 'remedy' in entry:
                    st.write(f"**Remedy:** {entry['remedy']}")
                if 'name' in entry:
                    st.write(f"**Consultation for:** {entry['name']}")
                    st.write(f"**Phone:** {entry['phone']}")
    else:
        st.info("No symptom history yet. Start by describing your symptoms on the Home tab.")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Consultation History
    st.markdown("### 🩺 Consultation History")
    consultation_history = [item for item in st.session_state.symptom_history if 'name' in item]
    if consultation_history:
        for i, consultation in enumerate(reversed(consultation_history)):
            st.write(f"**{consultation['timestamp']}** - {consultation['name']}")
            st.write(f"Symptoms: {consultation['symptoms'][:50]}...")
            st.markdown("---")
    else:
        st.info("No consultation history yet. Book a consultation using the sidebar form.")

elif st.session_state.active_tab == "Medicine Tracker":
    st.markdown("# 💊 Medicine Tracker")
    st.markdown("### Manage your herbal medicine inventory")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Add new medicine
    with st.form("medicine_form"):
        st.write("**Add New Medicine:**")
        col1, col2 = st.columns(2)
        with col1:
            med_name = st.text_input("Medicine Name")
            med_quantity = st.text_input("Quantity")
        with col2:
            med_expiry = st.date_input("Expiry Date", datetime.now() + timedelta(days=180))
            med_uses = st.text_input("Common Uses")
        
        submitted = st.form_submit_button("➕ Add Medicine")
        
        if submitted:
            if med_name and med_quantity:
                new_medicine = {
                    "name": med_name,
                    "quantity": med_quantity,
                    "expiry": str(med_expiry),
                    "uses": med_uses,
                    "added": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.medicine_inventory.append(new_medicine)
                st.success("Medicine added to inventory!")
            else:
                st.error("Please enter medicine name and quantity")
    
    # Display medicine inventory
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📦 Medicine Inventory")
    
    if st.session_state.medicine_inventory:
        for i, medicine in enumerate(st.session_state.medicine_inventory):
            st.markdown(f"<div class='medicine-card'>" +
                       f"<h4>{medicine['name']} ({medicine['quantity']})</h4>" +
                       f"<p>📅 Expiry: {medicine['expiry']}</p>" +
                       f"<p>💊 Uses: {medicine['uses']}</p>" +
                       f"</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("Delete", key=f"med_{i}"):
                    st.session_state.medicine_inventory.pop(i)
                    st.rerun()
    else:
        st.info("No medicines in inventory. Add one above!")
        
    # Medicine usage statistics
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Medicine Usage Stats")
    
    if st.session_state.symptom_history:
        # Count remedies used
        remedy_counts = {}
        for entry in st.session_state.symptom_history:
            if 'remedy' in entry:
                remedy = entry['remedy'].split(':')[0]
                remedy_counts[remedy] = remedy_counts.get(remedy, 0) + 1
        
        if remedy_counts:
            df = pd.DataFrame({
                'Remedy': list(remedy_counts.keys()),
                'Count': list(remedy_counts.values())
            })
            
            # Matplotlib bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df['Remedy'], df['Count'])
            ax.set_title('Most Used Remedies')
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No remedy usage data yet.")
    else:
        st.info("No medicine usage data yet. Start by getting some remedies on the Home tab.")

elif st.session_state.active_tab == "Symptom Analysis":
    st.markdown("# 📊 Symptom Analysis")
    st.markdown("### Track and analyze your health patterns")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Log new symptom
    with st.form("symptom_form"):
        st.write("**Log New Symptom:**")
        col1, col2 = st.columns(2)
        with col1:
            symptom_name = st.text_input("Symptom")
            symptom_date = st.date_input("Date", datetime.now())
        with col2:
            symptom_time = st.time_input("Time", datetime.now())
            symptom_severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
        
        submitted = st.form_submit_button("➕ Log Symptom")
        
        if submitted:
            if symptom_name:
                new_symptom = {
                    "symptom": symptom_name,
                    "date": str(symptom_date),
                    "time": str(symptom_time),
                    "severity": symptom_severity
                }
                st.session_state.symptom_logs.append(new_symptom)
                st.success("Symptom logged successfully!")
            else:
                st.error("Please enter a symptom")
    
    # Display symptom logs
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📝 Symptom Logs")
    
    if st.session_state.symptom_logs:
        for i, log in enumerate(reversed(st.session_state.symptom_logs[-10:])):
            st.markdown(f"<div class='symptom-tracker'>" +
                       f"<h4>{log['symptom']} ({log['severity']})</h4>" +
                       f"<p>📅 {log['date']} at {log['time']}</p>" +
                       f"</div>", unsafe_allow_html=True)
    else:
        st.info("No symptoms logged yet. Add one above!")
    
    # Symptom analysis
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📈 Symptom Frequency")
    
    if st.session_state.symptom_logs:
        # Count symptoms
        symptom_counts = {}
        for log in st.session_state.symptom_logs:
            symptom = log['symptom']
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        
        if symptom_counts:
            df = pd.DataFrame({
                'Symptom': list(symptom_counts.keys()),
                'Count': list(symptom_counts.values())
            })
            
            # Matplotlib pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(df['Count'], labels=df['Symptom'], autopct='%1.1f%%')
            ax.set_title('Symptom Frequency')
            st.pyplot(fig)
            
            # Show most common symptom
            most_common = max(symptom_counts, key=symptom_counts.get)
            st.info(f"Your most frequent symptom is **{most_common}** ({symptom_counts[most_common]} times)")
        else:
            st.info("No symptom data to analyze yet.")
    else:
        st.info("No symptom data to analyze yet. Log some symptoms above!")

elif st.session_state.active_tab == "Family Health":
    st.markdown("# 👨‍👩‍👧‍👦 Family Health")
    st.markdown("### Manage your family's health in one place")
    
    # Check if we're viewing a specific family member's profile
    if st.session_state.current_family_member:
        member = st.session_state.current_family_member
        st.markdown(f"<div class='profile-header'><h2>{member['name']}'s Health Profile</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📋 Basic Information")
            st.markdown(f"<div class='health-metric'><strong>Name:</strong> {member['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Relation:</strong> {member['relation']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Age:</strong> {member['age']} years</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Gender:</strong> {member['gender']}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🩺 Medical Information")
            st.markdown(f"<div class='health-metric'><strong>Blood Type:</strong> {member['blood_type']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Allergies:</strong> {member['allergies']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Medical Conditions:</strong> {member['conditions']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='health-metric'><strong>Last Checkup:</strong> {member['last_checkup']}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Age-specific health tips
        st.markdown("### 💡 Age-Specific Health Tips")
        age_tips = get_age_specific_tips(member['age'])
        for tip in age_tips:
            st.markdown(f"<div class='health-tip'>{tip}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Health metrics tracking
        st.markdown("### 📊 Health Metrics")
        
        if member['name'] not in st.session_state.family_health_data:
            st.session_state.family_health_data[member['name']] = {
                'height': 0,
                'weight': 0,
                'blood_pressure': '120/80',
                'last_updated': datetime.now().strftime("%Y-%m-%d")
            }
        
        with st.form(f"health_metrics_{member['name']}"):
            st.write("**Update Health Metrics:**")
            col1, col2 = st.columns(2)
            with col1:
                height = st.number_input("Height (cm)", value=st.session_state.family_health_data[member['name']]['height'])
                weight = st.number_input("Weight (kg)", value=st.session_state.family_health_data[member['name']]['weight'])
            with col2:
                blood_pressure = st.text_input("Blood Pressure", value=st.session_state.family_health_data[member['name']]['blood_pressure'])
            
            submitted = st.form_submit_button("💾 Update Metrics")
            if submitted:
                st.session_state.family_health_data[member['name']] = {
                    'height': height,
                    'weight': weight,
                    'blood_pressure': blood_pressure,
                    'last_updated': datetime.now().strftime("%Y-%m-%d")
                }
                st.success("Health metrics updated!")
        
        # Show BMI if height and weight are available
        if (st.session_state.family_health_data[member['name']]['height'] > 0 and 
            st.session_state.family_health_data[member['name']]['weight'] > 0):
            height_m = st.session_state.family_health_data[member['name']]['height'] / 100
            bmi = st.session_state.family_health_data[member['name']]['weight'] / (height_m * height_m)
            st.info(f"**BMI:** {bmi:.1f} - {'Underweight' if bmi < 18.5 else 'Normal weight' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese'}")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        if st.button("← Back to Family Members"):
            st.session_state.current_family_member = None
            st.rerun()
    
    else:
        # Main Family Health page
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Family Members List
        st.markdown("### 👪 Family Members")
        for i, member in enumerate(st.session_state.family_members):
            st.markdown(f"<div class='family-member'>" +
                       f"<h4>{member['name']} ({member['relation']})</h4>" +
                       f"<p>Age: {member['age']} years • {member['gender']}</p>" +
                       f"</div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("View Profile", key=f"view_{i}"):
                    st.session_state.current_family_member = member
                    st.rerun()
            with col2:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.editing_member_index = i
                    st.session_state.current_family_member = member
                    st.rerun()
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.family_members.pop(i)
                    st.rerun()
        
        # Add new family member
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### ➕ Add Family Member")
        
        with st.form("family_form"):
            col1, col2 = st.columns(2)
            with col1:
                member_name = st.text_input("Name")
                member_relation = st.selectbox("Relation", ["Child", "Spouse", "Parent", "Sibling", "Grandparent", "Other"])
                member_age = st.number_input("Age", min_value=0, max_value=120, value=30)
                member_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            with col2:
                blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
                allergies = st.text_input("Allergies", "None")
                conditions = st.text_input("Medical Conditions", "None")
                last_checkup = st.date_input("Last Checkup", datetime.now())
            
            submitted = st.form_submit_button("➕ Add Member")
            
            if submitted and member_name:
                new_member = {
                    "name": member_name,
                    "relation": member_relation,
                    "age": member_age,
                    "gender": member_gender,
                    "blood_type": blood_type,
                    "allergies": allergies,
                    "conditions": conditions,
                    "last_checkup": last_checkup.strftime("%Y-%m-%d")
                }
                st.session_state.family_members.append(new_member)
                st.success(f"{member_name} added to family!")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Family Health Summary
        st.markdown("### 📊 Family Health Summary")
        
        if st.session_state.family_members:
            # Fixed the error: Make sure arrays have the same length
            member_names = [m['name'] for m in st.session_state.family_members]
            wellness_scores = [8] * len(member_names)  # Sample scores, same length as member_names
            
            # Create a DataFrame with the data
            family_data = {
                'Member': member_names,
                'Wellness Score': wellness_scores
            }
            
            df = pd.DataFrame(family_data)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df['Member'], df['Wellness Score'])
            ax.set_ylim(0, 10)
            ax.set_ylabel('Wellness Score (out of 10)')
            ax.set_title('Family Wellness Comparison')
            st.pyplot(fig)
        else:
            st.info("Add family members to see health summary")

elif st.session_state.active_tab == "Health Journal":
    st.markdown("# 📓 Health Journal")
    st.markdown("### Track your daily health and mood")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # New Journal Entry
    with st.form("journal_form"):
        st.write("**New Journal Entry:**")
        
        # Mood selection
        st.write("**How are you feeling today?**")
        moods = ["😢", "😐", "😊", "😁", "😍"]
        mood_labels = ["Very Sad", "Neutral", "Happy", "Very Happy", "Excellent"]
        
        cols = st.columns(5)
        selected_mood = st.session_state.get('selected_mood', 2)
        
        for i, (mood, label) in enumerate(zip(moods, mood_labels)):
            with cols[i]:
               if st.form_submit_button(f"{mood}\n{label}", key=f"mood_{i}"):
                    selected_mood = i
                    st.session_state.selected_mood = i
        
        # Journal content
        journal_date = st.date_input("Date", datetime.now())
        journal_text = st.text_area("Journal Entry", placeholder="How was your day? Any symptoms? How did remedies work?")
        
        submitted = st.form_submit_button("💾 Save Entry")
        
        if submitted and journal_text:
            new_entry = {
                "date": str(journal_date),
                "mood": selected_mood,
                "mood_label": mood_labels[selected_mood],
                "text": journal_text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.journal_entries.append(new_entry)
            st.success("Journal entry saved!")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Journal History
    st.markdown("### 📖 Journal History")
    
    if st.session_state.journal_entries:
        for entry in reversed(st.session_state.journal_entries):
            st.markdown(f"<div class='health-journal'>" +
                       f"<h4>{entry['date']} - {entry['mood_label']} {moods[entry['mood']]}</h4>" +
                       f"<p>{entry['text']}</p>" +
                       f"<small>{entry['timestamp']}</small>" +
                       f"</div>", unsafe_allow_html=True)
    else:
        st.info("No journal entries yet. Add your first entry above!")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Mood Trend Chart
    st.markdown("### 📈 Mood Trend")
    
    if st.session_state.journal_entries:
        # Prepare data for chart
        dates = []
        mood_scores = []
        
        for entry in st.session_state.journal_entries[-7:]:  # Last 7 entries
            dates.append(entry['date'])
            mood_scores.append(entry['mood'])
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, mood_scores, marker='o', linewidth=2, markersize=8)
        ax.set_ylim(0, 4)
        ax.set_yticks([0, 1, 2, 3, 4])
        ax.set_yticklabels(["Very Sad", "Neutral", "Happy", "Very Happy", "Excellent"])
        ax.set_title('Mood Trend Over Time')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Add journal entries to see mood trends")

elif st.session_state.active_tab == "Emergency Guide":
    st.markdown("# 🚑 Emergency Medical Guide")
    st.markdown("### First aid instructions for common emergency situations")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Emergency situation selector
    emergency_type = st.selectbox("Select Emergency Situation", list(emergency_guides.keys()))
    
    if emergency_type:
        guide = emergency_guides[emergency_type]
        
        st.markdown(f"<div class='emergency-guide'><h2>🚨 {emergency_type} - First Aid Guide</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ What to Do")
            for i, step in enumerate(guide['steps'], 1):
                st.markdown(f"{i}. {step}")
        
        with col2:
            st.markdown("### ❌ What NOT to Do")
            for i, donot in enumerate(guide['donot'], 1):
                st.markdown(f"{i}. {donot}")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Nearby hospitals finder
    st.markdown("### 🏥 Find Nearby Hospitals")
    location = st.selectbox("Select Your City", ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Multan", "Peshawar"])
    
    if st.button("Find Hospitals"):
        hospitals = find_nearby_hospitals(location)
        
        st.markdown(f"### Hospitals in {location}")
        for hospital in hospitals:
            st.markdown(f"<div class='health-metric'>" +
                       f"<h4>{hospital['name']}</h4>" +
                       f"<p>Distance: {hospital['distance']}</p>" +
                       f"<p>Phone: {hospital['phone']}</p>" +
                       f"</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Emergency contact cards
    st.markdown("### 📞 Emergency Contacts")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='emergency-guide' style='text-align: center;'>" +
                   "<h3>🚑 Ambulance</h3>" +
                   "<h2>102</h2>" +
                   "</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='emergency-guide' style='text-align: center;'>" +
                   "<h3>🆘 Emergency</h3>" +
                   "<h2>112</h2>" +
                   "</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='emergency-guide' style='text-align: center;'>" +
                   "<h3>👮 Police</h3>" +
                   "<h2>100</h2>" +
                   "</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='emergency-guide' style='text-align: center;'>" +
                   "<h3>🔥 Fire</h3>" +
                   "<h2>101</h2>" +
                   "</div>", unsafe_allow_html=True)

elif st.session_state.active_tab == "Health Reports":
    st.markdown("# 📄 Health Reports")
    st.markdown("### Generate and export your health information")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Report type selection
    report_type = st.selectbox("Select Report Type", [
        "Comprehensive Health Summary",
        "Symptom History Report",
        "Medicine Inventory Report",
        "Family Health Report",
        "Doctor Consultation History"
    ])
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Generate report button
    if st.button("Generate Report", type="primary"):
        report_content = generate_health_report()
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Report Preview")
        st.text_area("Report Content", report_content, height=300)
        
        # Download button
        st.download_button(
            label="Download Report as Text File",
            data=report_content,
            file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Quick export options
    st.markdown("### ⚡ Quick Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Symptom History"):
            symptom_data = "\n".join([f"{entry['timestamp']}: {entry['symptoms']}" for entry in st.session_state.symptom_history])
            st.download_button(
                label="Download Symptoms",
                data=symptom_data,
                file_name="symptom_history.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("Export Medicine List"):
            medicine_data = "\n".join([f"{med['name']} ({med['quantity']}) - Expiry: {med['expiry']}" for med in st.session_state.medicine_inventory])
            st.download_button(
                label="Download Medicines",
                data=medicine_data,
                file_name="medicine_inventory.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("Export Family Health"):
            family_data = "\n".join([f"{member['name']} ({member['relation']}, {member['age']} years)" for member in st.session_state.family_members])
            st.download_button(
                label="Download Family Data",
                data=family_data,
                file_name="family_health.txt",
                mime="text/plain"
            )

elif st.session_state.active_tab == "Voice Assistant":
    st.markdown("# 🎤 Voice Assistant")
    st.markdown("### Use voice commands for hands-free operation")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Voice input section
    st.markdown("### 🎤 Voice Input")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        voice_input = st.text_input("Describe your symptoms or command", value=st.session_state.voice_input, 
                                  placeholder="Click the microphone button and speak...")
    
    with col2:
        if st.button("🎤 Start Listening", key="voice_button", use_container_width=True):
            thread = threading.Thread(target=listen_to_voice)
            thread.start()
    
    if st.session_state.is_listening:
        st.info("Listening... Please speak now")
    
    if voice_input:
        if st.button("Process Voice Command"):
            # Process the voice input
            if any(word in voice_input.lower() for word in ["symptom", "pain", "hurt", "ache", "feel"]):
                st.session_state.symptoms_input = voice_input
                st.session_state.active_tab = "Home"
                st.rerun()
            elif any(word in voice_input.lower() for word in ["reminder", "alert", "remember"]):
                st.session_state.reminder_prefill = voice_input
                st.session_state.active_tab = "Health Reminder"
                st.rerun()
            elif any(word in voice_input.lower() for word in ["report", "summary", "history"]):
                st.session_state.active_tab = "Health Reports"
                st.rerun()
            else:
                st.info("Voice command processed. How can I help you with this?")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Text-to-speech section
    st.markdown("### 🔊 Text-to-Speech")
    
    tts_text = st.text_area("Enter text to convert to speech", placeholder="Type something to hear it spoken...")
    
    if st.button("Speak Text"):
        if tts_text:
            thread = threading.Thread(target=speak_text, args=(tts_text,))
            thread.start()
            st.success("Speaking...")
        else:
            st.error("Please enter some text to speak")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Voice commands guide
    st.markdown("### 📋 Voice Command Guide")
    
    st.markdown("""
    You can use these voice commands:
    
    - **"I have a headache"** - Get remedy for headache
    - **"Set a reminder for my medicine"** - Create a new reminder
    - **"Show my health report"** - Generate health report
    - **"Add family member"** - Go to family health section
    - **"Find nearby hospitals"** - Emergency guide
    """)
    
    # Quick voice command buttons
    st.markdown("### ⚡ Quick Commands")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("I have a headache"):
            st.session_state.voice_input = "I have a headache"
            st.rerun()
    
    with col2:
        if st.button("Set medicine reminder"):
            st.session_state.voice_input = "Set reminder for my medicine"
            st.rerun()
    
    with col3:
        if st.button("Show health report"):
            st.session_state.voice_input = "Show my health report"
            st.rerun()

# Footer
st.markdown("""
<div class='footer'>
    <p>⚠️ <strong>Disclaimer:</strong> For educational purposes only. Consult a doctor for medical advice.</p>
    <p>🌿 Made with ❤️ for better health</p>
</div>
""", unsafe_allow_html=True)
