# PlainRay

**Turn radiology reports into plain-language patient explainers - entirely on the clinic's own laptop, with an open-weight model, for zero dollars per report.**

PlainRay reads a radiology report and gives the patient:

- a **plain-language summary** of what was done and what it showed (< 150 words, ~8th-grade reading level),
- a **glossary** of every medical term / abbreviation it used, translated to everyday words,
- **questions the patient can ask their doctor**, and
- a calm **urgency note** (none invented - only what the report itself says).

Powered by **Gemma 3** running locally through [Ollama](https://ollama.com). Python only, from the standard library. No pip installs, no cloud, no runtime network access.

```
ollama pull gemma3:4b
python -m plainray serve          # web UI at http://127.0.0.1:7860
python -m plainray explain --file report.txt
python -m plainray selftest       # prompts + validation + samples, no GPU needed
```

## Why local-first? (the open-innovation argument)

Radiology reports are PHI. Real clinics cannot paste them into a hosted closed API, and cloud billing makes a "nice-to-have" patient-communication feature a hard sell: a mid-size clinic reading ~120 reports a day would spend roughly **$1-3/day** on an API - for a feature that must not exist when the internet is down.

PlainRay flips that:

| | PlainRay (Gemma 3 local) | Hosted closed API |
|---|---|---|
| Cost per 1,000 reports | **$0** | tens of dollars |
| PHI leaves the machine | **never** | always |
| Works during an outage | **yes** | no |
| Fine-tune the prompt/model for your clinic | **yes, weights included** | no |

The open-weight model is not a detail of the implementation - it's **the reason this product is legal, private and free to run**. A closed model would require sending protected health information to someone else's server before it could do anything.

## Who would pay for this

Small radiology groups and outpatient imaging clinics. Patient complaints and "I didn't understand my report" are exactly the low-value calls that eat front-desk time, and "understanding the report" is a feature patients mention in satisfaction surveys. A clinic already owns the laptop; PlainRay costs nothing per report and nothing per seat, so the pitch is a flat, per-workstation license (for example a few hundred dollars a year) instead of a usage meter.

See `PRODUCT_NOTES.md` for the one-page pitch, pricing and first-user plan.

## Design notes

- **Structured output, not prose.** Gemma is asked for a fixed JSON shape; `_validate()` enforces it, drops over-length cells and picks a sane fallback for the urgency line. A one-shot "empty summary" retry is handled at the caller.
- **Readability grade is not marketing.** `readability.py` computes Flesch-Kincaid on the raw report and on the generated summary; the UI shows both so the "plain language" claim is measured, not asserted.
- **Guardrails beat style.** The system prompt forbids diagnosis, new findings and alarmism; the validator caps list lengths; the temptation to fabricate urgency is closed by instructing the model to reuse the report's own wording.
- **No pip.** Everything is stdlib (`urllib`, `http.server`). A clinic IT person can run this without touching a package manager - which is exactly how clinic machines actually work.
- **127.0.0.1 only.** The server refuses to bind to 0.0.0.0 on purpose; if you want a multi-user deployment, put it behind the network you signed off on.

## Repository

```
plainray/
  plainray/
    app.py          CLI: explain / serve / selftest
    llm.py          minimal local Ollama client (urllib only)
    prompts.py      the patient-safety prompt
    readability.py  Flesch-Kincaid (stdlib)
    server.py       local-only web UI (http.server)
  static/index.html the UI everyone uses
  samples/          three synthetic reports for testing (no PHI)
```

Run the demo:

```
ollama pull gemma3:4b          # one time, ~3 GB
python -m plainray serve
# open http://127.0.0.1:7860 - no login, no cloud, no network
```

## Status

- [x] Local inference with Gemma 3 4B (Ollama)
- [x] Web UI + CLI (JSON out)
- [x] Reading-grade drop report (raw vs plain)
- [x] Selftest that runs without a model
- [ ] Batch folder mode (`explain --folder ./reports/`)
- [ ] Optional DICOM-attachment pass (image -> MedGemma caption -> include in explainer)

## Honest notes

- Gemma 3 4B occasionally misabbreviates dense mammography terms; the glossary letting a human spot-check every translation before the printed version goes to the patient is one click per report, not one rewrite.
- Model swap is one variable (`PLAINRAY_MODEL`): pull `gemma3:12b` for the same code on a beefier box, or `medgemma` if a clinic wants the medical-tuned sibling.

## AI assistance

This project was built in one working session with an AI coding agent (design + implementation + this README), re-checked and run locally by the author. Faithful to the spirit and rules of the challenge: handouts came from a human, code from an agent.

## License

MIT - see [LICENSE](LICENSE).
