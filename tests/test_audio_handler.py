"""
Unit tests for the AudioHandler class.
"""

import unittest
from unittest.mock import MagicMock, patch
import queue
import numpy as np
import torch

# Add the project root to the path to allow importing the modules
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_handler import AudioHandler

class TestAudioHandler(unittest.TestCase):
    """
    Tests the AudioHandler class.
    """

    @patch('sounddevice.InputStream')
    @patch('torch.hub.load')
    def setUp(self, mock_torch_load, mock_input_stream):
        """
        Set up the test environment for AudioHandler.
        """
        # Mock the VAD model loading
        self.mock_vad_model = MagicMock(return_value=torch.tensor([0.0]))
        mock_utils = (MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock())
        mock_torch_load.return_value = (self.mock_vad_model, mock_utils)

        self.audio_queue = queue.Queue()
        self.audio_handler = AudioHandler(self.audio_queue)
        self.audio_handler.stop_event.set() # Ensure the recording loop doesn't start automatically

    def test_audio_callback_speech_and_silence(self):
        """
        Test the _audio_callback method for handling speech and silence.
        """
        # Simulate speech
        self.mock_vad_model.return_value = torch.tensor([0.8]) # High speech probability
        speech_data = np.random.rand(self.audio_handler.block_size, 1).astype(np.float32)
        self.audio_handler._audio_callback(speech_data, None, None, None)
        self.assertTrue(self.audio_handler.is_speaking)
        self.assertEqual(len(self.audio_handler.speech_buffer), 1)
        self.assertEqual(self.audio_handler.silence_counter, 0)

        # Simulate more speech
        self.audio_handler._audio_callback(speech_data, None, None, None)
        self.assertEqual(len(self.audio_handler.speech_buffer), 2)

        # Simulate silence
        self.mock_vad_model.return_value = torch.tensor([0.1]) # Low speech probability
        silence_data = np.zeros((self.audio_handler.block_size, 1), dtype=np.float32)
        
        # Simulate enough silence to trigger the end of speech
        for _ in range(6):
            self.audio_handler._audio_callback(silence_data, None, None, None)

        # Check if the speech buffer was processed and put into the queue
        self.assertFalse(self.audio_handler.is_speaking)
        self.assertTrue(self.audio_queue.qsize() == 1)
        self.assertEqual(len(self.audio_handler.speech_buffer), 0)

        # Verify the content of the queue
        try:
            queued_audio = self.audio_queue.get_nowait()
            self.assertIsInstance(queued_audio, np.ndarray)
            # The queued audio should be the concatenation of the two speech buffers
            self.assertEqual(queued_audio.shape[0], speech_data.shape[0] * 2)
        except queue.Empty:
            self.fail("Audio queue was empty after speech detection.")

if __name__ == '__main__':
    unittest.main()
