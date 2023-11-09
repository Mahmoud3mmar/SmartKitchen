import speech_recognition as sr

def speak():
    # Create a Recognizer instance
    recognizer = sr.Recognizer()

    # Use the microphone to capture audio
    with sr.Microphone() as source:
        print("Please start speaking...")
        audio = recognizer.listen(source)

    # Recognize the speech
    try:
        text = recognizer.recognize_google(audio)  # You can choose other recognition engines as well
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Sorry, there was an error making the request: {0}".format(e))







