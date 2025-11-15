#!/usr/bin/env python3
"""
Personal Health Management App
A comprehensive mobile application for managing personal health data,
medical reports, and medication notifications.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior

from controllers.app_controller import AppController
from services.database_service import DatabaseService
from services.notification_service import NotificationService
from utils.config import Config


class HealthApp(MDApp):
    """Main Health Management Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "💊 Personal Health Manager"
        
        # Modern machine/tech theme - dark with neon accents
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"  # Correct palette name
        self.theme_cls.primary_hue = "900"  # Very dark
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.accent_hue = "A400"  # Bright cyan accent
        
        # Initialize services
        self.config = Config()
        self.db_service = DatabaseService()
        self.notification_service = NotificationService()
        self.notification_service.set_database_service(self.db_service)
        self.app_controller = AppController(self)
        
    def build(self):
        """Build the main application"""
        # Initialize database
        self.db_service.initialize_database()
        
        # Create screen manager
        screen_manager = ScreenManager()
        
        # Load screens through controller
        self.app_controller.setup_screens(screen_manager)
        
        return screen_manager
    
    def on_start(self):
        """Called when the app starts"""
        print("Health Management App started successfully!")
        # Start background services
        self.notification_service.start_medication_scheduler()
    
    def on_stop(self):
        """Called when the app stops"""
        print("Health Management App stopped.")
        # Cleanup resources
        self.notification_service.stop_scheduler()
        self.db_service.close_connection()


if __name__ == '__main__':
    HealthApp().run()