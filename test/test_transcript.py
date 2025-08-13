import unittest
import sys
import os

# Add the parent directory to the Python path to allow importing from utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.transcript import TranscriptParser


class TestTranscriptParser(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = TranscriptParser("")
    
    def test_timestamp_to_seconds(self):
        """Test timestamp string to seconds conversion."""
        # Normal cases
        self.assertEqual(TranscriptParser.timestamp_to_seconds("0:00"), 0)
        self.assertEqual(TranscriptParser.timestamp_to_seconds("0:30"), 30)
        self.assertEqual(TranscriptParser.timestamp_to_seconds("1:00"), 60)
        self.assertEqual(TranscriptParser.timestamp_to_seconds("1:30"), 90)
        self.assertEqual(TranscriptParser.timestamp_to_seconds("10:45"), 645)
        self.assertEqual(TranscriptParser.timestamp_to_seconds("59:59"), 3599)
    
    def test_parse_transcript_to_map_basic(self):
        """Test basic transcript parsing functionality."""
        transcript = """0:00
Hello world
0:30
This is a test
1:00
Final segment"""
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {
            (0, 30): "Hello world",
            (30, 60): "This is a test",
            (60, None): "Final segment"
        }
        self.assertEqual(result, expected)
    
    def test_parse_transcript_to_map_single_entry(self):
        """Test parsing transcript with single entry."""
        transcript = """0:00
Only one segment"""
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {(0, None): "Only one segment"}
        self.assertEqual(result, expected)
    
    def test_parse_transcript_to_map_empty_transcript(self):
        """Test parsing empty transcript."""
        transcript = ""
        result = self.parser.parse_transcript_to_map(transcript)
        self.assertEqual(result, {})
    
    def test_parse_transcript_to_map_whitespace_handling(self):
        """Test that parser handles extra whitespace correctly."""
        transcript = """  0:00  
  Hello world  
  0:30  
  This is a test  """
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {
            (0, 30): "Hello world",
            (30, None): "This is a test"
        }
        self.assertEqual(result, expected)
    
    def test_parse_transcript_to_map_malformed_timestamp(self):
        """Test parsing with malformed timestamps (should be ignored)."""
        transcript = """0:00
Valid entry
invalid_timestamp
Should be ignored
1:00
Another valid entry"""
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {
            (0, 60): "Valid entry",
            (60, None): "Another valid entry"
        }
        self.assertEqual(result, expected)
    
    def test_parse_transcript_to_map_missing_text(self):
        """Test parsing when timestamp is at end of transcript."""
        transcript = """0:00
Hello world
0:30"""
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {(0, None): "Hello world"}
        self.assertEqual(result, expected)
    
    def test_get_text_from_map_normal_cases(self):
        """Test retrieving text from interval map."""
        interval_map = {
            (0, 30): "First segment",
            (30, 60): "Second segment",
            (60, None): "Final segment"
        }
        
        # Test queries within intervals
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:00"), "First segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:15"), "First segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:29"), "First segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:30"), "Second segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:45"), "Second segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:59"), "Second segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "1:00"), "Final segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "5:00"), "Final segment")
    
    def test_get_text_from_map_boundary_cases(self):
        """Test boundary conditions for text retrieval."""
        interval_map = {
            (0, 30): "First segment",
            (30, 60): "Second segment"
        }
        
        # Test exact boundaries
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:00"), "First segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:30"), "Second segment")
        
        # Test out of range queries
        self.assertIsNone(self.parser.get_text_from_map(interval_map, "1:00"))
        self.assertIsNone(self.parser.get_text_from_map(interval_map, "2:00"))
    
    def test_get_text_from_map_empty_map(self):
        """Test retrieving text from empty interval map."""
        interval_map = {}
        self.assertIsNone(self.parser.get_text_from_map(interval_map, "0:00"))
    
    def test_get_text_from_map_single_open_ended_interval(self):
        """Test retrieving text from map with single open-ended interval."""
        interval_map = {(0, None): "Only segment"}
        
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:00"), "Only segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "1:00"), "Only segment")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "10:00"), "Only segment")
    
    def test_integration_parse_and_query(self):
        """Test complete workflow: parse transcript and query results."""
        transcript = """0:00
Welcome to the meeting
0:30
Let's discuss the agenda
1:15
Any questions?
2:00
Thank you for joining"""
        
        interval_map = self.parser.parse_transcript_to_map(transcript)
        
        # Test various queries
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:00"), "Welcome to the meeting")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "0:45"), "Let's discuss the agenda")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "1:30"), "Any questions?")
        self.assertEqual(self.parser.get_text_from_map(interval_map, "3:00"), "Thank you for joining")
    
    def test_complex_timestamps(self):
        """Test parsing with various timestamp formats within valid range."""
        transcript = """00:00
Start
9:59
Middle
10:00
End"""
        
        result = self.parser.parse_transcript_to_map(transcript)
        expected = {
            (0, 599): "Start",
            (599, 600): "Middle", 
            (600, None): "End"
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main() 