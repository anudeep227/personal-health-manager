"""
Basic tests for the Health Management App
"""

import sys
import os
import unittest
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import Config


class TestConfig(unittest.TestCase):
    """Test configuration module"""
    
    def setUp(self):
        self.config = Config()
    
    def test_config_initialization(self):
        """Test that config initializes properly"""
        self.assertIsNotNone(self.config)
        self.assertTrue(os.path.exists(self.config.data_dir))
    
    def test_app_settings(self):
        """Test app settings"""
        settings = self.config.get_app_settings()
        self.assertIn('app_name', settings)
        self.assertEqual(settings['app_name'], 'Personal Health Manager')
    
    def test_notification_settings(self):
        """Test notification settings"""
        settings = self.config.get_notification_settings()
        self.assertIn('medication_reminders', settings)
        self.assertTrue(settings['medication_reminders'])


class TestDatabaseService(unittest.TestCase):
    """Test database service"""
    
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
    def test_import_database_service(self):
        """Test that database service can be imported"""
        try:
            from services.database_service import DatabaseService
            db_service = DatabaseService()
            self.assertIsNotNone(db_service)
        except ImportError as e:
            self.fail(f"Could not import DatabaseService: {e}")


if __name__ == '__main__':
    # Run tests
    unittest.main()