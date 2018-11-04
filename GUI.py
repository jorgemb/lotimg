# -*- coding: cp1252 -*-
from tkinter import Frame, Menu, LabelFrame, N, S, Scrollbar, VERTICAL, StringVar, Listbox, EXTENDED, W, E, Button, \
    Canvas, SINGLE, Label, Entry, RIGHT, END, Radiobutton, IntVar, DISABLED, NORMAL, Tk
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText

from PIL import ImageTk

import tkDialog
from files import *
from images import *
import sys


class GUI(Frame):
    def __init__(self, resources, master=None):
        Frame.__init__(self, master)
        self.resources = resources

        # Tkinter objects
        self.model_initial_names = None
        self.model_final_names = None
        self.widget_initial_names = None
        self.widget_final_names = None
        self.canvas_view = None

        self.model_height = None
        self.model_width = None
        self.vcmd = None

        self.selected_format = None
        self.validate = None

        # Initialize tkinter
        self.grid()
        self.create_objects()

        self.last_directory = ""

        # Lists for image name handling
        self.image_files = list()
        self.image_names = list()
        self.new_image_names = list()
        self.directory = ""

        # Thumbnails
        self.last_view = ""

        # Rules
        self.rule = None
        self.user_rule = ""

    def create_objects(self):
        top = self.winfo_toplevel()

        # Menu
        menu_top = Menu(top)
        top["menu"] = menu_top

        menu_top.add_command(label="About...")

        # Image line
        form_general = Frame(self, padx=10, pady=10)
        form_general.grid(row=0, column=0)

        # Original names
        form_initial_data = LabelFrame(form_general, text="Images",
                                       padx=10, pady=5)
        form_initial_data.grid(column=0, row=0, rowspan=2, sticky=N + S)

        initial_scroll_y = Scrollbar(form_initial_data, orient=VERTICAL)
        initial_scroll_y.grid(column=2, row=0,
                              rowspan=5, sticky=N + S)

        self.model_initial_names = StringVar(self)
        self.widget_initial_names = Listbox(form_initial_data,
                                            height=27,
                                            width=35,
                                            activestyle="dotbox",
                                            listvariable=self.model_initial_names,
                                            selectmode=EXTENDED,
                                            yscrollcommand=initial_scroll_y.set)
        self.widget_initial_names.grid(column=0, row=0,
                                       rowspan=5, columnspan=2,
                                       sticky=N + S + W + E)

        initial_scroll_y["command"] = self.widget_initial_names.yview
        self.widget_initial_names.bind("<Double-Button-1>",
                                       self.select_name)
        self.widget_initial_names.bind("<<ListboxSelect>>",
                                       self.preview)

        button_up = Button(form_initial_data, image=self.resources["up"],
                           command=self.name_up)
        button_up.grid(column=3, row=1, sticky=N + S)

        button_down = Button(form_initial_data, image=self.resources["down"],
                             command=self.name_down)
        button_down.grid(column=3, row=3, sticky=N + S)

        button_add = Button(form_initial_data, image=self.resources["add"],
                            command=self.add_file_names)
        button_add.grid(column=0, row=5, sticky=W + E)

        button_delete = Button(form_initial_data, image=self.resources["delete"],
                               command=self.remove_file_names)
        button_delete.grid(column=1, row=5, sticky=W + E)

        # Preview
        form_preview = LabelFrame(form_general, text="Preview",
                                  padx=10, pady=5)
        form_preview.grid(column=1, row=0, columnspan=2,
                          sticky=N + S + W + E, padx=10)

        form_preliminary = Frame(form_preview)
        form_preliminary.grid(column=1, row=0, sticky=N + S + W + E)

        self.canvas_view = Canvas(form_preliminary, width=256, height=256,
                                  bg="white", cursor="crosshair")
        self.canvas_view.grid(sticky=N + S + W + E)

        # Final names
        form_final_names = Frame(form_preview)
        form_final_names.grid(column=2, row=0, sticky=N + S + W + E)

        final_scroll_y = Scrollbar(form_final_names)
        final_scroll_y.grid(column=1, row=0, sticky=N + S)

        self.model_final_names = StringVar()
        self.widget_final_names = Listbox(form_final_names,
                                          height=18,
                                          width=35,
                                          activestyle="dotbox",
                                          listvariable=self.model_final_names,
                                          selectmode=SINGLE,
                                          yscrollcommand=final_scroll_y.set)
        self.widget_final_names.grid(column=0, row=0, sticky=N + W + E)
        final_scroll_y["command"] = self.widget_final_names.yview

        self.widget_final_names.bind("<Double-Button-1>",
                                     self.select_name)
        self.widget_final_names.bind("<<ListboxSelect>>",
                                     self.preview)

        # Options line
        form_options = Frame(form_general)
        form_options.grid(row=1, column=1, columnspan=2,
                          sticky=E + W, padx=10)

        # ..dimensions
        self.model_width = StringVar()
        self.model_height = StringVar()
        form_dimensions = LabelFrame(form_options, text="Dimensions (0 = no change)", padx=10, pady=10)
        form_dimensions.grid(row=0, column=1, sticky=N + S + W + E, padx=5)
        self.vcmd = (form_dimensions.register(self.event_on_validate), "%S", "%P")

        label_width = Label(form_dimensions, text="Width")
        label_width.grid(column=0, row=1, sticky=W)

        entry_width = Entry(form_dimensions, validate="key",
                            validatecommand=self.vcmd,
                            textvariable=self.model_width,
                            justify=RIGHT)
        entry_width.grid(column=1, row=1, sticky=E + W)
        entry_width.insert(END, "0")

        label_height = Label(form_dimensions, text="Height")
        label_height.grid(column=0, row=2, sticky=W)

        entry_height = Entry(form_dimensions, validate="key",
                             validatecommand=self.vcmd,
                             textvariable=self.model_height,
                             justify=RIGHT)
        entry_height.grid(column=1, row=2, sticky=E + W)
        entry_height.insert(END, "0")

        # .. formats
        form_formats = LabelFrame(form_options, text="Formats", padx=10, pady=10)
        form_formats.grid(row=0, column=0, rowspan=2, sticky=N + S + E + W)

        formats = ["No change", "JPG", "GIF", "BMP", "PNG", "TIFF"]
        self.selected_format = StringVar(value="No change")

        for n in range(len(formats)):
            radio_format = Radiobutton(form_formats, text=formats[n],
                                       value=formats[n],
                                       variable=self.selected_format)
            radio_format.grid(row=n + 1, column=0, sticky=W)

        # .. name change
        self.validate = (form_dimensions.register(self.event_validate_rule), "%P")
        form_names = LabelFrame(form_options, text="Names",
                                padx=10, pady=10)
        form_names.grid(row=1, column=1, sticky=N + S + E + W,
                        padx=5)

        self.selected_name = IntVar(value=0)
        radio_nochange = Radiobutton(form_names, text="No change",
                                     value=0,
                                     variable=self.selected_name,
                                     command=self.rule_change)
        radio_nochange.grid(row=1, column=0, columnspan=2,
                            sticky=W)

        radio_name_only = Radiobutton(form_names, text="Nombre + N",
                                      value=1,
                                      variable=self.selected_name,
                                      command=self.rule_change)
        radio_name_only.grid(row=2, column=0, sticky=W)

        self.entry_name_only = Entry(form_names, width=10,
                                     validate="key",
                                     validatecommand=self.validate)
        self.entry_name_only.grid(row=2, column=1, sticky=W + E)

        radio_rule = Radiobutton(form_names, text="Rule",
                                 value=2,
                                 variable=self.selected_name,
                                 command=self.rule_change)
        radio_rule.grid(row=3, column=0, sticky=W)
        self.button_change = Button(form_names, text="Change",
                                    command=self.custom_rule)
        self.button_change.grid(row=3, column=1, sticky=W + E)

        self.entry_name_only["state"] = DISABLED
        self.button_change["state"] = DISABLED

        # ..directory
        form_directory = LabelFrame(form_options, text="Destination",
                                    padx=10, pady=10)
        form_directory.grid(row=0, column=2, sticky=N + S + W)

        button_directory = Button(form_directory,
                                  image=self.resources["dir"],
                                  command=self.choose_directory)
        button_directory.grid(row=0, column=0, sticky=N + S + E + W)

        self.label_selected_directory = Label(form_directory,
                                              text="<Directory not chosen>",
                                              width=25, anchor=W)
        self.label_selected_directory.grid(row=0, column=1, stick=W + E)

        # .. convert
        self.button_convert = Button(form_options,
                                     image=self.resources["convert_d"],
                                     state=DISABLED,
                                     height=91,
                                     command=self.convert_images)
        self.button_convert.grid(row=1, column=2, sticky=E + W + S)

    #### EVENTS ############################################

    def add_file_names(self):
        new_names = get_image_file_names(self, self.last_directory)

        if len(new_names) > 0:
            names = get_names_in_path(new_names)
            self.image_files.extend(new_names)
            self.image_names.extend(names)
            self.change_names()

            self.refresh_names()

            self.last_directory = os.path.split(new_names[0])[0]

    def remove_file_names(self):
        indices = self.widget_initial_names.curselection()
        while len(indices) > 0:
            ind = indices[0]
            self.widget_initial_names.delete(ind)
            self.image_files.pop(int(ind))
            self.image_names.pop(int(ind))
            indices = self.widget_initial_names.curselection()

        if self.last_view not in self.image_files:
            self.canvas_view.delete("Image")

        self.change_names()
        self.refresh_names(True)

    def name_up(self):
        indices = list(self.widget_initial_names.curselection())
        for n in range(len(indices)):
            indices[n] = int(indices[n])
        indices.sort()

        for n in range(len(indices)):
            idx = indices[n]
            if idx != 0 and idx - 1 not in indices:
                x = self.image_files.pop(idx)
                self.image_files.insert(idx - 1, x)

                indices[n] -= 1

        self.image_names = get_names_in_path(self.image_files)

        self.change_names()
        self.refresh_names()

        for n in indices:
            self.widget_initial_names.selection_set(n)

    def name_down(self):
        indices = list(self.widget_initial_names.curselection())
        for n in range(len(indices)):
            indices[n] = int(indices[n])
        indices.sort()
        indices = indices[::-1]

        total = len(self.image_files)

        for n in range(len(indices)):
            indices[n] = int(indices[n])
            idx = indices[n]
            if idx != total - 1 and idx + 1 not in indices:
                x = self.image_files.pop(idx)
                self.image_files.insert(idx + 1, x)

                indices[n] += 1

        self.image_names = get_names_in_path(self.image_files)

        self.change_names()
        self.refresh_names()

        for n in indices:
            self.widget_initial_names.selection_set(n)

    def change_names(self):
        # Apply name rule
        self.new_image_names = self.image_names[:]
        for n in range(len(self.new_image_names)):
            self.new_image_names[n] = os.path.splitext(self.new_image_names[n])[0]

        if self.rule is not None:
            self.new_image_names = change_names_with_rule(self.new_image_names, self.rule)[0]
        return True

    def select_name(self, e):
        indices = e.widget.curselection()
        if len(indices) > 0:
            ind = int(indices[-1])
            if e.widget == self.widget_initial_names:
                self.widget_final_names.selection_clear(0, END)
                self.widget_final_names.selection_set(ind)
                self.widget_final_names.see(ind)
            else:
                self.widget_initial_names.selection_clear(0, END)
                self.widget_initial_names.selection_set(ind)
                self.widget_initial_names.see(ind)

    def refresh_names(self, only_last=False):
        if not only_last:
            self.model_initial_names.set('')
            for n in self.image_names:
                self.widget_initial_names.insert(END, n)

        self.model_final_names.set('')
        for n in self.new_image_names:
            self.widget_final_names.insert(END, n)

    def preview(self, e):
        indices = e.widget.curselection()
        if len(indices) > 0:
            idx = int(indices[-1])
            if self.last_view == self.image_files[idx]:
                return
            else:
                self.last_view = self.image_files[idx]

            try:
                current_image = Image.open(self.image_files[idx])
                current_image.thumbnail((256, 256))
                self.photo = ImageTk.PhotoImage(current_image)

                self.canvas_view.delete("Image")
                self.canvas_view.create_image(128, 128, image=self.photo)
                self.canvas_view.addtag_all("Image")
            except:
                showerror("Error in preview",
                          "It was not possible to preview image: " + self.image_files[idx])

    def rule_change(self):
        n = self.selected_name.get()
        if n == 0:
            self.entry_name_only["state"] = DISABLED
            self.button_change["state"] = DISABLED
            self.rule = None
        elif n == 1:
            self.entry_name_only["state"] = NORMAL
            self.button_change["state"] = DISABLED
            self.rule = make_naming_rule(self.entry_name_only.get())
        elif n == 2:
            self.entry_name_only["state"] = DISABLED
            self.button_change["state"] = NORMAL

            self.custom_rule()

        self.change_names()
        self.refresh_names(True)

    def custom_rule(self):
        input_rule = AskRule(self, self.user_rule)
        if input_rule.result is not None:
            self.user_rule = input_rule.result
            rule = compile_rule(self.user_rule)
            if rule is None:
                showerror("Error - Rule",
                          "Compilation error")
            else:
                self.rule = rule

        self.change_names()
        self.refresh_names(True)

    def event_validate_rule(self, text):
        self.rule = make_naming_rule(text)
        self.change_names()
        self.refresh_names(True)
        return True

    def choose_directory(self):
        directory = get_save_directory()
        if directory != "":
            self.directory = directory
            if len(directory) > 25:
                directory = directory[0:5] + "..." + directory[-16:]
            self.label_selected_directory["text"] = directory

        if self.directory != "":
            self.button_convert["state"] = NORMAL
            self.button_convert["image"] = self.resources["convert"]
        else:
            self.button_convert["state"] = DISABLED
            self.button_convert["image"] = self.resources["convert_d"]

    def convert_images(self):
        if len(self.image_files) == 0:
            showinfo("No images",
                     "No images were selected.")
            return

        selected_format = self.selected_format.get()

        width = self.model_width.get()
        if width == "":
            width = 0
        else:
            width = int(width)

        height = self.model_height.get()
        if height == "":
            height = 0
        else:
            height = int(height)

        current_directory = self.directory

        for n in range(len(self.image_files)):
            path = self.image_files[n]
            name = self.new_image_names[n]
            name = os.path.splitext(name)[0]

            current_image = Images(path)
            if not current_image.is_valid():
                showerror("Error while converting",
                          "Unable to open image: " + path)
            else:
                if not (width == 0 and height == 0):
                    current_image.change_size(width, height)
                if selected_format != "No change":
                    current_image.change_format(selected_format)
                current_image.save(current_directory, name)

    def event_on_validate(self, modification, text):
        try:
            if len(text) > 5:
                return False

            n = int(modification)
            return True

        except ValueError:
            return False


class AskRule(tkDialog.Dialog):
    def __init__(self, parent, anterior):
        top = tkDialog.Dialog.__init__(self, parent,
                                       "Enter naming rule",
                                       anterior)
        self.text = None

    def body(self, master):
        self.text = ScrolledText(master,
                                 width=60,
                                 height=10)
        self.text.grid(sticky=N + W + E + S)
        self.text.insert(END, self.other)
        self.result = None

    def apply(self):
        self.result = self.text.get(1.0, END)


if __name__ == '__main__':
    root = Tk()
    root.title("lotimg - Image conversion tool")
    root.resizable(width=False, height=False)

    images = dict()

    try:
        resources = open("resources.dat")
        for linea in resources:
            linea = linea.strip()
            name, path = linea.split()
            img = Image.open(path)

            images[name] = ImageTk.PhotoImage(img)
    except:
        root.withdraw()
        showerror("Error while loading resource images",
                  "Unable to load image: " + path,
                  parent=root)
        root.destroy()
        sys.exit(-1)

    app = GUI(images, root)
    app.mainloop()
