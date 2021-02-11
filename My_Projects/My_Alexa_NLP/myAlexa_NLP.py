import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import requests
 
listener = sr.Recognizer()
engine = pyttsx3.init()
voices =  engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    # engine using for pyttsx python talk to me
    engine.say(text)
    engine.runAndWait()

def myCommand():
    print("Ram....")
    try:
        with sr.Microphone() as source:
            print("Listening Ram....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace("alexa","")
                print(command)
    except:
        pass
    return command

def run_Alexa():
    command = myCommand()
    if "play" in command:
        video = command.replace("play", '')
        talk("Playing your"+video)
        pywhatkit.playonyt(video)
    elif "info" or "information" or "details" in command:
        info1 = command.replace('info','')
        info1 = command.replace('information','')
        info1 = command.replace('details','')
        info = wikipedia.summary(info1, 1)
        print(info)
        talk(info)
    
while True:
    run_Alexa()
