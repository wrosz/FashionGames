# funkcje używane do generowania ilustracji w pracy licencjackiej

import matplotlib.pyplot as plt
import fashion as fs
import random
import numpy as np


def wykres_h_rejony():
    offs = 0.012  # odstęp linii przerywanych od grubych
    fontsize = 16

    # linie oddzielające (i1) oraz (i2):
    plt.plot([0, 0.5], [0, 0.5], lw=1, color='black', alpha=0.5)
    plt.plot([0, 0.5], [offs, 0.5 + offs], '--', lw=1, color='black', alpha=0.5)  # linia oddzielająca (i2) na dole
    plt.plot([offs, 0.5 + offs], [0, 0.5], '--', lw=1, color='black', alpha=0.5)  # linia oddzielająca (i1) po lewej

    # linie oddzielające (ii) oraz (iii):
    plt.plot([0.5, 1], [0.5, 0.5], lw=1, color='black', alpha=0.5)
    plt.plot([0.5, 1], [0.5 - offs, 0.5 - offs], '--', lw=1, color='black', alpha=0.5)  # oddziela (iii) od góry

    plt.plot([0.5, 0.5], [0, 0.5], lw=3, color='C0')  # linia (v)
    plt.plot([0.5 - offs, 0.5 - offs], [0, 0.5], '--', lw=1, color='black', alpha=0.5)  # oddziela (i1) od prawej
    plt.plot([0.5 + offs, 0.5 + offs], [0, 0.5], '--', lw=1, color='black', alpha=0.5)  # oddziela (iv) od lewej

    plt.plot([0, 0.5], [1, 0.5], lw=3, color='C1')  # linia (vi)
    plt.plot(0.5, 0.5, 'o', color='C1', markersize=10, zorder=100)
    plt.plot([0, 0.5], [1 - offs, 0.5 - offs], '--', lw=1, color='black', alpha=0.5)  # oddziela (i2) od góry
    plt.plot([0 + offs, 0.5 + offs], [1, 0.5], '--', lw=1, color='black', alpha=0.5)  # oddziela (ii) od lewej

    plt.plot([0.5, 1], [0.5, 0], lw=3, color='C2')  # linia (vii)
    plt.plot([0.5 - offs, 1 - offs], [0.5, 0], '--', lw=1, color='black', alpha=0.5)  # oddziela (iv) od prawej
    plt.plot([0.5, 1], [0.5 + offs, 0 + offs], '--', lw=1, color='black', alpha=0.5)  # oddziela (iii) od dołu

    plt.text(0.3, 0.2, '$(i1)$', fontsize=fontsize)
    plt.text(0.2, 0.5, '$(i2)$', fontsize=fontsize)
    plt.text(0.7, 0.7, '$(ii)$', fontsize=fontsize)
    plt.text(0.8, 0.3, '$(iii)$', fontsize=fontsize)
    plt.text(0.6, 0.15, '$(iv)$', fontsize=fontsize)
    plt.text(0.47, 0.2, '$(v)$', fontsize=fontsize, rotation=90)
    plt.text(0.25, 0.64, '$(vi)$', fontsize=fontsize, rotation=-45)
    plt.text(0.72, 0.15, '$(vii)$', fontsize=fontsize, rotation=-45)

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.axis('square')
    plt.xlabel('$h_C$')
    plt.ylabel('$h_R$')
    plt.show()


def homofilia_dynamika_przypadki(liczba_wierzcholkow=400, liczba_iteracji=4000):
    przypadek = [(None, None) for i in range(8)]

    # (i1)
    hc = random.uniform(0.1, 0.45)
    przypadek[0] = (hc, random.uniform(0.05, hc-0.05))

    # (i2)
    hc = random.uniform(0.05, 0.45)
    hr = random.uniform(hc+0.05, 0.95-hc)
    przypadek[1] = (hc, hr)

    # (ii)
    hc = random.uniform(0.1, 0.95)
    przypadek[2] = (hc, random.uniform(max(0.55, 1.05-hc), 0.95))

    # (iii)
    hc = random.uniform(0.6, 0.95)
    przypadek[3] = (hc, random.uniform(1.05-hc, 0.45))

    # (iv)
    hc = random.uniform(0.55, 0.9)
    przypadek[4] = (hc, random.uniform(0.05, 0.95-hc))

    # (v)
    przypadek[5] = (0.5, random.uniform(0.5, 0.45))

    # (vi)
    hc = random.uniform(0.05, 0.45)
    przypadek[6] = (hc, 1 - hc)

    # (vii)
    hc = random.uniform(0.55, 0.95)
    przypadek[7] = (hc, 1 - hc)

    fig, axs = plt.subplots(4, 8)
    plt.rc('font', size=8)
    for i in range(0, 8):
        nr_przypadku = ['$i1$', '$i2$', '$ii$', '$iii$', '$iv$', '$v$', '$vi$', '$vii$'][i]
        hc, hr = przypadek[i]
        print(f'\nPrzypadek {nr_przypadku}')
        F1 = (fs.erdosGenerator(hc, hr, n=liczba_wierzcholkow))
        hc_rz = F1.homophily('C')
        hr_rz = F1.homophily('R')
        F = (F1, F1.copy())
        F[1].setStrategyProportions(0.8, 0.8)
        for j in range(2):
            print(f'{j + 1}:')
            (x, y, z) = F[j].sequentialDynamic(n=liczba_iteracji)
            k = len(x)
            if k < liczba_iteracji-2:
                print(f'(x_{j+1}, y_{+1}) = ({x[-1]}, {y[-1]})')  # wypisanie końcowych proporcji, aby porównać je
                # z punktami stabilnymi asymptotycznie RRZ
            axs[2*j, i].set_xlim(0, 1)
            axs[2*j, i].set_ylim(0, 1)
            axs[2*j, i].set_aspect('equal', 'box')
            col = 'green' if k < liczba_iteracji-2 else 'red'
            axs[2*j, i].plot(x, y, lw=1, color=col)
            axs[2*j, i].tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
            axs[1+2*j, i].set_xticks([k+1])
            axs[1+2*j, i].tick_params(left=False, right=False, labelleft=False, labelbottom=True, bottom=False)
            axs[1+2*j, i].set_aspect(0.8)
            axs[1+2*j, i].set_xlim(0, k+1)
            axs[1+2*j, i].set_ylim(0, 1)
            axs[1+2*j, i].set_aspect(k/2)
            axs[1+2*j, i].plot(x, alpha=0.5)
            axs[1+2*j, i].plot(y, alpha=0.5)
            axs[1+2*j, i].plot(z)

            if i == 6:  # rysowanie prostej globalnie przyciągającej
                axs[2*j, i].plot([0, 1], [1 / (2 * (1 - hc_rz)), 1 / (2 * (1 - hc_rz)) - hc_rz / (1 - hc_rz)], '--',
                                 color='black', lw=0.7)

            if j == 0:
                axs[j, i].set_title(f'Przypadek ({nr_przypadku})\n'
                                    f'hc={round(hc_rz,2)}, hr={round(hr_rz,2)}\n'
                                    f'{F1.number_of_edges()} krawędzi')
    plt.tight_layout()
    plt.show()


