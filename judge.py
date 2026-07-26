#!/usr/bin/env python3
"""
DSA practice judge  (see CLAUDE.md for the full session workflow).

Layout per problem folder  problems/<YYYY-MM-DD_story_NN>/ :
    problem.md
    sample_input_1.txt / sample_output_1.txt
    sample_input_2.txt / sample_output_2.txt
    hidden/input_1.txt ... input_10.txt  +  output_1.txt ... output_10.txt
    weights.txt            <- optional: 10 ints (marks per hidden case); default 5/5/5/5/10/10/15/15/15/15
    solution.py            <- you write this (starts as templates/solution.py)

Single-question mode:
    python judge.py random [topic]      # pick a random problem, set it current, start the clock
    python judge.py show [problem]      # print the problem statement
    python judge.py run [problem]       # run solution.py vs the 2 samples (shows diffs)
    python judge.py submit [problem]    # run vs 10 hidden cases, weighted score
    python judge.py start [problem]     # (re)start the 45-minute clock
    python judge.py hold [problem]      # pause/clear the clock
    python judge.py status              # current problem + timer
    python judge.py time                # elapsed / remaining minutes
    python judge.py list                # all problems, with attempted/clean state
    python judge.py reset [problem]     # restore solution.py to the starter template

Contest mode:
    python judge.py contest new [count] [minutes]  # random set from the bank (default 3, 50 min each)
    python judge.py contest start                  # start the shared contest clock
    python judge.py contest status                 # overview + shared timer
    python judge.py contest score                  # score every contest problem + grand total
    python judge.py contest stop                   # stop/clear the contest clock

Authoring (used when a new problem is generated):
    python judge.py new <story-slug>    # scaffold a problem folder from templates/

[problem] may be a folder slug, or (during a contest) p1/p2/p3.
If omitted, the slug in problems/.current is used.

Env:
    DSA_TIMEOUT   per-case time limit, seconds (default 3)
    DSA_SOLUTION  override path to the solution file
"""
import sys
import os
import random
import shutil
import subprocess
import time
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS = os.path.join(ROOT, "problems")
TEMPLATES = os.path.join(ROOT, "templates")
SOLUTION_TEMPLATE = os.path.join(TEMPLATES, "solution.py")
PROBLEM_TEMPLATE = os.path.join(TEMPLATES, "problem.md")
CURRENT_FILE = os.path.join(PROBLEMS, ".current")
CONTEST_DIR = os.path.join(ROOT, "contest")
CONTEST_META = os.path.join(CONTEST_DIR, "meta.txt")
CONTEST_STARTED = os.path.join(CONTEST_DIR, ".started_at")
TIMEOUT = float(os.environ.get("DSA_TIMEOUT", "3"))
TIME_LIMIT_MIN = 45

# default weighted marks per hidden case (index 1..10) -> total 100
WEIGHTS = {1: 5, 2: 5, 3: 5, 4: 5, 5: 10, 6: 10, 7: 15, 8: 15, 9: 15, 10: 15}
BAND = {1: "small", 2: "small", 3: "edge", 4: "edge", 5: "medium", 6: "medium",
        7: "large", 8: "large", 9: "adversarial", 10: "adversarial"}

if os.name == "nt":
    os.system("")  # enable ANSI colors on Windows terminals
# statements and test data contain unicode (math and arrow glyphs); don't let a
# cp1252 console kill the run
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; C = "\033[96m"; B = "\033[1m"; D = "\033[2m"; X = "\033[0m"


def die(msg):
    print(f"{R}error:{X} {msg}")
    sys.exit(1)


# ---------- contest ----------
def contest_meta():
    if not os.path.exists(CONTEST_META):
        return None
    lines = [l.strip() for l in open(CONTEST_META, encoding="utf-8").read().splitlines() if l.strip()]
    if not lines:
        return None
    name, limit = lines[0].split("|")
    probs = []
    for l in lines[1:]:
        slug, total = l.split("|")
        probs.append((slug, int(total)))
    return {"name": name, "limit": float(limit), "problems": probs}


def contest_elapsed():
    if not os.path.exists(CONTEST_STARTED):
        return None
    try:
        started = float(open(CONTEST_STARTED, encoding="utf-8").read().strip())
    except ValueError:
        return None
    return (time.time() - started) / 60.0


