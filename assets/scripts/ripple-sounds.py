"""Synthesize, plot, and play ripple sounds.

"""
from random import getrandbits

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import seaborn as sb

from scipy.interpolate import interp1d
from scipy.io import wavfile

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
    f = f0 * (fm1 / f0) ** (i / (n - 1))
    sphi = 2 * np.pi * np.random.random(shapeb)
    s = np.sin(2 * np.pi * f * t + sphi)

    # create amplitude envelopes
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
    f = interp1d(np.linspace(0, dur, len(points)), points, "cubic")
    return f(np.linspace(0, dur, dur * sr))


def plot_env(a, ax, labels=False):
    """Plots an envelope onto an axis.

    Args:
        a (np.array): An array with shape (m, n) where m is the total number of samples
            and n in the number of sinusoids and values representing instantaneous
            amplitudes.
        ax (matplotlib.axes._subplots.AxesSubplot): Axis.
        labels (:obj:`bool`, optional): Include labels or not.

    """
    ax.pcolormesh(a, rasterized=True, vmin=0, vmax=2)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    if labels is True:
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency\n($log_2$ scale)")


def main():
    """Create and plot some ripple sounds.

    """
    from matplotlib import rcParams

    figsize = rcParams["figure.figsize"]
    rcParams["figure.figsize"] = [figsize[0], int(figsize[1] / 2)]
    rcParams["font.size"] = 14

    # default parameter values
    np.random.seed(0)
    dur = 1.5
    n = 1400
    omega = 1
    w = 8
    delta = 0.9
    ran_gamma = True
    f0 = 125.0
    fm1 = 16000.0
    phi = 0.0
    args = (phi, f0, fm1, ran_gamma)

    # filenames of figures and wavfiles
    fn = "../../assets/images/%s-ripples.svg"
    wn = "../../assets/sounds/%s-%i.wav"

    # static ripple sounds
    print("making static ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    for i, ax in enumerate(axes):
        _omega = 1.5 if i == 1 else omega
        _delta = 0.5 if i == 2 else delta
        y, a = ripple_sound(dur, n, _omega, 0, _delta, *args)
        print("    playing a sound")
        sd.play(y, sr)
        print("    saving the waveform")
        wavfile.write(wn % ("static", i), sr, y)
        print("    plotting")
        plot_env(a, ax, ax == axes[0])

    print("making a figure")
    plt.savefig(fn % "static", bbox_inches=0, transparent=True)

    # moving ripple sounds
    print("making moving ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    for i, ax in enumerate(axes):
        y, a = ripple_sound(dur, n, omega, [4, 8, -4][i], delta, *args)
        print("playing a sound")
        sd.play(y, sr)
        plot_env(a, ax, ax == axes[0])
        print("    playing a sound")
        sd.play(y, sr)
        print("    saving the waveform")
        wavfile.write(wn % ("moving", i), sr, y)
        print("    plotting")
        plot_env(a, ax, ax == axes[0])
    print("making a figure")
    plt.savefig(fn % "moving", bbox_inches=0, transparent=True)

    # dynamic moving ripple sounds
    print("making dynamic static ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    for i, ax in enumerate(axes):
        _omega = random_walk(np.random.random(4) * 2.5, dur) if i != 1 else omega
        _w = np.random.choice([-1, 1], 4) * 2 ** (np.random.random(4) * 5 + 0.5)
        _w = random_walk(_w, dur) if i != 0 else w
        y, a = ripple_sound(dur, n, _omega, _w, delta, *args)
        print("    playing a sound")
        sd.play(y, sr)
        print("    saving the waveform")
        wavfile.write(wn % ("dynamic", i), y, sr)
        print("    plotting")
        plot_env(a, ax, ax == axes[0])
    print("making a figure")
    plt.savefig(fn % "dynamic", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
