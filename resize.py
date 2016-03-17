###################
# Images with PIL #
###################

# includes
from PIL import Image

uploaded_image = Image.open("imageTest1.jpg") #This will be the uploaded image

print("Image Test")
print(uploaded_image.format, uploaded_image.size) 
print("")
resized_image = uploaded_image.resize([720, 1080]) #resizing image
resized_image.format = uploaded_image.format #keeping the same format as before, if this isnt done then it comes back none
print(resized_image.format, resized_image.size)
resized_image.save("/home/pythondev/Development/PixelGram/newImageTest1.jpg")