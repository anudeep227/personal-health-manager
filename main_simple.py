#!/usr/bin/env python3
"""
Simplified Health Management App
A basic version to test the core functionality
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

from services.database_service import DatabaseService
from services.notification_service import NotificationService
from utils.config import Config


class HomeScreen(MDScreen):
    """Simple home screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top app bar
        toolbar = MDTopAppBar(
            title="Personal Health Manager",
            elevation=2
        )
        main_layout.add_widget(toolbar)
        
        # Content area
        content_layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            adaptive_height=True
        )
        
        # Welcome card
        welcome_card = MDCard(
            size_hint_y=None,
            height="200dp",
            padding=20,
            elevation=2
        )
        
        card_layout = MDBoxLayout(orientation='vertical', spacing=10)
        
        welcome_label = MDLabel(
            text="Welcome to Personal Health Manager!",
            theme_text_color="Primary",
            size_hint_y=None,
            height="40dp"
        )
        card_layout.add_widget(welcome_label)
        
        description_label = MDLabel(
            text="Your comprehensive health management solution.\nManage medications, appointments, and health records.",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="80dp"
        )
        card_layout.add_widget(description_label)
        
        # Test database button
        test_db_btn = MDRaisedButton(
            text="Test Database",
            size_hint_y=None,
            height="40dp",
            on_release=self.test_database
        )
        card_layout.add_widget(test_db_btn)
        
        welcome_card.add_widget(card_layout)
        content_layout.add_widget(welcome_card)
        
        # Features card
        features_card = MDCard(
            size_hint_y=None,
            height="300dp",
            padding=20,
            elevation=2
        )
        
        features_layout = MDBoxLayout(orientation='vertical', spacing=10)
        
        features_title = MDLabel(
            text="Available Features:",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp"
        )
        features_layout.add_widget(features_title)
        
        features = [
            "✅ Database System - Working",
            "✅ Configuration Management - Working", 
            "✅ Notification Service - Working",
            "🔧 Medication Management - Ready",
            "🔧 Medical Reports - Ready",
            "🔧 Appointment Scheduling - Ready",
            "🔧 Health Records Tracking - Ready"
        ]
        
        for feature in features:
            feature_label = MDLabel(
                text=feature,
                theme_text_color="Secondary",
                size_hint_y=None,
                height="25dp"
            )
            features_layout.add_widget(feature_label)
        
        features_card.add_widget(features_layout)
        content_layout.add_widget(features_card)
        
        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)
    
    def test_database(self, instance):
        """Test database functionality"""
        try:
            # Get the app instance
            app = MDApp.get_running_app()
            db_service = app.db_service
            
            # Test database connection
            with db_service.get_session() as session:
                # Try to get user count
                from models.database_models import User
                user_count = session.query(User).count()
                
                # Show result
                instance.text = f"Database OK! Users: {user_count}"
                
                # Create a test user if none exists
                if user_count == 0:
                    test_user_data = {
                        'first_name': 'Test',
                        'last_name': 'User',
                        'email': 'test@example.com'
                    }
                    test_user = db_service.create_user(test_user_data)
                    instance.text = f"Database OK! Created test user: {test_user.first_name}"
                
        except Exception as e:
            instance.text = f"Database Error: {str(e)}"


class HealthApp(MDApp):
    """Simplified Health Management Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Personal Health Manager"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        # Initialize services
        self.config = Config()
        self.db_service = DatabaseService()
        self.notification_service = NotificationService()
        
    def build(self):
        """Build the application"""
        # Initialize database
        self.db_service.initialize_database()
        
        # Set up notification service
        self.notification_service.set_database_service(self.db_service)
        
        # Create screen manager
        screen_manager = MDScreenManager()
        
        # Add home screen
        home_screen = HomeScreen()
        screen_manager.add_widget(home_screen)
        
        return screen_manager
    
    def on_start(self):
        """Called when the app starts"""
        print("✅ Health Management App started successfully!")
        
        # Send welcome notification
        self.notification_service.send_custom_notification(
            "Health Manager", 
            "Welcome! Your health management app is ready."
        )
    
    def on_stop(self):
        """Called when the app stops"""
        print("Health Management App stopped.")
        # Cleanup resources
        if hasattr(self, 'notification_service'):
            self.notification_service.stop_scheduler()
        if hasattr(self, 'db_service'):
            self.db_service.close_connection()


if __name__ == '__main__':
    HealthApp().run()