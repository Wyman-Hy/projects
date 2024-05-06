import openai
import pyttsx3
import speech_recognition

openai.api_key = "USE YOUR OWN API KEY"

limit = 1
context = ""
here_sir = "You called sir"
on = "Powering on sir"
off = "Powering off sir"
anytime = "Anytime sir"
activate = False

def jarvis_answer(query, context):
    answer = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=context + query,
        max_tokens = 50,
        temperature = 0.5,
        top_p = 1
    )
    return answer.choices[0].text.strip()

def jarvis_speak(speak):
    jarvis = pyttsx3.init()
    jarvis.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    jarvis.setProperty("rate", 150)
    jarvis.setProperty("volume", 1)
    jarvis.say(speak)
    jarvis.runAndWait()

speech = speech_recognition.Recognizer()
speech.energy_threshold = 4000



while True:
    try:
        with speech_recognition.Microphone() as mic:
            print("I'm listening sir..")
            speech.adjust_for_ambient_noise(mic)
            listen = speech.listen(mic, timeout=5)
            
        activation = speech.recognize_google(listen).lower()
        print(activation)
        if activation in ["on", "turn on"]:
            jarvis_speak(on)
            print(on)
            activate = True
        elif activation in ["off", "turn off"]:
            jarvis_speak(off)
            print(off)
            activate = False
        elif activation in ["thank you", "that is all"]:
            jarvis_speak(anytime)
            print(anytime)
            activate = False
    except Exception as error:
        print("Error: ", str(error))
    try:
        with speech_recognition.Microphone() as mic:
            print("I'm listening sir..")
            print(activate)
            speech.adjust_for_ambient_noise(mic)
            listen = speech.listen(mic, timeout=5)

        activation = speech.recognize_google(listen).lower()
        print(activation)

        if activate:
            if activation in ["jarvis", "travis", "arvis"]:
                jarvis_speak(here_sir)
                print("You called sir.")
                with speech_recognition.Microphone() as mic:
                    audio = speech.listen(mic)
                query = speech.recognize_google(audio).lower()
                print(query)
                answer = jarvis_answer(query, context)
                context += f"\nUser: {query}\nAI: {answer}"
                context = context.split("\n")[-limit*2:]
                context = "\n".join(context)
                print(answer)
                jarvis_speak(answer)
    except Exception as error:
        print("Error: ", str(error))