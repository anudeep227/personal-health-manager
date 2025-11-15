"""
Beautiful Health App Color Scheme and Material Design Theme
"""

class HealthAppColors:
    """Enhanced graphical color palette for the health management app"""
    
    # Primary Health Colors (Enhanced Teal-based medical theme)
    PRIMARY = {
        50: (0.94, 0.98, 0.97, 1),   # Very light teal
        100: (0.8, 0.94, 0.92, 1),   # Light teal
        200: (0.6, 0.88, 0.84, 1),   # Medium light teal
        300: (0.3, 0.8, 0.76, 1),    # Medium teal
        400: (0.15, 0.74, 0.68, 1),  # Medium dark teal
        500: (0.0, 0.65, 0.58, 1),   # Primary teal
        600: (0.0, 0.58, 0.51, 1),   # Dark teal
        700: (0.0, 0.51, 0.45, 1),   # Darker teal
        800: (0.0, 0.42, 0.37, 1),   # Very dark teal
        900: (0.0, 0.3, 0.26, 1),    # Darkest teal
    }
    
    # Enhanced Accent Colors with Gradients
    ACCENT = {
        'A100': (0.5, 0.9, 1.0, 1),    # Very light blue
        'A200': (0.25, 0.85, 1.0, 1),  # Light blue
        'A400': (0.0, 0.75, 1.0, 1),   # Medium blue
        'A700': (0.0, 0.55, 0.95, 1),  # Dark blue
    }
    
    # Enhanced Semantic Colors with Visual Appeal
    SUCCESS = (0.15, 0.85, 0.35, 1)     # Vibrant green for success/healthy
    WARNING = (1.0, 0.65, 0.0, 1)       # Bright orange for warnings
    ERROR = (0.95, 0.26, 0.21, 1)       # Material red for errors/critical
    INFO = (0.13, 0.59, 0.95, 1)        # Material blue for information
    
    # New Graphical Colors for Visual Enhancement
    GRADIENT_START = (0.0, 0.65, 0.58, 1)    # Primary teal
    GRADIENT_END = (0.13, 0.59, 0.95, 1)     # Info blue
    
    # Activity Status Colors (More Vibrant)
    COMPLETED = (0.15, 0.85, 0.35, 1)        # Bright green
    PENDING = (1.0, 0.65, 0.0, 1)            # Bright orange
    OVERDUE = (0.95, 0.26, 0.21, 1)          # Material red
    SCHEDULED = (0.40, 0.23, 0.72, 1)        # Deep purple
    
    # Enhanced Category Colors with Visual Pop
    MEDICATION = (0.67, 0.35, 0.95, 1)  # Vivid purple for medications
    APPOINTMENT = (0.25, 0.75, 0.95, 1) # Sky blue for appointments  
    REPORT = (0.95, 0.55, 0.25, 1)      # Warm orange for reports
    VITAL_SIGNS = (0.91, 0.30, 0.24, 1) # Coral red for vital signs
    REMINDER = (1.0, 0.84, 0.0, 1)      # Golden yellow for reminders
    ACHIEVEMENT = (0.0, 0.80, 0.40, 1)  # Emerald green for achievements
    
    # Modern Machine/Tech Colors - Neon and Cyber Theme
    MATRIX_GREEN = (0.0, 0.8, 0.4, 1)     # Matrix-style green
    ELECTRIC_BLUE = (0.2, 0.6, 1.0, 1)    # Electric blue
    NEON_PURPLE = (0.8, 0.2, 1.0, 1)      # Neon purple
    CYBER_ORANGE = (1.0, 0.3, 0.0, 1)     # Cyber orange
    CYAN_BLUE = (0.0, 1.0, 1.0, 1)        # Bright cyan
    HOT_PINK = (1.0, 0.0, 0.5, 1)         # Hot pink
    ELECTRIC_YELLOW = (0.7, 0.7, 0.0, 1)   # Electric yellow
    STEEL_BLUE = (0.27, 0.51, 0.71, 1)    # Steel blue
    NEON_GREEN = (0.2, 1.0, 0.2, 1)       # Bright neon green
    MAGENTA = (1.0, 0.0, 1.0, 1)          # Pure magenta
    
    # Card Background Colors with Subtle Gradients
    CARD_GRADIENT_1 = (0.98, 0.98, 1.0, 1)      # Light blue tint
    CARD_GRADIENT_2 = (1.0, 0.98, 0.98, 1)      # Light pink tint  
    CARD_GRADIENT_3 = (0.98, 1.0, 0.98, 1)      # Light green tint
    CARD_GRADIENT_4 = (1.0, 1.0, 0.98, 1)       # Light yellow tint
    
    # Background Colors
    BACKGROUND_LIGHT = (0.98, 0.98, 0.98, 1)  # Almost white
    SURFACE_LIGHT = (1.0, 1.0, 1.0, 1)        # Pure white
    BACKGROUND_DARK = (0.12, 0.12, 0.12, 1)   # Dark background
    SURFACE_DARK = (0.18, 0.18, 0.18, 1)      # Dark surface
    
    # Text Colors
    TEXT_PRIMARY_LIGHT = (0.13, 0.13, 0.13, 1)    # Dark text on light
    TEXT_SECONDARY_LIGHT = (0.4, 0.4, 0.4, 1)     # Gray text on light
    TEXT_PRIMARY_DARK = (1.0, 1.0, 1.0, 1)        # White text on dark
    TEXT_SECONDARY_DARK = (0.7, 0.7, 0.7, 1)      # Light gray on dark
    
    # Card and Component Colors
    CARD_LIGHT = (1.0, 1.0, 1.0, 1)
    CARD_DARK = (0.2, 0.2, 0.2, 1)
    DIVIDER_LIGHT = (0.9, 0.9, 0.9, 1)
    DIVIDER_DARK = (0.3, 0.3, 0.3, 1)


