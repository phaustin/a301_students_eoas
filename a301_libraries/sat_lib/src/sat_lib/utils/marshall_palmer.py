import numpy as np
from matplotlib import pyplot as plt


def marshall_dist(Dvec, RR):
    """
    Calcuate the Marshall Palmer drop size distribution

    Input: Dvec: vector of diameters in mm
           RR: rain rate in mm/hr
    output: n(Dvec), length of Dvec, in m^{-3} mm^{-1}
    """
    N0 = 8000  # m^{-3} mm^{-1}
    the_lambda = 4.1 * RR ** (-0.21)
    output = N0 * np.exp(-the_lambda * Dvec)
    return output


def plot_marshall():
    Dvec = np.arange(0, 5, 0.1)  # mm
    rr_1 = marshall_dist(Dvec, 1.0)
    rr_5 = marshall_dist(Dvec, 5.0)
    rr_25 = marshall_dist(Dvec, 25.0)

    fig = plt.figure(1)
    fig.clf()
    ax1 = fig.add_subplot(111)
    ax1.semilogy(Dvec, rr_1, label="1 mm/hr")
    ax1.semilogy(Dvec, rr_5, label="5 mm/hr")
    ax1.semilogy(Dvec, rr_25, label="25 mm/hr")
    ax1.set_xlabel("Drop diameter (mm)")
    ax1.set_ylabel("$n(D)\ m^{-3}\,mm^{-1}$")
    ax1.set_title("Marshall Palmer distribution for three rain rates")
    ax1.set_ylim([0.1, 1.0e4])
    ax1.legend()
    fig.savefig("marshall_palmer.png")
    plt.show()

