"""The measurement discipline, as data.

Published before any numbers existed:
https://shashforge.dev/log/edge-ai-benchmark-protocol/

The rules live here as constants so the runner cannot drift from the
protocol without the diff saying so.
"""
from __future__ import annotations

WARMUP_RUNS = 3          # discarded, always
MEASURED_RUNS = 10       # medians with IQR reported, never means
GENERATION_TOKENS = 256  # steady-state decode measured over this many

# Every measured session starts by confirming each of these by hand.
# The runner records the checklist confirmation into the results file;
# unconfirmed runs are marked unprotocolled and excluded from reports.
PREFLIGHT = (
    "airplane mode on",
    "screen on at fixed brightness",
    "battery above 80 percent",
    "device cooled to ambient since the previous configuration",
    "physical device, not an emulator",
)

MODELS = ("Llama-3.2-1B-Instruct", "Gemma3-1B")
QUANTS = ("fp16", "int8", "int4")
DELEGATES = ("cpu", "gpu", "npu")