def resolve_slug(arg):
    if arg is None:
        return get_current()
    a = arg.lower()
    meta = contest_meta()
    if meta:
        order = [p[0] for p in meta["problems"]]
        for i in range(len(order)):
            if a in (f"p{i + 1}", str(i + 1)):
                return order[i]
    return arg


# ---------- problem access ----------
def all_slugs():
    if not os.path.isdir(PROBLEMS):
        return []
    return sorted(d for d in os.listdir(PROBLEMS)
                  if os.path.isdir(os.path.join(PROBLEMS, d)))


def get_current():
    if not os.path.exists(CURRENT_FILE):
        die("no current problem set. Ask for a question, or run: python judge.py random")
    with open(CURRENT_FILE, encoding="utf-8") as f:
        slug = f.read().strip()
    if not slug:
        die("no current problem set. Ask for a question, or run: python judge.py random")
    return slug


def set_current(slug):
    os.makedirs(PROBLEMS, exist_ok=True)
    with open(CURRENT_FILE, "w", encoding="utf-8") as f:
        f.write(slug)


def problem_dir(slug):
    d = os.path.join(PROBLEMS, slug)
    if not os.path.isdir(d):
        die(f"problem '{slug}' not found in {PROBLEMS}")
    return d


def solution_path(slug):
    env = os.environ.get("DSA_SOLUTION")
    if env:
        return env
    return os.path.join(problem_dir(slug), "solution.py")


def is_untouched(slug):
    """True if solution.py is still byte-identical to the starter template."""
    sol = solution_path(slug)
    if not (os.path.exists(sol) and os.path.exists(SOLUTION_TEMPLATE)):
        return False
    with open(sol, "rb") as a, open(SOLUTION_TEMPLATE, "rb") as b:
        return a.read() == b.read()


def warn_if_untouched(slug):
    if is_untouched(slug):
        print(f"{Y}note:{X} {D}solution.py is still the starter template - write your solution first.{X}\n")


def contest_total_for(slug):
    """Marks this problem is worth in the active contest, or None if not in one."""
    meta = contest_meta()
    if not meta:
        return None
    for s, total in meta["problems"]:
        if s == slug:
            return total
    return None


def load_weights(slug):
    """Per-case marks: contest share if the problem is in the active contest,
    else weights.txt if the author supplied one, else the default /100 spread."""
    total = contest_total_for(slug)
    if total is not None:
        w = scaled_weights(total)
        return {i + 1: w[i] for i in range(10)}
    wf = os.path.join(problem_dir(slug), "weights.txt")
    if os.path.exists(wf):
        vals = open(wf, encoding="utf-8").read().split()
        if len(vals) >= 10:
            return {i + 1: int(vals[i]) for i in range(10)}
    return dict(WEIGHTS)


def scaled_weights(total):
    """Spread `total` marks over the 10 bands, keeping the default 5/10/15 shape."""
    base = [WEIGHTS[i] for i in range(1, 11)]
    w = [max(1, int(round(b * total / 100.0))) for b in base]
    diff = total - sum(w)
    order = sorted(range(10), key=lambda i: -base[i])
    i = 0
    while diff != 0 and i < 1000:
        j = order[i % 10]
        if diff > 0:
            w[j] += 1
            diff -= 1
        elif w[j] > 1:
            w[j] -= 1
            diff += 1
        i += 1
    return w


def sample_cases(slug):
    d = problem_dir(slug)
    cases = []
    for i in (1, 2):
        ip = os.path.join(d, f"sample_input_{i}.txt")
        op = os.path.join(d, f"sample_output_{i}.txt")
        if os.path.exists(ip) and os.path.exists(op):
            cases.append((str(i), ip, op))
    return cases


def hidden_cases(slug):
    d = os.path.join(problem_dir(slug), "hidden")
    if not os.path.isdir(d):
        return []
    cases = []
    for i in range(1, 11):
        ip = os.path.join(d, f"input_{i}.txt")
        op = os.path.join(d, f"output_{i}.txt")
        if os.path.exists(ip) and os.path.exists(op):
            cases.append((i, ip, op))
    return cases


def normalize(text):
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_case(sol, in_path):
    with open(in_path, encoding="utf-8") as f:
        stdin = f.read()
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, sol],
            input=stdin, capture_output=True, text=True, timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return {"verdict": "TLE", "elapsed": TIMEOUT, "stdout": "", "stderr": ""}
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        return {"verdict": "RE", "elapsed": elapsed, "stdout": proc.stdout, "stderr": proc.stderr}
    return {"verdict": "OK", "elapsed": elapsed, "stdout": proc.stdout, "stderr": proc.stderr}


