# AGENT NOTES - how PlainRay was built

One working session, one human, one AI coding agent (OpenCode + GLM). This file is
the short version of the session log, kept because (a) the Hacktoberfest challenge
invites exactly this kind of disclosure and (b) the design decisions are the useful
part, not the keystrokes.

## The brief the agent got

"Build something with open-source AI at its core that someone would actually pay
for. Small, specific, useful. It must actually run on this laptop."

## Constraints discovered first

- The author's machine: Windows 11, RTX 4060 Laptop (8 GB VRAM), 24 GB RAM.
- No Ollama installed at start - installed within the session, then pulled
  `gemma3:4b` (a ~3 GB one-time download).
- Hard rule from the challenge: brand-new repo, built inside the challenge window.
  So this is new code, not a fork of anything.

## Decisions worth keeping

1. **Stdlib-only Python.** No pip installs. The pitch is "clinic IT will actually run
   this", and the most common blocker is dependency management on locked-down
   machines. `urllib + http.server` cost nothing and removed that blocker entirely.
2. **Local via Ollama, not a hosted API.** The entire product thesis is "PHI never
   leaves the laptop". A hosted model would collapse the argument to "we're a
   chatbot with NIH-style wording".
3. **JSON-shaped output enforced in code, not trusted from the model.** `_validate()`
   rebuilds the structure, caps lengths, and refuses an empty summary. LLM output
   shape is a promise the caller makes, not a hope.
4. **Measured readability.** A Flesch-Kincaid grader runs on the raw report and on the
   generated summary; the UI shows both. "Plain language" is a claim you can test.
5. **The prompt is the product.** Anti-diagnosis, no invented findings, calm urgency
   wording, glossary mandatory. Most of the safety work lives in `prompts.py` where a
   clinic can read it in plain text.

## What was hard

- Gemma 3 4B sometimes packs "no acute findings" into cheerful-sounding paragraphs -
  the "calm, not reassuring" line in the system prompt came from watching that happen.
- Mammography abbreviations (ACR, MLO, CC) are the weakest spot of a 4B model; the
  glossary exists so a human can see each translation before it ships.

## Timeline

| Time | Done |
|---|---|
| 0:00 | Repo created, rules re-read (new project inside the window; AI allowed) |
| 0:10 | Ollama installed, `gemma3:4b` pull started in background |
| 0:10-0:40 | Code written while the model was still downloading |
| 0:40 | Selftest green (prompts / validator / readability on 3 synthetic reports) |
| 0:45 | First real runs against Gemma 3 4B locally, prompt iterations |
| 1:00 | UI demo captured, post written, submitted |

## Honest gaps

- No real patient data was ever used - samples are synthetic.
- The "first user" run with an actual clinic is planned, not yet done.
