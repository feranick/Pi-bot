from PIL import Image
import numpy as np
import sys, time
import picamera


def init_camera(size):
    camera = picamera.PiCamera()
    camera.resolution = size
    camera.vflip = True
    camera.hflip = True
    return camera

def get_image(camera, size):
    resized_size = (10,10)
    output = np.empty((size[0],size[1],3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    print(output.shape)
    img = Image.fromarray(output).convert('L')
    img_resized = img.resize(resized_size, Image.ANTIALIAS)
    data = np.asarray( img_resized, dtype="int32" )
    print(data.shape)
     return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )

size = (768, 768)
camera = init_camera(size)
while True:
    data = get_image(camera, size)
    #time.sleep(1)
    print(data)

