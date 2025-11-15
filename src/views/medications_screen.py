"""
Beautiful Medications screen with Material Design 3 components
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.chip import MDChip
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
from datetime import datetime, time

from views.base_screen import BaseScreen
from src.utils.theme import HealthAppColors


class MedicationsScreen(BaseScreen):
    """Medications management screen"""
    
    def get_screen_title(self) -> str:
        return "My Medications"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["plus", lambda x: self.add_medication()],
            ["bell", lambda x: self.manage_reminders()]
        ]
    
    def setup_content(self):
        """Setup beautiful medications screen content"""
        app = MDApp.get_running_app()
        
        # Create scrollable content
        scroll = ScrollView()
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing="16dp",
            adaptive_height=True,
            padding=["16dp", "8dp", "16dp", "16dp"]
        )
        
        # Quick stats card
        stats_card = self.create_medication_stats_card()
        main_layout.add_widget(stats_card)
        
        # Add medication hero card
        add_card = self.create_add_medication_card()
        main_layout.add_widget(add_card)
        
        # Active medications section
        active_card = self.create_active_medications_card()
        main_layout.add_widget(active_card)
        
        # Medication schedule card
        schedule_card = self.create_schedule_card()
        main_layout.add_widget(schedule_card)
        
        scroll.add_widget(main_layout)
        self.content_layout.add_widget(scroll)
        
        # Load medications
        self.refresh_data()
    
    def create_medication_stats_card(self) -> MDCard:
        """Create enhanced medication statistics card with vibrant colors"""
        app = MDApp.get_running_app()
        
        card = MDCard(
            size_hint_y=None,
            height="130dp",  # Slightly increased for better spacing
            elevation=6,
            padding="20dp",
            md_bg_color=HealthAppColors.CARD_GRADIENT_2
        )
        
        layout = MDBoxLayout(orientation='horizontal', spacing="16dp")
        
        # Enhanced stats with more vibrant colors
        stats = [
            {
                "number": "5", 
                "label": "Active\nMedications", 
                "color": HealthAppColors.MEDICATION,
                "icon": "💊"
            },
            {
                "number": "3", 
                "label": "Due\nToday", 
                "color": HealthAppColors.WARNING,
                "icon": "⏰"
            },
            {
                "number": "2", 
                "label": "Missed\nDoses", 
                "color": HealthAppColors.ERROR,
                "icon": "⚠️"
            }
        ]
        
        for stat in stats:
            # Enhanced stat container with card background
            stat_card = MDCard(
                md_bg_color=(1.0, 1.0, 1.0, 1),
                elevation=3,
                padding="12dp",
                size_hint_x=None,
                width="100dp"
            )
            
            stat_layout = MDBoxLayout(orientation='vertical', spacing="6dp")
            
            # Icon with enhanced styling
            icon_label = MDLabel(
                text=stat["icon"],
                font_size="24sp",
                halign="center",
                size_hint_y=None,
                height="28dp"
            )
            
            # Number with color coordination
            number_label = MDLabel(
                text=stat["number"],
                font_style="H3",
                theme_text_color="Custom", 
                text_color=stat["color"],
                halign="center",
                size_hint_y=None,
                height="32dp",
                bold=True
            )
            
            # Description with proper text handling
            desc_label = MDLabel(
                text=stat["label"],
                font_style="Caption",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height="30dp",
                text_size=("90dp", None),  # Proper width for text wrapping
                valign="middle"
            )
            desc_label.bind(texture_size=desc_label.setter('size'))
            
            stat_layout.add_widget(icon_label)
            stat_layout.add_widget(number_label)
            stat_layout.add_widget(desc_label)
            stat_card.add_widget(stat_layout)
            layout.add_widget(stat_card)
        
        card.add_widget(layout)
        return card
    
    def create_add_medication_card(self) -> MDCard:
        """Create enhanced add medication card with gradient colors"""
        app = MDApp.get_running_app()
        
        card = MDCard(
            md_bg_color=HealthAppColors.MEDICATION,  # Use vibrant medication color
            size_hint_y=None,
            height="100dp",
            elevation=8,  # Higher elevation for prominence
            padding="20dp"
        )
        
        layout = MDBoxLayout(orientation='horizontal', spacing="16dp")
        
        # Text content
        text_layout = MDBoxLayout(orientation='vertical', spacing="4dp")
        
        title = MDLabel(
            text="Add New Medication",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        
        subtitle = MDLabel(
            text="Set up reminders and track your medications",
            font_style="Body2",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            text_size=("200dp", None),  # Enable text wrapping
            halign="left"
        )
        subtitle.bind(texture_size=subtitle.setter('size'))
        
        text_layout.add_widget(title)
        text_layout.add_widget(subtitle)
        layout.add_widget(text_layout)
        
        # Add button
        add_btn = MDIconButton(
            icon="plus-circle",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            icon_size="40dp",
            on_release=lambda x: self.add_medication()
        )
        layout.add_widget(add_btn)
        
        card.add_widget(layout)
        return card
    
    def create_active_medications_card(self) -> MDCard:
        """Create active medications list card"""
        card = MDCard(
            size_hint_y=None,
            height="300dp",
            elevation=4,
            padding="20dp"
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="12dp")
        
        # Title
        title = MDLabel(
            text="Active Medications",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp"
        )
        layout.add_widget(title)
        
        # Medications list
        medications_scroll = ScrollView(size_hint_y=None, height="250dp")
        self.medications_list = MDList()
        medications_scroll.add_widget(self.medications_list)
        layout.add_widget(medications_scroll)
        
        card.add_widget(layout)
        return card
    
    def create_schedule_card(self) -> MDCard:
        """Create today's medication schedule card"""
        card = MDCard(
            size_hint_y=None,
            height="200dp",
            elevation=4,
            padding="20dp"
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="12dp")
        
        # Title
        title = MDLabel(
            text="Today's Schedule",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height="30dp"
        )
        layout.add_widget(title)
        
        # Schedule items
        schedule_layout = MDBoxLayout(orientation='vertical', spacing="8dp")
        
        # Sample schedule items
        schedule_items = [
            {"time": "08:00", "med": "Aspirin 100mg", "status": "taken"},
            {"time": "12:00", "med": "Vitamin D", "status": "due"},
            {"time": "20:00", "med": "Blood Pressure Med", "status": "upcoming"}
        ]
        
        for item in schedule_items:
            item_card = MDCard(
                md_bg_color=(0.95, 0.95, 0.95, 1),
                size_hint_y=None,
                height="40dp",
                elevation=1,
                padding="12dp"
            )
            
            item_layout = MDBoxLayout(orientation='horizontal', spacing="12dp")
            
            time_label = MDLabel(
                text=item["time"],
                font_style="Subtitle2",
                theme_text_color="Primary",
                size_hint_x=None,
                width="60dp",
                bold=True
            )
            
            med_label = MDLabel(
                text=item["med"],
                font_style="Body2",
                theme_text_color="Primary"
            )
            
            # Status indicator
            status_colors = {
                "taken": HealthAppColors.SUCCESS,
                "due": HealthAppColors.WARNING,
                "upcoming": HealthAppColors.INFO
            }
            
            status_chip = MDLabel(
                text="✓" if item["status"] == "taken" else "●",
                theme_text_color="Custom",
                text_color=status_colors.get(item["status"], HealthAppColors.INFO),
                font_size="20sp",
                size_hint_x=None,
                width="30dp"
            )
            
            item_layout.add_widget(time_label)
            item_layout.add_widget(med_label)
            item_layout.add_widget(status_chip)
            item_card.add_widget(item_layout)
            schedule_layout.add_widget(item_card)
        
        layout.add_widget(schedule_layout)
        card.add_widget(layout)
        return card
    
    def refresh_data(self):
        """Refresh medications list"""
        try:
            if hasattr(self, 'medications_list'):
                self.medications_list.clear_widgets()
            
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get active medications (assuming user_id = 1)
            medications = db_service.get_active_medications(1)
            
            if not medications:
                no_meds_label = MDLabel(
                    text="No medications added yet.\nTap 'Add New Medication' to get started.",
                    theme_text_color="Secondary",
                    halign="center"
                )
                self.medications_list.add_widget(no_meds_label)
                return
            
            for medication in medications:
                # Create medication item
                reminder_text = "Reminders ON" if medication.reminder_enabled else "Reminders OFF"
                frequency_text = medication.frequency or "As needed"
                
                item = ThreeLineListItem(
                    text=medication.name,
                    secondary_text=f"Dosage: {medication.dosage or 'Not specified'}",
                    tertiary_text=f"{frequency_text} | {reminder_text}",
                    on_release=lambda x, med_id=medication.id: self.edit_medication(med_id)
                )
                
                self.medications_list.add_widget(item)
                
        except Exception as e:
            self.show_error(f"Failed to load medications: {str(e)}")
    
    def add_medication(self):
        """Show add medication dialog"""
        self.show_medication_dialog()
    
    def edit_medication(self, medication_id: int):
        """Edit existing medication"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get medication details
            with db_service.get_session() as session:
                from models.database_models import Medication
                medication = session.query(Medication).filter_by(id=medication_id).first()
                
                if medication:
                    self.show_medication_dialog(medication)
                else:
                    self.show_error("Medication not found")
                    
        except Exception as e:
            self.show_error(f"Failed to load medication: {str(e)}")
    
    def show_medication_dialog(self, medication=None):
        """Show medication add/edit dialog with proper sizing"""
        # Create form layout with proper sizing
        form_layout = MDBoxLayout(
            orientation='vertical', 
            spacing="12dp",
            size_hint_y=None,
            height="320dp",
            padding="16dp"
        )
        
        # Medication name
        name_field = MDTextField(
            hint_text="Medication Name",
            text=medication.name if medication else "",
            size_hint_y=None,
            height="48dp"
        )
        form_layout.add_widget(name_field)
        
        # Dosage
        dosage_field = MDTextField(
            hint_text="Dosage (e.g., 500mg, 1 tablet)",
            text=medication.dosage if medication else "",
            size_hint_y=None,
            height="48dp"
        )
        form_layout.add_widget(dosage_field)
        
        # Frequency
        frequency_field = MDTextField(
            hint_text="Frequency (e.g., 2 times daily)",
            text=medication.frequency if medication else "",
            size_hint_y=None,
            height="48dp"
        )
        form_layout.add_widget(frequency_field)
        
        # Instructions
        instructions_field = MDTextField(
            hint_text="Instructions (e.g., take with food)",
            text=medication.instructions if medication else "",
            multiline=True,
            size_hint_y=None,
            height="60dp"
        )
        form_layout.add_widget(instructions_field)
        
        # Reminder checkbox with proper layout
        reminder_layout = MDBoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height="40dp",
            spacing="8dp"
        )
        reminder_checkbox = MDCheckbox(
            size_hint_x=None,
            width="40dp",
            active=medication.reminder_enabled if medication else True
        )
        reminder_label = MDLabel(
            text="Enable reminders",
            size_hint_x=None,
            width="150dp",
            theme_text_color="Primary"
        )
        reminder_layout.add_widget(reminder_checkbox)
        reminder_layout.add_widget(reminder_label)
        form_layout.add_widget(reminder_layout)
        
        # Dialog buttons
        def save_medication(instance):
            try:
                # Validate required fields
                if not name_field.text.strip():
                    self.show_error("Medication name is required")
                    return
                
                # Prepare medication data
                med_data = {
                    'user_id': 1,  # Assuming user_id = 1
                    'name': name_field.text.strip(),
                    'dosage': dosage_field.text.strip(),
                    'frequency': frequency_field.text.strip(),
                    'instructions': instructions_field.text.strip(),
                    'reminder_enabled': reminder_checkbox.active,
                    'start_date': datetime.utcnow(),
                    'is_active': True
                }
                
                db_service = self.get_database_service()
                if not db_service:
                    self.show_error("Database service not available")
                    return
                
                if medication:  # Edit existing
                    updated_med = db_service.update_medication(medication.id, med_data)
                    if updated_med:
                        self.show_message(f"Updated {name_field.text}")
                    else:
                        self.show_error("Failed to update medication")
                else:  # Add new
                    new_med = db_service.add_medication(med_data)
                    if new_med:
                        self.show_message(f"Added {name_field.text}")
                        
                        # Setup reminders if enabled
                        if reminder_checkbox.active:
                            self.setup_medication_reminders(new_med.id)
                    else:
                        self.show_error("Failed to add medication")
                
                dialog.dismiss()
                self.refresh_data()
                
            except Exception as e:
                self.show_error(f"Failed to save medication: {str(e)}")
        
        # Create dialog with proper sizing
        dialog = MDDialog(
            title="Add Medication" if not medication else "Edit Medication",
            type="custom",
            content_cls=form_layout,
            size_hint=(0.9, None),  # 90% width, auto height
            height="450dp",  # Fixed height to prevent overflow
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=save_medication
                )
            ]
        )
        
        dialog.open()
    
    def setup_medication_reminders(self, medication_id: int):
        """Setup default reminders for medication"""
        try:
            notification_service = self.get_notification_service()
            if notification_service:
                # Setup default reminder times (e.g., 8 AM, 2 PM, 8 PM)
                default_times = ["08:00", "14:00", "20:00"]
                notification_service.schedule_medication_reminder(medication_id, default_times)
                
        except Exception as e:
            print(f"Error setting up reminders: {e}")
    
    def manage_reminders(self):
        """Show reminders management screen"""
        self.show_message("Reminders management - Coming soon!")
        
        # Here you would show a screen to manage all medication reminders
        # Including setting specific times, enabling/disabling, etc.