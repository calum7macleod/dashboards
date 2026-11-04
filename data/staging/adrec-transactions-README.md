# ADREC transaction export - all Abu Dhabi real estate sales 2 Jan 2019 to 3 Nov 2026
Source: Abu Dhabi Real Estate Centre open data, exported by Calum 4 Nov 2026. Gzipped CSV, 126,867 rows, 19MB raw.
Columns: Asset Class, Property Type, Sale Application Date, Property Sold Area (SQM), Land Plot Ground Area (SQM), Property Layout, District, Community, Project Name, Property Sale Price (AED), Property Sold Share, Rate (AED per SQM), Sale Application Type (off-plan / ready / court-mandated), Sale Sequence (Primary / Secondary).
Read with: `curl -sH "Accept: application/vnd.github.raw" .../data/staging/adrec-transactions-2019-2026.csv.gz | gunzip | python3 -c ...` - do not load it into a chat.
Headline (PA, 4 Nov): 118.5K residential rows. Volume by year AED bn: 2019 20 · 2020 47 · 2021 18 · 2022 26 · 2023 55 · 2024 53 · 2025 93 · 2026 YTD 135. Off-plan share of applications 32% (2019) -> 78% (2026). 2026 volume by district: Hudayriyat 33.8bn, Reem 20.1, Saadiyat 18.9, Yas 13.1. Median apartment rate AED/sqm 12,256 (2019) -> 20,659 (2026); villa 8,443 -> 18,677.
Owner: Market - adopt into data/dld/ or data/adrec/ and refresh quarterly. Staged by PA.
