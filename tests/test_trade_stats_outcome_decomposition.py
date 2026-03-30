import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from trade_stats import TradeStats


class TradeStatsOutcomeDecompositionTests(unittest.TestCase):
    def test_on_exit_persists_last_outcome_decomposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            stats_path = Path(tmp) / "trade_stats.json"
            csv_path = Path(tmp) / "trade_equity.csv"

            stats = TradeStats(
                path=str(stats_path),
                csv_path=str(csv_path),
                reset=True,
            )

            decomposition = {
                "perception_quality": 0.7,
                "felt_quality": 0.6,
                "thought_quality": 0.8,
                "plan_quality": 0.75,
                "execution_quality": 0.72,
                "risk_fit_quality": 0.68,
                "reason": "tp_hit",
            }

            stats.on_exit(
                entry=100.0,
                tp=102.0,
                sl=99.0,
                reason="tp_hit",
                side="LONG",
                amount=1.0,
                outcome_decomposition=decomposition,
            )

            saved = json.loads(stats_path.read_text(encoding="utf-8"))
            self.assertEqual(saved.get("last_outcome_decomposition"), decomposition)

    def test_on_cancel_persists_last_outcome_decomposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            stats_path = Path(tmp) / "trade_stats.json"
            csv_path = Path(tmp) / "trade_equity.csv"

            stats = TradeStats(
                path=str(stats_path),
                csv_path=str(csv_path),
                reset=True,
            )

            decomposition = {
                "perception_quality": 0.4,
                "felt_quality": 0.5,
                "thought_quality": 0.45,
                "plan_quality": 0.3,
                "execution_quality": 0.2,
                "risk_fit_quality": 0.35,
                "reason": "cancel",
            }

            stats.on_cancel(
                order_id="abc123",
                cause="exchange_cancel",
                outcome_decomposition=decomposition,
            )

            saved = json.loads(stats_path.read_text(encoding="utf-8"))
            self.assertEqual(saved.get("last_outcome_decomposition"), decomposition)


if __name__ == "__main__":
    unittest.main()
