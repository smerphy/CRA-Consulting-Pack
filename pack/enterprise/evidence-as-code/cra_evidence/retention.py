"""Retention calculator.

Art 13(13): technical documentation and the EU declaration of conformity are
kept for at least 10 years after the product is placed on the market or for
the support period, whichever is longer (reports/sections/10-conformity.md;
reports/sections/08-annex1-part2.md Table 2). Art 13(18) applies the same
rule to Annex II user information. Art 13(9): each security update remains
available for at least 10 years after issue or the remainder of the support
period (KB wording; treated here as whichever is longer, which is the
conservative reading).
"""

import datetime as _dt

LEGAL_YEARS = 10


def add_years(d, years):
    """Add whole years; 29 Feb maps to 28 Feb in non-leap target years."""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)


def parse_date(value):
    if isinstance(value, _dt.date):
        return value
    return _dt.date.fromisoformat(str(value)[:10])


def retain_until(placing_date, support_end, buffer_days=0):
    """max(placing + 10 years, support period end) [+ optional buffer]."""
    placing = parse_date(placing_date)
    end = parse_date(support_end)
    base = max(add_years(placing, LEGAL_YEARS), end)
    return base + _dt.timedelta(days=buffer_days)


def update_available_until(issue_date, support_end):
    """Art 13(9) availability of a security update (conservative reading)."""
    return max(add_years(parse_date(issue_date), LEGAL_YEARS), parse_date(support_end))


def support_years(placing_date, support_end):
    p, e = parse_date(placing_date), parse_date(support_end)
    return round((e - p).days / 365.25, 2)


def explain(placing_date, support_end, buffer_days=0):
    placing = parse_date(placing_date)
    end = parse_date(support_end)
    ten = add_years(placing, LEGAL_YEARS)
    result = retain_until(placing, end, buffer_days)
    driver = "placing + 10 years" if ten >= end else "support period end"
    return {
        "placing_date": placing.isoformat(),
        "support_end": end.isoformat(),
        "placing_plus_10y": ten.isoformat(),
        "retain_until": result.isoformat(),
        "driver": driver,
        "buffer_days": buffer_days,
        "rule": "Art 13(13): max(placing + 10 years, support period end)",
    }
