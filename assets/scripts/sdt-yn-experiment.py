"""Script to perform a simple at-home yes/no experiment and analyze the resulting data
using signal detection theory.

"""
import numpy as np
from scipy.stats import norm
import prettytable as pt
import sounddevice as sd


def trial(signal, n=None):
    """Performs a trial in the experiment.

    Args:
        signal (bool): Should the trial contain a tone?
        n (:obj:`bool`, optional): Trial number. If omitted, a "practice" trial is
            performed which will allow the observer an opportunity to change the volume
            settings on their computer.

    Returns:
        rsp (bool): On practice trials, this indicates whether the real experiment
            should begin. On real trials, it indicates whether the observer responded
            "yes".

    """
    t = np.arange(0, 0.1, 1 / 44100)
    tone = 1e-5 * 10 ** (50 / 20) * np.sin(2 * np.pi * 1000 * t + 0)
    noise = np.random.normal(size=len(t)) * tone.std() / np.sqrt(2)
    sd.play(noise + tone if signal and isinstance(n, int) else noise, 44100)
    responses = {"n": False, "y": True}
    if isinstance(n, int):
        instr = f"Trial {n}: Did you hear a tone? ([y] or [n])?"
    else:
        instr = "Adjust your volume settings until the noise barely audible."
        instr += "\n([y] to adjust and hear again; [n] to continue)"
    while 1:
        try:
            return responses[input(instr).lower()]
        except KeyError:
            pass


def experiment():
    """Performs a series of trials.

    """
    adj = True
    while adj:
        adj = trial(False)
    X = [False, True] * 20
    np.random.shuffle(X)
    Y = [trial(*p[::-1]) for p in enumerate(X)]
    c = sum([1 for x, y in zip(X, Y) if x == 0 and y == 0])
    f = sum([1 for x, y in zip(X, Y) if x == 0 and y == 1])
    m = sum([1 for x, y in zip(X, Y) if x == 1 and y == 0])
    h = sum([1 for x, y in zip(X, Y) if x == 1 and y == 1])
    return c, f, m, h


def sdt_yn(c, f, m, h):
    """Calcualte SDT statistics.

    """
    n = f + c
    s = m + h
    sens = norm.ppf(h / s) - norm.ppf(f / n)
    crit = 0.5 * (norm.ppf(h / s) + norm.ppf(f / n))
    return sens, crit


if __name__ == "__main__":

    print(
        """
████████╗██╗  ██╗███████╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
╚══██╔══╝██║  ██║██╔════╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
   ██║   ███████║█████╗      ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██║  ██║
   ██║   ██╔══██║██╔══╝      ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██║  ██║
   ██║   ██║  ██║███████╗    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ 
                                                                                     
██████╗  █████╗ ███████╗███████╗ ██████╗  ██████╗ ███╗   ██╗    ██╗██╗██╗██╗██╗██╗██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔═══██╗████╗  ██║    ██║██║██║██║██║██║██║
██████╔╝███████║███████╗███████╗██║   ██║██║   ██║██╔██╗ ██║    ██║██║██║██║██║██║██║
██╔══██╗██╔══██║╚════██║╚════██║██║   ██║██║   ██║██║╚██╗██║    ╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝
██████╔╝██║  ██║███████║███████║╚██████╔╝╚██████╔╝██║ ╚████║    ██╗██╗██╗██╗██╗██╗██╗
╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝╚═╝                                                                              

Welcome! This script performs a simple experiment and analyzes the data using signal
detection theory (SDT)."""
    )
    c, f, m, h = experiment()
    print("Experiment done!")
    table = pt.PrettyTable()
    table.field_names = ["", "x = 0", "x = 1"]
    table.add_row(["y = 0", c, m])
    table.add_row(["y = 1", f, h])
    print("Here is your contingency table:")
    print(table)
    if any(x == 0 for x in (c, f, m, h)):
        print(
            """\
Unfortunately, one or more of the cells has a value of 0. SDT statistics can't be
calculated without applying some form of correction. Exiting now"""
        )
        exit()
    print("Calculating SDT statistics ...")
    sens, crit = sdt_yn(c, f, m, h)
    print("sensitivity (d') = %.2f" % sens)
    print("criterion (c) = %.2f" % crit)
