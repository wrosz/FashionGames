# pliki części kodu, które końcowo nie zostały użyte w pracy,
# ale mogą być przydatne przy dalszym rozwijaniu projektu

import networkx as nx
import numpy as np
import random
import subprocess

# z klasy FashionGraph:

def drawFashionGraph(self, nazwa_pliku='drawFashionGraph_output.tex', as_pdf=True, node_label='u'):
    sciezka_do_pliku = 'grafiki/drawFashionGraph/' + nazwa_pliku  # żeby się zapisywało w osobnym folderze
    figure_wrapper = '\\begin{{figure}}\n\\centering\n{content}{caption}{label}\n\\end{{figure}}'
    for i in self:
        if self.nodes[i]['type'] == 'C':
            string = 'circle, draw, '
        else:
            string = 'rectangle, draw, '
        if self.nodes[i]['strategy'] == 0:
            string = string + 'fill=black!20'
        else:
            string = string + 'fill=white'
        self.nodes[i]['options'] = string
    if node_label == 'u':
        for i in range(self.number_of_nodes()):
            self.nodes[i]['label'] = self.utility(i)
    elif node_label == '':
        pass
    else:
        raise ValueError('Argument "label" powinien przyjmować wartość "\'\'" lub "u"')
    label = nx.get_node_attributes(self, 'label', default='')
    options = nx.get_node_attributes(self, 'options')
    if as_pdf is True:
        nx.write_latex(self, sciezka_do_pliku, tikz_options='scale=3', node_label=label, node_options=options,
                       as_document=True, figure_wrapper=figure_wrapper)
        subprocess.run(
            'pdflatex -output-directory=C:\\Users\\17ros\PycharmProjects\licencjat\grafiki\drawFashionGraph ' + sciezka_do_pliku,
            capture_output=False, check=True, stdout=subprocess.DEVNULL)
        print('Graf został narysowany chyba pomyślnie.')
    else:
        return nx.to_latex(self, tikz_options='scale=3', node_label=label, node_options=options, as_document=False,
                           figure_wrapper=figure_wrapper)

def wieksze_dynamic(self, p, n):
    # uwzględnia inne przypadki dynamiki niż sekwencyjna
    """Rysuje wykresy proporcji x(t) oraz y(t) w zależności od iteracji.
            Argumenty:
            p - prawdopodobieństwo, że niezadowolony gracz zmieni strategię
            p = 'smoothed'  ->  wygładzona dynamika sekwencyjna
            p = 'seq'  ->  dynamika sekwencyjna
            0 < p < 1  ->  dynamika asynchroniczna
            p = 'sim' lub 1  ->  dynamika symultaniczna
            n - maksymalna liczba iteracji"""

    # sprawdzenie poprawności argumentu p
    if p not in ['smoothed', 'seq', 'sim']:
        if not isinstance(p, (int, float)):
            raise ValueError('Argument p musi być liczbą albo słowem "sim", "smoothed" lub "seq"')
        elif not 0 < p <= 1:
            raise ValueError('Jeśli p jest liczbą, to musi spełniać 0 < p <= 1')

    if p == 'sim':
        p = 1

    nc = self.number_of_conformists()
    nr = self.number_of_rebels()

    if nc == 0:
        nc = -1
    if nr == 0:
        nr = -1

    x = np.empty(n)
    y = np.empty(n)
    z = np.empty(n)  # Proporcja graczy grających strategią 0
    liczba_zmian = 0

    wierzcholki = np.arange(self.number_of_nodes())

    for k in range(n):
        czy_rownowaga_znaleziona = True
        print("", end=f"\rPercentComplete: {round(k / n * 100, 0)} %")
        nc0 = self.nc0()
        nr0 = self.nr0()
        x[k] = nc0 / nc
        y[k] = nr0 / nr
        z[k] = (nc0 + nr0) / (nc + nr)

        if p == 'smoothed':  # dynamika jak w Fashion and Homophily

            # sprawdzenie, czy mamy równowagę Nasha:
            for i in self:
                if self.utility(i) < 0:
                    czy_rownowaga_znaleziona = False
                    break
            if czy_rownowaga_znaleziona:
                print('\nRównowaga Nasha znaleziona po %s iteracjach.' % k)
                break

            wierzcholek = random.randint(0, self.number_of_nodes() - 1)
            update_probability = max(0, -self.utility(wierzcholek) / self.degree(wierzcholek))

            if random.random() <= update_probability:
                liczba_zmian += 1
                self.nodes[wierzcholek]['strategy'] = 1 - self.nodes[wierzcholek]['strategy']

        else:  # dynamika sekwencyjna/asynchroniczna/symultaniczna
            np.random.shuffle(wierzcholki)
            for i in range(self.number_of_nodes()):
                wierzcholek = wierzcholki[i]
                if self.utility(wierzcholek) < 0:
                    czy_rownowaga_znaleziona = False
                    if p == 'seq':  # dynamika sekwencyjna
                        liczba_zmian += 1
                        self.nodes[wierzcholek]['strategy'] = 1 - self.nodes[wierzcholek]['strategy']
                        break
                    else:  # dynamika asynchroniczna/symultaniczna
                        if random.random() <= p:
                            liczba_zmian += 1
                            self.nodes[wierzcholek]['strategy'] = 1 - self.nodes[wierzcholek]['strategy']
            if czy_rownowaga_znaleziona:
                print('\nRównowaga Nasha znaleziona po %s iteracjach.' % k)
                break

        if k == n - 1:
            print('\nRównowaga Nasha nie została znaleziona po %s iteracjach.' % n)

    print(f'Łącznie wprowadzono {liczba_zmian} zmian strategii.')

    x = x[0:k]
    y = y[0:k]
    z = z[0:k]

    return x, y, z


# animowanie grafów:
import subprocess
import fitz
from moviepy.editor import ImageSequenceClip

# funkcje do robienia animacji z dynamiką:
def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"page_{page_num + 1}.png"
        pix.save(image_path)
        images.append(image_path)
    return images


def images_to_video(image_paths, output_path, fps=1):
    clip = ImageSequenceClip(image_paths, fps=fps)
    clip.write_videofile(output_path, codec='libx264')


def dynamicToPDF(lista_grafow, nazwa_pliku='dynamictopdf_output.tex', node_label='u'):
    sciezka_do_pliku = 'grafiki/dynamicToPDF/' + nazwa_pliku
    plik = open(sciezka_do_pliku, 'w')  # żeby się zapisywało w osobnym folderze
    plik.write('\documentclass{report}\n\\usepackage{tikz}\n\\usepackage{subcaption}')
    plik.write('\\begin{document}\n')
    graf = lista_grafow[0]
    plik.write(graf.drawFashionGraph(node_label=node_label, as_pdf=False))  # początkowe strategie
    for graf in lista_grafow[1:]:
        plik.write('\n\\clearpage\n')
        plik.write(graf.drawFashionGraph(node_label=node_label, as_pdf=False))
    plik.write('\n\\end{document}')
    plik.close()
    subprocess.run('pdflatex -output-directory=C:\\Users\\17ros\PycharmProjects\licencjat\grafiki\dynamicToPDF ' +sciezka_do_pliku, capture_output=False, check=True, stdout=subprocess.DEVNULL)
    print('PDF z dynamiką wygenerowany chyba pomyślnie.')