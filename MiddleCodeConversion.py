# ReverbTime 0

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment


# Function for calculating reverb time
def calculate_reverb_time(data, sample_rate):
    # Reshape mono data if necessary
    if data.ndim == 1:
        data = np.reshape(data, (-1, 1))

    print("Input data shape:", data.shape)
    spectrum, freqs, t, im = plt.specgram(data[:, 0], Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

    # select a frequency under 1kHz
    def find_target_frequency(freqs):
        for x in freqs:
            if x > 1000:
                break
            return x

    target_frequency = find_target_frequency(freqs)
    frequency_index = np.where(freqs == target_frequency)[0][0]

    # find sound data for a particular frequency
    frequency_data = spectrum[frequency_index]

    # change digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(frequency_data + 1e-10)

    # Find index of max value
    max_index = np.argmax(data_in_db_fun)

    # Slice our array from max value
    sliced_array = data_in_db_fun[max_index:]
    max_value_5_less = data_in_db_fun[max_index] - 5

    # Find nearest value less than 5 decibels
    max_value_5_less = find_nearest_value(sliced_array, max_value_5_less)
    max_index_5_less = np.where(data_in_db_fun == max_value_5_less)[0][0]

    # Slice array from max-5db
    max_value_25_less = data_in_db_fun[max_index] - 25
    max_value_25_less = find_nearest_value(sliced_array, max_value_25_less)
    max_index_25_less = np.where(data_in_db_fun == max_value_25_less)[0][0]

    rt20 = t[max_index_5_less] - t[max_index_25_less]
    rt60 = 3 * rt20

    return target_frequency, abs(rt60), t, data_in_db_fun, max_index, max_index_5_less, max_index_25_less


# Helper function for finding nearest value
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


# GUI Class

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

    def process_file(self, file_path):
        # Check if conversion to WAV is necessary
        if not file_path.lower().endswith('.wav'):
            converted_file_path, convert_to_mono = self.convert_to_wav(file_path)
            if converted_file_path:
                file_path = converted_file_path  # Use the converted file path
                self.load_conversion_to_wav.set("WAV Conversion: File converted to WAV")
            else:
                self.load_conversion_to_wav.set("WAV Conversion: No conversion necessary")
        else:
            convert_to_mono = False  # Assuming WAV file, so no conversion needed

        # Load the WAV file
        sample_rate, data = wavfile.read(file_path)

        # Check if the audio data is stereo
        if data.ndim == 2 and data.shape[1] == 2:
            # Convert stereo data to mono
            convert_to_mono = True
            data = np.mean(data, axis=1)

        # Calculate reverb time using the data
        target_frequency, rt60, t, data_in_db_fun, max_index, max_index_5_less, max_index_25_less = calculate_reverb_time(
            data, sample_rate)

        # Plot the spectrogram and points of interest
        plt.figure()
        plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        plt.plot(t, data_in_db_fun, linewidth=1, alpha=0.7, color='#004bc6')
        plt.plot(t[max_index], data_in_db_fun[max_index], 'go')
        plt.plot(t[max_index_5_less], data_in_db_fun[max_index_5_less], 'yo')
        plt.plot(t[max_index_25_less], data_in_db_fun[max_index_25_less], 'ro')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        plt.grid()
        plt.show()

        # Display the RT60 value
        messagebox.showinfo("Reverb Time",
                            f"The RT60 reverb time at freq {int(target_frequency)} Hz is {round(rt60, 2)} seconds")

        # Update conversion status for stereo to mono
        if convert_to_mono:
            self.load_conversion_to_mono.set("Mono Conversion: Stereo converted to mono")
        else:
            self.load_conversion_to_mono.set("Mono Conversion: No conversion necessary")

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

    def convert_to_mono(self, file_path):
        # Load the audio file
        sound = AudioSegment.from_file(file_path)

        # Debug: Print out the properties of the AudioSegment object before conversion
        print("Before conversion - Channels:", sound.channels)

        # Convert stereo to mono if necessary
        if sound.channels == 2:
            sound = sound.set_channels(1)

            # Debug: Print out the properties of the AudioSegment object after conversion
            print("After conversion - Channels:", sound.channels)

            # Destination file path for the converted file
            destination = os.path.splitext(file_path)[0] + "_mono" + ".wav"

            # Export the audio to WAV format
            sound.export(destination, format="wav")

            return destination, True

        return file_path, False


def main():
    root = tk.Tk()
    app = ReverbTimeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
