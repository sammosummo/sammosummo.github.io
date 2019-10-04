"""Format a number for inclusion in LaTeX.

"""
from scipy.stats import cauchy


def format_for_latex(x, p=3):
    """Convert a float to a LaTeX-formatted string displaying the value to p significant
    digits and in standard form.

    Args:
        x (float): Value.
        p (:obj:`int`, optional): Number of significant digits. Default is 3.

    Return:
        s (str): Formatted value.
    """

    def _f(x, p):
        s = "{:g}".format(float("{:.{p}g}".format(x, p=3)))
        n = p - len(s.replace(".", "").replace("-", "").lstrip("0"))
        s += "0" * n
        return s

    if abs(x) < 10 ** -p or abs(x) > 10 ** (p + 1):
        a, b = str("%e" % x).split("e")
        return "$%s$" % r"%s \times 10^{%i}" % (_f(float(a), p), int(b))

    return "$%s$" % _f(x, p)


def test():
    X = cauchy.rvs(size=100000)
    for x in X:
        print(x, format_for_latex(x))


if __name__ == "__main__":
    test()
