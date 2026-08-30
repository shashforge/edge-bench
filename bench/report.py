"""Render a session as the matrix the protocol promised: every cell
either numbers or a documented reason there are none."""
from __future__ import annotations

from .runner import Measured, Session, Unavailable


def render(session: Session) -> str:
    lines = [f"# edge-bench results · {session.device}", ""]
    if not session.preflight_confirmed:
        lines.append("**UNPROTOCOLLED SESSION** — preflight checklist was "
                     "not confirmed; these numbers do not meet the "
                     "published protocol and must not be quoted.")
        lines.append("")
    lines.append("| runtime | model | quant | delegate | TTFT p50/p95 (ms) "
                 "| decode tok/s (median, IQR) | peak RSS (MB) |")
    lines.append("|---|---|---|---|---|---|---|")
    for c in session.cells:
        if isinstance(c, Measured):
            lines.append(
                f"| {c.runtime} | {c.model} | {c.quant} | {c.delegate} "
                f"| {c.ttft_p50_ms:.0f} / {c.ttft_p95_ms:.0f} "
                f"| {c.decode_tps_median:.1f} (IQR {c.decode_tps_iqr:.1f}) "
                f"| {c.peak_rss_mb_median:.0f} |")
        elif isinstance(c, Unavailable):
            lines.append(
                f"| {c.runtime} | {c.model} | {c.quant} | {c.delegate} "
                f"| *no numbers: {c.reason}* | — | — |")
    return "\n".join(lines) + "\n"
