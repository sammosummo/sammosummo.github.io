import pymc3 as pm
import theano.tensor as tt


def main():
    with pm.Model() as m1:

        a = pm.Normal(name="a", shape=5)
        b = pm.Normal(name="b", shape=5)
        c = tt.max([a, b], axis=0)

    pm.sample(model=m1)  # works fine

    with pm.Model() as m2:

        a = pm.Normal(name="a", shape=5)
        b = pm.Normal(name="b", shape=5)
        c = tt.min([a, b], axis=0)

    pm.sample(model=m2)  # raises this exception:
    # ... error: non-constant-expression cannot be narrowed from type 'npy_intp' (aka
    # 'long') to 'int' in initializer list [-Wc++11-narrowing]


if __name__ == "__main__":
    main()