class HealthAppGradients:
    """Beautiful gradients for the health app"""
    
    HERO_GRADIENT = [
        (0.0, 0.65, 0.58, 1),  # Primary teal
        (0.0, 0.75, 0.65, 1),  # Lighter teal
    ]
    
    SUCCESS_GRADIENT = [
        (0.2, 0.8, 0.2, 1),    # Success green
        (0.3, 0.9, 0.3, 1),    # Lighter green
    ]
    
    WARNING_GRADIENT = [
        (1.0, 0.7, 0.0, 1),    # Warning orange
        (1.0, 0.8, 0.2, 1),    # Lighter orange
    ]
    
    MEDICATION_GRADIENT = [
        (0.6, 0.3, 0.9, 1),    # Purple
        (0.7, 0.4, 0.95, 1),   # Lighter purple
    ]


def get_theme_config():
    """Get complete theme configuration for the health app"""
    return {
        "theme_style": "Light",
        "primary_palette": "Teal",
        "primary_hue": "500",
        "accent_palette": "LightBlue", 
        "accent_hue": "A400",
        "material_style": "M3",
        
        # Custom colors
        "primary_color": HealthAppColors.PRIMARY[500],
        "accent_color": HealthAppColors.ACCENT['A400'],
        "success_color": HealthAppColors.SUCCESS,
        "warning_color": HealthAppColors.WARNING,
        "error_color": HealthAppColors.ERROR,
        "info_color": HealthAppColors.INFO,
        
        # Surface colors
        "bg_light": HealthAppColors.BACKGROUND_LIGHT,
        "surface_color": HealthAppColors.SURFACE_LIGHT,
        "card_color": HealthAppColors.CARD_LIGHT,
        
        # Text colors
        "text_primary": HealthAppColors.TEXT_PRIMARY_LIGHT,
        "text_secondary": HealthAppColors.TEXT_SECONDARY_LIGHT,
    }


def apply_theme_to_app(app):
    """Apply the beautiful health theme to the MDApp"""
    config = get_theme_config()
    
    app.theme_cls.theme_style = config["theme_style"]
    app.theme_cls.primary_palette = config["primary_palette"]
    app.theme_cls.primary_hue = config["primary_hue"]
    app.theme_cls.accent_palette = config["accent_palette"]
    app.theme_cls.accent_hue = config["accent_hue"]
    
    # Only set material_style if available in this version
    try:
        app.theme_cls.material_style = config["material_style"]
    except AttributeError:
        pass  # Not available in this KivyMD version
    
    # Note: primary_color and accent_color are automatically set by palette/hue
    # We don't need to set them manually as they're read-only properties