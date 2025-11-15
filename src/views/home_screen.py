"""
Home screen - Beautiful Material Design dashboard with health overview
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.chip import MDChip
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
        """Setup beautiful Material Design home screen content"""
        app = MDApp.get_running_app()
        
        # Create scrollable content
        scroll = ScrollView()
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing="16dp",
            adaptive_height=True,
            padding=["16dp", "8dp", "16dp", "16dp"]
        )
        
        # Set dark background for main layout
        main_layout.md_bg_color = (0.05, 0.05, 0.05, 1)  # Very dark background
        
        # Hero Welcome Card
        hero_card = self.create_hero_welcome_card()
        main_layout.add_widget(hero_card)
        
        # Quick Actions Grid
        actions_card = self.create_quick_actions_card()
        main_layout.add_widget(actions_card)
        
        # Health Overview Cards
        health_overview = self.create_health_overview_section()
        main_layout.add_widget(health_overview)
        
        # Recent Activity Card
        recent_card = self.create_recent_activity_card()
        main_layout.add_widget(recent_card)
        
        scroll.add_widget(main_layout)
        self.content_layout.add_widget(scroll)
        
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
            
            # Recent activity is now handled by the card-based display
            
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
    
    def create_hero_welcome_card(self) -> MDCard:
        """Create beautiful hero welcome card"""
        from src.utils.theme import HealthAppColors
        app = MDApp.get_running_app()
        
        card = MDCard(
            md_bg_color=HealthAppColors.MATRIX_GREEN,  # Use modern matrix green
            size_hint_y=None,
            height="140dp",
            elevation=8,
            padding="24dp",
            radius=[15]
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="8dp")
        
        # Welcome text
        welcome_text = MDLabel(
            text="Good Morning!",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        
        # Date and health tip with proper wrapping
        date_text = MDLabel(
            text=f"Today is {datetime.now().strftime('%A, %B %d')}\nTip: Remember to stay hydrated and take your medications on time!",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            size_hint_y=None,
            height="60dp",
            text_size=("300dp", None),  # Enable text wrapping
            halign="left",
            valign="top"
        )
        date_text.bind(texture_size=date_text.setter('size'))
        
        layout.add_widget(welcome_text)
        layout.add_widget(date_text)
        card.add_widget(layout)
        
        return card
    
    def create_quick_actions_card(self) -> MDCard:
        """Create quick actions card with enhanced Material Design buttons"""
        from src.utils.theme import HealthAppColors
        app = MDApp.get_running_app()
        
        card = MDCard(
            size_hint_y=None,
            height="200dp",
            elevation=4,
            padding="20dp",
            md_bg_color=HealthAppColors.CARD_GRADIENT_4
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="16dp")
        
        # Title
        title = MDLabel(
            text="Quick Actions",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp"
        )
        layout.add_widget(title)
        
        # Actions grid
        actions_grid = GridLayout(cols=2, spacing="12dp", size_hint_y=None, height="140dp")
        
        # Enhanced action buttons with vibrant colors
        actions = [
            {"text": "Add Medication", "color": HealthAppColors.MEDICATION, "screen": "medications"},
            {"text": "Book Appointment", "color": HealthAppColors.APPOINTMENT, "screen": "appointments"},
            {"text": "Upload Report", "color": HealthAppColors.REPORT, "screen": "reports"},
            {"text": "Track Vitals", "color": HealthAppColors.VITAL_SIGNS, "screen": "health_records"}
        ]
        
        for action in actions:
            btn = MDRaisedButton(
                text=action["text"],
                md_bg_color=action["color"],
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="12sp",  # Smaller font for better fit
                elevation=3,
                size_hint_y=None,
                height="50dp",  # Fixed height
                on_press=lambda x, screen=action["screen"]: self.navigate_to_screen(screen)
            )
            actions_grid.add_widget(btn)
        
        layout.add_widget(actions_grid)
        card.add_widget(layout)
        
        return card
    
    def create_health_overview_section(self) -> MDCard:
        """Create enhanced health overview with vibrant statistics"""
        from src.utils.theme import HealthAppColors
        app = MDApp.get_running_app()
        
        card = MDCard(
            size_hint_y=None,
            height="200dp",  # Increased height for better spacing
            elevation=6,
            padding="20dp",
            md_bg_color=(0.15, 0.15, 0.15, 1),  # Dark card background
            radius=[15]
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="16dp")
        
        # Enhanced title with icon
        title = MDLabel(
            text="Health Overview",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp",
            bold=True
        )
        layout.add_widget(title)
        
        # Stats grid with better spacing
        stats_grid = GridLayout(cols=3, spacing="16dp", size_hint_y=None, height="140dp")
        
        # Enhanced health statistics with modern machine colors
        stats = [
            {
                "number": "3", 
                "label": "Medications\nToday",
                "color": HealthAppColors.NEON_PURPLE  # Neon purple
            },
            {
                "number": "1", 
                "label": "Upcoming\nAppt",
                "color": HealthAppColors.CYAN_BLUE  # Bright cyan
            },
            {
                "number": "12", 
                "label": "Health\nRecords",
                "color": HealthAppColors.CYBER_ORANGE  # Cyber orange
            }
        ]
        
        for stat in stats:
            stat_card = MDCard(
                md_bg_color=(0.2, 0.2, 0.2, 1),  # Dark stat card background
                elevation=4,
                padding="12dp",
                radius=[10]
            )
            
            stat_layout = MDBoxLayout(orientation='vertical', spacing="8dp", padding="12dp")
            
            # Just show the number prominently without problematic icons
            number_label = MDLabel(
                text=stat["number"],
                font_style="H3",  # Larger, more prominent
                theme_text_color="Custom",
                text_color=stat["color"],
                halign="center",
                size_hint_y=None,
                height="50dp",
                bold=True
            )
            
            # Description with better text handling
            desc_label = MDLabel(
                text=stat["label"],
                font_style="Body2",
                theme_text_color="Primary",  # Make it more prominent
                halign="center",
                size_hint_y=None,
                height="50dp",
                text_size=("100dp", None),  # Better width for text wrapping
                valign="middle"
            )
            desc_label.bind(texture_size=desc_label.setter('size'))
            
            stat_layout.add_widget(number_label)
            stat_layout.add_widget(desc_label)
            stat_card.add_widget(stat_layout)
            stats_grid.add_widget(stat_card)
        
        layout.add_widget(stats_grid)
        card.add_widget(layout)
        
        return card
    
    def create_recent_activity_card(self) -> MDCard:
        """Create enhanced recent activity card with proper text wrapping and colors"""
        from src.utils.theme import HealthAppColors
        
        card = MDCard(
            size_hint_y=None,
            height="280dp",  # Reduced height to fit better on screen
            elevation=4,
            padding="16dp",
            md_bg_color=(0.15, 0.15, 0.15, 1),  # Dark card background
            radius=[15]
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="12dp")
        
        # Title with enhanced styling
        title = MDLabel(
            text="Recent Activity",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp",
            bold=True
        )
        layout.add_widget(title)
        
        # Activity list with proper scrolling
        activity_scroll = ScrollView(size_hint_y=None, height="220dp")  # Reduced to fit within card
        activity_container = MDBoxLayout(
            orientation='vertical',
            spacing="8dp",
            adaptive_height=True,
            padding="4dp"
        )
        
        # Enhanced sample activities with modern machine colors
        activities = [
            {
                "icon": "MED",
                "primary": "Took Aspirin 100mg",
                "secondary": "2 hours ago",
                "status": "completed",
                "color": HealthAppColors.NEON_PURPLE  # Neon purple
            },
            {
                "icon": "RPT",
                "primary": "Added Blood Test Report",
                "secondary": "Yesterday",
                "status": "completed", 
                "color": HealthAppColors.ELECTRIC_BLUE  # Electric blue
            },
            {
                "icon": "APT",
                "primary": "Cardiology Appointment",
                "secondary": "3 days ago",
                "status": "completed",
                "color": HealthAppColors.CYAN_BLUE  # Bright cyan
            },
            {
                "icon": "REC",
                "primary": "Updated Health Records",
                "secondary": "5 days ago", 
                "status": "completed",
                "color": HealthAppColors.MATRIX_GREEN  # Matrix green
            },
            {
                "icon": "RMD",
                "primary": "Set Medication Reminder",
                "secondary": "1 week ago",
                "status": "completed",
                "color": HealthAppColors.ELECTRIC_YELLOW  # Electric yellow
            }
        ]
        
        for activity in activities:
            # Create activity item card
            item_card = MDCard(
                size_hint_y=None,
                height="60dp",
                elevation=2,
                padding="12dp",
                md_bg_color=(1.0, 1.0, 1.0, 1)
            )
            
            item_layout = MDBoxLayout(
                orientation='horizontal',
                spacing="12dp",
                size_hint_y=None,
                height="36dp"
            )
            
            # Status indicator with safe text
            icon_label = MDLabel(
                text="*",  # Simple asterisk
                font_size="12sp",
                size_hint_x=None,
                width="20dp",
                halign="center",
                valign="center",
                theme_text_color="Custom",
                text_color=activity["color"],
                bold=True
            )
            
            # Activity text content
            text_layout = MDBoxLayout(orientation='vertical', spacing="2dp")
            
            primary_label = MDLabel(
                text=activity["primary"],
                font_style="Subtitle2",
                theme_text_color="Primary",
                size_hint_y=None,
                height="18dp",
                text_size=(None, None),  # Allow text to size naturally
                halign="left",
                valign="center"
            )
            
            secondary_label = MDLabel(
                text=activity["secondary"],
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="14dp",
                text_size=(None, None),  # Allow text to size naturally
                halign="left",
                valign="center"
            )
            
            text_layout.add_widget(primary_label)
            text_layout.add_widget(secondary_label)
            
            # Status indicator with simple text
            status_indicator = MDLabel(
                text="OK",  # Simple text instead of Unicode
                theme_text_color="Custom",
                text_color=activity["color"],
                font_size="10sp",
                size_hint_x=None,
                width="25dp",
                halign="center",
                valign="center",
                bold=True
            )
            
            item_layout.add_widget(icon_label)
            item_layout.add_widget(text_layout)
            item_layout.add_widget(status_indicator)
            item_card.add_widget(item_layout)
            activity_container.add_widget(item_card)
        
        activity_scroll.add_widget(activity_container)
        layout.add_widget(activity_scroll)
        card.add_widget(layout)
        
        return card