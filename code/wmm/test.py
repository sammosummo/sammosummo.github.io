from util import *
from wmm import *

with pm.Model():
    data = util.get_rouder_data()
    formulae = [
        'kappa ~ C(colour, Sum)',
        'gamma ~ C(prob_different, Treatment(0.5))',
        'zeta ~ 1'
    ]
    wmcap_morey_cowan(data, formulae)
    backend = pm.backends.Text('rouder_example')
    trace = pm.sample(draws=1000, tune=2000, trace=backend)
    pm.traceplot(trace)
    plt.savefig('rouder_example/traceplot.png')
