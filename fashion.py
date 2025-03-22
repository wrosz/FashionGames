# definicja klasy FashionGraph i związanych z nią funkcji

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

class FashionGraph(nx.Graph):
    def __init__(self, G=nx.Graph(), fc=0.5, x=0.5, y=0.5):
        """Tworzy obiekt FashionGraph o takich samych wierzchołkach i krawędziach, co graf G (domyślnie graf pusty).
        Losowo przydziela wierzchołkom typy C oraz R oraz strategie 0 albo 1.
        Argumenty:
        G=nx.Graph() - dowolny obiekt klasy nx.Graph()
        fc=0.5 - odsetek konformistów w grafie modowym, liczba z przedziału [0,1]
        x=0.5 - odsetek konformistów grających strategią 0 w populacji konformistów, liczba z przedziału [0,1]
        y=0.5 - odsetek rebeliantów grających strategią 0 w populacji rebeliantów, liczba z przedziału [0,1]"""

        # sprawdzenie poprawności argumentów:
        if not isinstance(G, nx.Graph):
            raise ValueError('G musi być obiektem klasy nx.Graph')
        if not 0 <= fc <= 1 or not 0 <= x <= 1 or not 0 <= y <= 1:
            raise ValueError('fc, x, y muszą być liczbami z przedziału [0, 1]')

        super().__init__()
        self.add_nodes_from(G.nodes(data=True))
        self.add_edges_from(G.edges(data=True))

        nc = int(fc*self.number_of_nodes())  # liczba konformistów
        nr = self.number_of_nodes() - nc  # liczba rebeliantów
        nc0 = int(nc*x)  # liczba konformistów grających strategią 0
        nr0 = int(nr*y)  # liczba rebeliantów grających strategią 0

        # przypisanie losowych typów i strategii wierzchołków:
        wierzcholki = np.arange(self.number_of_nodes())
        np.random.shuffle(wierzcholki)
        c0 = wierzcholki[0:nc0]
        c1 = wierzcholki[nc0:nc]
        r0 = wierzcholki[nc:nc+nr0]
        r1 = wierzcholki[nc+nr0:]
        for i in c0:
            self.nodes[i]['type'] = 'C'
            self.nodes[i]['strategy'] = 0
        for i in c1:
            self.nodes[i]['type'] = 'C'
            self.nodes[i]['strategy'] = 1
        for i in r0:
            self.nodes[i]['type'] = 'R'
            self.nodes[i]['strategy'] = 0
        for i in r1:
            self.nodes[i]['type'] = 'R'
            self.nodes[i]['strategy'] = 1

    def setStrategyProportions(self, x, y):
        """Ustawia profil strategii, aby proporcje graczy grających strategią 0 były odpowiednie.
        Argumenty:
        x=0.5 - odsetek konformistów grających strategią 0 w populacji konformistów, liczba z przedziału [0,1]
        y=0.5 - odsetek rebeliantów grających strategią 0 w populacji rebeliantów, liczba z przedziału [0,1]."""

        if not 0 <= x <= 1 or not 0 <= y <= 1:
            raise ValueError('fc, x, y muszą być liczbami z przedziału [0, 1]')

        c0 = int(self.number_of_conformists() * x)
        r0 = int(self.number_of_rebels() * y)
        for i in self.conformists()[:c0]:
            self.nodes[i]['strategy'] = 0
        for i in self.conformists()[c0:]:
            self.nodes[i]['strategy'] = 1
        for i in self.rebels()[:r0]:
            self.nodes[i]['strategy'] = 0
        for i in self.rebels()[r0:]:
            self.nodes[i]['strategy'] = 1

    def copy(self, as_view=False):
        """Tworzy kopię obiektu FashionGraph"""
        if as_view is True:
            return nx.graphviews.generic_graph_view(self)
        G = self.__class__(self)
        G.graph.update(self.graph)
        G.add_nodes_from((n, d.copy()) for n, d in self._node.items())
        G.add_edges_from(
            (u, v, datadict.copy())
            for u, nbrs in self._adj.items()
            for v, datadict in nbrs.items()
        )
        return G

    def number_of_conformists(self):
        """Zwraca liczbę konformistów grafu modowego"""
        suma = 0
        for i in self:
            if self.nodes[i]['type'] == 'C':
                suma += 1
        return suma

    def conformists(self):
        """Zwraca tablicę (1-wymiarowy obiekt klasy numpy.array) z liczbami całkowitymi
        odpowiadającymi konformistom grafu modowego"""
        tablica = np.empty(self.number_of_conformists(), dtype=int)
        k = 0
        for i in self:
            if self.nodes[i]['type'] == 'C':
                tablica[k] = i
                k += 1
        return tablica

    def number_of_rebels(self):
        """Zwraca liczbę rebeliantów grafu modowego"""
        return self.number_of_nodes() - self.number_of_conformists()

    def rebels(self):
        """Zwraca tablicę (1-wymiarowy obiekt klasy numpy.array) z liczbami całkowitymi
        odpowiadającymi rebeliantom grafu modowego"""
        tablica = np.empty(self.number_of_rebels(), dtype=int)
        k = 0
        for i in self:
            if self.nodes[i]['type'] == 'R':
                tablica[k] = i
                k += 1
        return tablica

    def nc0(self):
        """Liczba konformistów grających strategią 0"""
        suma = 0
        for i in self:
            if self.nodes[i]['type'] == 'C' and self.nodes[i]['strategy'] == 0:
                suma += 1
        return suma

    def nr0(self):
        """Liczba rebeliantów grających strategią 0"""
        suma = 0
        for i in self:
            if self.nodes[i]['type'] == 'R' and self.nodes[i]['strategy'] == 0:
                suma += 1
        return suma

    def homophily(self, typ='all'):
        """Zwraca zadany parametr związany z homofilią grafu modowego.
        Możliwe wartości argumentu 'typ':
        'C' - zwraca homofilię konformistów h_c,
        'R' - zwraca homofilię rebeliantów h_r,
        'avg' - zwraca średnią homofilię h,
        'all' - zwraca krotkę postaci (h_c, h_r, h).
        """
        if typ not in ['C', 'R', 'avg', 'all']:
            raise ValueError('Typ powinien być wyrazem "C", "R", "avg" albo "all"')
        kcc = 0
        kcr = 0
        krr = 0
        for e in self.edges:
            i, j = e
            if self.nodes[i]['type'] == 'C' and self.nodes[j]['type'] == 'C':
                kcc += 1
            elif self.nodes[i]['type'] == 'R' and self.nodes[j]['type'] == 'R':
                krr += 1
            else:
                kcr += 1
        hc = 2 * kcc / (2 * kcc + kcr)
        hr = 2 * krr / (2 * krr + kcr)
        if typ == 'C':
            return hc
        elif typ == 'R':
            return hr
        elif typ == 'avg':
            return (hc + hr) / 2
        else:
            return hc, hr, (hc + hr) / 2

    def utility(self, i):
        """Wypłata gracza i w grafie modowym"""
        suma = 0
        for j in self[i]:
            if self.nodes[j]['strategy'] == self.nodes[i]['strategy']:
                suma += 1
            else:
                suma -= 1
        if self.nodes[i]['type'] == 'C':
            return suma
        else:
            return -suma

    def sequentialDynamic(self, n=100):
        """Zwraca trzy tablice, zawierające proporcje x(t), y(t) oraz z(t) w zależności od iteracji.
        Na grafie rozgrywana jest dynamika sekwencyjna.
        Argumenty:
        n - maksymalna liczba iteracji, liczba naturalna
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError('n musi być liczbą naturalną.')

        nc = self.number_of_conformists()
        nr = self.number_of_rebels()

        # uniknięcie dzielenia przez 0 w przypadku homogenicznego grafu
        if nc == 0:
            warnings.warn('W grafie nie występują konformiści.\nFunkcja x jest stale równa 0.')
            nc = -1
        if nr == 0:
            warnings.warn('W grafie nie występują rebelianci.\nFunkcja y jest stale równa 0.')
            nr = -1

        x = np.empty(n)
        y = np.empty(n)
        z = np.empty(n)
        liczba_zmian = 0

        wierzcholki = np.arange(self.number_of_nodes())

        for k in range(n):
            print("", end=f"\rPostęp: {round(k/n*100, 0)} %")
            nc0 = self.nc0()
            nr0 = self.nr0()
            x[k] = nc0 / nc
            y[k] = nr0 / nr
            z[k] = (nc0 + nr0) / (nc + nr)
            np.random.shuffle(wierzcholki)

            # sprawdzenie, czy mamy równowagę Nasha:
            czy_rownowaga_znaleziona = True
            for i in range(self.number_of_nodes()):
                wierzcholek = wierzcholki[i]
                if self.utility(wierzcholek) < 0:
                    czy_rownowaga_znaleziona = False
                    liczba_zmian += 1
                    self.nodes[wierzcholek]['strategy'] = 1 - self.nodes[wierzcholek]['strategy']
                    break
            if czy_rownowaga_znaleziona:
                print('\nRównowaga Nasha znaleziona po %s iteracjach.' % k)
                break

        if k == n - 1:
            print('\nRównowaga Nasha nie została znaleziona po %s iteracjach.' % n)

        x = x[0:k]
        y = y[0:k]
        z = z[0:k]

        return x, y, z


def proportionsPlot(x, y, z, animate=False):
    """Rysuje wykresy proporcji x, y, z w zależności od czasu.
    Argumenty:
    x, y, z - tablice zwrócone za pomocą funkcji sequentialDynamic()
    animate - zmienna logiczna, jeśli animate==True, to wykresy są animowane."""
    if not isinstance(animate, bool):
        raise TypeError('Zmienna animate musi być zmienną logiczną.')

    k = len(x)
    fig, axs = plt.subplots(2, 1)
    fig.suptitle('Popularność strategii 0 w grze modowej', fontsize=16)

    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)
    axs[0].set_aspect('equal', 'box')
    axs[0].set_xlabel('Konformiści')
    axs[0].set_ylabel('Rebelianci')
    axs[0].grid(True)

    axs[1].set_xlim(0, k - 1)
    axs[1].set_ylim(0, 1)
    axs[1].set_xlabel('Iteracja')
    axs[1].set_ylabel('Wartości')

    axs[1].grid(True)

    if animate is True:
        line1, = axs[0].plot([], [], animated=True, lw=1)
        current_point, = axs[0].plot([], [], 'o', animated=True)
        line2, = axs[1].plot([], [], label='Konformiści', alpha=0.5, animated=True)
        line3, = axs[1].plot([], [], label='Rebelianci', alpha=0.5, animated=True)
        line4, = axs[1].plot([], [], label='Wszyscy gracze', animated=True)
        axs[1].legend(prop={'size': 5})

        def init():
            line1.set_data([], [])
            current_point.set_data([], [])
            line2.set_data([], [])
            line3.set_data([], [])
            return line1, line2, line3, line4, current_point

        def update(frame):
            line1.set_data(x[:frame], y[:frame])
            current_point.set_data([x[frame - 1]], [y[frame - 1]])
            line2.set_data(range(frame), x[:frame])
            line3.set_data(range(frame), y[:frame])
            line4.set_data(range(frame), z[:frame])
            return line1, line2, line3, line4, current_point

        FuncAnimation(fig, update, frames=range(1, k + 1), init_func=init, blit=True, repeat=False, interval=1.5)

    else:
        axs[0].plot(x, y, lw=1)
        axs[1].plot(x, label='Konformiści', alpha=0.5)
        axs[1].plot(y, label='Rebelianci', alpha=0.5)
        axs[1].plot(z, label='Wszyscy gracze')
        axs[1].legend(prop={'size': 5})

    plt.tight_layout()
    plt.show()


def erdosGenerator(hc, hr, fc=0.5, n=400):
    """Generuje losowe grafy modowe o zadanych parametrach homofilii.
    Argumenty:
    hc - oczekiwana homofilia konformistów, liczba z przedziału [0,1],
    hr - oczekiwana homofilia rebeliantów, liczba z przedziału [0,1],
    fc=0.5 - odsetek konformistów w populacji, liczba z przedziału [0,1],
    n=100 - liczba wierzchołków, liczba naturalna."""

    if not all((0 <= hc <= 1, 0 <= hr <= 1, 0 <= fc <= 1)):
        raise ValueError('Parametry hc, hr, fc muszą być liczbami całkowitymi z przedziału [0,1]')
    if not isinstance(n, int) or n < 0:
        raise ValueError('n musi być liczbą naturalną')

    # ustawienie parametrów pcc, prr, pcr:
    G = nx.Graph()
    G.add_nodes_from(np.arange(n))
    F = FashionGraph(G, fc=fc)
    if hc == 1 or hr == 1:
        warnings.warn('Homofilia jednej ze zmiennych równa 1 implikuje, że druga również musi być 1.'
                      'Ustawiam pcr=0, a prr oraz pcc są losowe.')
        pcc = random.random()
        prr = random.random()
        pcr = 0
    else:
        pcr = 0.8
        pcc = (n * pcr * hc * (1 - fc)) / ((1 - hc) * (n * fc - 1))
        prr = (n * pcr * hr * fc) / ((1 - hr) * (n - n * fc - 1))
        while pcc >= 1 or prr >= 1:
            pcr /= 1.5
            pcc = (n * pcr * hc * (1 - fc)) / ((1 - hc) * (n * fc - 1))
            prr = (n * pcr * hr * fc) / ((1 - hr) * (n - n * fc - 1))

    # łączenie wierzchołków krawędziami z odpowiednim prawdopodobieńswtem:
    konformisci = F.conformists()
    rebelianci = F.rebels()
    nc = F.number_of_conformists()
    nr = F.number_of_rebels()
    for i in range(nc):
        for j in range(i):
            if random.random() < pcc:
                F.add_edge(konformisci[i], konformisci[j])
        for j in range(nr):
            if random.random() < pcr:
                F.add_edge(konformisci[i], rebelianci[j])
    for i in range(nr):
        for j in range(i):
            if random.random() < prr:
                F.add_edge(rebelianci[i], rebelianci[j])

    return F

