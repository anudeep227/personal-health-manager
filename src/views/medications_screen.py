"""
Medications screen for managing medications and reminders
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime, time

from views.base_screen import BaseScreen


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
        """Setup medications screen content"""
        # Add medication button
        add_btn = MDRaisedButton(
            text="Add New Medication",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.add_medication()
        )
        self.content_layout.add_widget(add_btn)
        
        # Medications list
        medications_card = self.create_card("Active Medications")
        self.medications_list = MDList()
        medications_card.add_widget(self.medications_list)
        self.content_layout.add_widget(medications_card)
        
        # Load medications
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh medications list"""
        try:
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
        """Show medication add/edit dialog"""
        # Create form layout
        form_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Medication name
        name_field = MDTextField(
            hint_text="Medication Name",
            text=medication.name if medication else ""
        )
        form_layout.add_widget(name_field)
        
        # Dosage
        dosage_field = MDTextField(
            hint_text="Dosage (e.g., 500mg, 1 tablet)",
            text=medication.dosage if medication else ""
        )
        form_layout.add_widget(dosage_field)
        
        # Frequency
        frequency_field = MDTextField(
            hint_text="Frequency (e.g., 2 times daily, every 8 hours)",
            text=medication.frequency if medication else ""
        )
        form_layout.add_widget(frequency_field)
        
        # Instructions
        instructions_field = MDTextField(
            hint_text="Instructions (e.g., take with food)",
            text=medication.instructions if medication else "",
            multiline=True
        )
        form_layout.add_widget(instructions_field)
        
        # Reminder checkbox
        reminder_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height="40dp")
        reminder_checkbox = MDCheckbox(
            size_hint_x=None,
            width="40dp",
            active=medication.reminder_enabled if medication else True
        )
        reminder_label = MDLabel(text="Enable reminders")
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
        
        # Create dialog
        dialog = MDDialog(
            title="Add Medication" if not medication else "Edit Medication",
            type="custom",
            content_cls=form_layout,
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