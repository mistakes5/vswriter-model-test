# VSwriter model test

Prompts, model outputs and scores from a small test run for an essay on AI-assisted writing (POLISCI 3390F, The Politics of Artificial Intelligence). The prototype the essay describes is at https://github.com/mistakes5/writer-ide.

## Question

When a model is asked to write a paragraph from a writer's own interview answers, what changes if it can open the full readings, and what changes if it is asked for nuance?

## Design (round 2, the run the essay reports)

- **Models:** Gemini 4 Neon and Claude Opus 5.5, both at medium reasoning effort.
- **Input:** the same four interview answers (`round2/notes.txt`) and the same request for a 220-word paragraph quoting Mellamphy (2021), Carlson (2015) and Munn (2022).
- **Conditions,** three runs per model in each (18 runs):
  - `bare`: no files or tools (`round2/prompt-bare.txt`).
  - `workflow`: the full readings in a folder, with file-search tools; the model finds its own passages and cites printed pages (`round2/prompt-workflow.txt`).
  - `nuanced`: the workflow prompt plus one sentence asking for a nuanced assessment (`round2/prompt-nuanced.txt`).
- **Scoring:** `scripts/score.py` searches each quotation in the reading text and maps PDF pages to printed pages. Quotations the checker missed because of nested quotation marks or brackets were verified by hand. Scores are in `round2/scores.json` and the write-up is `round2/RESULTS.md`.

## Results

| Condition | Quotations | Argument |
|---|---|---|
| Bare | Gemini declined in 2 of 3 runs; its third cited a Munn quotation that is not in the book and a wrong Carlson page. Opus left bracketed placeholders in 3 of 3. | n/a |
| Workflow | 18 of 18 verbatim with correct printed pages. | 0 of 6 quoted Mellamphy's warning (p. 21) that the in-the-loop and on-the-loop distinction is hard to maintain; 1 of 6 used Carlson's question about the authority of human judgment (p. 429). |
| Nuanced | 18 of 18 verbatim with correct printed pages. | 6 of 6 used Carlson's question. Mellamphy's warning was still never quoted; 2 of 6 paraphrased it. |

## Limits

- Eighteen runs and one prompt per condition. The test shows kinds of failure and cannot establish how often they occur.
- The two models ran through different command-line tools. Opus was meant to run through the same tool as Gemini, but those six runs failed on a quota limit, so Opus was rerun through the Claude Code CLI with read-only tools.
- Round 1 (`round1/`) was an earlier single-run pilot at low reasoning effort. Its workflow prompt pasted the exact excerpts and pages, so its quotation accuracy was supplied by the prompt. The essay does not rely on it.

## What is not here

The reading files are copyrighted and are not included. To rerun the workflow conditions, place your own page-split text copies in a `readings/` folder as `Mellamphy-2021.md`, `Carlson-2015.md` and `Munn-2022.md`. Error logs from the runs are omitted because they only contained sign-in notices. Local file paths inside the model outputs were shortened to `./...`; nothing else in the outputs was edited.

## Readings

- Carlson, Matt. 2015. "The Robotic Reporter: Automated journalism and the redefinition of labor, compositional forms, and journalistic authority." *Digital Journalism* 3(3): 416–431.
- Mellamphy, Nandita Biswas. 2021. "Humans 'in the Loop'?: Human-Centrism, Posthumanism, and AI." *Nature and Culture* 16(1): 11–27.
- Munn, Luke. 2022. *Automation is a Myth*. Stanford: Stanford University Press.
