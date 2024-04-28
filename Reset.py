# Reset.py
# The point of this new and hopefully final draft is to clean data and place the RT60 graph into the GUI

import tkinter as tk
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_empty(plot_frame, title=None):
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


def process(data):
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(data)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")

def load_file():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("WAV files",
                                                                                                    "*.wav"), (
                                                                                                       "MP3 files",
                                                                                                       "*.mp3"), (
                                                                                                       "AAC files",
                                                                                                       "*.aac"), (
                                                                                                       "All files",
                                                                                                       "*.*")))

    sample_rate, data = wavfile.read(file_path)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f'this is data shape {data.shape}')
    print(f"sample rate = {sample_rate}Hz")
    length = data.shape[0] / sample_rate
    print(f"length = {length}s")


class ReverbTimeGUI:
    def __init__(self, master):
        # initializing ReverbTimeGUI class
        self.master = master
        self.master.title("Reverb Time GUI")
        self.master.geometry('800x600')
        self.master.resizable(True, True)

        self.load_btn = tk.Button(self.master, text='Load File', command=load_file)
        self.load_btn.grid(row=0, column=0, sticky='w', padx=5)

        self.plot_frame = tk.Frame()
        self.plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky='news')

        plot_empty(self.plot_frame, title="Waveform")

    def getFile(self, filepath):
        return filepath

# Run GUI
def main():
    root = tk.Tk()
    app = ReverbTimeGUI(root)
    root.mainloop()

# Listen from GUI
if __name__ == "__main__":
    main()