def show_diff(expected, got, in_text):
    print(f"    {D}input:{X}")
    for ln in in_text.rstrip("\n").split("\n")[:15]:
        print(f"      {ln}")
    print(f"    {D}expected:{X}")
    for ln in expected.split("\n")[:15]:
        print(f"      {G}{ln}{X}")
    print(f"    {D}your output:{X}")
    for ln in (got.split("\n")[:15] if got.strip() else ["(empty)"]):
        print(f"      {R}{ln}{X}")


# ---------- timers ----------
def started_path(slug):
    return os.path.join(problem_dir(slug), ".started_at")


def elapsed_minutes(slug):
    p = started_path(slug)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        try:
            started = float(f.read().strip())
        except ValueError:
            return None
    return (time.time() - started) / 60.0


def print_timer(slug):
    meta = contest_meta()
    if meta and any(slug == p[0] for p in meta["problems"]):
        mins = contest_elapsed()
        if mins is None:
            print(f"{D}[contest] timer not started - python judge.py contest start{X}")
            return
        limit = meta["limit"]
        left = limit - mins
        col = G if left > 30 else (Y if left > 10 else R)
        tag = "" if left >= 0 else "  OVER TIME!"
        print(f"{col}[contest timer] {mins:.1f} / {limit:.0f} min  ({left:+.1f} min left){tag}{X}")
        return
    mins = elapsed_minutes(slug)
    if mins is None:
        return
    left = TIME_LIMIT_MIN - mins
    col = G if left > 15 else (Y if left > 5 else R)
    tag = "" if left >= 0 else "  OVER TIME!"
    print(f"{col}[timer] {mins:.1f} min elapsed / {TIME_LIMIT_MIN} min target"
          f"  ({left:+.1f} min left){tag}{X}")


def start_clock(slug):
    with open(started_path(slug), "w", encoding="utf-8") as f:
        f.write(str(time.time()))
    print(f"{B}{C}clock started:{X} {slug}  {D}({TIME_LIMIT_MIN} min budget){X}")


def hold_clock(slug):
    p = started_path(slug)
    mins = elapsed_minutes(slug)
    if os.path.exists(p):
        os.remove(p)
    if mins is None:
        print(f"{D}no clock was running for {slug}{X}")
    else:
        print(f"clock held for {slug} {D}(was at {mins:.1f} min){X}")
    print(f"{D}resume with: python judge.py start{X}")


# ---------- single-question mode ----------
def pick_random(topic=None):
    slugs = all_slugs()
    if topic:
        t = topic.lower()
        slugs = [s for s in slugs if t in s.lower()]
        if not slugs:
            die(f"no problem folder matches '{topic}'")
    if not slugs:
        die("no problems in the bank yet - ask for a question to be generated")
    # problems reserved by an active contest are scored on the shared clock, so
    # keep them out of single-question practice unless nothing else is left
    meta = contest_meta()
    if meta:
        reserved = {s for s, _t in meta["problems"]}
        slugs = [s for s in slugs if s not in reserved] or slugs
    fresh = [s for s in slugs if is_untouched(s)]
    pool = fresh or slugs
    slug = random.choice(pool)
    set_current(slug)
    print(f"\n{B}{C}== RANDOM QUESTION =={X}")
    if not fresh:
        print(f"{D}(every problem in the bank has been attempted - reusing one){X}")
    print(f"  {B}{slug}{X}")
    print(f"  {D}statement:{X} problems/{slug}/problem.md")
    print(f"  {D}your code:{X} problems/{slug}/solution.py")
    start_clock(slug)
    print(f"{D}python judge.py show   # print the statement{X}")
    print(f"{D}python judge.py run    # check the 2 samples{X}\n")


def show_problem(slug):
    p = os.path.join(problem_dir(slug), "problem.md")
    if not os.path.exists(p):
        die(f"no problem.md for '{slug}'")
    with open(p, encoding="utf-8") as f:
        print("\n" + f.read())
    print_timer(slug)
    print()


