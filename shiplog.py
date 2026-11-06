#!/usr/bin/env python3
"""Ship's log: a terminal mission browser in the style of a plain CLI utility.

Draws with the terminal's own colours (no custom background). The home screen
shows a twinkling, slightly glitchy starfield with the Daedalus banner on the
left and the mission list on the right. An "Intro" entry above the missions
opens missions/intro.md with no answer box.

Each mission has an "a" and "b" part on the same page. Selecting a mission
shows missions/mission<N>a.md with an answer box below it; once part a is
solved, missions/mission<N>b.md is revealed underneath it (part a stays on the
page, since part b may build on it) and the box takes the part b answer.
Answers are checked against missions/answers.toml. Progress is kept in
progress.json.

To get the hash for an answer key:  python shiplog.py --hash 1a 42
"""

import hashlib
import json
import random
import sys
import tomllib
from pathlib import Path

from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.content import Content
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Input, Label, ListItem, ListView, Markdown, Static
from textual.widgets.markdown import MarkdownFence

MISSION_DIR = Path(__file__).parent / "missions"
MISSIONS = [1, 2, 3, 4]
PARTS = ["a", "b"]
ANSWER_FILE = MISSION_DIR / "answers.toml"
PROGRESS_FILE = Path(__file__).parent / "progress.json"
INTRO_FILE = MISSION_DIR / "intro.md"

OS_VERSION = "BoundStar OS v1.3.7"
GREETING = "welcome back, captain"

BANNER_WIDE = """\
██████╗  █████╗ ███████╗██████╗  █████╗ ██╗     ██╗   ██╗███████╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██║     ██║   ██║██╔════╝
██║  ██║███████║█████╗  ██║  ██║███████║██║     ██║   ██║███████╗
██║  ██║██╔══██║██╔══╝  ██║  ██║██╔══██║██║     ██║   ██║╚════██║
██████╔╝██║  ██║███████╗██████╔╝██║  ██║███████╗╚██████╔╝███████║
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝""".splitlines()

BANNER_NARROW = r"""
 ____                  _       _
|  _ \  __ _  ___   __| | __ _| |_   _  ___
| | | |/ _` |/ _ \ / _` |/ _` | | | | |/ __|
| |_| | (_| |  __/| (_| | (_| | | |_| |\__ \
|____/ \__,_|\___| \__,_|\__,_|_|\__,_||___/""".strip("\n").splitlines()

# Starfield tuning.
STAR_DENSITY = 0.022
STAR_GLYPHS = [(".", 30), ("·", 30), ("˙", 10), ("+", 8), ("*", 7), ("⋆", 8), ("✦", 4), ("✧", 3)]
STAR_COLOURS = [("white", 4), ("bright_white", 2), ("yellow", 3), ("bright_yellow", 2), ("bright_black", 3)]
TICK_SECONDS = 0.12
TWINKLES_PER_TICK = 3
GLITCH_CHANCE = 0.03
GLITCH_GLYPHS = "░▒▓▖▗▘▝▚▞"

# ```map code blocks: dim rock, bold drill, and a fixed colour per wormhole
# symbol, so matching wormholes stand out and keep their colour across pictures.
# Colour = MAP_COLOURS[position in MAP_SYMBOLS % 12]; the order is picked so the
# example symbols (a b A B 7) all get different hues.
MAP_STYLES = {".": "ansi_bright_black", "|": "bold", "⌄": "bold", "\n": ""}
MAP_SYMBOLS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
MAP_COLOURS = [
    "ansi_bright_red", "ansi_bright_green", "ansi_bright_magenta", "ansi_bright_cyan",
    "ansi_bright_yellow", "ansi_bright_blue", "ansi_red", "ansi_cyan", "ansi_magenta",
    "ansi_green", "ansi_yellow", "ansi_blue",
]

# ```maze code blocks (mission 4): green trees, dim open ground, a bold sample
# site and one style for the drone whichever way it faces. Only lines made of
# maze characters are coloured, so captions ("B: tick 4") and function lines
# ("A: FFLF") stay plain.
DRONE = "bold ansi_bright_yellow"
MAZE_STYLES = {
    "#": "ansi_green", ".": "ansi_bright_black", "S": "bold", "E": "bold ansi_bright_magenta",
    ">": DRONE, "<": DRONE, "^": DRONE, "v": DRONE,
}


