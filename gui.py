"""GUI implementation for the loan calculator"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from typing import Dict, Any

from config import Config, InvestorPreset
from loan import LoanCalculator, InputValidator, ValidationError


class ToolTip:
    """Creates a tooltip for a given widget"""

    def __init__(self, widget: tk.Widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        """Show tooltip"""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + Config.TOOLTIP["x_offset"]
        y += self.widget.winfo_rooty() + Config.TOOLTIP["y_offset"]

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            justify="left",
            background=Config.TOOLTIP["bg_color"],
            relief="solid",
            borderwidth=1,
            font=(Config.TOOLTIP["font_family"], Config.TOOLTIP["font_size"]),
            padx=Config.TOOLTIP["padx"],
            pady=Config.TOOLTIP["pady"],
        )
        label.pack()

    def leave(self, event=None):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class LoanCalculatorGUI:
    """Main GUI class for the loan calculator"""

    def __init__(self, root: tk.Tk):
        self.last_input_row = 0
        self.root = root
        self.calculator = LoanCalculator()
        self.inputs = {}
        self.output_labels = {}
        self.validation_command = (
            self.root.register(self.validate_numeric_input),
            "%P",
        )
        self.setup_gui()

    def setup_gui(self):
        """Initialize all GUI components"""
        self.root.title("Kalkulator kredita za nekretninu")
        self.root.configure(bg=Config.STYLES["bg_color"])
        self.create_frames()
        self.create_input_fields()
        self.create_output_fields()
        self.create_buttons()
        self.add_tooltips()

    def create_frames(self):
        """Create main frames"""
        self.input_frame = tk.Frame(self.root, bg=Config.STYLES["bg_color"])
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.output_frame = tk.Frame(self.root, bg=Config.STYLES["bg_color"])
        self.output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def create_input_field(self, field_id: str, label_text: str):
        """Create individual input field"""
        label = tk.Label(
            self.input_frame,
            text=label_text,
            bg=Config.STYLES["bg_color"],
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"]),
        )
        label.grid(row=self.last_input_row, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(
            self.input_frame,
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"]),
            validate="key",
            validatecommand=self.validation_command,  # Use the validation command here
        )
        entry.grid(row=self.last_input_row, column=1, padx=10, pady=5, sticky="w")
        self.last_input_row += 1
        self.inputs[field_id] = entry

        # Set default value if exists
        if field_id in Config.DEFAULTS:
            entry.insert(0, Config.DEFAULTS[field_id])

    def create_output_field(self, row: int, field_id: str, label_text: str):
        """Create individual output field"""
        label = tk.Label(
            self.output_frame,
            text=label_text,
            bg=Config.STYLES["bg_color"],
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"]),
        )
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        value_label = tk.Label(
            self.output_frame,
            text="0.00 EUR",
            bg=Config.STYLES["bg_color"],
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"]),
        )
        value_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        self.output_labels[field_id] = value_label

    def create_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.input_frame, bg=Config.STYLES["bg_color"])
        button_frame.grid(row=self.last_input_row, column=0, columnspan=2, pady=10)

        calculate_button = tk.Button(
            button_frame,
            text="Izračunaj",
            command=self.calculate,
            bg=Config.STYLES["button_color"],
            fg=Config.STYLES["button_text_color"],
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"], "bold"),
        )
        calculate_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Očisti",
            command=self.clear_fields,
            bg="#f44336",
            fg=Config.STYLES["button_text_color"],
            font=(Config.STYLES["font_family"], Config.STYLES["font_size"], "bold"),
        )
        clear_button.pack(side=tk.LEFT, padx=5)

    def add_tooltips(self):
        """Add tooltips to input fields"""
        tooltips = {
            "cijena_po_kvadratu": "Unesite cijenu po kvadratu u EUR",
            "ukupno_kvadrata": "Unesite ukupnu kvadraturu nekretnine",
            "cijena_parkirnog_mjesta": "Unesite cijenu parkirnog mjesta u EUR",
            "vlastito_ucesce": "Unesite iznos vlastitog učešća u EUR",
            "postotak_za_kaparu": "Unesite postotak za kaparu (0-100)",
            "stambeni_kredit_kamata": "Kamatna stopa za stambeni kredit",
            "stambeni_kredit_godine": "Razdoblje otplate stambenog kredita",
            "gotovinski_kredit_kamata": "Kamatna stopa za gotovinski kredit za kaparu",
            "gotovinski_kredit_godine": "Razdoblje otplate gotovinskog kredita",
        }

        for field_id, tooltip_text in tooltips.items():
            if field_id in self.inputs:
                ToolTip(self.inputs[field_id], tooltip_text)

    @staticmethod
    def validate_numeric_input(P: str) -> bool:
        """Validate numeric input"""
        if P == "" or P == ".":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def clear_fields(self):
        """Clear all fields and reset presets"""
        # Clear input fields (existing code)
        for entry in self.inputs.values():
            entry.delete(0, tk.END)

        # Reset default values (existing code)
        for field_id, value in Config.DEFAULTS.items():
            if field_id in self.inputs:
                self.inputs[field_id].insert(0, value)

        # Reset presets
        for preset_id, preset_field in Config.PRESETS.items():
            self.preset_dropdowns[preset_id].set(list(preset_field.options.keys())[0])

        # Clear results
        for label in self.output_labels.values():
            label.config(text="0.00 EUR")

    def update_results(self, results: dict):
        """Update result displays"""
        updates = {
            "ukupna_cijena": results["total_price"],
            "za_stambeni_kredit": results["mortgage_amount"],
            "za_gotovinski_kredit": results["cash_loan_amount"],
            "anuitet_stambeni": results["mortgage_monthly"],
            "ukupno_stambeni": results["mortgage_total"],
            "kamata_stambeni": results["mortgage_interest"],
            "anuitet_gotovinski": results["cash_loan_monthly"],
            "ukupno_gotovinski": results["cash_loan_total"],
            "kamata_gotovinski": results["cash_loan_interest"],
        }

        for field_id, value in updates.items():
            if field_id in self.output_labels:
                if value <= 10 and "gotovinski" in field_id:
                    self.output_labels[field_id].config(text="Nije potreban")
                else:
                    self.output_labels[field_id].config(text=f"{value:.2f} EUR")

    def calculate(self):
        """Perform calculations and update display"""
        try:
            # Get and validate inputs
            input_values = {
                field_id: entry.get() for field_id, entry in self.inputs.items()
            }
            validated = InputValidator.validate_inputs(input_values)

            # Calculate total price
            total_price = self.calculator.calculate_property_costs(
                validated["price_per_sqm"],
                validated["total_sqm"],
                validated["parking_price"],
            )

            # Calculate complete loan details
            results = self.calculator.calculate_complete_loan_details(
                total_price=total_price,
                own_money=validated["down_payment"],
                down_payment_percentage=validated["advance_percentage"],
                mortgage_rate=validated["mortgage_rate"],
                mortgage_years=validated["mortgage_years"],
                cash_loan_rate=validated["cash_loan_rate"],
                cash_loan_years=validated["cash_loan_years"],
            )

            # Update display
            self.update_results(results)

        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def create_labeled_separator(self, text: str, parent_frame: tk.Frame) -> tk.Frame:
        """Create a labeled separator"""
        frame = tk.Frame(parent_frame, bg=Config.STYLES["bg_color"])

        label = tk.Label(
            frame,
            text=text,
            bg=Config.STYLES["bg_color"],
            fg=Config.STYLES["text_color"],
            font=(Config.STYLES["font_family"], 11, "bold"),
        )
        label.pack(side="left", padx=(0, 10))

        separator = ttk.Separator(frame, orient="horizontal")
        separator.pack(side="left", fill="x", expand=True)

        return frame

    def create_section(self, title: str, fields: list) -> int:
        """Create a section with fields"""
        # Create and place separator
        separator = self.create_labeled_separator(title, self.input_frame)
        separator.grid(
            row=self.last_input_row,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=10,
            padx=10,
        )

        self.last_input_row += 1

        # Create fields
        for field_id, label_text in fields:
            self.create_input_field(field_id, label_text)

    def create_input_fields(self):
        """Create all input fields"""
        # Create preset selectors first
        self.create_preset_selectors()

        # Property details section
        self.create_section(
            "Podaci o nekretnini",
            [
                ("cijena_po_kvadratu", "Cijena po kvadratu (EUR):"),
                ("ukupno_kvadrata", "Površina (m²):"),
                ("cijena_parkirnog_mjesta", "Cijena parkirnog mjesta (EUR):"),
                ("postotak_za_kaparu", "Postotak za kaparu (%):"),
            ],
        )

        # Loan parameters section
        self.create_section(
            "Parametri otplate",
            [
                ("vlastito_ucesce", "Vlastito učešće (EUR):"),
                ("stambeni_kredit_kamata", "Kamata za stambeni kredit (%):"),
                ("stambeni_kredit_godine", "Rok otplate stambenog kredita (g.):"),
                ("gotovinski_kredit_kamata", "Kamata za gotovinski kredit (%):"),
                ("gotovinski_kredit_godine", "Rok otplate gotovinskog kredita (g.):"),
            ],
        )

    def create_output_fields(self):
        """Create output display fields"""
        # Create output sections and labels
        sections = [
            (
                "Otplatni plan",
                [
                    ("ukupna_cijena", "Ukupna cijena nekretnine:"),
                    ("za_stambeni_kredit", "Iznos stambenog kredita:"),
                    ("za_gotovinski_kredit", "Iznos gotovinskog kredita:"),
                ],
            ),
            (
                "Stambeni kredit",
                [
                    ("anuitet_stambeni", "Mjesečni anuitet:"),
                    ("ukupno_stambeni", "Ukupno za plaćanje:"),
                    ("kamata_stambeni", "Ukupna kamata:"),
                ],
            ),
            (
                "Gotovinski kredit",
                [
                    ("anuitet_gotovinski", "Mjesečni anuitet:"),
                    ("ukupno_gotovinski", "Ukupno za plaćanje:"),
                    ("kamata_gotovinski", "Ukupna kamata:"),
                ],
            ),
        ]

        for title, fields in sections:
            separator = self.create_labeled_separator(title, self.output_frame)
            separator.grid(
                row=self.last_input_row,
                column=0,
                columnspan=2,
                sticky="ew",
                pady=10,
                padx=10,
            )
            self.last_input_row += 1

            for field_id, label_text in fields:
                self.create_output_field(self.last_input_row, field_id, label_text)
                self.last_input_row += 1

    def create_preset_selectors(self) -> int:
        """
        Create dropdown menus for presets
        Returns the next available row
        """
        # Create frame for presets
        preset_frame = tk.Frame(self.input_frame, bg=Config.STYLES["bg_color"])
        preset_frame.grid(
            row=self.last_input_row,
            column=0,
            columnspan=2,
            pady=10,
            padx=10,
            sticky="ew",
        )

        # Store preset variables and dropdowns
        self.preset_vars = {}
        self.preset_dropdowns = {}

        # Create dropdowns for each preset type
        column = 0
        for preset_id, preset_field in Config.PRESETS.items():
            # Create label
            label = tk.Label(
                preset_frame,
                text=preset_field.label,
                bg=Config.STYLES["bg_color"],
                font=(Config.STYLES["font_family"], Config.STYLES["font_size"]),
            )
            label.grid(
                row=self.last_input_row, column=column, padx=5, pady=5, sticky="e"
            )

            # Create variable and dropdown
            self.preset_vars[preset_id] = tk.StringVar()
            self.preset_dropdowns[preset_id] = ttk.Combobox(
                preset_frame,
                textvariable=self.preset_vars[preset_id],
                values=list(preset_field.options.keys()),
                state="readonly",
                width=preset_field.width,
            )
            self.preset_dropdowns[preset_id].grid(
                row=self.last_input_row, column=column + 1, padx=5, pady=5, sticky="w"
            )
            self.preset_dropdowns[preset_id].set(list(preset_field.options.keys())[0])

            # Bind selection event
            self.preset_dropdowns[preset_id].bind(
                "<<ComboboxSelected>>",
                lambda e, pid=preset_id: self.on_preset_selected(pid),
            )

            column += 2

        self.last_input_row += 1

    def on_preset_selected(self, preset_id: str):
        """
        Handle preset selection dynamically based on preset dependencies
        and field updates defined in config
        """
        selected_value = self.preset_vars[preset_id].get()
        preset_options = Config.PRESETS[preset_id].options
        preset = preset_options.get(selected_value)

        # Get preset dependencies from config
        dependencies = Config.PRESET_DEPENDENCIES.get(preset_id, {})

        if preset_id == "apartment_type" and selected_value != "Odaberi tip stana":
            # Special handling for apartment type selection
            self.handle_apartment_selection(selected_value)
        elif preset:
            # Update all fields defined in the preset
            self.apply_preset_updates(preset.updates)

            # Handle dependent dropdowns
            for dependent_id, update_method in dependencies.get(
                "updates_dropdowns", {}
            ).items():
                if dependent_id in self.preset_dropdowns:
                    self.update_dependent_dropdown(dependent_id, preset, update_method)
        else:
            # Reset dependent dropdowns
            for dependent_id in dependencies.get("updates_dropdowns", {}):
                if dependent_id in self.preset_dropdowns:
                    self.reset_dropdown(dependent_id)

    def handle_apartment_selection(self, selected_apartment: str):
        """Handle apartment type selection and update area"""
        # Get current investor
        investor_name = self.preset_vars["investor_type"].get()
        investor_preset = Config.PRESETS["investor_type"].options.get(investor_name)

        if investor_preset and "apartment_types" in investor_preset.updates:
            apartment_types = investor_preset.updates["apartment_types"]
            if selected_apartment in apartment_types:
                # Update the area field
                area = apartment_types[selected_apartment]
                if "ukupno_kvadrata" in self.inputs:
                    self.inputs["ukupno_kvadrata"].delete(0, tk.END)
                    self.inputs["ukupno_kvadrata"].insert(0, str(area))

    def apply_preset_updates(self, updates: dict):
        """Apply updates to input fields and handle special cases"""
        for field_id, value in updates.items():
            if field_id in self.inputs:
                # Update regular input fields
                self.inputs[field_id].delete(0, tk.END)
                self.inputs[field_id].insert(0, str(value))
            elif isinstance(value, dict):
                # Handle nested updates (like apartment_types)
                self.handle_nested_updates(field_id, value)

    def handle_nested_updates(self, field_id: str, value: dict):
        """Handle nested update structures like apartment types"""
        if field_id == "apartment_types":
            # Update apartment type dropdown with new values
            if "apartment_type" in self.preset_dropdowns:
                current_default = (
                    Config.PRESETS["apartment_type"]
                    .options.keys()
                    .__iter__()
                    .__next__()
                )
                self.preset_dropdowns["apartment_type"]["values"] = [
                    current_default
                ] + list(value.keys())
                self.preset_dropdowns["apartment_type"].set(current_default)

    def update_dependent_dropdown(
        self, dependent_id: str, parent_preset: InvestorPreset, update_method: str
    ):
        """Update dependent dropdown based on parent preset"""
        if update_method == "apartment_types":
            apartment_types = parent_preset.updates.get("apartment_types", {})
            default_option = (
                Config.PRESETS[dependent_id].options.keys().__iter__().__next__()
            )
            self.preset_dropdowns[dependent_id]["values"] = [default_option] + list(
                apartment_types.keys()
            )
            self.preset_dropdowns[dependent_id].set(default_option)

    def reset_dropdown(self, dropdown_id: str):
        """Reset dropdown to its default state"""
        if dropdown_id in Config.PRESETS:
            default_options = [
                Config.PRESETS[dropdown_id].options.keys().__iter__().__next__()
            ]
            self.preset_dropdowns[dropdown_id]["values"] = default_options
            self.preset_dropdowns[dropdown_id].set(default_options[0])
