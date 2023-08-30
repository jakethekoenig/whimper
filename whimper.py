import pyaudio
import numpy as np
import struct
import pynvim
import openai
import os
import wave
from faster_whisper import WhisperModel

openai.api_key = os.getenv("OPENAI_API_KEY")

AUDIO_FILE = "temp.wav"
CHUNK = 512
RATE = 44100
WHISPER_BATCH_SECS = 1
GPT_BATCH_SECS = 4
NUM_CHUNKS = 1200

audio = pyaudio.PyAudio()
# TODO: replace 3 with selection menu
# I keep a buffer that's much larger than the chunks I read so I don't lose frames when I call whisper and or GPT.
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, input_device_index=3, frames_per_buffer=CHUNK*50)

whisper_model_size = "small"
whisper_model = WhisperModel(whisper_model_size)
gpt_model = "gpt-3.5-turbo"
system_prompt = {"role": "system",
                 "content": "The following is a transcription of spoken python. Write the transcript as syntactically valid python:"}

def write_audio(data):
    waveFile = wave.open(AUDIO_FILE, 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(data))	
    waveFile.close()

def segments_to_gpt_prompt(segments):
    history = [system_prompt]
    for segment in segments:
        segment_transcript = {"role": "user", "content": "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)}
        history.append(segment_transcript)
    return history

print("recording...")
data = [] 
last_whisper_run = 0
last_gpt_run = 0
history = []
for i in range(NUM_CHUNKS):
    data += [stream.read(CHUNK)]
    if (i - last_whisper_run) * CHUNK / RATE > WHISPER_BATCH_SECS:
        last_whisper_run = i
        # TODO: pass data directly to whisper
        write_audio(data)
        segments, info = whisper_model.transcribe(AUDIO_FILE, beam_size=5)
        history = segments_to_gpt_prompt(segments)
    if (i - last_gpt_run) * CHUNK / RATE > GPT_BATCH_SECS:
        last_gpt_run = i
        print(history)
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=history
            # stream=True
        )
        print(response["choices"][0]["message"]["content"])

print("finished recording")
stream.close()


@pynvim.plugin
class Whimper:
    def __init__(self, nvim):
        self.nvim = nvim

    def listen_and_insert(self, args):



