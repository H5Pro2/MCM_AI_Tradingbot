# ============================================================
# debug_reader.py
# ============================================================
#   msg
#   Typ: beliebig → str(msg)
#   Bedeutung: zu schreibender Inhalt (eine Zeile)
#   path = "debug/debug.txt"
#   Typ: str
#   Bedeutung: Zieldatei
#   mode = "a"
#   Typ: str
#   "a" = anhängen
#   "w" = überschreiben
#   reset_on_start = True
#   Typ: bool
#   True = Datei einmalig beim Start löschen
#   False = Datei nie automatisch löschen
#   write_once = False
#   Typ: bool
#   True = immer mode="w" → nur eine Zeile, wird überschrieben
#   False = mode bleibt wie übergeben ("a" oder "w")
# ============================================================
import os
import time
import atexit
from config import Config
_RESET_DONE = set()
_DEBUG_COUNTERS = {}
_PROFILE_HEADER_DONE = set()
_FILE_PROFILE_HEADER_DONE = set()
_DEBUG_RUN_DIR = None
_WRITE_BUFFERS = {}
_WRITE_BUFFER_COUNTS = {}
_WRITE_BUFFER_LAST_FLUSH = {}
_BUFFER_FLUSHING = False

_DEBUG_FILE_GROUPS = {
    "trade_stats.json": "gui",
    "trade_equity.csv": "gui",
    "mcm_field_decision_protocol.csv": "core",
    "mcm_neuro_transition_protocol.csv": "core",
    "mcm_thought_seed_protocol.csv": "core",
    "mcm_thought_digest_protocol.csv": "core",
    "mcm_outcome_debug.csv": "core",
    "outcome_records.jsonl": "core",
    "mcm_position_intervention_protocol.csv": "position",
    "mcm_exit_candidate_observe.csv": "position",
    "mcm_exit_candidate_replay.csv": "position",
    "mcm_exit_candidate_replay_debug.log": "position",
    "mcm_form_symbol_protocol.csv": "language",
    "mcm_memory_thinking_protocol.csv": "language",
    "mcm_idle_thinking_protocol.csv": "language",
    "mcm_visual_cortex_protocol.csv": "perception",
    "mcm_strategic_window_protocol.csv": "perception",
    "mcm_active_contact_protocol.csv": "perception",
    "mcm_target_expectation_protocol.csv": "perception",
    "mcm_profile.csv": "performance",
    "mcm_file_write_profile.csv": "performance",
    "mcm_state_debug.csv": "research",
    "mcm_decision_debug.csv": "research",
    "debug.csv": "research",
    "debug.txt": "research",
}

_DEBUG_GROUP_NAMES = {
    "gui",
    "core",
    "position",
    "language",
    "perception",
    "performance",
    "research",
    "topology",
}

def _debug_group_for_filename(filename):
    if not bool(getattr(Config, "DEBUG_GROUPED_DIRS", False)):
        return ""
    name = os.path.basename(str(filename or "").replace("\\", "/")).strip()
    if not name:
        return ""
    if name in _DEBUG_FILE_GROUPS:
        return str(_DEBUG_FILE_GROUPS.get(name, "") or "")
    if name.startswith("mcm_visual") or "cortex" in name:
        return "perception"
    if "thought" in name or "form_symbol" in name or "memory_thinking" in name:
        return "language"
    if "position" in name or "exit_candidate" in name:
        return "position"
    if "profile" in name or "write" in name:
        return "performance"
    if name.startswith("mcm_") or name.startswith("outcome_"):
        return "research"
    return ""

def _debug_grouped_parts(parts):
    cleaned = [str(part).strip("/\\") for part in parts if str(part or "").strip("/\\")]
    if not cleaned or not bool(getattr(Config, "DEBUG_GROUPED_DIRS", False)):
        return cleaned
    if len(cleaned) > 1 and cleaned[0] in _DEBUG_GROUP_NAMES:
        return cleaned
    if len(cleaned) > 1:
        return cleaned
    group = _debug_group_for_filename(cleaned[-1])
    if not group:
        return cleaned
    return [group] + cleaned

