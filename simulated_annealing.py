import random
import numpy as np
import time
import json
from generator_warunkow import *

N = 7

wyniki = {}


def pokaz_plansze(plansza):
    for fragment in plansza:
        print(fragment)


def wez_rzad(plansza, nr_rzedu):
    return plansza[nr_rzedu]


def wez_kolumne(plansza, nr_rzedu):
    w = []
    for rzad in plansza:
        w.append(rzad[nr_rzedu])
    return w


def wykreuj_kandydatow(plansza, koordy, nierownosci):
    # Stworz pule mozliwych
    kandydaci = []
    kandydaci_filtr = []
    n_kord = []
    m_od = []
    w_od = []
    for kord in koordy:
        n_kord.append(kord + 1)

    for i in range(1, N+1):
        kandydaci.append(i)

    for nierownosc in nierownosci:
        if nierownosc[0] == n_kord:
            w_od.append(plansza[nierownosc[1][0] - 1][nierownosc[1][1] - 1])
        if nierownosc[1] == n_kord:
            m_od.append(plansza[nierownosc[0][0] - 1][nierownosc[0][1] - 1])
    try:
        m_od = min(m_od)
    except ValueError:
        m_od = N+1
    except TypeError:
        m_od = N + 1
    try:
        w_od = max(w_od)
    except TypeError:
        w_od = N + 1
    except ValueError:
        w_od = -1
    if m_od == None or m_od == 0:
        m_od = N+2
    if w_od == None or w_od == 0:
        w_od = -1
    for kandydat in kandydaci:
        if kandydat > w_od and kandydat < m_od:
            kandydaci_filtr.append(kandydat)

    kandydaci = []

    for kandydat in kandydaci_filtr:
        if kandydat not in wez_kolumne(plansza, koordy[1]) and kandydat not in wez_rzad(plansza, koordy[0]):
            kandydaci.append(kandydat)

    if len(kandydaci) == 0:
        kandydaci.append(0)

    return kandydaci


def wylicz_zera(decyzje):
    l = 0
    for decyzja in decyzje:
        if decyzja[3] == 0:
            l += 1
    return l


def wylosuj_rozwiaznie_sasiednie(decyzje):
    m_alternatywy = []
    pula_wyboru = []
    nowe_decyzje = []
    for decyzja in decyzje:
        if len(decyzja[2]) > 1:
            m_alternatywy.append(decyzja)
    wybrana_decyzja = random.choice(m_alternatywy)
    for l in wybrana_decyzja[2]:
        if l != wybrana_decyzja[3]:
            pula_wyboru.append(l)
    wybrana_decyzja[3] = random.choice(pula_wyboru)
    for decyzja in decyzje:
        if decyzja[0] < wybrana_decyzja[0]:
            nowe_decyzje.append(decyzja)
    nowe_decyzje.append(wybrana_decyzja)
    return nowe_decyzje


def stworz_plansze_na_podstawie_decyzji(plansza_startowa, decyzje_przyj):
    plansza = []
    nowe_decyzje = []
    d = 1
    for i in range(N):
        fragment = []
        for j in range(N):
            fragment.append(None)
        plansza.append(fragment)

    for liczba in liczby:
        plansza[liczba[0][0] - 1][liczba[0][1] - 1] = liczba[1][0]

    for decyzja in decyzje_przyj:
        plansza[decyzja[1][0]][decyzja [1][1]] = decyzja[3]
        nowe_decyzje.append(decyzja)

    for i in range(N):
        for j in range(N):
            if plansza[i][j] is None:
                kandydaci = wykreuj_kandydatow(plansza, [i, j], nierownosci)
                wybor = random.choice(kandydaci)
                plansza[i][j] = wybor
                nowe_decyzje.append([d, [i, j], kandydaci, wybor])
                d += 1
    return plansza, nowe_decyzje


# nierownosci = [[[6, 5], [5, 4]], [[4, 2], [4, 3]], [[1, 3], [2, 3]], [[2, 1], [1, 2]], [[6, 5], [5, 6]], [[5, 6], [4, 6]], [[4, 2], [4, 1]], [[4, 2], [5, 2]], [[6, 2], [5, 1]], [[6, 2], [5, 2]], [[1, 6], [2, 5]], [[4, 5], [4, 6]], [[1, 5], [2, 6]], [[5, 2], [5, 1]], [[1, 1], [2, 1]], [[1, 4], [2, 5]]]
# liczby = [[[3, 3], [6, 6]], [[3, 6], [1, 1]], [[6, 6], [6, 6]]]

# Wielka pętla
for okrazenie in range(1, 6):
    wyniki[okrazenie] = {}
    plansza = []
    for i in range(N):
        fragment =[]
        for j in range(N):
            fragment.append(None)
        plansza.append(fragment)

    liczby = generuj_l_startowe(N, 4)
    nierownosci = generuj_nierownosci(N, 18)

    wyniki[okrazenie]['liczby'] = str(liczby)
    wyniki[okrazenie]['nierownosci'] = str(nierownosci)

    "Wsadzanie liczb startowych"
    for liczba in liczby:
        plansza[liczba[0][0] - 1 ][liczba[0][1] - 1] = liczba[1][0]

    plansza_start = plansza

    decyzje = []
    akceptowane_decyzje = []
    d = 1

    czas_poczotkowy = time.time()
    # Uzupełnij losowo poczatkowa orientacje
    for i in range(N):
        for j in range(N):
            if plansza[i][j] is None:
                kandydaci = wykreuj_kandydatow(plansza, [i, j], nierownosci)
                wybor = random.choice(kandydaci)
                plansza[i][j] = wybor
                decyzje.append([d, [i, j], kandydaci, wybor])
                d += 1


    #Akceptujemy pierwszą odpowiedz
    najlepsze_decyzje = decyzje
    obecny_l = wylicz_zera(akceptowane_decyzje)
    najlepszy_l = wylicz_zera(najlepsze_decyzje)


    # Rozżarzanie Symulowane
    T_poczotkowa = 2000
    T_obecna = T_poczotkowa
    alfa = 0.95
    warunek_stopu = 1

    while T_obecna >= warunek_stopu:
        n_roz = wylosuj_rozwiaznie_sasiednie(decyzje)
        n_plansza, n_decyzje = stworz_plansze_na_podstawie_decyzji(plansza_start, n_roz)
        nowy_l = wylicz_zera(n_decyzje)


        if nowy_l < obecny_l:
            decyzje = n_decyzje
            obecny_l = nowy_l
            if nowy_l < najlepszy_l:
                najlepsze_decyzje = n_decyzje
                najlepszy_l = nowy_l

        else:
            wagi = [np.exp( -1 * ( (obecny_l - nowy_l) / T_obecna) ), 1 - np.exp( -1 * ( (obecny_l - nowy_l) / T_obecna) )]
            wartosci = [1, 0]
            wybnik = random.choices(wartosci, wagi)[0]
            if wybnik == 1:
                decyzje = n_decyzje
                obecny_l = nowy_l

        T_obecna = T_obecna * alfa

    wyniki[okrazenie]['czas'] = time.time() - czas_poczotkowy
    wyniki[okrazenie]['liczba_zer'] = najlepszy_l
    wyniki[okrazenie]['CPLEX_czas'] = 0
    wyniki[okrazenie]['CPLEX_liczba_zer'] = 0

with open("wyniki_dokladka.json", 'w') as f:
    f.write(json.dumps(wyniki, indent=2))
