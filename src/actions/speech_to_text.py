import os

import speech_recognition as sr


def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something")
        audio = r.listen(source, timeout=1, phrase_time_limit=7)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text
        except sr.UnknownValueError:
            os.system("mpg123 '/home/pi/Robot/src/audio/sorryICouldNotUnderStandYou.mp3'")
