import pytest
import sys
import os
from unittest.mock import patch
from fetch_url import main, Config, valid_dir, validate_correct_content, extract_file_name, parser
from pathlib import Path


def test_basic_url_parsing():
    """Test that the URL is correctly captured."""
    test_args = ["fetch_url.py", "https://example.com"]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args(test_args[1:])
        assert args.url == "https://example.com"
        assert args.dir == Path(".")

def test_full_arguments():
    test_args = ["fetch_url.py", "https://example.com", "-o", "file.zip", "-d", "."]
    with patch.object(sys, 'argv', test_args):
        args = parser.parse_args(test_args[1:])
        assert args.output == "file.zip"
        assert args.dir == Path(".")


def test_invalid_directory_fails(capsys):
    """Test that an invalid directory causes the script to exit with an error."""
    test_args = ["fetch_url.py", "https://example.com", "-d", "/non/existent/path"]
    
    with pytest.raises(SystemExit):
        parser.parse_args(test_args[1:])