def pick(rng: random.Random, weighted):
    items, weights = zip(*weighted)
    return rng.choices(items, weights)[0]


def read_mission(number: int, part: str) -> str:
    path = MISSION_DIR / f"mission{number}{part}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"# Mission {number}{part}\n\n*No transmission received.*"


def read_intro() -> str:
    if INTRO_FILE.exists():
        return INTRO_FILE.read_text(encoding="utf-8")
    return "# Intro\n\n*No transmission received.*"


def hash_answer(mission: str, answer: str) -> str:
    return hashlib.sha256(f"{mission}:{answer}".encode()).hexdigest()


def load_progress() -> dict[str, str]:
    """Solved missions, mapped to the answer that solved them."""
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_progress(progress: dict[str, str]) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def check_answer(mission: str, answer: str) -> tuple[bool, str]:
    """Return (correct, message). Hints are tried in file order; first match wins."""
    keys = tomllib.loads(ANSWER_FILE.read_text(encoding="utf-8")) if ANSWER_FILE.exists() else {}
    key = keys.get(mission)
    if key is None:
        return False, "No answer key for this mission yet."
    if hash_answer(mission, answer) == key["answer"]:
        return True, "Correct!"
    try:
        number = float(answer)
    except ValueError:
        number = None
    for hint in key.get("hints", []):
        if "equals" in hint and answer == str(hint["equals"]):
            return False, hint["say"]
        if number is not None and "below" in hint and number < hint["below"]:
            return False, hint["say"]
        if number is not None and "above" in hint and number > hint["above"]:
            return False, hint["say"]
    return False, key.get("wrong", "That's not the right answer.")


