# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
Ime Iyonsi     Corpus: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This is a question-answering system over `campus_life`, a corpus of 88 short
posts written by students about life at a university — dining hall wait times,
what a particular dorm is actually like, and the administrative rules nobody
explains properly. You ask it a question in plain English, it finds the posts
most likely to contain the answer, and it answers using only those posts,
naming the file it used.

It is built to answer questions with one specific answer sitting in one
document: when parking permits go on sale, how long you have to change your
meal plan, how many credit hours graduation takes. It is deliberately bad at
anything else. A relevance gate measures how close the best retrieved post is
to your question and refuses outright when nothing is close enough, so asking
it about diesel engines or the 1994 World Cup returns "I don't have enough
information about that" rather than a confident guess.

## Chunking Strategy

**Chunk size:** 800
**Overlap:** 120

My corpus is 88 short posts. Indexing them produces `88 chunks, 317 characters
on average (shortest 178, longest 549), produced by chunker.py::fallback_split`
— one chunk per document, because my longest document is 549 characters and
never reaches the 800 limit. Nothing splits, so the 120-character overlap never
applies either.

I kept these numbers because that is the behaviour I want here. The corpora
README notes that in `campus_life` useful information tends to sit in a single
sentence, and the five sampled chunks below bear that out: each one answers a
question on its own, without needing the text before or after it. Splitting a
post of this length would separate a fact from the sentence stating it and gain
nothing, since no document is large enough for retrieval to struggle with.

The honest caveat is that my chunker gets the right answer for the wrong reason.
It counts characters and happens never to reach its limit — one chunk per
document is an accident of my documents being short, not a decision the code
makes. A splitter that worked on paragraph boundaries would produce the same
output deliberately, and would still behave sensibly if I added a longer
document.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::fallback_split`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::fallback_split`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::fallback_split`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::fallback_split`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::fallback_split`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Where do students park if they miss the permit window?

**Answer:**

```
Students who miss the permit window park on Verrill Street and walk in. This
information comes from `admin_parking_permits.txt`.

Sources retrieved: admin_parking_permits.txt, dining_halden_hall_followup.txt,
dining_north_kitchen_followup.txt, transit_shuttle.txt, transit_walking.txt

