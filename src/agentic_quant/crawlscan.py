"""
CrawlScan Mathematical Engine: Constant-Product AMM Liquidity Fragility & Price Dump Impact.
Derived from decentralized AMM invariant: x * y = k.
"""

class CrawlScanMath:
    @staticmethod
    def calculate_dump_impact(q_usd: float, pool_reserve_usd: float) -> float:
        """
        Constant-product AMM price impact formula:
        Drop = 1.0 - (Reserve / (Reserve + q)) ** 2
        """
        if q_usd <= 0:
            return 0.0
        if pool_reserve_usd <= 0:
            return 1.0
        ratio = pool_reserve_usd / (pool_reserve_usd + q_usd)
        return max(0.0, min(1.0, 1.0 - (ratio ** 2)))

    @staticmethod
    def analyze_token_fragility(liquidity_usd: float, fdv: float) -> dict:
        """
        Compute liquidity buffer ratio and projected price impact under various dump scenarios.
        """
        reserve_usd = max(1.0, liquidity_usd / 2.0)
        fragility_ratio = (liquidity_usd / max(1.0, fdv)) * 100.0 if fdv > 0 else 0.0

        # Scenario 1: Top 1 Holder / Dev sells 5% supply
        q_5pct = fdv * 0.05
        drop_5pct = CrawlScanMath.calculate_dump_impact(q_5pct, reserve_usd)

        # Scenario 2: Cabal cluster sells 12% supply
        q_12pct = fdv * 0.12
        drop_12pct = CrawlScanMath.calculate_dump_impact(q_12pct, reserve_usd)

        # Scenario 3: Sybil network sells 25% supply
        q_25pct = fdv * 0.25
        drop_25pct = CrawlScanMath.calculate_dump_impact(q_25pct, reserve_usd)

        # Safety Score (0 - 100)
        if drop_12pct <= 0.10 and liquidity_usd >= 15000:
            crawlscan_score = 100
        elif drop_12pct >= 0.70 or liquidity_usd < 2000:
            crawlscan_score = int(max(0, 100 - (drop_12pct * 120)))
        else:
            crawlscan_score = int(max(10, 100 - ((drop_12pct - 0.10) / 0.60) * 80))

        crawlscan_score = max(0, min(100, crawlscan_score))

        if crawlscan_score >= 75 and liquidity_usd >= 10000:
            crawlscan_band = "CLEAN"
            verdict = "SAFE"
        elif crawlscan_score >= 45 and liquidity_usd >= 3000:
            crawlscan_band = "SUSPICIOUS"
            verdict = "WARNING"
        else:
            crawlscan_band = "DANGER"
            verdict = "HIGH_RISK"

        return {
            "reserve_usd": reserve_usd,
            "fragility_ratio_pct": round(fragility_ratio, 2),
            "drop_5pct_dump": round(drop_5pct * 100, 1),
            "drop_12pct_cabal": round(drop_12pct * 100, 1),
            "drop_25pct_sybil": round(drop_25pct * 100, 1),
            "crawlscan_score": crawlscan_score,
            "crawlscan_band": crawlscan_band,
            "verdict": verdict,
        }
