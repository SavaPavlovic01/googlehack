from fastapi import FastAPI, File, UploadFile, Form
from google.cloud import speech, storage
from pydub import AudioSegment
import yt_dlp
import uuid
import os
import re
import requests
import tensorflow as tf
import numpy as np
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import vision
from fastapi.middleware.cors import CORSMiddleware

from databases import Database

app = FastAPI(debug=True)
origins = [
    "http://localhost:4200",  # Angular dev server
    # Add production domain here later if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Frontend URLs allowed to access the API
    allow_credentials=True,
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allow all headers
)
client = vision.ImageAnnotatorClient()
tokenizer = AutoTokenizer.from_pretrained("fine_tuned_bertic_hate_speech")
model = TFAutoModelForSequenceClassification.from_pretrained("fine_tuned_bertic_hate_speech")


DATABASE_URL = "postgresql+asyncpg://postgres:stagod@35.198.83.220:5432/postgres"

database = Database(DATABASE_URL)

async def insert_tweet(username: str, content: str, link: str, counter: int = 0):
    query = """
    INSERT INTO tweets (username, content, link, counter)
    VALUES (:username, :content, :link, :counter)
    ON CONFLICT(link) DO UPDATE SET counter = tweets.counter + :counter
    """
    await database.execute(query, values={
        "username": username,
        "content": content,
        "link": link,
        "counter": counter
    })

@app.get("/tweets/get")
async def get_tweets():
    query = "SELECT * FROM tweets"
    return await database.fetch_all(query)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Configure your bucket and credentials
GCS_BUCKET = "video_kofa"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\JA\\Desktop\\projekti\\hackaton\\bamboo-sweep-458718-t7-2c8cc2f20023.json"
def is_hate_speech_internal(text:str):
    encoded_samples = tokenizer(text, return_tensors='tf', padding=True, truncation=True, max_length=128)
    # Get model predictions (logits)
    raw_predictions = model.predict(encoded_samples).logits
    # Convert logits to probabilities (optional) and get predicted class
    probabilities = tf.nn.softmax(raw_predictions, axis=-1).numpy()
    predicted_classes = np.argmax(probabilities, axis=-1)
    print(predicted_classes, probabilities)
    return {"isHate":int(np.argmax(probabilities, axis=-1)[0]), "probability":float(np.max(probabilities)) }




@app.post("/text")
def is_hate_speech(text:str = Form(...)):

    result = is_hate_speech_internal(text)
    return result

def upload_to_gcs(local_path, gcs_filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob(gcs_filename)
    blob.upload_from_filename(local_path)
    return f"gs://{GCS_BUCKET}/{gcs_filename}"

def transcribe(gcs_uri):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sr",
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=600)
    return " ".join([r.alternatives[0].transcript for r in response.results])

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4()}.mp4"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    audio_path = temp_path.replace(".mp4", ".wav")
    AudioSegment.from_file(temp_path).set_channels(1).set_frame_rate(16000).export(audio_path, format="wav")

    gcs_uri = upload_to_gcs(audio_path, os.path.basename(audio_path))
    transcript = transcribe(gcs_uri)

    os.remove(temp_path)
    os.remove(audio_path)

    return is_hate_speech_internal(transcript)
                                                                 

def extract_id_from_url(url):
    match = re.search(r'/([^/]+)$', url)
    if match:
        return match.group(1)
    else:
        return None

def get_username_twitter(url):
    username =url.split("x.com/")[1].split('/')[0]
    return username

@app.post("/twitter")  
async def get_tweet_text(text: str = Form(...)):
    id = extract_id_from_url(text)
    url = f"https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"
    r = requests.get(url)
    data = r.json()

     
    
    
    result = is_hate_speech_internal(data['text'])
    if result['isHate']:
        await insert_tweet(get_username_twitter(text), data['text'], url, 1)
    return result

@app.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...)):
    # Read the file as bytes
    image_data = await file.read()

    # Prepare the image for Vision API
    image = vision.Image(content=image_data)

    # Call the Vision API to extract text
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # If no text is found
    if not texts:
        return 400

    # Return the full text detected
    detected_text = texts[0].description
    return is_hate_speech_internal(detected_text)

@app.post("/youtube")
def upload_youtube(text: str = Form(...)):
    output = f"/tmp/{uuid.uuid4()}.wav"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/temp_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text])

    audio_path = "/tmp/temp_audio.wav"
    AudioSegment.from_file(audio_path).set_channels(1).set_frame_rate(16000).export(output, format="wav")

    gcs_uri = upload_to_gcs(output, os.path.basename(output))
    transcript = transcribe(gcs_uri)

    os.remove(output)
    os.remove(audio_path)

    return is_hate_speech_internal(transcript)