def homofilia_10_wykresow():
    def fun_pom(F):  # zwraca liczbę wierzchołków o h_ind(i) < 1/2
        konformisci = F.conformists()
        suma = 0
        for i in konformisci:
            sasiedzi_konformisci = np.intersect1d(list(F[i]), konformisci, assume_unique=True)
            if len(sasiedzi_konformisci) >= 0.5 * F.degree(i):
                suma += 1
        return suma

    ods_ind = np.empty((10, 10), dtype=float)  # tablica do zapełnienia wartościami z fun_pom()

    fig, axs = plt.subplots(11, 11)
    for i in range(11):
        for j in range(11):
            print(i, j)

            axs[i, j].set_xlim(0, 1)
            axs[i, j].set_ylim(0, 1)
            axs[i, j].set_aspect('equal', 'box')
            axs[i, j].tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)

            hc = j / 10
            hr = (10 - i) / 10

            if (hc == 1 and hr != 1) or (hr == 1 and hc != 1):
                axs[i, j].set_facecolor('black')
                continue

            F = fs.erdosGenerator(hc=hc, hr=hr, n=400)
            F.setStrategyProportions(0.8, 0.8)
            (x, y, z) = F.sequentialDynamic(n=4000)
            k = len(x)
            col = 'green' if k < 3998 else 'red'
            axs[i, j].plot(x, y, lw=1, color=col)

            # kolory:
            h = (hc + hr) / 2
            if h < 1 / 2 and 1 / 2 > hc > hr:
                przyp = 0
            elif h < 1 / 2 and hc < 1 / 2 and hr > hc:
                przyp = 1
            elif h > 1 / 2 and hr >= 1 / 2:
                przyp = 2
            elif h > 1 / 2 and hr < 1 / 2:
                przyp = 3
            elif h < 1 / 2 and hc > 1 / 2:
                przyp = 4
            elif h < 1 / 2 and hc == 1 / 2:
                przyp = 5
            elif h == 1 / 2 and hc <= 1 / 2:
                przyp = 6
            elif h == 1 / 2 and hc > 1 / 2:
                przyp = 7
            else:
                przyp = 9  # linia oddzielajaca (i1) oraz (i2)
            axs[i, j].set_facecolor(('C' + str(przyp), 0.2))

            # do wykresu nr 2:
            if i != 0 and j != 10:
                ods_ind[i-1, j] = fun_pom(F)/200

    # tytuły:
    for j in range(11):
        axs[10, j].text(0.5, -0.1, f'$h_C$={j / 10}', ha='center', va='top')
    for i in range(11):
        axs[i, 0].text(-0.1, 0.5, f'$h_R$={(10 - i) / 10}', ha='right', va='center')

    # wykres indywidualnej homofilii:
    plt.figure(2)
    plt.imshow(ods_ind, extent=[0, 1, 0, 1], cmap='spring')
    plt.grid(which='both')
    ticks = np.arange(0, 1.1, 0.1)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.xlabel('$h_C$')
    plt.ylabel('$h_R$')
    plt.colorbar()
    plt.title('Odsetek konformistów spełniających $h_{ind}(i) \geq 0.5$')

    # podpisanie komórek ich wartościami
    num_rows, num_cols = ods_ind.shape
    for i in range(num_rows):
        for j in range(num_cols):
            x_pos = (j + 0.5) / num_cols
            y_pos = (num_rows - i - 0.5) / num_rows
            plt.text(x_pos, y_pos, f'{round(ods_ind[i, j], 2)}', color='black',
                     ha='center', va='center', fontsize=8)

    plt.show()

