"""The runner obeys the protocol it imports."""
from bench import protocol
from bench.adapters.mock import MockRuntime
from bench.runner import Measured, Session, Unavailable, measure_cell


def test_warmups_are_taken_and_discarded():
    rt = MockRuntime(ttft_ms=100.0, drift_per_call=1.0)
    cell = measure_cell(rt, "Llama-3.2-1B-Instruct", "int4", "cpu")
    assert rt.calls == protocol.WARMUP_RUNS + protocol.MEASURED_RUNS
    assert isinstance(cell, Measured)
    # first measured sample is call 4: ttft 104; tenth is 113; median 108.5
    assert cell.ttft_p50_ms == 108.0           # nearest-rank on 104..113
    assert cell.samples == protocol.MEASURED_RUNS


def test_a_refused_cell_reports_its_reason():
    rt = MockRuntime(refuse={("Gemma3-1B", "int4", "npu"):
                             "delegate unsupported: no NNAPI path"})
    cell = measure_cell(rt, "Gemma3-1B", "int4", "npu")
    assert isinstance(cell, Unavailable)
    assert cell.reason == "delegate unsupported: no NNAPI path"
    assert rt.calls == 0                       # nothing ran, nothing warmed


def test_steady_numbers_have_zero_iqr():
    cell = measure_cell(MockRuntime(decode_tps=20.0), "m", "int8", "cpu")
    assert cell.decode_tps_median == 20.0
    assert cell.decode_tps_iqr == 0.0


def test_session_collects_cells_in_order():
    s = Session(device="test-bench", preflight_confirmed=True)
    s.measure(MockRuntime(), "m", "fp16", "cpu")
    s.measure(MockRuntime(refuse={("m", "int4", "npu"): "crash"}),
              "m", "int4", "npu")
    assert isinstance(s.cells[0], Measured)
    assert isinstance(s.cells[1], Unavailable)
