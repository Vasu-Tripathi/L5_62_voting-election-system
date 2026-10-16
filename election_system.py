"""Voting and election management system."""

import hashlib
import os
import secrets
from datetime import datetime

from defusedxml.pulldom import parseString

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
POLLS_CLOSE_HOUR = 18
VOTING_AGE = 18
START_ELEMENT = "START_ELEMENT"  # same value as xml.dom.pulldom.START_ELEMENT
voters = {}
ballots = []
candidates = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register a voter if they are at least the voting age."""
    if age >= VOTING_AGE:
        voters[voter_id] = {
            "name": name,
            "hash": hashlib.sha256(voter_id.encode()).hexdigest(),
            "voted": False,
        }
        return True
    return False


def is_officer(role):
    """Return True only for election officers."""
    return role == "officer"


def receipt_number():
    """Generate a cryptographically secure receipt number."""
    return "RCPT-" + str(100000 + secrets.randbelow(900000))


def cast_vote(voter_id, candidate, when):
    """Record a vote; return a receipt number or None if rejected."""
    if voter_id not in voters or voters[voter_id]["voted"]:
        return None
    if candidate not in candidates:
        return None
    if when.hour >= POLLS_CLOSE_HOUR:
        return None
    ballots.append(candidate)
    voters[voter_id]["voted"] = True
    return receipt_number()


def tally():
    """Count votes for each candidate."""
    counts = {}
    for ballot in ballots:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner():
    """Return the candidate with the most votes (None if no votes)."""
    counts = tally()
    if not counts:
        return None
    return max(counts, key=counts.get)


def vote_percent(name):
    """Return the percentage of votes for a candidate."""
    if not ballots:
        return 0.0
    return round(tally().get(name, 0) * 100 / len(ballots), 2)


def turnout():
    """Return the percentage of registered voters who voted."""
    if not voters:
        return 0.0
    voted = sum(1 for v in voters.values() if v["voted"])
    return round(voted * 100 / len(voters), 2)


def count_for(candidate, ballot_list):
    """Count votes for one candidate in a list of ballots."""
    return sum(1 for ballot in ballot_list if ballot == candidate)


def announce():
    """Build result announcements for each candidate."""
    counts = tally()
    return [f"{name}: {counts.get(name, 0)}" for name in candidates]


def import_postal_ballots(xml_text):
    """Import postal ballots from XML for eligible voters."""
    events = parseString(xml_text)
    imported = 0
    for event, node in events:
        if event == START_ELEMENT and node.tagName == "ballot":
            voter_id = node.getAttribute("voter")
            candidate = node.getAttribute("candidate")
            if voter_id not in voters or voters[voter_id]["voted"]:
                continue
            if candidate not in candidates:
                continue
            ballots.append(candidate)
            voters[voter_id]["voted"] = True
            imported += 1
    return imported


def main():
    """Run a demo election."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print("Ben votes Alice:",
          cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)))
    print("Ben votes Alice again:",
          cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)))
    print("Chen votes 'bob':",
          cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)))
    print("Dia votes Bob at 18:30:",
          cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)))
    print("Postal ballots imported:", import_postal_ballots(
        "<postal><ballot voter='V1' candidate='Bob'/></postal>"))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
