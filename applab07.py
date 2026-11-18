"""Sejf sekretow i kalkulator - poprawna i bezpieczna wersja aplikacji.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import re
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error as exc:
        app.logger.exception("Błąd bazy danych w /sekret dla klucza: %s", klucz)
        blad = "Wystąpił błąd podczas przetwarzania żądania."
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    # 1. Wejście na /kalkulator bez parametru - wyświetlenie samego formularza (HTTP 200)
    if "wyrazenie" not in request.args:
        return render_template("kalkulator.html", wyrazenie="", wynik=None), 200

    wyrazenie = request.args.get("wyrazenie", "")

    # 2. Puste pole (?wyrazenie=) lub przekroczenie 100 znaków -> HTTP 400
    if not wyrazenie or len(wyrazenie) > 100:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="Błąd: Niepoprawne wejście"), 400

    # 3. Weryfikacja formatu: liczba, operator (+, -, *, /), liczba z opcjonalnymi spacjami i minusami
    pattern = r"^\s*(-?\d+(?:\.\d+)?)\s*([\+\-\*/])\s*(-?\d+(?:\.\d+)?)\s*$"
    match = re.fullmatch(pattern, wyrazenie)

    if not match:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="Błąd: Niepoprawne wyrażenie"), 400

    num1_str, operator, num2_str = match.groups()
    num1 = float(num1_str)
    num2 = float(num2_str)

    # 4. Obsługa dzielenia przez zero -> HTTP 400
    if operator == "/" and num2 == 0:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="Błąd: Dzielenie przez zero"), 400

    # Obliczenie wyniku
    if operator == "+":
        res = num1 + num2
    elif operator == "-":
        res = num1 - num2
    elif operator == "*":
        res = num1 * num2
    elif operator == "/":
        res = num1 / num2

    # Konwersja float do int, jeśli liczba jest całkowita (np. 5.0 -> 5)
    wynik = int(res) if res.is_integer() else res
    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=wynik), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)