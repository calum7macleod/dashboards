#!/bin/bash
# DLD RECON 2 - which doors open from the droplet. Tiny requests only.
echo "=== DLD RECON2 $(date -u +%FT%TZ) ==="
echo "--- 1. dubailand.gov.ae reachability"
curl -sIL --max-time 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126" "https://dubailand.gov.ae/en/open-data/real-estate-data/" | grep -iE "HTTP/|server|location" | head -5
echo "--- 2. DLD gateway API probe (transactions search backend)"
curl -s --max-time 25 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126" -H "Content-Type: application/json" -X POST "https://gateway.dubailand.gov.ae/open-data/transactions" -d '{"P_FROM_DATE":"08/01/2026","P_TO_DATE":"08/03/2026","P_GROUP_ID":"","P_IS_OFFPLAN":"","P_IS_FREE_HOLD":"","P_AREA_ID":"","P_USAGE_ID":"","P_PROP_TYPE_ID":"","P_TAKE":"5","P_SKIP":"0","P_SORT":"TRANSACTION_NUMBER_ASC"}' -w "\nhttp:%{http_code} bytes:%{size_download}\n" | head -c 1200
echo ""
echo "--- 3. dubaipulse retry with browser UA + http1.1"
curl -sI --http1.1 --max-time 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126" "https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open" -w "http:%{http_code}\n" | grep -iE "HTTP/|http:" | head -3
echo "--- 4. droplet public IP + region hint"
curl -s --max-time 10 https://ipinfo.io/json | head -c 300
echo ""
echo "=== END RECON2 - paste ALL back to Max ==="
