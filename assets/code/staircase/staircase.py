class WUDM(object):

    def __init__(self, init_val, xp, reversals, ustep, geometric=False):
        """Helper class for the weighted up-down method.

        Uses the procedure described by Kaernbach (1991) to estimate a point on
        the psychometric function. This is a 'model-free' staircase method
        which is simpler, more flexible, and slightly more efficient than the
        more famous transformed up-down method described by Levitt (1971; see
        also Rammsayer, 1992).

        Args:
            init_val (float): Initial value of the staircase. 
            xp (float): Point on the psychometric function to track. 
            reversals (:obj:`int` or :obj:`list` of :obj:`int`): Number of
                reversals in each phase of the staircase. Can be a single
                integer or a list of integers if there is more than one phase.
                If a list, needs to be the same length as `upstep`.
            ustep (:obj:`float` or :obj:`list` of :obj:`float`): Size of the
                up step in each phase. The size of the downstep depends on xp.
            geometric (:obj:`bool`, optional): If `True`, the staircase
                progresses geometrically. Defaults to `False`.
        
        References:
            Levitt, H. The Journal of the Acoustical Society of America (1971)
            49: 467. http://dx.doi.org/10.1121/1.1912375
            
            Kaernbach, C. Perception & Psychophysics (1991) 49: 227. 
            https://doi.org/10.3758/BF03214307
            
            Rammsayer, T. H. Bulletin of the Psychonomic Society (1992) 30:
            425. https://doi.org/10.3758/BF03334107
            
        """
        self.done = False
        self.phase = 0
        self.val = init_val
        self.xp = xp
        self.factor = self.xp / (1 - self.xp)

        if hasattr(reversals, '__iter__'):

            self.reversals = reversals

        else:

            self.reversals = [reversals]

        if hasattr(ustep, '__iter__'):

            self.ustep = ustep

        else:

            self.ustep = [ustep]

        assert len(self.reversals) == len(
            self.ustep), 'Lists of reversals and step sizes are not the ' \
                         'same length.'

        self.geometric = geometric
        self.outcomes = [[] for i in self.reversals]
        self.vals = [[] for i in self.reversals]

        @property
        def dstep():
            """Calculate the down step; depends on `ustep` and `xp`."""
            if self.geometric is True:

                return self.ustep ** (1 / self.factor)

            else:

                return self.ustep * (1 / self.factor)

        self.dstep = dstep

        @property
        def revs():
            """Mark the reversals in the current phase."""
            from itertools import tee

            _outcomes = self.outcomes[self.phase]
            _a, _b = tee(_outcomes)
            _b.__next__()

            return [a != b for a, b in zip(_a, _b)]

        self.revs = revs

        @property
        def countr():
            """Count the number of reversals in the current phase."""
            return sum(self.revs)

        self.countr = countr

    def trial(self, previous_trial_correct):
        """Progress the staircase by one trial, updating all the internal
        attributes accordingly.

        Args:
            previous_trial_correct (bool): Was the previous trial correct?

        """
        self.outcomes[self.phase].append(previous_trial_correct)
        self.vals[self.phase].append(self.val)

        if self.countr == self.reversals[self.phase]:

            if self.phase == len(self.reversals):

                self.done = True

            else:

                self.phase += 1

        if self.geometric is True:

            if previous_trial_correct is True:

                self.val *= self.ustep

            else:

                self.val /= self.dstep

        else:

            if previous_trial_correct is True:

                self.val += self.ustep

            else:

                self.val -= self.dstep



