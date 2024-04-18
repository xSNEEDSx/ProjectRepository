# ReverbTime 0

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sample_rate, data = wavfile.read("enter file")
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))


# select a frequency under 1kHz
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
        return x


def frequency_check():
    # identity a frequency to check
    # print(freqs)
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    frequency_index = np.where(freqs == target_frequency)[0][0]
    # find sound data for a particular frequency
    frequency_data = spectrum[frequency_index]
    # change digital signal for a values in decibels
    data_in_db_fun = 10 * np.log10(frequency_data)
    return data_in_db_fun


data_in_db = frequency_check()

# Plot stuff
plt.figure(2)
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')

# Find index of max value
max_index = np.argmax(data_in_db)
max_value = data_in_db[max_index]
plt.plot(t[max_index], data_in_db[max_index], 'go')

# Slice our array from max value
sliced_array = data_in_db[max_index:]
max_value_5_less = max_value - 5


# Find nearest value less than 5 decibels
def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


max_value_5_less = find_nearest_value(sliced_array, max_value_5_less)
max_index_5_less = np.where(data_in_db == max_value_5_less)
plt.plot(t[max_value_5_less], data_in_db[max_value_5_less], 'yo')

# Slice array from max-5db
max_value_25_less = max_value - 25
max_value_25_less = find_nearest_value(sliced_array, max_value_25_less)
max_index_25_less = np.where(data_in_db == max_value_25_less)
plt.plot(t[max_index_25_less], data_in_db[max_index_25_less], 'ro')

rt20 = (t[max_index_5_less] - t[max_index_25_less])[0]
# Print(f'rt20 = {rt20}')
rt60 = 3 * rt20
# plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
plt.grid()

plt.show()

print(f'The RT60 reverb time at freq {int(target_frequency)} Hz is {round(abs(rt60), 2)} seconds')
