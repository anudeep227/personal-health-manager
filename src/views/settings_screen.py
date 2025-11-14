"""
Settings screen for app configuration
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.card import MDCard

from views.base_screen import BaseScreen


class SettingsScreen(BaseScreen):
    """Application settings screen"""
    
    def get_screen_title(self) -> str:
        return "Settings"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["content-save", lambda x: self.save_settings()],
            ["backup-restore", lambda x: self.backup_data()]
        ]
    
    def setup_content(self):
        """Setup settings screen content"""
        # Notifications settings
        notifications_card = self.create_card("Notifications")
        notifications_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Medication reminders
        med_reminder_layout = BoxLayout(orientation='horizontal')
        med_reminder_label = MDLabel(text="Medication Reminders")
        self.med_reminder_switch = MDSwitch(active=True)
        med_reminder_layout.add_widget(med_reminder_label)
        med_reminder_layout.add_widget(self.med_reminder_switch)
        notifications_layout.add_widget(med_reminder_layout)
        
        # Appointment reminders
        appt_reminder_layout = BoxLayout(orientation='horizontal')
        appt_reminder_label = MDLabel(text="Appointment Reminders")
        self.appt_reminder_switch = MDSwitch(active=True)
        appt_reminder_layout.add_widget(appt_reminder_label)
        appt_reminder_layout.add_widget(self.appt_reminder_switch)
        notifications_layout.add_widget(appt_reminder_layout)
        
        notifications_card.add_widget(notifications_layout)
        self.content_layout.add_widget(notifications_card)
        
        # Data & Privacy settings
        privacy_card = self.create_card("Data & Privacy")
        privacy_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Backup setting
        backup_layout = BoxLayout(orientation='horizontal')
        backup_label = MDLabel(text="Auto Backup")
        self.backup_switch = MDSwitch(active=True)
        backup_layout.add_widget(backup_label)
        backup_layout.add_widget(self.backup_switch)
        privacy_layout.add_widget(backup_layout)
        
        # Encryption setting
        encryption_layout = BoxLayout(orientation='horizontal')
        encryption_label = MDLabel(text="Data Encryption")
        self.encryption_switch = MDSwitch(active=True)
        encryption_layout.add_widget(encryption_label)
        encryption_layout.add_widget(self.encryption_switch)
        privacy_layout.add_widget(encryption_layout)
        
        privacy_card.add_widget(privacy_layout)
        self.content_layout.add_widget(privacy_card)
        
        # Actions
        actions_card = self.create_card("Actions")
        actions_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        backup_btn = MDRaisedButton(
            text="Backup Data",
            on_release=lambda x: self.backup_data()
        )
        actions_layout.add_widget(backup_btn)
        
        export_btn = MDRaisedButton(
            text="Export Data",
            on_release=lambda x: self.export_data()
        )
        actions_layout.add_widget(export_btn)
        
        about_btn = MDRaisedButton(
            text="About App",
            on_release=lambda x: self.show_about()
        )
        actions_layout.add_widget(about_btn)
        
        actions_card.add_widget(actions_layout)
        self.content_layout.add_widget(actions_card)
        
        # Load current settings
        self.load_settings()
    
    def load_settings(self):
        """Load current settings from database"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Load settings
            med_reminders = db_service.get_setting('medication_reminders')
            if med_reminders:
                self.med_reminder_switch.active = med_reminders.lower() == 'true'
            
            appt_reminders = db_service.get_setting('appointment_reminders')
            if appt_reminders:
                self.appt_reminder_switch.active = appt_reminders.lower() == 'true'
            
            backup_enabled = db_service.get_setting('backup_enabled')
            if backup_enabled:
                self.backup_switch.active = backup_enabled.lower() == 'true'
            
            encryption_enabled = db_service.get_setting('encryption_enabled')
            if encryption_enabled:
                self.encryption_switch.active = encryption_enabled.lower() == 'true'
                
        except Exception as e:
            self.show_error(f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        """Save settings to database"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                self.show_error("Database service not available")
                return
            
            # Save settings
            db_service.update_setting('medication_reminders', str(self.med_reminder_switch.active).lower())
            db_service.update_setting('appointment_reminders', str(self.appt_reminder_switch.active).lower())
            db_service.update_setting('backup_enabled', str(self.backup_switch.active).lower())
            db_service.update_setting('encryption_enabled', str(self.encryption_switch.active).lower())
            
            self.show_message("Settings saved successfully!")
            
        except Exception as e:
            self.show_error(f"Failed to save settings: {str(e)}")
    
    def backup_data(self):
        """Backup application data"""
        self.show_message("Data backup feature - Coming soon!")
        # Here you would implement data backup functionality
    
    def export_data(self):
        """Export data to file"""
        self.show_message("Data export feature - Coming soon!")
        # Here you would implement data export functionality
    
    def show_about(self):
        """Show about information"""
        config = self.controller.get_config() if self.controller else None
        if config:
            settings = config.get_app_settings()
            about_text = f"{settings['app_name']} v{settings['version']}\n\nA comprehensive health management application."
            self.show_message(about_text)
        else:
            self.show_message("Personal Health Manager v1.0.0")
    
    def refresh_data(self):
        """Refresh settings data"""
        self.load_settings()