# -*- coding: cp1252 -*-
##############################################################
# Interfaz.py
# Autor: Jorge Luis Martínez
# Contiene las funciones de creación de la ventana y la lógica
# principal del aplicación.
# Fecha de creacion: 06 de junio del 2011
##############################################################

from Tkinter import *
from Archivos import *
from Imagenes import *
import Image
import ImageTk

from tkMessageBox import *
import sys

class Interfaz(Frame):
    def __init__( self,  recursos, master = None ):
        Frame.__init__( self, master )
        self.recursos = recursos
        
        self.grid()
        self.crearObjetos()

        self.lastdir = ""

        # Listas para manejar los nombres de las imagenes
        self.fileImagenes = list()
        self.nombreImagenes = list()
        self.nuevoImagenes = list()
        self.directorio = ""

        # Variables para manejar vistas previas
        self.ultimaVista = ""

        # Variables para manejar reglas
        self.regla = None
        self.reglaUsuario = ""


    def crearObjetos( self ):
        top = self.winfo_toplevel()
                
        # Menu
        mnuTodo = Menu( top )
        top["menu"] = mnuTodo

        mnuTodo.add_command( label = "Acerca de" )
        
        # Linea de imagenes
        frmGeneral = Frame( self, padx = 10, pady = 10 )
        frmGeneral.grid( row = 0, column = 0 )

        # ..Nombres originales
        frmIniciales = LabelFrame( frmGeneral, text = "Imágenes",
                                   padx = 10, pady = 5 )
        frmIniciales.grid( column = 0, row = 0, rowspan = 2, sticky = N+S )

        niScrollY = Scrollbar( frmIniciales, orient = VERTICAL )
        niScrollY.grid( column = 2, row = 0,
                        rowspan = 5, sticky = N+S )

        self.nombresIniciales = StringVar( self )
        self.lstNombresIniciales = Listbox( frmIniciales,
                                       height = 27,
                                       width = 35,
                                       activestyle = "dotbox",
                                       listvariable = self.nombresIniciales,
                                       selectmode = EXTENDED,
                                       yscrollcommand = niScrollY.set )
        self.lstNombresIniciales.grid( column = 0, row = 0,
                                  rowspan = 5, columnspan = 2,
                                  sticky = N+S+W+E )
        niScrollY["command"] = self.lstNombresIniciales.yview
        self.lstNombresIniciales.bind( "<Double-Button-1>",
                                       self.seleccionarNombre )
        self.lstNombresIniciales.bind( "<<ListboxSelect>>",
                                       self.vistaPrevia )

        btnSubir = Button( frmIniciales, image = self.recursos["up"],
                           command = self.subirNombre )
        btnSubir.grid( column = 3, row = 1, sticky = N+S )

        btnBajar = Button( frmIniciales, image = self.recursos["down"],
                           command = self.bajarNombre )
        btnBajar.grid( column = 3, row = 3, sticky = N+S )

        btnAgregar = Button( frmIniciales, image = self.recursos["add"],
                             command = self.agregarNombres )
        btnAgregar.grid( column = 0, row = 5, sticky = W+E )

        btnEliminar = Button( frmIniciales, image = self.recursos["delete"],
                              command = self.eliminarNombres )
        btnEliminar.grid( column = 1, row = 5, sticky = W+E )

        # ..Vista preliminar
        frmVistas = LabelFrame( frmGeneral, text = "Vista previa",
                                padx = 10, pady = 5 )
        frmVistas.grid( column = 1, row = 0, columnspan = 2,
                        sticky = N+S+W+E, padx = 10 )
        
        frmPreliminar = Frame( frmVistas )
        frmPreliminar.grid( column = 1, row = 0, sticky = N+S+W+E )

        self.cnvVista = Canvas( frmPreliminar, width = 256, height = 256,
                                bg = "white", cursor = "crosshair" )
        self.cnvVista.grid( sticky = N+S+W+E )

        # ..Nombres finales
        frmFinales = Frame( frmVistas )
        frmFinales.grid( column = 2, row = 0, sticky = N+S+W+E )

        nfScrollY = Scrollbar( frmFinales )
        nfScrollY.grid( column = 1, row = 0, sticky = N+S )

        self.nombresFinales = StringVar()
        self.lstNombresFinales = Listbox( frmFinales,
                                     height = 18,
                                     width = 35,
                                     activestyle = "dotbox",
                                     listvariable = self.nombresFinales,
                                     selectmode = SINGLE,
                                     yscrollcommand = nfScrollY.set )
        self.lstNombresFinales.grid( column = 0, row = 0, sticky = N+W+E )
        nfScrollY["command"] = self.lstNombresFinales.yview

        self.lstNombresFinales.bind( "<Double-Button-1>",
                                       self.seleccionarNombre )
        self.lstNombresFinales.bind( "<<ListboxSelect>>",
                                       self.vistaPrevia )


        # Linea de opciones
        frmOpciones = Frame( frmGeneral )
        frmOpciones.grid( row = 1, column = 1, columnspan = 2,
                          sticky = E+W, padx = 10 )

        # ..Dimensiones
        self.varAncho = StringVar()
        self.varAlto = StringVar()
        frmDimensiones = LabelFrame( frmOpciones,
                                     text = "Dimensiones (0 = sin cambio)",
                                     padx = 10, pady = 10 )
        frmDimensiones.grid( row = 0, column = 1, sticky = N+S+W+E,
                             padx = 5 )
        self.vcmd = ( frmDimensiones.register( self.Entry_onValidate ),
                      "%S", "%P" )

        lblAncho = Label( frmDimensiones, text = "Ancho" )
        lblAncho.grid( column = 0, row = 1, sticky = W )

        entAncho = Entry( frmDimensiones, validate = "key",
                               validatecommand = self.vcmd,
                               textvariable = self.varAncho,
                               justify = RIGHT )
        entAncho.grid( column = 1, row = 1, sticky = E+W )
        entAncho.insert( END, "0" )

        lblAlto = Label( frmDimensiones, text = "Alto" )
        lblAlto.grid( column = 0, row = 2, sticky = W )

        entAlto = Entry( frmDimensiones, validate = "key",
                         validatecommand = self.vcmd,
                         textvariable = self.varAlto,
                         justify = RIGHT )
        entAlto.grid( column = 1, row = 2, sticky = E+W )
        entAlto.insert( END, "0" )


        # ..Formatos
        frmFormatos = LabelFrame( frmOpciones, text = "Formatos",
                                  padx = 10, pady = 10 )
        frmFormatos.grid( row = 0, column = 0, rowspan = 2,
                          sticky = N+S+E+W )

        formatos = [ "Sin cambios", "JPG", "GIF", "BMP", "PNG", "TIFF" ]
        self.formatoElegido = StringVar( value = "Sin cambios" )

        for n in range( len(formatos) ):
            rbtFormato = Radiobutton( frmFormatos, text = formatos[n],
                                      value = formatos[n],
                                      variable = self.formatoElegido )
            rbtFormato.grid( row = n+1, column = 0, sticky = W )

        # ..Cambio nombre
        self.validar = ( frmDimensiones.register( self.Entry_reglaValidar ),
                         "%P" )
        frmNombre = LabelFrame( frmOpciones, text = "Nombres",
                                padx = 10, pady = 10 )
        frmNombre.grid( row = 1, column = 1, sticky = N+S+E+W,
                        padx = 5 )

        self.nombreElegido = IntVar( value = 0 )
        rbtSinCambio = Radiobutton( frmNombre, text = "Sin cambios",
                                    value = 0,
                                    variable = self.nombreElegido,
                                    command = self.reglaCambio )
        rbtSinCambio.grid( row = 1, column = 0, columnspan = 2,
                           sticky = W )



        rbtSoloNombre = Radiobutton( frmNombre, text = "Nombre + N",
                                     value = 1,
                                     variable = self.nombreElegido,
                                     command = self.reglaCambio )
        rbtSoloNombre.grid( row = 2, column = 0, sticky = W )
        
        self.entSoloNombre = Entry( frmNombre, width = 10,
                                    validate = "key",
                                    validatecommand = self.validar )
        self.entSoloNombre.grid( row = 2, column = 1, sticky = W+E )



        rbtRegla = Radiobutton( frmNombre, text = "Regla",
                                value = 2,
                                variable = self.nombreElegido,
                                command = self.reglaCambio )
        rbtRegla.grid( row = 3, column = 0, sticky = W )
        self.btnRegla = Button( frmNombre, text = "Cambiar",
                                command = self.reglaPersonalizada )
        self.btnRegla.grid( row = 3, column = 1, sticky = W+E )

        self.entSoloNombre["state"] = DISABLED
        self.btnRegla["state"] = DISABLED

        # ..Directorio
        frmDirectorio = LabelFrame( frmOpciones, text = "Directorio destino",
                                    padx = 10, pady = 10 )
        frmDirectorio.grid( row = 0, column = 2, sticky = N+S+W )

        btnDirectorio = Button( frmDirectorio,
                                     image = self.recursos["dir"],
                                     command = self.escogerDirectorio )
        btnDirectorio.grid( row = 0, column = 0, sticky = N+S+E+W )

        self.lblDirEscogido = Label( frmDirectorio,
                                     text = "<Directorio no elegido>",
                                     width = 25, anchor = W )
        self.lblDirEscogido.grid( row = 0, column = 1, stick = W+E )

        # ..Convertir
        self.btnConvertir = Button( frmOpciones,
                                    image = self.recursos["convertir_d"],
                                    state = DISABLED,
                                    height = 91,
                                    command = self.convertirImagenes )
        self.btnConvertir.grid( row = 1, column = 2, sticky = E+W+S )

    #### EVENTOS ############################################

    # Nombres (listbox)
    def agregarNombres( self ):
        # Pedir archivos
        nuevas = getFileNames( self, self.lastdir )

        if( len(nuevas) > 0 ):
            nombres = getNames( nuevas )
            self.fileImagenes.extend( nuevas )
            self.nombreImagenes.extend( nombres )
            self.cambiarNombres()
            
            self.refrescarNombres()

            self.lastdir = os.path.split( nuevas[0] )[0]


    def eliminarNombres( self ):
        indices = self.lstNombresIniciales.curselection()
        while( len(indices) > 0 ):
            ind = indices[0]
            self.lstNombresIniciales.delete( ind )
            self.fileImagenes.pop( int(ind) )
            self.nombreImagenes.pop( int(ind) )
            indices = self.lstNombresIniciales.curselection()

        if( self.ultimaVista not in self.fileImagenes ):
            self.cnvVista.delete( "Imagen" )

        self.cambiarNombres()
        self.refrescarNombres( True )

    def subirNombre( self ):
        indices = list( self.lstNombresIniciales.curselection() )
        for n in range( len(indices) ):
            indices[n] = int( indices[n] )
        indices.sort()

        
        for n in range( len(indices) ):
            ind = indices[n]
            if( ind != 0 and ind-1 not in indices ):
                x = self.fileImagenes.pop( ind )
                self.fileImagenes.insert( ind-1, x )

                indices[n] -= 1


        self.nombreImagenes = getNames( self.fileImagenes )

        self.cambiarNombres()
        self.refrescarNombres()

        for n in indices:
            self.lstNombresIniciales.selection_set(n)

    def bajarNombre( self ):
        indices = list( self.lstNombresIniciales.curselection() )
        for n in range( len(indices) ):
            indices[n] = int(indices[n])
        indices.sort()
        indices = indices[::-1]

        total = len( self.fileImagenes )
        
        for n in range( len(indices) ):
            indices[n] = int(indices[n])
            ind = indices[n]
            if( ind != total-1 and ind+1 not in indices ):
                x = self.fileImagenes.pop( ind )
                self.fileImagenes.insert( ind+1, x )

                indices[n] += 1


        self.nombreImagenes = getNames( self.fileImagenes )

        self.cambiarNombres()
        self.refrescarNombres()

        for n in indices:
            self.lstNombresIniciales.selection_set(n)
        

    def cambiarNombres( self ):
        # Aplica la regla de los nombres
        self.nuevoImagenes = self.nombreImagenes[:]
        for n in range( len(self.nuevoImagenes) ):
            self.nuevoImagenes[n] = os.path.splitext( self.nuevoImagenes[n] )[0]
            
        if( self.regla != None ):
            self.nuevoImagenes = changeNames( self.nuevoImagenes,
                                              self.regla )[0]
        return True

    def seleccionarNombre( self, e ):
        # Selecciona un nombre para vista previa
        indices = e.widget.curselection()
        if( len(indices) > 0 ):
            ind = int( indices[-1] )
            if( e.widget == self.lstNombresIniciales ):
                self.lstNombresFinales.selection_clear( 0, END )
                self.lstNombresFinales.selection_set( ind )
                self.lstNombresFinales.see( ind )
            else:
                self.lstNombresIniciales.selection_clear( 0, END )
                self.lstNombresIniciales.selection_set( ind )
                self.lstNombresIniciales.see( ind )

    def refrescarNombres( self, soloFinales = False ):
        # Llena los listbox de nombres con sus respectivas listas
        if( not soloFinales ):
            self.nombresIniciales.set( '' )
            for n in self.nombreImagenes:
                self.lstNombresIniciales.insert( END, n )
        
        self.nombresFinales.set( '' )
        for n in self.nuevoImagenes:
            self.lstNombresFinales.insert( END, n )

    def vistaPrevia( self, e ):
        indices = e.widget.curselection()
        if( len(indices) > 0 ):
            ind = int( indices[-1] )
            if( self.ultimaVista == self.fileImagenes[ind] ):
                return
            else:
                self.ultimaVista = self.fileImagenes[ind]
            
            try:
                imagen = Image.open( self.fileImagenes[ind] )
                imagen.thumbnail( (256,256) )
                self.photo = ImageTk.PhotoImage( imagen )

                self.cnvVista.delete( "Imagen" )
                self.cnvVista.create_image( 128, 128, image = self.photo )
                self.cnvVista.addtag_all( "Imagen" )
            except:
                showerror( "Error vista previa",
                           "No se pudo visualizar la imagen " +
                            self.fileImagenes[ind] )

    # Reglas (cambios)
    def reglaCambio( self ):
        n = self.nombreElegido.get()
        if( n == 0 ):
            self.entSoloNombre["state"] = DISABLED
            self.btnRegla["state"] = DISABLED
            self.regla = None
        elif( n == 1 ):
            self.entSoloNombre["state"] = NORMAL
            self.btnRegla["state"] = DISABLED
            self.regla = makeNamingRule( self.entSoloNombre.get() )
        elif( n == 2 ):
            self.entSoloNombre["state"] = DISABLED
            self.btnRegla["state"] = NORMAL
            
            self.reglaPersonalizada()


        # Refrescar los nombre finales de acuerdo a la seleccion
        self.cambiarNombres()
        self.refrescarNombres( True )

    def reglaPersonalizada( self ):
        # Muestra el dialogo para crear una nueva regla
        ingreso = PedirRegla( self, self.reglaUsuario )
        if( ingreso.result != None ):
            self.reglaUsuario = ingreso.result
            regla = compileRule( self.reglaUsuario )
            if( regla == None ):
                showerror( "Error - Regla",
                           "No se pudo compilar la regla ingresada" )
            else:
                self.regla = regla

        # Refrescar los nombre finales de acuerdo a la seleccion
        self.cambiarNombres()
        self.refrescarNombres( True )

    def Entry_reglaValidar( self, texto ):
        self.regla =  makeNamingRule( texto )
        self.cambiarNombres()
        self.refrescarNombres( True )
        return True

    # Directorio
    def escogerDirectorio( self ):
        directorio = getSaveDirectory()
        if( directorio != "" ):
            self.directorio = directorio
            if( len(directorio) > 25 ):
                directorio = directorio[0:5] + "..." + directorio[-16:]
            self.lblDirEscogido["text"] = directorio


        if( self.directorio != "" ):
            self.btnConvertir["state"] = NORMAL
            self.btnConvertir["image"] = self.recursos["convertir"]
        else:
            self.btnConvertir["state"] = DISABLED
            self.btnConvertir["image"] = self.recursos["convertir_d"]

    # Convertir
    def convertirImagenes( self ):
        if( len( self.fileImagenes ) == 0 ):
            showinfo( "No imágenes",
                      "No se seleccionó ninguna imagen para convertir" )
            return
        
        # Convertir todas las imágenes una a una
        formato = self.formatoElegido.get()
        
        ancho = self.varAncho.get()
        if( ancho == "" ):
            ancho = 0
        else:
            ancho = int(ancho)
            
        alto = self.varAlto.get()
        if( alto == "" ):
            alto = 0
        else:
            alto = int(alto)
            
        directorio = self.directorio
        
        for n in range( len( self.fileImagenes ) ):
            path = self.fileImagenes[n]
            nombre = self.nuevoImagenes[n]
            nombre = os.path.splitext( nombre )[0]

            n_imagen = Imagenes( path )
            if( not n_imagen.isValid() ):
                showerror( "Error convertir",
                           "No se pudo abrir la imagen " + path )
            else:
                if not ( ancho == 0 and alto == 0 ):
                    n_imagen.SizeChanger( ancho, alto )
                if( formato != "Sin cambios" ):
                    n_imagen.FormatChanger( formato )
                n_imagen.Save( directorio, nombre )            
            
        

    # Entries (int)
    def Entry_onValidate( self, modificacion, texto ):
        try:
            if( len(texto) > 5 ):
                return False
            
            n = int( modificacion )
            return True
        
        except ValueError:
            return False

