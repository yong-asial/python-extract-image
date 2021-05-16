import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
print(pytesseract.image_to_string(r'./data/videoqZg6k_0.jpg'))