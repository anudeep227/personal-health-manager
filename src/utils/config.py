"""
Configuration module for the Health Management App
"""

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Application configuration management"""
    
    def __init__(self):
        self.app_dir = Path(__file__).parent.parent
        self.data_dir = self.app_dir / 'data'
        self.assets_dir = self.app_dir / 'assets'
        self.llm_dir = self.app_dir / 'llm'
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.llm_dir.mkdir(exist_ok=True)
    
    @property
    def database_path(self) -> str:
        """Get database file path"""
        return str(self.data_dir / 'health_data.db')
    
    @property
    def reports_dir(self) -> str:
        """Get reports directory path"""
        reports_path = self.data_dir / 'reports'
        reports_path.mkdir(exist_ok=True)
        return str(reports_path)
    
    @property
    def backup_dir(self) -> str:
        """Get backup directory path"""
        backup_path = self.data_dir / 'backups'
        backup_path.mkdir(exist_ok=True)
        return str(backup_path)
    
    def get_app_settings(self) -> Dict[str, Any]:
        """Get application settings"""
        return {
            'app_name': 'Personal Health Manager',
            'version': '1.0.0',
            'theme': 'light',
            'notification_enabled': True,
            'backup_enabled': True,
            'encryption_enabled': True,
            'max_file_size_mb': 50,
            'supported_formats': ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        }
    
    def get_notification_settings(self) -> Dict[str, Any]:
        """Get notification settings"""
        return {
            'medication_reminders': True,
            'appointment_reminders': True,
            'health_checkup_reminders': True,
            'default_reminder_minutes': [30, 60, 1440],  # 30min, 1hr, 1day
            'notification_sound': True,
            'vibration': True
        }