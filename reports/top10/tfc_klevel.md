# THIRD FARM CLUB at levels K1, K2 and K3

Built 2026-09-17 by `scripts/top10/klevel.py --team "THIRD FARM CLUB"` from the 135 encoded
games of its current submission 56279316 (2026-09-16 to 09-17 03:10Z, the crawl cutoff),
`data/top10/klevel_third-farm-club.parquet`; executed sales and purchases from the market
replica (`research/market_replay.py`; 6 of 135 games carry a last-step money mismatch, the
known bounded gap of P18). Opponent classes: "line" = the opponent's field line through turn
136 equals the public tape's (v41 and v7 share it; 63 games), "top10" = a top-10 team by the
gold snapshot (27 games), "other" = everyone else (45 games). Every figure names its count.

## Why this team

Among the top ten's current submissions it is the only one whose field play is one line
deep into the game: 135 of 135 games identical through turn 24, 128 through turn 48, 104
through turn 144 (77%, strict comparison of every unit op and market order; the study's
looser field hash gave 98% through turn 136), 25 through turn 200. Majkel1337 has 73
different openings at turn 24 in 228 games; DSM 4; SpaTaro injects noise. Its median bank
(111k) is the highest of the ten. Its branching after turn 144 is not a route table: games
sharing the first two shops agree 0.55 at turn 200 and 0.28 at turn 300 (21 shop pairs
with three or more games), so the second half is a runtime policy, not a tape.

## K1: the field it plays against

| opponent class | games | win rate | median margin | opponent's median bank |
|---|---|---|---|---|
| line (v41/v7 tape) | 63 | 0.92 | +12,718 | 99,715 |
| other | 45 | 0.93 | +12,364 | 92,684 |
| top-10 team | 27 | 0.33 | -2,406 | 112,147 |

The margin over the line does not depend on the shop draw: median +13,030 with a Yarn
Store by day 9 (16 games) against +12,370 without (47); +12,370 with a milk shop (51)
against +13,586 without (12); +9,780 with an egg shop (35) against +13,498 without (28);
+12,370 with a carrot shop (35) against +13,535 without (28). Its own bank moves with the
town (95k to 126k) but the line's moves with it. Gate G0's artefact test is passed.

## K2: how it beats the line (means over the 63 line games, own / line)

- **Gross revenue is equal, spending is not**: 142,772 against 141,610 in sales, but it
  spends 23,044 on seeds, animals and products against the line's 33,741. It buys no
  fertilizer: 176 FERTILIZE ops against 114 from its own 259 collected units (the line
  sells 347 and buys back what it spreads). About 10.7k of the 12.7k margin is the
  purchase bill.
- **Product mix**: wheat 12,081 (298 units, 20 lots) against 27,757 (658 units); carrots
  9,118 against 4,959; tomatoes 6,751 against 980 (81 units against 8); eggs 8,171
  against 3,780 (164 against 77 units, 5-7 geese); milk 30,565 against 27,583 on fewer
  units (209 against 219); wool 20,462 against 18,793 on fewer units (133 against 155);
  strawberries 28,086 against 26,972 on far fewer units (177 against 246, $159 against
  $110 a unit); melon 14,728 against 15,719 (93 units against 72). The last three days
  bring 31,020 against 21,725.
