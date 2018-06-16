import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def get_user_input(language_code='en-US'):
    audio_file = '/home/pi/data/audio/recording.wav'

    # record audio
    os.system('python /home/pi/Robot/src/record.py')
    if not os.path.exists(audio_file):
        os.system("mpg123 '/home/pi/Robot/src/audio/sorryICouldNotUnderStandYou.mp3'")
        return

    client = speech.SpeechClient()
    with io.open(audio_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code
    )

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        if not result.alternatives[0].transcript:
            os.system("mpg123 '/home/pi/Robot/src/audio/sorryICouldNotUnderStandYou.mp3'")
            return None
        return result.alternatives[0].transcript
