from clarifai.client import ClarifaiApi
import os
import json

os.environ["CLARIFAI_APP_ID"] = "-twKcoSu0xkRCq8HET2KifyNid-QTNIy19cafkUY"
os.environ["CLARIFAI_APP_SECRET"] = "6Q-aSKltdpmgmgWAFCuTtd2wm-oPrcGYutHWbAaX"

clarifai_api = ClarifaiApi() # assumes environment variables are set.
url = 'http://img05.deviantart.net/e789/i/2004/319/8/9/clenched_hand_by_hands_stock.jpg'
result = clarifai_api.tag_image_urls(url)

print(json.dumps(result, sort_keys=True, indent=2, separators=(',', ':')))
