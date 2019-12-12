"""Synthesize, plot, and play ripple sounds.

"""
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from scipy.io import wavfile


a0 = 1e-5  # reference amplitude
sr = 44100  # sample rate


def ripple_sound(dur, n, omega, w, delta, phi, f0, fm1, l=70):
    """Synthesizes a ripple sound.

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
        l (:obj:`float`, optional): Level in dB of the sound, assuming a pure tone with
            peak amplitude `a0` is 0 dB SPL. TODO: Implement this correctly!

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
    x = np.log2(f / f0)
    if hasattr(w, "__iter__"):
        wprime = np.cumsum(w) / sr
    else:
        wprime = w * t
    a = 1 + delta * np.sin(2 * np.pi * (wprime + omega * x) + phi)

    # create the waveform
    y = (a * s / np.sqrt(f)).sum(axis=0)

    # scale to a given SPL
    # TODO: This is likely wrong; I haven't checked it
    y /= np.abs(y).max()
    y *= a0 * 10 ** (l / 20)

    return y, a


def smooth_walk(points, dur):
    """Return a smooth walk.

    Args:
        points (:obj:`array`-like): Points to visit. These are spaced evenly and a
            spline is used to interpolate them.
        dur (float): Duration of sound in s.

    Returns:
        y (numpy.array): Values of the random walk.

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
    dur = 1
    n = 1000  # reduce this if you want to make figures; otherwise it takes forever!
    omega = 1
    w = 8
    delta = 0.9
    f0 = 250
    fm1 = 8000
    phi = 0.0
    args = (phi, f0, fm1)

    # filenames of figures
    fn = "../../assets/images/%s-ripples.svg"

    # static ripple sounds
    print("making static ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    for i, ax in enumerate(axes):
        _omega = 1.5 if i == 1 else omega
        _w = 0
        _delta = 0.5 if i == 2 else delta
        print(f"sound with omega={_omega:.2f}, w={_w:.2f}, and delta={_delta:.2f}")
        y, a = ripple_sound(dur, n, _omega, _w, _delta, *args)
        print("playing sound")
        sd.play(y, sr, blocking=True)
        print("plotting")
        plot_env(a, ax, ax == axes[0])
    print("saving a figure")
    plt.savefig(fn % "static", bbox_inches=0, transparent=True)

    # moving ripple sounds
    print("making moving ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    _ws = [4, 8, -4]
    for i, ax in enumerate(axes):
        _omega = omega
        _w = _ws[i]
        _delta = delta
        print(f"sound with omega={_omega:.2f}, w={_w:.2f}, and delta={_delta:.2f}")
        y, a = ripple_sound(dur, n, _omega, _w, _delta, *args)
        print("playing sound")
        sd.play(y, sr, blocking=True)
        print("plotting")
        plot_env(a, ax, ax == axes[0])
    print("making a figure")
    plt.savefig(fn % "moving", bbox_inches=0, transparent=True)

    # dynamic moving ripple sounds
    print("making dynamic static ripple sounds")
    _, axes = plt.subplots(1, 3, constrained_layout=True, sharex="all", sharey="all")
    for i, ax in enumerate(axes):
        _delta = smooth_walk(np.random.random(10), dur) if i == 0 else delta
        _omega = smooth_walk([1] * 5 + [1.5] * 5, dur) if i == 1 else omega
        _w = smooth_walk([-8, 0, 4, 8], dur) if i == 2 else w
        print(f"{[_delta, _omega, _w][i].shape}")
        y, a = ripple_sound(dur, n, _omega, _w, _delta, *args)
        print("playing sound")
        sd.play(y, sr, blocking=True)
        print("plotting")
        plot_env(a, ax, ax == axes[0])
    print("making a figure")
    plt.savefig(fn % "dynamic", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
