"""The statistics the protocol allows, and none it forbids."""
import pytest

import bench.stats as stats
from bench.stats import iqr, median, percentile


def test_median_odd_and_even():
    assert median([3.0, 1.0, 2.0]) == 2.0
    assert median([4.0, 1.0, 3.0, 2.0]) == 2.5


def test_percentile_nearest_rank():
    xs = [float(i) for i in range(1, 11)]      # 1..10
    assert percentile(xs, 50) == 5.0
    assert percentile(xs, 95) == 10.0
    assert percentile(xs, 100) == 10.0


def test_iqr_on_known_data():
    xs = [float(i) for i in range(1, 11)]
    assert iqr(xs) == 8.0 - 3.0                # nearest-rank q3 - q1


def test_empty_input_refused():
    with pytest.raises(ValueError):
        median([])
    with pytest.raises(ValueError):
        percentile([], 50)


def test_there_is_no_mean():
    """The protocol says medians, never means. Hold the file to it."""
    assert not hasattr(stats, "mean")
    assert "def mean" not in open(stats.__file__).read()
