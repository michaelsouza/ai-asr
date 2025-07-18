# **Project Plan: Real-Time ASR Desktop Application**

**Objective:** To build a desktop application for real-time speech recognition (ASR) using Python. The application will capture audio from a microphone and transcribe it to text locally using an optimized version of the Whisper model.

### **1\. Core Technologies & Rationale**

This project will use the following libraries. Understanding why each was chosen is key.

* **Language:** Python 3.9+  
* **ASR Model:** **faster-whisper**  
  * **Why?** It's a highly optimized reimplementation of OpenAI's Whisper model. It provides significantly faster performance and lower memory usage, which is crucial for a smooth real-time experience on a local machine, especially on a GPU.  
* **GUI Framework:** **customtkinter**  
  * **Why?** It's a modern wrapper around Python's standard Tkinter library. It makes creating a visually appealing and professional-looking user interface much simpler than with standard Tkinter.  
* **Audio Handling:** **sounddevice** & **numpy**  
  * **Why?** sounddevice provides a straightforward, cross-platform interface for capturing audio from a microphone. numpy is used to handle the audio data as numerical arrays efficiently.  
* **Voice Activity Detection (VAD):** **silero-vad**  
  * **Why?** To avoid transcribing silence, which wastes computing resources. This lightweight model listens to the audio stream and tells us when speech is present, so we only send actual speech to the main ASR model.  
* **GPU Acceleration:** **torch** (with CUDA support)  
  * **Why?** The target hardware has a powerful NVIDIA GPU. Using torch with CUDA allows faster-whisper to run on the GPU, making transcription dramatically faster.

### **2\. Software Engineering Best Practices**

To ensure the project is robust, maintainable, and of high quality, the following practices must be adopted.

* **2.1. Version Control (Git)**  
  * The entire project must be managed under Git version control from the beginning.  
  * Use clear and descriptive commit messages (e.g., "feat: Add microphone toggle button" or "fix: Correct audio buffer overflow").  
  * Use feature branches for developing new functionalities to keep the main branch stable.  
* **2.2. Code Quality and Style**  
  * All code must adhere to the **PEP 8** style guide.  
  * Use a code formatter like **black** to ensure a consistent style across the entire project.  
  * Use a linter like **ruff** or flake8 to automatically check for code errors, bugs, and stylistic issues.  
* **2.3. Documentation**  
  * Every class and function must have a clear **docstring** explaining its purpose, arguments (Args), and what it returns (Returns). This is non-negotiable for creating maintainable code.  
* **2.4. Testing (pytest)**  
  * A dedicated tests/ directory must be created at the project root.  
  * **Unit tests** must be written for all non-GUI logic. This includes functions for audio processing, file handling, and any data manipulation.  
  * The pytest framework should be used for writing and running tests. This practice is essential for verifying functionality and preventing regressions when adding new features or refactoring.  
* **2.5. Design Patterns**  
  * Patterns should be used pragmatically to solve specific problems, not for their own sake. Avoid over-engineering.  
  * The core architecture already uses the **Producer-Consumer Pattern** (via thread-safe queues), which is the correct pattern for decoupling the audio capture, processing, and GUI update tasks.  
  * If complexity increases, other patterns like the **Observer Pattern** (to notify the GUI of state changes) or **Singleton** (to ensure only one instance of the Transcriber exists) could be considered.

### **3\. Project Setup: A Step-by-Step Guide**

Follow these steps precisely to set up the development environment.

Step 3.1: Create the Project Directory  
Open a terminal and navigate to the specified path.  
\# For Linux/macOS  
mkdir \-p /home/michael/gitrepos/ai-asr  
cd /home/michael/gitrepos/ai-asr

**Step 3.2: Create and Activate a Python Virtual Environment**

python \-m venv venv  
\# On Windows: venv\\Scripts\\activate.bat  
\# On Linux/macOS: source venv/bin/activate

Step 3.3: Install Dependencies  
Create two files for dependencies: one for the application and one for development tools.  
**requirements.txt**

customtkinter  
sounddevice  
numpy  
faster-whisper  
silero

**requirements-dev.txt**

pytest  
black  
ruff

Install dependencies using these commands:

\# Install PyTorch with CUDA support first  
pip install torch torchaudio \--index-url https://download.pytorch.org/whl/cu121

\# Install application and development dependencies  
pip install \-r requirements.txt  
pip install \-r requirements-dev.txt

### **4\. Application Architecture: The Multi-Threaded Approach**

(This section remains the same as the previous version, detailing the Main, Audio Handler, and Transcriber threads and their interaction via queues.)

Data Flow:  
Microphone \-\> Audio Handler Thread \-\> \[audio\_queue\] \-\> Transcriber Thread \-\> \[text\_queue\] \-\> GUI Thread \-\> Screen

### **5\. Implementation Steps & File Structure**

Create the following file structure. Note the addition of the tests/ directory.

/ai-asr/  
├── venv/  
├── tests/                \# Directory for all test files  
│   ├── test\_transcriber.py  
│   └── ...  
├── main.py               \# Main script to launch the app and threads  
├── gui.py                \# The main UI class and its components  
├── audio\_handler.py      \# Class for microphone capture and VAD  
├── transcriber.py        \# Class to load and run the Whisper model  
├── config.json           \# To store user settings (e.g., save path)  
├── requirements.txt  
└── requirements-dev.txt

The implementation steps (4.1 to 4.5 from the previous plan) remain the same, but with the added requirement that as each piece of logic is built in audio\_handler.py and transcriber.py, corresponding unit tests must be written in the tests/ directory.

This detailed plan provides a complete and professional roadmap for the project. Good luck\!