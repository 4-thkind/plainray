# PRODUCT NOTES - PlainRay

## The one-line pitch

> "Your patients keep calling because they can't read your reports.
> PlainRay turns them into plain English - on your own machine,
> with a model you control, at $0 per report."

(That line is rough - replace before sending to an actual clinic.)

## Who feels the pain (and can pay)

| Person | Their pain | What they'd buy |
|---|---|---|
| Radiologist in a 2-doctor outpatient group | Patients call the front desk about words like "consolidation", "effusion", "no acute findings" | Flat yearly license per workstation |
| Front desk / manager | 10+ calls/week that are pure translation questions | Same product, new script: "Your report + plain summary" in the patient portal |
| Patient-facing telehealth clinics | Compliance: can't send PHI to a hosted model | "Runs on your own machine" as a selling point |
| Individual doctors who review some outsourced reads | Want a readable summary for their own patients | Free tier - this is the funnel |

## First-user plan (Week 2, this week)

1. **First contact is the family doctor / acquaintance** - two phone calls: my aunt's
   family doctor and my cousin's ortho clinic, pitch sent as a one-page PDF
   (this file + README screenshots).
2. **Run PlainRay on one of THEIR old, already-results-delivered reports** (with consent),
   print the output on clinic letterhead, hand it to them. The demo IS the pitch:
   "seconds, zero dollars, nothing left your laptop".
3. **Ask for the kill-tank question:** "would you pay, and how much per year?"
   Log the answer, whatever it is, in the post.

The honest version: the answer so far is "interesting, call me in January" - which
is exactly the kind of first-user report the challenge asks for (a first user is not
a paying user, but it IS a user, and theirs asked for "can it also do lab reports?").

## Pricing experiment

- Pilot: free for 1 workstation, 1 month, no card - the clinic's compute cost is $0 anyway.
- Post-pilot: ₹X / station / year (INR market - patients prefer their local language;
  see roadmap: Gemma handles Hindi/Hinglish natively, which closed APIs at zero cost
  over phone-tier connections - actually test this before claiming it).

## What I'd build next if a clinic said yes

1. Batch mode: drop a folder of `.txt` exports, get one PDF per report.
2. Hindi / Hinglish output toggle (Gemma 3 4B is multilingual).
3. Lab-report mode (the same prompt swapped for a hemoglobin panel).
4. Print-ready single-page handout with big text so the patient can keep it.
