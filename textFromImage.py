from google.cloud import vision
from google.oauth2 import service_account
from google.cloud import vision

creds = service_account.Credentials.from_service_account_file("C:\\Users\\JA\\Desktop\\projekti\\hackaton\\bamboo-sweep-458718-t7-2c8cc2f20023.json")
client = vision.ImageAnnotatorClient(credentials=creds)

client = vision.ImageAnnotatorClient()

with open("image.webp","rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)

texts = response.text_annotations
if texts:
    print("Full text:", texts[0].description)
