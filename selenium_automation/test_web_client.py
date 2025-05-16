import unittest
from unittest.mock import patch
from selenium_automation.web_client import WebClient

class TestWebClient(unittest.TestCase):

    @patch("selenium_automation.web_client.subprocess.check_output")
    def test_is_valid_driver_matching_version(self, mock_subproc):
        # Giả lập đầu ra cho Chrome và chromedriver
        mock_subproc.side_effect = [
            b"Google Chrome 122.0.6261.69\n",     # Output for chrome --version
            b"ChromeDriver 122.0.6261.69\n"       # Output for chromedriver --version
        ]

        client = WebClient(headless=True)
        path = "/path/to/fake/chromedriver"

        self.assertTrue(client._is_valid_driver(path))

    @patch("selenium_automation.web_client.subprocess.check_output")
    def test_is_valid_driver_mismatched_version(self, mock_subproc):
        mock_subproc.side_effect = [
            b"Google Chrome 123.0.1234.56\n",
            b"ChromeDriver 122.0.9999.88\n"
        ]

        client = WebClient(headless=True)
        path = "/path/to/fake/chromedriver"

        self.assertFalse(client._is_valid_driver(path))

    @patch("selenium_automation.web_client.subprocess.check_output", side_effect=Exception("Không chạy được"))
    def test_is_valid_driver_error(self, mock_subproc):
        client = WebClient(headless=True)
        path = "/path/to/fake/chromedriver"

        self.assertFalse(client._is_valid_driver(path))

if __name__ == "__main__":
    unittest.main()
