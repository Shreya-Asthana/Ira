import speech_recognition as sr
import pyttsx3
import openai


# Set the OpenAI API key
openai.api_key = "your api_key"

# Initialize the speech recognition object
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine1 = pyttsx3.init()

def listen():
    """
    Listen for voice input and return the text transcription
    """
    # Create a new speech recognition object
    r = sr.Recognizer()

    try:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Say something!")
            # Listen for audio input with a timeout of 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            try:
                # Recognize the spoken words using Google's speech recognition API
                text = r.recognize_google(audio)
                print("You said: ", text)
                return text
            except sr.UnknownValueError:
                # Handle the case where the speech recognition API cannot understand the audio
                print("Sorry, I could not understand what you said.")
    except sr.WaitTimeoutError:
        # Handle the case where no speech is detected within the timeout period
        print("Timeout: No speech detected.")
    except sr.RequestError as e:
        # Handle the case where there is an error with the speech recognition API request
        print("Error fetching results: {0}".format(e))
    return ""

def chat_with_gpt(prompt):
    """
    Send the user's prompt to the OpenAI API and return the response
    """
    # Create a new completion request to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # Return the text response from the OpenAI API
    return response.choices[0].text.strip()

def speak(text):
    """
    Speak the given text using the text-to-speech engine
    """
    # Use the text-to-speech engine to speak the text
    engine1.say(text)
    engine1.runAndWait()

if __name__ == "__main__":
    # Initialize a flag to control the loop
    flag = 0
    while flag == 0:
        # Listen for voice input
        text = listen().lower()
        # Check if the user said something
        if text:
            if "that's it stop" in text:
                # Set the flag to exit the loop
                flag = 1
            else:
                # Generate a response using the OpenAI API
                response = chat_with_gpt(text)
                print(response)
                # Speak the response using the text-to-speech engine
                speak(response)

# Close the text-to-speech engine
engine1.stop()