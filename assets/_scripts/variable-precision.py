# approximate sum of two von mises with a single von mises
import numpy as np
from scipy.stats import vonmises

def sim(a, b, plot=False, n=int(1e8)):
    unwrapped = vonmises.rvs(a, size=n) + vonmises.rvs(b, size=n)
    unwrapped = unwrapped
    wrapped = (unwrapped + np.pi) % (2 * np.pi) - np.pi
    kappa, _, _ = vonmises.fit(wrapped, floc=0, fscale=1)
    if plot is True:
        plt.hist(wrapped, normed=True, bins=100)
        x = np.linspace(-np.pi, np.pi)
        y = vonmises.pdf(x, kappa)
        plt.plot(x, y)
    return kappa



# import numpy as np
# import pymc3 as pm
# import matplotlib.pyplot as plt
# import theano.tensor as tt
# from scipy.stats import norm, vonmises
# from scipy.integrate import quad
#
#
# n = 10000
# mu = 3
# sigma = 3
#
# k = np.exp(norm.rvs(mu, sigma, size=n))
# x = vonmises.rvs(kappa=k, size=n)
#
# with pm.Model():
#
#     mu = pm.Normal(name="mu", mu=0, sigma=10)
#     sigma = pm.HalfCauchy(name="sigma", beta=1)
#     delta = pm.Normal(name="delta", mu=0, sigma=1, shape=n)
#     kappa = tt.exp(mu + delta * sigma)  # IMPORTANT! Use non-centered parameterization
#     pm.VonMises(name="obs", mu=0, kappa=kappa, observed=x)
#     trace = pm.sample(10000, tune=5000, chains=2)
#     pm.traceplot(trace, compact=True, var_names=["mu", "sigma"])
#     plt.savefig("tmp.png")
#
# # hist(x, bins=100, normed=True)
# #
# # x = np.linspace(-np.pi, np.pi, 100)
# #
# # def pdf(x, mu, sigma, a):
# #     g = 1
# #     v = vonmises.pdf(x, kappa=mu)
# #     def f(k, x):
# #         g = gamma.pdf(k, mu**2 / sigma**2, scale=1. / (mu / sigma**2))
# #         v = vonmises.pdf(x, kappa=k)
# #         return g * v
# #     return [quad(f, 0, a, _x)[0] for _x in x]
# #
# # def logpdf(x, mu, sigma, a):
# #     g = 1
# #     v = vonmises.pdf(x, kappa=mu)
# #     def f(k, x):
# #         g = gamma.logpdf(k, mu**2 / sigma**2, scale=1. / (mu / sigma**2))
# #         v = vonmises.logpdf(x, kappa=k)
# #         return g * v
# #     return [quad(f, 0, a, _x)[0] for _x in x]
# #
# # [plot(x, pdf(x, mu, sigma, a)) for a in [500]]
# #
# #
# # plot(x, np.log(pdf(x, mu, sigma)))
#
#
#
#
#
#
# # from scipy.integrate import quad
# # import theano
# # import theano.tensor as tt
# # import numpy as np
# # import pymc3 as pm
# #
# #
# # class Integrate(theano.Op):
# #     def __init__(self, expr, var, *extra_vars):
# #         super().__init__()
# #         self._expr = expr
# #         self._var = var
# #         self._extra_vars = extra_vars
# #         self._func = theano.function(
# #             [var] + list(extra_vars),
# #             self._expr,
# #             on_unused_input='ignore')
# #
# #     def make_node(self, start, stop, *extra_vars):
# #         self._extra_vars_node = extra_vars
# #         assert len(self._extra_vars) == len(extra_vars)
# #         self._start = start
# #         self._stop = stop
# #         vars = [start, stop] + list(extra_vars)
# #         # vars = list(extra_vars)
# #         return theano.Apply(self, vars, [tt.dscalar().type()])
# #
# #     def perform(self, node, inputs, out):
# #         start, stop, *args = inputs
# #         val = quad(self._func, start, stop, args=tuple(args))[0]
# #         out[0][0] = np.array(val)
# #
# #     def grad(self, inputs, grads):
# #         start, stop, *args = inputs
# #         out, = grads
# #         replace = dict(zip(self._extra_vars, args))
# #
# #         replace_ = replace.copy()
# #         replace_[self._var] = start
# #         dstart = out * theano.clone(-self._expr, replace=replace_)
# #
# #         replace_ = replace.copy()
# #         replace_[self._var] = stop
# #         dstop = out * theano.clone(self._expr, replace=replace_)
# #
# #         grads = tt.grad(self._expr, self._extra_vars)
# #         dargs = []
# #         for grad in grads:
# #             integrate = Integrate(grad, self._var, *self._extra_vars)
# #             darg = out * integrate(start, stop, *args)
# #             dargs.append(darg)
# #
# #         return [dstart, dstop] + dargs
# #
# #
# # y_obs = 8.3
# #
# # start = theano.shared(1.)
# # stop = theano.shared(2.)
# # with pm.Model() as basic_model:
# #     a = pm.Uniform('a', 1.5, 3.5)
# #     b = pm.Uniform('b', 4., 6.)
# #
# #     # Define the function to integrate in plain theano
# #     t = tt.dscalar('t')
# #     t.tag.test_value = np.zeros(())
# #     a_ = tt.dscalar('a_')
# #     a_.tag.test_value = np.ones(())*2.
# #     b_ = tt.dscalar('b_')
# #     b_.tag.test_value = np.ones(())*5.
# #     func = t**a_ + b_
# #     integrate = Integrate(func, t, a_, b_)
# #
# #     # Now we plug in the values from the model.
# #     # The `a_` and `b_` from above corresponds to the `a` and `b` here.
# #     mu = integrate(start, stop, a, b)
# #     y = pm.Normal('y', mu=mu, sd=0.4, observed=y_obs)
# #     trace = pm.sample(1500, tune=500, cores=2, chains=2)