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
        """Open navigation drawer"""
        if self.controller:
            # Create navigation menu
            menu_items = [
                ("home", "Home", "home"),
                ("account", "Profile", "profile"),
                ("pill", "Medications", "medications"),
                ("file-document", "Reports", "reports"),
                ("calendar", "Appointments", "appointments"),
                ("heart-pulse", "Health Records", "health_records"),
                ("cog", "Settings", "settings"),
            ]
            
            # Show navigation options
            self.show_navigation_menu(menu_items)
    
    def show_navigation_menu(self, menu_items):
        """Show navigation menu dialog"""
        menu_list = MDList()
        
        for icon, title, screen_name in menu_items:
            item = OneLineListItem(
                text=title,
                on_release=lambda x, screen=screen_name: self.navigate_to_screen(screen)
            )
            menu_list.add_widget(item)
        
        dialog = MDDialog(
            title="Navigation",
            type="custom",
            content_cls=menu_list,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
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