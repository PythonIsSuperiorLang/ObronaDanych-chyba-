import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# --- obliczanie entropii ---

def oblicz_entropie(dane_bajty):
    wystapienia = {}
    for bajt in dane_bajty:
        wystapienia[bajt] = wystapienia.get(bajt, 0) + 1
        
    dlugosc = len(dane_bajty)
    entropia = 0.0
    
    #obliczanie entropi wg wzoru
    for licznik in wystapienia.values():
        p_b = licznik / dlugosc
        entropia -= p_b * math.log2(p_b)
        
    return entropia

alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"
wyniki = []

# wczystanie pliku i probka
with open("slaby_ecb.bin", "rb") as f:
    kryptogram = f.read()
    
probka = kryptogram[:4096]

print("--- OBLICZANIE ENTROPII DLA KANDYDATÓW ---")
# przesjce po 36 mozliwosciach 
for znak in alfabet:
    # tworzymy klucz z 16 powtorzen znaku
    klucz = (znak * 16).encode('ascii')
    
    szyfr = Cipher(algorithms.AES(klucz), modes.ECB())
    dekryptor = szyfr.decryptor()

    odszyfrowana_probka = dekryptor.update(probka) + dekryptor.finalize()

    H = oblicz_entropie(odszyfrowana_probka)

    wyniki.append((H, znak))
wyniki.sort()

print("\nPięciu najlepszych kandydatów:")
for i in range(5):
    H, znak = wyniki[i]
    print(f"{i+1}. Znak: '{znak}', Entropia: {H:.4f}")

najlepszy_znak = wyniki[0][1]
najlepszy_klucz = (najlepszy_znak * 16).encode('ascii')

print(f"\nOdszyfrowywanie całego pliku kluczem znak: '{najlepszy_znak}'...")

szyfr_calosc = Cipher(algorithms.AES(najlepszy_klucz), modes.ECB())
dekryptor_calosc = szyfr_calosc.decryptor()
odszyfrowana_calosc_padded = dekryptor_calosc.update(kryptogram) + dekryptor_calosc.finalize()

# Usuwamy dopełnienie 
unpadder = padding.PKCS7(128).unpadder()
odszyfrowana_calosc = unpadder.update(odszyfrowana_calosc_padded) + unpadder.finalize()

# Wyciągamy pierwszy wiersz (do znaku nowej linii)
pierwszy_wiersz = odszyfrowana_calosc.split(b'\n')[0].decode('utf-8')
print("\nPierwszy wiersz odszyfrowanego tekstu:")
print(pierwszy_wiersz)