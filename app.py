import os
import openai
from flask import Flask, render_template, request, send_file
from gtts import gTTS
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def malayalam_speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="ml-IN")
        return text
    except Exception as e:
        return str(e)

def generate_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message['content']

def text_to_speech(text):
    tts = gTTS(text=text, lang='ml')
    tts.save("response.mp3")
    return "response.mp3"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get voice input
    user_input = malayalam_speech_to_text()
    
    # Generate response
    bot_response = generate_gpt_response(user_input)
    
    # Convert to speech
    audio_file = text_to_speech(bot_response)
    
    return send_file(audio_file, mimetype="audio/mp3")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)