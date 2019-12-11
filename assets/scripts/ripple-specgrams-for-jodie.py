import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from scipy.io import wavfile
from scipy.signal import spectrogram


a0 = 1e-5  # reference amplitude
sr = 44100  # sample rate


def ripple_sound(dur, n, omega, w, delta, phi, f0, fm1, rand_gamma=True, l=60):
    """Synthesises a ripple sound.

    Args:
        dur (float): Duration of sound in s.
        n (int): Number of sinusoids.
        omega (:obj:`float` or `array`-like): Ripple density in Hz. Must be a single
            value or an array with length `duration * samplerate`.
        w (:obj:`float` or `array`-like): Ripple drift in Hz. Must be a single
            value or an array with length `duration * samplerate`.
        delta (:obj:`float` or `array`-like): Normalized ripple depth. Must be a single
            value or an array with length `duration * samplerate`. Value(s) must be in
            the range [0, 1].
        phi (float): Ripple starting phase in radians.
        f0 (float): Frequency of the lowest sinusoid in Hz.
        fm1 (float): Frequency of the highest sinusoid in Hz.
        rand_gamma (:obj:`bool`, optional): Randomize the normalized amplitudes of the
            sinusoids prior to scaling. Defaults to `False`.

    Returns:
        y (np.array): The waveform.
        a (np.array): The evnelope
    """
    # create the sinusoids
    m = int(dur * sr)  # total number of samples
    shapea = (1, m)
    shapeb = (n, 1)
    t = np.linspace(0, dur, int(m)).reshape(shapea)
    i = np.arange(n).reshape(shapeb)
    f = f0 * (fm1 / f0) ** (i / (n-1))
    sphi = 2 * np.pi * np.random.random(shapeb)
    s = np.sin(2 * np.pi * f * t + sphi)

    # create amplitude envelopes
    if hasattr(w, '__iter__'):
        assert len(w) == m, "w vector has incorrect length"
    else:
        w = np.tile(w, m)
    wprime = (np.cumsum(w) / sr).reshape(shapea)

    if hasattr(omega, '__iter__'):
        assert len(omega) == m, "w vector has incorrect length"
    else:
        omega = np.tile(omega, m)
    omega = omega.reshape(shapea)
    x = np.log2(f / f0)
    a = 1 + delta * np.sin(2 * np.pi * (wprime + omega * x) + phi)
    if rand_gamma:
        gamma = np.random.random(shapeb)
    else:
        gamma = 1
    y = (gamma * a * s / np.sqrt(f)).sum(axis=0)
    y /= np.abs(y).max()
    y *= a0 * 10 ** (l / 20)

    return y, a


def random_walk(points, dur):
    """Return a smooth random walk.

    Creates a smooth vector of length duration in which the values within
    points are visited. Points are spaced equally along the vector.

    Args:
        points (:obj:`array`-like): Points to visit.


    """
    f = interp1d(np.linspace(0, dur, len(points)), points, 'cubic')
    return f(np.linspace(0, dur, dur * sr))


def main():
    """Create and plot some ripple sounds.

    """
    from matplotlib import rcParams

    figsize = rcParams["figure.figsize"]
    rcParams["figure.figsize"] = [figsize[0], int(figsize[1] * 2)]
    rcParams["font.size"] = 14

    # default parameter values
    np.random.seed(0)
    dur = 1.5
    n = 1400
    ran_gamma = True
    f0 = 125.
    fm1 = 16000.
    phi = 0.
    args = (phi, f0, fm1, ran_gamma)

    # filenames of figures and wavfiles
    fn = "../../assets/images/jodie-%i-%i.png"

    for i in range(4):
        for j in range(4):
            print(i, j)
            _, ax = plt.subplots(1, 1, constrained_layout=True)
            omega = np.random.random(4) * 2.5
            if i < 2:
                omega = 0
            elif i < 3:
                omega = omega[0]
            else:
                omega = random_walk(omega, dur)
            w = np.random.choice([-1, 1], 4) * 2 ** (np.random.random(4) * 5 + 0.5)
            w = w[0] if i < 3 else random_walk(w, dur)
            delta = 0 if i == 0 else 0.9
            y, a = ripple_sound(dur, n, omega, w, delta, *args)
            f, t, Sxx = spectrogram(y, sr, "hamming", 4096)
            ax.pcolormesh(t, f, Sxx)
            ax.set_ylim(f0, 1600)
            # ax.set_xlim(0, dur)
            ax.set_yscale('log', basey=2)
            plt.savefig(fn % (i, j))
            wavfile.write((fn % (i, j)).replace("png", "wav"), sr, y)


if __name__ == '__main__':
    main()
