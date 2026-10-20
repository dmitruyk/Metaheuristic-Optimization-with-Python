"""Manuscript PSO, DE, and GWO variants.

Names follow the handbook. ``GWOEPD`` is the Appendix B function ``EPDGWO``.
"""

from metaopt.variants.bb_pso import minimize as bb_pso_minimize
from metaopt.variants.gwoepd import minimize as gwoepd_minimize
from metaopt.variants.ia_pso import minimize as ia_pso_minimize
from metaopt.variants.ldw_pso import minimize as ldw_pso_minimize
from metaopt.variants.med_pso import minimize as med_pso_minimize
from metaopt.variants.mgwo import minimize as mgwo_minimize
from metaopt.variants.ring_pso import minimize as ring_pso_minimize
from metaopt.variants.sade import minimize as sade_minimize
from metaopt.variants.vct_pso import minimize as vct_pso_minimize
from metaopt.variants.von_neumann_pso import minimize as von_neumann_pso_minimize

__all__ = [
    "bb_pso_minimize",
    "gwoepd_minimize",
    "ia_pso_minimize",
    "ldw_pso_minimize",
    "med_pso_minimize",
    "mgwo_minimize",
    "ring_pso_minimize",
    "sade_minimize",
    "vct_pso_minimize",
    "von_neumann_pso_minimize",
]
