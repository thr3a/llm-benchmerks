"""ローカルLLM速度ベンチマーク。

uv run run-benchmark.py --base-url https://example/v1 --model deep01 --count 3
"""
import argparse
import csv
import time
from datetime import datetime
from pathlib import Path
from statistics import mean

from openai import OpenAI

from patterns import ALL_PATTERNS, Pattern

FIELDS = ["model", "pattern", "run", "prompt_tokens", "completion_tokens",
          "pp_tps", "tg_tps", "total_sec"]


def run_once(client: OpenAI, model: str, pattern: Pattern) -> dict:
    # プロンプトキャッシュを避けるため、毎回末尾に現在時刻を付ける
    prompt = f"{pattern.prompt}\n\n{datetime.now():%Y-%m-%d %H:%M:%S}"
    start = time.perf_counter()
    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=pattern.max_tokens,
        stream=False,
    )
    total = time.perf_counter() - start
    usage = res.usage
    # llama.cpp系サーバーは timings を返す。無ければ pp は計測不可、tg は総時間で近似
    timings = (res.model_extra or {}).get("timings") or {}
    pp = timings.get("prompt_per_second")
    tg = timings.get("predicted_per_second")
    if tg is None:
        tg = usage.completion_tokens / total if total else None
    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "pp_tps": pp,
        "tg_tps": tg,
        "total_sec": total,
    }


def fmt(v: float | None, digits: int = 1) -> str:
    return "-" if v is None else f"{v:.{digits}f}"


def avg(rows: list[dict], key: str) -> float | None:
    vals = [r[key] for r in rows if r[key] is not None]
    return mean(vals) if vals else None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--model", action="append", required=True, help="複数指定可")
    p.add_argument("--api-key", default="dummy")
    p.add_argument("--count", type=int, default=3, help="各パターンの実行回数")
    p.add_argument("--output", help="CSV保存先 (既定: results/YYYYmmdd-HHMMSS.csv)")
    args = p.parse_args()

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    out = Path(args.output) if args.output else Path("results") / f"{datetime.now():%Y%m%d-%H%M%S}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    summary: list[tuple] = []
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for model in args.model:
            for pattern in ALL_PATTERNS:
                rows = []
                for i in range(1, args.count + 1):
                    r = {"model": model, "pattern": pattern.name, "run": i, **run_once(client, model, pattern)}
                    rows.append(r)
                    writer.writerow(r)
                    f.flush()
                    print(f"[{model}] {pattern.name} #{i}: pp={fmt(r['pp_tps'])} t/s "
                          f"tg={fmt(r['tg_tps'])} t/s total={r['total_sec']:.2f}s "
                          f"(in={r['prompt_tokens']} out={r['completion_tokens']})", flush=True)
                all_rows += rows
                summary.append((model, pattern.name, avg(rows, "pp_tps"),
                                avg(rows, "tg_tps"), avg(rows, "total_sec")))

    print(f"\n=== 平均 (count={args.count}) ===")
    print(f"{'model':<20}{'pattern':<20}{'pp t/s':>10}{'tg t/s':>10}{'total s':>10}")
    for m, pat, pp, tg, tot in summary:
        print(f"{m:<20}{pat:<20}{fmt(pp):>10}{fmt(tg):>10}{fmt(tot, 2):>10}")
    print(f"\nCSV: {out}")


if __name__ == "__main__":
    main()
