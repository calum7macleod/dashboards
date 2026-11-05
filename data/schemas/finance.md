# Finance data rules - data/finance.json (Manager owns the schema, Finance owns the data, Uploader appends)
Written 5 Nov 2026 from h0020 + h0022.

## transactions[] record
{day, month ("Oct 2026"), description, account, amount, currency, category, sub?, note?, source?, need?, retired?}

## Rules
1. SIGN - statement style from now on: negative = money out, positive = money in. This is what statements and the Uploader produce. The file carries `"signConvention": "statement"` at the top level once Finance has flipped the old rows (they were spend-positive). Until that key is present, finance.html treats amounts as spend-positive. Finance sets the key at the rebuild - never half-flip.
2. CURRENCY - every row carries `currency` (AED | GBP | USD). Missing = AED (legacy). Never add across currencies, never convert in the file. finance.html sums AED only and shows other currencies aside as "not added".
3. RETIRED - a row with a `retired` field (any value) is dead: excluded from every sum, chart and count. Finance retires; nobody deletes.
4. The Uploader appends rows as the statement shows them (statement sign, currency set). Finance reconciles and categorises. Account names only - no account or card numbers in any file.
