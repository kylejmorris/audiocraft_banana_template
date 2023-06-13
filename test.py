import requests
import base64

# URL of the server endpoint
url = 'http://localhost:8000/'  # Replace with the actual URL

# post a json payload
payload = {
    "prompt": "russion hard bass with jazz background",
    "duration": 10
}

response = requests.post(url, json=payload)

# Ensure the request was successful
if response.status_code == 200:
    # Extract the base64-encoded audio data from the response
    audio_data_base64 = response.json().get('outputs')

    # Decode the base64-encoded audio data
    audio_data_bytes = base64.b64decode(audio_data_base64)

    # Specify the output file path
    output_path = 'output.wav'  # Replace with your desired output file path

    # Save the audio data to a WAV file
    with open(output_path, 'wb') as f:
        f.write(audio_data_bytes)
   
    print('WAV file saved successfully.')
else:
    print('Error occurred. Status Code:', response.status_code)
