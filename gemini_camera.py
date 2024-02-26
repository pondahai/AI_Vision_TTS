from gtts import gTTS
from io import BytesIO
import os
import json
import base64

import pygame
pygame.init()

import cv2

# take photo
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imshow("capture", frame)
cv2.imwrite("image1.jpg", frame)
cv2.waitKey(3000)

cap.release()
cv2.destroyAllWindows()

#os.system("fswebcam -r 800x600 --no-banner image1.jpg")

import time
time.sleep(1)

# base64 encode
with open("image1.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# json
dictionary = {
    'contents':[
        {
            'parts':[
                {   'text': '看到什麼'},
                {    
                    'inline_data':{
                        'mime_type': 'image/jpeg',
                        'data': encoded_string.decode('utf-8')
                    }
                }
            ]
        }
    ]
}
 
#print(dictionary)

# Serializing json
json_object = json.dumps(dictionary)
 
# Writing to sample.json
with open("request.json", "w") as outfile:
    outfile.write(json_object)


# get API_KEY
with open("apikey.txt", "r") as f:
    first_line = f.readline()
API_KEY = first_line

# REST API
import requests
response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key="+API_KEY+"", json=dictionary)
response_json = response.json()
#print(response_json)
def get_value(data, key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                return v
            else:
                value = get_value(v, key)
                if value is not None:
                    return value
    elif isinstance(data, list):
        for v in data:
            value = get_value(v, key)
            if value is not None:
                return value
    return None
#print(get_value(response_json, "text"))
#response_text = response_json['candidates'][0]['content']['parts'][0]['text']
response_text = get_value(response_json, "text")

#result = os.popen("curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key="+API_KEY+" -H 'Content-Type: application/json' -d @request.json ").read()
#print(result)
#response_text = json.loads(result)
print(response_text)

# TTS
mp3_fp = BytesIO()
tts = gTTS(text=response_text, lang='zh-TW')
tts.write_to_fp(mp3_fp)

# audio play
mp3_fp.seek(0)
pygame.mixer.init()
pygame.mixer.music.load(mp3_fp)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

