"""
This module defines the Transcriber class, responsible for loading the ASR model
and processing audio data from a queue.
"""

import queue
import threading
from faster_whisper import WhisperModel
import numpy as np

class Transcriber:
    """
    The Transcriber class loads a faster-whisper model and transcribes audio chunks.
    """

    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        Initializes the Transcriber with a specified model size and device.

        Args:
            model_size (str): The size of the Whisper model to load (e.g., "base", "small").
            device (str): The device to run the model on ("cpu" or "cuda").
            compute_type (str): The compute type for the model (e.g., "int8", "float16").
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.stop_event = threading.Event()

    def transcribe_audio(self):
        """
        Continuously fetches audio data from the queue and transcribes it.
        """
        print("Transcription thread started.")
        while not self.stop_event.is_set():
            try:
                # Wait for an audio chunk to be available
                audio_chunk = self.audio_queue.get(timeout=1)

                # Ensure audio is in the correct format (float32)
                if audio_chunk.dtype != np.float32:
                    audio_chunk = audio_chunk.astype(np.float32) / np.iinfo(audio_chunk.dtype).max

                # Transcribe the audio chunk
                segments, _ = self.model.transcribe(audio_chunk, beam_size=5)
                
                transcribed_text = ""
                for segment in segments:
                    transcribed_text += segment.text + " "
                
                if transcribed_text.strip():
                    self.text_queue.put(transcribed_text.strip())

            except queue.Empty:
                # This is expected when there's no speech
                continue
            except Exception as e:
                print(f"Error during transcription: {e}")
        print("Transcription thread stopped.")

    def stop_transcribing(self):
        """
        Stops the transcription thread.
        """
        print("Stopping transcription...")
        self.stop_event.set()
