import os, hashlib

# 1 funkcja liczaca sha256 pliku
def sha256_pliku(sciezka):
    if not os.path.exists(sciezka):
        return None
    with open(sciezka, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

# 2 weryfikacja plikow z sha256sums txt
with open('SHA256SUMS.txt', 'r', encoding='utf-8') as f:
    for linia in f:
        if not linia.strip() in linia:
            continue
        expected_hash, path = linia.strip().split('  ')
        filename = path.split('/')[-1]
        computed_hash = sha256_pliku(filename)
        status = "BRAK" if computed_hash is None else ("OK" if computed_hash == expected_hash else "BŁĄD")
        print(f"{path}: {status}")

# 3 roznica bitow miedzy ala ma kota i ola ma kota
h1 = hashlib.sha256(b"Ala ma kota.").digest()
h2 = hashlib.sha256(b"Ola ma kota.").digest()
diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(h1, h2))
print(f"Liczba rozniacych sie bitow: {diff_bits}")