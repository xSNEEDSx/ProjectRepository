# ReverbTime 0

import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.utils import mediainfo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sample_rate, data = wavfile.read('Aula Magna Reverb.wav')
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


def debugg(fstring):
    print(fstring)


selection = "high"


def rt60_threshold(selection):
    if selection == "low":
        return 100
    if selection == "mid":
        return 1000
    if selection == "high":
        return 5000


def find_target_frequency(freqs, selection):
    threshold = rt60_threshold(selection)
    for x in freqs:
        if x > threshold:
            break
    return x


def frequency_check():
    debugg(f'freqs {freqs[:10]}')
    target_frequency = find_target_frequency(freqs, selection)
    debugg(f'target_frequency {target_frequency}')
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    debugg(f'index_of_frequency {index_of_frequency}')

    data_for_frequency = spectrum[index_of_frequency]
    debugg(f'data_for_frequency {data_for_frequency[:10]}')

    # change a digital signal for a values in decibels

    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


data_in_db = frequency_check()
plt.figure()

plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB')

print("Values of t:", t)
print("Values of data_in_db:", data_in_db)

index_of_max = np.argmax(data_in_db)

value_of_max = data_in_db[index_of_max]

plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

sliced_array = data_in_db[index_of_max:]

value_of_max_less_5 = value_of_max - 5

# Find highest resonance frequency excluding 0 Hz
highest_resonance_index = np.argmax(spectrum[index_of_max:]) + index_of_max
if highest_resonance_index < len(freqs):
    highest_resonance_freq = freqs[highest_resonance_index]
else:
    highest_resonance_freq = 0  # Default value if index is out of bounds


def find_nearest_value(array, value):
    array = np.asarray(array)
    debugg(f'array {array[:10]}')
    idx = (np.abs(array - value)).argmin()
    debugg(f'idx {idx}')
    debugg(f'array[idx] {array[idx]}')
    return array[idx]


value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
rt60 = rt20 * 3

plt.grid()
plt.show()

print(f'The RT60 reverb time is {round(abs(rt60), 2)} seconds')


