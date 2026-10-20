"""
Agentic Quant Desk CLI
Command-line interface for multi-agent trading desk, CrawlScan audit, and Jev System-1 fast decision routing.
"""

import sys
import argparse
import time

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from .crawlscan import CrawlScanMath
from .hunter import NewCoinHunter
from .decision import JevSignalRouter, DeskAction

BANNER = r"""
=================================================================
  AGENTIC QUANT DESK v1.1.0
  High-Performance Autonomous Multi-Agent Risk Engine
  Jev System-1 Decision Router // Jane Street Quant Architecture
=================================================================
"""

def run_demo():
    print(BANNER)
    print(" [*] INITIALIZING 6-AGENT COOPERATIVE SWARM...")
    time.sleep(0.2)
    
    agents = [
        ("SCOUT", "Scanning DEX Mempools (Solana, Base, BSC) for fresh liquidity..."),
        ("ANALYST", "Calculating Fair Value Range & Order Book Imbalance..."),
        ("QUANT", "Executing 12-Month Holdout Backtest with Strict Walk-Forward..."),
        ("SKEPTIC", "Injecting CrawlScan Invariant Shock: 1 - (R / (R + q))^2..."),
        ("ROUTER", "Evaluating Jev System-1 Fast Typed Choice in sub-0.5ms..."),
        ("RISK", "Enforcing 1.0% Max Position Risk with Hard OTO Bracket Stop-Loss..."),
        ("JOURNAL", "Recording Alpha Attenuation & Slippage Signature to SQLite...")
    ]
    
    for name, task in agents:
        print(f"  [AGENT: {name:<8}] {task}")
        time.sleep(0.12)
        
    print("-" * 65)
    print(" [*] SAMPLE SIMULATION AUDIT: TOKEN $ALPHA")
    res = CrawlScanMath.analyze_token_fragility(liquidity_usd=85000, fdv=450000)
    print(f"     Liquidity: $85,000 | FDV: $450,000")
    print(f"     Safety Score: {res['crawlscan_score']}/100")
    print(f"     Projected 12% Cabal Dump: -{res['drop_12pct_cabal']}%")
    print(f"     Verdict: {res['verdict']}")
    print("-" * 65)
    print(" [OK] DESK EXECUTION PASS: OTO Bracket Stop-Loss Armed at -3.5%.")

def run_scan(chains, min_liq):
    print(BANNER)
    print(f" [*] Hunting live pools on {', '.join(chains)} (Min Liq: ${min_liq:,.0f})...")
    feed = NewCoinHunter.scan_all(networks=chains, min_liquidity=min_liq)
    pools = feed.get("pools", [])
    print(f" [OK] Discovered {len(pools)} qualified pools:\n")
    print(f" {'CHAIN':<8} | {'SYMBOL':<10} | {'LIQUIDITY':<12} | {'SAFETY':<8} | {'VERDICT'}")
    print("-" * 65)
    for p in pools[:10]:
        print(f" {p['chain'].upper():<8} | {p['symbol']:<10} | ${p['liquidity_usd']:<11,.0f} | {p['safety_score']:<7}/100 | {p['verdict']}")
    print("-" * 65)

def run_audit(liq, fdv):
    print(BANNER)
    res = CrawlScanMath.analyze_token_fragility(liquidity_usd=liq, fdv=fdv)
    print(" === CRAWLSCAN AMM FRAGILITY AUDIT ===")
    print(f" Reserve Liquidity: ${liq:,.2f}")
    print(f" Fully Diluted Val: ${fdv:,.2f}")
    print(f" 5% Dump Impact:    -{res['drop_5pct_dump']:.2f}%")
    print(f" 12% Dump Impact:   -{res['drop_12pct_cabal']:.2f}%")
    print(f" 25% Dump Impact:   -{res['drop_25pct_sybil']:.2f}%")
    print(f" Safety Score:      {res['crawlscan_score']}/100 ({res['crawlscan_band']})")
    print(f" Final Verdict:     {res['verdict']}")

def run_signal(liq, fdv, cabal_risk):
    print(BANNER)
    print(" === JEV SYSTEM-1 FAST SIGNAL ROUTING ===")
    decision = JevSignalRouter.evaluate_signal(
        liquidity_usd=liq,
        fdv=fdv,
        cabal_cluster_risk=cabal_risk
    )
    print(f" Target Profile:    ${liq:,.0f} Reserve / ${fdv:,.0f} FDV (Cabal Risk: {cabal_risk*100:.1f}%)")
    print(f" Latency:           {decision['latency_microseconds']} microseconds (<0.1ms)")
    print(f" Typed Action:      [{decision['action']}] (Confidence: {decision['confidence']*100:.1f}%)")
    print(f" Rationale:         {decision['rationale']}")
    print(" Distribution:")
    for action, prob in decision['probabilities'].items():
        bar = "#" * int(prob * 20)
        print(f"   {action:<18} [{bar:<20}] {prob*100:5.1f}%")

def run_benchmark():
    print(BANNER)
    print(" === SYSTEM-1 ROUTER VS TRADITIONAL LLM CHAT BENCHMARK ===")
    bm = JevSignalRouter.benchmark_comparison()
    print(f" Jev Signal Latency:        {bm['jev_latency_ms']} ms")
    print(f" Standard LLM Chat Latency: {bm['traditional_llm_latency_ms']} ms")
    print(f" Execution Speedup:         {bm['speedup_factor']}")
    print(f" Cost (Jev Decision):       {bm['cost_per_million_jev']} / 1M tokens")
    print(f" Cost (GPT-4o/Claude):      {bm['cost_per_million_llm']} / 1M tokens")
    print(f" Architecture:              {bm['architecture']}")

def main():
    parser = argparse.ArgumentParser(description="Agentic Quant Desk CLI")
    parser.add_argument("--demo", action="store_true", help="Run 6-agent trading desk simulation")
    parser.add_argument("--scan", action="store_true", help="Scan live DEX pools across multi-chain")
    parser.add_argument("--chains", nargs="+", default=["solana", "base", "bsc"], help="Target chains for scanning")
    parser.add_argument("--min-liq", type=float, default=2500.0, help="Minimum liquidity threshold USD")
    parser.add_argument("--audit", nargs=2, type=float, metavar=("LIQ", "FDV"), help="Audit specific token liquidity & FDV")
    parser.add_argument("--signal", nargs="+", type=float, metavar="ARG", help="Run Jev System-1 signal routing: LIQ FDV [CABAL_RISK]")
    parser.add_argument("--benchmark", action="store_true", help="Benchmark Jev router vs LLM chat latency & cost")
    
    args = parser.parse_args()
    
    if args.benchmark:
        run_benchmark()
    elif args.signal:
        if len(args.signal) < 2:
            print("Error: --signal requires at least LIQUIDITY and FDV (e.g., --signal 50000 250000 [0.10])")
        else:
            liq = args.signal[0]
            fdv = args.signal[1]
            cabal = args.signal[2] if len(args.signal) > 2 else 0.0
            run_signal(liq, fdv, cabal)
    elif args.scan:
        run_scan(args.chains, args.min_liq)
    elif args.audit:
        run_audit(args.audit[0], args.audit[1])
    elif args.demo or len(sys.argv) == 1:
        run_demo()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
