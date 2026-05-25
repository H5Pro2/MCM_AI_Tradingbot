from __future__ import annotations

import argparse
import json
import math
import re
import tkinter as tk
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure


REFRESH_MS = 350
WINDOW_SIZE = "980x680"
WINDOW_MIN_SIZE = (720, 480)
MAX_DRAW_NEURONS = 420
GRID_SIZE = 180
HEAT_SIGMA = 0.045

C = {
    "bg_root": "#000000",
    "bg_card": "#181c24",
    "bg_chart": "#0b0f16",
    "border": "#252a36",
    "text_label": "#4e5f87",
    "text_hi": "#e8eaf0",
    "text_lo": "#4a5168",
    "green": "#4caf78",
    "blue": "#5b8dd9",
    "orange": "#d4894a",
    "red": "#c05050",
    "violet": "#8a6fdb",
}

HEAT_CMAP = LinearSegmentedColormap.from_list(
    "dio_neuron_heat",
    ["#000000", "#101724", "#183047", "#235364", "#367474", "#d4894a"],
)

matplotlib.rcParams.update(
    {
        "figure.facecolor": C["bg_card"],
        "axes.facecolor": C["bg_chart"],
        "axes.edgecolor": C["border"],
        "xtick.color": C["text_lo"],
        "ytick.color": C["text_lo"],
        "text.color": C["text_label"],
        "font.family": "monospace",
        "font.size": 8,
    }
)


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(float(low), min(float(high), float(value)))


def safe_load_json(path: Path) -> dict:
    try:
        if not path.exists():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def resolve_debug_dir(base_dir: Path, requested: str | None = None) -> Path:
    debug_root = base_dir / "debug"
    if requested:
        candidate = Path(requested)
        if not candidate.is_absolute():
            candidate = debug_root / requested
        if candidate.exists():
            return candidate

    runs: list[tuple[int, float, Path]] = []
    if debug_root.exists():
        for child in debug_root.iterdir():
            if not child.is_dir():
                continue
            match = re.fullmatch(r"debug_lauf_(\d+)", child.name)
            if match:
                runs.append((int(match.group(1)), child.stat().st_mtime, child))
    if runs:
        return sorted(runs, key=lambda item: (item[0], item[1]))[-1][2]
    return debug_root


def metric_color(value: float) -> str:
    value = clamp(value)
    if value >= 0.66:
        return C["green"]
    if value >= 0.36:
        return C["blue"]
    return C["text_lo"]


