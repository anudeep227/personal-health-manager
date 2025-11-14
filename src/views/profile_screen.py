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
        """Setup profile screen content"""
        # Profile form
        form_card = self.create_card("Personal Information")
        form_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
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
        
        form_card.add_widget(form_layout)
        self.content_layout.add_widget(form_card)
        
        # Load existing profile data
        self.load_profile_data()
    
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