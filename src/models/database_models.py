"""
Database models for the Health Management App
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from typing import Optional

Base = declarative_base()


class User(Base):
    """User model for personal information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    gender = Column(String(10))
    blood_group = Column(String(10))
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    emergency_contact = Column(String(100))
    allergies = Column(Text)
    medical_conditions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medications = relationship("Medication", back_populates="user")
    medical_reports = relationship("MedicalReport", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")
    health_records = relationship("HealthRecord", back_populates="user")


class Medication(Base):
    """Medication model for managing medicines"""
    __tablename__ = 'medications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50))
    frequency = Column(String(50))  # e.g., "2 times daily", "every 8 hours"
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    instructions = Column(Text)
    side_effects = Column(Text)
    is_active = Column(Boolean, default=True)
    reminder_enabled = Column(Boolean, default=True)
    reminder_times = Column(String(200))  # JSON string of reminder times
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="medications")
    medication_logs = relationship("MedicationLog", back_populates="medication")


class MedicationLog(Base):
    """Log for tracking medication intake"""
    __tablename__ = 'medication_logs'
    
    id = Column(Integer, primary_key=True)
    medication_id = Column(Integer, ForeignKey('medications.id'), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    taken_time = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, taken, missed, delayed
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    medication = relationship("Medication", back_populates="medication_logs")


class MedicalReport(Base):
    """Medical reports and documents"""
    __tablename__ = 'medical_reports'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(50))  # Lab Report, X-Ray, Prescription, etc.
    doctor_name = Column(String(100))
    hospital_name = Column(String(150))
    report_date = Column(DateTime, nullable=False)
    file_path = Column(String(500))
    file_name = Column(String(200))
    file_size = Column(Integer)
    description = Column(Text)
    tags = Column(String(200))  # comma-separated tags
    is_critical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="medical_reports")


class Appointment(Base):
    """Medical appointments"""
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    doctor_name = Column(String(100))
    hospital_name = Column(String(150))
    appointment_date = Column(DateTime, nullable=False)
    duration = Column(Integer)  # in minutes
    type = Column(String(50))  # consultation, checkup, follow-up, etc.
    status = Column(String(20), default='scheduled')  # scheduled, completed, cancelled
    reminder_enabled = Column(Boolean, default=True)
    reminder_minutes = Column(String(50))  # JSON string of reminder minutes
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="appointments")


class HealthRecord(Base):
    """Health measurements and vitals"""
    __tablename__ = 'health_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    record_type = Column(String(50), nullable=False)  # blood_pressure, weight, temperature, etc.
    value = Column(String(50), nullable=False)
    unit = Column(String(20))
    measured_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_records")


class Settings(Base):
    """Application settings"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)