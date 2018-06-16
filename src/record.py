import os
import wave
from array import array

import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
AUDIO_FILE_NAME = "/home/pi/data/audio/recording.wav"

if not os.path.exists('/home/pi/data'):
    os.mkdir('/home/pi/data')
    os.mkdir('/home/pi/data/audio')
elif not os.path.exists('/home/pi/data/audio'):
    os.mkdir('/home/pi/data/audio')

audio = pyaudio.PyAudio()

# recording prerequisites
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# starting recording
frames = []
recording = False
tried = 0
volume = []

while True:
    data = stream.read(CHUNK)
    vol = max(array('h', data))
    print(vol)
    if vol > 10000:
        recording = True
        tried = 0
    else:
        if recording:
            tried += 1
            if tried > 25:
                break
        else:
            tried += 1
            if tried > 50:
                break

    if recording:
        frames.append(data)

# end of recording
stream.stop_stream()
stream.close()
audio.terminate()

if recording:
    # writing to file
    wavfile = wave.open(AUDIO_FILE_NAME, 'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(frames))
    wavfile.close()
else:
    try:
        os.remove(AUDIO_FILE_NAME)
    except FileNotFoundError:
        pass
