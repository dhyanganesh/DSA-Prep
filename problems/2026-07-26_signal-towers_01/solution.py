"""
Contest solution template.

Read from stdin, write to stdout. Only stdout is judged: no prompts, and no
debug prints on stdout (use sys.stderr for tracing).

    python judge.py run       # 2 visible samples, with diffs
    python judge.py submit    # 10 hidden cases, weighted score /100
"""
import sys


def solve(lines):
    """Return the answer: a string, a number, or a list of output lines.

    `lines` is stdin split into stripped lines. Common shapes:

        n = int(lines[0])                          # single count
        a = list(map(int, lines[1].split()))       # one array on one line
        r, c = map(int, lines[0].split())          # grid dimensions
        grid = lines[1:1 + r]                      # grid rows as strings
    """
    raise NotImplementedError("write your solution here")


def main():
    lines = sys.stdin.read().splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return
    out = solve(lines)
    if isinstance(out, (list, tuple)):
        out = "\n".join(map(str, out))
    sys.stdout.write(f"{out}\n")


if __name__ == "__main__":
    main()
