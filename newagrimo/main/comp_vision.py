from google.cloud import vision
import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Tron\\Desktop\\SAQTA\\birge\\newagrimo\\main\\direct-mission-386119-fe2d509be625.json"

image_path = "../static/images/Untitled.jpg"

client = vision.ImageAnnotatorClient()

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

print('Texts:')
for text in texts:
    print(text.description)