def reset_solution(slug):
    if not os.path.exists(SOLUTION_TEMPLATE):
        die(f"missing template: {SOLUTION_TEMPLATE}")
    sol = solution_path(slug)
    if is_untouched(slug):
        print(f"{D}{slug}/solution.py is already the starter template{X}")
        return
    shutil.copyfile(SOLUTION_TEMPLATE, sol)
    print(f"reset {D}problems/{slug}/solution.py{X} to the starter template")


def new_problem(slug):
    if not slug:
        die("usage: python judge.py new <story-slug>   e.g. new watchtower-signals")
    if not slug[:4].isdigit():
        n = 1
        base = f"{date.today().isoformat()}_{slug}"
        while os.path.isdir(os.path.join(PROBLEMS, f"{base}_{n:02d}")):
            n += 1
        slug = f"{base}_{n:02d}"
    d = os.path.join(PROBLEMS, slug)
    if os.path.isdir(d):
        die(f"'{slug}' already exists")
    os.makedirs(os.path.join(d, "hidden"))
    shutil.copyfile(PROBLEM_TEMPLATE, os.path.join(d, "problem.md"))
    shutil.copyfile(SOLUTION_TEMPLATE, os.path.join(d, "solution.py"))
    for i in (1, 2):
        for kind in ("input", "output"):
            open(os.path.join(d, f"sample_{kind}_{i}.txt"), "w", encoding="utf-8").close()
    set_current(slug)
    print(f"scaffolded {B}problems/{slug}{X}  {D}(now the current problem){X}")
    print(f"{D}fill in problem.md, the 2 samples, and hidden/input_1..10 + output_1..10{X}")


def run_samples(slug):
    cases = sample_cases(slug)
    if not cases:
        die(f"no sample cases found for '{slug}'")
    sol = solution_path(slug)
    if not os.path.exists(sol):
        die(f"solution file not found: {sol}")

    print(f"\n{B}{C}== RUN - sample cases =={X}  {D}problem: {slug}{X}\n")
    warn_if_untouched(slug)
    passed = 0
    slowest = 0.0
    for name, ip, op in cases:
        with open(op, encoding="utf-8") as f:
            expected = f.read()
        with open(ip, encoding="utf-8") as f:
            in_text = f.read()
        res = run_case(sol, ip)
        slowest = max(slowest, res["elapsed"])
        if res["verdict"] == "TLE":
            print(f"  {R}[TLE]{X} sample {name}  {D}> {TIMEOUT:.1f}s{X}")
        elif res["verdict"] == "RE":
            print(f"  {R}[RE ]{X} sample {name}  {D}runtime error{X}")
            for ln in res["stderr"].strip().split("\n")[-5:]:
                print(f"      {R}{ln}{X}")
        elif normalize(res["stdout"]) == normalize(expected):
            print(f"  {G}[PASS]{X} sample {name}  {D}{res['elapsed']*1000:6.0f} ms{X}")
            passed += 1
        else:
            print(f"  {R}[FAIL]{X} sample {name}  {D}wrong answer{X}")
            show_diff(normalize(expected), normalize(res["stdout"]), in_text)
    print()
    col = G if passed == len(cases) else R
    print(f"{B}{col}{passed}/{len(cases)} samples passed{X}")
    if passed == len(cases):
        print(f"{D}Samples good. Say `submit` to score against the 10 hidden cases.{X}")
    print(f"{D}slowest sample: {slowest*1000:.0f} ms (limit {TIMEOUT:.1f}s){X}")
    print_timer(slug)
    print()


def score_hidden(slug, verbose=True):
    """Run the 10 hidden cases. Returns (score, total, passed, slowest)."""
    cases = hidden_cases(slug)
    if len(cases) < 10:
        die(f"expected 10 hidden cases for '{slug}', found {len(cases)}")
    sol = solution_path(slug)
    if not os.path.exists(sol):
        die(f"solution file not found: {sol}")

    weights = load_weights(slug)
    total = sum(weights.values())
    score = 0
    passed = 0
    slowest = 0.0
    for idx, ip, op in cases:
        with open(op, encoding="utf-8") as f:
            expected = f.read()
        res = run_case(sol, ip)
        slowest = max(slowest, res["elapsed"])
        w = weights[idx]
        tag = f"{BAND[idx]:<11} {w:>2} mk"
        if res["verdict"] == "TLE":
            if verbose:
                print(f"  {R}[TLE ]{X} case {idx:<2} {D}{tag}  > {TIMEOUT:.1f}s{X}")
        elif res["verdict"] == "RE":
            if verbose:
                print(f"  {R}[RE  ]{X} case {idx:<2} {D}{tag}  runtime error{X}")
        elif normalize(res["stdout"]) == normalize(expected):
            if verbose:
                print(f"  {G}[PASS]{X} case {idx:<2} {D}{tag}  {res['elapsed']*1000:5.0f} ms{X}")
            score += w
            passed += 1
        elif verbose:
            print(f"  {R}[FAIL]{X} case {idx:<2} {D}{tag}  wrong answer{X}")
    return score, total, passed, slowest


