import os

directory = r'./video'
for filename in os.listdir(directory):
  print(filename)
  print(os.path.join(directory, filename))