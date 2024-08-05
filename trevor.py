import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser
import random
import time
import randfacts

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(wake_word=False):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        if wake_word:
            print("Listening for wake word...")
        else:
            print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        if not wake_word:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        if not wake_word:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    except Exception as e:
        if not wake_word:
            print(f"Unexpected error: {e}")
            speak(f"Unexpected error: {e}")
        return ""

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I assist you today?")

def get_time():
    now = datetime.datetime.now().strftime("%H:%M")
    return f"The current time is {now}"

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def tell_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        joke_data = response.json()
        joke = f"{joke_data['setup']} ... {joke_data['punchline']}"
        return joke
    except Exception as e:
        return "Sorry, I can't tell you a joke right now."

def set_reminder(reminder, seconds):
    speak(f"Setting a reminder for {reminder} in {seconds} seconds.")
    time.sleep(seconds)
    speak(f"Reminder: {reminder}")

def fun_fact():
    fact = randfacts.get_fact()
    print(fact)
    speak(fact)

def dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    dog_image = response.json()
    speak("Here's a random dog image:")
    print(dog_image['message'])

def web_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching for {query} on the web")

def kanye_quote():
    try:
        response = requests.get("https://api.kanye.rest")
        quote_data = response.json()
        quote = quote_data['quote']
        speak(f"Kanye says: {quote}")
    except Exception as e:
        speak("Sorry, I couldn't fetch a Kanye quote at the moment.")

def main():
    wake_words = ("hey trevor", "yo trevor", "hi trevor")
    while True:
        command = listen(wake_word=True)
        if any(wake_word in command for wake_word in wake_words):
            greet_user()
            while True:
                command = listen()
                if not command:  # If command is empty, skip processing
                    continue
                if "hello" in command:
                    speak("Hello! How can I help you?")
                elif "time" in command:
                    current_time = get_time()
                    speak(current_time)
                elif "open" in command and "website" in command:
                    speak("Which website?")
                    website = listen()
                    if website:
                        open_website(website)
                elif "tell me a joke" in command or "a joke" in command:
                    joke = tell_joke()
                    speak(joke)
                elif "set a reminder" in command or "remind me" in command:
                    speak("What should I remind you about?")
                    reminder = listen()
                    speak("In how many seconds?")
                    seconds = int(listen())
                    set_reminder(reminder, seconds)
                elif "exit" in command or "stop" in command:
                    speak("Goodbye!")
                    return
                elif "heads and tails" in command or "coin flip" in command:
                    random_number = random.randint(0, 1)
                    if random_number == 0:
                        speak("Heads")
                    else:
                        speak("Tails")
                elif "tell me a fun fact" in command or "tell me a random fact" in command:
                    fun_fact()
                elif "show me a dog" in command or "dog" in command:
                    speak("Show you an image of a dog:")
                    dog()
                elif "search" in command or "google" in command:
                    speak("What do you want to search for?")
                    query = listen()
                    if query:
                        web_search(query)
                elif "kanye quote" in command or "kanye says" in command:
                    kanye_quote()
                else:
                    speak("I'm sorry, I didn't understand that.")
            break  # Break out of the while loop after processing commands

if __name__ == "__main__":
    main()
