# Crisis Detection Logic & Appointment Scheduler

This project leverages Natural Language Processing (NLP) to detect crisis situations based on user input and provides an appointment scheduling system for urgent cases. The system uses various NLP techniques to identify critical keywords, analyze sentiment, and evaluate urgency based on the time of day.

## Features
- **Keyword Detection**: Detects urgent keywords like "suicide", "self-harm", "help", etc.
- **Sentiment Analysis**: Analyzes the sentiment of the message (positive, negative, or neutral).
- **Time of Day**: Evaluates the time of day to determine urgency.
- **Urgency Scoring**: Combines keyword detection, sentiment analysis, and time of day to compute an urgency score.
- **Staff Alert**: Notifies staff based on the urgency score.
- **Appointment Scheduler**: Schedules an appointment based on urgency, with flexible days (today, tomorrow, etc.).
- **Streamlit UI**: Provides an easy-to-use interface for users to input messages and view results.

## Requirements

### For Crisis Detection Logic
- Python 3.x
- Install the following dependencies:
  ```bash
  pip install -r requirements.txt
  ```

  **requirements.txt** for Crisis Detection Logic:
  ```txt
  spacy==3.6.0
  nltk==3.8.1
  ```

### For Streamlit Version with UI
- Install the following dependencies:
  ```bash
  pip install -r requirements.txt
  ```

  **requirements.txt** for Streamlit Version:
  ```txt
  streamlit==1.22.0
  spacy==3.6.0
  nltk==3.8.1
  ```

## Setup Instructions

### 1. Install the Dependencies
First, make sure to install the required Python packages by running the following command:
```bash
pip install -r requirements.txt
```

### 2. Run the Crisis Detection Logic
To run the crisis detection logic:
1. Run the Python script using:
   ```bash
   python crisis_detection.py
   ```

### 3. Run the Streamlit App
To run the Streamlit app:
1. Open a terminal in the project folder and activate your virtual environment (if any).
2. Run the following command:
   ```bash
   streamlit run app.py
   ```
3. Visit the URL provided by Streamlit in your browser to interact with the app.

## Example Usage

1. **Crisis Detection Logic (Command Line Interface)**:
   - Enter a patient's message when prompted.
   - The system will return detected keywords, sentiment, time of day, urgency score, and whether staff should be alerted.

2. **Streamlit App**:
   - Enter a patient's message in the text area.
   - Click "Detect" to see the results and the appointment scheduling.
   - If needed, click "Clear" to reset the inputs.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Made by **Tanishq Bololu**  
[LinkedIn](https://www.linkedin.com/in/tanishqbololu/)
