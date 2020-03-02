import pymc3 as pm
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # with pm.Model():
    #
    #     a = pm.Normal(name="a")
    #     trace = pm.sample(10000, tune=2000, chains=2)
    #     pm.traceplot(trace, compact=True)
    #     plt.savefig("test_00.png")
    #     pm.autocorrplot(trace, "a")
    #     plt.savefig("test_01.png")

    # with pm.Model():
    #
    #     a = pm.Normal(name="a")
    #     M = pm.LKJCorr(name="C", n=4, eta=1)
    #     trace = pm.sample(10000, tune=2000, chains=2)
    #     pm.traceplot(trace, compact=True)
    #     plt.savefig("test_10.png")
    #     pm.autocorrplot(trace, "a")
    #     plt.savefig("test_11.png")

    with pm.Model():

        a = pm.Normal(name="a", shape=(1, 2))
        pm.sample()
        # f = pm.HalfNormal.dist()
        # M = pm.LKJCholeskyCov(name="M", n=4, eta=1, sd_dist=f)
        # trace = pm.sample(10000, tune=2000, chains=2)
        # pm.traceplot(trace, compact=True)
        # plt.savefig("test_20.png")
        # pm.autocorrplot(trace, "a")
        # plt.savefig("test_21.png")
