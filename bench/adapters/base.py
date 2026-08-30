"""What a runtime has to provide to be measured.

An adapter that cannot serve a configuration raises
AdapterUnavailable with the reason. The runner records the reason as
the cell's result. Negative results are results; silent gaps are how
vendor benchmarks lie.
"""
from __future__ import annotations

from dataclasses import dataclass


class AdapterUnavailable(Exception):
    """This (model, quant, delegate) cell cannot run; the message says why."""


@dataclass(frozen=True)
class RunSample:
    """One generation, measured on-device."""

    ttft_ms: float        # request to first token
    decode_tps: float     # steady-state tokens per second
    peak_rss_mb: float    # high-water mark during generation


class RuntimeAdapter:
    """One runtime (ExecuTorch, LiteRT, ONNX Runtime, llama.cpp)."""

    name = "unnamed"

    def prepare(self, model: str, quant: str, delegate: str) -> None:
        """Load or convert. Raises AdapterUnavailable with the reason
        when this cell cannot run: conversion failed, delegate
        unsupported, crash."""
        raise NotImplementedError

    def generate(self, tokens: int) -> RunSample:
        """One measured generation of `tokens` tokens."""
        raise NotImplementedError
