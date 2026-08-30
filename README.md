# edge-bench

The [shashforge.dev Edge AI benchmark protocol](https://shashforge.dev/log/edge-ai-benchmark-protocol/),
as runnable code. The protocol was published on 2026-08-04, before any
numbers existed; this repo encodes it so the eventual numbers cannot
quietly drift from the methodology they answer to.

**Status: harness only. No numbers yet.** Every result in a report
comes from a `RuntimeAdapter`, and the only adapter here is a scripted
mock that exists to test the harness itself. Real adapters (ExecuTorch,
LiteRT, ONNX Runtime, llama.cpp) land together with the first results,
measured on physical devices named in the results post.

## The rules, enforced in code

- `bench/protocol.py` holds the discipline as constants: 3 warmups
  discarded, 10 measured runs, medians with IQR. The runner imports
  them; changing the protocol is a visible diff.
- `bench/stats.py` contains no `mean()`, and a test pins that. One
  thermal throttle event ruins a mean and merely dents a median.
- Every cell of the matrix is `Measured` or `Unavailable(reason)`.
  Negative results are results; there is no way to skip a cell
  silently.
- A session records whether the preflight checklist (airplane mode,
  fixed brightness, battery, ambient temperature, physical device) was
  confirmed. Reports brand unconfirmed sessions UNPROTOCOLLED and say
  the numbers must not be quoted.

## Run the tests

```bash
pip install pytest
python -m pytest tests/ -v
```

MIT licensed. By [Shashi Shankar](https://shashforge.dev).
