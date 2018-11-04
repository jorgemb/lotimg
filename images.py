# -*- coding: utf-8 -*-
import os

from PIL import Image


class Images:
    def __init__(self, infile):
        self.photoPath = infile
        self.photoName = os.path.split(infile)[0]
        self.format = os.path.splitext(infile)[1]

        try:
            self.image = Image.open(infile)
            self.isOpen = True
        except IOError:
            self.isOpen = False

    def is_valid(self):
        return self.isOpen

    def change_format(self, new_format):
        if not self.is_valid():
            return False

        self.format = "." + new_format
        return True

    def change_size(self, x, y):
        if not self.is_valid():
            return False

        if x < 0 or y < 0:
            return False

        old_size = self.image.size

        if x == 0:
            x = old_size[0]
        if y == 0:
            y = old_size[1]

        img = self.image.resize((x, y), Image.ANTIALIAS)
        self.image = img
        return True

    def save(self, directory, name):
        if not self.is_valid():
            return False
        if len(directory) == 0:
            return False

        # Save
        path = os.path.join(directory, name + self.format)
        try:
            self.image.save(path)
            return True
        except IOError:
            return False

    # TODO: Make rotation and rolling transformations
    """
    def Rotation (degrees):
        import Image
        outfile="90"+self.photo
        if self.photo!=outfile:
            try:
                (Image.open(self.photo).rotate(degrees)).save(outfile)
            except IOError:
                print "No sepuede crear una imagen desde: ", self.photo
        else:
            print "Ya existe una imagen con el mismo nombre y extension"
    """

    """
    def RollImages(image,delta):
        import Image
        delt=str(delta)
        infile=image
        outfile="Move"+delt+image
        def roll(image,delta):
            image=Image.open(image)
            xsize,ysize=image.size
            delta=delta % xsize
            if delta==0: return image
            part1=image.crop((0,0,delta,ysize))
            part2=image.crop((delta,0,xsize,ysize))
            image.paste(part2,(0,0,xsize-delta,ysize))
            image.paste(part1,(xsize-delta, 0, xsize, ysize))
            return image
        if infile!=outfile:
            try:
                (roll(image,delta)).save(outfile)
            except IOError:
                print "No sepuede crear una imagen desde: ", infile
        else:
            print "Ya existe una imagen con el mismo nombre y extension"
    """
