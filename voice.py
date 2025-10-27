import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import sounddevice as sd
import numpy as np

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)  # speaking speed

def speak(text):
    """Make the assistant speak"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen using sounddevice instead of PyAudio"""
    recognizer = sr.Recognizer()
    fs = 44100  # Sample rate
    duration = 5  # seconds to record

    speak("Listening...")
    print("🎤 Listening for 5 seconds... Speak now!")

    # Record audio from mic
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording finishes

    # Convert recording to AudioData for SpeechRecognition
    audio_data = sr.AudioData(recording.tobytes(), fs, 2)

    try:
        print("🧠 Recognizing speech...")
        command = recognizer.recognize_google(audio_data, language='en-in')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please say that again.")
        return ""
    except sr.RequestError:
        speak("Sorry, there seems to be a network issue.")
        return ""

def greet_user():
    """Greet user based on time"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def run_assistant():
    """Main assistant loop"""
    greet_user()
    speak("Hi, I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        if 'hello' in command:
            speak("Hello there! How are you today?")
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
        elif 'date' in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today is {today}")
        elif 'search' in command:
            search_term = command.replace("search", "").strip()
            if search_term:
                speak(f"Searching the web for {search_term}")
                pywhatkit.search(search_term)
            else:
                speak("Please tell me what you want to search for.")
        elif 'bye' in command or 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a nice day.")
            break
        elif command != "":
            speak("Sorry, I don't understand that yet. Try saying 'search', 'time', or 'date'.")

if __name__ == "__main__":
    run_assistant()

