import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def oblicz_odleglosc(punkt1, punkt2):
    return math.sqrt((punkt1.x - punkt2.x)**2 + (punkt1.y - punkt2.y)**2)

class Trasa:
    def __init__(self, punkty):
        self.trasa = punkty
        self.odleglosc = self.oblicz_calkowita_odleglosc()

    def oblicz_calkowita_odleglosc(self):
        calkowita_odleglosc = 0
        for i in range(len(self.trasa) - 1):
            calkowita_odleglosc += oblicz_odleglosc(self.trasa[i], self.trasa[i+1])
        return calkowita_odleglosc

def generuj_losowa_trase(punkty, punkt_startowy):
    losowe_punkty = random.sample([punkt for punkt in punkty if punkt != punkt_startowy], len(punkty) - 1)
    return Trasa([punkt_startowy] + losowe_punkty + [punkt_startowy])

def krzyzowanie(rodzic1, rodzic2):
    indeks_poczatkowy = random.randint(1, len(rodzic1.trasa) - 2)
    indeks_koncowy = random.randint(indeks_poczatkowy, len(rodzic1.trasa) - 1)
    dziecieca_trasa = rodzic1.trasa[indeks_poczatkowy:indeks_koncowy] + [punkt for punkt in rodzic2.trasa if punkt not in rodzic1.trasa[indeks_poczatkowy:indeks_koncowy]]
    return Trasa([rodzic1.trasa[0]] + dziecieca_trasa + [rodzic1.trasa[0]])

def mutacja(trasa):
    indeks1 = random.randint(1, len(trasa.trasa) - 2)
    indeks2 = random.randint(1, len(trasa.trasa) - 2)
    trasa.trasa[indeks1], trasa.trasa[indeks2] = trasa.trasa[indeks2], trasa.trasa[indeks1]

def pobierz_punkt_od_uzytkownika():
    x = float(input("Podaj współrzędną x punktu: "))
    y = float(input("Podaj współrzędną y punktu: "))
    return Punkt(x, y)

def algorytm_genetyczny(punkty, rozmiar_populacji, generacje, punkt_startowy):
    populacja = [generuj_losowa_trase(punkty, punkt_startowy) for _ in range(rozmiar_populacji)]

    najlepsze_trasy = []

    for generacja in range(generacje):
        populacja.sort(key=lambda trasa: trasa.odleglosc)

        najlepsze_trasy.append(populacja[0].trasa)

        nowa_populacja = populacja[:rozmiar_populacji // 2]
        while len(nowa_populacja) < rozmiar_populacji:
            rodzic1 = random.choice(populacja)
            rodzic2 = random.choice(populacja)
            dziecko = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko)
            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    najlepsza_trasa = min(populacja, key=lambda trasa: trasa.odleglosc).trasa
    najlepsze_trasy.append(najlepsza_trasa)

    return najlepsze_trasy

def rysuj_trase(ax, trasa, color='limegreen', label='Trasa'):
    x_wartosci = [punkt.x for punkt in trasa]
    y_wartosci = [punkt.y for punkt in trasa]

    ax.plot(x_wartosci, y_wartosci, marker='o', linestyle='-', linewidth=2, markersize=8, color=color, label=label)
    for punkt in trasa:
        ax.text(punkt.x, punkt.y, f"({punkt.x}, {punkt.y})", fontsize=8, ha='right', va='bottom')

def animuj_trasy(trasy):
    fig, ax = plt.subplots()

    def aktualizuj(frame):
        ax.clear()

        color = 'red'  # Kolor czerwony dla ostatecznej trasy
        label = 'Ostateczna trasa'
        rysuj_trase(ax, trasy[frame], color=color, label=label)

        ax.set_title(f'TSP Tour - Generacja {frame + 1}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()

    ani = FuncAnimation(fig, aktualizuj, frames=len(trasy), repeat=False)
    plt.show()

def main():
    rozmiar_populacji = int(input("Podaj rozmiar populacji: "))
    generacje = int(input("Podaj liczbę generacji - warunek stopu algorytmu: "))
    punkt_koncowy = pobierz_punkt_od_uzytkownika()
    PUNKTY = [(3, 4), (11, 5), (27, 23), (27, 25), (22, 32), (24, 34), (19, 38), (17, 37), (7, 40), (8, 36),
              (8, 28), (16, 21)]

    punkty = [Punkt(point[0], point[1]) for point in PUNKTY]

    # Dodaj punkt początkowy użytkownika do listy miast
    punkty.append(punkt_koncowy)

    # Ustaw mniejszą liczbę generacji
    najlepsze_trasy = algorytm_genetyczny(punkty, rozmiar_populacji, generacje, punkt_koncowy)
    trasa_wspolrzedne = [(punkt.x, punkt.y) for punkt in najlepsze_trasy[0]]

    print(f"Kolejnosc ostatecznej trasy: {trasa_wspolrzedne}")
    animuj_trasy(najlepsze_trasy)


if __name__ == "__main__":
    main()
