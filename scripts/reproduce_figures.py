"""Library figures. These are not handbook figures.

Outputs go to figures/generated and are labeled in the file name and in the
validation report as unverified against the book.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from metaopt.benchmarks import Ackley1Function, benchmark_domain
from metaopt.plotting import plot_convergence, plot_xy
from metaopt.pso import minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "generated"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    def sphere(x):
        return float(np.sum(np.square(x)))

    result = minimize(sphere, [[-5.0, 5.0]] * 2, seed=1, population_size=20, iterations=25)
    figure = plot_convergence(
        {"PSO seed 1, not a book figure": result.history},
        ylabel="best sphere value",
        title="Library convergence curve (unverified against the handbook)",
        log_scale=True,
        path=OUT / "pso_sphere_convergence_unverified.png",
    )
    plt.close(figure)

    domain = np.asarray(benchmark_domain(0, 2), dtype=float)
    grid = np.linspace(domain[0, 0], domain[0, 1], 80)
    xx, yy = np.meshgrid(grid, grid)
    zz = np.empty_like(xx)
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            zz[i, j] = Ackley1Function([xx[i, j], yy[i, j]])
    figure, axis = plt.subplots(figsize=(6, 4.5))
    image = axis.contour(xx, yy, zz, levels=12, colors="black", linewidths=0.6)
    axis.clabel(image, inline=True, fontsize=8, fmt="%.0f")
    axis.set_xlabel("x1")
    axis.set_ylabel("x2")
    axis.set_title("Ackley No. 1 contour (library drawing, not Appendix A)")
    figure.tight_layout()
    figure.savefig(OUT / "ackley1_contour_unverified.png", dpi=150)
    plt.close(figure)

    figure = plot_xy(
        {"zero section": (grid, zz[zz.shape[0] // 2])},
        xlabel="x1",
        ylabel="Ackley No. 1",
        title="Ackley No. 1 section at x2 = 0 (not a book figure)",
        path=OUT / "ackley1_section_unverified.png",
    )
    plt.close(figure)
    print(f"wrote figures under {OUT}")


if __name__ == "__main__":
    main()
