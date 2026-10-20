import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from agentic_quant.decision import JevSignalRouter, DeskAction

class TestJevSignalRouter(unittest.TestCase):
    def test_safe_execution(self):
        # Deep liquidity ($500K liq, $1M FDV, low cabal risk)
        res = JevSignalRouter.evaluate_signal(liquidity_usd=500000, fdv=1000000, cabal_cluster_risk=0.02)
        self.assertEqual(res["action"], DeskAction.EXECUTE_SWAP.value)
        self.assertGreaterEqual(res["confidence"], 0.40)
        self.assertLess(res["latency_microseconds"], 5000) # Sub-5ms

    def test_fragile_rejection(self):
        # Thin liquidity trap ($2K liq, $1M FDV)
        res = JevSignalRouter.evaluate_signal(liquidity_usd=2000, fdv=1000000)
        self.assertEqual(res["action"], DeskAction.REJECT_FRAGILE.value)
        self.assertIn("Fragile", res["rationale"])

    def test_sybil_blocking(self):
        # High sybil cabal cluster risk (85%)
        res = JevSignalRouter.evaluate_signal(liquidity_usd=100000, fdv=500000, cabal_cluster_risk=0.85)
        self.assertEqual(res["action"], DeskAction.BLOCK_SYBIL.value)

    def test_benchmark_metrics(self):
        bm = JevSignalRouter.benchmark_comparison()
        self.assertIn("speedup_factor", bm)
        self.assertLess(bm["jev_latency_ms"], 1.0) # Sub-1ms

if __name__ == "__main__":
    unittest.main()