def submit(slug):
    weights = load_weights(slug)
    print(f"\n{B}{C}== SUBMIT - hidden cases =={X}  {D}problem: {slug}  (out of {sum(weights.values())}){X}\n")
    warn_if_untouched(slug)
    score, total, passed, slowest = score_hidden(slug)
    print()
    col = G if passed == 10 else (Y if passed > 0 else R)
    print(f"{B}{col}SCORE: {score}/{total}   ({passed}/10 cases passed){X}")
    print(f"{D}slowest case: {slowest*1000:.0f} ms (limit {TIMEOUT:.1f}s){X}")
    print_timer(slug)
    print()


def list_problems():
    slugs = all_slugs()
    cur = None
    if os.path.exists(CURRENT_FILE):
        with open(CURRENT_FILE, encoding="utf-8") as f:
            cur = f.read().strip()
    meta = contest_meta()
    in_contest = {}
    if meta:
        for i, (s, _t) in enumerate(meta["problems"], 1):
            in_contest[s] = f"P{i}"
    print(f"\n{B}Problems:{X}")
    if not slugs:
        print(f"  {D}(none yet - ask for a question){X}")
    for s in slugs:
        mark = f" {G}<- current{X}" if s == cur else ""
        state = f"{D}[clean]{X}" if is_untouched(s) else f"{Y}[attempted]{X}"
        ctag = f" {C}({in_contest[s]}){X}" if s in in_contest else ""
        print(f"  - {s:<40} {state}{ctag}{mark}")
    print()


