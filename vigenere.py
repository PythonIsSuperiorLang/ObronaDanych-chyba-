def vigenere_encrypt(data: bytes, key: bytes) -> bytes:
  m = len(key)
  return bytes((p + key[i % m]) % 256 for i, p in enumerate(data))


def vigenere_decrypt(data: bytes, key: bytes) -> bytes:
  m = len(key)
  return bytes((c - key[i % m]) % 256 for i, c in enumerate(data))

def test_vigenere():
  print("\n--- Testy brzegowe (puste dane i skrajne wartości bajtów) ---")
  key = b"TEST"

  # Test puste dane
  empty_p = b""
  empty_c = vigenere_encrypt(empty_p, key)
  empty_d = vigenere_decrypt(empty_c, key)
  assert empty_d == empty_p

  # Test bajty 0 i 255
  boundary_p = bytes([0, 255, 0, 255, 128, 1, 254])
  boundary_c = vigenere_encrypt(boundary_p, key)
  boundary_d = vigenere_decrypt(boundary_c, key)
  assert boundary_d == boundary_p
  print("jezeli przeszlo tzn ze testy brzegowe przeszly pomyslnie")

def run_vigenere_task():
  input_file = "tekst_pl.txt"

  with open(input_file, "rb") as f:
    plaintext_pl = f.read()

  key_zamek = b"ZAMEK"
  cipher_zamek = vigenere_encrypt(plaintext_pl, key_zamek)

  with open("vigenere.bin", "wb") as f:
    f.write(cipher_zamek)

  decrypted_zamek = vigenere_decrypt(cipher_zamek, key_zamek)
  assert (
      decrypted_zamek == plaintext_pl
  ), "odszyfrowany teskt nie dziala pzdr"

  print(
      f"[+] Zadanie 2.1: Zapisano vigenere.bin ({len(cipher_zamek)} B)."
      " Zgodność z oryginałem czyli git"
  )

  test_vigenere()

  print("\n=== Zadanie 2.2: Kryptogramy dla BRAMABRAMABRAMA ===")
  msg = b"BRAMABRAMABRAMA"

  c_szyfr = vigenere_encrypt(msg, b"SZYFR")
  hex_szyfr = c_szyfr.hex()
  blocks_szyfr = [hex_szyfr[i : i + 10] for i in range(0, len(hex_szyfr), 10)]

  c_kod = vigenere_encrypt(msg, b"KOD")
  hex_kod = c_kod.hex()
  blocks_kod = [hex_kod[i : i + 10] for i in range(0, len(hex_kod), 10)]

  print(f"Klucz SZYFR (len 5): {' '.join(blocks_szyfr)}")
  print(f"Klucz KOD   (len 3): {' '.join(blocks_kod)}")

run_vigenere_task()