import difflib
import base64
import io
from PIL import Image
import pytesseract

def search_discourse(query, data):
    ranked = sorted(data, key=lambda x: difflib.SequenceMatcher(None, query, x['content']).ratio(), reverse=True)
    return ranked[:5]

def extract_text_from_image(b64_img):
    img_data = base64.b64decode(b64_img)
    img = Image.open(io.BytesIO(img_data))
    return pytesseract.image_to_string(img)
