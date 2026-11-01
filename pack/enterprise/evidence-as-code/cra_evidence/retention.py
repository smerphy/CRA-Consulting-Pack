"""Retention calculator.

Art 13(13): technical documentation and the EU declaration of conformity are
kept for at least 10 years after the product is placed on the market or for
the support period, whichever is longer (reports/sections/10-conformity.md;
reports/sections/08-annex1-part2.md Table 2). Art 13(18) applies the same
rule to Annex II user information. Art 13(9): each security update remains
available for at least 10 years after issue or the remainder of the support
period (KB wording; treated here as whichever is longer, which is the
conservative reading).

Placing date for software versions (Commission draft guidance C(2026) 5252,
paras 13-15 and Example 2; reports/sections/03-scope.md): a standalone
software version is placed on the market at its first offering. A later
version that is not a substantial modification (and is not a distinct
variant, para 14) keeps that placing date. The record then carries the
inherited date in `placing_on_market.inherited_placing_date`, and the
retention clock runs from it where it is earlier than the version's own
date. Using the version date instead gives a later retain-until date, which
errs on the safe side but overstates the legal minimum.
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


def effective_placing_date(placing):
    """Placing date that starts the Art 13(13) clock for a record's placing block.

    For an `update_to_placed_product` event carrying an inherited placing
    date, the earlier of that date and the version date; otherwise the
    version date. Returns None when no date is recorded.
    """
    placing = placing or {}
    own = placing.get("date")
    inherited = placing.get("inherited_placing_date")
    if placing.get("event") == "update_to_placed_product" and inherited:
        if not own:
            return parse_date(inherited)
        return min(parse_date(own), parse_date(inherited))
    return parse_date(own) if own else None


def retain_until(placing_date, support_end, buffer_days=0, inherited_placing_date=None):
    """max(placing + 10 years, support period end) [+ optional buffer].

    `inherited_placing_date` is the placing date a non-substantial version
    keeps (guidance para 15, Example 2); it is used where it is earlier.
    """
    placing = parse_date(placing_date)
    if inherited_placing_date:
        placing = min(placing, parse_date(inherited_placing_date))
    end = parse_date(support_end)
    base = max(add_years(placing, LEGAL_YEARS), end)
    return base + _dt.timedelta(days=buffer_days)


def update_available_until(issue_date, support_end):
    """Art 13(9) availability of a security update (conservative reading)."""
    return max(add_years(parse_date(issue_date), LEGAL_YEARS), parse_date(support_end))


def support_years(placing_date, support_end):
    p, e = parse_date(placing_date), parse_date(support_end)
    return round((e - p).days / 365.25, 2)


def explain(placing_date, support_end, buffer_days=0, inherited_placing_date=None):
    version_date = parse_date(placing_date)
    placing = version_date
    if inherited_placing_date:
        placing = min(version_date, parse_date(inherited_placing_date))
    end = parse_date(support_end)
    ten = add_years(placing, LEGAL_YEARS)
    result = retain_until(placing, end, buffer_days)
    driver = "placing + 10 years" if ten >= end else "support period end"
    out = {
        "placing_date": placing.isoformat(),
        "support_end": end.isoformat(),
        "placing_plus_10y": ten.isoformat(),
        "retain_until": result.isoformat(),
        "driver": driver,
        "buffer_days": buffer_days,
        "rule": "Art 13(13): max(placing + 10 years, support period end)",
    }
    if inherited_placing_date:
        out["version_date"] = version_date.isoformat()
        out["inherited_placing_date"] = parse_date(inherited_placing_date).isoformat()
        out["placing_basis"] = ("inherited placing date (guidance para 15, Example 2)"
                                if placing < version_date else "version date (not later than the inherited date)")
    return out
