from __future__ import annotations

import argparse
import csv
import json
import re
import tkinter as tk
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

try:
    from config import Config
except Exception:
    Config = None


REFRESH_MS = 350
MAX_CANDLES = 80

WINDOW_SIZE = "1180x740"
WINDOW_MIN_SIZE = (960, 560)

MARKET_CARD_SIZE = (800, 450)
STATS_CARD_SIZE = (392, 300)
CANDLE_CARD_SIZE = (288, 160)
BACKTEST_CARD_SIZE = (104, 160)
EQUITY_CARD_SIZE = (1192, 240)


OPTIONAL = "Optional: debug_lauf_56"
STARTEQUITY = Config.START_EQUITY if Config else 100.0

C = {
    "bg_root": "#000000",
    "bg_panel": "#13161c",
    "bg_card": "#181c24",
    "bg_chart": "#0f1319",
    "border": "#252a36",
    "border_hi": "#2e3548",
    "text_hi": "#e8eaf0",
    "text_med": "#8b92a8",
    "text_lo": "#4a5168",
    "text_label": "#4e5f87",
    "green": "#4caf78",
    "red": "#c05050",
    "blue": "#5b8dd9",
    "orange": "#d4894a",
}

matplotlib.rcParams.update(
    {
        "figure.facecolor": C["bg_card"],
        "axes.facecolor": C["bg_chart"],
        "axes.edgecolor": C["border"],
        "axes.labelcolor": C["text_med"],
        "axes.titlecolor": C["text_label"],
        "xtick.color": C["text_lo"],
        "ytick.color": C["text_lo"],
        "grid.color": "#1a1f2b",
        "grid.linewidth": 0.5,
        "text.color": C["text_med"],
        "font.family": "monospace",
        "font.size": 8,
    }
)


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def safe_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)


def fmt_num(value, digits: int = 2) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "-"


def fmt_pct(value, digits: int = 0) -> str:
    try:
        return f"{float(value) * 100.0:.{digits}f}%"
    except Exception:
        return "-"


def normalize_timestamp_ms(value) -> float | None:
    try:
        ts = float(value)
    except Exception:
        return None
    if ts <= 0:
        return None
    if ts > 10_000_000_000_000:
        ts /= 1000.0
    elif ts < 10_000_000_000:
        ts *= 1000.0
    return float(ts)


def fmt_ts(value) -> str:
    ts = normalize_timestamp_ms(value)
    if ts is None:
        return "-"
    try:
        return datetime.fromtimestamp(ts / 1000.0).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return "-"


def safe_load_json(path: Path) -> dict:
    try:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def read_equity_curve(path: Path) -> list[float]:
    values: list[float] = []
    try:
        if not path.exists():
            return values
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                value = safe_float(row.get("current_equity"), 0.0)
                if value > 0.0:
                    values.append(value)
    except Exception:
        return []
    return values


def first_existing_path(*paths: Path) -> Path:
    for path in paths:
        try:
            if path.exists():
                return path
        except Exception:
            continue
    return paths[0]


def resolve_debug_dir(base_dir: Path, preferred: str | None = None) -> Path:
    debug_root = base_dir / "debug"
    if preferred:
        candidate = Path(preferred)
        if not candidate.is_absolute():
            candidate = debug_root / preferred
        if candidate.exists():
            return candidate

    runs = []
    if debug_root.exists():
        for item in debug_root.iterdir():
            if not item.is_dir():
                continue
            match = re.match(r"debug_lauf_(\d+)$", item.name)
            if match:
                runs.append((int(match.group(1)), item.stat().st_mtime, item))

    if runs:
        runs.sort(key=lambda row: (row[0], row[1]))
        return runs[-1][2]

    return debug_root


class CardFrame(tk.Frame):
    def __init__(
        self,
        parent,
        title: str = "",
        width: int | None = None,
        height: int | None = None,
    ):
        super().__init__(
            parent,
            bg=C["bg_card"],
            highlightbackground=C["border"],
            highlightthickness=1,
            width=width,
            height=height,
        )
        self.body = tk.Frame(self, bg=C["bg_card"])
        if width is not None or height is not None:
            self.pack_propagate(False)
            self.grid_propagate(False)

        if title:
            display_title = str(title).upper().replace("MARKT?BERBLICK", "MARKTÜBERBLICK")
            display_title = display_title.replace("MARKT?BERBLICK", "MARKT\u00dcBERBLICK")
            if display_title.startswith("MARKT"):
                display_title = "MARKT\u00dcBERBLICK"
            tk.Label(
                self,
                text=display_title,
                bg=C["bg_card"],
                fg=C["text_label"],
                font=("Courier New", 8, "bold"),
                anchor="w",
                padx=8,
                pady=5,
            ).pack(fill="x")
            tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        self.body.pack(fill="both", expand=True)


