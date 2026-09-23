# DESIGNER STATE - queue and piece log. Updated 2026-09-23 by Designer Sept 26.

## Queue
LOCKED 23 Sep (Calum's call, the 9 Sep J519 card): design-system/templates/offer-letter.html = the 1080x1350 card, every offer to a seller. Fields only - no redesign, no new fonts, no layout changes. Agency 2% flat (VAT not itemised), conveyancing 9,950 under Đ10M, PNG 2x + PDF, path content-assets/offers/<Owner>-<Unit>-Offer-<Price>M. Render with templates/render-offer.py fields.json. A4 letter archived as offer-letter-a4-archived.html, not used. Same rule for any future template in design-system/templates/.

1. design-system/ - lock the fonts with Calum (licensed, bespoke), write the tokens and rules. Everything else waits on this. STATUS 21 Sep: Calum's steer = wide geometric sans (said 'Montserrat wide' - no such cut exists). Specimen round 1 out: sans A Montserrat / B Archivo Expanded / C Mona Sans Expanded, serif Newsreader Display vs Libre Caslon Display / Bodoni Moda / Gloock. All OFL, Đ0. Designer rec: B + Newsreader. AWAITING CALUM'S PICK. Assumed Latin only (no Arabic) - unconfirmed. On lock: commit fonts to design-system/fonts/, write tokens.css, update README.
2. Fix or bin the Wadeem 5/15/80 mortgage carousel (wrong vs official 25/75).
3. Options pack template (Bashayer standard) ready for Tuesday's buyer callouts.
4. YouTube thumbnail template (face + three words + one number).

## Piece log
- 23 Sep: Offer-letter template rebuilt as the card (Calum's pick), + render-offer.py + rules + sample render - design-system/templates/ (Designer Sept 26).
- 23 Sep: Seema J519 Costa Brava offer Đ2.65M - SUPERSEDED. My freehand 4:5 image (2% + VAT, own fonts) was off-template and wrong; redone from the locked template by Calum, same path content-assets/offers/Seema-J519-Offer-2.65M.pdf/.png (net Đ2,587,050 at 2% flat). Not mine to touch.
- 21 Sep: Type specimen round 1 (4pp A4 landscape), for Calum - design-system/specimens/2026-09-21-type-specimen.pdf + .html (Designer Sept 26).
- 21 Sep: Lewis CRM build brief PDF (7pp) - content-assets/lewis/crm-build-brief.pdf (Max).
- Earlier: Wadeem Investor Briefing v4 (13pp), insider carousel v2, keys-2031 carousel, mortgage cards, Tara schedules, Marsa guide v2, Amer income plan + calculator, Tyron Yas Point, B4-412 - all in content-assets/.
