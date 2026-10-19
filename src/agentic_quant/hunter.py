"""
Multi-Chain DEX Pool Scanner & Real-Time Discovery Engine (Solana, Base, BSC, Ethereum).
"""

import urllib.request
import urllib.parse
import json
import ssl
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .crawlscan import CrawlScanMath

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

class NewCoinHunter:
    @staticmethod
    def _fetch_url(url: str, timeout: int = 6, extra_headers: dict = None) -> dict:
        hdr = {**HEADERS}
        if extra_headers:
            hdr.update(extra_headers)
        req = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as res:
            return json.loads(res.read().decode('utf-8'))

    @classmethod
    def get_new_pools(cls, network: str = "solana", min_liquidity: float = 1000.0) -> list:
        url = f"https://api.geckoterminal.com/api/v2/networks/{network}/new_pools?page=1"
        try:
            raw = cls._fetch_url(url, extra_headers={"Accept": "application/json;version=20230302"})
            pools = raw.get("data", [])
            results = []
            for p in pools:
                attr = p.get("attributes", {})
                rel = p.get("relationships", {})

                pair_name = attr.get("name", "Unknown/Unknown")
                parts = pair_name.split("/")
                symbol = parts[0].strip() if len(parts) > 0 else "UNKNOWN"

                base_token_data = rel.get("base_token", {}).get("data", {})
                base_token_id = base_token_data.get("id", "")
                token_address = base_token_id.replace(f"{network}_", "") if base_token_id else attr.get("address", "")
                pool_address = attr.get("address", "")

                dex_data = rel.get("dex", {}).get("data", {})
                dex_name = dex_data.get("id", "dex")

                price_usd = float(attr.get("base_token_price_usd") or 0.0)
                reserve_usd = float(attr.get("reserve_in_usd") or 0.0)
                fdv_usd = float(attr.get("fdv_usd") or 0.0)

                if reserve_usd < min_liquidity:
                    continue

                audit = CrawlScanMath.analyze_token_fragility(reserve_usd, fdv_usd)

                results.append({
                    "chain": network.upper(),
                    "symbol": symbol,
                    "pair": pair_name,
                    "token_address": token_address,
                    "pool_address": pool_address,
                    "dex": dex_name,
                    "price_usd": price_usd,
                    "liquidity_usd": reserve_usd,
                    "fdv_usd": fdv_usd,
                    "safety_score": audit["crawlscan_score"],
                    "band": audit["crawlscan_band"],
                    "verdict": audit["verdict"],
                    "chart_url": f"https://dexscreener.com/{network}/{token_address}"
                })
            return results
        except Exception:
            return []

    @classmethod
    def scan_all(cls, networks=("solana", "base", "bsc"), min_liquidity: float = 1000.0) -> dict:
        results = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pools": []
        }
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_net = {executor.submit(cls.get_new_pools, net, min_liquidity): net for net in networks}
            for f in as_completed(future_to_net):
                results["pools"].extend(f.result())

        results["pools"].sort(key=lambda x: (x["safety_score"], x["liquidity_usd"]), reverse=True)
        return results
