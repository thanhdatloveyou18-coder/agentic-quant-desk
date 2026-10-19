"""
CEX Pre-Listing Intelligence & Tier-1 Graduation Ladder Radar.
"""

import urllib.request
import json
import ssl
import datetime

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {"User-Agent": "Mozilla/5.0"}

class CexListingRadar:
    @staticmethod
    def get_binance_announcements(limit: int = 5) -> list:
        url = f"https://www.binance.com/bapi/composite/v1/public/cms/article/catalog/list/query?catalogId=48&pageNo=1&pageSize={limit}"
        req = urllib.request.Request(url, headers={**HEADERS, "lang": "en"})
        try:
            with urllib.request.urlopen(req, timeout=5, context=SSL_CTX) as res:
                data = json.loads(res.read().decode("utf-8"))
                articles = data.get("data", {}).get("articles", [])
                announcements = []
                for a in articles:
                    title = a.get("title", "")
                    code = a.get("code", "")
                    ts = a.get("releaseDate")
                    date_str = ""
                    if ts:
                        date_str = datetime.datetime.fromtimestamp(ts / 1000.0).strftime("%Y-%m-%d %H:%M")
                    announcements.append({
                        "exchange": "BINANCE",
                        "title": title,
                        "url": f"https://www.binance.com/en/support/announcement/{code}",
                        "date": date_str,
                        "is_listing": "Will List" in title or "Listing" in title
                    })
                return announcements
        except Exception:
            return []
