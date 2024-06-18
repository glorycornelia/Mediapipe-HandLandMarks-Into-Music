# Voice to Keynote Function
import pyaudio
import numpy as np
import librosa

def detect_key_from_chromagram(chromagram):
    # Define the mapping of chroma features to keys
    chroma_to_key = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    
    # Calculate the mean chroma feature across time
    mean_chroma = np.mean(chromagram, axis=1)
    
    # Find the key by selecting the maximum chroma feature
    estimated_key_index = np.argmax(mean_chroma)
    estimated_key = chroma_to_key[estimated_key_index]
    
    return estimated_key

def detect_key():
    # Constants
    BUFFER_SIZE = 2048  # Number of frames per buffer
    CHANNELS = 1        # Mono audio
    FORMAT = pyaudio.paFloat32  # Audio format
    RATE = 44100       # Sampling rate

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=BUFFER_SIZE)

    print("Listening to the microphone...")

    estimated_key = 'C'

    try:
        for i in range(50):
            # Read raw microphone data
            data = stream.read(BUFFER_SIZE)
            
            # Convert data to numpy array
            samples = np.frombuffer(data, dtype=np.float32)
            
            # Ensure there is enough data to process
            if len(samples) < BUFFER_SIZE:
                continue
            
            # Compute the Chroma Short-Time Fourier Transform (chroma_stft)
            chromagram = librosa.feature.chroma_stft(y=samples, sr=RATE, n_fft=BUFFER_SIZE)
            
            # Detect the key
            estimated_key = detect_key_from_chromagram(chromagram)
            
            # Print the detected key
            if i == 49:
                print("Detected Key:", estimated_key)
                break
            else:
                continue
            
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
    return estimated_key