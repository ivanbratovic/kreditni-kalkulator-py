import tkinter as tk
from tkinter import messagebox


def calculate():
    try:
        cijena_po_kvadratu = float(entry_cijena_po_kvadratu.get())
        ukupno_kvadrata = float(entry_ukupno_kvadrata.get())
        cijena_parkirnog_mjesta = float(entry_cijena_parkirnog_mjesta.get())
        vlastito_ucesce = float(entry_vlastito_ucesce.get())
        postotak_za_kaparu = float(entry_postotak_za_kaparu.get()) / 100

        stambeni_kredit_kamata = float(entry_stambeni_kredit_kamata.get()) / 100
        stambeni_kredit_godine = int(entry_stambeni_kredit_godine.get())

        gotovinski_kredit_kamata = float(entry_gotovinski_kredit_kamata.get()) / 100
        gotovinski_kredit_godine = int(entry_gotovinski_kredit_godine.get())

        # Calculate total property cost
        ukupna_cijena = (cijena_po_kvadratu * ukupno_kvadrata) + cijena_parkirnog_mjesta

        # Calculate kapara
        kapara = ukupna_cijena * postotak_za_kaparu
        preostalo_za_kredit = ukupna_cijena * (1 - postotak_za_kaparu)
        kapara -= vlastito_ucesce

        if kapara <= 0:
            preostalo_za_kredit += kapara
            kapara = 0

        if preostalo_za_kredit <= 0:
            preostalo_za_kredit = 0

        # Monthly annuity formula: A = P * (r(1+r)^n) / ((1+r)^n - 1)
        def calculate_annuity(principal, annual_rate, years):
            monthly_rate = annual_rate / 12
            months = years * 12
            return (
                principal
                * (monthly_rate * (1 + monthly_rate) ** months)
                / ((1 + monthly_rate) ** months - 1)
            )

        anuitet_stambeni = calculate_annuity(
            preostalo_za_kredit, stambeni_kredit_kamata, stambeni_kredit_godine
        )
        anuitet_gotovinski = calculate_annuity(
            kapara, gotovinski_kredit_kamata, gotovinski_kredit_godine
        )

        za_platiti_stambeni = anuitet_stambeni * stambeni_kredit_godine * 12
        za_platiti_kamata_stambeni = za_platiti_stambeni - preostalo_za_kredit
        za_platiti_gotovinski = anuitet_gotovinski * gotovinski_kredit_godine * 12
        za_platiti_kamata_gotovinski = za_platiti_gotovinski - kapara

        ukupni_mjesecni_trosak = anuitet_stambeni + anuitet_gotovinski

        # Update output fields
        label_anuitet_stambeni_value.config(text=f"{anuitet_stambeni:.2f} EUR")
        label_anuitet_gotovinski_value.config(text=f"{anuitet_gotovinski:.2f} EUR")
        label_ukupna_cijena_value.config(text=f"{ukupna_cijena:.2f} EUR")
        label_ukupno_stambeni_value.config(text=f"{za_platiti_stambeni:.2f} EUR")
        label_kamata_stambeni_value.config(text=f"{za_platiti_kamata_stambeni:.2f} EUR")
        label_ukupno_gotovinski_value.config(text=f"{za_platiti_gotovinski:.2f} EUR")
        label_kamata_gotovinski_value.config(text=f"{za_platiti_kamata_gotovinski:.2f} EUR")
        label_ukupni_trosak_value.config(text=f"{ukupni_mjesecni_trosak:.2f} EUR")
        

    except ValueError:
        messagebox.showerror(
            "Input Error", "Molimo unesite ispravne brojčane vrijednosti u sva polja."
        )


# Create main window
root = tk.Tk()
root.title("Kalkulator kredita za nekretninu")
root.resizable(False, False)  # Prevent resizing
root.configure(bg="#f0f0f5")  # Set background color


# Input fields
label_cijena_po_kvadratu = tk.Label(root, text="Cijena po kvadratu:", bg="#f0f0f5", font=("Arial", 10))
label_cijena_po_kvadratu.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_cijena_po_kvadratu = tk.Entry(root, font=("Arial", 10))
entry_cijena_po_kvadratu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

label_ukupno_kvadrata = tk.Label(root, text="Ukupno kvadrata:", bg="#f0f0f5", font=("Arial", 10))
label_ukupno_kvadrata.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_ukupno_kvadrata = tk.Entry(root, font=("Arial", 10))
entry_ukupno_kvadrata.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_cijena_parkirnog_mjesta = tk.Label(root, text="Cijena parkirnog mjesta:", bg="#f0f0f5", font=("Arial", 10))
label_cijena_parkirnog_mjesta.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_cijena_parkirnog_mjesta = tk.Entry(root, font=("Arial", 10))
entry_cijena_parkirnog_mjesta.grid(row=2, column=1, padx=10, pady=5, sticky="w")

label_vlastito_ucesce = tk.Label(root, text="Vlastito učešće:", bg="#f0f0f5", font=("Arial", 10))
label_vlastito_ucesce.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_vlastito_ucesce = tk.Entry(root, font=("Arial", 10))
entry_vlastito_ucesce.grid(row=3, column=1, padx=10, pady=5, sticky="w")

label_postotak_za_kaparu = tk.Label(root, text="Postotak za kaparu (%):", bg="#f0f0f5", font=("Arial", 10))
label_postotak_za_kaparu.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_postotak_za_kaparu = tk.Entry(root, font=("Arial", 10))
entry_postotak_za_kaparu.grid(row=4, column=1, padx=10, pady=5, sticky="w")

