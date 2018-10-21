# -*- coding: cp1252 -*-
##############################################################
# Imagenes.py
# Autores:
#   - Jorge Luis Martínez
# Este módulo contiene las funciones básicas convertir y
# modificar las imágenes individuales del usuario.
# Fecha de creacion: 8 de mayo del 2011
##############################################################

import os, sys
import Image

class Imagenes():
    
    def __init__(self,infile):
        self.photoPath = infile
        self.photoName = os.path.split( infile )[0]
        self.format = os.path.splitext( infile )[1]

        # Trata de abrir la imagen
        try:
            self.image = Image.open( infile )
            self.isOpen = True
        except IOError:
            self.isOpen = False

    def isValid( self ):
        return self.isOpen
        
        
    def FormatChanger(self,formato):
        # Validar
        if( not self.isValid() ):
            return False

        self.format = "." + formato
        return True
    
    def SizeChanger(self, x,y ):
        # Validar
        if( not self.isValid() ):
            return False

        if( x < 0 or y < 0 ):
            return False

        # Cambiar tamano
        oldSize = self.image.size
        # ..si alguno de los argumentos es cero, utilizar el tamano
        # que tenia la imagen
        if( x == 0 ):
            x = oldSize[0]
        if( y == 0 ):
            y = oldSize[1]
        
        img = self.image.resize( (x, y), Image.ANTIALIAS )
        self.image = img
        return True

    def Save( self, directory, name ):
        # Validar
        if( not self.isValid() ):
            return False
        if( len(directory) == 0 ):
            return False

        # Guardar
        path = os.path.join( directory, name + self.format )

        try:
            self.image.save( path )
            return True
        except IOError:
            return False

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
        
