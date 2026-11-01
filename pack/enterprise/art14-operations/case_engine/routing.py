"""Coordinator CSIRT derivation under Art 14(7).

KB: reports/sections/09-reporting.md "Routing"; corporate guide 07 "Choosing and
documenting the coordinator CSIRT"; research notes KQ4 (ENISA SRP FAQ 8 and 18).

Order applied:
 1. Main establishment = Member State where decisions related to the
    cybersecurity of the products are predominantly taken.
 2. If that cannot be determined: the EU establishment with the most employees.
 3. No EU establishment: Member State of the authorised representative, then
    importer, then distributor (each "handling the highest number of products"),
    then the Member State with the most users.
A wrong choice "may invalidate the notification" (ENISA SRP FAQ 18), so the
result is a decision record for legal sign-off, not a runtime guess.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RoutingDecision:
    member_state: str
    basis: str
    csirt_name: str | None
    csirt_url: str | None
    outage_fallback: str | None

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class RoutingError(ValueError):
    pass


def derive_coordinator(manufacturer: dict, csirts: dict) -> RoutingDecision:
    ests = manufacturer.get("eu_establishments") or []
    ms, basis = None, None
    if ests:
        predominant = [e for e in ests if e.get("product_security_decisions_predominant")]
        if len(predominant) == 1:
            ms = predominant[0]["member_state"]
            basis = (f"Art 14(7): main establishment, where product cybersecurity decisions are "
                     f"predominantly taken ({predominant[0].get('entity', ms)})")
        else:
            top = max(ests, key=lambda e: e.get("employees", 0))
            ms = top["member_state"]
            basis = ("Art 14(7): decision-making location not determinable; EU establishment with "
                     f"the most employees ({top.get('entity', ms)})")
    else:
        for key, label in (("authorised_representative_member_state", "authorised representative"),
                           ("importer_member_state", "importer"),
                           ("distributor_member_state", "distributor"),
                           ("most_users_member_state", "most users")):
            if manufacturer.get(key):
                ms = manufacturer[key]
                basis = f"Art 14(7) third subparagraph: no EU establishment; Member State of the {label}"
                break
    if ms is None:
        raise RoutingError("cannot derive a coordinator CSIRT: no establishment or fallback data")
    c = csirts.get(ms, {})
    return RoutingDecision(ms, basis, c.get("name"), c.get("url"), c.get("outage_fallback"))
