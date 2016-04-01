#####################
# PixelGram Backend #
#####################
#      resizr.py    #
#####################
#  Images with PIL  #
#####################

import json, os

from PIL import Image

def ResizeForAll(fpath):
    availableDevices = []
    
    # Load device specs
    with open('devices.json', 'r') as data_file:
        json_obj = json.load(data_file)
    
    print("Image UUID: " + fpath)
    #print(json_obj["device"][0]["width"])

    # Open image
    uploaded_img = Image.open(fpath)
    print(uploaded_img.format, uploaded_img.size) 

    # Resize image to fit every device with a lower or equal resolution
    for i in json_obj['device']:
        if uploaded_img.size[0] >= i['width'] and uploaded_img.size[1] >= i['height']:
            
            print ("Processing for " + i['name'])

            # Resize to device
            resized_img = uploaded_img.resize((i['width'], i['height']))

            # Set file directory and create if needed
            save_dir = ("static/uploads/" + str(i['id']) + "/")
            print("Saving to: " + save_dir)
            
            if not os.path.exists(save_dir):
                try:
                    print("Creating folder " + save_dir)
                    os.makedirs(save_dir)
                except Exception as e:
                    print(e)
            # Save to file
            if not os.path.isfile(save_dir + os.path.basename(fpath)):
                try:
                    resized_img.save((save_dir + os.path.basename(fpath)), 'jpeg', quality=85)
                    availableDevices.append(i['id'])
                except Exception as e:
                    print(e)
            
    return availableDevices
        # Check if equal to the size of a device, only compress

        # Need an option for users to submit single deivce wallpapers