"""
Document Analysis Screen for Health Management App
Allows users to upload and analyze medical documents, images, PDFs, etc.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import threading
import os
from typing import Dict, Any, Optional

from src.views.base_screen import BaseScreen
from src.services.document_processing_service import DocumentProcessingService
from llm.health_llm_service import HealthLLMService


class DocumentAnalysisScreen(BaseScreen):
    """Screen for uploading and analyzing medical documents"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Document Analysis"
        self.document_service = DocumentProcessingService()
        self.llm_service = HealthLLMService()
        self.file_manager = None
        self.current_file_path = None
        self.analysis_dialog = None
        self.progress_dialog = None
        
        self.build_ui()
    
    def build_ui(self):
        """Build the document analysis interface"""
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20
        )
        
        # Header card
        header_card = self.create_header_card()
        main_layout.add_widget(header_card)
        
        # Upload section
        upload_card = self.create_upload_section()
        main_layout.add_widget(upload_card)
        
        # Recent documents section
        recent_card = self.create_recent_documents_section()
        main_layout.add_widget(recent_card)
        
        # Analysis results section
        results_card = self.create_results_section()
        main_layout.add_widget(results_card)
        
        scroll = ScrollView()
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def create_header_card(self) -> MDCard:
        """Create header information card"""
        card = MDCard(
            size_hint_y=None,
            height="120dp",
            padding=20,
            md_bg_color=self.theme_cls.primary_color,
            elevation=3
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="Document Analysis",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.6
        )
        
        subtitle = Label(
            text="Upload medical documents, reports, images, or PDFs for AI-powered analysis",
            font_size="14sp",
            color=(0.9, 0.9, 0.9, 1),
            text_size=(None, None),
            size_hint_y=0.4
        )
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        card.add_widget(layout)
        
        return card
    
    def create_upload_section(self) -> MDCard:
        """Create document upload section"""
        card = MDCard(
            size_hint_y=None,
            height="200dp",
            padding=20,
            elevation=2
        )
        
        layout = BoxLayout(orientation='vertical', spacing=15)
        
        # Upload button
        upload_btn = MDRaisedButton(
            text="Select Document",
            icon="file-upload",
            on_release=self.open_file_manager,
            size_hint_y=None,
            height="48dp"
        )
        
        # Supported formats info
        formats_text = "Supported: PDF, DOCX, Images (JPG, PNG), Text files"
        formats_label = Label(
            text=formats_text,
            font_size="12sp",
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=None,
            height="30dp"
        )
        
        # Selected file display
        self.selected_file_label = Label(
            text="No file selected",
            font_size="14sp",
            size_hint_y=None,
            height="40dp"
        )
        
        # Analyze button
        self.analyze_btn = MDRaisedButton(
            text="Analyze Document",
            icon="brain",
            on_release=self.start_analysis,
            disabled=True,
            size_hint_y=None,
            height="48dp"
        )
        
        layout.add_widget(upload_btn)
        layout.add_widget(formats_label)
        layout.add_widget(self.selected_file_label)
        layout.add_widget(self.analyze_btn)
        
        card.add_widget(layout)
        return card
    
    def create_recent_documents_section(self) -> MDCard:
        """Create recent documents section"""
        card = MDCard(
            size_hint_y=None,
            height="200dp",
            padding=20,
            elevation=2
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="Recent Analyses",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height="30dp"
        )
        
        # Placeholder for recent documents list
        self.recent_list = BoxLayout(
            orientation='vertical',
            spacing=5
        )
        
        # Populate with sample data
        self.load_recent_documents()
        
        scroll_recent = ScrollView(size_hint_y=0.8)
        scroll_recent.add_widget(self.recent_list)
        
        layout.add_widget(title)
        layout.add_widget(scroll_recent)
        
        card.add_widget(layout)
        return card
    
    def create_results_section(self) -> MDCard:
        """Create analysis results section"""
        card = MDCard(
            size_hint_y=None,
            height="300dp",
            padding=20,
            elevation=2
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="Analysis Results",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height="30dp"
        )
        
        # Results display area
        self.results_scroll = ScrollView()
        self.results_content = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.results_content.bind(minimum_height=self.results_content.setter('height'))
        
        self.results_scroll.add_widget(self.results_content)
        
        # Initially show placeholder
        placeholder = Label(
            text="Upload and analyze a document to see results here",
            font_size="14sp",
            color=(0.6, 0.6, 0.6, 1),
            text_size=(None, None)
        )
        self.results_content.add_widget(placeholder)
        
        layout.add_widget(title)
        layout.add_widget(self.results_scroll)
        
        card.add_widget(layout)
        return card
    
    def open_file_manager(self, *args):
        """Open file manager for document selection"""
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_file_manager,
                select_path=self.select_file_path,
                preview=False,
            )
        
        # Set initial path to Documents or home directory
        home_path = os.path.expanduser("~")
        documents_path = os.path.join(home_path, "Documents")
        initial_path = documents_path if os.path.exists(documents_path) else home_path
        
        self.file_manager.show(initial_path)
    
    def select_file_path(self, path: str):
        """Handle file selection"""
        self.exit_file_manager()
        
        # Validate file
        is_valid, message = self.document_service.validate_file(path)
        
        if is_valid:
            self.current_file_path = path
            filename = os.path.basename(path)
            self.selected_file_label.text = f"Selected: {filename}"
            self.analyze_btn.disabled = False
            toast(f"File selected: {filename}")
        else:
            toast(f"Invalid file: {message}")
            self.current_file_path = None
            self.selected_file_label.text = "No file selected"
            self.analyze_btn.disabled = True
    
    def exit_file_manager(self, *args):
        """Close file manager"""
        if self.file_manager:
            self.file_manager.close()
    
    def start_analysis(self, *args):
        """Start document analysis in background thread"""
        if not self.current_file_path:
            toast("Please select a file first")
            return
        
        # Show progress dialog
        self.show_progress_dialog()
        
        # Start analysis in background thread
        threading.Thread(
            target=self.analyze_document_background,
            daemon=True
        ).start()
    
    def show_progress_dialog(self):
        """Show analysis progress dialog"""
        content = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint_y=None,
            height="100dp"
        )
        
        progress_label = Label(
            text="Processing document...",
            size_hint_y=None,
            height="30dp"
        )
        
        progress_bar = MDProgressBar()
        progress_bar.start()
        
        content.add_widget(progress_label)
        content.add_widget(progress_bar)
        
        self.progress_dialog = MDDialog(
            title="Analyzing Document",
            type="custom",
            content_cls=content,
            auto_dismiss=False
        )
        self.progress_dialog.open()
    
    def analyze_document_background(self):
        """Perform document analysis in background thread"""
        try:
            # Step 1: Process document
            document_data = self.document_service.process_document(self.current_file_path)
            
            # Step 2: Analyze with LLM
            if not document_data.get('error'):
                llm_analysis = self.llm_service.analyze_document_comprehensive(document_data)
                document_data['llm_analysis'] = llm_analysis
            
            # Step 3: Update UI on main thread
            Clock.schedule_once(
                lambda dt: self.display_analysis_results(document_data),
                0
            )
                
        except Exception as e:
            # Handle errors on main thread
            Clock.schedule_once(
                lambda dt: self.handle_analysis_error(str(e)),
                0
            )
    
    def display_analysis_results(self, results: Dict[str, Any]):
        """Display analysis results in UI"""
        # Close progress dialog
        if self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None
        
        # Clear previous results
        self.results_content.clear_widgets()
        
        if results.get('error'):
            error_label = Label(
                text=f"Analysis Error: {results['error']}",
                color=(1, 0, 0, 1),
                text_size=(None, None)
            )
            self.results_content.add_widget(error_label)
            return
        
        # Document info
        doc_info = self.create_document_info_widget(results)
        self.results_content.add_widget(doc_info)
        
        # LLM Analysis
        if 'llm_analysis' in results:
            llm_widget = self.create_llm_analysis_widget(results['llm_analysis'])
            self.results_content.add_widget(llm_widget)
        
        # Extracted text preview
        if results.get('text_content'):
            text_widget = self.create_text_preview_widget(results['text_content'])
            self.results_content.add_widget(text_widget)
        
        toast("Analysis completed successfully!")
    
    def create_document_info_widget(self, results: Dict[str, Any]) -> MDCard:
        """Create document information widget"""
        card = MDCard(
            size_hint_y=None,
            padding=15,
            elevation=1
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="Document Information",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="25dp"
        )
        
        info_text = f"""
File: {results.get('file_name', 'Unknown')}
Type: {results.get('document_type', 'Unknown')}
Size: {results.get('file_size_bytes', 0) / 1024:.1f} KB
Confidence: {results.get('confidence_score', 0):.1%}
Processed: {results.get('processed_at', 'Unknown')}
        """.strip()
        
        info_label = Label(
            text=info_text,
            font_size="12sp",
            text_size=(None, None),
            valign='top'
        )
        
        layout.add_widget(title)
        layout.add_widget(info_label)
        
        # Auto-size the card
        layout.bind(minimum_height=layout.setter('height'))
        card.height = layout.minimum_height + 30
        
        card.add_widget(layout)
        return card
    
    def create_llm_analysis_widget(self, analysis: Dict[str, Any]) -> MDCard:
        """Create LLM analysis results widget"""
        card = MDCard(
            size_hint_y=None,
            padding=15,
            elevation=1
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="AI Analysis",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="25dp"
        )
        
        # Analysis text
        analysis_text = analysis.get('analysis', 'No analysis available')
        analysis_label = Label(
            text=analysis_text,
            font_size="12sp",
            text_size=(None, None),
            valign='top'
        )
        
        # Disclaimer
        disclaimer = analysis.get('disclaimer', 'Consult healthcare professionals for medical advice.')
        disclaimer_label = Label(
            text=f"Disclaimer: {disclaimer}",
            font_size="10sp",
            italic=True,
            color=(0.7, 0.7, 0.7, 1),
            text_size=(None, None),
            valign='top'
        )
        
        layout.add_widget(title)
        layout.add_widget(analysis_label)
        layout.add_widget(disclaimer_label)
        
        # Auto-size the card
        layout.bind(minimum_height=layout.setter('height'))
        card.height = layout.minimum_height + 30
        
        card.add_widget(layout)
        return card
    
    def create_text_preview_widget(self, text_content: str) -> MDCard:
        """Create text content preview widget"""
        card = MDCard(
            size_hint_y=None,
            padding=15,
            elevation=1
        )
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        title = Label(
            text="Extracted Text (Preview)",
            font_size="16sp",
            bold=True,
            size_hint_y=None,
            height="25dp"
        )
        
        # Truncate text for preview
        preview_text = text_content[:500] + "..." if len(text_content) > 500 else text_content
        
        text_label = Label(
            text=preview_text,
            font_size="10sp",
            text_size=(None, None),
            valign='top'
        )
        
        layout.add_widget(title)
        layout.add_widget(text_label)
        
        # Auto-size the card
        layout.bind(minimum_height=layout.setter('height'))
        card.height = layout.minimum_height + 30
        
        card.add_widget(layout)
        return card
    
    def handle_analysis_error(self, error_message: str):
        """Handle analysis errors"""
        if self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None
        
        toast(f"Analysis failed: {error_message}")
        
        # Show error in results
        self.results_content.clear_widgets()
        error_label = Label(
            text=f"Analysis Error: {error_message}",
            color=(1, 0, 0, 1),
            text_size=(None, None)
        )
        self.results_content.add_widget(error_label)
    
    def load_recent_documents(self):
        """Load recent document analyses"""
        # Placeholder - in real app, load from database
        recent_items = [
            ("Blood Test Results", "Analyzed 2 days ago", "blood_test"),
            ("ECG Report", "Analyzed 1 week ago", "ecg"),
            ("Prescription", "Analyzed 2 weeks ago", "prescription")
        ]
        
        for title, subtitle, doc_type in recent_items:
            item = TwoLineListItem(
                text=title,
                secondary_text=subtitle,
                on_release=lambda x, dt=doc_type: self.view_recent_analysis(dt)
            )
            self.recent_list.add_widget(item)
    
    def view_recent_analysis(self, doc_type: str):
        """View a recent analysis"""
        toast(f"Viewing {doc_type} analysis (feature coming soon)")
    
    def on_enter(self):
        """Called when screen is entered"""
        super().on_enter()
        # Refresh recent documents when entering screen
        self.recent_list.clear_widgets()
        self.load_recent_documents()