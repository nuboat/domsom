#!/usr/bin/env python3
"""
scrape_reddit_live.py - Live Reddit Dispute Scraper
Fetches live, real-time dispute threads from target subreddits using Reddit's public JSON API.

Target Subreddits:
- r/AmItheAsshole
- r/relationship_advice
- r/marriage
- r/family_issues
"""

import os
import sys
import csv
import json
import time
import argparse
import urllib.request

SUBREDDITS = ["AmItheAsshole", "relationship_advice", "marriage", "family_issues"]

def fetch_subreddit_posts(subreddit: str, listing: str = "new", limit: int = 100):
    url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Academic Research; Naturalistic Behavioral Study 1.0)"}
    )
    posts = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            children = data.get("data", {}).get("children", [])
            for child in children:
                p = child.get("data", {})
                # Filter out pinned/mod announcements
                if p.get("stickied", False):
                    continue
                posts.append({
                    "id": p.get("id"),
                    "subreddit": p.get("subreddit"),
                    "title": p.get("title", "").replace("\n", " "),
                    "selftext": p.get("selftext", "").replace("\n", " "),
                    "author": p.get("author"),
                    "created_utc": p.get("created_utc"),
                    "score": p.get("score"),
                    "num_comments": p.get("num_comments"),
                    "url": f"https://reddit.com{p.get('permalink')}"
                })
    except Exception as e:
        print(f"Error fetching r/{subreddit}: {e}")
    return posts

def main():
    parser = argparse.ArgumentParser(description="Live scraper for Reddit relationship dispute threads.")
    parser.add_argument("--subreddits", nargs="+", default=SUBREDDITS, help="Subreddits to scrape")
    parser.add_argument("--limit-per-sub", type=int, default=50, help="Posts per subreddit (max 100)")
    parser.add_argument("--output", default="analysis/data/raw_reddit_live_posts.csv", help="Output CSV path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    all_posts = []

    print("=== Live Reddit Relationship Dispute Scraper ===")
    for sub in args.subreddits:
        print(f"Scraping r/{sub}...")
        posts = fetch_subreddit_posts(sub, limit=args.limit_per_sub)
        print(f"  Retrieved {len(posts)} posts from r/{sub}")
        all_posts.extend(posts)
        time.sleep(1.5)  # Respect polite crawling rate limits

    if all_posts:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_posts[0].keys())
            writer.writeheader()
            writer.writerows(all_posts)
        print(f"\n[DONE] Saved {len(all_posts)} live posts to {args.output}")
    else:
        print("No posts retrieved.")

if __name__ == "__main__":
    main()