class NeuronenGui:
    def __init__(self, root: tk.Tk, base_dir: Path, debug_run: str | None = None, link_mode: str = "both"):
        self.root = root
        self.base_dir = Path(base_dir).resolve()
        self.debug_run = debug_run
        self.link_mode = str(link_mode or "both").lower()
        if self.link_mode not in {"real", "field", "both", "none"}:
            self.link_mode = "both"
        self.debug_dir = resolve_debug_dir(self.base_dir, debug_run)
        self.snapshot_path = self.debug_dir / "bot_inner_snapshot.json"
        self._after_id = None
        self._last_snapshot_signature: tuple[int, int] | None = None
        self._fixed_layout_cache: dict[int, np.ndarray] = {}
        self._link_cache: dict[int, list[tuple[int, int]]] = {}

        self.root.title("DIO Neuronen GUI")
        self.root.configure(bg=C["bg_root"])
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*WINDOW_MIN_SIZE)

        self._build_layout()
        self._refresh()

    def _build_layout(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        frame = tk.Frame(
            self.root,
            bg=C["bg_card"],
            highlightbackground=C["border"],
            highlightthickness=1,
        )
        frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        header = tk.Frame(frame, bg=C["bg_card"], height=34)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        tk.Label(
            header,
            text="MCM-NEURONENAKTIVITÄT",
            bg=C["bg_card"],
            fg=C["text_label"],
            font=("Courier New", 9, "bold"),
            anchor="w",
            padx=10,
        ).grid(row=0, column=0, sticky="ew")

        self.status_label = tk.Label(
            header,
            text="-",
            bg=C["bg_card"],
            fg=C["text_lo"],
            font=("Courier New", 8, "bold"),
            anchor="e",
            padx=10,
        )
        self.status_label.grid(row=0, column=1, sticky="e")

        tk.Frame(frame, bg=C["border"], height=1).grid(row=1, column=0, sticky="new")

        plot_frame = tk.Frame(frame, bg=C["bg_card"])
        plot_frame.grid(row=1, column=0, sticky="nsew", pady=(1, 0))

        self.fig = Figure(figsize=(9.4, 6.1), dpi=100)
        self.fig.subplots_adjust(left=0.018, right=0.988, top=0.985, bottom=0.025)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _refresh(self):
        self.debug_dir = resolve_debug_dir(self.base_dir, self.debug_run)
        self.snapshot_path = self.debug_dir / "bot_inner_snapshot.json"
        signature = self._snapshot_signature(self.snapshot_path)
        if signature is not None and signature == self._last_snapshot_signature:
            self._after_id = self.root.after(REFRESH_MS, self._refresh)
            return
        self._last_snapshot_signature = signature

        snapshot = safe_load_json(self.snapshot_path)
        field_state = dict(snapshot.get("inner_field_perception_state", {}) or {})
        self._draw(field_state)
        self._after_id = self.root.after(REFRESH_MS, self._refresh)

    def _snapshot_signature(self, path: Path) -> tuple[int, int] | None:
        try:
            stat = path.stat()
            return (int(stat.st_mtime_ns), int(stat.st_size))
        except Exception:
            return None

    def _extract_source_neurons(self, field_state: dict) -> list[dict]:
        population = field_state.get("field_neuron_population", [])
        if isinstance(population, list):
            return [dict(item or {}) for item in population if isinstance(item, dict)]
        return []

    def _tissue_count(self, field_state: dict, source: list[dict]) -> int:
        configured = int(field_state.get("field_neuron_count", 0) or 0)
        if configured <= 0:
            configured = len(source) or 64
        return min(max(configured, len(source), 24), MAX_DRAW_NEURONS)

    def _layout(self, count: int, source: list[dict]) -> np.ndarray:
        n = max(1, int(count or 1))
        if n not in self._fixed_layout_cache:
            cols = int(math.ceil(math.sqrt(n * 1.75)))
            rows = int(math.ceil(n / max(1, cols)))
            points = []
            for row in range(rows):
                for col in range(cols):
                    if len(points) >= n:
                        break
                    x = col / max(1, cols - 1)
                    y = row / max(1, rows - 1)
                    if row % 2:
                        x += 0.5 / max(2, cols)
                    x += math.sin((row + 1) * (col + 3)) * 0.004
                    y += math.cos((col + 1) * (row + 2)) * 0.004
                    points.append((clamp(x, 0.025, 0.975), clamp(1.0 - y, 0.035, 0.965)))
            self._fixed_layout_cache[n] = np.asarray(points, dtype=float)

        layout = self._fixed_layout_cache[n].copy()
        source_positions = []
        for item in source:
            position = item.get("field_position", [])
            if isinstance(position, list) and len(position) >= 2:
                source_positions.append([safe_float(position[0]), safe_float(position[1])])
        if len(source_positions) >= 8:
            source_array = np.asarray(source_positions[: min(len(source_positions), n)], dtype=float)
            min_xy = np.min(source_array, axis=0)
            max_xy = np.max(source_array, axis=0)
            span = np.maximum(max_xy - min_xy, 1e-9)
            normalized = (source_array - min_xy) / span
            usable = min(len(layout), len(normalized))
            layout[:usable, 0] = 0.035 + normalized[:usable, 0] * 0.93
            layout[:usable, 1] = 0.045 + (1.0 - normalized[:usable, 1]) * 0.91
        return layout

    def _real_links(self, layout: np.ndarray, source: list[dict]) -> list[tuple[int, int]]:
        count = len(layout)
        index_map = {}
        for local_index, item in enumerate(source[:count]):
            agent_index = int(item.get("agent_index", local_index) or local_index)
            index_map[agent_index] = local_index

        links: set[tuple[int, int]] = set()
        for local_index, item in enumerate(source[:count]):
            source_agent = int(item.get("agent_index", local_index) or local_index)
            source_local = index_map.get(source_agent, local_index)
            neighbors = item.get("topology_neighbors", [])
            if not isinstance(neighbors, list):
                continue
            for neighbor in neighbors:
                try:
                    neighbor_agent = int(neighbor)
                except Exception:
                    continue
                if neighbor_agent in index_map:
                    a, b = sorted((source_local, index_map[neighbor_agent]))
                    if a != b:
                        links.add((a, b))

        return sorted(links)

    def _field_links(self, layout: np.ndarray) -> list[tuple[int, int]]:
        count = len(layout)
        if count in self._link_cache:
            return self._link_cache[count]

        links: set[tuple[int, int]] = set()
        if count <= 1:
            return []

        for index in range(count):
            delta = layout - layout[index]
            dist = np.sqrt(np.sum(delta * delta, axis=1))
            order = np.argsort(dist)
            linked = 0
            for neighbor in order:
                ni = int(neighbor)
                if ni == index:
                    continue
                if float(dist[ni]) > 0.115:
                    break
                a, b = sorted((index, ni))
                links.add((a, b))
                linked += 1
                if linked >= 4:
                    break

        resolved = sorted(links)
        self._link_cache[count] = resolved
        return resolved

    def _values(self, field_state: dict, source: list[dict], count: int) -> dict[str, np.ndarray]:
        mean_activation = safe_float(field_state.get("field_neuron_activation_mean"), 0.0)
        mean_pressure = safe_float(field_state.get("field_neuron_regulation_pressure_mean"), 0.0)
        mean_memory = safe_float(field_state.get("field_neuron_memory_norm_mean"), 0.0)
        mean_coupling = safe_float(field_state.get("field_neuron_coupling_norm_mean"), 0.0)
        mean_external = safe_float(field_state.get("field_neuron_external_impulse_norm_mean"), mean_activation)

        activation = np.full(count, mean_activation, dtype=float)
        pressure = np.full(count, mean_pressure, dtype=float)
        memory = np.full(count, mean_memory, dtype=float)
        coupling = np.full(count, mean_coupling, dtype=float)
        external = np.full(count, mean_external, dtype=float)

        for local_index, item in enumerate(source[:count]):
            activation[local_index] = safe_float(item.get("activation"), activation[local_index])
            pressure[local_index] = safe_float(item.get("regulation_pressure"), pressure[local_index])
            memory[local_index] = safe_float(item.get("memory_norm"), memory[local_index])
            coupling[local_index] = safe_float(item.get("coupling_norm"), coupling[local_index])
            external[local_index] = safe_float(item.get("external_impulse_norm"), external[local_index])

        visual = np.clip(
            (activation * 0.58) + (external * 0.16) + (memory * 0.12) + (coupling * 0.10) + (pressure * 0.04),
            0.0,
            1.0,
        )
        return {
            "activation": np.clip(activation, 0.0, 1.0),
            "pressure": np.clip(pressure, 0.0, 1.0),
            "memory": np.clip(memory, 0.0, 1.0),
            "coupling": np.clip(coupling, 0.0, 1.0),
            "external": np.clip(external, 0.0, 1.0),
            "visual": visual,
        }

    def _heat(self, layout: np.ndarray, visual: np.ndarray) -> np.ndarray:
        grid = np.linspace(0.0, 1.0, GRID_SIZE)
        xx, yy = np.meshgrid(grid, grid)
        heat = np.zeros_like(xx, dtype=float)

        active_count = min(180, len(visual))
        for index in np.argsort(visual)[-active_count:]:
            strength = float(visual[int(index)])
            if strength <= 0.015:
                continue
            x, y = layout[int(index)]
            dist2 = ((xx - x) ** 2) + ((yy - y) ** 2)
            heat += strength * np.exp(-dist2 / (2.0 * HEAT_SIGMA * HEAT_SIGMA))

        max_value = float(np.max(heat)) if heat.size else 0.0
        if max_value > 1e-9:
            heat = heat / max_value
        return heat

    def _draw(self, field_state: dict):
        self.ax.clear()
        self.ax.set_facecolor(C["bg_chart"])
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)
        self.ax.set_aspect("auto")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_color(C["border"])

        source = self._extract_source_neurons(field_state)
        count = self._tissue_count(field_state, source)
        if count <= 0:
            self.ax.text(0.5, 0.5, "KEINE NEURONENDATEN", ha="center", va="center", color=C["text_lo"])
            self.canvas.draw_idle()
            return

        layout = self._layout(count, source)
        real_links = self._real_links(layout, source)
        field_links = self._field_links(layout)
        values = self._values(field_state, source, count)
        heat = self._heat(layout, values["visual"])

        activation_mean = safe_float(field_state.get("field_neuron_activation_mean"), float(np.mean(values["activation"])))
        pressure_mean = safe_float(field_state.get("field_neuron_regulation_pressure_mean"), float(np.mean(values["pressure"])))
        coupling_mean = safe_float(field_state.get("field_neuron_coupling_norm_mean"), float(np.mean(values["coupling"])))
        island_count = int(field_state.get("field_activity_island_count", 0) or 0)
        self.status_label.configure(
            text=(
                f"{self.debug_dir.name} | n={int(field_state.get('field_neuron_count', count) or count)} "
                f"act={activation_mean:.2f} kopplung={coupling_mean:.2f} druck={pressure_mean:.2f} "
                f"inseln={island_count} real={len(real_links)} feld={len(field_links)}"
            )
        )

        self.ax.imshow(
            heat,
            extent=(0.0, 1.0, 0.0, 1.0),
            origin="lower",
            cmap=HEAT_CMAP,
            alpha=0.38,
            interpolation="bicubic",
            aspect="auto",
            zorder=1,
        )

        max_heat = float(np.max(heat)) if heat.size else 0.0
        if max_heat > 0.10:
            levels = [level for level in (0.24, 0.44, 0.66) if level < max_heat]
            if levels:
                self.ax.contour(
                    np.linspace(0.0, 1.0, heat.shape[1]),
                    np.linspace(0.0, 1.0, heat.shape[0]),
                    heat,
                    levels=levels,
                    colors=[C["blue"], C["green"], C["orange"]][: len(levels)],
                    linewidths=[0.35, 0.48, 0.65][: len(levels)],
                    alpha=0.24,
                    zorder=2,
                )

        if self.link_mode in {"field", "both"} and field_links:
            field_lines = [[layout[a], layout[b]] for a, b in field_links if a < len(layout) and b < len(layout)]
            if field_lines:
                self.ax.add_collection(
                    LineCollection(
                        field_lines,
                        colors="#2f4058",
                        linewidths=0.18,
                        alpha=0.10 if self.link_mode == "both" else 0.18,
                        zorder=3,
                    )
                )

        if self.link_mode in {"real", "both"} and real_links:
            real_lines = [[layout[a], layout[b]] for a, b in real_links if a < len(layout) and b < len(layout)]
            if real_lines:
                self.ax.add_collection(
                    LineCollection(
                        real_lines,
                        colors=C["green"],
                        linewidths=0.65,
                        alpha=0.46,
                        zorder=4.4,
                    )
                )

        active_source_links = real_links if self.link_mode == "real" else field_links if self.link_mode == "field" else sorted(set(real_links) | set(field_links))
        if self.link_mode != "none" and active_source_links:
            real_link_set = set(real_links)
            scored = []
            for a, b in active_source_links:
                if a >= len(layout) or b >= len(layout):
                    continue
                strength = float((values["visual"][a] + values["visual"][b]) * 0.5)
                strength += float((values["coupling"][a] + values["coupling"][b]) * 0.22)
                is_real = tuple(sorted((a, b))) in real_link_set
                scored.append((strength, [layout[a], layout[b]], is_real))

            if scored:
                threshold = max(0.08, float(np.percentile([item[0] for item in scored], 70.0)))
                active = [(value, line, is_real) for value, line, is_real in scored if value >= threshold]
                active = sorted(active, key=lambda item: item[0], reverse=True)[:260]
                if active:
                    max_strength = max(value for value, _, _ in active)
                    for is_real_group, color, alpha, zorder in (
                        (False, C["blue"], 0.30, 4.0),
                        (True, C["green"], 0.62, 4.8),
                    ):
                        group = [(value, line) for value, line, is_real in active if bool(is_real) == is_real_group]
                        if not group:
                            continue
                        self.ax.add_collection(
                            LineCollection(
                                [line for _, line in group],
                                colors=color,
                                linewidths=[0.25 + clamp(value / max_strength) * (1.55 if is_real_group else 1.05) for value, _ in group],
                                alpha=alpha,
                                zorder=zorder,
                            )
                        )

        legend_parts = []
        if self.link_mode in {"real", "both"}:
            legend_parts.append("gruen = echte topology_neighbors")
        if self.link_mode in {"field", "both"}:
            legend_parts.append("blau = rekonstruierte Feldnaehe")
        if legend_parts:
            self.ax.text(
                0.012,
                0.018,
                " | ".join(legend_parts),
                transform=self.ax.transAxes,
                ha="left",
                va="bottom",
                color=C["text_lo"],
                alpha=0.78,
                fontsize=7,
                zorder=9,
            )

        visual = values["visual"]
        memory = values["memory"]
        pressure = values["pressure"]
        node_colors = [metric_color(float(value)) for value in visual]
        node_sizes = 5.0 + visual * 30.0 + memory * 14.0
        glow_sizes = 26.0 + visual * 155.0 + pressure * 72.0

        self.ax.scatter(
            layout[:, 0],
            layout[:, 1],
            s=glow_sizes,
            c=node_colors,
            alpha=0.08 + visual * 0.16,
            linewidths=0.0,
            zorder=5,
        )
        self.ax.scatter(
            layout[:, 0],
            layout[:, 1],
            s=node_sizes,
            c=node_colors,
            alpha=0.72 + visual * 0.16,
            edgecolors="#102030",
            linewidths=0.16,
            zorder=6,
        )

        for metric, color, limit in ((memory, C["violet"], 42), (pressure, C["red"], 32), (values["external"], C["orange"], 28)):
            if len(metric) <= 0 or float(np.max(metric)) <= 0.04:
                continue
            selected = [int(index) for index in np.argsort(metric)[-limit:] if float(metric[int(index)]) > 0.04]
            if selected:
                selected_arr = np.asarray(selected, dtype=int)
                self.ax.scatter(
                    layout[selected_arr, 0],
                    layout[selected_arr, 1],
                    s=18.0 + metric[selected_arr] * 120.0,
                    c=color,
                    alpha=0.055 + metric[selected_arr] * 0.08,
                    linewidths=0.0,
                    zorder=5.6,
                )

        self.canvas.draw_idle()


def main():
    parser = argparse.ArgumentParser(description="Schlichte DIO-Neuronenaktivitäts-GUI")
    parser.add_argument("--base-dir", default=".", help="Projektbasisordner")
    parser.add_argument("--debug-run", default=None, help="debug_lauf_x oder absoluter Debug-Pfad")
    parser.add_argument(
        "--links",
        default="both",
        choices=("real", "field", "both", "none"),
        help="Verbindungsebene: real=Debug-Nachbarn, field=rekonstruierte Feldnaehe, both=beides, none=keine Linien",
    )
    args = parser.parse_args()

    root = tk.Tk()
    app = NeuronenGui(root, Path(args.base_dir), args.debug_run, link_mode=args.links)

    def on_close():
        if app._after_id:
            root.after_cancel(app._after_id)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