label_stambeni_kredit_kamata = tk.Label(root, text="Kamata za stambeni kredit (%):", bg="#f0f0f5", font=("Arial", 10))
label_stambeni_kredit_kamata.grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_stambeni_kredit_kamata = tk.Entry(root, font=("Arial", 10))
entry_stambeni_kredit_kamata.grid(row=5, column=1, padx=10, pady=5, sticky="w")
entry_stambeni_kredit_kamata.insert(0, "2.89")

label_stambeni_kredit_godine = tk.Label(root, text="Godine za stambeni kredit:", bg="#f0f0f5", font=("Arial", 10))
label_stambeni_kredit_godine.grid(row=6, column=0, padx=10, pady=5, sticky="e")
entry_stambeni_kredit_godine = tk.Entry(root, font=("Arial", 10))
entry_stambeni_kredit_godine.grid(row=6, column=1, padx=10, pady=5, sticky="w")
entry_stambeni_kredit_godine.insert(0, "30")

label_gotovinski_kredit_kamata = tk.Label(root, text="Kamata za gotovinski kredit (%):", bg="#f0f0f5", font=("Arial", 10))
label_gotovinski_kredit_kamata.grid(row=7, column=0, padx=10, pady=5, sticky="e")
entry_gotovinski_kredit_kamata = tk.Entry(root, font=("Arial", 10))
entry_gotovinski_kredit_kamata.grid(row=7, column=1, padx=10, pady=5, sticky="w")
entry_gotovinski_kredit_kamata.insert(0, "4.5")

label_gotovinski_kredit_godine = tk.Label(root, text="Godine za gotovinski kredit:", bg="#f0f0f5", font=("Arial", 10))
label_gotovinski_kredit_godine.grid(row=8, column=0, padx=10, pady=5, sticky="e")
entry_gotovinski_kredit_godine = tk.Entry(root, font=("Arial", 10))
entry_gotovinski_kredit_godine.grid(row=8, column=1, padx=10, pady=5, sticky="w")
entry_gotovinski_kredit_godine.insert(0, "10")

# Calculate button
button_calculate = tk.Button(root, text="Izračunaj", command=calculate)
button_calculate.grid(row=9, column=0, columnspan=2, pady=10)

# Output fields
label_ukupna_cijena = tk.Label(root, text="Ukupna cijena nekretnine:", bg="#f0f0f5", font=("Arial", 10))
label_ukupna_cijena.grid(row=10, column=0, padx=10, pady=5, sticky="e")
label_ukupna_cijena_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10))
label_ukupna_cijena_value.grid(row=10, column=1, padx=10, pady=5, sticky="w")

label_anuitet_stambeni = tk.Label(root, text="Anuitet za stambeni kredit:", bg="#f0f0f5", font=("Arial", 10))
label_anuitet_stambeni.grid(row=11, column=0, padx=10, pady=5, sticky="e")
label_anuitet_stambeni_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10, "bold"))
label_anuitet_stambeni_value.grid(row=11, column=1, padx=10, pady=5, sticky="w")

label_ukupno_stambeni = tk.Label(root, text="Ukupno za plaćanje:", bg="#f0f0f5", font=("Arial", 10))
label_ukupno_stambeni.grid(row=12, column=0, padx=10, pady=5, sticky="e")
label_ukupno_stambeni_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10))
label_ukupno_stambeni_value.grid(row=12, column=1, padx=10, pady=5, sticky="w")

label_kamata_stambeni = tk.Label(root, text="Od toga je kamata:", bg="#f0f0f5", font=("Arial", 10))
label_kamata_stambeni.grid(row=13, column=0, padx=10, pady=5, sticky="e")
label_kamata_stambeni_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10))
label_kamata_stambeni_value.grid(row=13, column=1, padx=10, pady=5, sticky="w")

label_anuitet_gotovinski = tk.Label(root, text="Anuitet za gotovinski kredit:", bg="#f0f0f5", font=("Arial", 10))
label_anuitet_gotovinski.grid(row=14, column=0, padx=10, pady=5, sticky="e")
label_anuitet_gotovinski_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10, "bold"))
label_anuitet_gotovinski_value.grid(row=14, column=1, padx=10, pady=5, sticky="w")

label_ukupno_gotovinski = tk.Label(root, text="Ukupno za plaćanje:", bg="#f0f0f5", font=("Arial", 10))
label_ukupno_gotovinski.grid(row=15, column=0, padx=10, pady=5, sticky="e")
label_ukupno_gotovinski_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10))
label_ukupno_gotovinski_value.grid(row=15, column=1, padx=10, pady=5, sticky="w")

label_kamata_gotovinski = tk.Label(root, text="Ukupna kamata:", bg="#f0f0f5", font=("Arial", 10))
label_kamata_gotovinski.grid(row=16, column=0, padx=10, pady=5, sticky="e")
label_kamata_gotovinski_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10))
label_kamata_gotovinski_value.grid(row=16, column=1, padx=10, pady=5, sticky="w")

label_ukupni_trosak = tk.Label(root, text="Ukupni mjesečni trošak:", bg="#f0f0f5", font=("Arial", 10))
label_ukupni_trosak.grid(row=17, column=0, padx=10, pady=5, sticky="e")
label_ukupni_trosak_value = tk.Label(root, text="0.00 EUR", bg="#f0f0f5", font=("Arial", 10, "bold"))
label_ukupni_trosak_value.grid(row=17, column=1, padx=10, pady=5, sticky="w")

# Run the application
root.mainloop()
