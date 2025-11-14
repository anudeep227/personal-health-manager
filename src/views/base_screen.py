"""
Base screen class for all application screens
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerMenu
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar


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