import ScrolledText
import tkDialog
class PedirRegla( tkDialog.Dialog ):
    def __init__( self, parent, anterior ):
        top = tkDialog.Dialog.__init__( self, parent,
                                        "Ingrese código de nombrado" ,
                                        anterior )

    def body( self, master ):
        self.text = ScrolledText.ScrolledText( master,
                                          width = 60,
                                          height = 10 )
        self.text.grid( sticky = N+W+E+S )
        self.text.insert( END, self.other )
        self.result = None
        
    def apply( self ):
        self.result = self.text.get( 1.0, END )
        

# PROGRAMA PRINCIPAL ########################################
root = Tk()
root.title( "lotimg - Herramienta de conversión de imágenes" )
root.resizable( width = False, height = False )

# Cargar imagenes externas
imagenes = dict()

try:
    recursos = open( "resources.dat" )
    for linea in recursos:
        linea = linea.strip()
        nombre, path = linea.split()
        img = Image.open( path )
        
        imagenes[nombre] = ImageTk.PhotoImage( img )
except:
    root.withdraw()
    showerror( "Error al cargar imágenes",
               "No se pudo cargar la imagen: " + path,
               parent = root )
    root.destroy()
    sys.exit( -1 )

# Iniciar aplicacion
app = Interfaz( imagenes, root )
app.mainloop()
