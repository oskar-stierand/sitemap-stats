
How to use it:

python3 sitemap_stats.py https://example.com/sitemap_index.xml
# or no argument - asks interactively
python3 sitemap_stats.py

What it can do:

Recursively traverses the entire sitemap tree (index → ​​sub-indexes → final sitemaps)
Supports gzipped sitemaps (.xml.gz)
Continuously prints progress to stderr
Displays frequency table + grand total at the end
No external dependencies - just stdlib
