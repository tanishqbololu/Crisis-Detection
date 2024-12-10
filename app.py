# Track B: Crisis Detection Logic
import streamlit as st
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime,timedelta
import base64

# Function to add a background image to Streamlit app
def add_bg_image(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    bg_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

# Add background image
add_bg_image("bg.png")

# Streamlit UI
st.title("Crisis Detection and Appointment Scheduler")  # Title
st.write(
    'The Crisis Detection and Appointment Scheduler is a sophisticated tool designed to assist mental health professionals '
    'in identifying urgent situations and managing patient appointments seamlessly. By leveraging advanced Natural Language '
    'Processing (NLP) techniques and a structured rule-based system, the application provides timely insights and facilitates '
    'efficient intervention for patients in crisis'
)  # Description

nlp = spacy.load("en_core_web_md")

# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def nltk_tokenize_and_filter(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def spacy_analyze(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    named_objs = [(objs.text, objs.label_) for objs in doc.ents]
    return tokens, named_objs


URGENT_KEYWORDS = {"suicide", "self-harm", "emergency", "help", "crisis", "danger","dying","bleeding","risky","die"}

def detect_keywords(tokens):
    detected_keywords = [word for word in tokens if word in URGENT_KEYWORDS]
    return detected_keywords


SENTIMENT_WORDS = {
    'positive': {"good", "happy", "safe", "calm", "hopeful"},
    'negative':{"bad", "sad", "angry", "hopeless", "unsafe", "scared"}
}
positive_words = SENTIMENT_WORDS['positive']
negative_words = SENTIMENT_WORDS['negative']

def sentiment_analyze(tokens):
    positive_count = sum(1 for token in tokens if token in positive_words)
    negative_count = sum(1 for token in tokens if token in negative_words)
    if positive_count > negative_count:
        return 1 # Positive sentiment
    elif negative_count > positive_count:
        return -1 # Negative sentiment
    else:
        return 0  # Neutral sentiment
    
    
def time_of_day(current_hour):
    if current_hour < 6:
        return "night"
    elif current_hour < 9:
        return "early morning"
    elif current_hour < 12:
        return "morning"
    elif current_hour < 18:
        return "afternoon"
    else:
        return "evening"
    
def urgency_score(detected_keywords, sentiment, time_of_day):
    keyword_weight = len(detected_keywords) * 10
    sentiment_weight = (1 - sentiment) * 20
    time_weight = 5 if time_of_day in ['night', 'early morning'] else 0
    return int(keyword_weight + sentiment_weight + time_weight)


def should_alert_staff(urgency_score, threshold=50):
    return urgency_score >= threshold


# Example for preferred data, available slots
def schedule_appointment(urgency_score):
    if urgency_score > 90:
        days_offset = 0  # Today
    elif urgency_score > 70:
        days_offset = 1  # Tomorrow
    elif urgency_score > 50:
        days_offset = 2  # Day after tomorrow
    elif urgency_score > 30:
        days_offset = 3  # Two days later
    else:
        return "Urgency score too low. No urgent appintment needed."
    
    # Calculate the target date
    target_date = (datetime.now() + timedelta(days=days_offset)).strftime("%d-%m-%Y")
    return target_date

# Take User Input
user_input = st.text_area("Enter the patient's message:")  # User input

# Process Input
tokens = nltk_tokenize_and_filter(user_input)
detected_keywords = detect_keywords(tokens)
sentiment = sentiment_analyze(tokens)
current_hour = datetime.now().hour
time_period = time_of_day(current_hour)
calculated_score = urgency_score(detected_keywords, sentiment, time_period)
alert = should_alert_staff(calculated_score)

# Get current date
current_date = datetime.now().strftime("%dd-%mm-%Y")

###
def clear_inputs():
    st.session_state['detected_keywords'] = []
    st.session_state['sentiment'] = 0
    st.session_state['time_period'] = ''
    st.session_state['calculated_score'] = 0
    st.session_state['alert'] = False
    st.session_state['target_date'] = ''
    st.session_state['user_input'] = ""

if st.button('Detect'):
    if user_input:
        # Process Input
        tokens = nltk_tokenize_and_filter(user_input)
        detected_keywords = detect_keywords(tokens)
        sentiment = sentiment_analyze(tokens)
        current_hour = datetime.now().hour
        time_period = time_of_day(current_hour)
        score = urgency_score(detected_keywords, sentiment, time_period)
        alert = should_alert_staff(score)

        # Display Results
        st.subheader("Results")
        st.write("Detected Keywords:", detected_keywords)
        st.write("Sentiment (1=Positive, -1=Negative, 0=Unrecognisable/Neutral):", sentiment)
        st.write("Time of Day:", time_period)
        st.write("Urgency Score:", score)
        st.write("Should Alert Human Staff:", alert)

        # Appointment Scheduler Section
        st.subheader("Appointment Scheduler")
        target_date = schedule_appointment(score)
        if "Urgency score too low" not in target_date:
            st.write("Appointment Target Date:", target_date)
            # Clear button
            if st.button('Clear'):
             clear_inputs()
        else:
            st.write(target_date)
            # Clear button
            if st.button('Clear'):
             clear_inputs()
    else:
        st.error('Please enter a message')

st.markdown("""
    ---
    <div style="text-align: center;">
        Made by Tanishq Bololu 😁<br>
        🚀 <a href="https://www.linkedin.com/in/tanishqbololu/" target="_blank">LinkedIn</a>
    </div>
""", unsafe_allow_html=True)


# To run streamlit app: 
    # 1. Activate env  
    # 2. In terminal write : streamlit run app.py