#                  dv0=1, p=0.75, reversals=[2, 4], stepsizes=(2.25, 1.5),
#                  initialerrfix=True, geometric=True, avgrevsonly=True,
#                  cap=False):
#         """
#         Helper class for tracking an adaptive staircase using the weighted
#         transformed up/down method proposed by Kaernbach (1991). Keywords are
#         used to set parameters at initialisation, but they can be changed at
#         any point during the run if necessary.
#
#         The main part is the method 'trial' which advances the staircase.
#         Once the staircase is over, all of the data can be accessed, and
#         summarised graphically using the function 'makefig' (requires
#         matplotlib).
#
#         """
#         s = self
#         s.dv = dv0
#         s.dvs = []
#         s.dvs4avg = []
#         s.p = p
#         s.factor = self.p / (1 - self.p)
#         s.reversals = reversals
#         s.stepsizes = stepsizes
#         s.initialerrfix = initialerrfix
#         s.geometric = geometric
#         s.avgrevsonly = avgrevsonly
#         s.revn = 0
#         s.phase = 0
#         s.staircaseover = False
#         s.firsttrial = True
#         s.prevcorr = None
#         s.trialn = 0
#         s.cap = cap
#
#     def trial(self, corr):
#         """
#         Advance the staircase by one trial. Takes a Boolean which indicates
#         whether the listener got the trial correct or incorrect.
#
#         """
#         # do nothing if the staircase is already over
#         s = self
#         if not s.staircaseover:
#             s.trialn += 1
#             s.dvs.append(self.dv)
#             # record dv if needed
#             if not s.firsttrial:
#                 if corr != s.prevcorr:
#                     reversal = True
#                     s.revn += 1
#                 else:
#                     reversal = False
#             if s.phase == 1:
#                 if s.avgrevsonly:
#                     if reversal:
#                         s.dvs4avg.append(s.dv)
#                 else:
#                     s.dvs4avg.append(s.dv)
#             # initial error fix: if the dv goes above the initial value during
#             # the first phase, add more reversals ...
#             if s.initialerrfix:
#                 if not corr:
#                     if s.trialn <= s.factor + 1:
#                         s.reversals[0] += 2
#                         s.initialerrfix = False
#             # change the dv
#             if s.geometric:
#                 if corr:
#                     s.dv /= (s.stepsizes[s.phase] ** (1 / float(s.factor)))
#                 else:
#                     s.dv *= s.stepsizes[s.phase]
#             else:
#                 if corr:
#                     s.dv -= (s.stepsizes[s.phase] / float(s.factor))
#                 else:
#                     s.dv += s.stepsizes[s.phase]
#             # cap dv
#             if s.cap:
#                 if s.dv > s.cap: s.dv = s.cap
#             # update the object
#             if s.revn >= s.reversals[0]:
#                 s.phase = 1
#             if s.revn >= np.sum(s.reversals):
#                 s.staircaseover = True
#             s.firsttrial = False
#             s.prevcorr = corr
#
#     def getthreshold(self):
#         """
#         Once the staircase is over, get the average (geometric by default) of
#         the dvs to calculate the threshold.
#
#         """
#         s = self
#         if s.staircaseover:
#             if s.geometric:
#                 return np.exp(np.mean(np.log(s.dvs4avg)))
#             else:
#                 return np.mean(s.dvs4avg)
#
#     def makefig(self, f=None):
#         """
#         View or save the staircase.
#
#         """
#         s = self
#         x = np.arange(s.trialn) + 1
#         y = s.dvs
#         if s.geometric:
#             plt.semilogy(x, y)
#         else:
#             plt.plot(x, y)
#         plt.xlim(min(x), max(x))
#         plt.ylim(min(y), max(y))
#         plt.ylabel('Dependent variable')
#         plt.xlabel('Trial')
#         if s.staircaseover:
#             plt.hlines(s.getthreshold(), min(x), max(x), 'r')
#         if f:
#             s.savefig(f)
#         else:
#             plt.show()
#
#
# def main():
#     trials = np.random.randint(0, 2, 50)
#     kaernbach1991 = Kaernbach1991()
#     for trial in trials:
#         kaernbach1991.trial(trial)
#         if kaernbach1991.staircaseover:
#             break
#     print
#     kaernbach1991.getthreshold()
#     kaernbach1991.makefig()


# if __name__ == '__main__':
#     main()

WUDM()
