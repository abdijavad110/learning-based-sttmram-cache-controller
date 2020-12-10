import sys
import matplotlib
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from plt import parse_log, parse_borders, plot_borders

MIN, MAX, BINS, TITLE = 47080010194960, 47080010428432, 200, "histogram of sth"

if __name__ == '__main__':
    lls = parse_log()
    x_borders, _ = parse_borders()
    if len(sys.argv) == 5:
        MIN, MAX, BINS, TITLE = sys.argv[1:5]
        MIN, MAX, BINS = int(MIN), int(MAX), int(BINS),

    plot_borders(tts=x_borders, labels=True)
    lls = list(map(lambda q: q[0], filter(lambda q: MIN < q[1] < MAX, lls)))
    plt.hist(lls, label=TITLE, bins=BINS)
    plt.legend()
    plt.show()
