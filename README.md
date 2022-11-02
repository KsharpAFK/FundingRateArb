# FundingRateArb

Funding rate is used in perpetual futures in cryptocurrency trading. Every 8 hours, anyone with an open position has to pay a funding fee.
If funding rate is negative, all short position holders have to pay
If funding rate positive, all long position holders have to pay.

This project waits for the time of funding, and opens a position and holds for 1 second. After funding fee is received, the position is closed immediately.
The position is hedged in the spot market on binance as it is commission free.
