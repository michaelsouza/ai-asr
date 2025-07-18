# Real-Time ASR Desktop Application

This project implements a real-time Automatic Speech Recognition (ASR) desktop application using Python. It captures audio from your microphone and transcribes it to text locally using an optimized version of the Whisper model.

## Core Technologies

*   **Language:** Python 3.9+
*   **ASR Model:** `faster-whisper` (optimized Whisper model)
*   **GUI Framework:** `customtkinter`
*   **Audio Handling:** `sounddevice` & `numpy`
*   **Voice Activity Detection (VAD):** `silero-vad`
*   **GPU Acceleration:** `torch` (with CUDA support for NVIDIA GPUs)

## Project Structure

```
/ai-asr/
├── .venv/                  # Python Virtual Environment
├── tests/                  # Unit tests
│   ├── test_transcriber.py
│   └── test_audio_handler.py
├── main.py                 # Main script to launch the application
├── gui.py                  # User Interface (customtkinter)
├── audio_handler.py        # Microphone capture and VAD logic
├── transcriber.py          # Whisper model loading and transcription
├── config.json             # Application settings
├── requirements.txt        # Application dependencies
├── requirements-dev.txt    # Development dependencies (pytest, black, ruff)
└── README.md               # This file
```

## Setup and Installation

Follow these steps to set up the development environment and install dependencies:

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/your-repo/ai-asr.git
    cd ai-asr
    ```

2.  **Create and activate a Python Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    # .venv\Scripts\activate.bat  # On Windows
    ```

3.  **Install Dependencies:**
    First, install PyTorch with CUDA support (if you have an NVIDIA GPU). Refer to the official PyTorch website for the correct command for your specific CUDA version. For CUDA 12.1, it would be:
    ```bash
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```
    Then, install the application and development dependencies:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

## Running the Application

To start the application, activate your virtual environment and run `main.py`:

```bash
source .venv/bin/activate
python main.py
```

## Running Tests

To run the unit tests, activate your virtual environment and use `pytest`:

```bash
source .venv/bin/activate
PYTHONPATH=. pytest
```

## Known Issues

*   **Audio Device Not Found:** The application currently faces an issue where `sounddevice` cannot detect audio input devices on some Linux systems, resulting in an "Error querying device -1". This is likely due to underlying system audio configuration or missing drivers/libraries (e.g., PortAudio, ALSA). Ensure your system's audio input is properly configured and working outside of this application.

## To-Do List

*   Implement proper error handling and logging throughout the application.
*   Add configuration options for model size, device, and audio input device selection in `config.json` and the GUI.
*   Implement a visual indicator in the GUI for when speech is detected.
*   Add functionality to save transcribed text to a file.
*   Improve GUI responsiveness and user feedback.
*   Explore options for packaging the application into a standalone executable.
*   Add more comprehensive unit and integration tests.
