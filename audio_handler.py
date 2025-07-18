"""
This module defines the AudioHandler class, responsible for capturing audio
from the microphone and performing voice activity detection (VAD).
"""

import queue
import sounddevice as sd
import numpy as np
import torch
import threading

class AudioHandler:
    """
    The AudioHandler class manages microphone input and VAD.
    """

    def __init__(self, audio_queue, sample_rate=16000, block_size=512, channels=1):
        """
        Initializes the AudioHandler.

        Args:
            audio_queue (queue.Queue): A queue to put audio chunks into.
            sample_rate (int): The sample rate for audio recording.
            block_size (int): The block size for the audio stream.
            channels (int): The number of audio channels.
        """
        self.audio_queue = audio_queue
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.device = sd.default.device[0]
        self.speech_buffer = []
        self.silence_counter = 0
        self.is_speaking = False
        self.stop_event = threading.Event()

        # Load Silero VAD model
        self.vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                               model='silero_vad',
                                               force_reload=True)
        (self.get_speech_timestamps,
         self.save_audio,
         self.read_audio,
         self.VADIterator,
         self.collect_chunks) = utils

    def _audio_callback(self, indata, frames, time, status):
        """
        This function is called for each audio block from the sounddevice stream.
        """
        if status:
            print(status)

        # The VAD model expects a single-channel float32 tensor
        audio_tensor = torch.from_numpy(indata[:, 0]).float()

        # Check for speech
        speech_prob = self.vad_model(audio_tensor, self.sample_rate).item()

        if speech_prob > 0.5:  # Threshold for speech detection
            if not self.is_speaking:
                self.is_speaking = True
                self.speech_buffer = [] # Start a new buffer
            self.speech_buffer.append(indata.copy())
            self.silence_counter = 0
        else:
            if self.is_speaking:
                self.silence_counter += 1
                # End of speech detected after a few silent chunks
                if self.silence_counter > 5: # 5 * block_size / sample_rate seconds of silence
                    self.is_speaking = False
                    # Concatenate the buffer and put it on the queue
                    if self.speech_buffer:
                        full_speech = np.concatenate(self.speech_buffer, axis=0)
                        self.audio_queue.put(full_speech)
                    self.speech_buffer = []
                    self.silence_counter = 0

    def start_recording(self):
        """
        Starts the audio recording stream.
        """
        print("Starting audio recording...")
        try:
            with sd.InputStream(samplerate=self.sample_rate,
                                blocksize=self.block_size,
                                device=self.device,
                                channels=self.channels,
                                dtype='float32',
                                callback=self._audio_callback):
                while not self.stop_event.is_set():
                    sd.sleep(100) # Keep the stream alive
        except Exception as e:
            print(f"Error in audio stream: {e}")
        finally:
            print("Audio recording stopped.")


    def stop_recording(self):
        """
        Stops the audio recording stream.
        """
        print("Stopping audio recording...")
        self.stop_event.set()
