# ==================================================
# _gui.py
# ==================================================
# READ-ONLY DARK GUI
# KEIN BOT-START
# KEIN SCHREIBEN
# KEIN RESET
#
# GUI IST REINER LESER VON:
#   debug/trade_stats.json
#   debug/trade_equity.csv
#
# KEIN FREEZE / KEIN RUCKELN
# STATISCHE LAYOUT-GRÖSSEN
# ==================================================

import tkinter as tk
from tkinter import ttk
import time
import os
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
from datetime import datetime
from config import Config
# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
STATS_PATH = "debug/trade_stats.json"
EQUITY_PATH = "debug/trade_equity.csv"
CMAP = 'magma' 
# coolwarm, seismic, RdBu, RdYlBu, RdYlGn, Spectral, PiYG, PRGn, BrBG, PuOr, RdGy
# viridis, plasma, inferno, magma, cividis, turbo
# ─────────────────────────────────────────────
if Config.MODE == "LIVE":
    WORKSPACE_PATH = "data/workspace.csv"
else:
    WORKSPACE_PATH = Config.BACKTEST_FILEPATH

# ─────────────────────────────────────────────
REFRESH_MS = 1000

matplotlib.use("TkAgg")

# ─────────────────────────────────────────────
# COLORS / STYLE
# ─────────────────────────────────────────────
BG = "#121212"
FG = "#e0e0e0"
FG_DIM = "#9aa0a6"
ACCENT = "#4fc3f7"
GOOD = "#66bb6a"
BAD = "#ef5350"
# anzeige
green ="#66bb6a"    # grün
orange ="#ffa726"  # orange
red ="#ef5350"   # red

