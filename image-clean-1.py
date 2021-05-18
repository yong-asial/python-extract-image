import pytesseract
import os

image_directory = 'image'
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
THRESHOLD = 100 # threshold (text len in an image) to include image to training
previous_extracted_text = ''

def extract_text(image_path):
  text = pytesseract.image_to_string(image_path)
  text = ' '.join(text.split())
  return text

def remove_file(file):
  try:
    os.remove(file)
  except OSError as e:  ## if failed, report it back to the user ##
    print ("Error: %s - %s." % (e.filename, e.strerror))

print('start cleanup process')
for image_filename in sorted(os.listdir(image_directory)):
  if not (image_filename.endswith(".jpg") or image_filename.endswith(".png")):
    continue
  file_path = os.path.join(image_directory, image_filename)
  text = extract_text(file_path)
  if len(text) > THRESHOLD:
    if text == previous_extracted_text:
      remove_file(file_path)
      continue
    previous_extracted_text = text
  else:
    remove_file(file_path)

print('finish cleanup process')