- **Sale hours**: it sells first thing in the morning where the line dumps in the
  afternoon. Share of revenue at hours 0-1 / 2-11 / 12-19 / 20-23: milk 42/29/8/20
  against the line's 23/39/27/10; eggs 72/15/0/13 against 57/5/12/26; wool 34/40/9/16
  against 22/38/23/17; strawberries 26/28/32/14 against 12/9/41/38; melon 40/41/17/2
  against 12/64/24/0; wheat 65/0/1/35 against 11/24/35/30. Its premium units are in the
  market before the line's lots of the same day, and its strawberries are few and early
  (planted from day 2; 33 on the farm at day 16, 5 left at day 24 against the line's 20).
- **Herd and crops by the shop draw** (with / without the shop by day 9): Yarn Store
  sheep 11.5 / 3.5 and cows 6.8 / 10.5 (37 / 98 games); milk shop cows 10.1 / 7.5 (105 /
  30); egg shop geese 6.6 / 3.9 (78 / 57); carrot shop carrots planted 59.1 / 31.6 (75 /
  60); tomatoes 12 whatever the draw; strawberries 31-32 whatever the draw. Hands by day
  (median): 4, 4, 6, 6, 6, 6, 11, 9, 9, 12, 13, then 9-11 to the end.
- **Farm at day 16** (one game, typical): 33 strawberries, 7 tomatoes, 13 wheat, 3 melons,
  18 animals; the line: 33 strawberries, 24 wheat, 17 animals. At day 24 (means): 25.5
  wheat, 8.3 carrots, 6.7 tomatoes, 5.3 strawberries, 4.5 weeds; the line: 37 wheat, 19.9
  strawberries, 0.2 weeds.

So the K2 mechanisms, in order of dollar weight: no purchases of fertilizer or feed
beyond need (about 10k), a diversified late economy the line's dumps do not crash (eggs,
tomatoes, carrots: about 14k of revenue against the line's 10k), selling first each
morning (higher unit prices on milk, wool and strawberries: about 3k), and a strong
last-three-days liquidation (+9k), against a smaller wheat and strawberry volume (-15k).

## K3: what beats it

26 losses in 135 games: 18 to top-10 teams, 5 to the line (margins -58 to -1,083, coin
flips), 3 to others. Against top-10 teams it is 9-18. What the peer winners did in those
18 games (means, opponent / own): wheat planted 175 / 130 and wheat units sold 504 / 298;
strawberry units 193 / 160; carrots planted 41 / 51; tomatoes 11 / 14; geese 2.8 / 5.9;
hands 9.5 / 9.3; fertilize ops 163 / 170; gross revenue 134,076 / 127,810; spend
21,769 / 23,479; last three days 20,641 / 27,092. The loss table names the product the
winner was ahead on: wheat in 16 of 26 top-3 lists (DSM +13.4k, SpaTaro +23.9k, Sida Zuo
+13.6k), strawberries in 10 (Orbital Terraformer +8.7k to +11.9k, SpaTaro +22.2k, Arda
Ceylan +10.3k), wool on Yarn Store towns in 3 (Arda Ceylan +34.8k, Orbital Terraformer
+16.9k), carrots on triple-Pet-Cafe towns in 2 (ymg_aq +28.2k, Sida Zuo +12.9k).

Hypotheses tested: (a) front-running by the opponent: rejected, its own share of premium
revenue at hours 0-1 is 40-61% in the losses against the winners' 11-42%; (b) Yarn Store
towns to sheep-heavy opponents: 10 of 26 losses on Yarn towns against 27% of games, and
the two largest margins (-35.9k, -16.5k) are wool losses, so it holds for the big losses;
(c) larger strawberry fields: the winners sell 193 strawberry units to its 160 in the 18
peer losses. The dominant K3 reading is volume: the peers keep its morning-sale timing
(their own early share is 11-42%, the line's 8-15%) and out-produce it in bulk wheat and
strawberries; it out-produces them only in geese, tomatoes and the last three days.

## What the clone keeps and what it adds

Keep (K2): the opening line as a tape through turn 144; the shop-conditioned herd and
carrot counts; no fertilizer or feed purchases beyond need; morning sales of every premium
product from the previous day's harvest; tomatoes and geese; the last-three-days sale.
Add (K3), each as a single measured change after the clone reproduces the K2 play: a
larger wheat volume on the tiles it leaves empty or weeded (2.7 empty and 4.5 weeds at
day 24), and on Yarn Store towns the sheep count the peers use (the study's SpaTaro 20,
v41's Yarn route 14-17) instead of its 11.5. Nothing else: its carrot and tomato
responses already match the peers', and its timing is already the front-running kind.

## Caveats

Its 135 games are one week of one submission on a ladder where 47% of its opponents were
the public line; the gold teams' ratings above 3,000 come from beating that line, and the
peers' record against it (18-9) says a faithful clone lands near its own 3,005, not above
the peers. The market replica's last-step gap affects 6 games by at most a few hundred
dollars. "Top10" uses today's snapshot ranks; Artem The Farmer is absent from its
opponents. The K3 volume reading rests on 18 games.
