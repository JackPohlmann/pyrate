# Integration module

This module serves to centralize custom integration functions.
The motivation for this is that the integration is the greatest bottleneck in radiometric calculations.
Therefore, the main integration function in this module seeks to take advantage of multiprocessing in order to speed up computation.

NOTE: This was a valiant attempt, but threading doesn't work like this in Python (Google Python GIL).
I used a much more Pythonic way to speed up the integration: memoizing the SAIGs (from the core module).
SciPy's integration calls the same values for each call of integration, so memoizing the SAIG's interpolation outputs causes the repeated calls to the interpolator's get method to not have to reevaluate.
Pretty simple workaround once executed but hard to see!
