# 🍎 Your Nutritionist

**A private, evidence-based nutrition calculator.** Answer a few questions and get ~42 personalised daily targets — calories, macros, limits, food groups, and 21 vitamins and minerals — each with the research rule behind it.

**→ [Open the calculator](https://meni-gottesman.github.io/nutritionist/)**
**→ [Read the full evidence guide](https://meni-gottesman.github.io/nutritionist/Healthiest-Diet-Guide.html)**

Everything runs in your browser. No account, no server, no upload — the page is static and the math is local.

---

## What makes it different

**Every number is checked.** The engine is differentially tested against an independent, separately-written evidence oracle encoded from the primary sources (NIH ODS, DGA 2025–2030, WHO, AHA, KDIGO, NASEM/IOM DRIs). The current build passes **0 violations across 12,104,478 profiles** — every discrete branch (all 2,048 condition combinations, every age, every life stage) plus a dense sweep of the continuous inputs.

**Targets carry a timescale.** Most tools imply everything is a daily goal. Here each target shows the horizon it's genuinely best judged over — protein **per meal**, calories as a **weekly average**, most vitamins and minerals **monthly+** because your body buffers them for weeks. You can browse the whole set grouped by timescale.

**Energy is additive, not double-counted.** Daily activity (your job and lifestyle) and logged workouts are separate inputs — `BMR × activity + workout kcal` — because the classic 1.2–1.9 multipliers already bake exercise in, and adding workouts on top of those inflates the estimate.

**Rates are honest.** Fat-loss pace is sized as a percentage of body weight per week (0.5 / 0.75 / 1.0%), genuinely capped at 1%, and the displayed weekly rate is recomputed from your *actual* deficit after the calorie floor applies — so the number on screen is never a claim the math isn't making.

**Built to be safe.** Maintain is the default goal. Under-18s are shown maintenance. Low BMI or very low body fat blocks a deficit. Pregnancy, kidney disease, and GLP-1 medication override the usual rules. Body fat % is framed as one input to the math, not a score.

---

## Structure

```
index.html                  the calculator (generated — do not edit by hand)
Healthiest-Diet-Guide.html  the full guide, 22 sections, ~360 cited sources (generated)
Healthiest-Diet-Guide.md    the assembled guide source (generated from sections/)
sections/                   the guide's source markdown, one file per section
src/app.template.html       the calculator's UI shell
build_html.py               builds the guide + the engine
build_app.py                injects the engine into the UI shell → index.html
```

## Building

```bash
python3 build_html.py   # assembles the guide and the calculator engine
python3 build_app.py    # injects that engine into the UI → index.html
```

`build_app.py` never reimplements any math. It lifts the engine `<script>` verbatim out of the built guide and injects it into the UI shell, then **re-extracts it from its own output and compares SHA-256** — the build fails if the shipped engine is not byte-identical to the verified one. The UI is free to change; the numbers are not.

To edit the guide, change the files in `sections/`, reassemble, then rebuild:

```bash
python3 -c "import glob;parts=[open(f).read().rstrip(chr(10)) for f in sorted(glob.glob('sections/*.md'))];open('Healthiest-Diet-Guide.md','w').write((chr(10)*3).join(parts)+chr(10))"
python3 build_html.py && python3 build_app.py
```

---

## Disclaimer

Educational, not medical advice. It gives a near-optimal *starting* target set, not a validated meal plan. Accuracy is bounded by your inputs — body-fat % and workout calories are estimates — and by individual variation no calculator can see. For pregnancy, medical conditions, medications, or any history of disordered eating, work with a doctor or registered dietitian.

## License

MIT — see [LICENSE](LICENSE).
