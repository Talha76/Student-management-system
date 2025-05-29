import unittest
import sys
import os
import importlib.util
from unittest.mock import patch, MagicMock
from tkinter import StringVar
import sqlite3

# Path to the Student Management System file
SMS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Student Management System.py')

# Mock the external API calls before importing the module
with patch('requests.get') as mock_requests_get:
    with patch('bs4.BeautifulSoup') as mock_bs4:
        # Mock location API response
        mock_location_response = MagicMock()
        mock_location_response.json.return_value = {'loc': '19.0760,72.8777'}
        
        # Mock weather API response
        mock_weather_response = MagicMock()
        mock_weather_response.json.return_value = {'main': {'temp': 25.0}}
        
        # Mock quote scraping response
        mock_quote_response = MagicMock()
        mock_quote_response.text = '<html><img class="p-qotd" alt="Test quote" /></html>'
        
        # Configure side_effect to return different responses for different calls
        mock_requests_get.side_effect = [mock_location_response, mock_weather_response, mock_quote_response]
        
        # Mock BeautifulSoup
        mock_soup = MagicMock()
        mock_img = MagicMock()
        mock_img.__getitem__.return_value = "Test quote"
        mock_soup.find.return_value = mock_img
        mock_bs4.return_value = mock_soup
        
        # Import the module using importlib.util to handle the space in the filename
        spec = importlib.util.spec_from_file_location("student_management", SMS_PATH)
        student_management = importlib.util.module_from_spec(spec)
        sys.modules["student_management"] = student_management
        spec.loader.exec_module(student_management)

class TestStudentManagementSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test method."""
        # Create a test database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE student (
                rno INTEGER PRIMARY KEY,
                name TEXT,
                marks INTEGER
            )
        ''')
        self.conn.commit()
        
        # Mock StringVar objects
        self.mock_st_rno = MagicMock()
        self.mock_st_nme = MagicMock()
        self.mock_st_mks = MagicMock()
        
    def tearDown(self):
        """Clean up after each test method."""
        self.conn.close()
    
    def test_roll_validate_empty(self):
        """Test roll number validation with empty input."""
        # Save original reference
        original_st_rno = student_management.st_rno
        # Replace with mock
        student_management.st_rno = self.mock_st_rno
        self.mock_st_rno.get.return_value = ""
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._roll_validate()
            mock_showerror.assert_called_once_with("Failure", "Roll no should not be empty ")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_rno = original_st_rno
            student_management.showerror = original_showerror
    
    def test_roll_validate_alpha(self):
        """Test roll number validation with alphabetic input."""
        # Save original reference
        original_st_rno = student_management.st_rno
        # Replace with mock
        student_management.st_rno = self.mock_st_rno
        self.mock_st_rno.get.return_value = "abc"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._roll_validate()
            mock_showerror.assert_called_once_with("Failure", "Only numbers allowed for roll no")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_rno = original_st_rno
            student_management.showerror = original_showerror
    
    def test_roll_validate_negative(self):
        """Test roll number validation with negative number."""
        # Save original reference
        original_st_rno = student_management.st_rno
        # Replace with mock
        student_management.st_rno = self.mock_st_rno
        self.mock_st_rno.get.return_value = "-5"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._roll_validate()
            mock_showerror.assert_called_once_with("Failure", "Roll no should be greater than 0")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_rno = original_st_rno
            student_management.showerror = original_showerror
    
    def test_roll_validate_valid(self):
        """Test roll number validation with valid input."""
        # Save original reference
        original_st_rno = student_management.st_rno
        # Replace with mock
        student_management.st_rno = self.mock_st_rno
        self.mock_st_rno.get.return_value = "123"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._roll_validate()
            mock_showerror.assert_not_called()
            self.assertEqual(result, 0)
        finally:
            # Restore original references
            student_management.st_rno = original_st_rno
            student_management.showerror = original_showerror
    
    def test_name_validate_empty(self):
        """Test name validation with empty input."""
        # Save original reference
        original_st_nme = student_management.st_nme
        # Replace with mock
        student_management.st_nme = self.mock_st_nme
        self.mock_st_nme.get.return_value = ""
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._name_validate()
            mock_showerror.assert_called_once_with("Failure", "Name should not be empty ")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_nme = original_st_nme
            student_management.showerror = original_showerror
    
    def test_name_validate_digits(self):
        """Test name validation with digits."""
        # Save original reference
        original_st_nme = student_management.st_nme
        # Replace with mock
        student_management.st_nme = self.mock_st_nme
        self.mock_st_nme.get.return_value = "123"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._name_validate()
            mock_showerror.assert_called_once_with("Failure", "Only characters allowed for Name")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_nme = original_st_nme
            student_management.showerror = original_showerror
    
    def test_name_validate_short(self):
        """Test name validation with short name."""
        # Save original reference
        original_st_nme = student_management.st_nme
        # Replace with mock
        student_management.st_nme = self.mock_st_nme
        self.mock_st_nme.get.return_value = "A"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._name_validate()
            mock_showerror.assert_called_once_with("Failure", "Length of name should be greater than 1")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_nme = original_st_nme
            student_management.showerror = original_showerror
    
    def test_name_validate_valid(self):
        """Test name validation with valid input."""
        # Save original reference
        original_st_nme = student_management.st_nme
        # Replace with mock
        student_management.st_nme = self.mock_st_nme
        self.mock_st_nme.get.return_value = "John"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._name_validate()
            mock_showerror.assert_not_called()
            self.assertEqual(result, 0)
        finally:
            # Restore original references
            student_management.st_nme = original_st_nme
            student_management.showerror = original_showerror
    
    def test_marks_validate_empty(self):
        """Test marks validation with empty input."""
        # Save original reference
        original_st_mks = student_management.st_mks
        # Replace with mock
        student_management.st_mks = self.mock_st_mks
        self.mock_st_mks.get.return_value = ""
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._marks_validate()
            mock_showerror.assert_called_once_with("Failure", "Marks should not be empty ")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_mks = original_st_mks
            student_management.showerror = original_showerror
    
    def test_marks_validate_alpha(self):
        """Test marks validation with alphabetic input."""
        # Save original reference
        original_st_mks = student_management.st_mks
        # Replace with mock
        student_management.st_mks = self.mock_st_mks
        self.mock_st_mks.get.return_value = "abc"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._marks_validate()
            mock_showerror.assert_called_once_with("Failure", "Only numbers allowed for marks")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_mks = original_st_mks
            student_management.showerror = original_showerror
    
    def test_marks_validate_negative(self):
        """Test marks validation with negative number."""
        # Save original reference
        original_st_mks = student_management.st_mks
        # Replace with mock
        student_management.st_mks = self.mock_st_mks
        self.mock_st_mks.get.return_value = "-5"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._marks_validate()
            mock_showerror.assert_called_once_with("Failure", "Marks should be greater than 0")
            self.assertEqual(result, 1)
        finally:
            # Restore original references
            student_management.st_mks = original_st_mks
            student_management.showerror = original_showerror
    
    def test_marks_validate_valid(self):
        """Test marks validation with valid input."""
        # Save original reference
        original_st_mks = student_management.st_mks
        # Replace with mock
        student_management.st_mks = self.mock_st_mks
        self.mock_st_mks.get.return_value = "85"
        
        # Save original showerror
        original_showerror = student_management.showerror
        # Mock showerror
        mock_showerror = MagicMock()
        student_management.showerror = mock_showerror
        
        try:
            result = student_management._marks_validate()
            mock_showerror.assert_not_called()
            self.assertEqual(result, 0)
        finally:
            # Restore original references
            student_management.st_mks = original_st_mks
            student_management.showerror = original_showerror
    
    def test_database_operations(self):
        """Test database operations (add, view, update, delete)."""
        # Save original connect function
        original_connect = student_management.connect
        # Mock connect
        student_management.connect = MagicMock(return_value=self.conn)
        
        # Save original validation functions
        original_roll_validate = student_management._roll_validate
        original_name_validate = student_management._name_validate
        original_marks_validate = student_management._marks_validate
        
        # Mock validation functions
        student_management._roll_validate = MagicMock(return_value=0)
        student_management._name_validate = MagicMock(return_value=0)
        student_management._marks_validate = MagicMock(return_value=0)
        
        # Save original entry fields
        original_add_ent_rno = student_management.add_ent_rno
        original_add_ent_name = student_management.add_ent_name
        original_add_ent_marks = student_management.add_ent_marks
        
        # Mock entry fields
        mock_add_ent_rno = MagicMock()
        mock_add_ent_name = MagicMock()
        mock_add_ent_marks = MagicMock()
        
        student_management.add_ent_rno = mock_add_ent_rno
        student_management.add_ent_name = mock_add_ent_name
        student_management.add_ent_marks = mock_add_ent_marks
        
        mock_add_ent_rno.get.return_value = "1"
        mock_add_ent_name.get.return_value = "John"
        mock_add_ent_marks.get.return_value = "85"
        
        # Save original showinfo
        original_showinfo = student_management.showinfo
        # Mock showinfo
        mock_showinfo = MagicMock()
        student_management.showinfo = mock_showinfo
        
        try:
            # Test add operation
            student_management.f9()
            
            # Check if record was added
            self.cursor.execute("SELECT * FROM student WHERE rno=1")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 1)
            self.assertEqual(result[1], "John")
            self.assertEqual(result[2], 85)
            
            mock_showinfo.assert_called_once_with('Success', 'record added')
        finally:
            # Restore original references
            student_management.connect = original_connect
            student_management._roll_validate = original_roll_validate
            student_management._name_validate = original_name_validate
            student_management._marks_validate = original_marks_validate
            student_management.add_ent_rno = original_add_ent_rno
            student_management.add_ent_name = original_add_ent_name
            student_management.add_ent_marks = original_add_ent_marks
            student_management.showinfo = original_showinfo

if __name__ == '__main__':
    unittest.main()
