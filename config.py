"""Configuration settings for the loan calculator"""

class Config:
    """Configuration settings for the application"""
    DEFAULTS = {
        "stambeni_kredit_kamata": "2.89",
        "stambeni_kredit_godine": "30",
        "gotovinski_kredit_kamata": "4.5",
        "gotovinski_kredit_godine": "10"
    }
    
    STYLES = {
        "bg_color": "#f0f0f5",
        "text_color": "#333333",
        "button_color": "#4CAF50",
        "button_text_color": "white",
        "font_family": "Arial",
        "font_size": 10
    }
    
    VALIDATION = {
        "min_price_per_sqm": 0,
        "max_price_per_sqm": 10000,
        "min_area": 20,
        "max_area": 1000,
        "min_interest": 0.1,
        "max_interest": 20,
        "min_years": 1,
        "max_years": 40
    }

    TOOLTIP = {
        "font_size": 8,
        "x_offset": 15,
        "y_offset": 10,
        "padx": 3,
        "pady": 1,
        "bg_color": "#ffffe0",
        "font_family": "Arial"
    }