class Starfield(Widget):
    """Full-screen backdrop: stars, the banner, the greeting and the OS line.

    Each tick a few stars twinkle (flare up or blink out) and, now and then, a
    short streak of block glyphs flashes across a row like signal noise.
    """

    def __init__(self, avoid: str, **kwargs):
        super().__init__(**kwargs)
        self.avoid = avoid  # selector of a widget the stars should keep clear of
        self.rng = random.Random()
        self.stars: dict[tuple[int, int], tuple[str, str]] = {}
        self.effects: dict[tuple[int, int], tuple[str, str, int]] = {}

    def on_mount(self) -> None:
        self.set_interval(TICK_SECONDS, self.tick)

    def on_resize(self) -> None:
        self.scatter()

    def layout_text(self) -> list[tuple[int, int, str, Style]]:
        """Return (x, y, text, style) runs for the banner, greeting and OS line."""
        w, h = self.size
        menu = self.screen.query_one(self.avoid).region
        left_width = menu.x if menu.width else w
        banner = next(
            (b for b in (BANNER_WIDE, BANNER_NARROW) if max(map(len, b)) + 6 <= left_width),
            ["D A E D A L U S"],
        )
        banner_width = max(map(len, banner))
        x = max(2, (left_width - banner_width) // 2)
        y = max(1, (h - len(banner) - 2) // 2)
        runs = [(x, y + i, line, Style(bold=True)) for i, line in enumerate(banner)]
        greet_x = x + max(0, (banner_width - len(GREETING)) // 2)
        runs.append((greet_x, y + len(banner) + 1, GREETING, Style(color="yellow", italic=True)))
        runs.append((2, h - 2, OS_VERSION, Style(color="bright_black")))
        return runs

    def blocked(self) -> set[tuple[int, int]]:
        """Cells the stars stay out of: around the text and the menu."""
        cells = set()
        for x, y, text, _ in self.layout_text():
            for cx in range(x - 2, x + len(text) + 2):
                for cy in range(y - 1, y + 2):
                    cells.add((cx, cy))
        menu = self.screen.query_one(self.avoid).region
        for cx in range(menu.x - 3, menu.right + 3):
            for cy in range(menu.y - 1, menu.bottom + 1):
                cells.add((cx, cy))
        return cells

    def scatter(self) -> None:
        w, h = self.size
        self.stars = {
            (x, y): (pick(self.rng, STAR_GLYPHS), pick(self.rng, STAR_COLOURS))
            for y in range(h)
            for x in range(w)
            if self.rng.random() < STAR_DENSITY
        }
        self.effects.clear()
        self.refresh()

    def tick(self) -> None:
        self.effects = {cell: (g, c, n - 1) for cell, (g, c, n) in self.effects.items() if n > 1}
        stars = list(self.stars)
        for cell in self.rng.sample(stars, min(TWINKLES_PER_TICK, len(stars))):
            if self.rng.random() < 0.5:
                self.effects[cell] = (self.rng.choice("✦*+"), "bright_yellow", self.rng.randint(2, 6))
            else:
                self.effects[cell] = (" ", "white", self.rng.randint(1, 4))
        if stars and self.rng.random() < GLITCH_CHANCE:
            x0, y0 = self.rng.choice(stars)
            for x in range(x0, x0 + self.rng.randint(3, 9)):
                glyph = self.rng.choice(GLITCH_GLYPHS)
                self.effects[(x, y0)] = (glyph, self.rng.choice(["yellow", "bright_black"]), 2)
        self.refresh()

    def render(self) -> Text:
        w, h = self.size
        grid = [[" "] * w for _ in range(h)]
        styles: list[tuple[int, int, int, Style | str]] = []

        def put(x: int, y: int, text: str, style) -> None:
            if 0 <= y < h:
                for i, ch in enumerate(text[: max(0, w - x)]):
                    if x + i >= 0:
                        grid[y][x + i] = ch
                styles.append((x, y, len(text), style))

        blocked = self.blocked()
        for (x, y), (glyph, colour) in self.stars.items():
            if (x, y) not in blocked:
                put(x, y, glyph, colour)
        for (x, y), (glyph, colour, _) in self.effects.items():
            if (x, y) not in blocked:
                put(x, y, glyph, colour)
        for x, y, text, style in self.layout_text():
            put(x, y, text, style)

        text = Text("\n".join("".join(row) for row in grid), no_wrap=True, overflow="crop")
        for x, y, length, style in styles:
            start = y * (w + 1) + max(0, x)
            text.stylize(style, start, min(start + length, y * (w + 1) + w))
        return text


class IntroItem(ListItem):
    def __init__(self):
        super().__init__(Label("Intro"), classes="intro")


class MissionItem(ListItem):
    def __init__(self, number: int):
        super().__init__(Label())
        self.number = number

    def sync(self, progress: dict[str, str]) -> None:
        """Update solved state from progress: one green tick per solved part,
        and the whole line goes green once every part is solved."""
        solved = sum(f"{self.number}{part}" in progress for part in PARTS)
        self.set_class(solved == len(PARTS), "solved")
        label = Text(f"Mission {self.number}")
        if solved:
            label.append("  " + "✓" * solved, style="green")
        self.query_one(Label).update(label)


class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Starfield(avoid="#menu", id="stars")
        with Vertical(id="menu"):
            yield ListView(IntroItem(), *(MissionItem(n) for n in MISSIONS), id="missions")
            yield Static("↑↓ select · enter open · q quit", classes="hint")

    def on_mount(self) -> None:
        self.sync_missions()

    def on_screen_resume(self) -> None:
        self.sync_missions()

    def sync_missions(self) -> None:
        for item in self.query(MissionItem):
            item.sync(self.app.progress)


class MapFence(MarkdownFence):
    """A code block that colours ```map and ```maze blocks; any other language highlights as usual."""

    @classmethod
    def highlight(cls, code: str, language: str, ansi: bool = False, dark: bool = False) -> Content:
        if language == "maze":
            return cls.highlight_maze(code)
        if language != "map":
            return super().highlight(code, language, ansi, dark)
        parts = []
        for char in code:
            style = MAP_STYLES.get(char)
            if style is None:
                index = MAP_SYMBOLS.find(char)
                style = MAP_COLOURS[index % len(MAP_COLOURS)] if index >= 0 else ""
            parts.append((char, style))
        return Content.assemble(*parts)

    @staticmethod
    def highlight_maze(code: str) -> Content:
        parts = []
        for line in code.splitlines(keepends=True):
            if set(line.strip()) <= set(MAZE_STYLES) | {" "}:
                parts.extend((char, MAZE_STYLES.get(char, "")) for char in line)
            else:
                parts.append(line)
        return Content.assemble(*parts)


class ShipMarkdown(Markdown):
    """Markdown that draws its code blocks with MapFence."""

    BLOCKS = {**Markdown.BLOCKS, "fence": MapFence, "code_block": MapFence}


class PageScreen(Screen):
    """A scrollable markdown page, like a man page. Esc goes back."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "scroll('up')", show=False),
        Binding("down", "scroll('down')", show=False),
        Binding("pageup", "scroll('pageup')", show=False),
        Binding("pagedown", "scroll('pagedown')", show=False),
    ]

    def action_scroll(self, how: str) -> None:
        reader = self.query_one("#reader", VerticalScroll)
        {"up": reader.scroll_up, "down": reader.scroll_down,
         "pageup": reader.scroll_page_up, "pagedown": reader.scroll_page_down}[how]()


class IntroScreen(PageScreen):
    """The intro page: just text, nothing to answer."""

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="reader"):
            yield ShipMarkdown(read_intro())
        with Vertical(id="answer"):
            yield Static("↑↓ scroll · esc back", id="keys")


class ReaderScreen(PageScreen):
    """A mission page with a Claude Code-style answer box underneath.

    Shows part a; once it's solved, part b appears below it and the box moves
    on to part b.
    """

    def __init__(self, number: int):
        super().__init__()
        self.number = number

    @property
    def part(self) -> str | None:
        """The part the answer box is for, or None when every part is solved."""
        return next((p for p in PARTS if f"{self.number}{p}" not in self.app.progress), None)

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="reader"):
            for part in PARTS:
                yield from self.part_widgets(part)
                if part == self.part:
                    break
        with Vertical(id="answer"):
            yield Static(id="feedback")
            with Horizontal(id="prompt"):
                yield Static(">", id="caret")
                yield Input(compact=True, id="answer-input")
            yield Static("enter submit · ↑↓ scroll · esc back", id="keys")

    def part_widgets(self, part: str) -> list[Widget]:
        """The page section for one part: a dashed divider (after the first part),
        its text, then its answer if solved."""
        widgets = []
        if part != PARTS[0]:
            widgets.append(Static(Text("-" * 88, no_wrap=True, overflow="crop"), classes="divider"))
        widgets.append(ShipMarkdown(read_mission(self.number, part), id=f"part-{part}", classes="part"))
        answer = self.app.progress.get(f"{self.number}{part}")
        if answer is not None:
            widgets.append(Static(f"✓ Part {part} answer: {answer}", classes="part-answer"))
        return widgets

    def on_mount(self) -> None:
        self.sync_prompt()
        self.query_one(Input).focus()

    def sync_prompt(self) -> None:
        """Point the answer box at the current part, or close it when all are done."""
        box = self.query_one(Input)
        box.value = ""
        if self.part is None:
            box.placeholder = ""
            box.disabled = True
            self.feedback("✓ Mission complete.", "correct")
        else:
            box.placeholder = f"type your part {self.part} answer and press enter"

    def feedback(self, message: str, kind: str) -> None:
        line = self.query_one("#feedback", Static)
        line.update(message)
        line.set_classes(kind)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        answer = event.value.strip()
        part = self.part
        if not answer or part is None:
            return
        correct, message = check_answer(f"{self.number}{part}", answer)
        if not correct:
            event.input.value = ""
            self.feedback(f"✗ {answer}: {message}", "wrong")
            return
        self.app.progress[f"{self.number}{part}"] = answer
        save_progress(self.app.progress)
        reader = self.query_one("#reader", VerticalScroll)
        reader.mount(Static(f"✓ Part {part} answer: {answer}", classes="part-answer"), after=f"#part-{part}")
        self.sync_prompt()
        if self.part is not None:
            reader.mount_all(self.part_widgets(self.part))
            self.feedback(f"✓ {message} Part {self.part} is below.", "correct")
            self.call_after_refresh(reader.scroll_to_widget, self.query_one(f"#part-{self.part}"), top=True)


class ShipLog(App):
    CSS_PATH = "shiplog.tcss"
    BINDINGS = [Binding("q", "quit", "Quit")]

    def __init__(self):
        super().__init__(ansi_color=True)
        self.progress = load_progress()

    def get_default_screen(self) -> Screen:
        return HomeScreen()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, IntroItem):
            self.push_screen(IntroScreen())
        else:
            self.push_screen(ReaderScreen(event.item.number))


if __name__ == "__main__":
    if sys.argv[1:2] == ["--hash"] and len(sys.argv) == 4:
        print(hash_answer(sys.argv[2], sys.argv[3].strip()))
    else:
        ShipLog().run()
