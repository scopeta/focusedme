"""Test the audio playback functionality across different platforms."""

import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, "..")


class TestAudioPlayback(unittest.TestCase):
    """Test suite for audio playback functionality."""

    @patch("focusedme.__main__.subprocess.run")
    def test_audio_playback_macos(self, mock_run):
        """Test audio playback on macOS."""
        from focusedme.__main__ import View

        # Simulate macOS
        with patch("focusedme.__main__.sys.platform", "darwin"):
            View.ring_bell("Ring01.wav")
            mock_run.assert_called_once()

    @patch("focusedme.__main__.playsound")
    def test_audio_playback_windows(self, mock_playsound):
        """Test audio playback on Windows."""
        from focusedme.__main__ import View

        # Simulate Windows with playsound available
        with patch("focusedme.__main__.sys.platform", "win32"):
            with patch("focusedme.__main__.playsound", mock_playsound):
                View.ring_bell("Ring01.wav")
                mock_playsound.assert_called_once()

    @patch("focusedme.__main__.sa.WaveObject.from_wave_file")
    def test_audio_playback_linux(self, mock_wave_file):
        """Test audio playback on Linux using simpleaudio."""
        from focusedme.__main__ import View

        # Simulate Linux with simpleaudio available
        with patch("focusedme.__main__.sys.platform", "linux"):
            with patch("focusedme.__main__.sa") as mock_sa:
                mock_wave_obj = MagicMock()
                mock_sa.WaveObject.from_wave_file.return_value = mock_wave_obj

                View.ring_bell("Ring01.wav")
                mock_sa.WaveObject.from_wave_file.assert_called_once()
                mock_wave_obj.play.assert_called_once()

    def test_audio_playback_exception_handling(self):
        """Test that audio playback exceptions are properly handled."""
        from focusedme.__main__ import View

        # Test that exceptions are caught and don't propagate
        with patch("focusedme.__main__.sys.platform", "darwin"):
            with patch(
                "focusedme.__main__.subprocess.run", side_effect=Exception("Test error")
            ):
                # This should not raise an exception
                View.ring_bell("Ring01.wav")


if __name__ == "__main__":
    unittest.main()
