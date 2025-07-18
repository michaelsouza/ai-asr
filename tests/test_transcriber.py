"""
Unit tests for the Transcriber class.
"""

import unittest
from unittest.mock import MagicMock, patch
import queue
import numpy as np
from transcriber import Transcriber

class TestTranscriber(unittest.TestCase):
    """
    Tests the Transcriber class.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.model_size = "base"
        self.device = "cpu"
        self.compute_type = "int8"

        # Patch the WhisperModel to avoid loading the actual model
        self.mock_model_patch = patch('transcriber.WhisperModel')
        self.mock_model = self.mock_model_patch.start()
        self.mock_model_instance = self.mock_model.return_value

        self.transcriber = Transcriber(self.model_size, self.device, self.compute_type)
        self.transcriber.audio_queue = queue.Queue()
        self.transcriber.text_queue = queue.Queue()

    def tearDown(self):
        """
        Clean up the test environment.
        """
        self.mock_model_patch.stop()

    def test_transcribe_audio(self):
        """
        Tests the transcribe_audio method.
        """
        # Create a mock audio chunk
        mock_audio = np.random.rand(16000).astype(np.float32)
        self.transcriber.audio_queue.put(mock_audio)

        # Mock the model's transcribe method
        mock_segment = MagicMock()
        mock_segment.text = "This is a test transcription."
        self.mock_model_instance.transcribe.return_value = ([mock_segment], None)

        # Run the transcription in a separate thread so we can stop it
        import threading
        thread = threading.Thread(target=self.transcriber.transcribe_audio)
        thread.daemon = True
        thread.start()

        # Check the text queue for the transcribed text
        try:
            transcribed_text = self.transcriber.text_queue.get(timeout=2)
            self.assertEqual(transcribed_text, "This is a test transcription.")
        except queue.Empty:
            self.fail("Text queue was empty after transcription.")
        finally:
            self.transcriber.stop_transcribing()
            thread.join(timeout=2)

if __name__ == '__main__':
    unittest.main()
