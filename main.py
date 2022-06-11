import os
import numpy as np
from PIL import Image
import sys
from scipy.ndimage.interpolation import rotate

class MyImage():

    def __init__(self, path = None):
        if path != None:
            with Image.open(path, 'r') as image:
                self.width = image.size[0]
                self.height = image.size[1]
                im_array = np.frombuffer(image.convert('L').tobytes(), dtype=np.uint8)
                self.pixel_array = im_array.reshape((self.height, self.width))
        else:
            self.width = 0
            self.height = 0

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def rotate(self, direction, angle):
        if direction == 'ccw':
            angle = - int(angle)
        angle = int(angle) % 360
        rotation_mode = int(angle) // 90
        if rotation_mode == 0:
            return self
        new_image = MyImage()
        if rotation_mode == 1:
            new_image.set_width(self.height)
            new_image.set_height(self.width)
            new_image.pixel_array = rotate(self.pixel_array, 270)
            return new_image
        if rotation_mode == 2:
            new_image.set_width(self.width)
            new_image.set_height(self.height)
            new_image.pixel_array = rotate(self.pixel_array, 180)
            return new_image
        if rotation_mode == 3:
            new_image.set_width(self.height)
            new_image.set_height(self.width)
            new_image.pixel_array = rotate(self.pixel_array, 90)
            return new_image
        return self

    def auto_rotate(self):
        top = 0.0
        right = 0.0
        bot = 0.0
        left = 0.0
        horizont = self.height // 2
        vertical = self.width // 2
        for y in range(horizont):
            for x in range(self.width):
                top += self.pixel_array[y][x]
                bot += self.pixel_array[-y - 1][x]
        for y in range(self.height):
            for x in range(vertical):
                left += self.pixel_array[y][x]
                right += self.pixel_array[y][-x - 1]
        max_intensity = max(left, right, top, bot)
        if left == max_intensity:
            return self.rotate('cw', 90)
        if right == max_intensity:
            return self.rotate('cw', 270)
        if top == max_intensity:
            return self
        return self.rotate('cw', 180)

    def mirror(self, axis):
        new_image = MyImage()
        if axis == 'h':
            new_image.set_height(self.height)
            new_image.set_width(self.width)
            new_image.pixel_array = self.pixel_array[::-1]
            return new_image
        if axis == 'v':
            new_image.set_width(self.width)
            new_image.set_height(self.height)
            new_image.pixel_array = self.pixel_array.transpose()[::-1].transpose()
            return new_image
        if axis == 'd':
            new_image.set_width(self.height)
            new_image.set_height(self.width)
            new_image.pixel_array = self.pixel_array.transpose()
            return new_image
        if axis == 'cd':
            new_image.set_width(self.height)
            new_image.set_height(self.width)
            new_image.pixel_array = self.pixel_array[::-1].transpose()[::-1]
            return new_image

    def extract(self, left, top, width, height):
        new_image = MyImage()
        new_image.set_width(width)
        new_image.set_height(height)
        if top < 0:
            self.pixel_array = np.pad(self.pixel_array, ((-top, 0), (0,0)))
        if left < 0:
            self.pixel_array = np.pad(self.pixel_array, ((0, 0),(- left, 0)))
        if top + height > self.height:
            self.pixel_array = np.pad(self.pixel_array, ((0, top + height - self.height ), (0,0)))
        if left + width > self.width:
            self.pixel_array = np.pad(self.pixel_array, ((0, 0), (0, left + width - self.width)))
        new_image.pixel_array = self.pixel_array[max(top, 0):max(top, 0) + height, max(left, 0):max(left, 0) + width]
        return new_image

    def save(self, path):
        Image.frombuffer('L', (self.width, self.height), self.pixel_array.tobytes()).save(path)
        return self


if sys.argv[1] == 'mirror':
    image = MyImage(sys.argv[3])
    image.mirror(sys.argv[2]).save(sys.argv[4])
if sys.argv[1] == 'extract':
    image = MyImage(sys.argv[6])
    image = image.extract(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    image.save(sys.argv[7])
if sys.argv[1] == 'rotate':
    image = MyImage(sys.argv[4])
    image.save(sys.argv[5])
    image = image.rotate(sys.argv[2], sys.argv[3])
    image.save(sys.argv[5])
if sys.argv[1] == 'autorotate':
    image = MyImage(sys.argv[2])
    image = image.auto_rotate()
    image.save(sys.argv[3])
