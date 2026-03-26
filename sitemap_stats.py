#!/usr/bin/env python3
"""Sitemap index analyzer - rekurzivně projde strom sitemap a vypíše frekvenční tabulku."""

import gzip
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from urllib.request import Request, urlopen

NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
USER_AGENT = "SitemapStats/1.0"
TIMEOUT = 30


def fetch_sitemap(url: str) -> bytes:
    """Stáhne sitemapu a vrátí XML jako bytes (s podporou .gz)."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=TIMEOUT) as resp:
        data = resp.read()
    # Detekce gzip - podle URL nebo magic bytes
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def parse_sitemap(xml_bytes: bytes) -> tuple[list[str], list[str]]:
    """Rozparsuje sitemapu a vrátí (sub-sitemap URL, page URL)."""
    root = ET.fromstring(xml_bytes)
    sitemaps = [loc.text.strip() for loc in root.findall(f"{NS}sitemap/{NS}loc") if loc.text]
    urls = [loc.text.strip() for loc in root.findall(f"{NS}url/{NS}loc") if loc.text]
    return sitemaps, urls


def crawl_sitemaps(index_url: str) -> list[tuple[str, int]]:
    """Rekurzivně projde strom sitemap a vrátí [(sitemap_url, počet_url), ...]."""
    stack = [index_url]
    results = []

    while stack:
        url = stack.pop()
        print(f"  Stahuji: {url}", file=sys.stderr)
        try:
            xml_bytes = fetch_sitemap(url)
            sitemaps, urls = parse_sitemap(xml_bytes)
        except Exception as e:
            print(f"  CHYBA: {url} -> {e}", file=sys.stderr)
            continue

        if sitemaps:
            stack.extend(sitemaps)
        if urls:
            results.append((url, len(urls)))
            print(f"    -> {len(urls):,} URL", file=sys.stderr)
        elif not sitemaps:
            # Sitemap bez URL i bez sub-sitemap
            results.append((url, 0))
            print(f"    -> 0 URL (prázdná)", file=sys.stderr)

    return results


def print_table(results: list[tuple[str, int]]) -> None:
    """Vypíše frekvenční tabulku a souhrnné statistiky."""
    if not results:
        print("Nebyly nalezeny žádné sitemapy s URL.")
        return

    freq = Counter(count for _, count in results)
    total_urls = sum(count for _, count in results)
    total_sitemaps = len(results)

    print()
    print(f" {'Počet URL v sitemapě':>22} | {'Počet sitemap':>14}")
    print(f" {'-' * 22}-+-{'-' * 14}")
    for url_count in sorted(freq.keys()):
        sitemap_count = freq[url_count]
        print(f" {url_count:>22,} | {sitemap_count:>14,}")
    print(f" {'-' * 22}-+-{'-' * 14}")
    print(f" {'CELKEM':>22} | {total_sitemaps:>14,}")
    print(f"\n Celkem URL napříč všemi sitemapami: {total_urls:,}")


def main() -> None:
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Zadej URL sitemap indexu: ").strip()

    if not url:
        print("Nebyla zadána URL.", file=sys.stderr)
        sys.exit(1)

    print(f"\nAnalyzuji sitemap index: {url}\n", file=sys.stderr)
    results = crawl_sitemaps(url)
    print_table(results)


if __name__ == "__main__":
    main()
