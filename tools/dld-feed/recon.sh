#!/bin/bash
# DLD FEED RECON v0 - run on droplet. Finds the real download URLs + sizes for DLD open datasets.
# No downloads > 1KB happen here. Output is what Max needs to build the collector.
echo "=== DLD RECON $(date -u +%FT%TZ) ==="
for page in \
  "https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open" \
  "https://www.dubaipulse.gov.ae/data/dld-registration/dld_transactions-open" \
  "https://www.dubaipulse.gov.ae/organisation/dubai-land-department" ; do
  echo "--- PAGE: $page"
  curl -sL --max-time 30 "$page" -o /tmp/dld_page.html -w "http:%{http_code} size:%{size_download}\n"
  grep -oE 'https?://[^"'\'' ]+\.(csv|zip|xlsx)[^"'\'' ]*' /tmp/dld_page.html | sort -u | head -20
  grep -oE '/api/[^"'\'' ]+' /tmp/dld_page.html | sort -u | head -10
done
echo "--- HEAD known candidate CSVs"
for f in \
  "https://www.dubaipulse.gov.ae/dataset/00768c45-f014-4cc6-937d-2b17dcab53fb/resource/a37511b0-ea36-485d-bd7f-6bc7d66d0e5c/download/transactions.csv" ; do
  echo "$f"; curl -sIL --max-time 30 "$f" | grep -iE "HTTP/|content-length|content-type|location" | head -6
done
echo "=== END RECON - paste ALL of this back to Max ==="
