"""Companion library for *Metaheuristic Optimization with Python*.

Authors of the handbook: Yuriy Romasevych and Viatcheslav Loveikin.
This package implements the published algorithms. It does not replace them
with third-party solvers. ``metaopt.de.scipy_minimize`` is an explicitly
separate SciPy baseline.
"""

from metaopt.api import Bounds, OptimizationResult, Problem

__version__ = "0.1.0"

__all__ = ["Bounds", "OptimizationResult", "Problem", "__version__"]
