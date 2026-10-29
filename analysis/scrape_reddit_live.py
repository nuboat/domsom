#!/usr/bin/env python3
"""
scrape_reddit_live.py - Reddit AITA Dispute Data Collector & Pipeline

Collects authentic first-person moral-judgment seeking conflict narratives exclusively from:
- r/AmItheAsshole

Supports dual data ingestion modes:
1. Clean Sample Mode (--source sample):
   Loads verified archival relationship dispute disclosures from `data/raw_reddit_disputes_sample.csv`
   (N = 10,000 cases with full community moral verdicts: NTA, YTA, ESH, NAH, and reader arguments).
2. Live Scraping Mode (--source live):
   Fetches real-time dispute threads directly from `r/AmItheAsshole` via Reddit's JSON endpoints.
"""

import os
import sys
import csv
import json
import time
import argparse
import urllib.request
import urllib.error

# Target Subreddits: Strictly r/AmItheAsshole
SUBREDDITS = ["AmItheAsshole"]

DEFAULT_SAMPLE_PATH = "data/raw_reddit_disputes_sample.csv"
DEFAULT_OUTPUT_PATH = "analysis/data/raw_reddit_disputes_curated.csv"

def fetch_subreddit_posts(subreddit: str = "AmItheAsshole", listing: str = "new", limit: int = 100):
    """Fetches real-time posts from r/AmItheAsshole via Reddit's public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 (Academic Behavioral Study / Q1 IS Research)"
        }
    )
    posts = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            children = data.get("data", {}).get("children", [])
            for child in children:
                p = child.get("data", {})
                if p.get("stickied", False):
                    continue
                
                # Extract link flair / verdict if present
                verdict = p.get("link_flair_text", "").strip().lower()
                if not verdict:
                    verdict = "unadjudicated"

                posts.append({
                    "id": p.get("id"),
                    "subreddit": p.get("subreddit", subreddit),
                    "title": p.get("title", "").replace("\n", " ").strip(),
                    "text": p.get("selftext", "").replace("\n", " ").strip(),
                    "verdict": verdict,
                    "comment1": "",
                    "comment2": "",
                    "score": p.get("score", 0),
                    "author": p.get("author", "[deleted]"),
                    "created_utc": p.get("created_utc", ""),
                    "num_comments": p.get("num_comments", 0),
                    "url": f"https://reddit.com{p.get('permalink', '')}"
                })
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP Error fetching r/{subreddit}: {e.code} {e.reason}")
        if e.code in (401, 403, 429):
            print("  [HINT] Reddit blocked unauthenticated requests or rate-limited your IP.")
            print(f"  [RECOMMENDATION] Use clean sample data instead: python3 analysis/scrape_reddit_live.py --source sample")
    except Exception as e:
        print(f"[ERROR] Error fetching r/{subreddit}: {e}")
    return posts

def load_sample_disputes(sample_path: str, limit: int = None, filter_keywords: list = None):
    """Loads authentic AITA dispute cases from pre-cleaned sample CSV."""
    if not os.path.exists(sample_path):
        raise FileNotFoundError(f"Sample data file not found at: {sample_path}")

    print(f"Loading verified AITA dispute records from: {sample_path}")
    posts = []
    with open(sample_path, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("title", "").strip()
            text = row.get("text", "").strip()
            
            # Optional keyword filtering
            if filter_keywords:
                full_text_lower = f"{title} {text}".lower()
                if not any(kw.lower() in full_text_lower for kw in filter_keywords):
                    continue

            posts.append({
                "id": row.get("id", ""),
                "subreddit": "AmItheAsshole",
                "title": title.replace("\n", " "),
                "text": text.replace("\n", " "),
                "verdict": row.get("verdict", "").strip().lower(),
                "comment1": row.get("comment1", "").replace("\n", " ").strip(),
                "comment2": row.get("comment2", "").replace("\n", " ").strip(),
                "score": row.get("score", "0")
            })
            if limit and len(posts) >= limit:
                break
    return posts

def print_verdict_summary(posts: list):
    """Prints demographic breakdown of community moral verdicts."""
    verdict_counts = {}
    for p in posts:
        v = p.get("verdict", "unknown")
        verdict_counts[v] = verdict_counts.get(v, 0) + 1
    
    print("-" * 50)
    print(f"Total Dispute Records: {len(posts):,}")
    print("Moral Verdict Distribution:")
    for verdict, count in sorted(verdict_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(posts)) * 100 if posts else 0
        print(f"  - {verdict.upper():<15}: {count:5,} ({pct:5.1f}%)")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="AITA Reddit Dispute Pipeline: Targets exclusively r/AmItheAsshole with sample and live modes."
    )
    parser.add_argument(
        "--source",
        choices=["sample", "live"],
        default="sample",
        help="Data source mode: 'sample' loads verified data from CSV; 'live' scrapes real-time posts (default: sample)."
    )
    parser.add_argument("--live", action="store_true", help="Shortcut flag to scrape live posts from r/AmItheAsshole.")
    parser.add_argument("--sample", action="store_true", help="Shortcut flag to load from clean sample dataset.")
    parser.add_argument(
        "--subreddits",
        nargs="+",
        default=SUBREDDITS,
        help="Target subreddits (default: AmItheAsshole only)."
    )
    parser.add_argument(
        "--sample-path",
        default=DEFAULT_SAMPLE_PATH,
        help=f"Path to clean sample CSV (default: {DEFAULT_SAMPLE_PATH})."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max number of records to load or scrape (default: all for sample, 100 for live)."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT_PATH})."
    )
    parser.add_argument(
        "--filter-keywords",
        nargs="+",
        default=None,
        help="Optional keywords to filter disputes (e.g. '50/50', 'fair', 'split', 'boundary')."
    )
    args = parser.parse_args()

    # Priority determination
    source_mode = args.source
    if args.live:
        source_mode = "live"
    elif args.sample:
        source_mode = "sample"

    print("=" * 70)
    print("AITA REDDIT RELATIONSHIP DISPUTE DATA PIPELINE (Study 1)")
    print(f"Target Subreddit: {', '.join(args.subreddits)} (Exclusively)")
    print(f"Selected Mode:    {source_mode.upper()}")
    print("=" * 70)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    all_posts = []

    if source_mode == "sample":
        try:
            all_posts = load_sample_disputes(
                sample_path=args.sample_path,
                limit=args.limit,
                filter_keywords=args.filter_keywords
            )
            print(f"[SUCCESS] Loaded {len(all_posts):,} clean cases from sample dataset.")
        except Exception as e:
            print(f"[FATAL] Failed to load sample data: {e}")
            sys.exit(1)

    elif source_mode == "live":
        limit_per_sub = args.limit if args.limit is not None else 100
        for sub in args.subreddits:
            print(f"Scraping live posts from r/{sub} (limit: {limit_per_sub})...")
            posts = fetch_subreddit_posts(subreddit=sub, limit=limit_per_sub)
            print(f"  Retrieved {len(posts)} posts from r/{sub}")
            all_posts.extend(posts)
            time.sleep(1.5)

        if not all_posts:
            print("\n[WARNING] No live posts could be retrieved (likely due to Reddit API restrictions).")
            if os.path.exists(args.sample_path):
                print(f"[FALLBACK] Automatically switching to clean sample data ({args.sample_path})...")
                all_posts = load_sample_disputes(
                    sample_path=args.sample_path,
                    limit=args.limit,
                    filter_keywords=args.filter_keywords
                )
                print(f"[SUCCESS] Loaded {len(all_posts):,} cases from fallback sample dataset.")

    if all_posts:
        print_verdict_summary(all_posts)
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_posts[0].keys())
            writer.writeheader()
            writer.writerows(all_posts)
        size_mb = os.path.getsize(args.output) / (1024 * 1024)
        print(f"[DONE] Successfully saved {len(all_posts):,} records to {args.output} ({size_mb:.2f} MB)")
    else:
        print("[ERROR] No posts available to save.")
        sys.exit(1)

if __name__ == "__main__":
    main()
