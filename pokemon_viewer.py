# Importing the required libraries.
import poke_api
from tkinter import *
from tkinter import ttk
import os
import ctypes

# Path and the Directory of the script.
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# Creating new folder images in the same folder of the the script.
image_cache_dir = os.path.join(script_dir, 'images')


if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

# Create the main window
root = Tk()
root.title("Pokèmon Image Viewer")
root.minsize(600,700)


# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('pokemon_viewer')
icon_path = os.path.join(script_dir, 'Icon.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)

# creating a main frame 
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# First row -----> Pokemon Image.
img_poke = PhotoImage(file= os.path.join(script_dir, 'logo.png'))
lbl_poke_image = ttk.Label(frame, image=img_poke)
lbl_poke_image.grid(padx=10, pady=10)

# Second row -----> Selection bar for name of the Pokemon.
pokemone_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=pokemone_name_list, state='readonly')
cbox_poke_names.set('Select a Pokemon')
cbox_poke_names.grid(row=1,column=0,padx=10,pady=10)

# Changing the image on the screen according to the selected pokemon name.
def handle_pokemon_sel(event):
    
    pokemon_name = cbox_poke_names.get()
    global image_path
    image_path = poke_api.download_pokemon_artwork(pokemon_name=pokemon_name, save_dir=image_cache_dir)
    if image_path is not None:
        img_poke['file'] = image_path
cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)

# What to do when the set background button is clicked.
def handle_on_click():
    changeBG(image_path)
    return

# Third row -----> Button to set the desktop wallpaper of the selected pokemon.
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image' ,command=handle_on_click)
btn_set_desktop.grid(row=2,column=0,padx=10,pady=10)
btn_set_desktop.state(['disabled'])

# Enabling the button if user have selected a name  of the pokemon.
def enable_btn(event):
    if cbox_poke_names.get() is not 'Select a Pokemon':
        btn_set_desktop.state(['!disabled'])
cbox_poke_names.bind('<<ComboboxSelected>>', enable_btn)

# Function to change the background of the Desktop.
def changeBG(path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    return


root.mainloop()