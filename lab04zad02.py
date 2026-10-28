import hashlib
import hmac
import os

# globalny slownik na baze hasel
baza_hasel = {}

# wczytanie bazy z pliku hasla txt
try:
    with open('hasla.txt', 'r', encoding='utf-8') as f:
        for linia in f:
            login, iteracje, sol, skrot = linia.strip().split(':')
            # zapisujemy do bazy konwertujac hex na bajty
            baza_hasel[login] = (int(iteracje), bytes.fromhex(sol), bytes.fromhex(skrot))
except FileNotFoundError:
    print("brak pliku hasla.txt")

# funkcja weryfikujaca logowanie
def weryfikuj(login, haslo):
    if login not in baza_hasel:
        return False
        
    iteracje, sol, zapisany_skrot = baza_hasel[login]
    
    # liczymy skrot z podanego hasla
    obliczony_skrot = hashlib.pbkdf2_hmac(
        'sha256', 
        haslo.encode('utf-8'), 
        sol, 
        iteracje
    )
    
    # porownujemy skroty w stalym czasie
    return hmac.compare_digest(obliczony_skrot, zapisany_skrot)

# funkcja generujaca nowe konto
def dodaj(login, haslo):
    # losowa bezpieczna sol 16 bajtow
    sol = os.urandom(16)
    iteracje = 600000
    
    skrot = hashlib.pbkdf2_hmac(
        'sha256', 
        haslo.encode('utf-8'), 
        sol, 
        iteracje
    )
    # dopisujemy od razu do naszej bazy zeby moc potem zweryfikowac
    baza_hasel[login] = (iteracje, sol, skrot)
    
    # zwracamy wygenerowany rekord tak jak chce polecenie
    return f"{login}:{iteracje}:{sol.hex()}:{skrot.hex()}"

# 1 sprawdzanie 4 wyznaczonych przypadkow
print("Weryfikacja bazy:")
print("anna, Kasztan-2026 ->", weryfikuj("anna", "Kasztan-2026"))
print("anna, kasztan-2026 ->", weryfikuj("anna", "kasztan-2026"))
print("piotr, Żółw na łące ->", weryfikuj("piotr", "Żółw na łące"))
print("kasia, Kasztan-2026 ->", weryfikuj("kasia", "Kasztan-2026"))

# 2 tworzenie kont testowych z tym samym haslem
print("\nDodawanie nowych kont (haslo: JanPawelDluuuuugi):")
rekord1 = dodaj("test1", "JanPawelDluuuuugi")
rekord2 = dodaj("test2", "JanPawelDluuuuugi")

print("Rekord test1:", rekord1)
print("Rekord test2:", rekord2)

# weryfikacja nowych kont
print("\nWeryfikacja nowych kont:")
print("test1, JanPawelDluuuuugi ->", weryfikuj("test1", "JanPawelDluuuuugi"))
print("test2, JanPawelDluuuuugi ->", weryfikuj("test2", "JanPawelDluuuuugi"))