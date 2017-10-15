from util import *
from wmm import *

with pm.Model():
    data = util.get_rouder_data()
    formulae = [
        'kappa ~ C(subject) + C(colour)',
        'gamma ~ C(subject) + C(prob_different)',
        'zeta ~ C(subject)'
    ]
    wmcap_morey_cowan(data, formulae)
    backend = pm.backends.Text('wmcap_morey_cowan')
    trace = pm.sample(draws=10000, tune=2000, trace=backend)
    pm.traceplot(trace)
    plt.savefig('traceplot.png')