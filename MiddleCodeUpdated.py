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
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

    # select a frequency under 1kHz
    # select a frequency under 1kHz
    def find_target_frequency(freqs):
        for x in freqs:
            if x > 1000:
                break
            return x

    def debugg(fstring):
        print(fstring)

    debugg(f'freqs {freqs[:10]}')
    target_frequency = find_target_frequency(freqs)

    frequency_index = np.where(freqs == target_frequency)[0][0]
    debugg(f'frequency_index {frequency_index}')

    # find sound data for a particular frequency
    frequency_data = spectrum[frequency_index]
    debugg(f'frequency_data {frequency_data[:10]}')

    # change digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(frequency_data + 1e-10)

    # Find index of max value
    max_index = np.argmax(data_in_db_fun)
    max_value = data_in_db_fun[max_index]
    plt.plot(t[max_index], data_in_db_fun[max_index], 'go')

    # Slice our array from max value
    sliced_array = data_in_db_fun[max_index:]
    max_value_5_less = max_value - 5

    # Find nearest value less than 5 decibels
    def find_nearest_value(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    max_value_5_less = find_nearest_value(sliced_array, max_value_5_less)
    max_index_5_less = np.where(data_in_db_fun == max_value_5_less)[0][0]  # Find index in data_in_db_fun

    # Slice array from max-5db
    max_value_25_less = max_value - 25
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
class ReverbTimeGUI: # Functions only rn
    def load_file(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("WAV files",
            "*.wav"), ("MP3 files", "*.mp3"),("AAC files", "*.aac"), ("All files", "*.*")))
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        # Check file type and convert if necessary
        if file_path.endswith('.wav'):
            converted_file_path = file_path
            channel_count = self.channel_count(file_path)
        else:
            # Convert to WAV
            converted_file_path = self.convert_to_wav(file_path)
            channel_count = self.channel_count(converted_file_path)

        # Read WAV file
        sample_rate, data = wavfile.read(converted_file_path)

        # Calculate reverb time
        target_frequency, rt60, t, data_in_db_fun, max_index, max_index_5_less, max_index_25_less = (
            calculate_reverb_time(data, sample_rate))

        # Show plots and text output
        self.show_output(target_frequency, rt60, t, data_in_db_fun, max_index, max_index_5_less, max_index_25_less,
                         data, sample_rate, channel_count)

    def channel_count(self, file_path):
        raw_audio = AudioSegment.from_file(file_path, format="wav")
        channel_count = raw_audio.channels
        print(channel_count)
        mono_wav = raw_audio.set_channels(1)
        mono_wav.export(f"{file_path} mono.wav", format="wav")
        mono_wav_audio = AudioSegment.from_file(f"{file_path} mono.wav", format="wav")
        channel_count = mono_wav_audio.channels
        print(channel_count)
        return channel_count

    def convert_to_wav(self, file_path):
        # Destination file path for WAV
        destination = "converted_file.wav"

        # Load the MP3 file
        sound = AudioSegment.from_mp3(file_path)

        # Export the MP3 file to WAV format
        sound.export(destination, format="wav")

        # Return the path of the converted WAV file
        return destination

    def show_output(self, target_frequency, rt60, t, data_in_db_fun, max_index, max_index_5_less, max_index_25_less,
                    data, sample_rate, channel_count):
        # Plotting the spectrogram and points of interest
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
        messagebox.showinfo("Channel Count", f"The channel count is {channel_count}")
def main():
    root = tk.Tk()
    app = ReverbTimeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()