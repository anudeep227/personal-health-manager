"""
Home screen - Dashboard with overview of health data
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, TwoLineListItem
from datetime import datetime, timedelta

from views.base_screen import BaseScreen


class HomeScreen(BaseScreen):
    """Home dashboard screen"""
    
    def get_screen_title(self) -> str:
        return "Health Dashboard"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["refresh", lambda x: self.refresh_data()],
            ["bell", lambda x: self.show_notifications()]
        ]
    
    def setup_content(self):
        """Setup home screen content"""
        # Welcome message
        welcome_label = MDLabel(
            text=f"Welcome back! Today is {datetime.now().strftime('%B %d, %Y')}",
            theme_text_color="Primary",
            size_hint_y=None,
            height="40dp"
        )
        self.content_layout.add_widget(welcome_label)
        
        # Quick stats grid
        stats_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height="120dp")
        
        # Medications due today
        med_card = self.create_stat_card("💊", "Medications", "Loading...", lambda: self.navigate_to_screen('medications'))
        stats_grid.add_widget(med_card)
        
        # Upcoming appointments
        appt_card = self.create_stat_card("📅", "Appointments", "Loading...", lambda: self.navigate_to_screen('appointments'))
        stats_grid.add_widget(appt_card)
        
        self.content_layout.add_widget(stats_grid)
        
        # Recent activity
        activity_card = self.create_card("Recent Activity")
        self.activity_list = MDList()
        activity_card.add_widget(self.activity_list)
        self.content_layout.add_widget(activity_card)
        
        # Quick actions
        actions_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height="60dp")
        
        add_med_btn = MDRaisedButton(
            text="Add Medication",
            on_release=lambda x: self.navigate_to_screen('medications')
        )
        actions_layout.add_widget(add_med_btn)
        
        add_report_btn = MDRaisedButton(
            text="Add Report",
            on_release=lambda x: self.navigate_to_screen('reports')
        )
        actions_layout.add_widget(add_report_btn)
        
        analyze_doc_btn = MDRaisedButton(
            text="Analyze Document",
            on_release=lambda x: self.navigate_to_screen('document_analysis')
        )
        actions_layout.add_widget(analyze_doc_btn)
        
        schedule_appt_btn = MDRaisedButton(
            text="Schedule Appointment",
            on_release=lambda x: self.navigate_to_screen('appointments')
        )
        actions_layout.add_widget(schedule_appt_btn)
        
        self.content_layout.add_widget(actions_layout)
        
        # Load initial data
        self.refresh_data()
    
    def create_stat_card(self, icon: str, title: str, value: str, on_tap_callback):
        """Create a stat card widget"""
        card = MDCard(
            size_hint=(1, 1),
            padding=10,
            elevation=2,
            radius=[5],
            on_release=on_tap_callback
        )
        
        card_layout = BoxLayout(orientation='vertical', spacing=5)
        
        # Icon and title
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height="30dp")
        
        icon_label = MDLabel(
            text=icon,
            size_hint_x=None,
            width="30dp",
            font_size="20sp"
        )
        header_layout.add_widget(icon_label)
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            font_size="14sp"
        )
        header_layout.add_widget(title_label)
        
        card_layout.add_widget(header_layout)
        
        # Value
        value_label = MDLabel(
            text=value,
            theme_text_color="Secondary",
            font_size="12sp"
        )
        card_layout.add_widget(value_label)
        
        card.add_widget(card_layout)
        return card
    
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Update medication stats
            self.update_medication_stats()
            
            # Update appointment stats
            self.update_appointment_stats()
            
            # Update recent activity
            self.update_recent_activity()
            
        except Exception as e:
            self.show_error(f"Failed to refresh data: {str(e)}")
    
    def update_medication_stats(self):
        """Update medication statistics"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get current user (assuming user_id = 1 for now)
            current_user_id = 1
            
            # Get active medications
            active_medications = db_service.get_active_medications(current_user_id)
            
            # Count medications due today
            today = datetime.now().date()
            due_today = len([med for med in active_medications if med.reminder_enabled])
            
            # Update the stat card (you'd need to store reference to update it)
            # For now, just log the info
            print(f"Medications due today: {due_today}")
            
        except Exception as e:
            print(f"Error updating medication stats: {e}")
    
    def update_appointment_stats(self):
        """Update appointment statistics"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get current user
            current_user_id = 1
            
            # Get upcoming appointments
            upcoming_appointments = db_service.get_upcoming_appointments(current_user_id)
            
            # Count appointments in next 7 days
            next_week = datetime.now() + timedelta(days=7)
            upcoming_count = len([appt for appt in upcoming_appointments 
                                if appt.appointment_date <= next_week])
            
            print(f"Upcoming appointments: {upcoming_count}")
            
        except Exception as e:
            print(f"Error updating appointment stats: {e}")
    
    def update_recent_activity(self):
        """Update recent activity list"""
        try:
            # Clear existing items
            self.activity_list.clear_widgets()
            
            # Add some sample recent activities
            recent_activities = [
                ("Added medication: Aspirin", "2 hours ago"),
                ("Uploaded lab report", "Yesterday"),
                ("Completed appointment with Dr. Smith", "2 days ago"),
                ("Updated health measurements", "3 days ago")
            ]
            
            for activity, time_ago in recent_activities:
                item = TwoLineListItem(
                    text=activity,
                    secondary_text=time_ago
                )
                self.activity_list.add_widget(item)
                
        except Exception as e:
            print(f"Error updating recent activity: {e}")
    
    def show_notifications(self):
        """Show notifications panel"""
        self.show_message("Checking for new notifications...")
        
        # Here you would typically show a notifications dialog
        # For now, just show a message
        notification_service = self.get_notification_service()
        if notification_service:
            notification_service.send_custom_notification(
                "Health Manager", 
                "You have 2 medications due today"
            )