import pyaudio
import pynvim
import openai
import os
import wave
from faster_whisper import WhisperModel

openai.api_key = os.getenv("OPENAI_API_KEY")

audio_file = "temp.wav"

CHUNK = 512
RATE = 44100
WHISPER_BATCH_SECS = 1
GPT_BATCH_SECS = 4
NUM_CHUNKS = 1000

audio = pyaudio.PyAudio()
# TODO: replace 3 with selection menu
# I keep a buffer that's much larger than the chunks I read so I don't lose frames when I call whisper and or GPT.
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, input_device_index=3, frames_per_buffer=CHUNK*50)

model_size = "tiny"
model = WhisperModel(model_size)
gpt_model = "gpt-3.5-turbo"
system_prompt = {"role": "system",
                 "content": "The following is a transcription of spoken python. Write the transcript as syntactically valid python:"}
print("recording...")
data = []
for i in range(NUM_CHUNKS):
    data += [stream.read(CHUNK)]
    if i % (RATE * WHISPER_BATCH_SECS // CHUNK) == 0:
        waveFile = wave.open(audio_file, 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(data))	
        waveFile.close()
        segments, info = model.transcribe(audio_file, beam_size=5)
        history = [system_prompt]
        for segment in segments:
            segment_transcript = {"role": "user", "content": "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)}
            history.append(segment_transcript)
            print(segment_transcript)
    # response = openai.ChatCompletion.create(
        # model=gpt_model,
        # messages=history
        # # stream=True
    # )
    # print(response["choices"][0]["message"]["content"])

print("finished recording")
stream.close()


@pynvim.plugin
class Whimper:
    def __init__(self, nvim):
        self.nvim = nvim


