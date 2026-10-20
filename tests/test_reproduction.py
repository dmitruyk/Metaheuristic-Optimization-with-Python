"""Quick validation profile and published-scalar comparison."""

from __future__ import annotations

import numpy as np
from scripts.compare_published_values import build_report

from metaopt.experiments import rank_by_median
from metaopt.reproduction import QUICK_PROFILE, estimate_full_cost, run_quick


def test_quick_profile_is_deterministic_and_not_an_appendix():
    first = run_quick()
    second = run_quick()
    assert first["protocol"]["matches_appendix_c"] is False
    assert first["protocol"]["matches_appendix_e"] is False
    assert first["protocol"]["label"] == "quick-validation"
    assert [row["fun"] for row in first["rows"]] == [row["fun"] for row in second["rows"]]
    assert {row["nfev"] for row in first["rows"]} == {QUICK_PROFILE["max_evaluations"]}
    assert len(first["rows"]) == 3 * 2 * 2
    assert first["ranks"]


def test_full_job_schedule_uses_the_manuscript_seed_formula():
    from metaopt.reproduction import iter_full_jobs

    first = next(iter_full_jobs())
    assert first["seed"] == 12345
    assert first["matches_appendix_c"] is False
    assert first["dimension"] == 30
    assert sum(1 for _ in iter_full_jobs()) == 14 * 54 * 100


def test_full_protocol_estimate_is_not_executed():
    estimate = estimate_full_cost()
    assert estimate["objective_evaluations_nominal"] == 14 * 54 * 100 * 25 * 500
    assert estimate["matches_appendix_c"] is False
    assert estimate["matches_appendix_e"] is False
    assert estimate["hour_range"][0] > 1
    assert estimate["hour_range"][1] > estimate["hour_range"][0]


def test_published_comparison_matches_worked_scalars_and_leaves_appendices_unmatched():
    report = build_report()
    assert report["matches_appendix_c"] is False
    assert report["matches_appendix_e"] is False
    itae = [row for row in report["rows"] if row["area"] == "Problem 1a ITAE"]
    assert len(itae) == 2
    assert all(row["status"] == "matched" for row in itae)
    settling = next(row for row in report["rows"] if row["area"].startswith("Problem 1a settling"))
    assert settling["status"] == "unmatched"
    appendices = [row for row in report["rows"] if row["area"] in {"Appendix C", "Appendix E"}]
    assert len(appendices) == 2
    assert all(row["status"] == "unmatched" for row in appendices)
    matched = [row for row in report["rows"] if row["status"] == "matched"]
    assert matched
    assert all(np.isfinite(row["observed"]) for row in matched)


def test_median_ranks_share_ties():
    summary = [
        {"algorithm": "PSO", "benchmark": "Spherical", "median": 2.0},
        {"algorithm": "DE/rand", "benchmark": "Spherical", "median": 2.0},
        {"algorithm": "GWO", "benchmark": "Spherical", "median": 5.0},
    ]
    ranks = {row["algorithm"]: row["median_rank"] for row in rank_by_median(summary)}
    assert ranks == {"PSO": 1, "DE/rand": 1, "GWO": 3}
