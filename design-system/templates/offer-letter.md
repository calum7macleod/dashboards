# Offer letter - locked template (design-system/templates/offer-letter.html)

The look is fixed. Fill the fields, render, ship. No redesign, no new fonts, no new layout - every offer looks like every other offer.

Fields: CLUSTER, UNIT, COMMUNITY (DAMAC Lagoons), OWNER (e.g. "Ms. Seema"), DATE (e.g. "23 September 2026"), PRICE, AGENCY (2% flat - Calum's convention on the letter; VAT is not itemised), CONVEY (9,950 under Đ10M), NET (price - agency - conveyancing), BUYER_INTRO (one or two sentences on the buyer: financing held, viewed, ready to sign), BUYER_POSITION (one line), NOTE_LEAD (one sentence, e.g. "This is a clean, financed offer from a decided buyer who has viewed the property."), BROKERAGE ("White & Co Real Estate" until 1 Oct 2026, then Jake's brokerage).

Render: Playwright Chromium, A4, print_background, PDF; PNG at 2x for WhatsApp. Output to content-assets/offers/<Owner>-<Unit>-Offer-<Price>M.pdf and .png. Log the offer in data/offers.json via a handoff to the PA.

Fonts: TeX Gyre Pagella (Palatino-class) + Carlito (Calibri-class) until the brand fonts are locked; when they are, the template changes once, here.
