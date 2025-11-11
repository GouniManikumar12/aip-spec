# 05 · Events & States

AMXP models every downstream action (exposure, click, conversion, ledger movements) as an event with a strongly typed schema. State machines cover how opportunities transition between `offered`, `filled`, `served`, `converted`, and `settled`.

Event order, retry semantics, and deduplication strategies are defined here to keep analytics and billing consistent across parties.
