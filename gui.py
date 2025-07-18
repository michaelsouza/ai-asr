"""
This module defines the main application GUI using customtkinter.
"""

import customtkinter as ctk
import queue

class App(ctk.CTk):
    """
    The main application window.
    """

    def __init__(self, text_queue, start_event, stop_event):
        """
        Initializes the main application window.

        Args:
            text_queue (queue.Queue): A queue to get transcribed text from.
            start_event (threading.Event): An event to signal the start of processing.
            stop_event (threading.Event): An event to signal the stop of processing.
        """
        super().__init__()
        self.title("Real-Time ASR")
        self.geometry("800x600")

        self.text_queue = text_queue
        self.start_event = start_event
        self.stop_event = stop_event
        self.is_running = False

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Textbox for transcription
        self.textbox = ctk.CTkTextbox(self.main_frame, wrap="word", font=("Arial", 14))
        self.textbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Button frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Start/Stop button
        self.toggle_button = ctk.CTkButton(self.button_frame, text="Start Recording", command=self.toggle_recording)
        self.toggle_button.pack(side="left", padx=5, pady=5)

        # Clear button
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Text", command=self.clear_text)
        self.clear_button.pack(side="left", padx=5, pady=5)

        # Set the closing protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the queue processing loop
        self.after(100, self.process_text_queue)

    def toggle_recording(self):
        """
        Toggles the recording state.
        """
        if not self.is_running:
            self.is_running = True
            self.toggle_button.configure(text="Stop Recording")
            self.start_event.set() # Signal other threads to start
            self.stop_event.clear()
        else:
            self.is_running = False
            self.toggle_button.configure(text="Start Recording")
            self.stop_event.set() # Signal other threads to stop
            self.start_event.clear()

    def clear_text(self):
        """
        Clears the text in the textbox.
        """
        self.textbox.delete("1.0", "end")

    def process_text_queue(self):
        """
        Processes the text queue and updates the GUI.
        """
        try:
            while not self.text_queue.empty():
                text = self.text_queue.get_nowait()
                self.textbox.insert("end", text + "\n")
                self.textbox.see("end") # Auto-scroll
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_text_queue)

    def on_closing(self):
        """
        Handles the application closing event.
        """
        self.stop_event.set() # Ensure other threads are stopped
        self.destroy()