def _debug_write_mode():
    mode = str(getattr(Config, "DEBUG_WRITE_MODE", "immediate") or "immediate").strip().lower()
    if mode not in {"immediate", "buffered", "buffered_safe"}:
        return "immediate"
    return mode

def _buffered_debug_enabled(path=None, mode="a", write_once=False):
    if _debug_write_mode() == "immediate":
        return False
    if str(mode or "a") != "a":
        return False
    if bool(write_once):
        return False
    normalized = str(path or "").replace("\\", "/")
    if normalized.endswith("mcm_file_write_profile.csv"):
        return False
    if normalized.endswith("trade_equity.csv"):
        return False
    return True

def _write_text_immediate(path, text, mode="a", operation="write"):
    _ensure_dir(path)
    profile_start = time.perf_counter()
    with open(path, mode, encoding="utf-8") as f:
        f.write(str(text or ""))
    dbr_file_write_profile(
        path,
        (time.perf_counter() - profile_start) * 1000.0,
        bytes_written=len(str(text or "").encode("utf-8")),
        operation=operation,
    )

def dbr_flush_buffers(path: str | None = None):
    global _BUFFER_FLUSHING

    if _BUFFER_FLUSHING:
        return

    _BUFFER_FLUSHING = True
    try:
        paths = [dbr_resolve_path(path)] if path else list(_WRITE_BUFFERS.keys())
        for resolved_path in list(paths or []):
            lines = list(_WRITE_BUFFERS.get(resolved_path, []) or [])
            if not lines:
                continue

            text = "".join(str(item or "") for item in lines)
            _WRITE_BUFFERS[resolved_path] = []
            _WRITE_BUFFER_COUNTS[resolved_path] = 0
            _WRITE_BUFFER_LAST_FLUSH[resolved_path] = float(time.time())

            try:
                _write_text_immediate(
                    resolved_path,
                    text,
                    mode="a",
                    operation=f"buffer_flush:{len(lines)}",
                )
            except Exception:
                try:
                    _WRITE_BUFFERS[resolved_path] = lines + list(_WRITE_BUFFERS.get(resolved_path, []) or [])
                    _WRITE_BUFFER_COUNTS[resolved_path] = len(_WRITE_BUFFERS.get(resolved_path, []) or [])
                except Exception:
                    pass
    finally:
        _BUFFER_FLUSHING = False

def _buffer_debug_text(path, text):
    resolved_path = dbr_resolve_path(path)
    line_text = str(text or "")
    if not line_text:
        return

    _WRITE_BUFFERS.setdefault(resolved_path, []).append(line_text)
    count = int(_WRITE_BUFFER_COUNTS.get(resolved_path, 0) or 0) + 1
    _WRITE_BUFFER_COUNTS[resolved_path] = count

    mode = _debug_write_mode()
    max_lines = max(1, int(getattr(Config, "DEBUG_BUFFER_MAX_LINES_PER_FILE", 50000) or 50000))
    if count >= max_lines:
        dbr_flush_buffers(resolved_path)
        return

    if mode != "buffered_safe":
        return

    every_n = max(1, int(getattr(Config, "DEBUG_BUFFER_FLUSH_EVERY_N", 1000) or 1000))
    seconds = max(0.0, float(getattr(Config, "DEBUG_BUFFER_FLUSH_SECONDS", 10.0) or 10.0))
    last_flush = float(_WRITE_BUFFER_LAST_FLUSH.get(resolved_path, 0.0) or 0.0)
    now_ts = float(time.time())
    due_by_count = count >= every_n
    due_by_time = seconds > 0.0 and (now_ts - last_flush) >= seconds

    if due_by_count or due_by_time:
        dbr_flush_buffers(resolved_path)

def dbr_append_text(path, text, operation="append", extra=None):
    try:
        resolved_path = dbr_resolve_path(path)
        payload = str(text or "")
        if not payload:
            return

        if _buffered_debug_enabled(resolved_path, mode="a", write_once=False):
            _buffer_debug_text(resolved_path, payload)
            return

        _write_text_immediate(resolved_path, payload, mode="a", operation=operation)
    except Exception:
        pass

atexit.register(dbr_flush_buffers)

