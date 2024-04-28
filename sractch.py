import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


wav_fname = filepath
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[len(data.shape) - 1]}")
print(f'this is data shape {data.shape}')
print(f"sample rate = {samplerate}Hz")
length = data.shape[0] / samplerate
print(f"length = {length}s")

time = np.linspace(0., length, data.shape[0])
plt.plot(time, data)
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()