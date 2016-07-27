import time
import struct
import base64
import cv2

pipe = open(r'\\.\pipe\XimeaPipe', 'r+b', 0)
number_of_images = struct.unpack('I', pipe.read(4))[0]
print number_of_images
for count in range(number_of_images):
    image_length = struct.unpack('I', pipe.read(4))[0]
    pipe_input = pipe.read(image_length)
    pipe.seek(0)
    imgdata = base64.b64decode(pipe_input)
    with open('some_image{}.jpg'.format(count), 'wb') as f:
        f.write(imgdata)