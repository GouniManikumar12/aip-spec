# 04 · Auction

Each auction is initiated by a context request, followed by bid submissions, and culminates in a clearing decision.

1. **Context Request:** Defines the opportunity, constraints, and accountability metadata.
2. **Bid Submission:** Bidders respond with price, creative payload, and signals.
3. **Result Emission:** The clearinghouse communicates the winning bid, price, and settlement token.

Tie-breaking, pacing, and experimental arms are all codified within this chapter to ensure deterministic behavior.
