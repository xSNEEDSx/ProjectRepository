import tkinter as tk
from tkinter import filedialog, messagebox

class ReverbTimeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Reverb Time GUI")
        self.master.geometry('640x200')
        self.master.resizable(True, True)

        self.structure = tk.Frame(self.master)
        self.structure.grid(row=0, column=0, sticky='nesw')

        # Button to load file
        self.load_btn = tk.Button(self.structure, text='Load File', command=self.load_file)
        self.load_btn.grid(row=0, column=1, sticky='w', padx=5)

        # Display the name of the file selected
        self.load_field = tk.StringVar()
        self.load_field.set("Loaded File... ")
        self.load_field_frame = tk.Entry(self.structure, width=60, textvariable=self.load_field)
        self.load_field_frame.grid(row=0, column=2, sticky='e', padx=5)

        # Display conversion status
        self.load_conversion_to_wav = tk.StringVar()
        self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
        self.load_conversion_to_wav_label = tk.Label(self.structure, textvariable=self.load_conversion_to_wav)
        self.load_conversion_to_wav_label.grid(row=1, column=1, columnspan=2, sticky='w', padx=5)

        self.load_conversion_to_mono = tk.StringVar()
        self.load_conversion_to_mono.set("Mono Conversion: No conversion necessary")
        self.load_conversion_to_mono_label = tk.Label(self.structure, textvariable=self.load_conversion_to_mono)
        self.load_conversion_to_mono_label.grid(row=2, column=1, columnspan=2, sticky='w', padx=5)

        # Display waveform

        # Display frequency of highest resonance (Hz_highest)

        # Display Low, Med & High plots separately

        # (Extra Credit) Button that alternates thru the plots rather than displaying all 3 simultaneously

        # Button to combine the 3 plots into one

        # Button for significant statistics
