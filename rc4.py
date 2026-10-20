import math
import string
import time


# tutaj caly ten algorytm
def rc4(data: bytes, key: bytes) -> bytes:
  S = list(range(256))
  j = 0
  for i in range(256):
    j = (j + S[i] + key[i % len(key)]) % 256
    S[i], S[j] = S[j], S[i]
  i = j = 0
  out = bytearray()
  for byte in data:
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    k = S[(S[i] + S[j]) % 256]
    out.append(byte ^ k)

  return bytes(out)


# 2. Obliczanie entropii Shannona dla bajtów
def entropy(data: bytes) -> float:
  length = len(data)
  counts = [0] * 256
  for b in data:
    counts[b] += 1

  res = 0.0
  for count in counts:
    if count > 0:
      p = count / length
      res -= p * math.log2(p)
  return res


# Testujemy odwracalność RC4
assert rc4(rc4(b"test", b"abc"), b"abc") == b"test"

#jezeli preszlo dalej i sie kod nie wywalil to znaczy ze dziala

# Odczyt zaszyfrowanego pliku
with open("rc4.bin", "rb") as f:
  ciphertext = f.read()

# Entropia kryptogramu
ciphertext_entropy = entropy(ciphertext)

sample = ciphertext[:512]
alphabet = string.ascii_lowercase

start_time = time.time()
results = []
attempts = 0

# Przeszukiwanie wszystkich kombinacji 3 liter a-z
# zlozonosc n^3 smh
for c1 in alphabet:
  for c2 in alphabet:
    for c3 in alphabet:
      key = (c1 + c2 + c3).encode("ascii")
      attempts += 1
      decrypted_sample = rc4(sample, key)
      ent = entropy(decrypted_sample)
      results.append((ent, key, decrypted_sample))

elapsed_time = time.time() - start_time

# Sortowanie tego czegos
results.sort(key=lambda x: (x[0], x[1]))

print("=== PODSUMOWANIE PRZESZUKIWANIA ===")
print(f"Liczba prób: {attempts}")
print(f"Czas przeszukiwania: {elapsed_time:.4f} s")
print(f"Entropia całego kryptogramu (rc4.bin): {ciphertext_entropy:.4f} b/B\n")

print("=== TOP 5 KANDYDATÓW (RANKING) ===")
for rank, (ent, key, dec_sample) in enumerate(results[:5], 1):
  print(
      f"{rank}. Klucz: '{key.decode()}' | Entropia próbki: {ent:.4f} b/B |"
      f" Początek: {repr(dec_sample[:40])}"
  )

# wybór pierwszego klucza z rankingu
best_key = results[0][1]

#   odszyfrowanie całego pliku
full_decrypted = rc4(ciphertext, best_key)

# Entropia całego odszyfrowania
decrypted_entropy = entropy(full_decrypted)

with open("rc4.txt", "wb") as f:
  f.write(full_decrypted)

# Sprawdzenie poprawności ponownego szyfrowania
assert rc4(full_decrypted, best_key) == ciphertext

print("\n=== WYNIKI DLA ODZYSKANEGO PLIKU ===")
print(f"Odzyskany klucz: '{best_key.decode()}'")
print(
    "Entropia całego odszyfrowania (rc4.txt):"
    f" {decrypted_entropy:.4f} b/B"
)
