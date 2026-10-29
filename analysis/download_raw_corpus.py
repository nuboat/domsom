#!/usr/bin/env python3
"""
download_raw_corpus.py - Academic Reddit Dispute Corpus Downloader
Fetches authentic raw relationship conflict narratives from public research repositories.

Source: OsamaBsher/AITA-Reddit-Dataset (Pushshift AITA Corpus, 270,709 posts, arXiv:2310.18336)
Columns: id, title, text, verdict, comment1, comment2, score
"""

import os
import sys
import csv
import io
import argparse
import urllib.request

DATASET_URL = "https://huggingface.co/datasets/OsamaBsher/AITA-Reddit-Dataset/resolve/main/cleaned_dataset.csv"

def download_corpus(output_path: str, limit: int = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Connecting to academic repository: {DATASET_URL}")
    print(f"Target destination: {output_path}")
    if limit:
        print(f"Extraction limit: {limit:,} records")
    else:
        print("Extraction limit: FULL dataset (~270,709 records, ~649 MB)")

    req = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Mozilla/5.0 (Academic Research; Q1 Study)"})
    
    with urllib.request.urlopen(req, timeout=120) as resp:
        text_stream = io.TextIOWrapper(resp, encoding="utf-8", errors="ignore")
        reader = csv.reader(text_stream)
        header = next(reader)
        
        with open(output_path, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header)
            count = 0
            
            for row in reader:
                writer.writerow(row)
                count += 1
                if count % 10000 == 0:
                    print(f"  Processed {count:,} records...")
                if limit and count >= limit:
                    break

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n[DONE] Successfully saved {count:,} authentic raw records to {output_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download authentic raw Reddit dispute corpus for research.")
    parser.add_argument("--output", default="analysis/data/raw_reddit_disputes_full.csv", help="Output file path")
    parser.add_argument("--limit", type=int, default=None, help="Number of records to extract (default: all)")
    args = parser.parse_args()
    
    download_corpus(args.output, args.limit)
