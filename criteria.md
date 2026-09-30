# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next week costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

I picked 4 of 5 because the parking permit answer sits in a single sentence in one document, and if that document ever gets split the sentence could be separated from the question it answers.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
All five, because naming a source happens in my prompt in generate.py. It either works for every answer or it is broken for all of them.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
The two groups did not overlap at all. My five in-corpus questions scored 0.178 to 0.456 and the five out-of-corpus ones scored 0.825 to 0.934, leaving a 0.37-wide gap with nothing in it, so a cutoff of 0.6 separates them with margin on both sides. I still said 4 of 5 rather than 5 of 5 because that gap is only this clean while my out-of-corpus questions are about unrelated subjects — a question that sounded like campus life but was not covered would land far closer to the line.

> **Revised in week 2:** The gate also refuses at least 4 of 5 campus-sounding
> questions that my corpus does not answer.
>
> **Why revised:** This tightens the target rather than lowering it. The original
> five questions were all from unrelated subjects, so the criterion could not
> tell whether the gate stopped the questions that actually matter. At 0.6 it
> refused only 2 of 5 campus-sounding ones.


---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

Every chunk is one complete document — 88 documents produce 88 chunks, no chunk contains text from more than one source, and every chunk ends with a full stop, question mark or exclamation mark.

**Why this target:**
My longest document is 549 characters against a chunk size of 800, so nothing splits. For short posts where useful information sits in a single sentence, one post per chunk is what I want, and this is how I would notice if a Milestone 3 change broke it.


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

For 5 of 5 questions, every document my system names as a source contains the text its answer relied on — not just one of them.


**Why this target:**
Criterion 2 only checks that a source is named, not that it is the right one. A confident answer citing the wrong document is worse than no answer, because a reader has no way to tell.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in week 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
