#!/usr/bin/python3
import os

print("Content-Type: text/plain; charset=utf-8")
print()

uid = os.geteuid()
gid = os.getegid()

print(f"Efektywny UID: {uid}")
print(f"Efektywny GID: {gid}")
print("-" * 20)

pliki = ["/lab-data/ogolny.txt", "/lab-data/poufny.txt"]

for plik in pliki:
    try:
        with open(plik, "r", encoding="utf-8") as f:
            tresc = f.read().strip()
            print(f"Plik {plik}: SUKCES - {tresc}")
    except PermissionError:
        print(f"Plik {plik}: ODMOWA DOSTĘPU")
    except Exception as e:
        print(f"Plik {plik}: BŁĄD - {e}")