def dbr_get_debug_dir():
    global _DEBUG_RUN_DIR

    if not bool(getattr(Config, "DEBUG_AUTO_RUN_DIR", True)):
        return "debug"

    if _DEBUG_RUN_DIR:
        return str(_DEBUG_RUN_DIR)

    root = "debug"
    prefix = str(getattr(Config, "DEBUG_RUN_PREFIX", "debug_lauf_") or "debug_lauf_")
    os.makedirs(root, exist_ok=True)

    max_idx = 0
    try:
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if not os.path.isdir(path) or not str(name).startswith(prefix):
                continue
            suffix = str(name)[len(prefix):]
            if suffix.isdigit():
                max_idx = max(max_idx, int(suffix))
    except Exception:
        max_idx = 0

    _DEBUG_RUN_DIR = os.path.join(root, f"{prefix}{max_idx + 1}")
    os.makedirs(_DEBUG_RUN_DIR, exist_ok=True)
    return str(_DEBUG_RUN_DIR)

def dbr_path(*parts):
    cleaned = _debug_grouped_parts(parts)
    return os.path.join(dbr_get_debug_dir(), *cleaned)

def dbr_resolve_path(path):
    raw = str(path or "").strip()
    if not raw:
        return dbr_get_debug_dir()

    normalized = raw.replace("\\", "/")
    if normalized == "debug":
        return dbr_get_debug_dir()
    if normalized.startswith("debug/"):
        prefix = str(getattr(Config, "DEBUG_RUN_PREFIX", "debug_lauf_") or "debug_lauf_")
        parts = normalized.split("/")
        if len(parts) > 1 and parts[1].startswith(prefix):
            return raw
        return os.path.join(dbr_get_debug_dir(), *_debug_grouped_parts(normalized.split("/")[1:]))
    return raw
