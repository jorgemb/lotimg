# -*- coding: cp1252 -*-
##############################################################
# Archivos.py
# Autores:
#   - Jorge Luis Martínez
# Este módulo contiene las funciones básicas para interactuar
# con los archivos de imagenes.
# Fecha de creacion: 13 de mayo del 2011
##############################################################

import Tkinter, tkFileDialog
import os, os.path

# Pide al usuario que especifique los archivos de imagenes a convertir.
# Parametros: parent (interface de Tkinter), initial_dir (primer directorio
# que le muestra al usuario)
# Retorno: lista de archivos que escogio el usuario.
def getFileNames( parent = None, initial_dir = "" ):
    # Inicializar parametros si es necesario
    root = parent
    if( parent == None ):
        root = Tkinter.Tk()
        root.withdraw()

    if( initial_dir == "" ):
        initial_dir = os.path.expanduser("~")

    opts = { "parent":root,
             "filetypes":[("Imagenes", "*.jpg;*.bmp;*.gif;*.png;*.tiff;*.tga")],
             "initialdir":initial_dir }

    allFiles = tkFileDialog.askopenfilenames( **opts )

    if( len(allFiles) == 0 ):
        return []

    fileNames = splitFilenames( allFiles )

    # Finalizar parametros si es necesario
    if( parent == None ):
        root.destroy()
        del root

    return fileNames

# Esta funcion regresa una lista con los nombres de los archivos,
# dados los paths.
# Parametros: paths ( lista - devuelta por getFileNames )
# Retorno: lista de nombres de los archivos
def getNames( path_list ):
    names = list()
    for path in path_list:
        name = os.path.split( path )[1]
        names.append( name )

    return names

# Esta funcion separa los nombre de los archivos que se reciben del
# dialogo que utiliza el usuario para escoger las imagenes.
# Es de uso interno.
# Parametros: names( string con los archivos )
# Retorno: lista de archivos separados
def splitFilenames( names ):
    begin = 0
    cont = 0
    NamesList = list()

    for letter in names:
        if letter == unicode("{"):
            begin = cont
        elif letter == unicode( "}" ):
            NamesList.append( names[begin+1:cont] )
        cont += 1

    return NamesList


# Pide al usuario que escoja un directorio donde guardar los
# archivos.
# Parametros: parent (interface de Tkinter), initial_dir (directorio
# inicial que le muestra al usuario)
# Retorno: string con el directorio que se escogio
def getSaveDirectory( parent = None, initial_dir = "" ):
    # Inicializar parametros si es necesario
    root = parent
    if( parent == None ):
        root = Tkinter.Tk()
        root.withdraw()

    if( initial_dir == "" ):
        initial_dir = os.path.expanduser("~")

    opts = { "parent":root,
             "initialdir":initial_dir }

    directory = tkFileDialog.askdirectory( **opts )

    # Finalizar parametros si es necesario
    if( parent == None ):
        root.destroy()
        del root

    return directory


# Cambia los nombres de los archivos dados (en una lista) utilizando
# la regla dada, la cual es ejecutada como codigo de Python
# Parametros: names (lista con nombres), rule( string o codigo de Python
# compilado).
# Retorno: tupla con lista de los nombres cambiados y cuantos nombres se cambiaron
def changeNames( names, rule ):
    changed = 0
    if( rule == None ):
        return [], 0
    
    # Compilar la regla si es necesario
    if( isinstance( rule, str ) ):
        try:
            rule = compile( rule, "<string>", "exec" )
        except:
            print "changeNames - Bad rule"
            return [], changed

    # Aplicar la regla a cada nombre
    modNames = names[:]
    for n in range( len(modNames) ):
        try:
            locs = { "name":modNames[n], "n":n }
            exec rule in locs

            # TODO: Se pueden agregar algunos chequeos como: nombre valido, no muy largo, no igual a otro..."
            modNames[n] = locs["name"]
            changed += 1
        except:
            continue

    return modNames, changed

# Esta funcion crea una nueva regla utilizando los parametros de nombre
# que se dan, te tal forma que los archivos a cambiar utilizando la regla
# tengan el nombre 'Name0001'...
# Parametros: name (str)
# Retorno: regla compilada
def makeNamingRule( name ):
    # Validar
    if( len(name) == 0 ):
        return None

    rule = "name = '" + str(name) + "' + str(n+1).zfill(4)\n"
    return compileRule( rule )

# Esta funcion trata de compilar la regla que se da, en forma de string,
# la devuelve como un objeto compilado. Sirve para comprobar que una
# regla este bien escrita.
# Parametros: rule (str)
# Retorno: regla compilada
def compileRule( rule ):
    # Validar
    if( len(rule) == 0 ):
        return None

    try:
        c_rule = compile( rule, "<string>", "exec" )
        return c_rule
    except:
        return None
    

######################################
# DEBUG:
######################################
"""

root = Tkinter.Tk()
root.withdraw()


names = getFileNames( root)

print ""
print ""

directory = tkFileDialog.askdirectory( parent = root, mustexist = True )
print directory


nombres = list()

for nombre in names:
    path, fil = os.path.split( nombre )
    print "Archivo: ", fil
    print "Ruta: ", path
    name, ext = os.path.splitext( fil )
    print "Nombre: ", name
    print "Extension: ", ext
    print ""
    # nombres.append( fil )


modNombres = getNames( names )
print modNombres    

rule = makeNamingRule( "Nombre" )
print changeNames( modNombres, rule )

print getSaveDirectory( root )

root.destroy()
del root

"""