# ---------- contest mode ----------
def contest_new(count_arg, minutes_arg):
    count = int(count_arg) if count_arg else 3
    if count < 1:
        die("contest needs at least 1 problem")
    slugs = all_slugs()
    if len(slugs) < count:
        die(f"only {len(slugs)} problems in the bank, need {count}")
    fresh = [s for s in slugs if is_untouched(s)]
    pool = fresh if len(fresh) >= count else slugs
    chosen = random.sample(pool, count)
    minutes = float(minutes_arg) if minutes_arg else count * 50.0

    # marks: 100 total on clean multiples of 5, last problem carries the rest
    # (3 -> 30/30/40, 2 -> 50/50, 4 -> 25 each)
    base = max(5, (100 // count) // 5 * 5)
    totals = [base] * (count - 1) + [100 - base * (count - 1)]

    os.makedirs(CONTEST_DIR, exist_ok=True)
    counter = os.path.join(CONTEST_DIR, ".count")
    n = 1
    if os.path.exists(counter):
        try:
            n = int(open(counter, encoding="utf-8").read().strip()) + 1
        except ValueError:
            n = 1
    open(counter, "w", encoding="utf-8").write(str(n))
    name = f"Mock Contest {n:02d}"
    with open(CONTEST_META, "w", encoding="utf-8") as f:
        f.write(f"{name}|{minutes:.0f}\n")
        for slug, total in zip(chosen, totals):
            f.write(f"{slug}|{total}\n")

    # per-case marks are derived from the contest share at scoring time
    # (load_weights); nothing in the problem bank is modified. Just clear any
    # stale single-question clock so each plays as a fresh contest problem.
    for slug in chosen:
        sp = started_path(slug)
        if os.path.exists(sp):
            os.remove(sp)
    set_current(chosen[0])
    if os.path.exists(CONTEST_STARTED):
        os.remove(CONTEST_STARTED)

    print(f"\n{B}{C}{name} built:{X} {count} problems, {minutes:.0f} min, 100 marks\n")
    for i, (slug, total) in enumerate(zip(chosen, totals), 1):
        print(f"  {B}P{i}{X} {total:>3} mk   {D}problems/{slug}/{X}")
    print(f"\n{D}python judge.py contest start   # start the shared clock{X}")
    print(f"{D}python judge.py run p1 / submit p2 / contest score{X}\n")


def contest_score():
    meta = contest_meta()
    grand_total = sum(p[1] for p in meta["problems"])
    print(f"\n{B}{C}== CONTEST SCORE =={X}  {D}{meta['name']}{X}\n")
    grand = 0
    passed_all = 0
    for i, (slug, _total) in enumerate(meta["problems"], 1):
        print(f"{B}P{i}{X}  {D}{slug}{X}")
        score, total, passed, slowest = score_hidden(slug)
        col = G if passed == 10 else (Y if passed > 0 else R)
        print(f"     {col}{score}/{total}{X}  {D}({passed}/10 cases, slowest {slowest*1000:.0f} ms){X}\n")
        grand += score
        passed_all += passed
    threshold = grand_total // 2
    verdict = f"{G}PASSED{X}" if grand >= threshold else f"{R}BELOW THRESHOLD{X}"
    print(f"{B}GRAND TOTAL: {grand}/{grand_total}{X}   {D}({passed_all}/{10 * len(meta['problems'])} cases){X}")
    print(f"  {verdict} {D}(threshold {threshold}, {grand - threshold:+d}){X}")
    mins = contest_elapsed()
    if mins is not None:
        print(f"{D}time used: {mins:.1f} / {meta['limit']:.0f} min{X}")
    print()


def contest_cmd(sub, arg2=None, arg3=None):
    if sub == "new":
        contest_new(arg2, arg3)
        return
    meta = contest_meta()
    if not meta:
        die("no contest configured - build one with: python judge.py contest new")
    if sub == "start":
        os.makedirs(CONTEST_DIR, exist_ok=True)
        open(CONTEST_STARTED, "w", encoding="utf-8").write(str(time.time()))
        print(f"\n{B}{C}Contest started:{X} {meta['name']}  {D}({meta['limit']:.0f} min total){X}")
        for i, (slug, total) in enumerate(meta["problems"], 1):
            print(f"  {B}P{i}{X} ({total} mk)  {D}{slug}{X}")
        print(f"{D}run/submit with p1/p2/p3, e.g.  python judge.py submit p2{X}\n")
        return
    if sub == "stop":
        if os.path.exists(CONTEST_STARTED):
            os.remove(CONTEST_STARTED)
        print("contest timer stopped")
        return
    if sub == "score":
        contest_score()
        return
    # status / overview
    grand = sum(p[1] for p in meta["problems"])
    print(f"\n{B}{C}{meta['name']}{X}  {D}{grand} marks / {meta['limit']:.0f} min{X}")
    for i, (slug, total) in enumerate(meta["problems"], 1):
        state = f"{D}[clean]{X}" if is_untouched(slug) else f"{Y}[attempted]{X}"
        print(f"  {B}P{i}{X}  {total:>3} mk  {state}  {D}{slug}{X}")
    mins = contest_elapsed()
    if mins is None:
        print(f"{D}timer not started - python judge.py contest start{X}")
    else:
        left = meta["limit"] - mins
        col = G if left > 30 else (Y if left > 10 else R)
        tag = "" if left >= 0 else "  OVER TIME!"
        print(f"{col}[contest timer] {mins:.1f} / {meta['limit']:.0f} min  ({left:+.1f} min left){tag}{X}")
    print()


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    a1 = args[1] if len(args) > 1 else None
    a2 = args[2] if len(args) > 2 else None
    if cmd == "run":
        run_samples(resolve_slug(a1))
    elif cmd == "submit":
        submit(resolve_slug(a1))
    elif cmd == "time":
        print_timer(resolve_slug(a1))
    elif cmd == "status":
        s = resolve_slug(a1) if a1 else get_current()
        print(f"{B}current problem:{X} {s}")
        print_timer(s)
    elif cmd == "list":
        list_problems()
    elif cmd in ("random", "pick"):
        pick_random(a1)
    elif cmd == "show":
        show_problem(resolve_slug(a1))
    elif cmd == "start":
        start_clock(resolve_slug(a1))
    elif cmd in ("hold", "pause"):
        hold_clock(resolve_slug(a1))
    elif cmd == "reset":
        reset_solution(resolve_slug(a1))
    elif cmd == "new":
        new_problem(a1)
    elif cmd == "contest":
        contest_cmd(a1 or "status", a2, args[3] if len(args) > 3 else None)
    else:
        print(__doc__)
        die(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
