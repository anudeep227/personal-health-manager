"""
Database service for managing data operations
"""

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os

from src.models.database_models import Base, User, Medication, MedicationLog, MedicalReport, Appointment, HealthRecord, Settings
from src.utils.config import Config


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        self.config = Config()
        self.engine = None
        self.SessionLocal = None
        
    def initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            # Create SQLAlchemy engine
            database_url = f"sqlite:///{self.config.database_path}"
            self.engine = create_engine(database_url, echo=False)
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            print(f"Database initialized at: {self.config.database_path}")
            
            # Initialize default settings
            self._initialize_default_settings()
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    @contextmanager
    def get_session(self):
        """Get database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def _initialize_default_settings(self):
        """Initialize default application settings"""
        default_settings = [
            ('theme', 'light', 'Application theme'),
            ('notifications_enabled', 'true', 'Enable notifications'),
            ('medication_reminders', 'true', 'Enable medication reminders'),
            ('appointment_reminders', 'true', 'Enable appointment reminders'),
            ('backup_enabled', 'true', 'Enable automatic backups'),
            ('encryption_enabled', 'true', 'Enable data encryption'),
        ]
        
        with self.get_session() as session:
            for key, value, description in default_settings:
                existing = session.query(Settings).filter_by(key=key).first()
                if not existing:
                    setting = Settings(key=key, value=value, description=description)
                    session.add(setting)
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        with self.get_session() as session:
            user = User(**user_data)
            session.add(user)
            session.flush()
            session.refresh(user)
            return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with self.get_session() as session:
            return session.query(User).filter_by(id=user_id).first()
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """Update user information"""
        with self.get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.updated_at = datetime.utcnow()
                session.flush()
                session.refresh(user)
                return user
            return None
    
    # Medication operations
    def add_medication(self, medication_data: Dict[str, Any]) -> Medication:
        """Add a new medication"""
        with self.get_session() as session:
            medication = Medication(**medication_data)
            session.add(medication)
            session.flush()
            session.refresh(medication)
            return medication
    
    def get_active_medications(self, user_id: int) -> List[Medication]:
        """Get all active medications for a user"""
        with self.get_session() as session:
            return session.query(Medication).filter_by(
                user_id=user_id, 
                is_active=True
            ).all()
    
    def update_medication(self, medication_id: int, medication_data: Dict[str, Any]) -> Optional[Medication]:
        """Update medication information"""
        with self.get_session() as session:
            medication = session.query(Medication).filter_by(id=medication_id).first()
            if medication:
                for key, value in medication_data.items():
                    setattr(medication, key, value)
                medication.updated_at = datetime.utcnow()
                session.flush()
                session.refresh(medication)
                return medication
            return None
    
    def log_medication_intake(self, log_data: Dict[str, Any]) -> MedicationLog:
        """Log medication intake"""
        with self.get_session() as session:
            log = MedicationLog(**log_data)
            session.add(log)
            session.flush()
            session.refresh(log)
            return log
    
    # Medical report operations
    def add_medical_report(self, report_data: Dict[str, Any]) -> MedicalReport:
        """Add a new medical report"""
        with self.get_session() as session:
            report = MedicalReport(**report_data)
            session.add(report)
            session.flush()
            session.refresh(report)
            return report
    
    def get_medical_reports(self, user_id: int, category: Optional[str] = None) -> List[MedicalReport]:
        """Get medical reports for a user"""
        with self.get_session() as session:
            query = session.query(MedicalReport).filter_by(user_id=user_id)
            if category:
                query = query.filter_by(category=category)
            return query.order_by(MedicalReport.report_date.desc()).all()
    
    # Appointment operations
    def add_appointment(self, appointment_data: Dict[str, Any]) -> Appointment:
        """Add a new appointment"""
        with self.get_session() as session:
            appointment = Appointment(**appointment_data)
            session.add(appointment)
            session.flush()
            session.refresh(appointment)
            return appointment
    
    def get_upcoming_appointments(self, user_id: int) -> List[Appointment]:
        """Get upcoming appointments for a user"""
        with self.get_session() as session:
            return session.query(Appointment).filter(
                Appointment.user_id == user_id,
                Appointment.appointment_date >= datetime.utcnow(),
                Appointment.status == 'scheduled'
            ).order_by(Appointment.appointment_date).all()
    
    # Health record operations
    def add_health_record(self, record_data: Dict[str, Any]) -> HealthRecord:
        """Add a new health record"""
        with self.get_session() as session:
            record = HealthRecord(**record_data)
            session.add(record)
            session.flush()
            session.refresh(record)
            return record
    
    def get_health_records(self, user_id: int, record_type: Optional[str] = None) -> List[HealthRecord]:
        """Get health records for a user"""
        with self.get_session() as session:
            query = session.query(HealthRecord).filter_by(user_id=user_id)
            if record_type:
                query = query.filter_by(record_type=record_type)
            return query.order_by(HealthRecord.measured_date.desc()).all()
    
    # Settings operations
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        with self.get_session() as session:
            setting = session.query(Settings).filter_by(key=key).first()
            return setting.value if setting else None
    
    def update_setting(self, key: str, value: str) -> None:
        """Update a setting value"""
        with self.get_session() as session:
            setting = session.query(Settings).filter_by(key=key).first()
            if setting:
                setting.value = value
                setting.updated_at = datetime.utcnow()
            else:
                setting = Settings(key=key, value=value)
                session.add(setting)
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            print("Database connection closed.")