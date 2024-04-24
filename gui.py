import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.utils import mediainfo

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

        # Display file conversion status
        self.load_conversion_to_wav = tk.StringVar()
        self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
        self.load_conversion_to_wav_label = tk.Label(self.structure, textvariable=self.load_conversion_to_wav)
        self.load_conversion_to_wav_label.grid(row=3, column=1, columnspan=2, sticky='w', padx=5)

        # Display channel conversion status
        self.load_conversion_to_mono = tk.StringVar()
        self.load_conversion_to_mono.set("Mono Conversion: No conversion necessary")
        self.load_conversion_to_mono_label = tk.Label(self.structure, textvariable=self.load_conversion_to_mono)
        self.load_conversion_to_mono_label.grid(row=4, column=1, columnspan=2, sticky='w', padx=5)

        # Display initial file
        self.load_initial_file = tk.StringVar()
        self.load_initial_file.set("Initial File: None")
        self.load_initial_file_label = tk.Label(self.structure, textvariable=self.load_initial_file)
        self.load_initial_file_label.grid(row=1, column=1, columnspan=2, sticky='w', padx=5)

        # Display initial channel count
        self.load_initial_channel = tk.StringVar()
        self.load_initial_channel.set("Initial Channel Count: None")
        self.load_initial_channel_label = tk.Label(self.structure, textvariable=self.load_initial_channel)
        self.load_initial_channel_label.grid(row=2, column=1, columnspan=2, sticky='w', padx=5)

        # Display metadata (duration)
        self.load_duration = tk.StringVar()
        self.load_duration.set("Duration: None")
        self.load_duration_label = tk.Label(self.structure, textvariable=self.load_duration)
        self.load_duration_label.grid(row=1, column=3, columnspan=2, sticky='w', padx=5)

        # Display metadata (artist)
        self.load_artist = tk.StringVar()
        self.load_artist.set("Artist: None")
        self.load_artist_label = tk.Label(self.structure, textvariable=self.load_artist)
        self.load_artist_label.grid(row=2, column=3, columnspan=2, sticky='w', padx=5)

        # Display metadata (title)
        self.load_title = tk.StringVar()
        self.load_title.set("Title: None")
        self.load_title_label = tk.Label(self.structure, textvariable=self.load_title)
        self.load_title_label.grid(row=3, column=3, columnspan=2, sticky='w', padx=5)

        # Display metadata (album)
        self.load_album = tk.StringVar()
        self.load_album.set("Album: None")
        self.load_album_label = tk.Label(self.structure, textvariable=self.load_album)
        self.load_album_label.grid(row=4, column=3, columnspan=2, sticky='w', padx=5)

        # Display metadata (genre)
        self.load_genre = tk.StringVar()
        self.load_genre.set("Genre: None")
        self.load_genre_label = tk.Label(self.structure, textvariable=self.load_genre)
        self.load_genre_label.grid(row=5, column=3, columnspan=2, sticky='w', padx=5)

        # Display metadata (date)
        self.load_year = tk.StringVar()
        self.load_year.set("Year: None")
        self.load_year_label = tk.Label(self.structure, textvariable=self.load_year)
        self.load_year_label.grid(row=6, column=3, columnspan=2, sticky='w', padx=5)

        # Display waveform

        # Display frequency of highest resonance (Hz_highest)

        # Display Low, Med & High plots separately

        # (Extra Credit) Button that alternates through the plots rather than displaying all 3 simultaneously

        # Button to combine the 3 plots into one

        # Button for significant statistics
