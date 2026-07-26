# DSA Practice Arena

Timed, exam-like DSA practice in **Python**, driven by [Claude Code](https://claude.com/claude-code).

Claude acts as the **question setter and judge** — it invents a fresh problem in
certification-exam style, silently builds and verifies 10 weighted hidden test cases, starts
a 45-minute clock, and scores you. It won't tell you which pattern the problem is, because
the real exam doesn't either. `judge.py` is a plain local runner — no accounts, no network,
no dependencies beyond Python 3.8+.

Built for **SWPCT-style** tests (medium difficulty, one concept per question, constraints
tight enough to force a single technique), but the drill scope is just a table in
[CLAUDE.md](CLAUDE.md) — edit it to match whatever test you're preparing for.

## Quick start

```bash
git clone <your-fork-url>
cd dsa-practice-arena
claude                       # open Claude Code in this folder
```

Then either ask Claude for a problem, or solve one from the bundled bank:

```bash
python judge.py random       # pick a random unattempted problem, start the 45-min clock
python judge.py show         # print the statement
#   ... write your code in the problem's solution.py ...
python judge.py run          # check the 2 visible samples (with diffs)
python judge.py submit       # score against the 10 hidden cases, weighted /100
```

Or in the Claude Code session: **"give me a sliding window question"** → Claude writes a
brand-new problem with fresh hidden tests. Then say **run** and **submit**; Claude executes
the judge, reports your score, and diagnoses failures without handing you the answer.

13 ready-made problems ship in [problems/](problems/) so you can practice immediately.

## Two modes

**Single question** — 45-minute budget, one problem.

```bash
python judge.py random [topic]   # random problem (optionally filter by folder name)
python judge.py show [problem]   # print the statement
python judge.py run [problem]    # 2 samples, with diffs
python judge.py submit [problem] # 10 hidden cases, weighted score /100
python judge.py start / hold     # (re)start or pause the clock
python judge.py status / time    # current problem, elapsed / remaining
python judge.py list             # whole bank, with clean/attempted state
python judge.py reset [problem]  # restore solution.py to the starter template
```

**Contest** — several problems on one shared clock, like the real thing.

```bash
python judge.py contest new 3 150   # random 3-problem set, 150 min, 100 marks (30/30/40)
python judge.py contest start       # start the shared clock
python judge.py run p1              # problems are addressed p1 / p2 / p3
python judge.py submit p2
python judge.py contest score       # every problem + grand total, pass/fail at 50%
python judge.py contest status      # overview + remaining time
```

## Scoring

Hidden cases are banded and weighted, so a solution that is correct but too slow still
scores partial marks — exactly like the real exam:

| Cases | Band              | Marks each | Subtotal |
| ----- | ----------------- | ---------- | -------- |
| 1–4   | small / edge      | 5          | 20       |
| 5–6   | medium            | 10         | 20       |
| 7–8   | large / stress    | 15         | 30       |
| 9–10  | adversarial       | 15         | 30       |

Verdicts: **PASS** / **FAIL** / **TLE** (over 3s, tune with `DSA_TIMEOUT`) / **RE** (crash).
Trailing whitespace is forgiven. In contest mode the same 5/10/15 shape is rescaled to each
problem's share of the 100 marks.

## Layout

```
.
├── CLAUDE.md          # session rules for Claude — the authoritative spec
├── judge.py           # runner / scorer (no dependencies)
├── templates/         # solution.py starter, problem.md skeleton, scores.md header
├── contest/           # active contest definition (generated)
└── problems/
    └── YYYY-MM-DD_<story-title>_NN/
        ├── problem.md
        ├── sample_input_1.txt / sample_output_1.txt
        ├── sample_input_2.txt / sample_output_2.txt
        ├── hidden/    # input_1..10.txt + expected output_1..10.txt
        └── solution.py    # starter template — you write this
```

Problem folders are named after the **story**, never the technique, so the path itself
can't leak the pattern.

## Notes

- Your `scores.md` log, timers, `problems/.current`, and anything in `reference/` are
  git-ignored — practice state stays local, so pulling updates never clobbers your work.
- `solution.py` files **are** tracked (they ship as the starter template), so your own
  solutions will show up as local modifications. That's expected; `git stash` or just leave
  them.
- Hidden expected outputs are plain text files in the repo. Nothing stops you from opening
  them — the honour system does the rest. Problems Claude generates for you fresh in a
  session are the real test of whether you can solve cold.

## License

MIT — see [LICENSE](LICENSE).
