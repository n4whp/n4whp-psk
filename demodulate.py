import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

# Function to read audio signal from WAV file
def read_wave(file_path):
    sample_rate, wave = read(file_path)
    wave = wave.astype(np.float32) / 32767.0  # Normalize to [-1, 1]
    return sample_rate, wave

# Function to demodulate the received signal
def demodulate_wave(signal, sample_rate, symbol_duration=0.005):  # 200 bps corresponds to 1/200 seconds
    num_symbols = int(len(signal) / (sample_rate * symbol_duration))
    bits = []

    # Generate time vector
    t = np.linspace(0, symbol_duration, int(sample_rate * symbol_duration), endpoint=False)

    for i in range(num_symbols):
        start = int(i * sample_rate * symbol_duration)
        end = int((i + 1) * sample_rate * symbol_duration)

        # Average amplitude to determine bit value
        amplitude = np.mean(np.abs(signal[start:end]))

        # Debugging output for amplitude values
        print(f"Symbol {i}: Amplitude = {amplitude:.2f}")

        # Adjusted thresholds based on your modulation scheme
        if amplitude > 0.5:  # Assuming >0.5 corresponds to `1`
            bits.append('1')
        else:  # Assuming <=0.5 corresponds to `0`
            bits.append('0')

    return ''.join(bits)

# Function to convert bits to characters
def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int("".join(byte), 2))
        chars.append(char)
    return ''.join(chars)

# Function to plot frequency spectrum
def plot_frequency_spectrum(signal, sample_rate):
    freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
    spectrum = np.abs(np.fft.rfft(signal))
    
    plt.figure(figsize=(12, 6))
    plt.plot(freqs, spectrum)
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 22050)  # Limit to half of the sample rate
    plt.grid()
    plt.show()

# Main function to run demodulation
def main(input_file):
    sample_rate, wave = read_wave(input_file)

    # Demodulate the signal
    demodulated_bits = demodulate_wave(wave, sample_rate)

    # Convert bits back to text
    decoded_text = bits_to_text(demodulated_bits)

    print(f"Decoded Bits: {demodulated_bits}")  # Debugging output for bits
    print(f"Decoded Text: {decoded_text}")

    # Plot frequency spectrum of the signal
    plot_frequency_spectrum(wave, sample_rate)

# Run the demodulation on the specified WAV file
if __name__ == "__main__":
    main('binary_modulation.wav')  # Ensure this matches the saved file from the modulation code
