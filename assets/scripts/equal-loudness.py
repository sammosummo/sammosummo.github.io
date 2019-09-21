import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import rcParams as defaults

f = np.array(
    [
        20,
        25,
        31.5,
        40,
        50,
        63,
        80,
        100,
        125,
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000,
        10000,
        12500,
    ]
)
af = np.array(
    [
        0.532,
        0.506,
        0.480,
        0.455,
        0.432,
        0.409,
        0.387,
        0.367,
        0.349,
        0.330,
        0.315,
        0.301,
        0.288,
        0.276,
        0.267,
        0.259,
        0.253,
        0.250,
        0.246,
        0.244,
        0.243,
        0.243,
        0.243,
        0.242,
        0.242,
        0.245,
        0.254,
        0.271,
        0.301,
    ]
)
Lu = np.array(
    [
        -31.6,
        -27.2,
        -23.0,
        -19.1,
        -15.9,
        -13.0,
        -10.3,
        -8.1,
        -6.2,
        -4.5,
        -3.1,
        -2.0,
        -1.1,
        -0.4,
        0.0,
        0.3,
        0.5,
        0.0,
        -2.7,
        -4.1,
        -1.0,
        1.7,
        2.5,
        1.2,
        -2.1,
        -7.1,
        -11.2,
        -10.7,
        -3.1,
    ]
)
Tf = np.array(
    [
        78.5,
        68.7,
        59.5,
        51.1,
        44.0,
        37.5,
        31.5,
        26.5,
        22.1,
        17.9,
        14.4,
        11.4,
        8.6,
        6.2,
        4.4,
        3.0,
        2.2,
        2.4,
        3.5,
        1.7,
        -1.3,
        -4.2,
        -6.0,
        -5.4,
        -1.5,
        6.0,
        12.6,
        13.9,
        12.3,
    ]
)


def elc(phon, frequencies=None):
    """Returns an equal-loudness contour.

    Args:
        phon (float): Phon value of the contour.
        frequencies (:obj:`np.ndarray`, optional): Frequencies to evaluate. If not
            passed, all 29 points of the ISO standard are returned. Any frequencies not
            present in the standard are found via spline interpolation.

    Returns:
        contour (np.ndarray): db SPL values.

    """
    assert 0 <= phon <= 90, f"{phon} is not [0, 90]"
    Ln = phon
    Af = (
        4.47e-3 * (10 ** (0.025 * Ln) - 1.15)
        + (0.4 * 10 ** (((Tf + Lu) / 10) - 9)) ** af
    )
    Lp = ((10.0 / af) * np.log10(Af)) - Lu + 94

    if frequencies is not None:

        assert frequencies.min() >= f.min(), "Frequencies are too low"
        assert frequencies.max() <= f.max(), "Frequencies are too high"
        tck = interpolate.splrep(f, Lp, s=0)
        Lp = interpolate.splev(frequencies, tck, der=0)

    return Lp


def plot_elcs():
    """Makes the equal-loudness-contour plot.

    """
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    x = np.logspace(np.log10(f.min()), np.log10(f.max()), 1000)

    for p in range(0, 100, 10):
        c, l = ("C0", None) if p != 60 else ("C1", "60 phon")
        ax.plot(x, elc(p, x), c=c, label=l)

    ax.legend(fancybox=False, framealpha=0)
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Sound pressure level (dB)")
    plt.savefig(
        f"../../assets/images/equal-loudness-contours.svg",
        bbox_inches=0,
        transparent=True,
    )


if __name__ == "__main__":

    plot_elcs()
