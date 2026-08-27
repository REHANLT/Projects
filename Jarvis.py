import os
import re
import requests
import speech_recognition as sr
import wikipedia
import win32com.client
from dotenv import load_dotenv
from google import genai

# Load environment variables
dotenv_path = r"C:\Users\Victus\.env"
load_dotenv(dotenv_path)

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Xweather Credentials
XWEATHER_CLIENT_ID = (
    os.getenv("XWEATHER_CLIENT_ID") or "xqF6CDGA25WrsQX5ZmC4e"
).strip()
XWEATHER_CLIENT_SECRET = (
    os.getenv("XWEATHER_CLIENT_SECRET")
    or "3dq4wkXfdnZl0xek84x18hDmFWQqJPl6IeHog6qQ"
).strip()
DEFAULT_CITY = "Ahmedabad"

# Text-to-Speech setup (Windows Native SAPI)
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0


def speak(text):
    print("JARVIS:", text)
    text = re.sub(r"[*_`#>-]", "", str(text))
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,!?'\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    speaker.Speak(text)


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print("YOU:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""


def get_weather(location=DEFAULT_CITY):
    """Fetches real-time weather for any location globally with automatic fallback matching."""
    if not XWEATHER_CLIENT_ID or not XWEATHER_CLIENT_SECRET:
        return "Xweather API credentials missing."

    url = "https://data.api.xweather.com/conditions"

    # Clean location input
    clean_location = location.strip()

    # Create primary and fallback location search queries
    queries_to_try = [clean_location]

    # If simple city string (no comma), add automatic fallback with country
    if "," not in clean_location:
        queries_to_try.append(f"{clean_location},India")
        queries_to_try.append(f"{clean_location},IN")

    data = None
    for query in queries_to_try:
        params = {
            "p": query,
            "client_id": XWEATHER_CLIENT_ID,
            "client_secret": XWEATHER_CLIENT_SECRET,
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if response.status_code == 200 and data.get("success"):
                break  # Successful match found
        except requests.exceptions.RequestException:
            continue

    if data and data.get("success"):
        periods = data["response"][0]["periods"][0]
        temp_c = periods["tempC"]
        temp_f = periods["tempF"]
        weather_desc = periods["weather"]

        place_info = data["response"][0]["place"]
        city_name = place_info.get("name", location).title()
        state_or_country = (
            place_info.get("state") or place_info.get("country") or ""
        ).upper()

        full_place = (
            f"{city_name}, {state_or_country}" if state_or_country else city_name
        )

        return f"The weather in {full_place} is currently {weather_desc} with a temperature of {temp_c} degrees Celsius ({temp_f} degrees Fahrenheit)."
    else:
        error_desc = (
            data.get("error", {}).get("description", "Location not found.")
            if data
            else "No response."
        )
        print(f"[DEBUG API Response]: {data}")
        return f"Could not find weather details for '{location}'. {error_desc}"



def extract_location(command):
    """Extracts target location from voice commands accurately."""
    # Pattern to match: "weather in Paris", "temperature of New York", "weather for Japan"
    match = re.search(
        r"(?:weather|temperature)(?:\s+(?:in|of|for|at))?\s+(.+)", command
    )
    if match:
        location = match.group(1).strip()
        # Clean up stray leading prepositions
        location = re.sub(r"^(in|of|for|at)\s+", "", location).strip()
        return location
    return DEFAULT_CITY


def jarvis():
    speak("Hello. I am Jarvis. How can I help you?")

    while True:
        command = listen()

        if command == "":
            continue

        if any(kw in command for kw in ["exit", "quit", "stop", "bye"]):
            speak("Goodbye. Have a nice day.")
            break

        elif "weather" in command or "temperature" in command:
            location = extract_location(command)
            speak(f"Fetching weather information for {location}.")
            weather_report = get_weather(location)
            speak(weather_report)

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                speak("Searching Wikipedia.")
                try:
                    summary = wikipedia.summary(
                        topic, sentences=2, auto_suggest=True
                    )
                    speak(summary)
                except Exception:
                    speak("Could not find that topic on Wikipedia.")

        else:
            speak("Let me think.")
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash", contents=command
                )
                speak(response.text)
            except Exception as e:
                print(f"Gemini Error: {e}")
                speak("I encountered an error processing your request.")


if __name__ == "__main__":
    jarvis()
