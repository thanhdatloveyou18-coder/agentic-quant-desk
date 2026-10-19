import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from agentic_quant.crawlscan import CrawlScanMath

class TestCrawlScan(unittest.TestCase):
    def test_zero_dump(self):
        impact = CrawlScanMath.calculate_dump_impact(0, 10000)
        self.assertEqual(impact, 0.0)

    def test_zero_reserve(self):
        impact = CrawlScanMath.calculate_dump_impact(1000, 0)
        self.assertEqual(impact, 1.0)

    def test_known_impact(self):
        # Reserve = 100, Dump = 100 => Ratio = 100/200 = 0.5 => Drop = 1 - 0.25 = 0.75
        impact = CrawlScanMath.calculate_dump_impact(100, 100)
        self.assertAlmostEqual(impact, 0.75, places=4)

    def test_fragility_scoring(self):
        # Deep liquidity pool (Reserve = $250,000, FDV = $250,000)
        rep = CrawlScanMath.analyze_token_fragility(liquidity_usd=500000, fdv=250000)
        self.assertIn("crawlscan_score", rep)
        self.assertGreaterEqual(rep["crawlscan_score"], 70)
        self.assertIn(rep["crawlscan_band"], ["CLEAN", "SUSPICIOUS"])

        # Thin liquidity trap (Liquidity = $1,000, FDV = $1,000,000)
        rep_thin = CrawlScanMath.analyze_token_fragility(liquidity_usd=1000, fdv=1000000)
        self.assertLess(rep_thin["crawlscan_score"], 40)
        self.assertEqual(rep_thin["crawlscan_band"], "DANGER")

if __name__ == "__main__":
    unittest.main()
