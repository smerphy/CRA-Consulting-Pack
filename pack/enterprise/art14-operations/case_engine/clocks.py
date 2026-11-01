"""Article 14 clocks.

Legal rules (KB: reports/sections/09-reporting.md "Timeline"; pack_data fact F04;
verification.md claim 7):
  - AEV early warning: within 24 hours of awareness (Art 14(2)(a)).
  - AEV vulnerability notification: within 72 hours of awareness (Art 14(2)(b)).
  - AEV final report: no later than 14 days after a corrective or mitigating
    measure is available (Art 14(2)(c)).
  - Severe incident early warning: 24 hours; notification: 72 hours (Art 14(4)(a)-(b)).
  - Severe incident final report: within one month after the submission of the
    incident notification under point (b) (Art 14(4)(c)).
  - The 24 h and 72 h clocks both run from awareness, not consecutively
    (application guide 10-reporting-runbook.md).

Design choices (pack, labelled):
  - All arithmetic is in UTC on exact instants. No business-day, weekend or
    public-holiday adjustment is applied: clocks are weekend-agnostic.
  - Calendar periods use the earliest defensible end: 14 days = 14 x 24 h from
    the instant the measure became available; one month = same day and time in
    the next calendar month, clamped to the last day of a shorter month.
    Any general EU rule that might extend day or month periods ending on a
    weekend is deliberately NOT relied on (not in the KB; unverified).
"""
from __future__ import annotations

import calendar
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

EARLY_WARNING_HOURS = 24
NOTIFICATION_HOURS = 72
AEV_FINAL_DAYS = 14
SI_FINAL_MONTHS = 1
# ENISA SRP FAQ 26 (KB 09-reporting.md "Known quirk"): the platform's 72-hour
# counter currently shows a due time 48 hours after early-warning submission.
SRP_72H_COUNTER_HOURS_AFTER_EW = 48


class ClockError(ValueError):
    pass


def parse_utc(value: str | datetime) -> datetime:
    """Parse an ISO 8601 timestamp that carries an offset and return it in UTC.

    Naive timestamps are rejected: the SRP date fields are UTC and an
    ambiguous local time is the commonest source of a wrong awareness time.
    """
    if isinstance(value, datetime):
        dt = value
    else:
        text = value.strip()
        if text.endswith("Z") or text.endswith("z"):
            text = text[:-1] + "+00:00"
        if text.endswith(" UTC"):
            text = text[:-4] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ClockError(f"not an ISO 8601 timestamp: {value!r}") from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ClockError(f"timestamp has no UTC offset: {value!r}; add 'Z' or '+00:00'")
    return dt.astimezone(UTC)


def fmt_utc(dt: datetime | None) -> str:
    """Format in the SRP glossary style, e.g. '2026-08-24 09:15 UTC'."""
    if dt is None:
        return "-"
    return dt.astimezone(UTC).strftime("%Y-%m-%d %H:%M UTC")


def iso(dt: datetime | None) -> str | None:
    return None if dt is None else dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def add_months(dt: datetime, months: int) -> datetime:
    """Same day and time `months` later; clamp to the month's last day."""
    month_index = dt.month - 1 + months
    year = dt.year + month_index // 12
    month = month_index % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def early_warning_due(aware_at: datetime) -> datetime:
    return aware_at + timedelta(hours=EARLY_WARNING_HOURS)


def notification_due(aware_at: datetime) -> datetime:
    return aware_at + timedelta(hours=NOTIFICATION_HOURS)


def aev_final_due(fix_available_at: datetime | None) -> datetime | None:
    """14 days after a corrective or mitigating measure is available; None until one is."""
    if fix_available_at is None:
        return None
    return fix_available_at + timedelta(days=AEV_FINAL_DAYS)


def si_final_due(notification_submitted_at: datetime | None) -> datetime | None:
    """One month after submission of the 72-hour incident notification; None until submitted."""
    if notification_submitted_at is None:
        return None
    return add_months(notification_submitted_at, SI_FINAL_MONTHS)


def si_final_due_projected(aware_at: datetime) -> datetime:
    """Latest possible SI final deadline if the notification is filed at the 72 h limit."""
    return add_months(notification_due(aware_at), SI_FINAL_MONTHS)


def srp_72h_counter(early_warning_submitted_at: datetime | None) -> datetime | None:
    """What the SRP counter will display (a visibility aid, not the legal deadline)."""
    if early_warning_submitted_at is None:
        return None
    return early_warning_submitted_at + timedelta(hours=SRP_72H_COUNTER_HOURS_AFTER_EW)


def status(due_at: datetime | None, done_at: datetime | None, now: datetime, warn_hours: float = 6) -> str:
    """Return one of: pending-trigger, met, met-late, overdue, due-soon, open."""
    if due_at is None:
        return "met" if done_at else "pending-trigger"
    if done_at is not None:
        return "met" if done_at <= due_at else "met-late"
    if now > due_at:
        return "overdue"
    if due_at - now <= timedelta(hours=warn_hours):
        return "due-soon"
    return "open"
