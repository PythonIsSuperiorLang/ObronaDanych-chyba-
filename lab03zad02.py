
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- FUNKCJE POMOCNICZE ---

def wyprowadz_klucz(haslo_tekst, sol):
    # Parametry z polecenia
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sol,
        iterations=200000,
    )
    return kdf.derive(haslo_tekst.encode('utf-8'))

def zaszyfruj(dane_bajty, klucz, iv):
    padder = padding.PKCS7(128).padder()
    dane_padded = padder.update(dane_bajty) + padder.finalize()
    
    szyfr = Cipher(algorithms.AES(klucz), modes.CBC(iv))
    enkryptor = szyfr.encryptor()
    kryptogram = enkryptor.update(dane_padded) + enkryptor.finalize()
    
    return kryptogram

def odszyfruj(kryptogram, klucz, iv):
    szyfr = Cipher(algorithms.AES(klucz), modes.CBC(iv))
    dekryptor = szyfr.decryptor()
    dane_padded = dekryptor.update(kryptogram) + dekryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    dane_bajty = unpadder.update(dane_padded) + unpadder.finalize()
    
    return dane_bajty

# --- PRZYGOTOWANIE DO TESTÓW ---

haslo = "moje_bezpieczne_haslo_123"
sol = os.urandom(16) # Losowa sól 16 B
iv = os.urandom(16)  # Losowe IV 16 B do pierwszego szyfrowania

# Wyprowadzenie klucza z hasła i soli
klucz = wyprowadz_klucz(haslo, sol)

# Przygotowanie pliku wiadomosc.txt (jeśli nie istnieje, tworzymy go)
nazwa_pliku = "wiadomosc.txt"
# --- testy ---

dane_testowe = [
    b"",                                  # Test 1: puste dane
    b"0123456789ABCDEF",                  # Test 2: 16 bajtów ASCII
    open(nazwa_pliku, "rb").read()        # Test 3: bajty pliku wiadomosc.txt
]

print("--- WYNIKI TESTÓW ---")
for i, dane in enumerate(dane_testowe, 1):
    kryptogram = zaszyfruj(dane, klucz, iv)
    odszyfrowane = odszyfruj(kryptogram, klucz, iv)
    sukces = (dane == odszyfrowane)
    
    print(f"Test {i}:")
    print(f"  Długość wejścia: {len(dane)} B")
    print(f"  Długość kryptogramu: {len(kryptogram)} B")
    print(f"  Czy dane przed i po są równe?: {sukces}\n")

# Losujemy nową sól i nowe IV
nowa_sol = os.urandom(16)
nowe_iv = os.urandom(16)

# Ponieważ sól jest inna, musimy wygenerować nowy klucz z hasła
nowy_klucz = wyprowadz_klucz(haslo, nowa_sol)

dane_do_porownania = dane_testowe[2] 

kryptogram_1 = zaszyfruj(dane_do_porownania, klucz, iv)
kryptogram_2 = zaszyfruj(dane_do_porownania, nowy_klucz, nowe_iv)

print("--- PORÓWNANIE KRYPTOGRAMÓW ---")
print(f"Czy kryptogramy są identyczne?: {kryptogram_1 == kryptogram_2}")