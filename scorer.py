"""
Decides whether one answer was right. run_eval.py finds this file automatically.

An answer passes when the phrase in `expects` (from questions.py) appears in it,
ignoring case. A refusal never passes, even if the phrase happens to be in it.
"""

import gate


def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects or answer.strip() == gate.REFUSAL:
        return False
    return expects.lower() in answer.lower()
