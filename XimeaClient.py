import struct
import base64
import numpy

class XimeaClient:
    pipe = None
    pipe_name = 'XimeaPipe'
    image_direcoty = 'images'

    def __init__(self,values):
        self.pipe = open(r'\\.\pipe\{}'.format(self.pipe_name), 'r+b', 0)
        print 'opening {}...',format(r'\\.\pipe\{}'.format(self.pipe_name))
        self.pipe.write(numpy.uint32(values[0]))
        print 'sending {} {}'.format(self.pipe_name, values[1])
        self.pipe.write(numpy.uint32(values[1]))

    def get_image(self):
        image_length = struct.unpack('I', self.pipe.read(4))[0]
        pipe_input = self.pipe.read(image_length)
        self.pipe.seek(0)
        image = base64.b64decode(pipe_input)
        return image

    def save_image(self,imgdata,number):
        with open('{}\\rawXimeaimage{}.jpg'.format(self.image_direcoty, number), 'wb') as file:
            file.write(imgdata)

    def save_all_images(self,all_images):
        count = 0
        for image in all_images:
            self.save_image(image,count)

def main():
    try:
        client = XimeaClient(250,2);
        count = 0
        run = True
        while run:
            try:
                current_image = client.get_image()
                client.save_image(current_image,count)
                count+=1
            except struct.error as struct_err:
                print('Server Disconnected: ({})'.format(struct_err))
                run = False
    except IOError as io_err:
        print(io_err)

if __name__ == "__main__":
    main()