class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.canvas.grid(row=1, column=0, sticky="news")

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky="news")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((5, 5), window=self.frame, anchor="nw")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# GUI Class
class ReverbTimeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Reverb Time GUI")
        self.master.geometry('1600x1200')
        self.master.resizable(True, True)

        self.scrollable_frame = ScrollableFrame(self.master)
        self.scrollable_frame.grid(row=8, column=0, rowspan=5, columnspan=3, padx=0, pady=0, sticky='news')
        self.scrollable_frame.canvas.config(width=1250, height=500)

        # Create a frame for each plot
        self.free_frame = tk.Frame(self.scrollable_frame.frame)
        self.free_frame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

        self.rt60_low_plot_frame = tk.Frame(self.scrollable_frame.frame)
        self.rt60_low_plot_frame.grid(row=1, column=1, padx=10, pady=10, sticky='news')

        self.rt60_mid_plot_frame = tk.Frame(self.scrollable_frame.frame)
        self.rt60_mid_plot_frame.grid(row=2, column=0, padx=10, pady=10, sticky='news')

        self.rt60_high_plot_frame = tk.Frame(self.scrollable_frame.frame)
        self.rt60_high_plot_frame.grid(row=2, column=1, padx=10, pady=10, sticky='news')

        self.rt60_combined_frame = tk.Frame(self.scrollable_frame.frame)
        self.rt60_combined_frame.grid(row=3, column=0, padx=10, pady=10, sticky='news')

        self.plot_frame = tk.Frame(self.scrollable_frame.frame)
        self.plot_frame.grid(row=3, column=1, padx=10, pady=10, sticky='news')

        # Frequency change buttons
        self.low_freq_button = tk.Button(self.master, text="Low Frequency", command=lambda: self.update_plots("low"))
        self.low_freq_button.grid(row=0, column=1, padx=(199, 1600), sticky='n')
        self.mid_freq_button = tk.Button(self.master, text="Mid Frequency", command=lambda: self.update_plots("mid"))
        self.mid_freq_button.grid(row=0, column=1, padx=(198, 1400), sticky='n')
        self.high_freq_button = tk.Button(self.master, text="High Frequency", command=lambda: self.update_plots("high"))
        self.high_freq_button.grid(row=0, column=1, padx=(202, 1200), sticky='n')

        # Create empty plot for spectrogram
        self.plot_empty(self.plot_frame, title="Spectrogram")

        # Create empty plots for RT60 values
        self.plot_empty(self.free_frame, title="Waveform")
        self.plot_empty(self.rt60_low_plot_frame, title="Low Frequencies")
        self.plot_empty(self.rt60_mid_plot_frame, title="Mid Frequencies")
        self.plot_empty(self.rt60_high_plot_frame, title="High Frequencies")
        self.plot_empty(self.rt60_combined_frame, title="Combined Frequencies")

        # Button to load file
        self.load_btn = tk.Button(self.master, text='Load File', command=self.load_file)
        self.load_btn.grid(row=0, column=0, sticky='w', padx=5)

        # Display the name of the file selected
        self.load_field = tk.StringVar()
        self.load_field.set("Loaded File... ")
        self.load_field_frame = tk.Entry(self.master, width=60, textvariable=self.load_field)
        self.load_field_frame.grid(row=0, column=0, sticky='w', padx=80)

        # Display file conversion status
        self.load_conversion_to_wav = tk.StringVar()
        self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
        self.load_conversion_to_wav_label = tk.Label(self.master, textvariable=self.load_conversion_to_wav)
        self.load_conversion_to_wav_label.grid(row=3, column=0, columnspan=1, sticky='w', padx=5)

        # Display channel conversion status
        self.load_conversion_to_mono = tk.StringVar()
        self.load_conversion_to_mono.set("Mono Conversion: No conversion necessary")
        self.load_conversion_to_mono_label = tk.Label(self.master, textvariable=self.load_conversion_to_mono)
        self.load_conversion_to_mono_label.grid(row=4, column=0, columnspan=1, sticky='w', padx=5)

        # Display initial file
        self.load_initial_file = tk.StringVar()
        self.load_initial_file.set("Initial File: None")
        self.load_initial_file_label = tk.Label(self.master, textvariable=self.load_initial_file)
        self.load_initial_file_label.grid(row=1, column=0, columnspan=1, sticky='w', padx=5)

        # Display initial channel count
        self.load_initial_channel = tk.StringVar()
        self.load_initial_channel.set("Initial Channel Count: None")
        self.load_initial_channel_label = tk.Label(self.master, textvariable=self.load_initial_channel)
        self.load_initial_channel_label.grid(row=2, column=0, columnspan=1, sticky='w', padx=5)

        # Display metadata (duration)
        self.load_duration = tk.StringVar()
        self.load_duration.set("Duration: None")
        self.load_duration_label = tk.Label(self.master, textvariable=self.load_duration)
        self.load_duration_label.grid(row=1, column=1, columnspan=1, sticky='w', padx=5)

        # Display metadata (artist)
        self.load_artist = tk.StringVar()
        self.load_artist.set("Artist: None")
        self.load_artist_label = tk.Label(self.master, textvariable=self.load_artist)
        self.load_artist_label.grid(row=2, column=1, columnspan=1, sticky='w', padx=5)

        # Display metadata (title)
        self.load_title = tk.StringVar()
        self.load_title.set("Title: None")
        self.load_title_label = tk.Label(self.master, textvariable=self.load_title)
        self.load_title_label.grid(row=3, column=1, columnspan=1, sticky='w', padx=5)

        # Display metadata (album)
        self.load_album = tk.StringVar()
        self.load_album.set("Album: None")
        self.load_album_label = tk.Label(self.master, textvariable=self.load_album)
        self.load_album_label.grid(row=4, column=1, columnspan=1, sticky='w', padx=5)

        # Display metadata (genre)
        self.load_genre = tk.StringVar()
        self.load_genre.set("Genre: None")
        self.load_genre_label = tk.Label(self.master, textvariable=self.load_genre)
        self.load_genre_label.grid(row=5, column=1, columnspan=1, sticky='w', padx=5)

        # Display metadata (date)
        self.load_year = tk.StringVar()
        self.load_year.set("Year: None")
        self.load_year_label = tk.Label(self.master, textvariable=self.load_year)
        self.load_year_label.grid(row=6, column=1, columnspan=1, sticky='w', padx=5)

        # Display frequency of highest resonance
        self.hz_highest = tk.StringVar()
        self.hz_highest.set("Frequency of Highest Resonance: None")
        self.hz_highest_label = tk.Label(self.master, textvariable=self.hz_highest)
        self.hz_highest_label.grid(row=5, column=0, columnspan=1, sticky='w', padx=5)

        # (Extra Credit) Button that alternates through the plots rather than displaying all 3 simultaneously

        # Button to combine the 3 plots into one

        # Button for significant statistics

    # Function to create empty plots using grid
    def plot_empty(self, plot_frame, title=None):
        fig, ax = plt.subplots(figsize=(6, 4.2))
        if title:
            ax.set_title(title)
        ax.set_xlabel("X Label")
        ax.set_ylabel("Y Label")
        ax.grid()

        # Embed the plot in the plot_frame
        plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().grid(row=0, column=0, sticky='news', padx=10, pady=10)

    def plot(self, plot_frame, data=None, sample_rate=None, t=None, data_in_db_fun=None, title=None):
        fig, ax = plt.subplots(figsize=(6, 4.2))
        if data is not None and sample_rate is not None and t is not None and data_in_db_fun is not None:
            ax.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
        else:
            ax.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Power (dB)")
            print("Values of t:", t)
            print("Values of data_in_db:", data_in_db)

        if title is None:
            title = "Plot"
        ax.set_title(title)
        ax.grid()

        # Clear previous plot in the plot_frame
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Embed the plot in the plot_frame using grid layout
        plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().grid(row=0, column=0, sticky='news', padx=10, pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("WAV files",
                                                                                                        "*.wav"), (
                                                                                                       "MP3 files",
                                                                                                       "*.mp3"), (
                                                                                                       "AAC files",
                                                                                                       "*.aac"), (
                                                                                                       "All files",
                                                                                                       "*.*")))
        if file_path:
            self.process_file(file_path)

    def convert_to_wav(self, file_path):
        # Destination file path for WAV
        print("Converting", file_path, "to WAV...")
        destination = os.path.splitext(file_path)[0] + ".wav"

        # Load the audio file
        sound = AudioSegment.from_file(file_path)

        # Debug: Print out the properties of the AudioSegment object before export
        print("Channels:", sound.channels)
        print("Sample width (bytes):", sound.sample_width)
        print("Frame rate (Hz):", sound.frame_rate)

        # Export the audio to WAV format
        sound.export(destination, format="wav")

        print("Conversion complete.")

        # Check if the destination file exists
        if os.path.exists(destination):
            return destination, sound.channels == 2
        else:
            return None, None

    def process_file(self, file_path):
        # Check if conversion to WAV is necessary
        if not file_path.lower().endswith('.wav'):
            converted_file_path, convert_to_mono = self.convert_to_wav(file_path)
            if converted_file_path:
                file_path = converted_file_path  # Use the converted file path
                self.load_conversion_to_wav.set("WAV Conversion: File converted to WAV")
                self.load_initial_file.set("Initial File: MP3")
            else:
                self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
                self.load_initial_file.set("Initial File: WAV")
        else:
            convert_to_mono = False  # Assuming WAV file, so no conversion needed
            self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
            self.load_initial_file.set("Initial File: WAV")

        # Load the WAV file
        sample_rate, data = wavfile.read(file_path)

        # Check if the audio data is stereo
        if data.ndim == 2 and data.shape[1] == 2:
            # Convert stereo data to mono
            convert_to_mono = True

        # Numbers numbers
        sample_rate, data = wavfile.read(file_path)
        print(f"number of channels = {data.shape[len(data.shape) - 1]}")
        print(f'this is data shape {data.shape}')
        print(f"sample rate = {sample_rate}Hz")
        length = data.shape[0] / sample_rate
        print(f"length = {length}s")


        # Update conversion status for stereo to mono
        if convert_to_mono:
            self.load_conversion_to_mono.set("Mono Conversion: Stereo converted to mono")
            self.load_initial_channel.set("Initial Channel Count: 2")
        else:
            self.load_conversion_to_mono.set("Mono Conversion: No conversion necessary")
            self.load_initial_channel.set("Initial Channel Count: 1")

        # Extract metadata using pydub
        metadata = mediainfo(file_path)

        # Extract relevant metadata fields
        duration = metadata.get('duration', 'None')
        artist = metadata.get('artist', 'None')
        title = metadata.get('title', 'None')
        album = metadata.get('album', 'None')
        genre = metadata.get('genre', 'None')
        year = metadata.get('date', 'None')

        # Display metadata in the GUI
        self.load_duration.set(f"Duration: {duration} seconds")
        self.load_artist.set(f"Artist: {artist}")
        self.load_title.set(f"Title: {title}")
        self.load_album.set(f"Album: {album}")
        self.load_genre.set(f"Genre: {genre}")
        self.load_year.set(f"Year: {year}")

        # Display frequency of highest resonance
        self.hz_highest.set(f"Frequency of Highest Resonance: {highest_resonance_freq:.2f} Hz")

        # Update the plot for the spectrogram
        self.plot(self.plot_frame, data, sample_rate, t, data_in_db, title="Spectrogram")

        # Plot the [blank] frequency graph

        # Update the plot for RT60 value of low-frequencies
        self.plot(self.rt60_low_plot_frame, t, data_in_db, title="Low Frequencies RT60")


def main():
    root = tk.Tk()
    app = ReverbTimeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
