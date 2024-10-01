import numpy as np
from scipy.io.wavfile import write

# Define modulation parameters
sample_rate = 44100  # Sample rate for audio
symbol_rate = 200  # Symbol rate in bits per second (bps)
symbol_duration = 1 / symbol_rate  # Duration of each symbol in seconds
amplitude_1 = 3.0  # Amplitude for bit 1
amplitude_0 = 1.5  # Amplitude for bit 0

# Generate audio wave from binary string
def generate_wave(bit_string, sample_rate=44100, symbol_duration=symbol_duration):
    total_samples = int(sample_rate * symbol_duration * len(bit_string))
    wave = np.zeros(total_samples, dtype=np.float32)
    t = np.linspace(0, symbol_duration, int(sample_rate * symbol_duration), endpoint=False)

    for i, bit in enumerate(bit_string):
        # Determine amplitude based on bit value
        if bit == '1':
            amplitude = amplitude_1
        else:
            amplitude = amplitude_0

        # Generate wave for the current bit
        wave[i * len(t):(i + 1) * len(t)] = amplitude * np.sin(2 * np.pi * 440 * t)

    return wave

# Main function to run modulation and save to WAV
def main(input_text):
    # Convert text to binary
    bit_string = ''.join(format(ord(char), '08b') for char in input_text)
    
    # Generate wave based on the binary string
    wave = generate_wave(bit_string)
    
    # Normalize wave to prevent clipping
    wave /= np.max(np.abs(wave))  # Optional: ensure it doesn't exceed [-1, 1] for saving
    write('binary_modulation.wav', sample_rate, (wave * 32767).astype(np.int16))  # Save to WAV format

# Example input text
input_text = 'N4WHP CQ CQ CQ FM07RO      '
main(input_text)
