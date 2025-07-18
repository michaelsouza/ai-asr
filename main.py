"""
Main script to launch the real-time ASR application.
"""

import threading
import customtkinter as ctk
from transcriber import Transcriber
from audio_handler import AudioHandler
from gui import App

def main():
    """
    Main function to initialize and run the application threads.
    """
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Events for thread synchronization
    start_event = threading.Event()
    stop_event = threading.Event()

    # Initialize components
    transcriber = Transcriber(model_size="base", device="cuda", compute_type="int8")
    audio_handler = AudioHandler(transcriber.audio_queue)

    # The GUI now controls the start and stop events
    app = App(transcriber.text_queue, start_event, stop_event)

    def run_audio_processing():
        start_event.wait() # Wait for the start button to be pressed
        audio_handler.start_recording()

    def run_transcription():
        start_event.wait() # Wait for the start button to be pressed
        transcriber.transcribe_audio()

    # Create and start the threads
    audio_thread = threading.Thread(target=run_audio_processing)
    transcriber_thread = threading.Thread(target=run_transcription)
    
    audio_thread.start()
    transcriber_thread.start()

    # Start the GUI
    app.mainloop()

    # Cleanly stop the threads when the GUI is closed
    audio_handler.stop_recording()
    transcriber.stop_transcribing()
    audio_thread.join()
    transcriber_thread.join()
    print("Application closed successfully.")

if __name__ == "__main__":
    main()
