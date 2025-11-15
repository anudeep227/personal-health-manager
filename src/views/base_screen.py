"""
Base screen class for all application screens
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerMenu
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast


class BaseScreen(Screen):
    """Base screen with common functionality"""
    
    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.toolbar = None
        self.main_layout = None
        self.content_layout = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup basic UI structure"""
        # Main vertical layout
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Top toolbar
        self.setup_toolbar()
        
        # Content area
        self.content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.main_layout.add_widget(self.content_layout)
        
        # Add main layout to screen
        self.add_widget(self.main_layout)
        
        # Setup screen-specific content
        self.setup_content()
    
    def setup_toolbar(self):
        """Setup top toolbar"""
        self.toolbar = MDTopAppBar(
            title=self.get_screen_title(),
            left_action_items=[["menu", lambda x: self.open_navigation_drawer()]],
            right_action_items=self.get_toolbar_actions()
        )
        self.main_layout.add_widget(self.toolbar)
    
    def setup_content(self):
        """Override this method to setup screen-specific content"""
        pass
    
    def get_screen_title(self) -> str:
        """Override to return screen title"""
        return "Health Manager"
    
    def get_toolbar_actions(self) -> list:
        """Override to return toolbar action items"""
        return []
    
    def open_navigation_drawer(self):
        """Open navigation drawer with sliding animation"""
        if self.controller:
            # Create navigation menu
            menu_items = [
                ("Home", "home"),
                ("Profile", "profile"),
                ("Medications", "medications"),
                ("Reports", "reports"),
                ("Appointments", "appointments"),
                ("Health Records", "health_records"),
                ("Settings", "settings"),
            ]
            
            # Show navigation options with sliding drawer
            self.show_sliding_navigation(menu_items)
    
    def show_sliding_navigation(self, menu_items):
        """Show navigation menu with sliding animation"""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.list import MDList, OneLineIconListItem
        from kivymd.uix.scrollview import MDScrollView
        from kivy.animation import Animation
        from src.utils.theme import HealthAppColors
        
        # Create sliding menu panel
        if not hasattr(self, 'nav_panel'):
            self.nav_panel = MDCard(
                size_hint=(None, 1),
                width=0,  # Start hidden - use numeric value for animation
                md_bg_color=(0.12, 0.12, 0.12, 0.95),  # Modern dark background
                elevation=16,
                radius=[0, 16, 16, 0],
                pos_hint={'x': 0, 'y': 0}
            )
            
            # Panel content
            panel_layout = MDBoxLayout(
                orientation='vertical',
                spacing="8dp",
                padding="16dp"
            )
            
            # Header with modern gradient
            header = MDCard(
                size_hint_y=None,
                height="100dp",
                md_bg_color=(0.1, 0.1, 0.1, 1),  # Modern dark header
                elevation=0,
                padding="16dp",
                radius=[8]
            )
            
            header_label = MDLabel(
                text="Health Manager\nNavigation",
                font_style="H6",
                theme_text_color="Custom",
                text_color=(0.9, 0.9, 0.9, 1),  # Light text on dark
                bold=True,
                halign="left"
            )
            header.add_widget(header_label)
            panel_layout.add_widget(header)
            
            # Scrollable menu
            scroll = MDScrollView()
            menu_layout = MDBoxLayout(
                orientation='vertical',
                spacing="4dp",
                adaptive_height=True
            )
            
            # Modern machine/tech colors - dark theme with neon accents
            colors = [
                (0.0, 0.8, 0.4, 1),      # Matrix green - Home
                (0.2, 0.6, 1.0, 1),      # Electric blue - Profile  
                (0.8, 0.2, 1.0, 1),      # Neon purple - Medications
                (1.0, 0.3, 0.0, 1),      # Cyber orange - Reports
                (0.0, 1.0, 1.0, 1),      # Cyan blue - Appointments
                (1.0, 0.0, 0.5, 1),      # Hot pink - Health Records
                (0.7, 0.7, 0.0, 1)       # Electric yellow - Settings
            ]
            
            for i, (title, screen_name) in enumerate(menu_items):
                # Create transparent version of color for dark theme
                base_color = colors[i % len(colors)]
                transparent_color = (base_color[0], base_color[1], base_color[2], 0.25)  # Slightly more visible on dark
                
                item = MDCard(
                    size_hint_y=None,
                    height="48dp",
                    md_bg_color=transparent_color,  # Properly formatted transparent color
                    radius=[8],
                    elevation=2,
                    padding="12dp",
                    on_release=lambda x, screen=screen_name: self._slide_navigate(screen)
                )
                
                item_layout = MDBoxLayout(orientation='horizontal', spacing="12dp")
                
                # Icon (first letter)
                icon = MDLabel(
                    text=title[0],
                    size_hint_x=None,
                    width="30dp",
                    font_style="H6",
                    theme_text_color="Custom",
                    text_color=colors[i % len(colors)],
                    halign="center",
                    bold=True
                )
                
                # Title
                title_label = MDLabel(
                    text=title,
                    font_style="Subtitle1",
                    theme_text_color="Custom",
                    text_color=(0.9, 0.9, 0.9, 1),  # Light text for dark theme
                    valign="center"
                )
                
                item_layout.add_widget(icon)
                item_layout.add_widget(title_label)
                item.add_widget(item_layout)
                menu_layout.add_widget(item)
            
            scroll.add_widget(menu_layout)
            panel_layout.add_widget(scroll)
            self.nav_panel.add_widget(panel_layout)
            
            # Add to main layout
            self.main_layout.add_widget(self.nav_panel)
        
        # Animate slide in/out with numeric values
        from kivy.metrics import dp
        if self.nav_panel.width == 0:
            anim = Animation(width=dp(280), duration=0.3, t="out_quart")
            anim.start(self.nav_panel)
        else:
            # Slide out
            anim = Animation(width=0, duration=0.3, t="out_quart")
            anim.start(self.nav_panel)
    
    def _slide_navigate(self, screen_name):
        """Navigate and close sliding menu"""
        # Close menu first
        if hasattr(self, 'nav_panel'):
            anim = Animation(width=0, duration=0.3, t="out_quart")
            anim.start(self.nav_panel)
        
        # Navigate
        self.navigate_to_screen(screen_name)
    
    def navigate_to_screen(self, screen_name):
        """Navigate to specified screen"""
        if self.controller:
            self.controller.navigate_to(screen_name)
    
    def show_message(self, message: str, duration: int = 3):
        """Show snackbar message"""
        snackbar = Snackbar(text=message, duration=duration)
        snackbar.open()
    
    def show_error(self, error_message: str):
        """Show error message"""
        self.show_message(f"Error: {error_message}")
    
    def refresh_data(self):
        """Override to refresh screen data"""
        pass
    
    def get_database_service(self):
        """Get database service from controller"""
        if self.controller:
            return self.controller.get_database_service()
        return None
    
    def get_notification_service(self):
        """Get notification service from controller"""
        if self.controller:
            return self.controller.get_notification_service()
        return None
    
    def create_card(self, title: str = "", content_widget=None) -> MDCard:
        """Create a material design card"""
        card = MDCard(
            size_hint=(1, None),
            height="200dp",
            padding=10,
            spacing=10,
            elevation=2,
            radius=[5]
        )
        
        card_layout = BoxLayout(orientation='vertical', spacing=5)
        
        if title:
            title_label = MDLabel(
                text=title,
                theme_text_color="Primary",
                size_hint_y=None,
                height="30dp"
            )
            card_layout.add_widget(title_label)
        
        if content_widget:
            card_layout.add_widget(content_widget)
        
        card.add_widget(card_layout)
        return card
    
    def show_beautiful_dialog(self, title: str, message: str, dialog_type: str = "info", 
                             confirm_callback=None, cancel_callback=None):
        """Show a beautiful Material Design dialog"""
        app = MDApp.get_running_app()
        
        # Choose icon and colors based on dialog type
        dialog_configs = {
            "info": {"icon": "information", "color": app.theme_cls.primary_color},
            "success": {"icon": "check-circle", "color": (0.3, 0.8, 0.3, 1)},
            "warning": {"icon": "alert", "color": (0.9, 0.7, 0.2, 1)},
            "error": {"icon": "alert-circle", "color": (0.9, 0.3, 0.3, 1)},
            "question": {"icon": "help-circle", "color": app.theme_cls.accent_color}
        }
        
        config = dialog_configs.get(dialog_type, dialog_configs["info"])
        
        # Create dialog content
        content = MDBoxLayout(
            orientation="vertical",
            spacing="16dp",
            size_hint_y=None,
            height="140dp",  # Increased height to accommodate larger text
            padding="20dp"
        )
        
        # Message text with proper wrapping
        message_label = MDLabel(
            text=message,
            theme_text_color="Primary",
            font_style="Body1",
            halign="left",
            valign="top",
            text_size=("300dp", None),  # Increased width for better text wrapping
            size_hint_y=None,
            height="100dp",  # Increased height
            markup=True  # Enable markup for better text formatting
        )
        message_label.bind(texture_size=message_label.setter('size'))
        content.add_widget(message_label)
        
        # Create buttons
        buttons = []
        
        if confirm_callback or cancel_callback:
            # Confirmation dialog
            if cancel_callback:
                cancel_btn = MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.disabled_hint_text_color,
                    on_release=lambda x: self._close_dialog_and_callback(cancel_callback)
                )
                buttons.append(cancel_btn)
            
            if confirm_callback:
                confirm_btn = MDRaisedButton(
                    text="Confirm",
                    md_bg_color=config["color"],
                    on_release=lambda x: self._close_dialog_and_callback(confirm_callback)
                )
                buttons.append(confirm_btn)
        else:
            # Simple OK dialog
            ok_btn = MDRaisedButton(
                text="OK",
                md_bg_color=config["color"],
                on_release=lambda x: self._close_dialog()
            )
            buttons.append(ok_btn)
        
        # Create and show dialog with proper sizing
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=buttons,
            size_hint=(0.9, None),  # Wider for better text display
            height="320dp",  # Adjusted height to accommodate larger content
            elevation=8,
            auto_dismiss=False  # Prevent accidental dismissal
        )
        
        self.dialog.open()
    
    def _close_dialog_and_callback(self, callback):
        """Close dialog and execute callback"""
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()
        if callback:
            callback()
    
    def _close_dialog(self):
        """Close dialog"""
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()
    
    def show_success_message(self, message: str):
        """Show success toast and dialog"""
        toast(f"✅ {message}")
        self.show_beautiful_dialog("Success", message, "success")
    
    def show_error_message(self, message: str):
        """Show error toast and dialog"""
        toast(f"❌ {message}")
        self.show_beautiful_dialog("Error", message, "error")
    
    def show_warning_message(self, message: str):
        """Show warning toast and dialog"""
        toast(f"⚠️ {message}")
        self.show_beautiful_dialog("Warning", message, "warning")
    
    def show_confirmation_dialog(self, title: str, message: str, confirm_callback, cancel_callback=None):
        """Show confirmation dialog"""
        self.show_beautiful_dialog(title, message, "question", confirm_callback, cancel_callback)
    
    def show_loading_dialog(self, message: str = "Loading..."):
        """Show loading dialog with progress indicator"""
        from kivymd.uix.progressbar import MDProgressBar
        
        content = MDBoxLayout(
            orientation="vertical",
            spacing="16dp",
            size_hint_y=None,
            height="100dp",
            padding="20dp"
        )
        
        progress = MDProgressBar(type="indeterminate")
        progress.start()
        
        loading_label = MDLabel(
            text=message,
            theme_text_color="Primary",
            font_style="Body1",
            halign="center"
        )
        
        content.add_widget(progress)
        content.add_widget(loading_label)
        
        self.loading_dialog = MDDialog(
            title="Please Wait",
            type="custom",
            content_cls=content,
            size_hint=(0.75, None),  # Better width
            height="180dp",  # Adjusted height
            auto_dismiss=False
        )
        
        self.loading_dialog.open()
        return self.loading_dialog
    
    def hide_loading_dialog(self):
        """Hide loading dialog"""
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.dismiss()