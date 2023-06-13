from potassium import Potassium, Request, Response
import base64

from transformers import pipeline

import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

app = Potassium("my_app")

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = MusicGen.get_pretrained('melody', device=device)
   
    context = {
        "model": model
    }

    return context

# @app.handler runs for every call
@app.handler()
def handler(context: dict, request: Request) -> Response:
    prompt = request.json.get("prompt")
    duration = request.json.get("duration", 4)
    descriptions = [prompt]

    model = context.get("model")
    model.set_generation_params(duration=duration)  # generate 8 seconds.

    wav = model.generate(descriptions)  # generates a sample
    print(wav.shape)
    # the shape of wav is torch.Size([1, 1, 320000]) can you extract just the wav part

    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)


    # load wav file and encode as base64
    wav_bytes = open('0.wav', 'rb').read()
    wav_encoded = base64.b64encode(wav_bytes).decode('utf-8')

    return Response(
        json = {"outputs": wav_encoded}, 
        status=200
    )

if __name__ == "__main__":
    app.serve()