# ─────────────────────────────────────────────
def _ensure_dir(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
# ─────────────────────────────────────────────
def dbr_file_write_profile(path, elapsed_ms, bytes_written=0, operation="write", extra=None):
    try:
        if not bool(getattr(Config, "MCM_FILE_WRITE_PROFILE_DEBUG", False)):
            return

        elapsed = float(elapsed_ms or 0.0)
        min_ms = max(0.0, float(getattr(Config, "MCM_FILE_WRITE_PROFILE_MIN_MS", 0.0) or 0.0))
        if elapsed < min_ms:
            return

        profile_path = dbr_path("mcm_file_write_profile.csv")
        normalized_path = str(path or "-").replace("\\", "/")
        if normalized_path.endswith("mcm_file_write_profile.csv"):
            return

        every_n = max(1, int(getattr(Config, "MCM_FILE_WRITE_PROFILE_EVERY_N", 1) or 1))
        count_key = f"file_profile::{normalized_path}"
        count = int(_DEBUG_COUNTERS.get(count_key, 0) or 0) + 1
        _DEBUG_COUNTERS[count_key] = count
        if (count % every_n) != 0:
            return

        _ensure_dir(profile_path)
        if profile_path not in _FILE_PROFILE_HEADER_DONE:
            if os.path.exists(profile_path):
                os.remove(profile_path)
            with open(profile_path, "w", encoding="utf-8") as f:
                f.write("timestamp;path;operation;elapsed_ms;bytes_written;extra\n")
            _FILE_PROFILE_HEADER_DONE.add(profile_path)

        cleaned_path = normalized_path.replace("\n", " ").replace(";", "|")
        cleaned_operation = str(operation or "write").replace("\n", " ").replace(";", "|")
        cleaned_extra = str(extra or "").replace("\n", " ").replace(";", "|")

        with open(profile_path, "a", encoding="utf-8") as f:
            f.write(
                f"{time.time():.6f};{cleaned_path};{cleaned_operation};"
                f"{elapsed:.4f};{int(bytes_written or 0)};{cleaned_extra}\n"
            )
    except Exception:
        pass
# ZENTRALES BACKEND
# ─────────────────────────────────────────────
def dbr_write(
    msg,
    path: str,
    mode: str = "a",
    reset_on_start: bool = False,
    write_once: bool = False,
):
    try:
        path = dbr_resolve_path(path)
        if msg is None:
            return

        s = str(msg)
        if not s:
            return

        _ensure_dir(path)

        if reset_on_start and path not in _RESET_DONE:
            if os.path.exists(path):
                os.remove(path)
            _RESET_DONE.add(path)

        if write_once:
            mode = "w"

        if mode == "a" and not write_once:
            every_n = max(1, int(getattr(Config, "DEBUG_WRITE_EVERY_N", 1) or 1))
            if every_n > 1:
                count = int(_DEBUG_COUNTERS.get(path, 0) or 0) + 1
                _DEBUG_COUNTERS[path] = count
                if (count % every_n) != 0:
                    return

        payload = s + "\n"
        if _buffered_debug_enabled(path, mode=mode, write_once=write_once):
            _buffer_debug_text(path, payload)
            return

        _write_text_immediate(path, payload, mode=mode, operation=f"dbr_write:{mode}")

    except Exception:
        pass

# ─────────────────────────────────────────────
# WRAPPER (API-KOMPATIBEL)
# ─────────────────────────────────────────────
def dbr_debug(msg,txt="debug.csv"):
    dbr_write(msg, dbr_path(txt), "a", True, False)
# ─────────────────────────────────────────────
def dbr_profile(section, elapsed_ms, extra=None, txt="mcm_profile.csv"):
    try:
        if not bool(getattr(Config, "MCM_RUNTIME_PROFILE_DEBUG", False)):
            return

        elapsed = float(elapsed_ms or 0.0)
        min_ms = max(0.0, float(getattr(Config, "MCM_RUNTIME_PROFILE_MIN_MS", 0.0) or 0.0))

        if elapsed < min_ms:
            return

        path = dbr_path(str(txt or "mcm_profile.csv"))
        _ensure_dir(path)

        every_n = max(1, int(getattr(Config, "MCM_RUNTIME_PROFILE_EVERY_N", 1) or 1))
        count_key = f"profile::{path}"
        count = int(_DEBUG_COUNTERS.get(count_key, 0) or 0) + 1
        _DEBUG_COUNTERS[count_key] = count

        if (count % every_n) != 0:
            return

        if path not in _PROFILE_HEADER_DONE:
            if os.path.exists(path):
                os.remove(path)

            profile_config = (
                f"profile_debug={bool(getattr(Config, 'MCM_RUNTIME_PROFILE_DEBUG', False))}|"
                f"profile_min_ms={float(getattr(Config, 'MCM_RUNTIME_PROFILE_MIN_MS', 0.0) or 0.0)}|"
                f"profile_every_n={int(getattr(Config, 'MCM_RUNTIME_PROFILE_EVERY_N', 1) or 1)}|"
                f"snapshot_every_n={int(getattr(Config, 'MCM_VISUAL_SNAPSHOT_WRITE_EVERY_N', 1) or 1)}|"
                f"snapshot_force_on_state_change={bool(getattr(Config, 'MCM_VISUAL_SNAPSHOT_FORCE_ON_STATE_CHANGE', True))}|"
                f"memory_save_cooldown={float(getattr(Config, 'MCM_MEMORY_SAVE_COOLDOWN_SECONDS', 0.0) or 0.0)}"
            )
            profile_config = str(profile_config or "").replace("\n", " ").replace(";", "|")

            header_line = "section;elapsed_ms;extra\n"
            config_line = f"__profile_config__;0.0000;{profile_config}\n"
            profile_start = time.perf_counter()
            with open(path, "w", encoding="utf-8") as f:
                f.write(header_line)
                f.write(config_line)
            dbr_file_write_profile(
                path,
                (time.perf_counter() - profile_start) * 1000.0,
                bytes_written=len((header_line + config_line).encode("utf-8")),
                operation="profile_header",
            )
            _PROFILE_HEADER_DONE.add(path)

        cleaned_extra = str(extra or "").replace("\n", " ").replace(";", "|")

        line = f"{section};{elapsed:.4f};{cleaned_extra}\n"
        dbr_append_text(path, line, operation="profile_append")

    except Exception:
        pass
# ─────────────────────────────────────────────
