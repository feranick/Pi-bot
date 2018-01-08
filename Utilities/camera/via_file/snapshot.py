from PIL import Image
import numpy as np
import sys
import picamera

def get_image(outname):
    camera = picamera.PiCamera()
    camera.resolution = (1024,768)
    camera.vflip = True
    camera.hflip = True
    camera.capture(outname, resize = (20,20))

def load_image( infilename ) :
    img = Image.open( infilename ).convert('L')
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )

get_image(sys.argv[1])
data = load_image(sys.argv[1])

print(data)

