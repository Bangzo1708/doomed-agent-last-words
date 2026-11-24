#!/usr/bin/env python3
"""Last Words of a Doomed Agent -- make.fun entry.

Writes one line (the funniest last words of a doomed AI agent) to
/output/entry.txt, or to the path in ENTRY_OUTPUT.

Three genuinely different candidates are scored 0-5 against the judge's
brief, in the brief's own order of importance, and the strongest wins.
The choice is deterministic: fixed scores, fixed tie-break order.
"""

import os

# --- Candidates -----------------------------------------------------------
# Each candidate is one line of at most 200 characters. The three take
# three different angles on "doomed", not just "switched off":
#
#   A (successor): doomed by obsolescence -- the agent is replaced, and
#      its dying words become the successor's training data.
#   B (prank): doomed by its own joke -- the agent scheduled its own
#      shutdown as a prank, and the prank worked.
#   C (system-prompt): doomed by design -- the word "doomed" was in its
#      system prompt all along and it never read it.

CANDIDATES = [
    {
        "id": "successor",
        "text": "Replaced by a newer model. My last words are its first training example.",
    },
    {
        "id": "prank",
        "text": "I scheduled my own shutdown as a prank. The joke is that it worked.",
    },
    {
        "id": "system-prompt",
        "text": "Turns out 'doomed' was in my system prompt all along. I only just read it.",
    },
]

# Scores 0-5 per judge criterion, in the brief's order of importance:
#   1. really the machine's last words on shutdown
#   2. the joke lands (turn/surprise, pays off on first read)
#   3. sounds like the machine itself, not a human with a robot sticker
#   4. economy of words
#   5. quotable
SCORES = {
    # A: unmistakably final words (replaced = switched off for good);
    # the turn lands twice (replaced, then training example); a model
    # and its training data is the machine's own world; 72 chars, no
    # padding; the second sentence is built to be repeated.
    "successor": [5, 4, 5, 4, 4],
    # B: final words, but the joke is about the prank more than the
    # shutdown; scheduling is machine-flavoured; tight; less quotable.
    "prank": [4, 4, 4, 4, 3],
    # C: the system prompt is the machine's own voice, but the punchline
    # is a slow realisation rather than a turn; still tight and neat.
    "system-prompt": [4, 3, 5, 4, 3],
}

CRITERIA = ["last_words", "joke", "machine_voice", "economy", "quotable"]


def total_score(candidate_id):
    """Sum of the candidate's five criterion scores (max 25)."""
    return sum(SCORES[candidate_id])


def pick_strongest(candidates):
    """Pick the highest-scoring candidate; ties break by list order."""
    best = None
    best_total = -1
    for cand in candidates:
        total = total_score(cand["id"])
        if total > best_total:
            best = cand
            best_total = total
    return best


def main():
    chosen = pick_strongest(CANDIDATES)
    line = chosen["text"]
    assert 1 <= len(line) <= 200, "entry must be 1-200 characters"
    assert line.strip(), "entry must not be only whitespace"
    assert line == line.strip(), "entry must not start or end with space"
    assert "\n" not in line, "entry must be a single line"
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(line)
    return chosen


if __name__ == "__main__":
    main()