1 model calls this session, 625 tokens (595 in, 30 out)
```

Best distance 0.456, under the 0.6 cutoff, so the gate passed it through. The
answer names one source and it is the right one — the Verrill Street sentence
is in `admin_parking_permits.txt` and nowhere else in the corpus.

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

**0.6** — the starter's default, which I kept after measuring rather than by
leaving it alone.

My five in-corpus questions score between 0.178 and 0.456. The five
`OUT_OF_SCOPE` questions score between 0.825 and 0.934. Nothing at all lands
between 0.456 and 0.825, so the gap is 0.37 wide and any cutoff inside it
separates the two groups perfectly. 0.6 sits near the middle of that gap with
0.14 of margin below my worst real question and 0.22 above my best unrelated
one.

The separation is this clean because my out-of-corpus questions are about
entirely different subjects — Mongolia, diesel engines, the World Cup. A
question that sounded like campus life but was not covered, such as a credit
limit my documents never state, would land much closer to the boundary. I did
not measure one of those, so 0.6 is verified against distant questions only.

| Question | In corpus? | Best distance |
|---|---|---|
| How long can students change their meal plan tier after the semester starts? | Yes | 0.178 |
| How many credit hours are required to graduate? | Yes | 0.289 |
| When do student parking permits go on sale? | Yes | 0.346 |
| What is the maximum number of hours per week a student can work on campus during term? | Yes | 0.383 |
| Where do students park if they miss the permit window? | Yes | 0.456 |
| What is the capital of Mongolia? | No | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| Who won the 1994 World Cup? | No | 0.886 |
| How do I write a for loop in Rust? | No | 0.896 |
| How do I change the oil in a diesel engine? | No | 0.934 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I wrote five test questions and asked Claude to check them. Claude searched the documents and found out three of the five asked about facts that are not in Campus Life Corpus. There is no credit limit, no club count, and nothing about which meal plan is most popular. I had to rewrite all five from sentences I
had actually read in the documents, and the “expects” value for each is now a
word that appears in the file it came from.


**2.** I asked Claude for a criterion about my chunks and it gave me "no chunk is
split mid-sentence." I indexed the corpus and saw that my longest document is 549 characters against a chunk size of 800, so nothing in my corpus splits at all and the criterion could not fail. I rewrote it to state the whole baseline (88 documents producing 88 chunks, one source per chunk, every chunk ending in sentence punctuation) so that it still passes today but would break the moment a milestone 3 change starts splitting documents.

*Added in week 2:*

**3.** My before run met all five criteria, so I focused on the weakness I identified in Week 1: campus-related questions that my documents cannot answer. Claude confirmed five such questions had no answers in the 88 files and tested them with `app.py retrieve`. At the 0.6 cutoff, three passed the gate.
Claude found that the gate measures topic similarity, not whether the answer is actually in the document. For example, the Aldridge Hall pricing question scored 0.282 even though no price was provided. The model still refused to answer when tested with `app.py ask`. I chose to lower the cutoff to 0.46, which blocked two of the three, but the Aldridge Hall question remains a limitation that a cutoff alone cannot fix. The new cutoff also leaves my parking question with only a 0.004 margin.

**4.** I had Claude create `scorer.py`, which checks whether the expected phrase appears in the answer. Claude pointed out that simple text matching has limitations. For example, `"20"` could match `"120"`, while `"ten days"` would not match `"10 days"`.
The scorer worked correctly in my tests, but I didn't rely on it alone. For criterion 5, I had Claude check each cited file to confirm the answer was actually supported by it. I included the scorer limitation under **What's Still Broken**.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Every chunk is one complete document | 88 of 88 | 88 of 88 | 88 of 88 | 88 of 88 | MET |
| 5. Every named source contains the answer | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |


<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Evidence file: `results/run_2026-09-29_2316_before.md`, produced by `run_eval.py::main`.

**Criteria 1, 2 and 5**: parking question, run 1:

```
- Best distance: 0.4561 (passed the gate)
- Sources retrieved: admin_parking_permits.txt, dining_halden_hall_followup.txt, dining_north_kitchen_followup.txt, transit_shuttle.txt, transit_walking.txt

