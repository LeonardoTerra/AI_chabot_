import openai
import speech_recognition as sr
import time
import threading
import pyttsx3

# Getting API_key from env variable

openai.api_key = 'api key goes here'

AIreply = False
final_msg = ""

# Initiation of the text to vocal engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
# changing index, changes voices
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')  # details about the current speaking rate
engine.setProperty('rate', 160)  # new voice rate


# Function that will execute the AI engine
def generate_response(prompt):
    global AIreply, final_msg
    completions = openai.Completion.create(
        engine="text-davinci-003",  # "text-davinci-003"#"text-babbage-001" #other AI
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    final_msg = message.strip()
    AIreply = True


def chatprinter(chat):
    for word in chat:
        time.sleep(0.055)
        print(word, end="", flush=True)
    print()

# Without speech recognition

print('--------------------- Frida ---------------------')
while True:
    print("User:", end=' ', flush=True)
    try:
        TextResult = input()
        if 'stop' in TextResult:
            print("Ending comunication")
            break
        t1 = threading.Thread(target=generate_response, args=(TextResult,))
        t1.start()

        chatprinter(TextResult)

        while AIreply == False:
            pass
        AIreply = False

        print("ChatGPT:", end="")
        t2 = threading.Thread(target=chatprinter, args=(final_msg,))
        t2.start()

        # start reading the text received
        engine.say(final_msg)
        engine.runAndWait()
        print("-------------------------------------------------")

    except KeyboardInterrupt:
        print('Ending application.')

# Setting up the speech recognition and praparing the main loop
'''
r = sr.Recognizer()
with sr.Microphone() as source:
    print('--------------------- Frida ---------------------')
    while True:
        print("User:", end=' ', flush=True)
        audio = r.listen(source)
        # here we execute the code to understand the speech
        try:
            text = r.recognize_google(audio, show_all=True)
            TextResult = text['alternative'][0]['transcript']
            if 'stop' in TextResult:
                print("Ending comunication")
                break
            t1 = threading.Thread(target=generate_response, args=(TextResult,))
            t1.start()

            chatprinter(TextResult)

            while AIreply == False:
                pass
            AIreply = False

            print("ChatGPT:", end="")
            t2 = threading.Thread(target=chatprinter, args=(final_msg,))
            t2.start()

            # start reading the text received
            engine.say(final_msg)
            engine.runAndWait()
            print("-------------------------------------------------")

        except:
            print("Sorry, I couldn't recognize your voice")
'''
