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
        self.master.geometry('1600x1200')
        self.master.resizable(True, True)

        self.structure = tk.Frame(self.master)
        self.structure.grid(row=0, column=0, sticky='news')

        # Create a frame for each plot
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

        self.rt60_low_plot_frame = tk.Frame(self.master)
        self.rt60_low_plot_frame.grid(row=1, column=1, padx=10, pady=10, sticky='news')

        self.rt60_mid_plot_frame = tk.Frame(self.master)
        self.rt60_mid_plot_frame.grid(row=2, column=0, padx=10, pady=10, sticky='news')

        self.rt60_high_plot_frame = tk.Frame(self.master)
        self.rt60_high_plot_frame.grid(row=2, column=1, padx=10, pady=10, sticky='news')

        self.spectrogram_frame = tk.Frame(self.master)
        self.spectrogram_frame.grid(row=5, column=0, sticky='news')

        # Create empty plots for RT60 values
        self.plot_empty(self.rt60_low_plot_frame, title="Low Frequencies")
        self.plot_empty(self.rt60_mid_plot_frame, title="Mid Frequencies")
        self.plot_empty(self.rt60_high_plot_frame, title="High Frequencies")

        # Create empty plot for spectrogram
        self.plot_empty(self.plot_frame, title="Spectrogram")

        # Create a plot canvas for the original plot
        self.fig, self.ax = plt.subplots(figsize=(6, 4.2))
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().grid(row=0, column=0, sticky='news', padx=10, pady=10)

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

        # Display frequency of highest resonance
        self.hz_highest = tk.StringVar()
        self.hz_highest.set("Frequency of Highest Resonance: None")
        self.hz_highest_label = tk.Label(self.structure, textvariable=self.hz_highest)
        self.hz_highest_label.grid(row=5, column=1, columnspan=2, sticky='w', padx=5)

        # (Extra Credit) Button that alternates through the plots rather than displaying all 3 simultaneously

        # Button to combine the 3 plots into one

        # Button for significant statistics
