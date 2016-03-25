#####################
# PixelGram Backend #
#####################
#      resizr.py    #
#####################
#  Images with PIL  #
#####################

# includes
import json
import pprint
from PIL import Image

# Load device specs from json
with open('devices.json', 'r') as data_file:
    data = json.load(data_file)
    
print(data["devices"][0]["width"])

# Open image
uploaded_image = Image.open("testimg.jpg")

print(uploaded_image.format, uploaded_image.size) 
#print("")
resized_image = uploaded_image.resize([720, 1080]) #resizing image
resized_image.format = uploaded_image.format #keeping the same format as before, if this isnt done then it comes back none
print(resized_image.format, resized_image.size)
#resized_image.save("/home/pythondev/Development/PixelGram/newImageTest1.jpg")