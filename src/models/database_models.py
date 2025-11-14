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
    document_analyses = relationship("DocumentAnalysis", back_populates="user")


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


class DocumentAnalysis(Base):
    """Document analysis results and metadata"""
    __tablename__ = 'document_analyses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_name = Column(String(200), nullable=False)
    file_path = Column(String(500))
    file_extension = Column(String(10))
    file_size_bytes = Column(Integer)
    document_type = Column(String(50))  # ecg, blood_test, prescription, radiology, etc.
    confidence_score = Column(Float, default=0.0)
    
    # Processing metadata
    processing_method = Column(String(50))  # tesseract, easyocr, pdfplumber, etc.
    processing_duration = Column(Float)  # seconds
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    # Content
    text_content = Column(Text)
    extracted_data = Column(Text)  # JSON string of structured data
    
    # AI Analysis
    llm_analysis = Column(Text)  # Full AI analysis text
    key_findings = Column(Text)  # JSON string of key findings
    recommendations = Column(Text)  # JSON string of recommendations
    medical_terms = Column(Text)  # JSON string of explained medical terms
    
    # Status and flags
    analysis_status = Column(String(20), default='completed')  # processing, completed, failed
    is_critical = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="document_analyses")


class DocumentTag(Base):
    """Tags for document categorization"""
    __tablename__ = 'document_tags'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document_analyses.id'), nullable=False)
    tag_name = Column(String(50), nullable=False)
    tag_type = Column(String(20), default='user')  # user, system, ai
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("DocumentAnalysis")


class ExtractedMedication(Base):
    """Medications extracted from document analysis"""
    __tablename__ = 'extracted_medications'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document_analyses.id'), nullable=False)
    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(50))
    frequency = Column(String(50))
    duration = Column(String(50))
    instructions = Column(Text)
    extracted_confidence = Column(Float, default=0.0)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_added_to_profile = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("DocumentAnalysis")


class ExtractedLabValue(Base):
    """Lab values extracted from test results"""
    __tablename__ = 'extracted_lab_values'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document_analyses.id'), nullable=False)
    test_name = Column(String(100), nullable=False)
    value = Column(String(50))
    unit = Column(String(20))
    reference_range = Column(String(100))
    is_abnormal = Column(Boolean, default=False)
    abnormal_flag = Column(String(10))  # H, L, *, etc.
    extracted_confidence = Column(Float, default=0.0)
    
    # Clinical context
    clinical_significance = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("DocumentAnalysis")


class DocumentSummary(Base):
    """AI-generated document summaries"""
    __tablename__ = 'document_summaries'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document_analyses.id'), nullable=False, unique=True)
    
    # Summary content
    short_summary = Column(Text)  # 2-3 sentences
    detailed_summary = Column(Text)  # comprehensive summary
    key_points = Column(Text)  # JSON array of key points
    action_items = Column(Text)  # JSON array of action items
    
    # Analysis metadata
    summary_type = Column(String(50))  # ai_generated, manual, hybrid
    model_used = Column(String(50))  # gpt-3.5-turbo, local_model, etc.
    generation_date = Column(DateTime, default=datetime.utcnow)
    
    # Quality metrics
    readability_score = Column(Float)
    accuracy_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    document = relationship("DocumentAnalysis", uselist=False)


class Settings(Base):
    """Application settings"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)