# -*- coding: UTF-8 -*-

import os
import os.path
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askdirectory


def get_image_file_names(parent=None, initial_dir=""):
    """
    Asks the user to specify image files to convert.
    :param parent: TKinter interface
    :param initial_dir: Initial directory to be shown to the user.
    :return: List of files picked by the user
    """
    root = parent
    if parent is None:
        root = tkinter.Tk()
        root.withdraw()

    if initial_dir == "":
        initial_dir = os.path.expanduser("~")

    opts = {"parent": root,
            "filetypes": [("Imagenes", "*.jpg;*.bmp;*.gif;*.png;*.tiff;*.tga")],
            "initialdir": initial_dir}

    all_files = filedialog.askopenfilenames(**opts)

    if len(all_files) == 0:
        return []

    # No longer necessary to split file names
    # file_names = split_file_names(all_files)
    file_names = list(all_files)

    if parent is None:
        root.destroy()
        del root

    return file_names


def get_names_in_path(path_list):
    """
    Returns a list with the name of all the archives in a path.
    :param path_list: A path list, as returned by getFileNames
    :return: A name list
    """
    names = list()
    for path in path_list:
        name = os.path.split(path)[1]
        names.append(name)

    return names


def split_file_names(names):
    """
    Splits file names from the response given by the selection dialog.
    :param names: String with names separated with {}
    :return: List with paths as string
    """
    first = 0
    counter = 0
    names_list = list()

    for letter in names:
        if letter == "{":
            first = counter
        elif letter == "}":
            names_list.append(names[first + 1:counter])
        counter += 1

    return names_list


def get_save_directory(parent=None, initial_dir=""):
    """
    Asks the user to choose a directory where the converted images will be saved.
    :param parent: Tkinter parent
    :param initial_dir: Initial directory to show to the user.
    :return: String with the chosen directory.
    """
    root = parent
    if parent is None:
        root = tkinter.Tk()
        root.withdraw()

    if initial_dir == "":
        initial_dir = os.path.expanduser("~")

    opts = {"parent": root,
            "initialdir": initial_dir}

    directory = askdirectory(**opts)

    if parent is None:
        root.destroy()
        del root

    return directory


def change_names_with_rule(names, rule):
    """
    Changes the names list using the given rule, which is executed as Python code.
    :param names: List of original names
    :param rule: Rule to apply to each name
    :return: List with changed names
    """
    changed = 0
    if rule is None:
        return [], 0

    # Compile rule
    if isinstance(rule, str):
        try:
            rule = compile(rule, "<string>", "exec")
        except:
            print("changeNames - Bad rule")
            return [], changed

    # Apply rule to each name
    modified_names = names[:]
    for n in range(len(modified_names)):
        try:
            local_variables = {"name": modified_names[n], "n": n}
            # TODO: Define allowed builtins
            exec(rule, {"__builtins__": {'str': str, 'int': int}}, local_variables)

            # TODO: Add verifications in order to see if there's a name clash or blank names.
            modified_names[n] = local_variables["name"]
            changed += 1
        except Exception as e:
            # Any exception is logged
            # TODO: Log exception
            pass

    return modified_names, changed


def make_naming_rule(name, digits=4):
    """
    Compiles a new naming rule in the form: Name####
    :param name: Name to use
    :param digits: Amount of digits to use
    :return: Compiled rule
    """
    rule = "name = '%s' + str(n+1).zfill(%d)\n" % (str(name), digits)
    return compile_rule(rule)


def compile_rule(rule):
    """
    Compiles a rule in string format. Basically checks that is valid python format.
    :param rule:
    :return:
    """
    if len(rule) == 0:
        return None

    try:
        c_rule = compile(rule, "<string>", "exec")
        return c_rule
    except:
        return None
