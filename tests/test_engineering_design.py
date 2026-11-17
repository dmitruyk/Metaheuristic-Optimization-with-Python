import pytest

from metaopt.applications.engineering_design import beam_components, gripper_components


@pytest.mark.parametrize(
    ("point", "expected", "feasible"),
    [
        ([20, 50, 3, 3], 865522268.4252858, False),
        ([50, 80, 1.7, 5], 31900000000.00664, False),
        ([40, 70, 1.5, 2.5], 0.019066155587773827, True),
    ],
)
def test_beam_geometry_and_stress_cap(point, expected, feasible):
    result = beam_components(point)
    assert result["fun"] == pytest.approx(expected, rel=1e-12)
    assert bool(result["feasible"]) == feasible


@pytest.mark.parametrize(
    ("point", "expected", "feasible"),
    [
        ([6.22, 50.30, 223.27, 98.17, 26.05, 118.64, 1.66], 664233798.3388561, False),
        ([114.532, 20.1116, 299.668, 83.5222, 0.17874, 105.607, 2.81435], -26.603621311081888, True),
    ],
)
def test_gripper_worst_sampled_closure(point, expected, feasible):
    result = gripper_components(point)
    assert result["fun"] == pytest.approx(expected, rel=1e-12)
    assert bool(result["feasible"]) == feasible


@pytest.mark.parametrize("a,b,e,length", [(0, 50, 20, 100), (50, 0, 20, 100), (50, 50, 0, 25)])
def test_gripper_rejects_undefined_linkage(a, b, e, length):
    result = gripper_components([a, b, 100, e, 30, length, 2])
    assert result["fun"] == result["penalty"] == 1e30
    assert result["feasible"] is False
