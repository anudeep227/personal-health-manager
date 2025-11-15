"""
Profile screen for managing user information
"""

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from datetime import datetime

from views.base_screen import BaseScreen


class ProfileScreen(BaseScreen):
    """User profile management screen"""
    
    def get_screen_title(self) -> str:
        return "My Profile"
    
    def get_toolbar_actions(self) -> list:
        return [
            ["content-save", lambda x: self.save_profile()],
            ["account-edit", lambda x: self.edit_profile()]
        ]
    
    def setup_content(self):
        """Setup profile screen content with single block design"""
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.card import MDCard
        
        # Create scroll view for better layout
        scroll = MDScrollView()
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing="20dp",
            adaptive_height=True,
            padding="20dp"
        )
        
        # Single comprehensive profile card
        profile_card = MDCard(
            size_hint_y=None,
            height="600dp",
            elevation=8,
            padding="24dp",
            md_bg_color=(0.15, 0.15, 0.15, 1),  # Dark background
            radius=[15]
        )
        
        form_layout = MDBoxLayout(orientation='vertical', spacing="20dp")
        
        # Profile header within the card
        header_layout = self.create_compact_profile_header()
        form_layout.add_widget(header_layout)
        
        # Name fields
        self.first_name_field = MDTextField(
            hint_text="First Name",
            helper_text="Enter your first name",
            helper_text_mode="persistent"
        )
        form_layout.add_widget(self.first_name_field)
        
        self.last_name_field = MDTextField(
            hint_text="Last Name",
            helper_text="Enter your last name",
            helper_text_mode="persistent"
        )
        form_layout.add_widget(self.last_name_field)
        
        # Contact fields
        self.email_field = MDTextField(
            hint_text="Email",
            helper_text="Enter your email address",
            helper_text_mode="persistent"
        )
        form_layout.add_widget(self.email_field)
        
        self.phone_field = MDTextField(
            hint_text="Phone Number",
            helper_text="Enter your phone number",
            helper_text_mode="persistent"
        )
        form_layout.add_widget(self.phone_field)
        
        # Health information
        self.blood_group_field = MDTextField(
            hint_text="Blood Group",
            helper_text="e.g., A+, B-, O+",
            helper_text_mode="persistent"
        )
        form_layout.add_widget(self.blood_group_field)
        
        # Save button
        save_btn = MDRaisedButton(
            text="Save Profile",
            on_release=lambda x: self.save_profile()
        )
        form_layout.add_widget(save_btn)
        
        # Add all form fields to the single card\n        profile_card.add_widget(form_layout)\n        main_layout.add_widget(profile_card)\n        \n        scroll.add_widget(main_layout)\n        self.content_layout.add_widget(scroll)
        
        # Load existing profile data
        self.load_profile_data()
    
    def create_profile_header(self):
        """Create colorful profile header"""
        from src.utils.theme import HealthAppColors
        from kivymd.uix.boxlayout import MDBoxLayout
        
        card = MDCard(
            size_hint_y=None,
            height="150dp",
            elevation=8,
            padding="24dp",
            md_bg_color=HealthAppColors.PRIMARY[500],  # Vibrant teal
            radius=[15]
        )
        
        layout = MDBoxLayout(orientation='vertical', spacing="12dp")
        
        # Profile avatar (using initials)
        avatar_card = MDCard(
            size_hint=(None, None),
            size=("80dp", "80dp"),
            md_bg_color=HealthAppColors.ACCENT['A200'],  # Bright blue
            radius=[40],
            elevation=4,
            pos_hint={'center_x': 0.5}
        )
        
        avatar_label = MDLabel(
            text="JP",  # Default initials
            font_style="H4",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        avatar_card.add_widget(avatar_label)
        layout.add_widget(avatar_card)
        
        # Welcome text
        welcome_label = MDLabel(
            text="Welcome to Your Health Profile",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        layout.add_widget(welcome_label)
        
        card.add_widget(layout)
        return card
    
    def create_compact_profile_header(self):
        """Create compact profile header for single block design"""
        from src.utils.theme import HealthAppColors
        from kivymd.uix.boxlayout import MDBoxLayout
        
        header_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="80dp",
            spacing="16dp",
            padding="12dp"
        )
        
        # Avatar
        avatar_card = MDCard(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            md_bg_color=HealthAppColors.ELECTRIC_BLUE,
            radius=[30],
            elevation=4
        )
        
        avatar_label = MDLabel(
            text="JP",
            font_style="H6",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        avatar_card.add_widget(avatar_label)
        header_layout.add_widget(avatar_card)
        
        # Welcome text
        text_layout = MDBoxLayout(orientation='vertical', spacing="4dp")
        welcome_label = MDLabel(
            text="Personal Profile",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            bold=True
        )
        subtitle_label = MDLabel(
            text="Manage your health information",
            font_style="Body2",
            theme_text_color="Custom",
            text_color=(0.7, 0.7, 0.7, 1)
        )
        text_layout.add_widget(welcome_label)
        text_layout.add_widget(subtitle_label)
        header_layout.add_widget(text_layout)
        
        return header_layout
    
    def load_profile_data(self):
        """Load existing profile data"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            # Get current user (assuming user_id = 1)
            user = db_service.get_user(1)
            
            if user:
                self.first_name_field.text = user.first_name or ""
                self.last_name_field.text = user.last_name or ""
                self.email_field.text = user.email or ""
                self.phone_field.text = user.phone or ""
                self.blood_group_field.text = user.blood_group or ""
            else:
                # Create a default user if none exists
                self.create_default_user()
                
        except Exception as e:
            self.show_error(f"Failed to load profile: {str(e)}")
    
    def create_default_user(self):
        """Create a default user profile"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                return
            
            default_user_data = {
                'first_name': 'User',
                'last_name': 'Name',
                'email': 'user@example.com',
                'created_at': datetime.utcnow()
            }
            
            user = db_service.create_user(default_user_data)
            
            if self.controller:
                self.controller.set_current_user(user)
            
            self.show_message("Default profile created. Please update your information.")
            
        except Exception as e:
            self.show_error(f"Failed to create profile: {str(e)}")
    
    def save_profile(self):
        """Save profile changes"""
        try:
            db_service = self.get_database_service()
            if not db_service:
                self.show_error("Database service not available")
                return
            
            # Validate required fields
            if not self.first_name_field.text.strip():
                self.show_error("First name is required")
                return
            
            if not self.last_name_field.text.strip():
                self.show_error("Last name is required")
                return
            
            # Prepare update data
            update_data = {
                'first_name': self.first_name_field.text.strip(),
                'last_name': self.last_name_field.text.strip(),
                'email': self.email_field.text.strip(),
                'phone': self.phone_field.text.strip(),
                'blood_group': self.blood_group_field.text.strip(),
                'updated_at': datetime.utcnow()
            }
            
            # Update user (assuming user_id = 1)
            updated_user = db_service.update_user(1, update_data)
            
            if updated_user:
                if self.controller:
                    self.controller.set_current_user(updated_user)
                self.show_message("Profile updated successfully!")
            else:
                self.show_error("Failed to update profile")
                
        except Exception as e:
            self.show_error(f"Failed to save profile: {str(e)}")
    
    def edit_profile(self):
        """Enable profile editing"""
        self.show_message("Profile editing enabled")
    
    def refresh_data(self):
        """Refresh profile data"""
        self.load_profile_data()