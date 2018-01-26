"""Transcribe the given audio file."""
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()
speech_file = "output.wav"
with open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

audio = types.RecognitionAudio(content=content)
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')

response = client.recognize(config, audio)
# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print('Transcript: {}'.format(result.alternatives[0].transcript))