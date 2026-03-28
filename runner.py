# ==================================================
# runner.py
# ==================================================
import csv
import time
from workspace import append_workspace_live, init_workspace_live
from datetime import datetime
from config import Config
from bot import Bot
from ph_ohlcv import (
    create_exchange,
    get_sufficient_balance,
    get_account_value,
    fetch_ohlcv,
)

from place_orders import _SYMBOL, set_context, place_order

# --------------------------------------------------
# BACKTEST RANGE PRINT
# --------------------------------------------------
def _print_backtest_range(path):
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

        if first_ts and last_ts:

            # Mikrosekunden → Millisekunden
            if first_ts > 10_000_000_000_000:
                first_ts = first_ts / 1000

            if last_ts > 10_000_000_000_000:
                last_ts = last_ts / 1000

            first_dt = datetime.fromtimestamp(first_ts / 1000).strftime("%d.%m.%Y")
            last_dt = datetime.fromtimestamp(last_ts / 1000).strftime("%d.%m.%Y")
            print(f"BACKTEST RANGE: {first_dt} → {last_dt}")

    except Exception:
        print("BACKTEST RANGE: -")

# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":

    print("-------------------------------------------------------")
    print("WORKSPACE")
    print(f"  WINDOW_SIZE: {Config.WINDOW_SIZE}")

    print("-------------------------------------------------------")
    print("RISK MANAGEMENT")
    print(f"  RR: {Config.RR}")
    print(f"  MIN_RR: {Config.MIN_RR}")
    print(f"  MAX_RR: {Config.MAX_RR}")
    print(f"  BASE_RISK_PCT: {Config.BASE_RISK_PCT}")
    print(f"  MAX_SL_DISTANCE: {Config.MAX_SL_DISTANCE}")
    print(f"  MIN_TP_DISTANCE: {Config.MIN_TP_DISTANCE}")
    print(f"  RR_EXECUTION_MIN: {Config.RR_EXECUTION_MIN}")
    print(f"  PENDING_ENTRY_MAX_WAIT_BARS: {Config.PENDING_ENTRY_MAX_WAIT_BARS}")

    print("-------------------------------------------------------")
    print("MCM")
    print(f"  MCM_ENABLED: {Config.MCM_ENABLED}")
    print(f"  MCM_INTERNAL_CYCLES: {Config.MCM_INTERNAL_CYCLES}")
    print(f"  MCM_REPLAY_SCALE: {Config.MCM_REPLAY_SCALE}")
    print(f"  MCM_COUPLING: {Config.MCM_COUPLING}")
    print(f"  MCM_NOISE: {Config.MCM_NOISE}")
    print(f"  MCM_PRESSURE_WEIGHT: {Config.MCM_PRESSURE_WEIGHT}")
    print(f"  MCM_MEMORY_WEIGHT: {Config.MCM_MEMORY_WEIGHT}")
    print(f"  MCM_REGULATION_WEIGHT: {Config.MCM_REGULATION_WEIGHT}")

    print("-------------------------------------------------------")
    print("COSTS")
    print(f"  FEE_RATE: {Config.FEE_RATE}")
    print(f"  FEE_PER_TRADE: {Config.FEE_PER_TRADE}")

    print("-------------------------------------------------------")
    print("SYSTEM")
    print(f"  AKTIV_ORDER: {Config.AKTIV_ORDER}")
    # --------------------------------------------------
    # BACKTEST MODE
    # --------------------------------------------------
    if Config.MODE == "BACKTEST":

        filepath = Config.BACKTEST_FILEPATH

        bot = Bot(filepath)

        buffer = []
        bot.processed = 0

        for row in bot.feed.rows(delay_seconds=0.0):
            buffer.append(row)

            if len(buffer) < Config.WINDOW_SIZE:
                continue

            if len(buffer) > Config.WINDOW_SIZE:
                buffer.pop(0)

            bot._process_window(buffer)

            bot.processed += 1

        stats = bot.stats.snapshot()

        _print_backtest_range(filepath)

        '''
        print(
            f"BACKTEST EXPLORATION | "
            f"TRADES: {stats.get('exploration_trades', 0)} | "
            f"TP: {stats.get('exploration_tp', 0)} | "
            f"SL: {stats.get('exploration_sl', 0)} | "
            f"CANCELS: {stats.get('exploration_cancels', 0)} | "
            f"PNL: {stats.get('exploration_pnl', 0.0):.4f}"
        )
        '''
        print(
            f"BACKTEST GESAMT | "
            f"TRADES: {stats.get('trades', 0)} | "
            f"TP: {stats.get('tp', 0)} | "
            f"SL: {stats.get('sl', 0)} | "
            f"CANCELS: {stats.get('cancels', 0)} | "
            f"PNL_NETTO: {stats.get('pnl_netto', 0.0):.4f}"
        )

    # --------------------------------------------------
    # LIVE MODE (SEQUENZIELL · BACKEND-IDENTISCH)
    # --------------------------------------------------
    elif Config.MODE == "LIVE":

        timeframe = Config.TIMEFRAME
        symbol = Config.SYMBOL

        # --------------------------------------------------
        # Dynamisches Polling-Intervall
        # --------------------------------------------------
        tf = timeframe.lower().strip()

        if tf.endswith("m"):
            tf_seconds = int(tf[:-1]) * 60
        elif tf.endswith("h"):
            tf_seconds = int(tf[:-1]) * 3600
        else:
            tf_seconds = 60

        # Polling ≈ 1/60 der Candle-Dauer (min 1s, max 15s)
        poll_interval = max(1, min(15, tf_seconds // 60))

        exchange = create_exchange(Config.MECHANIK)

        set_context(
            exchange=exchange,
            symbol=symbol,
            timeframe=timeframe,
            get_sufficient_balance=get_sufficient_balance,
            get_account_value=get_account_value,
        )

        bot = Bot(None)

        last_processed_ts = None
        buffer = []

        while True:

            raw = fetch_ohlcv(exchange, symbol, timeframe)

            if raw is None or not isinstance(raw, list):
                continue

            if len(raw) < Config.WINDOW_SIZE + 1:
                continue

            # --------------------------------------------------
            # Letzte Kerze nur entfernen wenn sie noch läuft
            # --------------------------------------------------
            tf = timeframe.lower().strip()

            if tf.endswith("m"):
                tf_seconds = int(tf[:-1]) * 60
            elif tf.endswith("h"):
                tf_seconds = int(tf[:-1]) * 3600
            else:
                tf_seconds = 60

            now_ts = int(time.time())
            last_candle_ts = int(raw[-1][0]) // 1000

            # Wenn letzte Kerze noch nicht geschlossen ist → entfernen
            if now_ts < (last_candle_ts + tf_seconds):
                raw = raw[:-1]

            # --------------------------------------------------
            # INITIALISIERUNG (einmalig)
            # --------------------------------------------------
            if last_processed_ts is None:

                init_slice = raw[-Config.WINDOW_SIZE:]
                init_workspace_live(symbol, timeframe, init_slice)

                buffer = [
                    {
                        "timestamp": int(ts),
                        "open": float(o),
                        "high": float(h),
                        "low": float(l),
                        "close": float(c),
                        "volume": float(v),
                    }
                    for ts, o, h, l, c, v in init_slice
                ]

                last_processed_ts = buffer[-1]["timestamp"]
                continue

            # --------------------------------------------------
            # NEUE KERZEN ERMITTELN
            # --------------------------------------------------
            new_candles = [
                c for c in raw
                if int(c[0]) > last_processed_ts
            ]

            if not new_candles:
                continue

            # --------------------------------------------------
            # SEQUENZIELLE VERARBEITUNG
            # --------------------------------------------------     
            for ts, o, h, l, c, v in new_candles:

                # Workspace append
                append_workspace_live(symbol, timeframe, (ts, o, h, l, c, v))

                row = {
                    "timestamp": int(ts),
                    "open": float(o),
                    "high": float(h),
                    "low": float(l),
                    "close": float(c),
                    "volume": float(v),
                }

                buffer.append(row)

                if len(buffer) > Config.WINDOW_SIZE:
                    buffer.pop(0)

                bot._process_window(buffer)

                last_processed_ts = int(ts)
                
            time.sleep(poll_interval)