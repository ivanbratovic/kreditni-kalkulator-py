"""Main entry point for the loan calculator application"""

import tkinter as tk
from gui import LoanCalculatorGUI


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = LoanCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
