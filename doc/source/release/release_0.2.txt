scikit-tracker v0.2
-------------------

We are glad to announce the first release of **scikit-tracker**.

There is still many feature to add and documentation is very poor but you can do already a lot of
things with **scikit-tracker v0.2**.

- detect cell nucleus with :func:`sktracker.detection.nuclei_detector`
- detect fluorescent peaks with :func:`sktracker.detection.peak_detector`

Both algorithms are parallelized.

- import detected peaks from Trackmate XML with :func:`sktracker.io.trackmate.trackmate_peak_import`
- track objects with brownian motion with :class:`sktracker.tracker.solver.ByFrameSolver`
- fill gaps in tracked trajectories with :class:`sktracker.tracker.solver.GapCloseSolver`

We hope to provide you some code examples in the documentation soon.

**scikit-tracker** has released a v0.2.1 due to a bug preventing users to install from pip.
