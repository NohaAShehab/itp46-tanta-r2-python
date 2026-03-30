#!/usr/bin/env python3
"""Notebook helpers: inject explanatory markdown and apply colorful HTML callouts."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Rotating pastel callouts (background, left border, text)
CALLOUT_PALETTE: list[tuple[str, str, str]] = [
    ("#e0f2fe", "#0284c7", "#0c4a6e"),
    ("#fef3c7", "#d97706", "#78350f"),
    ("#dcfce7", "#16a34a", "#14532d"),
    ("#fce7f3", "#db2777", "#831843"),
    ("#ede9fe", "#7c3aed", "#4c1d95"),
    ("#ffedd5", "#ea580c", "#7c2d12"),
]


def inline_md_to_html(text: str) -> str:
    """Turn `code` and **bold** into HTML; escape everything else."""
    parts: list[str] = []
    pos = 0
    for m in re.finditer(r"`([^`]+)`|\*\*(.+?)\*\*", text, flags=re.DOTALL):
        parts.append(html.escape(text[pos : m.start()]))
        if m.group(1) is not None:
            parts.append(
                '<code style="background:rgba(255,255,255,0.65);padding:2px 7px;border-radius:5px;'
                'font-size:0.9em;font-family:ui-monospace,Consolas,monospace;">'
                f"{html.escape(m.group(1))}</code>"
            )
        else:
            parts.append(f"<strong>{html.escape(m.group(2))}</strong>")
        pos = m.end()
    parts.append(html.escape(text[pos:]))
    return "".join(parts)


def wrap_callout(text: str, i: int) -> str:
    bg, border, fg = CALLOUT_PALETTE[i % len(CALLOUT_PALETTE)]
    inner = inline_md_to_html(text.strip())
    return (
        '<div class="day02-callout" style="'
        f"background:{bg};border-left:5px solid {border};padding:12px 16px;border-radius:10px;"
        f"color:{fg};margin:10px 0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
        f'line-height:1.55;box-shadow:0 2px 10px rgba(0,0,0,0.07);">'
        f"{inner}</div>"
    )


def wrap_topic_title(body: str, gradient: tuple[str, str]) -> str:
    """Turn '# title' plus optional '- bullet' lines into a gradient banner."""
    lines = [ln for ln in body.strip().split("\n") if ln.strip()]
    if not lines:
        return body
    title = re.sub(r"^#+\s*", "", lines[0]).strip()
    bullets: list[str] = []
    for ln in lines[1:]:
        s = ln.strip()
        if s.startswith("-"):
            bullets.append(s[1:].strip())
    g1, g2 = gradient
    lis = "".join(
        f'<li style="margin:5px 0;">{inline_md_to_html(b)}</li>' for b in bullets
    )
    ul = f'<ul style="margin:0;padding-left:20px;opacity:0.96;line-height:1.55;">{lis}</ul>'
    return (
        '<div class="day02-title" style="'
        f"background:linear-gradient(135deg,{g1},{g2});color:#fff;padding:18px 22px;border-radius:12px;"
        f'margin:8px 0 16px 0;box-shadow:0 8px 24px rgba(0,0,0,0.18);">'
        f'<h2 style="margin:0 0 12px 0;font-size:1.35rem;font-weight:700;">{html.escape(title)}</h2>'
        f"{ul}</div>"
    )


def wrap_section_ribbon(text: str) -> str:
    """Short section header like '# sets'."""
    t = re.sub(r"^#+\s*", "", text.strip()).strip()
    return (
        '<div class="day02-section" style="'
        "background:linear-gradient(90deg,#f59e0b,#ea580c);color:#fff;padding:0.65rem 1.1rem;"
        "border-radius:10px;font-weight:700;margin:14px 0 14px 0;letter-spacing:0.02em;"
        f'box-shadow:0 4px 14px rgba(234,88,12,0.35);">{html.escape(t)}</div>'
    )


def wrap_optional_params_banner() -> str:
    return (
        '<div class="day02-section" style="'
        "background:linear-gradient(90deg,#6366f1,#8b5cf6);color:#fff;padding:0.65rem 1.1rem;"
        "border-radius:10px;font-weight:700;margin:14px 0 14px 0;"
        'box-shadow:0 4px 14px rgba(99,102,241,0.35);">Optional parameters &amp; beyond</div>'
    )


def cell_source(cell: dict) -> str:
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def to_source_lines(text: str) -> list[str]:
    if not text.strip():
        return ["\n"]
    lines = text.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else ["\n"])


def html_cell_source(html: str) -> list[str]:
    return [html + "\n"]


EXPLANATIONS: dict[str, list[str]] = {
    "lists.ipynb": [
        "Create empty lists with the literal `[]` or the `list()` constructor. `mul` is imported for possible later use.",
        "Build a list that mixes types (strings, numbers, booleans, `None`) and nests another list inside it.",
        "Access a single element by **index** (0-based): index `2` is the third item.",
        "Use **slicing** `[start:end]` to take a sub-range; `end` is exclusive.",
        "Index into a nested list: first pick the inner list, then pick an element inside it.",
        "Rebuild the list with repeated values, then use **`len()`** to see how many items it holds.",
        "**`count(x)`** tells how many times a value appears in the list.",
        "**`index(x)`** returns the position of the **first** occurrence of `x`.",
        "Loop with **`for`** to process each element in order.",
        "Lists are **mutable**: assign to an existing index to replace that element.",
        "Assignment only works for **existing** indices; going past the end raises **`IndexError`**.",
        "**`append(x)`** adds one item at the end of the list.",
        "**`insert(i, x)`** shifts items and inserts `x` at position `i`.",
        "If the index is too large, **`insert`** appends at the end instead of erroring.",
        "**`pop()`** removes and returns the **last** item (stack-like behavior).",
        "**`pop(i)`** removes and returns the item at index `i`.",
        "The value returned by **`pop`** is whatever was removed (here, the element at index 5).",
        "**`remove(x)`** deletes the **first** matching value when you know the value, not the index.",
        "Use **`+`** to build a **new** list that concatenates two lists.",
        "**`extend(iterable)`** adds each element from another iterable to the **same** list (in place).",
        "**`sort()`** compares elements; mixed types that cannot be compared raise **`TypeError`**.",
        "When all items are comparable (e.g. all strings), **`sort()`** orders them ascending.",
        "Pass **`reverse=True`** to sort in descending order.",
        "Copy elements into an empty list with **`extend`** (another way to duplicate a sequence).",
        "**`append`** a whole list adds **one** nested list object, not each item separately.",
        "Assignment **`ll2 = ll`** makes two names point to the **same** list (alias).",
        "Mutating through one name is visible through the other—they share one object.",
        "**`copy()`** makes a **shallow** copy: a new list, but shared inner objects if any.",
        "Changes after **`copy()`** affect only the list you mutate, not the copy (for top-level items).",
        "Inspect the list before reversing.",
        "**`reverse()`** reverses the list **in place** (does not create a new list).",
        "The **`in`** operator tests membership: is this value in the list?",
        "You can track the index manually with a counter variable inside a **`for`** loop.",
        "Calling **`enumerate(ll)`** builds an iterator; printing it only shows the object repr.",
        "**`enumerate`** pairs each index with its value—cleaner than manual counters.",
        "Define another heterogeneous list for more enumeration examples.",
        "Store **`enumerate(...)`** in a variable: you get an iterator object.",
        "Iterate over that iterator once to print index and item for each element.",
        "An **iterator is exhausted** after one full loop—reusing it without rebuilding prints nothing.",
        "You can call **`enumerate`** directly in the **`for`** line; idiomatic and readable.",
        "**`min()`** returns the smallest item (here, the most negative number).",
        "**`list(string)`** splits a string into a list of **characters**.",
        "**`split()`** (default: whitespace) breaks a string into **words** as a list.",
        "**`str.join(iterable)`** inserts a separator between strings from the iterable (here, underscores).",
        "Placeholder cell—add your own list exercises if you like.",
    ],
    "tuple.ipynb": [
        "Create empty tuples with `()` or **`tuple()`**.",
        "Tuples can hold mixed types and nest other tuples and lists (contents of nested mutable objects can still change).",
        "Index into a tuple like a list: **`[2]`** is the third element.",
        "Slicing works on tuples and returns a **new** tuple (a sub-range).",
        "Nested indexing: reach into an inner sequence stored inside the tuple.",
        "**`len()`** returns the number of top-level items in the tuple.",
        "**`count(x)`** counts how many times `x` appears in the tuple.",
        "**`index(x)`** finds the first index where `x` occurs.",
        "Loop over a tuple with **`for`**—same idea as lists.",
        "Use **`+`** to concatenate tuples into a **new** tuple (tuples themselves are immutable).",
        "Assigning **`tt2 = tt`** aliases the same tuple object to another name.",
        "Membership **`in`** checks whether a value appears anywhere in the tuple.",
        "Manual index tracking with a counter while iterating.",
        "**`enumerate`** on a tuple yields `(index, value)` pairs.",
        "Unpack those pairs in the **`for`** loop for readable indexed iteration.",
        "**`min()`** works on a tuple of comparable numbers.",
        "**`tuple(string)`** turns each character into a one-character tuple element.",
        "**`join`** works on any sequence of strings, including a tuple of words.",
        "Parentheses around a **single** non-comma expression are just grouping—`(\"iti\")` is still a **string**.",
        "**`tuple(\"iti\")`** iterates characters, so you get three one-character strings in a tuple.",
        "Wrapping a **list** in **`tuple()`** builds a tuple from the list’s elements.",
        "A one-character string in **`tuple()`** still becomes a one-element tuple.",
        "A **trailing comma** makes a one-item tuple: **`(\"iti\",)`**—the comma matters, not only parentheses.",
        "Placeholder cell for your own tuple experiments.",
    ],
    "dicts.ipynb": [
        "Contrast a plain list of fields with the need for **named** fields—motivating dictionaries.",
        "Create empty dicts with `{}` or **`dict()`**.",
        "Define **`key: value`** pairs; duplicate keys keep the **last** assignment. Dicts preserve insertion order (Python 3.7+).",
        "Read a value with **`d[key]`**; the key must exist (or you get **`KeyError`**).",
        "Assign to an **existing** key to update the value—dicts are mutable.",
        "Assigning to a **new** key inserts that entry into the dictionary.",
        "**`len()`** counts key-value pairs.",
        "Iterating **`for x in dict`** walks **keys** only.",
        "Unpacking **`for a, b in dict`** fails—dict iteration is only over keys unless you use **`.items()`**.",
        "Print each key with **`dict[key]`** to show the associated value.",
        "**.keys()** returns a view of keys (often converted with **`list(...)`**).",
        "**.values()** returns a view of all values.",
        "**.items()** yields **`(key, value)`** pairs—ideal for looping over both.",
        "Each item from **`.items()`** behaves like a small tuple **`(k, v)`**.",
        "Dicts do not support **`+`**; merging requires other operations (see **`.update()`**).",
        "**.update(other)`** merges keys from another dict; existing keys may be overwritten.",
        "**`in`** on a dict checks **keys** by default, not values.",
        "Use **`in dict.values()`** to search for a value.",
        "**`clear()`** empties the dict; **`del dict`** removes the name (variable).",
        "Rebuild a sample dictionary for later deletion demos.",
        "**`del dict[key]`** removes one key and its value.",
        "**`pop(key)`** removes that entry and **returns** the value.",
        "Placeholder cell for dict practice.",
    ],
    "functions.ipynb": [
        "Define a function with **`def`**, **`pass`** as a placeholder body, and note the odd unused import (can be removed in real code).",
        "A function name without **`()`** refers to the **function object** itself (its repr shows where it lives).",
        "Call the function with **`()`** to run its body.",
        "If the function has no **`return`**, the result of the call is **`None`**.",
        "A bare **`return`** also exits the function and returns **`None`**.",
        "Side effects: **`print`** inside the function runs when called; return value is still **`None`** if no return value.",
        "Use **`input()`** to read strings from the user, then **`return`** a combined result.",
        "Multiple values after **`return`** are packed into a **tuple** automatically.",
        "Parameters act as local names; **`return`** sends a result back to the caller.",
        "Calling with **too few** arguments raises **`TypeError`** (missing parameter).",
        "Calling with **too many** positional arguments also raises **`TypeError`**.",
        "Empty cell—separator before optional parameters section.",
        "**`print`** can take several arguments; they are shown separated by spaces.",
        "Multiple values print on one line by default, separated by spaces.",
        "**Default parameters** let callers omit arguments; defaults are used when not provided.",
        "In Python, parameters **with defaults must come after** parameters without defaults—otherwise **`SyntaxError`**.",
        "Demonstration of arbitrary extra values passed to **`print`**.",
        "A **`*args`** parameter collects extra positional arguments into a **tuple**.",
        "**.format** substitutes named placeholders inside a string.",
        "A **`**kwargs`** parameter collects keyword arguments into a **dictionary**.",
        "The **`**dict`** call syntax expands a dict into keyword arguments when calling a function.",
        "Example function that adds two values and prints; relies on **`+`** behavior of the operands.",
        "For strings, **`+`** means **concatenation**—no error, but meaning differs from numeric add.",
        "Mixing incompatible types for **`+`** raises **`TypeError`**—Python does not guess intent.",
        "Coercing with **`int()`** can fix numeric strings—**you** must validate real inputs in production.",
        "Both arguments as numeric strings can be converted and added.",
        "Non-numeric strings still break **`int()`** with **`ValueError`**.",
        "**.isdigit()`** only exists on **strings**—calling it on **`int`** raises **`AttributeError`**.",
        "Check types explicitly before operating; reject or convert invalid combinations.",
        "**`isinstance(obj, type)`** is the usual way to check types.",
        "**Type hints** document intent; they are **not** enforced at runtime by default.",
        "A docstring explains parameters and return value for humans and tools.",
    ],
    "tips.ipynb": [
        "**`range(stop)`** builds an iterator of integers from **`0`** up to **`stop - 1`**.",
        "Use **`range`** in a **`for`** loop to repeat a block a fixed number of times.",
        "**`type()`** shows that **`range`** is its own immutable sequence type.",
        "**`range(start, stop, step)`** controls beginning, end (exclusive), and stride.",
        "Materialize a range as a **list** to see all generated numbers at once.",
        "A **negative step** counts downward (handy for reverse iteration patterns).",
        "Printing a **`range`** object shows its parameters, not every element.",
        "Empty separator cell—next section introduces **sets**.",
        "A **set** literal uses **`{}`** with comma-separated items; duplicates are discarded.",
        "Sets **unordered**, unique membership; **`add`** inserts one new element.",
        "Adding another element shows typical set usage.",
        "Set elements must be **hashable**; lists are mutable and **not** hashable—**`TypeError`**.",
        "Tuples are hashable (if their contents are); a tuple can live inside a set.",
        "Print the current contents of the set after changes.",
        "A tuple may contain a **list**; the tuple is immutable but the **list inside** can still be mutated.",
        "Placeholder cell for set and range exercises.",
    ],
}


def inject(path: Path) -> None:
    name = path.name
    if name not in EXPLANATIONS:
        return
    expl = EXPLANATIONS[name]
    nb = json.loads(path.read_text(encoding="utf-8"))
    new_cells: list[dict] = []
    code_i = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            if not cell_source(cell).strip():
                continue
            new_cells.append(cell)
            continue
        if cell["cell_type"] != "code":
            new_cells.append(cell)
            continue
        if code_i >= len(expl):
            raise RuntimeError(f"{name}: more code cells than explanations ({code_i})")
        new_cells.append(
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": html_cell_source(wrap_callout(expl[code_i], code_i)),
            }
        )
        new_cells.append(cell)
        code_i += 1
    if code_i != len(expl):
        raise RuntimeError(f"{name}: expected {len(expl)} code cells, saw {code_i}")
    nb["cells"] = new_cells
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def inject_all() -> None:
    for fname in EXPLANATIONS:
        inject(ROOT / fname)
    print("Injected:", ", ".join(EXPLANATIONS))


def colorize_notebooks() -> None:
    """Wrap plain markdown in colorful HTML (skips cells already colorized)."""
    notebooks = ["lists.ipynb", "tuple.ipynb", "dicts.ipynb", "functions.ipynb", "tips.ipynb"]
    for fname in notebooks:
        path = ROOT / fname
        if not path.exists():
            continue
        nb = json.loads(path.read_text(encoding="utf-8"))
        callout_idx = 0
        for cell in nb["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            raw = cell_source(cell)
            if not raw.strip():
                continue
            if "day02-callout" in raw or "day02-title" in raw or "day02-section" in raw:
                continue
            name = path.name
            stripped = raw.strip()
            if name == "lists.ipynb" and stripped.startswith("# lists"):
                cell["source"] = html_cell_source(wrap_topic_title(raw, ("#667eea", "#764ba2")))
                continue
            if name == "tuple.ipynb" and stripped.startswith("# tuples"):
                cell["source"] = html_cell_source(wrap_topic_title(raw, ("#0f766e", "#14b8a6")))
                continue
            if stripped == "# sets":
                cell["source"] = html_cell_source(wrap_section_ribbon(raw))
                continue
            if stripped == "# functions with Optional Params.":
                cell["source"] = html_cell_source(wrap_optional_params_banner())
                continue
            cell["source"] = html_cell_source(wrap_callout(raw, callout_idx))
            callout_idx += 1
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Colorized:", fname)


def main() -> None:
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "inject":
        inject_all()
    else:
        colorize_notebooks()


if __name__ == "__main__":
    main()
