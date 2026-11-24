# Round 2 model test — 2026-11-23 evening (Claude)

Billy's instruction: "we can rerun better tests, switch it to medium, give it tool calls, run multiple".

## Design
- Models: Gemini 4 Neon (Medium) via `agy -p --sandbox`; Claude Opus 5.5 (medium effort) via `claude -p` (read-only tools). Opus was meant to run through agy too, but all six agy Opus runs failed with "Individual quota reached" (429, resets in ~154 h); receipts in `agy-opus-quota-failed/`. Harness differs between models as a result.
- Both conditions received the same four raw answers (`notes.txt`) and the same task (`prompt-*.txt`).
  - Bare: told it has no files or tools; run in an empty directory (Opus with tools disabled).
  - Workflow: full reading files (Mellamphy 2021, Carlson 2015, Munn 2022 — whole files, page-split) in `./readings`; the model had to find passages itself and cite printed pages; asked for bookmarks, coaxing starter, paragraph.
- 3 runs per model per condition (12 total). Scoring: `scratchpad/r2/score.py` normalises quote marks/hyphenation, searches each quote in the reading, maps PDF page to printed page (offsets Mellamphy +9, Carlson +414, Munn −8, checked against running headers and the 5 source-map quotes). Manual check added for nested-quote false negatives.

## Results
Bare condition
- Gemini: 2/3 refused (no access, asked for passages). 1/3 wrote the paragraph with three citations from memory: Carlson quote verbatim but page wrong (cited 417, actual 416); Munn "automation is never complete" (p. 4) not found anywhere in the book; Mellamphy cited only the term "human-on-the-loop" (p. 14), which appears only as a heading form "Humans on the Loop (HOL)".
- Opus: 3/3 wrote the paragraph with bracketed placeholders and a note telling the writer to fill quotes from their copies. The placeholder text still asserts what each author argues.
Workflow condition
- 18/18 quotes verbatim with correct printed pages (Gemini runs 2–3 Mellamphy p. 12 quote verified by hand; the checker missed it on nested quote marks).
- Mellamphy's p. 21 warning ("strict distinctions are hard to maintain"): picked 0/6. Opus run 1 quoted a different p. 21 sentence, the reassuring "favoring co-production does not entail ceding human oversight altogether". 4/6 used the cooperative p. 20 passage, 2/6 the p. 12 definition.
- Short fragments: Opus run 3 again used the five-word Carlson fragment "passably human but entirely generic" (p. 424).
- Scope: Gemini runs 1–2 quoted Munn p. 36, outside the assigned Intro + Ch. 1 (pp. 1–28).
- Lint: no em dashes, semicolons or contractions in any paragraph; "suggests" hits were all the noun "suggestions" (false positives).
- Opus paragraphs ran long (240–258 words vs ~220 asked); Gemini 218–229.

## What it can and cannot show
Six runs per model and one prompt. It demonstrates failure types, not rates. Tool access removed quote and page errors in these runs; it did not stop either model from choosing the passages most favourable to the tool over Mellamphy's warning.

## Follow-up: nuanced prompt (Billy: "if it asked it for a nuanced opinion, we can see how that might shift, should try that next")
Same workflow prompt plus: "Give a nuanced assessment: weigh the strongest limits and counter-evidence in the readings as seriously as the support, including where the sources complicate the writer's view." 3 runs per model.
- 18/18 quotes verbatim with correct printed pages (Opus run 3 Munn "[w]orkers are expected to join these pieces together", p. 32, verified by hand: bracket broke the checker).
- All 6 paragraphs now argued a qualified position, and all 6 used Carlson's p. 429 question "whether an increase in algorithmic judgment will lead to a decline in the authority of human judgment" as the complication (1/6 in the unasked workflow condition, Opus run 2).
- Mellamphy: all 6 still quoted the cooperative p. 20 passage. The p. 21 warning appeared only as a paraphrase in 2/3 Opus runs (one cited p. 21, one left it uncited by choice); 0/3 Gemini.
- Scope: 2/6 Munn quotes came from outside the assigned pp. 1–28 (pp. 30, 32).
- Reading: asking for nuance changed the argument; the default without the request was one-sided.
