Jak ho použít:

python3 sitemap_stats.py https://example.com/sitemap_index.xml
# nebo bez argumentu - zeptá se interaktivně
python3 sitemap_stats.py

Co umí:

Rekurzivně prochází celý strom sitemap (index → sub-indexy → koncové sitemapy)
Podporuje gzipované sitemapy (.xml.gz)
Průběžně vypisuje progress na stderr
Na konci zobrazí frekvenční tabulku + celkový součet
Žádné externí závislosti - jen stdlib
