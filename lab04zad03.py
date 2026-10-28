import hashlib

# funkcja skracajaca do pierwszych 6 znakow hex
def h24(dane):
    return hashlib.sha256(dane).hexdigest()[:6]

def wczytaj_linie(sciezka):
    with open(sciezka, 'rb') as plik:
        dane = plik.read()
    linie = dane.split(b'\n')
    # usuwamy ostatni pusty element jesli plik konczy sie nowa linia
    if linie[-1] == b'':
        linie = linie[:-1]
    return linie

# funkcja generujaca wariant z ewentualnymi spacjami
def generuj_wariant(linie, v):
    wynik = b""
    for i in range(13):
        if (v >> i) & 1 == 1:
            wynik += linie[i] + b" \n"
        else:
            wynik += linie[i] + b"\n"
    return wynik

# wczytywanie plikow
oryg = wczytaj_linie('oryginal.txt')
zmien = wczytaj_linie('zmieniony.txt')

slownik_skrotow = {}

# 1 zapamietywanie skrotow dla wszystkich wariantow oryginalu
for v in range(8192):
    dane = generuj_wariant(oryg, v)
    skrot = h24(dane)
    # zachowujemy pierwszy napotkany numer wariantu
    if skrot not in slownik_skrotow:
        slownik_skrotow[skrot] = v

# skrot wariantu 0 do zadania 3
h24_cel = h24(generuj_wariant(oryg, 0))

znaleziona_para = None
liczba_dopasowan_do_celu = 0

for v in range(8192):
    dane = generuj_wariant(zmien, v)
    skrot = h24(dane)
    
    #zapisanie pierwszej znalezionej kolizji
    if znaleziona_para is None and skrot in slownik_skrotow:
        v_oryg = slownik_skrotow[skrot]
        znaleziona_para = (v_oryg, v, skrot)
        
    #liczenie ile skrotow pasuje do oryginalu bez zmian
    if skrot == h24_cel:
        liczba_dopasowan_do_celu += 1

print("Znaleziona para kolizyjna (oryginal, zmieniony):", znaleziona_para[0], "oraz", znaleziona_para[1])
print("Ich wspolny skrot h24 to:", znaleziona_para[2])
print("Liczba kolizji dla wariantu 0 (niezmienionego):", liczba_dopasowan_do_celu)