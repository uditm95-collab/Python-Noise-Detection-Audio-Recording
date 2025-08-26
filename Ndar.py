import pyaudio
import wave
import numpy as np
import time
from datetime import datetime

# Audio recording parameters
FORMAT = pyaudio.paInt16       # 16-bit audio format
CHANNELS = 1                   # Mono channel
RATE = 44100                   # Sampling rate (44.1 kHz)
CHUNK = 1024                   # Frames per buffer
THRESHOLD = 500                # Noise threshold for recording start
SAVE_INTERVAL = 60             # Time in seconds to save audio
OUTPUT_FILENAME_PREFIX = "recorded_audio"  # Prefix for audio files

def is_silent(data_chunk):
    """
    Returns True if the audio chunk is below the threshold.
    """
    amplitude = np.frombuffer(data_chunk, dtype=np.int16)
    return np.abs(amplitude).mean() < THRESHOLD

def save_audio(audio_data, timestamp):
    """
    Save the collected audio data to a file.
    """
    filename = f"{OUTPUT_FILENAME_PREFIX}_{timestamp}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_data))
    print(f"Audio saved as {filename}")

def record_audio():
    """
    Record audio continuously and save it every SAVE_INTERVAL seconds.
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Listening for noise...")
    frames = []
    start_time = time.time()

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)

            # Save audio every SAVE_INTERVAL seconds
            if time.time() - start_time >= SAVE_INTERVAL:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_audio(frames, timestamp)
                frames = []  # Clear frames for the next interval
                start_time = time.time()  # Reset timer

    except KeyboardInterrupt:
        print("Recording stopped manually.")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    record_audio()
