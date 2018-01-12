from PIL import Image
import numpy as np
import sys
import picamera

def get_image():
    size = (768, 768)
    resized_size = (10,10)
    camera = picamera.PiCamera()
    camera.resolution = size
    camera.vflip = True
    camera.hflip = True
    output = np.empty((size[0],size[1],3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    camera.close()
    print(output.shape)
    img = Image.fromarray(output).convert('L')
    img_resized = img.resize(resized_size, Image.ANTIALIAS)
    data = np.asarray( img_resized, dtype="int32" )
    print(data.shape)
    #np.savetxt('test.out', data, fmt='%d')
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )

while True:
    data = get_image()
    print(data)

