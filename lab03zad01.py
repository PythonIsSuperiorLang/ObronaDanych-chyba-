import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


tekst_bazowy = b"0123456789ABCDEF"
dane_jawne = tekst_bazowy * 4

klucz_hex = "000102030405060708090a0b0c0d0e0f"
klucz_bajty = bytes.fromhex(klucz_hex)

# Szyfrowanie ECB
szyfr_ecb = Cipher(algorithms.AES(klucz_bajty), modes.ECB())
enkryptor_ecb = szyfr_ecb.encryptor()

# dane są wielokrotnością bloku, więc nie dodajemy paddingu
kryptogram_ecb = enkryptor_ecb.update(dane_jawne) + enkryptor_ecb.finalize()

# Szyfrowanie CBC
iv = os.urandom(16)  # Losujemy bezpieczne IV o długości 16 bajtów
szyfr_cbc = Cipher(algorithms.AES(klucz_bajty), modes.CBC(iv))
enkryptor_cbc = szyfr_cbc.encryptor()
kryptogram_cbc = enkryptor_cbc.update(dane_jawne) + enkryptor_cbc.finalize()


def wypisz_bloki(kryptogram, nazwa_trybu):
    print(f"\n--- Bloki kryptogramu dla trybu {nazwa_trybu} ---")
    for i in range(0, len(kryptogram), 16):
        blok = kryptogram[i:i+16]
        numer_bloku = (i // 16) + 1
        print(f"Blok {numer_bloku}: {blok.hex()}")

#wypisujemy bloki dla tych trybów
wypisz_bloki(kryptogram_ecb, "ECB")
wypisz_bloki(kryptogram_cbc, "CBC")

dekryptor_ecb = szyfr_ecb.decryptor()
odszyfrowane_ecb = dekryptor_ecb.update(kryptogram_ecb) + dekryptor_ecb.finalize()

dekryptor_cbc = szyfr_cbc.decryptor()
odszyfrowane_cbc = dekryptor_cbc.update(kryptogram_cbc) + dekryptor_cbc.finalize()

# Porównanie bajtów po odszyfrowaniu
print("\n--- sprawdzenie dzialania ---")
print(f"Czy ECB dziala? {odszyfrowane_ecb == dane_jawne}")
print(f"Czy CBC dziala? {odszyfrowane_cbc == dane_jawne}")