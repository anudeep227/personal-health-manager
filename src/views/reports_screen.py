"""
Reports screen for managing medical reports and documents
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, ThreeLineListItem
from datetime import datetime

from views.base_screen import BaseScreen


class ReportsScreen(BaseScreen):
    """Medical reports management screen"""
    
    def get_screen_title(self) -> str:
        return "Medical Reports"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["plus", lambda x: self.add_report()],
            ["folder-open", lambda x: self.open_reports_folder()]
        ]
    
    def setup_content(self):
        """Setup reports screen content"""
        # Add report button
        add_btn = MDRaisedButton(
            text="Add New Report",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.add_report()
        )
        self.content_layout.add_widget(add_btn)
        
        # Reports list
        reports_card = self.create_card("My Reports")
        self.reports_list = MDList()
        reports_card.add_widget(self.reports_list)
        self.content_layout.add_widget(reports_card)
        
        # Load reports
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh reports list"""
        try:
            self.reports_list.clear_widgets()
            
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get medical reports (assuming user_id = 1)
            reports = db_service.get_medical_reports(1)
            
            if not reports:
                no_reports_label = MDLabel(
                    text="No reports added yet.\nTap 'Add New Report' to upload documents.",
                    theme_text_color="Secondary",
                    halign="center"
                )
                self.reports_list.add_widget(no_reports_label)
                return
            
            for report in reports:
                date_str = report.report_date.strftime("%B %d, %Y") if report.report_date else "Unknown date"
                
                item = ThreeLineListItem(
                    text=report.title,
                    secondary_text=f"Category: {report.category or 'General'}",
                    tertiary_text=f"Date: {date_str} | Doctor: {report.doctor_name or 'Not specified'}",
                    on_release=lambda x, report_id=report.id: self.view_report(report_id)
                )
                
                self.reports_list.add_widget(item)
                
        except Exception as e:
            self.show_error(f"Failed to load reports: {str(e)}")
    
    def add_report(self):
        """Add new report"""
        self.show_message("Report upload feature - Coming soon!")
        # Here you would implement file upload functionality
    
    def view_report(self, report_id: int):
        """View report details"""
        self.show_message(f"Viewing report {report_id}")
        # Here you would open the report file or show details
    
    def open_reports_folder(self):
        """Open reports folder"""
        config = self.controller.get_config() if self.controller else None
        if config:
            reports_dir = config.reports_dir
            self.show_message(f"Reports are stored in: {reports_dir}")
        else:
            self.show_message("Unable to access reports folder")