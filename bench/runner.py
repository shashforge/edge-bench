"""Measure one cell of the matrix, or record exactly why you cannot.

A cell is (runtime, model, quant, delegate). The protocol is imported,
not restated: warmups come from protocol.WARMUP_RUNS, the sample count
from protocol.MEASURED_RUNS. Every cell yields either Measured numbers
or Unavailable with the adapter's own words for why.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import protocol
from .adapters.base import AdapterUnavailable, RuntimeAdapter
from .stats import iqr, median, percentile


@dataclass(frozen=True)
class Measured:
    runtime: str
    model: str
    quant: str
    delegate: str
    ttft_p50_ms: float
    ttft_p95_ms: float
    decode_tps_median: float
    decode_tps_iqr: float
    peak_rss_mb_median: float
    samples: int = protocol.MEASURED_RUNS


@dataclass(frozen=True)
class Unavailable:
    runtime: str
    model: str
    quant: str
    delegate: str
    reason: str


@dataclass
class Session:
    """One device session. Preflight confirmation is recorded, not
    assumed; reports refuse to bless cells measured without it."""

    device: str
    preflight_confirmed: bool
    cells: list = field(default_factory=list)

    def measure(self, adapter: RuntimeAdapter, model: str, quant: str,
                delegate: str):
        cell = measure_cell(adapter, model, quant, delegate)
        self.cells.append(cell)
        return cell


def measure_cell(adapter: RuntimeAdapter, model: str, quant: str,
                 delegate: str):
    try:
        adapter.prepare(model, quant, delegate)
        for _ in range(protocol.WARMUP_RUNS):
            adapter.generate(protocol.GENERATION_TOKENS)
        samples = [adapter.generate(protocol.GENERATION_TOKENS)
                   for _ in range(protocol.MEASURED_RUNS)]
    except AdapterUnavailable as e:
        return Unavailable(adapter.name, model, quant, delegate, str(e))

    ttfts = [s.ttft_ms for s in samples]
    tps = [s.decode_tps for s in samples]
    rss = [s.peak_rss_mb for s in samples]
    return Measured(
        runtime=adapter.name, model=model, quant=quant, delegate=delegate,
        ttft_p50_ms=percentile(ttfts, 50),
        ttft_p95_ms=percentile(ttfts, 95),
        decode_tps_median=median(tps),
        decode_tps_iqr=iqr(tps),
        peak_rss_mb_median=median(rss),
    )