class DIOGui:
    def __init__(self, root: tk.Tk, base_dir: Path, debug_run: str | None = None):
        self.root = root
        self.base_dir = Path(base_dir).resolve()
        self.debug_run = debug_run
        self.debug_dir = resolve_debug_dir(self.base_dir, self.debug_run)
        self.gui_dir = self.debug_dir / "gui"
        self.visual_path = first_existing_path(
            self.gui_dir / "bot_visual_snapshot.json",
            self.debug_dir / "bot_visual_snapshot.json",
        )
        self.stats_path = first_existing_path(
            self.gui_dir / "trade_stats.json",
            self.debug_dir / "trade_stats.json",
        )
        self.equity_path = first_existing_path(
            self.gui_dir / "trade_equity.csv",
            self.debug_dir / "trade_equity.csv",
        )
        self._backtest_range: tuple[float, float] | None = None
        self._after_id = None

        self.root.title("DIO GUI")
        self.root.configure(bg=C["bg_root"])
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*WINDOW_MIN_SIZE)

        self._build_layout()
        self._refresh()

    def _build_layout(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main = tk.Frame(self.root, bg=C["bg_root"])
        self.main.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.main.grid_columnconfigure(0, weight=68, minsize=660)
        self.main.grid_columnconfigure(1, weight=32, minsize=320)
        self.main.grid_rowconfigure(0, weight=44, minsize=260)
        self.main.grid_rowconfigure(1, weight=30, minsize=170)
        self.main.grid_rowconfigure(2, weight=26, minsize=155)

        self.card_market = CardFrame(
            self.main,
            "MARKTÜBERBLICK",
        )
        self.card_market.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 4), pady=(0, 4))

        self.card_stats = CardFrame(
            self.main,
            "TRADE STATS & KPI",
        )
        self.card_stats.grid(row=0, column=1, sticky="nsew", padx=(4, 0), pady=(0, 4))

        self.right_lower = tk.Frame(self.main, bg=C["bg_root"])
        self.right_lower.grid(row=1, column=1, sticky="nsew", padx=(4, 0), pady=(4, 4))
        self.right_lower.grid_columnconfigure(0, weight=72, minsize=230)
        self.right_lower.grid_columnconfigure(1, weight=28, minsize=90)
        self.right_lower.grid_rowconfigure(0, weight=1)

        self.card_candle = CardFrame(
            self.right_lower,
            "CANDLE STATE",
        )
        self.card_candle.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=(0, 0))

        self.card_backtest = CardFrame(
            self.right_lower,
            "BACKTEST %",
        )
        self.card_backtest.grid(row=0, column=1, sticky="nsew", padx=(4, 0), pady=(0, 0))

        self.card_equity = CardFrame(
            self.main,
            "EQUITY-KURVE",
        )
        self.card_equity.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(0, 0), pady=(4, 0))

        self.fig_market = Figure(figsize=(8.0, 4.35), dpi=100)
        self.fig_market.subplots_adjust(left=0.08, right=0.985, top=0.965, bottom=0.115)
        self.ax_market = self.fig_market.add_subplot(111)
        self.canvas_market = FigureCanvasTkAgg(self.fig_market, master=self.card_market.body)
        self.canvas_market.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        self.fig_equity = Figure(figsize=(10.8, 1.65), dpi=100)
        self.fig_equity.subplots_adjust(left=0.045, right=0.99, top=0.91, bottom=0.22)
        self.ax_equity = self.fig_equity.add_subplot(111)
        self.canvas_equity = FigureCanvasTkAgg(self.fig_equity, master=self.card_equity.body)
        self.canvas_equity.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        self.candle_labels: dict[str, tk.Label] = {}
        self._build_value_rows(
            self.card_candle.body,
            [
                ("Open", "open"),
                ("High", "high"),
                ("Low", "low"),
                ("Close", "close"),
                ("Volume", "volume"),
            ],
            self.candle_labels,
            value_align="compact",
        )

        self.stats_labels: dict[str, tk.Label] = {}
        self._build_value_rows(
            self.card_stats.body,
            [
                ("PnL Netto", "pnl_netto"),
                ("Wins / Loss", "wins_loss"),
                ("Trades", "trades"),
                ("Cancels", "cancels"),
                ("Attempts", "attempts"),
                ("Observed", "attempts_observed"),
                ("Replanned", "attempts_replanned"),
                ("Withheld", "attempts_withheld"),
                ("Max DD", "max_drawdown_pct"),
                ("Eq. Peak", "equity_peak"),

            ],
            self.stats_labels,
            value_align="right",
        )

        self.backtest_label = tk.Label(
            self.card_backtest.body,
            text="-",
            bg=C["bg_card"],
            fg=C["orange"],
            font=("Courier New", 18, "bold"),
            anchor="center",
        )
        self.backtest_label.pack(fill="both", expand=True)

    def _build_value_rows(
        self,
        parent: tk.Frame,
        rows: list[tuple[str, str]],
        target: dict,
        value_align: str = "compact",
    ):
        right_aligned = value_align == "right"
        parent.grid_columnconfigure(0, weight=0, minsize=118)
        parent.grid_columnconfigure(1, weight=1 if right_aligned else 0, minsize=122)
        parent.grid_columnconfigure(2, weight=0 if right_aligned else 1)
        for row_index, (label_text, key) in enumerate(rows):
            tk.Label(
                parent,
                text=label_text,
                bg=C["bg_card"],
                fg=C["text_label"],
                font=("Courier New", 9, "bold"),
                anchor="w",
            ).grid(row=row_index, column=0, sticky="w", padx=(16, 6), pady=3)

            value_label = tk.Label(
                parent,
                text="-",
                bg=C["bg_card"],
                fg=C["text_hi"],
                font=("Courier New", 9, "bold"),
                anchor="e",
                width=14,
            )
            value_label.grid(
                row=row_index,
                column=1,
                sticky="e",
                padx=(4, 18 if right_aligned else 8),
                pady=3,
            )
            target[key] = value_label

    def _refresh(self):
        self.debug_dir = resolve_debug_dir(self.base_dir, self.debug_run)
        self.gui_dir = self.debug_dir / "gui"
        self.visual_path = first_existing_path(
            self.gui_dir / "bot_visual_snapshot.json",
            self.debug_dir / "bot_visual_snapshot.json",
        )
        self.stats_path = first_existing_path(
            self.gui_dir / "trade_stats.json",
            self.debug_dir / "trade_stats.json",
        )
        self.equity_path = first_existing_path(
            self.gui_dir / "trade_equity.csv",
            self.debug_dir / "trade_equity.csv",
        )

        visual = safe_load_json(self.visual_path)
        stats = safe_load_json(self.stats_path)
        equity = read_equity_curve(self.equity_path)

        self._draw_market_chart(visual)
        self._draw_equity_chart(equity, stats)
        self._update_candle_state(visual)
        self._update_trade_stats(stats)
        self._update_backtest_progress(visual, stats)

        self._after_id = self.root.after(REFRESH_MS, self._refresh)

    def _resolve_window(self, visual: dict) -> list[dict]:
        chart_snapshot = dict(visual.get("chart_snapshot", {}) or {})
        candles = chart_snapshot.get("candles", [])
        if isinstance(candles, list) and candles:
            return [dict(item or {}) for item in candles if isinstance(item, dict)][-MAX_CANDLES:]

        window = visual.get("window", [])
        if isinstance(window, list):
            return [dict(item or {}) for item in window if isinstance(item, dict)][-MAX_CANDLES:]

        return []

    def _draw_market_chart(self, visual: dict):
        self.ax_market.clear()
        self.ax_market.set_facecolor(C["bg_chart"])
        self.ax_market.grid(True, alpha=0.55)

        candles = self._resolve_window(visual)
        if not candles:
            self.ax_market.text(
                0.5,
                0.5,
                "NO MARKET DATA",
                ha="center",
                va="center",
                color=C["text_lo"],
                transform=self.ax_market.transAxes,
            )
            self.canvas_market.draw_idle()
            return

        lows: list[float] = []
        highs: list[float] = []
        for index, candle in enumerate(candles):
            open_price = safe_float(candle.get("open"), 0.0)
            high_price = safe_float(candle.get("high"), open_price)
            low_price = safe_float(candle.get("low"), open_price)
            close_price = safe_float(candle.get("close"), open_price)
            lows.append(low_price)
            highs.append(high_price)

            color = C["green"] if close_price >= open_price else C["red"]
            self.ax_market.vlines(index, low_price, high_price, color="#31394d", linewidth=1.2)
            body_low = min(open_price, close_price)
            body_height = max(abs(close_price - open_price), 1e-9)
            self.ax_market.add_patch(
                Rectangle(
                    (index - 0.31, body_low),
                    0.62,
                    body_height,
                    facecolor=color,
                    edgecolor=color,
                    linewidth=0.8,
                    alpha=0.72,
                )
            )

        price_low = min(lows)
        price_high = max(highs)
        price_span = max(price_high - price_low, 1e-9)
        self.ax_market.set_xlim(-1, len(candles))
        self.ax_market.set_ylim(price_low - price_span * 0.06, price_high + price_span * 0.06)
        self.ax_market.tick_params(labelsize=8)
        self.canvas_market.draw_idle()

    def _draw_equity_chart(self, equity: list[float], stats: dict):
        self.ax_equity.clear()
        self.ax_equity.set_facecolor(C["bg_chart"])
        self.ax_equity.grid(True, alpha=0.55)

        values = list(equity or [])
        if not values:
            start_equity = safe_float(stats.get("start_equity"), 100.0)
            current_equity = safe_float(stats.get("current_equity"), start_equity)
            values = [start_equity, current_equity]

        x_values = list(range(len(values)))
        floor = min(values)
        self.ax_equity.plot(x_values, values, linewidth=2.0, color=C["blue"])
        self.ax_equity.fill_between(x_values, values, floor, alpha=0.14, color=C["blue"])
        self.ax_equity.tick_params(labelsize=8)
        self.canvas_equity.draw_idle()

    def _update_candle_state(self, visual: dict):
        candle_state = dict(visual.get("candle_state", {}) or {})
        candles = self._resolve_window(visual)
        last_candle = dict(candles[-1] if candles else {})
        source = dict(last_candle or candle_state or {})

        values = {
            "open": fmt_num(source.get("open"), 2),
            "high": fmt_num(source.get("high"), 2),
            "low": fmt_num(source.get("low"), 2),
            "close": fmt_num(source.get("close"), 2),
            "volume": fmt_num(source.get("volume"), 2) if source.get("volume") is not None else "-",
        }
        for key, value in values.items():
            label = self.candle_labels.get(key)
            if label is not None:
                label.configure(text=value)
        self.candle_labels["high"].configure(fg=C["green"])
        self.candle_labels["low"].configure(fg=C["red"])

    def _update_trade_stats(self, stats: dict):
        tp = safe_int(stats.get("tp"), 0)
        sl = safe_int(stats.get("sl"), 0)
        pnl = safe_float(stats.get("pnl_netto"), 0.0)
        values = {
            "pnl_netto": f"{pnl+STARTEQUITY:+.2f}",
            "wins_loss": f"{tp} / {sl}",
            "trades": str(safe_int(stats.get("trades"), 0)),
            "cancels": str(safe_int(stats.get("cancels"), 0)),
            "attempts": str(safe_int(stats.get("attempts"), 0)),
            "attempts_observed": str(safe_int(stats.get("attempts_observed"), 0)),
            "attempts_replanned": str(safe_int(stats.get("attempts_replanned"), 0)),
            "attempts_withheld": str(safe_int(stats.get("attempts_withheld"), 0)),
            "max_drawdown_pct": fmt_pct(stats.get("max_drawdown_pct"), 2),
            "equity_peak": fmt_num(stats.get("equity_peak"), 12),
        }
        for key, value in values.items():
            label = self.stats_labels.get(key)
            if label is not None:
                label.configure(text=value)
        self.stats_labels["pnl_netto"].configure(fg=C["green"] if pnl >= 0 else C["red"])

    def _load_backtest_range(self) -> tuple[float, float] | None:
        if self._backtest_range is not None:
            return self._backtest_range
        if Config is None:
            return None
        path = Path(str(getattr(Config, "BACKTEST_FILEPATH", "") or ""))
        if not path.is_absolute():
            path = self.base_dir / path
        if not path.exists():
            return None

        first_ts = None
        last_ts = None
        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = normalize_timestamp_ms(row.get("timestamp_ms") or row.get("timestamp") or row.get("time"))
                    if ts is None:
                        continue
                    if first_ts is None:
                        first_ts = ts
                    last_ts = ts
        except Exception:
            return None

        if first_ts is None or last_ts is None or last_ts <= first_ts:
            return None
        self._backtest_range = (float(first_ts), float(last_ts))
        return self._backtest_range

    def _update_backtest_progress(self, visual: dict, stats: dict):
        progress = stats.get("backtest_progress", stats.get("progress"))
        if progress is not None:
            self.backtest_label.configure(text=fmt_pct(progress, 0))
            return

        current_ts = normalize_timestamp_ms(stats.get("current_timestamp", visual.get("timestamp")))
        backtest_range = self._load_backtest_range()
        if current_ts is not None and backtest_range is not None:
            start_ts, end_ts = backtest_range
            value = max(0.0, min(1.0, (current_ts - start_ts) / max(end_ts - start_ts, 1.0)))
            self.backtest_label.configure(text=fmt_pct(value, 0))
            return

        self.backtest_label.configure(text=fmt_ts(stats.get("current_timestamp", visual.get("timestamp"))))

    def close(self):
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.root.destroy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=".")
    parser.add_argument("--debug-run", default=None, help=OPTIONAL)
    args = parser.parse_args()

    root = tk.Tk()
    app = DIOGui(root, Path(args.base_dir), args.debug_run)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
