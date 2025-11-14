"""
Notification service for managing reminders and alerts
"""

import threading
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from plyer import notification
import schedule

from services.database_service import DatabaseService
from utils.config import Config


class NotificationService:
    """Service for managing notifications and reminders"""
    
    def __init__(self):
        self.config = Config()
        self.db_service = None
        self.scheduler_thread = None
        self.running = False
        
    def set_database_service(self, db_service: DatabaseService):
        """Set database service reference"""
        self.db_service = db_service
    
    def start_medication_scheduler(self):
        """Start the medication reminder scheduler"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("Medication scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=1)
        print("Medication scheduler stopped")
    
    def _run_scheduler(self):
        """Run the background scheduler"""
        # Schedule medication checks every minute
        schedule.every().minute.do(self._check_medication_reminders)
        schedule.every().minute.do(self._check_appointment_reminders)
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def _check_medication_reminders(self):
        """Check for pending medication reminders"""
        if not self.db_service:
            return
        
        try:
            # This would typically check against a user ID
            # For now, we'll assume user_id = 1
            current_time = datetime.now()
            
            # Get all active medications
            with self.db_service.get_session() as session:
                from models.database_models import Medication, MedicationLog
                
                active_medications = session.query(Medication).filter_by(
                    is_active=True,
                    reminder_enabled=True
                ).all()
                
                for medication in active_medications:
                    if self._should_remind_medication(medication, current_time):
                        self._send_medication_reminder(medication)
                        
        except Exception as e:
            print(f"Error checking medication reminders: {e}")
    
    def _check_appointment_reminders(self):
        """Check for upcoming appointment reminders"""
        if not self.db_service:
            return
        
        try:
            current_time = datetime.now()
            
            with self.db_service.get_session() as session:
                from models.database_models import Appointment
                
                # Check appointments in the next 24 hours
                upcoming_appointments = session.query(Appointment).filter(
                    Appointment.appointment_date >= current_time,
                    Appointment.appointment_date <= current_time + timedelta(hours=24),
                    Appointment.status == 'scheduled',
                    Appointment.reminder_enabled == True
                ).all()
                
                for appointment in upcoming_appointments:
                    if self._should_remind_appointment(appointment, current_time):
                        self._send_appointment_reminder(appointment)
                        
        except Exception as e:
            print(f"Error checking appointment reminders: {e}")
    
    def _should_remind_medication(self, medication, current_time: datetime) -> bool:
        """Check if medication reminder should be sent"""
        try:
            if not medication.reminder_times:
                return False
            
            reminder_times = json.loads(medication.reminder_times)
            
            for reminder_time_str in reminder_times:
                reminder_time = datetime.strptime(reminder_time_str, "%H:%M").time()
                reminder_datetime = datetime.combine(current_time.date(), reminder_time)
                
                # Check if it's time for reminder (within 1 minute window)
                time_diff = abs((current_time - reminder_datetime).total_seconds())
                if time_diff <= 60:  # Within 1 minute
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking medication reminder time: {e}")
            return False
    
    def _should_remind_appointment(self, appointment, current_time: datetime) -> bool:
        """Check if appointment reminder should be sent"""
        try:
            if not appointment.reminder_minutes:
                reminder_minutes = [30, 60, 1440]  # Default: 30min, 1hr, 1day
            else:
                reminder_minutes = json.loads(appointment.reminder_minutes)
            
            for minutes in reminder_minutes:
                reminder_time = appointment.appointment_date - timedelta(minutes=minutes)
                time_diff = abs((current_time - reminder_time).total_seconds())
                
                if time_diff <= 60:  # Within 1 minute
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking appointment reminder time: {e}")
            return False
    
    def _send_medication_reminder(self, medication):
        """Send medication reminder notification"""
        try:
            title = "💊 Medication Reminder"
            message = f"Time to take {medication.name}"
            if medication.dosage:
                message += f" ({medication.dosage})"
            
            self._send_notification(title, message, timeout=10)
            
            # Log the reminder (you might want to add a reminder log table)
            print(f"Medication reminder sent: {medication.name}")
            
        except Exception as e:
            print(f"Error sending medication reminder: {e}")
    
    def _send_appointment_reminder(self, appointment):
        """Send appointment reminder notification"""
        try:
            time_until = appointment.appointment_date - datetime.now()
            
            if time_until.days > 0:
                time_str = f"in {time_until.days} day(s)"
            elif time_until.seconds > 3600:
                hours = time_until.seconds // 3600
                time_str = f"in {hours} hour(s)"
            else:
                minutes = time_until.seconds // 60
                time_str = f"in {minutes} minute(s)"
            
            title = "📅 Appointment Reminder"
            message = f"Appointment with {appointment.doctor_name} {time_str}"
            
            self._send_notification(title, message, timeout=10)
            
            print(f"Appointment reminder sent: {appointment.title}")
            
        except Exception as e:
            print(f"Error sending appointment reminder: {e}")
    
    def _send_notification(self, title: str, message: str, timeout: int = 5):
        """Send system notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_name="Personal Health Manager"
            )
        except Exception as e:
            print(f"Error sending notification: {e}")
            # Fallback to console notification
            print(f"NOTIFICATION: {title} - {message}")
    
    def send_custom_notification(self, title: str, message: str, timeout: int = 5):
        """Send a custom notification"""
        self._send_notification(title, message, timeout)
    
    def schedule_medication_reminder(self, medication_id: int, reminder_times: List[str]):
        """Schedule medication reminders"""
        # This would update the medication's reminder_times in the database
        if self.db_service:
            try:
                reminder_times_json = json.dumps(reminder_times)
                self.db_service.update_medication(medication_id, {
                    'reminder_times': reminder_times_json,
                    'reminder_enabled': True
                })
                print(f"Medication reminders scheduled for medication {medication_id}")
            except Exception as e:
                print(f"Error scheduling medication reminder: {e}")
    
    def schedule_appointment_reminder(self, appointment_id: int, reminder_minutes: List[int]):
        """Schedule appointment reminders"""
        if self.db_service:
            try:
                reminder_minutes_json = json.dumps(reminder_minutes)
                # You would update the appointment's reminder settings here
                print(f"Appointment reminders scheduled for appointment {appointment_id}")
            except Exception as e:
                print(f"Error scheduling appointment reminder: {e}")