"""
Agentic Quant Desk: Autonomous Multi-Agent Quantitative Trading & On-Chain Risk Discovery Framework.
Organization: HUYNH BUSINESS LLC | Founder: Thao Huynh
"""

__version__ = "1.1.0"
__author__ = "Thao Huynh"

from .crawlscan import CrawlScanMath
from .hunter import NewCoinHunter
from .radar import CexListingRadar
from .decision import JevSignalRouter, DeskAction

__all__ = ["CrawlScanMath", "NewCoinHunter", "CexListingRadar", "JevSignalRouter", "DeskAction"]
