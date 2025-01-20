# Kreditni kalkulator

Računa otplatni plan kupnje nekretnine, koristeći stambeni kredit te gotovinski kredit za kaparu. Uzima učešće u obzir pri izračunu oba kredita. Npr. učešće veće od kapare uklanja gotovinski kredit iz plana.

![image](https://github.com/user-attachments/assets/04b073c2-ad2b-4392-8abe-c527fb6e2b41)


Napisano programski jezik Python.

## Pokretanje binarne datoteke

Ažurnu izvršnu datoteku možete pronaći u posljednjem GitHub Izdanju (engl. _Release_). Nju sam generirao koristeći sljedeću naredbu:

```sh
pyinstaller --clean --onefile --windowed --name "Kalkulator Kredita" --icon=calculator.ico calculator.py
```

Ako ne vjerujete ovoj izvršnoj datoteci, slobodno preuzmite izvorni kod i nastavite s uputama u sljedećem odlomku.

## Pokretanje iz izvornog koda

Zahtijeva instaliran `Tkinter` Python modul, koji se **ne može** instalirati preko pip-a. Pogledajte opcije instalacije za operacijski sustav kojeg koristite.

Pokretanje:

```sh
python3 ./calculator.py
```
