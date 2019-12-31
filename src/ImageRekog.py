import pprint
import boto3

from PIL import Image, ImageDraw

rek = boto3.client('rekognition')
""":type: pyboto3.rekognition"""

with open('Avengers-Infinity.jpg', 'rb') as f:
    image_bytes = f.read()

# response = rek.detect_labels(
#     Image={
#         'Bytes': image_bytes
#     })
# pprint.pprint(response)

# response = rek.detect_faces(
#     Image={
#         'Bytes': image_bytes
#     },
#     Attributes=['ALL']
# )
# pprint.pprint(response)

response = rek.detect_text(
    Image={
        'Bytes': image_bytes
    }
)
pprint.pprint(response)
