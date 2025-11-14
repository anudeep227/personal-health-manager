"""
Appointments screen for managing medical appointments
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, ThreeLineListItem
from datetime import datetime

from views.base_screen import BaseScreen


class AppointmentsScreen(BaseScreen):
    """Medical appointments management screen"""
    
    def get_screen_title(self) -> str:
        return "Appointments"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["plus", lambda x: self.schedule_appointment()],
            ["calendar", lambda x: self.view_calendar()]
        ]
    
    def setup_content(self):
        """Setup appointments screen content"""
        # Schedule appointment button
        schedule_btn = MDRaisedButton(
            text="Schedule New Appointment",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.schedule_appointment()
        )
        self.content_layout.add_widget(schedule_btn)
        
        # Appointments list
        appointments_card = self.create_card("Upcoming Appointments")
        self.appointments_list = MDList()
        appointments_card.add_widget(self.appointments_list)
        self.content_layout.add_widget(appointments_card)
        
        # Load appointments
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh appointments list"""
        try:
            self.appointments_list.clear_widgets()
            
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get upcoming appointments (assuming user_id = 1)
            appointments = db_service.get_upcoming_appointments(1)
            
            if not appointments:
                no_appointments_label = MDLabel(
                    text="No upcoming appointments.\nTap 'Schedule New Appointment' to add one.",
                    theme_text_color="Secondary",
                    halign="center"
                )
                self.appointments_list.add_widget(no_appointments_label)
                return
            
            for appointment in appointments:
                date_str = appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")
                
                item = ThreeLineListItem(
                    text=appointment.title or "Medical Appointment",
                    secondary_text=f"Doctor: {appointment.doctor_name or 'Not specified'}",
                    tertiary_text=f"Date: {date_str} | Location: {appointment.hospital_name or 'Not specified'}",
                    on_release=lambda x, appt_id=appointment.id: self.view_appointment(appt_id)
                )
                
                self.appointments_list.add_widget(item)
                
        except Exception as e:
            self.show_error(f"Failed to load appointments: {str(e)}")
    
    def schedule_appointment(self):
        """Schedule new appointment"""
        self.show_message("Appointment scheduling - Coming soon!")
        # Here you would implement appointment scheduling dialog
    
    def view_appointment(self, appointment_id: int):
        """View appointment details"""
        self.show_message(f"Viewing appointment {appointment_id}")
        # Here you would show appointment details and options to edit/cancel
    
    def view_calendar(self):
        """View appointments in calendar format"""
        self.show_message("Calendar view - Coming soon!")
        # Here you would show a calendar widget with appointments