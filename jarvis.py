
import webbrowser
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>0 and hour<12:
       speak("Good morning!")

    elif hour>=12 and hour<17:
        speak("Good afternoon!")
    else:       
         speak("Good Evening!")
    speak("Hello Sir I am your digital assistant jarvis How may i help you")

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen( source)

    try :
        print("Recognition...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)

        print("Say that again please")
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()


        if 'wikipedia' in query:
            print("Searching Wikipedia")
            speak("Searching Wikipedia")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            print("According to wikipedia") 
            speak("According to wikipedia")
            print(results)
            speak(results)


        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
        
        elif 'open google' in query:
            webbrowser.open("www.google.com")
        
        elif 'open gmail' in query:
            webbrowser.open("www.gmail.com")

        elif 'open facebook' in query:
            webbrowser.open("www.facebook.com")

        
        elif 'open sami song' in query:
            webbrowser.open("www.youtube.com/watch?v=vdY5SFZBgnk")
        
        elif 'who is kushal ' in query:
            speak("kushal is a intelligent person")

        elif 'play music' in query:
            music = 'C:\\Music'
            songs = os.listdir(music)
            os.startfile(os.path.join(music ,songs[4]))

        elif 'exit' in query:
            quit()            





   
   
