"""The report shows numbers or reasons, and shames unprotocolled runs."""
from bench.adapters.mock import MockRuntime
from bench.report import render
from bench.runner import Session


def build_session(confirmed=True):
    s = Session(device="unit-test", preflight_confirmed=confirmed)
    s.measure(MockRuntime(ttft_ms=120.0, decode_tps=18.5,
                          peak_rss_mb=850.0), "Llama-3.2-1B-Instruct",
              "int4", "cpu")
    s.measure(MockRuntime(refuse={("Llama-3.2-1B-Instruct", "int4", "npu"):
                                  "conversion failed: unsupported op"}),
              "Llama-3.2-1B-Instruct", "int4", "npu")
    return s


def test_measured_and_unavailable_cells_both_render():
    text = render(build_session())
    assert "120 / 120" in text
    assert "18.5 (IQR 0.0)" in text
    assert "no numbers: conversion failed: unsupported op" in text


def test_unprotocolled_sessions_are_marked():
    text = render(build_session(confirmed=False))
    assert "UNPROTOCOLLED SESSION" in text
    assert "must not be quoted" in text


def test_protocolled_sessions_are_not_marked():
    assert "UNPROTOCOLLED" not in render(build_session())
