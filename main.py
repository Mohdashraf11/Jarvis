import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
import os

#pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "b9f3aeb83fab481bb82ca4a7431bb827"
openai.api_key = os.getenv("OPEN_API_KEY") #openI apikey

def speak(text):
    engine.say(text)
    engine.runAndWait()

#function to process command
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")   
        speak("Opening Instagram")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")   
        speak("Opening Youtube")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")   
        speak("Opening Linkedin")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]  
        webbrowser.open(link) 
    elif "news"in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the list of articles
            articles = data.get("articles", [])

            # Print each headline
            for article in articles:
                speak(article['title'])
    elif"openai" in c.lower():
        speak("what would you like to ask?")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=10)
            try:
                question = recognizer.recognize_google(audio)
                print(f"Question: {question}")
                response = ask_openai(question)
                speak(response)
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that.")
            except sr.RequestError:
                speak("Sorry, there was an error with the speech recognition service.")
    else:
        # Let OpenAi handle request   
        pass  
def ask_openai(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the GPT-4 engine
            prompt=question,
            max_tokens=150  # Adjust max tokens as per your needs
        )
        answer = response.choices[0].text.strip()
        print(f"jarvis Response: {answer}")
        return answer
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I couldn't get a response from OpenAI."           

if __name__ == "__main__":
    speak("initializing jarvis....")   
    while True:
        # Listen for the wake word "jarvis"
        r = sr.Recognizer() 

        # recognize speech using google 
       
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=3, phrase_time_limit=5)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yess..")
                 #Listen for command
                with sr.Microphone() as source:
                    print("jarvis active....")
                    audio = r.listen(source, timeout=2, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
        
