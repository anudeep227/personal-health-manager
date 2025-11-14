"""
Health Records screen for tracking vitals and measurements
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, ThreeLineListItem
from datetime import datetime

from views.base_screen import BaseScreen


class HealthRecordsScreen(BaseScreen):
    """Health records and vitals tracking screen"""
    
    def get_screen_title(self) -> str:
        return "Health Records"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["plus", lambda x: self.add_record()],
            ["chart-line", lambda x: self.view_trends()]
        ]
    
    def setup_content(self):
        """Setup health records screen content"""
        # Add record button
        add_btn = MDRaisedButton(
            text="Add New Measurement",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.add_record()
        )
        self.content_layout.add_widget(add_btn)
        
        # Health records list
        records_card = self.create_card("Recent Measurements")
        self.records_list = MDList()
        records_card.add_widget(self.records_list)
        self.content_layout.add_widget(records_card)
        
        # Load records
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh health records list"""
        try:
            self.records_list.clear_widgets()
            
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get health records (assuming user_id = 1)
            records = db_service.get_health_records(1)
            
            if not records:
                no_records_label = MDLabel(
                    text="No health records yet.\nTap 'Add New Measurement' to start tracking.",
                    theme_text_color="Secondary",
                    halign="center"
                )
                self.records_list.add_widget(no_records_label)
                return
            
            for record in records:
                date_str = record.measured_date.strftime("%B %d, %Y")
                unit_str = f" {record.unit}" if record.unit else ""
                
                item = ThreeLineListItem(
                    text=record.record_type.replace('_', ' ').title(),
                    secondary_text=f"Value: {record.value}{unit_str}",
                    tertiary_text=f"Measured: {date_str}",
                    on_release=lambda x, record_id=record.id: self.view_record(record_id)
                )
                
                self.records_list.add_widget(item)
                
        except Exception as e:
            self.show_error(f"Failed to load health records: {str(e)}")
    
    def add_record(self):
        """Add new health record"""
        self.show_message("Add measurement feature - Coming soon!")
        # Here you would implement a dialog to add different types of health measurements
    
    def view_record(self, record_id: int):
        """View record details"""
        self.show_message(f"Viewing record {record_id}")
        # Here you would show detailed record information
    
    def view_trends(self):
        """View health trends and charts"""
        self.show_message("Health trends view - Coming soon!")
        # Here you would show charts and graphs of health data over time