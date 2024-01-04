import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    # Calculate the root mean square (RMS) value of the audio input and set it to callback.sound_level
    rms = np.sqrt(np.mean(indata**2))
    if rms > callback.max_sound_level:
        callback.max_sound_level = rms

# Open a stream for audio input
def detect_sound(duration):
    sampling_rate = 44100
    callback.max_sound_level = 0
    with sd.InputStream(callback=callback, channels=1, samplerate=sampling_rate):
        sd.sleep(duration * 1000)  # Sleep for the specified duration in milliseconds

    return callback.max_sound_level

if __name__ == "__main__":
    # Sample params: sampling rate = 44100, duration is 5 seconds, threshold is 0.25
    detect_sound(10)
