# końcowy kod generujący wszystkie wykresy

import generowanie_wykresow as gw
import fashion as fs
import random
import numpy as np


def main():
    # rys. 4.1
    gw.wykres_h_rejony()

    # rys. 4.2
    random.seed(12052023)
    np.random.seed(1)
    F = fs.erdosGenerator(hc=0.3, hr=0.2)
    F.setStrategyProportions(0, 0)
    x, y, z = F.sequentialDynamic(n=4000)
    fs.proportionsPlot(x, y, z)

    # rys. 4.3
    F.setStrategyProportions(0, 0)
    x, y, z = F.sequentialDynamic(n=10000)
    fs.proportionsPlot(x, y, z)

    # rys. 4.4
    F.setStrategyProportions(0.5, 0.5)
    x, y, z = F.sequentialDynamic(n=4000)
    fs.proportionsPlot(x, y, z)

    # rys. 4.5
    random.seed(5)
    np.random.seed(5)
    F = fs.erdosGenerator(hc=0.5, hr=0.5)
    F.setStrategyProportions(0.5, 0.5)
    x, y, z = F.sequentialDynamic(n=4000)
    fs.proportionsPlot(x, y, z)

    # rys. 4.6
    F.setStrategyProportions(0.8, 0.8)
    x, y, z = F.sequentialDynamic(n=4000)
    fs.proportionsPlot(x, y, z)

    # rys. 4.7
    random.seed(2)
    np.random.seed(2)
    gw.homofilia_dynamika_przypadki()

    # rys. 4.8 i 4.9
    random.seed(3)
    np.random.seed(3)
    gw.homofilia_10_wykresow()


if __name__ == '__main__':
    main()
