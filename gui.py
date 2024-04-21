# gui.py

from tkinter import *
from tkinter import ttk, filedialog
from primary import *


# instance name is 'var'

# Make sure to file.close() when GUI closes

if __name__ == "__main__":  # adds logic
    _var = Tk()  # Tk class instance
    _var.title('Great Title')
    _var.geometry('640x480+300+300')
    _var.resizable(True, True)

    _structure = ttk.Frame(_var, padding= '5 5 5 5 ')
    _structure.grid(row=0, column=0, sticky='nesw')

    # Button to load file
    _load_btn = ttk.Button(_structure, text='Load File', command=ReverbTimeGUI.load_file)
    _load_btn.grid(row=0, column=1, sticky=W, padx=5)

    # Display the name of the file selected
    _load_field = StringVar()
    _load_field.set("Loaded File... ")
    _load_field_frame = ttk.Entry(_structure, width= 60, textvariable=_load_field)
    _load_field_frame.grid(row=0, column=2, sticky=E, padx=5)

    # (popup?) state conversion to .wav

    # Display waveform

    # Display frequency of highest resonance (Hz_highest)

    # Display Low, Med & High plots seperatly

    # (Extra Credit) Button that alternates thru the plots rather than displaying all 3 simultaneously

    # Button to combine the 3 plots into one

    # Button for significant statistics

    _var.mainloop()  # always listening for inputs


