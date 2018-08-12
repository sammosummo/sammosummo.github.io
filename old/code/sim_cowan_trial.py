from numpy.random import uniform


def trial(M, different, z, k, b):

    if uniform() > z:

        if uniform() < b:

            return True

        else:

            return False

    else:

        if uniform() < k / float(M):

            return different

        else:

            if uniform() < b:

                return True

            else:

                return False


trial(2, True, 0.9, 4, 0.5)  # example simulated trial