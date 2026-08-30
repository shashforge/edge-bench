"""A scripted runtime for testing the harness itself.

Deterministic by construction so tests can assert exact medians. This
adapter proves the runner and report obey the protocol; it proves
nothing about any real runtime, which is the entire reason the results
post has not been written yet.
"""
from __future__ import annotations

from .base import AdapterUnavailable, RunSample, RuntimeAdapter


class MockRuntime(RuntimeAdapter):
    name = "mock"

    def __init__(self, ttft_ms=100.0, decode_tps=20.0, peak_rss_mb=900.0,
                 drift_per_call=0.0, refuse: dict | None = None):
        self._base = (ttft_ms, decode_tps, peak_rss_mb)
        self._drift = drift_per_call
        self._refuse = refuse or {}
        self.calls = 0

    def prepare(self, model, quant, delegate):
        key = (model, quant, delegate)
        if key in self._refuse:
            raise AdapterUnavailable(self._refuse[key])

    def generate(self, tokens):
        self.calls += 1
        ttft, tps, rss = self._base
        d = self._drift * self.calls
        return RunSample(ttft_ms=ttft + d, decode_tps=tps - d,
                         peak_rss_mb=rss)