# ==================================================
# GUI
# ==================================================
class TradeStatsGUI:

    def __init__(self, root):
        self.root = root
        self.root.title(f"{Config.COIN} Trade Stats - {Config.MODE} Mode | RegimeStructure RL Bot")
        self.root.configure(bg=BG)

        # ---------------- STYLE ----------------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 11, "bold"), foreground=ACCENT)
        style.configure("Value.TLabel", font=("Consolas", 10))
        style.configure("Dim.TLabel", foreground=FG_DIM)

        self.vars = {}

        # Gemeinsamer Container für Header + Plot
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Equity State
        self._eq_trades = []
        self._eq_pnl_netto = []
        self._eq_pnl_tp = []
        self._eq_pnl_sl = []
        self._eq_last_line_count = 0

        # RL Heatmap Handles
        self.rl_heatmap = None
        self.cbar = None
        self._rl_last_mtime = 0.0

        # UI Aufbau
        self._build_ui(self.container)
        self._build_equity_window(self.container)

        # Initial laden
        self._reset_equity_state()
        self._load_full_equity()

        # Update Loop
        self._update_loop()

    # ─────────────────────────────────────────────
    # LOAD FULL EQUITY
    # ─────────────────────────────────────────────
    def _load_full_equity(self):
        if not os.path.exists(EQUITY_PATH):
            return

        try:
            with open(EQUITY_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue

                self._eq_trades.append(int(parts[0]))
                self._eq_pnl_netto.append(float(parts[1]))
                self._eq_pnl_tp.append(float(parts[2]))
                self._eq_pnl_sl.append(float(parts[3]))

            self._eq_last_line_count = len(lines)

        except Exception:
            pass

    # ─────────────────────────────────────────────
    # RL Heatmap: NUR DATEN (Matrix) – KEIN imshow / KEIN remove / KEIN self-call
    # ─────────────────────────────────────────────
    def _draw_rl_heatmap(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        path_abs_v2 = os.path.join(base_dir, "bot_memory", "mcm_meta_vector_memory.json")
        path_rel_v2 = os.path.join("bot_memory", "mcm_meta_vector_memory.json")
        path_abs_legacy = os.path.join(base_dir, "bot_memory", "mcm_memory_engine.json")
        path_rel_legacy = os.path.join("bot_memory", "mcm_memory_engine.json")

        if os.path.exists(path_abs_v2):
            path = path_abs_v2
        elif os.path.exists(path_rel_v2):
            path = path_rel_v2
        elif os.path.exists(path_abs_legacy):
            path = path_abs_legacy
        else:
            path = path_rel_legacy

        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                memory = json.load(f)
        except Exception:
            return None

        nodes = memory.get("regime_nodes")

        if not nodes:
            return None

        values = []

        for node in nodes:

            stats = node.get("side_stats", {})

            long_stats = stats.get("LONG", {})
            short_stats = stats.get("SHORT", {})

            tp_long = float(long_stats.get("tp", 0) or 0)
            sl_long = float(long_stats.get("sl", 0) or 0)

            tp_short = float(short_stats.get("tp", 0) or 0)
            sl_short = float(short_stats.get("sl", 0) or 0)

            tp = tp_long + tp_short
            sl = sl_long + sl_short

            rr_sum_long = float(long_stats.get("rr_sum", 0.0) or 0.0)
            rr_sum_short = float(short_stats.get("rr_sum", 0.0) or 0.0)

            rr_count_long = float(long_stats.get("rr_count", 0) or 0)
            rr_count_short = float(short_stats.get("rr_count", 0) or 0)

            rr_sum = rr_sum_long + rr_sum_short
            rr_count = rr_count_long + rr_count_short

            if rr_count > 0:
                avg_rr = rr_sum / rr_count
            else:
                avg_rr = 1.0

            score = (tp * avg_rr) - sl

            values.append(score)

        # --------
        if len(values) < 4:
            return None

        size = int(len(values) ** 0.5)

        if size < 2:
            return None

        values = values[: size * size]

        matrix = []

        for i in range(size):

            row = values[i * size:(i + 1) * size]

            matrix.append(row)

        return matrix

    # ─────────────────────────────────────────────
    # PRINT TIMERANGE
    # ─────────────────────────────────────────────
    def print_Time_Range(self, path):
        if not os.path.exists(path):
            return "-"

        first_ts = None
        last_ts = None

        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    ts = row.get("timestamp_ms")
                    if ts is None:
                        continue

                    ts = int(float(ts))

                    if first_ts is None:
                        first_ts = ts

                    last_ts = ts
        except Exception:
            return "-"

        if first_ts and last_ts:

            if first_ts > 10_000_000_000_000:
                first_ts = first_ts / 1000

            if last_ts > 10_000_000_000_000:
                last_ts = last_ts / 1000

            first_dt = datetime.fromtimestamp(first_ts / 1000).strftime("%d.%m.%Y")
            last_dt = datetime.fromtimestamp(last_ts / 1000).strftime("%d.%m.%Y")

            return f"{first_dt}  →  {last_dt}"

        return "-"

    # ─────────────────────────────────────────────
    # FIELD
    # ─────────────────────────────────────────────
    def _field(self, parent, row, name):
        ttk.Label(
            parent, text=name, style="Dim.TLabel"
        ).grid(row=row, column=0, sticky="w", pady=2)

        var = tk.StringVar(value="-")
        lbl = ttk.Label(
            parent,
            textvariable=var,
            style="Value.TLabel",
            width=26,
            anchor="e",
        )
        lbl.grid(row=row, column=1, sticky="e", pady=2)

        self.vars[name] = (var, lbl)

    # ─────────────────────────────────────────────
    # HEADER (zentriert, sauber strukturiert)
    # ─────────────────────────────────────────────
    def _build_ui(self, parent):

        main = ttk.Frame(parent, padding=14)
        main.pack(fill="x", expand=False)

        main.grid_anchor("center")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        # LEFT BLOCK
        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="n", padx=20)

        ttk.Label(
            left,
            text="TRADE SUMMARY",
            style="Title.TLabel",
            anchor="center",
            justify="center"
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        for i, f in enumerate(
            ["TRADES", "TP_COUNT", "SL_COUNT", "WINRATE"],
            start=1,
        ):
            self._field(left, i, f)

        # RIGHT BLOCK
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="n", padx=20)
        right.grid_columnconfigure(0, weight=1)
        right.grid_columnconfigure(1, weight=1)

        ttk.Label(
            right,
            text="PNL",
            style="Title.TLabel",
            anchor="center",
            justify="center"
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        row_index = 1

        for f in ["PNL_NETTO", "PNL_TP", "PNL_SL"]:
            self._field(right, row_index, f)
            row_index += 1

        self._field(right, row_index, "Time_Range")

    # ─────────────────────────────────────────────
    # EQUITY RESET (bei Bot-Neustart / CSV Reset)
    # ─────────────────────────────────────────────
    def _reset_equity_state(self):
        self._eq_trades = []
        self._eq_pnl_netto = []
        self._eq_pnl_tp = []
        self._eq_pnl_sl = []
        self._eq_last_line_count = 0

        if hasattr(self, "line_total"):
            self.line_total.set_data([], [])
            self.line_win.set_data([], [])
            self.line_loss.set_data([], [])
            self.eq_canvas.draw_idle()

        # --------------------------------------------------
        # BACKTEST TOTAL SIZE + CSV TIMESTAMP RANGE
        # --------------------------------------------------
        self._workspace_rows_total = 0
        self._csv_start_ts = None
        self._csv_end_ts = None

        try:
            if os.path.exists(WORKSPACE_PATH):

                with open(WORKSPACE_PATH, "r", encoding="utf-8") as f:

                    reader = csv.reader(f)
                    header = next(reader, None)

                    first_row = next(reader, None)

                    last_row = None
                    rows = 0

                    for row in reader:
                        last_row = row
                        rows += 1

                    self._workspace_rows_total = max(rows - Config.WINDOW_SIZE, 1)

                    if first_row:
                        self._csv_start_ts = first_row[0]

                    if last_row:
                        self._csv_end_ts = last_row[0]

        except Exception:

            self._workspace_rows_total = 0
            self._csv_start_ts = None
            self._csv_end_ts = None
    # ─────────────────────────────────────────────
    # EQUITY WINDOW
    # ─────────────────────────────────────────────
    def _build_equity_window(self, parent):
        main = ttk.Frame(parent)
        main.pack(fill="both", expand=True)
        
        plot_frame = ttk.Frame(main)
        plot_frame.pack(fill="both", expand=True)

        fig = Figure(figsize=(9, 5), dpi=100, facecolor=BG)
        self.eq_ax = fig.add_subplot(111)
        self.eq_ax.set_facecolor(BG)
        self.eq_ax.tick_params(colors=FG)

        for spine in self.eq_ax.spines.values():
            spine.set_color(FG_DIM)

        self.eq_ax.grid(True, color="#1e1e1e", linestyle="-", linewidth=0.5)

        # --------------------------------------------------
        # RL Heatmap Background
        # --------------------------------------------------
        matrix = self._draw_rl_heatmap()

        if matrix is not None:
            self.rl_heatmap = self.eq_ax.imshow(
                matrix,
                cmap=CMAP,
                alpha=0.50,
                aspect="auto",
                origin="lower",
                extent=(0, 1, 0, 1),
                transform=self.eq_ax.transAxes,
                zorder=0
            )

            self.cbar = fig.colorbar(
                self.rl_heatmap,
                ax=self.eq_ax,
                location="right",   # ← hier geändert
                fraction=0.03,
                pad=0.02
            )

            self.cbar.set_label("RL Score", color=FG)
            self.cbar.ax.yaxis.set_tick_params(color=FG)
            self.cbar.outline.set_edgecolor(FG_DIM)
            self.cbar.ax.set_facecolor(BG)

            for label in self.cbar.ax.get_yticklabels():
                label.set_color(FG)

        self.line_total, = self.eq_ax.plot([], [], label="PNL_NETTO", color=green)
        self.line_win, = self.eq_ax.plot([], [], label="PNL_TP", color=orange)
        self.line_loss, = self.eq_ax.plot([], [], label="PNL_SL", color=red)

        legend = self.eq_ax.legend(facecolor=BG, edgecolor=FG_DIM)
        for text in legend.get_texts():
            text.set_color(FG)

        self.eq_ax.set_xlabel("Trades", color=FG)
        self.eq_ax.set_ylabel("PnL", color=FG)

        # --------------------------------------------------
        # BACKTEST PROGRESS BAR
        # --------------------------------------------------
        if Config.MODE == 'BACKTEST': #LIVE
            progress_frame = ttk.Frame(plot_frame)
            progress_frame.pack(fill="x", padx=100, pady=(6, 4))

            self.progress = ttk.Progressbar(
                progress_frame,
                orient="horizontal",
                mode="determinate"
            )

            self.progress.pack(side="left", fill="x", expand=True)

            self.progress_text = tk.Label(
                progress_frame,
                text="0%",
                fg=FG,
                bg=BG,
                font=("Arial", 12),
                relief= "raised",
                stat= 'normal',
                width=6,
                anchor="center"
            )

            self.progress_text.pack(side="left", padx=(5, 10))

        self.eq_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.eq_canvas.draw_idle()
        self.eq_canvas.get_tk_widget().configure(bg=BG, highlightthickness=0)
        self.eq_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 60))   

    # ─────────────────────────────────────────────
    # READ STATS
    # ─────────────────────────────────────────────
    def _read_stats(self):
        if not os.path.exists(STATS_PATH):
            return {}

        try:
            with open(STATS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    # ─────────────────────────────────────────────
    # LOOP UPDATE
    # ─────────────────────────────────────────────
    def _update_loop(self):
        stats = self._read_stats()

        trades = stats.get("trades", 0)
        tp = stats.get("tp", 0)
        sl = stats.get("sl", 0)

        pnl_netto = stats.get("pnl_netto", 0.0)
        pnl_tp = stats.get("pnl_tp", 0.0)
        pnl_sl = stats.get("pnl_sl", 0.0)

        winrate = (tp / trades * 100.0) if trades > 0 else 0.0

        self.vars["TRADES"][0].set(trades)
        self.vars["TP_COUNT"][0].set(tp)
        self.vars["SL_COUNT"][0].set(sl)
        self.vars["WINRATE"][0].set(f"{winrate:.2f} %")

        self.vars["PNL_NETTO"][0].set(f"{pnl_netto:.4f}")
        self.vars["PNL_TP"][0].set(f"{pnl_tp:.4f}")
        self.vars["PNL_SL"][0].set(f"{pnl_sl:.4f}")

        ws_range = self.print_Time_Range(WORKSPACE_PATH)
        self.vars["Time_Range"][0].set(ws_range)

        self.vars["PNL_NETTO"][1].configure(foreground=green)
        self.vars["PNL_TP"][1].configure(foreground=orange)
        self.vars["PNL_SL"][1].configure(foreground=red)

        self._update_equity_plot()

        self.root.after(REFRESH_MS, self._update_loop)

    # ─────────────────────────────────────────────
    # EQUITY UPDATE
    # ─────────────────────────────────────────────
    def _update_equity_plot(self):

        if not os.path.exists(EQUITY_PATH):
            return

        try:
            with open(EQUITY_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()

            total_lines = len(lines)

            if total_lines < self._eq_last_line_count:
                self._reset_equity_state()
                self._load_full_equity()

            if total_lines > self._eq_last_line_count:

                new_lines = lines[self._eq_last_line_count:]
                self._eq_last_line_count = total_lines

                for line in new_lines:
                    parts = line.strip().split(",")
                    if len(parts) != 4:
                        continue
                    if parts[0] == "trade":
                        continue

                    self._eq_trades.append(int(parts[0]))
                    self._eq_pnl_netto.append(float(parts[1]))
                    self._eq_pnl_tp.append(float(parts[2]))
                    self._eq_pnl_sl.append(float(parts[3]))

        except Exception:
            return

        if not self._eq_trades:
            return

        # --------------------------------------------------
        # RL HEATMAP LIVE UPDATE (mit mtime-Prüfung)
        # --------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path_abs_v2 = os.path.join(base_dir, "bot_memory", "mcm_meta_vector_memory.json")
        path_rel_v2 = os.path.join("bot_memory", "mcm_meta_vector_memory.json")
        path_abs_legacy = os.path.join(base_dir, "bot_memory", "mcm_memory_engine.json")
        path_rel_legacy = os.path.join("bot_memory", "mcm_memory_engine.json")

        if os.path.exists(path_abs_v2):
            path = path_abs_v2
        elif os.path.exists(path_rel_v2):
            path = path_rel_v2
        elif os.path.exists(path_abs_legacy):
            path = path_abs_legacy
        else:
            path = path_rel_legacy

        if os.path.exists(path):
            try:
                mtime = os.path.getmtime(path)
            except Exception:
                mtime = 0.0

            if mtime > self._rl_last_mtime:

                matrix = self._draw_rl_heatmap()

                if matrix is not None:

                    if self.rl_heatmap is None:
                        self.rl_heatmap = self.eq_ax.imshow(
                            matrix,
                            cmap=CMAP,
                            alpha=0.18,
                            aspect="auto",
                            origin="lower",
                            extent=(0, 1, 0, 1),
                            transform=self.eq_ax.transAxes,
                            zorder=0
                        )
                    else:
                        self.rl_heatmap.set_data(matrix)

                    self._rl_last_mtime = mtime

        self.line_total.set_data(self._eq_trades, self._eq_pnl_netto)
        self.line_win.set_data(self._eq_trades, self._eq_pnl_tp)
        self.line_loss.set_data(self._eq_trades, self._eq_pnl_sl)

        self.eq_ax.relim()
        self.eq_ax.autoscale_view()

        self.eq_canvas.draw_idle()
        # --------------------------------------------------
        # BACKTEST PROGRESS UPDATE
        # --------------------------------------------------
        if self._workspace_rows_total > 0 and Config.MODE == 'BACKTEST':

            current_ts = None

            try:

                if os.path.exists(STATS_PATH):

                    with open(STATS_PATH, "r", encoding="utf-8") as f:

                        stats_data = json.load(f)

                        current_ts = stats_data.get("current_timestamp")

            except Exception:

                current_ts = None


            ts_value = None

            if current_ts:

                try:

                    ts_value = float(current_ts)

                    # µs → s
                    if ts_value > 10_000_000_000_000:
                        ts_value /= 1_000_000.0

                    # ms → s
                    elif ts_value > 10_000_000_000:
                        ts_value /= 1_000.0

                    if not (1_000_000_000 < ts_value < 4_000_000_000):
                        ts_value = None

                except Exception:

                    ts_value = None


            progress = 0.0

            if ts_value and self._csv_start_ts and self._csv_end_ts:

                try:

                    start_ts = float(self._csv_start_ts)
                    end_ts = float(self._csv_end_ts)

                    if start_ts > 10_000_000_000_000:
                        start_ts /= 1_000_000.0
                    elif start_ts > 10_000_000_000:
                        start_ts /= 1_000.0

                    if end_ts > 10_000_000_000_000:
                        end_ts /= 1_000_000.0
                    elif end_ts > 10_000_000_000:
                        end_ts /= 1_000.0

                    if end_ts > start_ts:
                        progress = (ts_value - start_ts) / (end_ts - start_ts)
                        progress = max(0.0, min(progress, 1.0))

                except Exception:

                    progress = 0.0

            percent = int(progress * 100)

            if percent < 0:
                percent = 0
            elif percent > 100:
                percent = 100

            self.progress["value"] = percent
            self.progress_text.config(text=f"{percent}%")
# ==================================================
# START
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    TradeStatsGUI(root)
    root.mainloop()
