def solve_cezar(file_path: str):
  with open(file_path, "rb") as f:
    data = f.read()

  total_len = len(data)
  printable = set(range(32, 127)) | {9, 10, 13}

  results = []
  for k in range(256):
    decrypted = bytes((b - k) % 256 for b in data)
    printable_count = sum(1 for b in decrypted if b in printable)
    score = printable_count / total_len if total_len > 0 else 0.0
    results.append((score, k, decrypted))

  def sort_key(item):
    return (-item[0], item[1])

  results.sort(key=sort_key)

  print("=== TOP 5 KANDYDATÓW (PRZESUNIĘCIE CEZARA) ===")
  for rank, (score, k, dec) in enumerate(results[:5], 1):
    poczatek = repr(dec[:50])
    print(
        f"{rank}. k = {k:3d} (0x{k:02X}) | Ocena: {score*100:6.2f}% |"
        f" Początek: {poczatek}"
    )

  best_dec = results[0][2]
  
  choice = input("Wybierz przesunięcie k: ")
  user_k = int(choice)
  best_dec = bytes((b - user_k) % 256 for b in data)

  with open("cezar.txt", "wb") as f:
    f.write(best_dec)

solve_cezar("cezar.bin")