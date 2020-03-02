"""Generate a bunch of spectrograms of ripple sounds.

"""
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from scipy.signal import spectrogram


a0 = 1e-5  # reference amplitude
sr = 44100  # sample rate


def ripple_sound(dur, n, omega, w, delta, phi, f0, fm1, rand_gamma=True, l=60):
    """Synthesises a ripple sound.

    Args:
        dur (float): Duration of sound in s.
        n (int): Number of sinusoids.
        omega (:obj:`float` or `array`-like): Ripple density in Hz. Must be a single
            value or an array with length `duration * sr`.
        w (:obj:`float` or `array`-like): Ripple drift in Hz. Must be a single
            value or an array with length `duration * sr`.
        delta (:obj:`float` or `array`-like): Normalized ripple depth. Must be a single
            value or an array with length `duration * sr`. Value(s) must be in
            the range [0, 1].
        phi (float): Ripple starting phase in radians.
        f0 (float): Frequency of the lowest sinusoid in Hz.
        fm1 (float): Frequency of the highest sinusoid in Hz.
        rand_gamma (:obj:`bool`, optional): Randomize the normalized amplitudes of the
            sinusoids prior to scaling. Defaults to `False`.
        l (:obj:`float`, optional): Level in dB of the sound, assuming a pure tone with
            peak amplitude `a0` is 0 dB SPL.

    Returns:
        y (np.array): The waveform.
        a (np.array): The envelope (useful for plotting).

    """
    # create sinusoids
    m = int(dur * sr)  # total number of samples
    shapea = (1, m)
    shapeb = (n, 1)
    t = np.linspace(0, dur, int(m)).reshape(shapea)
    i = np.arange(n).reshape(shapeb)
    f = f0 * (fm1 / f0) ** (i / (n - 1))
    sphi = 2 * np.pi * np.random.random(shapeb)
    s = np.sin(2 * np.pi * f * t + sphi)

    # create envelope
    if hasattr(w, "__iter__"):
        assert len(w) == m, "w vector has incorrect length"
    else:
        w = np.tile(w, m)
    wprime = (np.cumsum(w) / sr).reshape(shapea)

    if hasattr(omega, "__iter__"):
        assert len(omega) == m, "w vector has incorrect length"
    else:
        omega = np.tile(omega, m)
    omega = omega.reshape(shapea)
    x = np.log2(f / f0)
    a = 1 + delta * np.sin(2 * np.pi * (wprime + omega * x) + phi)

    # gamma is not traditional; it was added to make sounds from complexity level 1
    # sound a bit different from one another
    if rand_gamma:
        gamma = np.random.random(shapeb)
    else:
        gamma = 1

    # create the waveform
    y = (gamma * a * s / np.sqrt(f)).sum(axis=0)
    y /= np.abs(y).max()
    y *= a0 * 10 ** (l / 20)

    return y, a


def random_walk(points, dur):
    """Return a smooth random walk.

    Creates a smooth vector of length `duration` in which the values within `points`
    are visited. `Points` are spaced equally along the vector.

    Args:
        points (:obj:`array`-like): Points to visit.


    """
    f = interp1d(np.linspace(0, dur, len(points)), points, "cubic")
    return f(np.linspace(0, dur, dur * sr))


def make_figs(seed, dpi, fontsize, labels, aspect, ticks, ext, cmap):
    """Create and plot some ripple sounds; saving the figs to the current directory.

    Args:
        seed (int): Seed the random-number generator. Choose a different value to create
            different waveforms.
        dpi (int): Resolution of figures.
        fontsize (int): For axis and tick labels.
        labels (bool): Add the category number to the top of the figure.
        aspect (float): Makes the figure longer by this factor.
        ticks (bool): Show ticks on axes.
        ext (str): File extension. For vector graphics, choose "svg". For raster, choose
            "png". Either way, the spectrogram itself is a raster; this just effects the
            axes.
        cmap (str): Name of the colormap. Default is "viridis". Other good options are
            "cividis", "plasma" and "inferno". Don't use "jet"!

    """
    # don't change these!
    dur = 1.5
    n = 1400
    ran_gamma = True
    f0 = 125.0
    fm1 = 16000.0
    phi = 0.0
    args = (phi, f0, fm1, ran_gamma)

    np.random.seed(seed)

    # set up the figures
    from matplotlib import rcParams

    figsize = rcParams["figure.figsize"]
    rcParams["figure.figsize"] = [figsize[0], int(figsize[1] * aspect)]
    rcParams["font.size"] = fontsize
    rcParams["font.family"] = "Arial"

    for i in range(1, 5):

        for j in range(1, 3):

            print(f"Making figure {j} from category {i} ...", end=" ")

            _, ax = plt.subplots(1, 1, constrained_layout=True)
            omega = np.random.random(4) * 2.5
            omega = omega[0] if i < 4 else random_walk(omega, dur)
            w = np.random.choice([-1, 1], 4) * 2 ** (np.random.random(4) * 5 + 0.5)
            if i < 3:
                w = 0
            elif i == 3:
                w = w[0]
            else:
                w = random_walk(w, dur)
            delta = 0 if i == 1 else 0.9
            y, a = ripple_sound(dur, n, omega, w, delta, *args)
            print("done making sound ...", end=" ")
            f, t, Sxx = spectrogram(y, sr, "hamming", 521)
            mask = (f >= f0) & (f <= fm1)
            f = f[mask]
            Sxx = Sxx[mask, ...]
            ax.pcolormesh(t, f, np.log(Sxx), rasterized=True)
            ax.set_yscale("log", basey=2)
            ax.set_ylabel("Frequency (Hz)")
            ax.set_xlabel("Time (s)")
            if labels:
                ax.set_title(f"Category {i}")
            if not ticks:
                ax.set_xticks([], [])
                ax.set_yticks([], [])
            print("done making figure ...", end=" ")

            f = f"ripple-{i}-{j}.{ext}"
            plt.savefig(f, dpi=dpi)
            print(f"saved to {f}")


if __name__ == "__main__":

    make_figs(0, 300, 18, True, 1.5, True, "png", "viridis")