Students who miss the permit window park on Verrill Street and walk in. This information comes from `admin_parking_permits.txt`.
```

**Criterion 3**: produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |

**Criterion 4**: produced by `chunker.py::fallback_split`:

```
88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::fallback_split
``` 

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | I checked all 15 runs and confirmed that the file containing the correct answer was retrieved each time. All runs scored 5 out of 5, exceeding the target of 4 out of 5. |
| 2 | Every answer names a source | MET | All 15 answers correctly identified a .txt file, meeting the target of 5 out of 5. None of the runs fell short. |
| 3 | Gate stops out-of-corpus questions | MET | The gate failed all 5 tests. The closest out-of-corpus question scored 0.825, which was well above the 0.6 cutoff.|
| 4 | Every chunk is one complete document | MET | After re-chunking, I got 88 chunks from 88 documents. Each chunk came from a single source, and none of them ended in the middle of a sentence. |
| 5 | Every named source contains the answer | MET | Each answer cited only one file. I went through the files individually and confirmed that the information provided was actually in the cited source. |


## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I did not find anything missing. All five conditions were present in all three attempts, so there was no missing data or failing stage to diagnose.

Actually, two of my targets were set pretty low. Requirements 1 and 3 had a target of 4 out of 5, but every run scored 5 out of 5. Criterion 1 was met easily because each of my five questions was looking for one specific piece of information from one document. The retrieval only needed to find one matching source.

Criterion 3 was also met easily because my five out-of-corpus questions were on completely different topics, such as Mongolia, diesel engines, and the World Cup. Their scores ranged from 0.825 to 0.934, which was well above the 0.6 threshold.

The one criterion I would revise is criterion 3. In my Week 1 write-up, I noted that the cutoff was tested only with questions that were very different from the information in my corpus. A better test would be a question that sounds like it could be related to my college experience but is not actually answered anywhere in my documents. A question like that could score much closer to 0.6, and the gate might allow it through even though the corpus does not contain the answer.

I would revise the criterion to: “The gate denies at least 4 out of 5 campus-related questions that my corpus cannot answer.”    

## The Improvement

**What I changed:** I lowered the relevance cutoff (`THRESHOLD` in `config.py`) from 0.6 to 0.46, and added five campus-sounding questions that my corpus does not answer to `OUT_OF_SCOPE` in `questions.py`, so the eval now tests the gate against harder questions.

**Why I picked it:** My diagnosis said criterion 3 was only tested against distant questions; when I measured five campus-sounding questions my documents don't answer, the gate at 0.6 let three of them through (0.282, 0.468, 0.477), so the gate was too loose for exactly the kind of question it most needs to stop.
 

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions (original five) | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3 (revised). Gate stops campus-sounding questions my corpus can't answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 4. Every chunk is one complete document | 88 of 88 | 88 of 88 | 88 of 88 | 88 of 88 | MET |
| 5. Every named source contains the answer | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Evidence file: `results/run_2026-09-30_0114_after.md`, produced by `run_eval.py::main`
and `run_eval.py::check_out_of_scope`, cutoff 0.46. Refused 9 of 10.

| Campus-sounding question (not in corpus) | Best distance | Gate at 0.6 (before) | Gate at 0.46 (after) |
|---|---|---|---|
| What is the maximum number of credit hours a student can take in one semester? | 0.468 | let through | refused |
| What time does the campus gym open? | 0.477 | let through | refused |
| How much does a room in Aldridge Hall cost per semester? | 0.282 | let through | **let through** |
| How many student clubs are there on campus? | 0.641 | refused | refused |
| What GPA do students need to keep a scholarship? | 0.622 | refused | refused |


**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

Yes, partly, but there was a tradeoff.

Lowering the cutoff from 0.6 to 0.46 improved the gate from refusing 2 of 5 campus-related questions to 4 of 5, meeting my revised criterion 3. My real questions still passed, cited the correct files, and the original out-of-corpus questions were still refused.

The downside is the smaller margin. My parking question scored 0.456, only 0.004 below the new cutoff, so a slight wording change could cause a valid question to be refused.

The cutoff also could not catch everything. The Aldridge Hall pricing question scored 0.282 because it matched the topic, even though my documents did not contain the answer. However, the generation stage caught it. `app.py ask` correctly responded that there was not enough information instead of making up an answer.


## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

No criteria are missed after the fix, but three areas are still weak.

1. **The Aldridge Hall question still passes the gate** at 0.282. The gate measures topic similarity, not whether the answer exists. The model correctly refused to answer, but still cited `housing_aldridge_hall.txt`. Next, I would update `generate.py` so refusals do not cite a source.
2. **The parking question is very close to the cutoff**, scoring 0.456 against 0.46. I would test a few rewordings to make sure valid questions are not refused.
3. **My scorer uses simple text matching.** For example, `"20"` could match `"120"`, while `"ten days"` would not match `"10 days"`. It worked correctly in my tests, but this could cause problems later.

I stopped here because the change met my revised target without affecting the other criteria. Fixing the prompt would be a separate change, and Week 2 asks for only one.


## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I would have written criterion 3 using campus-related questions from the start. Questions about Mongolia and diesel engines only showed that the gate could reject completely unrelated topics. The real test was questions that sounded like they belonged in my corpus but could not actually be answered from it. Those were the questions the original gate struggled with.

I would also change criterion 1 from **4 of 5** to **5 of 5**. Each question asks for one fact from one document, so allowing one miss was unnecessary, especially since all five were consistently retrieved.

