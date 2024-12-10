# Track B: Crisis Detection Logic

import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime,timedelta

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
        return "Urgency score too low."
    
    # Calculate the target date
    target_date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    return target_date

# Take User Input
user_input = input("Enter the patient's message: ")

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

# Display Results
print("\n--- Results ---")
print("Filtered Tokens:", tokens)
print("Detected Keywords:", detected_keywords)
print("Sentiment (1=Positive, -1=Negative, 0=Unrecognisable/Neutral):", sentiment)
print("Time of Day:", time_period)
print("Current Date:", current_date)
print("Urgency Score:", calculated_score)
print("Should Alert Human Staff:", alert)

target_date = schedule_appointment(calculated_score)
if "Urgency score too low" not in target_date:
    print("Appointment Target Date:", target_date)
else:
    print(target_date)