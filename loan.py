"""Loan calculation logic and validation"""

from dataclasses import dataclass
from typing import Dict, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors"""

    pass


class InputValidator:
    """Handles all input validation"""

    @staticmethod
    def validate_numeric(
        value: str, min_val: float = None, max_val: float = None
    ) -> float:
        """Validate numeric input within optional range"""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                raise ValidationError(
                    f"Brojčana vrijednost ne smije biti manja od {min_val}."
                )
            if max_val is not None and num > max_val:
                raise ValidationError(
                    f"Brojčana vrijednost ne smije biti veća od {max_val}."
                )
            return num
        except ValueError:
            raise ValidationError(
                "Molimo unesite valjanu brojčanu vrijednost u sva polja."
            )

    @staticmethod
    def validate_inputs(inputs: Dict[str, str]) -> Dict[str, float]:
        """Validate all input fields"""
        from config import Config

        validated = {}

        # Validate property details
        validated["price_per_sqm"] = InputValidator.validate_numeric(
            inputs["cijena_po_kvadratu"],
            Config.VALIDATION["min_price_per_sqm"],
            Config.VALIDATION["max_price_per_sqm"],
        )

        validated["total_sqm"] = InputValidator.validate_numeric(
            inputs["ukupno_kvadrata"],
            Config.VALIDATION["min_area"],
            Config.VALIDATION["max_area"],
        )

        validated["parking_price"] = InputValidator.validate_numeric(
            inputs["cijena_parkirnog_mjesta"], 0
        )

        # Validate loan parameters
        validated["down_payment"] = InputValidator.validate_numeric(
            inputs["vlastito_ucesce"], 0
        )

        validated["advance_percentage"] = InputValidator.validate_numeric(
            inputs["postotak_za_kaparu"], 0, 100
        )

        validated["mortgage_rate"] = (
            InputValidator.validate_numeric(
                inputs["stambeni_kredit_kamata"],
                Config.VALIDATION["min_interest"],
                Config.VALIDATION["max_interest"],
            )
            / 100
        )

        validated["mortgage_years"] = int(
            InputValidator.validate_numeric(
                inputs["stambeni_kredit_godine"],
                Config.VALIDATION["min_years"],
                Config.VALIDATION["max_years"],
            )
        )

        validated["cash_loan_rate"] = InputValidator.validate_numeric(
            inputs["gotovinski_kredit_kamata"],
            Config.VALIDATION["min_interest"],
            Config.VALIDATION["max_interest"]
        ) / 100
        
        validated["cash_loan_years"] = int(InputValidator.validate_numeric(
            inputs["gotovinski_kredit_godine"],
            Config.VALIDATION["min_years"],
            Config.VALIDATION["max_years"]
        ))


        return validated


@dataclass
class LoanResult:
    """Data class for loan calculation results"""
    monthly_payment: float
    total_payment: float
    total_interest: float

class LoanCalculator:
    """Handles all loan calculation business logic"""
    
    def calculate_property_costs(self, price_per_sqm: float, total_sqm: float, 
                               parking_price: float) -> float:
        """Calculate total property cost"""
        return (price_per_sqm * total_sqm) + parking_price
    
    def calculate_loan_amounts(self, total_price: float, own_money: float, 
                             down_payment_percentage: float) -> Tuple[float, float]:
        """
        Calculate mortgage and cash loan amounts
        Returns: (mortgage_amount, cash_loan_amount)
        """
        # Calculate required down payment
        required_down_payment = total_price * (down_payment_percentage / 100)
        
        # Calculate how much of the down payment needs to be covered by a cash loan
        cash_loan_needed = required_down_payment - own_money
        
        if cash_loan_needed <= 0:
            # User has enough own money to cover the down payment
            mortgage_amount = total_price - own_money
            return mortgage_amount, 0
        else:
            # User needs a cash loan to cover part of the down payment
            mortgage_amount = total_price - required_down_payment
            return mortgage_amount, cash_loan_needed

    def calculate_loan_details(self, principal: float, annual_rate: float, 
                             years: int) -> LoanResult:
        """
        Calculate complete loan payment details
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.0289 for 2.89%)
            years: Loan term in years
        Returns:
            LoanResult with monthly payment, total payment, and total interest
        """
        if principal == 0:
            return LoanResult(0, 0, 0)
        
        monthly_rate = annual_rate / 12
        months = years * 12
        
        if monthly_rate > 0:
            # Standard loan amortization formula
            monthly_payment = (
                principal
                * (monthly_rate * (1 + monthly_rate) ** months)
                / ((1 + monthly_rate) ** months - 1)
            )
        else:
            # No interest, simple division
            monthly_payment = principal / months
        
        total_payment = monthly_payment * months
        total_interest = total_payment - principal
        
        return LoanResult(monthly_payment, total_payment, total_interest)

    def calculate_complete_loan_details(self, 
                                     total_price: float,
                                     own_money: float,
                                     down_payment_percentage: float,
                                     mortgage_rate: float,
                                     mortgage_years: int,
                                     cash_loan_rate: float,
                                     cash_loan_years: int) -> dict:
        """Calculate complete details for both loans"""
        
        # Calculate basic amounts
        mortgage_amount, cash_loan_amount = self.calculate_loan_amounts(
            total_price, own_money, down_payment_percentage)
        
        # Calculate mortgage details
        mortgage_details = self.calculate_loan_details(
            mortgage_amount, mortgage_rate, mortgage_years)
        
        # Calculate cash loan details if needed
        if cash_loan_amount > 0:
            cash_loan_details = self.calculate_loan_details(
                cash_loan_amount, cash_loan_rate, cash_loan_years)
        else:
            cash_loan_details = LoanResult(0, 0, 0)
            
        return {
            'total_price': total_price,
            'own_money': own_money,
            'required_down_payment': total_price * (down_payment_percentage / 100),
            'mortgage_amount': mortgage_amount,
            'cash_loan_amount': cash_loan_amount,
            'mortgage_monthly': mortgage_details.monthly_payment,
            'mortgage_total': mortgage_details.total_payment,
            'mortgage_interest': mortgage_details.total_interest,
            'cash_loan_monthly': cash_loan_details.monthly_payment,
            'cash_loan_total': cash_loan_details.total_payment,
            'cash_loan_interest': cash_loan_details.total_interest,
            'total_monthly': mortgage_details.monthly_payment + cash_loan_details.monthly_payment
        }