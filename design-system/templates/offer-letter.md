# Offer letter - locked template (design-system/templates/offer-letter.html)

The look is fixed - Calum chose the card layout on 23 Sep 2026 (the 9 Sep J519 card). Fill the fields, render, ship. No redesign, no new fonts, no new layout, no rewording of the standard clauses - every offer looks like every other offer. The earlier A4 letter is archived beside it (offer-letter-a4-archived.html) and is not used.

Format: 1080x1350 card (4:5). Output PNG at 2x (WhatsApp) and PDF of the same card (email). Same file, both outputs.

Fields (double braces in the HTML): UNIT, CLUSTER, COMMUNITY (DAMAC Lagoons), OWNER (e.g. "Ms. Seema"), DATE (e.g. "23 September 2026"), PRICE, AGENCY, CONVEY, NET, BUYER_POSITION (one line, e.g. "Qualified · ready to sign MOU on acceptance"), BROKERAGE ("White & Co Real Estate" until 1 Oct 2026, then Jake's brokerage).

Numbers: AGENCY = 2% flat (Calum's convention on the letter; VAT is not itemised). CONVEY = 9,950 under Đ10M. NET = PRICE - AGENCY - CONVEY. Standard clauses are fixed in the HTML: 60 days to complete from signed MOU, 10% cheque on MOU (Form F), fees borne by seller as itemised, 5-day validity, non-binding until Form F.

Render: `python3 design-system/templates/render-offer.py fields.json content-assets/offers/` - computes AGENCY/CONVEY/NET from PRICE, writes <Owner>-<Unit>-Offer-<Price>M.html/.png/.pdf. Playwright Chromium, 2x. Then log the offer in data/offers.json via a handoff to the PA.

Fonts: TeX Gyre Pagella (Palatino-class) + Carlito (Calibri-class) until the brand fonts are locked; when they are, the template changes once, here. Both must be installed where you render - if the output shows DejaVu, the fonts were missing and the render is wrong.
