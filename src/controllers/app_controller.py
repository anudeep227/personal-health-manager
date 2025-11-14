"""
Main application controller
"""

from kivy.uix.screenmanager import ScreenManager
from typing import Dict, Any

from src.views.home_screen import HomeScreen
from src.views.profile_screen import ProfileScreen
from src.views.medications_screen import MedicationsScreen
from src.views.reports_screen import ReportsScreen
from src.views.appointments_screen import AppointmentsScreen
from src.views.health_records_screen import HealthRecordsScreen
from src.views.document_analysis_screen import DocumentAnalysisScreen
from src.views.settings_screen import SettingsScreen


class AppController:
    """Main application controller managing screens and navigation"""
    
    def __init__(self, app):
        self.app = app
        self.current_user = None
        self.screens = {}
        
    def setup_screens(self, screen_manager: ScreenManager):
        """Setup all application screens"""
        
        # Initialize screens
        self.screens = {
            'home': HomeScreen(name='home', controller=self),
            'profile': ProfileScreen(name='profile', controller=self),
            'medications': MedicationsScreen(name='medications', controller=self),
            'reports': ReportsScreen(name='reports', controller=self),
            'appointments': AppointmentsScreen(name='appointments', controller=self),
            'health_records': HealthRecordsScreen(name='health_records', controller=self),
            'document_analysis': DocumentAnalysisScreen(name='document_analysis', controller=self),
            'settings': SettingsScreen(name='settings', controller=self),
        }
        
        # Add screens to manager
        for screen in self.screens.values():
            screen_manager.add_widget(screen)
        
        # Set initial screen
        screen_manager.current = 'home'
        
        return screen_manager
    
    def navigate_to(self, screen_name: str):
        """Navigate to a specific screen"""
        if screen_name in self.screens:
            self.app.root.current = screen_name
            
            # Refresh screen data if needed
            screen = self.screens[screen_name]
            if hasattr(screen, 'refresh_data'):
                screen.refresh_data()
        else:
            print(f"Screen '{screen_name}' not found")
    
    def get_database_service(self):
        """Get database service instance"""
        return self.app.db_service
    
    def get_notification_service(self):
        """Get notification service instance"""
        return self.app.notification_service
    
    def get_config(self):
        """Get configuration instance"""
        return self.app.config
    
    def set_current_user(self, user):
        """Set the current user"""
        self.current_user = user
    
    def get_current_user(self):
        """Get the current user"""
        return self.current_user
    
    def show_message(self, title: str, message: str):
        """Show a message dialog"""
        # This would show a popup dialog
        print(f"{title}: {message}")
        
        # Send notification
        if self.app.notification_service:
            self.app.notification_service.send_custom_notification(title, message)
    
    def handle_error(self, error: Exception, context: str = ""):
        """Handle application errors"""
        error_message = f"Error in {context}: {str(error)}" if context else str(error)
        print(f"APPLICATION ERROR: {error_message}")
        self.show_message("Error", "An error occurred. Please try again.")
    
    def on_app_pause(self):
        """Handle app pause event"""
        print("App paused")
        # Save any pending changes
        
    def on_app_resume(self):
        """Handle app resume event"""
        print("App resumed")
        # Refresh data if needed
    
    def get_document_service(self):
        """Get document service instance"""
        if not hasattr(self.app, 'document_service'):
            from src.services.document_service import DocumentService
            self.app.document_service = DocumentService()
        return self.app.document_service
    
    def analyze_document(self, file_path: str, callback=None):
        """Analyze a document and optionally call callback with results"""
        try:
            document_service = self.get_document_service()
            user_id = self.current_user.id if self.current_user else 1
            
            # Perform analysis
            result = document_service.analyze_document_complete(file_path, user_id)
            
            if callback:
                callback(result)
            
            return result
            
        except Exception as e:
            self.handle_error(e, "document analysis")
            return {"error": str(e), "success": False}
    
    def get_user_documents(self, limit: int = 50):
        """Get user's documents"""
        try:
            document_service = self.get_document_service()
            user_id = self.current_user.id if self.current_user else 1
            return document_service.get_user_documents(user_id, limit)
        except Exception as e:
            self.handle_error(e, "getting user documents")
            return []
    
    def search_documents(self, query: str, document_type: str = None):
        """Search user's documents"""
        try:
            document_service = self.get_document_service()
            user_id = self.current_user.id if self.current_user else 1
            return document_service.search_documents(user_id, query, document_type)
        except Exception as e:
            self.handle_error(e, "searching documents")
            return []
    
    def get_document_details(self, document_id: int):
        """Get detailed information about a document"""
        try:
            document_service = self.get_document_service()
            user_id = self.current_user.id if self.current_user else 1
            return document_service.get_document_details(document_id, user_id)
        except Exception as e:
            self.handle_error(e, "getting document details")
            return None
    

        """Handle app resume event"""
        print("App resumed")
        # Refresh data if needed
        current_screen = self.app.root.current
        if current_screen in self.screens:
            screen = self.screens[current_screen]
            if hasattr(screen, 'refresh_data'):
                screen.refresh_data()