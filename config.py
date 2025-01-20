"""Configuration settings for the loan calculator"""


class PresetField:
    def __init__(self, label: str, options: dict, width: int = 30):
        self.label = label
        self.options = options
        self.width = width


class InvestorPreset:
    def __init__(self, name: str, updates: dict):
        self.name = name
        self.updates = updates  # Dictionary of field_id: value to update


class Config:
    """Configuration settings for the application"""

    DEFAULTS = {
        "stambeni_kredit_kamata": "2.89",
        "stambeni_kredit_godine": "30",
        "gotovinski_kredit_kamata": "4.5",
        "gotovinski_kredit_godine": "10",
    }

    STYLES = {
        "bg_color": "#f0f0f5",
        "text_color": "#333333",
        "button_color": "#4CAF50",
        "button_text_color": "white",
        "font_family": "Arial",
        "font_size": 10,
    }

    VALIDATION = {
        "min_price_per_sqm": 0,
        "max_price_per_sqm": 10000,
        "min_area": 20,
        "max_area": 1000,
        "min_interest": 0.1,
        "max_interest": 20,
        "min_years": 1,
        "max_years": 40,
    }

    TOOLTIP = {
        "font_size": 8,
        "x_offset": 15,
        "y_offset": 10,
        "padx": 3,
        "pady": 1,
        "bg_color": "#ffffe0",
        "font_family": "Arial",
    }

    # Investor presets
    PRESET_DEPENDENCIES = {
        "investor_type": {
            "updates_dropdowns": {
                "apartment_type": "apartment_types",
            }
        },
        "apartment_type": {
            "requires": ["investor_type"],
        },
    }
    PRESETS = {
        "investor_type": PresetField(
            label="Novogradnja:",
            options={
                "Odaberi investitora": None,
                "Pionir - Čavićeva": InvestorPreset(
                    name="Pionir - Čavićeva",
                    updates={
                        "cijena_po_kvadratu": "2970",
                        "postotak_za_kaparu": "10",
                        "apartment_types": {
                            "Jednosoban": "57.7",
                            "Dvosoban": "71.85",
                            "Trosoban": "84.48",
                        },
                    },
                ),
                "Pionir - Špansko": InvestorPreset(
                    name="Pionir - Špansko",
                    updates={
                        "cijena_po_kvadratu": "2670",
                        "postotak_za_kaparu": "10",
                        "apartment_types": {
                            "Jednosoban 58": "58.22",
                            "Jednosoban 62": "62.37",
                            "Jednosoban 66": "62.14",
                            "Dvosoban": "84.36",
                            "Četverosoban": "198.95",
                        },
                    },
                ),
                "Pionir - Lovinčićeva": InvestorPreset(
                    name="Pionir - Lovinčićeva",
                    updates={
                        "cijena_po_kvadratu": "3390",
                        "postotak_za_kaparu": "10",
                        "apartment_types": {
                            "Jednosoban 58": "58.22",
                            "Jednosoban 62": "62.37",
                            "Jednosoban 66": "62.14",
                            "Dvosoban": "84.36",
                            "Četverosoban": "198.95",
                        },
                    },
                ),
            },
        ),
        "apartment_type": PresetField(
            label="Tip stana:",
            options={"Odaberi tip stana": None},  # Will be populated dynamically
        )
    }
