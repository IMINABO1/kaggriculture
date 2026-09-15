# elmo (rank 22, score 2932.4, next-15)

- team id 16811307; current submission 56234758 (102 public games)
- 22 submissions found; 3469 public games from 2026-09-04 to 2026-09-15; 32 of them with a known rating
- sampled games with a replay: 52

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 1-1-0 | 50 | 115531.5 | 115531.5 | 2976.5 | 50 | 1.32.7 | 2026-09-14 | 2026-09-14 |
| C0 | 50 | 46-4-0 | 92 | 106007.5 | 109760.8 | 2184.5 | 38 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 697, game 10: 1566, game 25: 2564, game 50: 2826, game 100: 2928, game last: 2929

![rating](figs/elmo_rating.png)

## Farm plan by window (median per game)

| median per game | L | C0 |
|---|---|---|
| hands (peak) | 12 | 12 |
| quadrants | 3 | 3 |
| land day 1 | 6 | 6 |
| land day 2 | 11 | 11 |
| cows bought | 7.5 | 7 |
| sheep bought | 5.5 | 6 |
| geese bought | 4 | 3 |
| first cow day | 0 | 0 |
| wheat planted | 135.5 | 158 |
| carrot planted | 57.5 | 35 |
| tomato planted | 0 | 0 |
| strawberry planted | 33 | 33 |
| melon planted | 12 | 12 |
| FERTILIZE ops | 114.5 | 112.5 |
| CARE ops | 405 | 405 |
| melon sold | 12 | 12 |
| strawberry sold | 132 | 131 |
| milk sold | 129.5 | 101 |
| wool sold | 70 | 84 |
| wheat sold | 732 | 1215.5 |
| fertilizer sold | 283.5 | 278 |
| units sold last 3 days | 271.5 | 266 |
| shed peak | 45 | 45 |
| weeds spawned | 19 | 19 |
| unexecutable market orders | 1 | 1 |

![money by day](figs/elmo_money.png)

## A typical recent game, day by day

Episode 109041867 (the median-bank game of the latest window): seat 0, bank 156087 vs 154966 (Kilupy), seed 276057442. Letters: W wheat, C carrot, T tomato, S strawberry, M melon, E egg, Mk milk, Wl wool, F fertilizer.

| day | money | hands | quads | bought | built | planted | care/fert | harvest | sold | revenue | farm at day end | new weeds | shop unlock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3000 | 5 | 1 | cow2 sheep2 \| W7 M12 | pasture 4  | W7 M12 | 3/0 | 0 |  | 0 | cow2 sheep2; W7 M12 |  |  |
| 1 | 22 | 3 | 1 |  | pasture 2  |  | 4/0 | 0 |  | 0 | cow2 sheep2; W7 M12; empty pens 2 |  |  |
| 2 | 81 | 4 | 1 | cow1 \| W3 |  | W3 | 5/0 | 3 | W2 F1 | 159 | cow3 sheep2; W7 M12; empty pens 1 |  |  |
| 3 | 194 | 5 | 1 | cow1 \| W4 |  | W4 | 6/0 | 4 | W4 | 120 | cow3 sheep2; W7 M12; empty pens 1 |  | Ice Cream |
| 4 | 277 | 4 | 1 | W3 |  | W3 | 6/0 | 3 | W2 F1 | 155 | cow4 sheep2; W7 M12 |  |  |
| 5 | 682 | 4 | 1 | S4 |  | S4 | 7/0 | 4 | W2 F1 | 155 | cow4 sheep2; W3 S4 M12 |  |  |
| 6 | 797 | 7 | 2 | cow2 \| W5 S8 | pasture 7  | W5 S8 | 8/0 | 5 | W9 Wl2 F4 | 1039 | cow6 sheep2; W6 S12 M12; empty pens 5 |  | Smoothie |
| 7 | 1121 | 7 | 2 | cow2 \| W4 S4 |  | W4 S4 | 11/0 | 0 | F2 | 175 | cow8 sheep2; W8 S16 M12; empty pens 3 |  |  |
| 8 | 541 | 8 | 2 | sheep2 \| W1 S4 |  | W1 S4 | 13/0 | 7 | W2 F2 | 240 | cow8 sheep4; W5 S20 M12; empty pens 1 |  |  |
| 9 | 1776 | 8 | 2 | cow1 sheep1 \| W4 |  | W4 | 15/0 | 6 | W2 F7 | 631 | cow9 sheep4; W5 S20 M12 |  | Ice Cream |
| 10 | 2615 | 11 | 2 | goose2 \| W7 | pasture 1 coop 4 | W7 | 16/0 | 15 | W3 F9 | 817 | goose2 cow9 sheep5; W12 S20; empty pens 2 |  |  |
| 11 | 16622 | 10 | 3 | goose1 \| W11 S13 |  | W11 S13 | 18/0 | 4 | W9 M12 F14 | 3000 | goose3 cow9 sheep5; W21 S33; empty pens 1 |  |  |
| 12 | 15856 | 9 | 3 | W8 |  | W8 | 17/0 | 8 | W9 Mk6 F16 | 2887 | goose3 cow9 sheep5; W24 S33; empty pens 1 |  | Smoothie |
| 13 | 19580 | 9 | 3 | W6 |  | W6 | 19/2 | 8 | W19 F17 | 1857 | goose3 cow9 sheep5; W24 S33; empty pens 1 |  |  |
| 14 | 22649 | 9 | 3 | W7 |  | W7 | 16/5 | 16 | Wl3 F15 | 844 | goose3 cow9 sheep5; W24 S33; empty pens 1 |  |  |
| 15 | 26494 | 10 | 3 | W8 |  | W7 | 17/8 | 19 | W8 E6 Mk9 F16 | 3616 | goose3 cow9 sheep5; W24 S33 |  | Farmers Market |
| 16 | 35073 | 11 | 3 | W8 |  | W8 | 18/4 | 23 | W6 E6 Mk6 Wl5 F11 | 2467 | goose3 cow9 sheep5; W25 S33 |  |  |
| 17 | 42434 | 11 | 3 | W7 |  | W7 | 17/4 | 22 | W7 E4 Mk3 F13 | 1733 | goose3 cow9 sheep5; W25 S33 |  |  |
| 18 | 47632 | 11 | 3 | W7 |  | W7 | 17/4 | 28 | W9 E4 Mk9 Wl2 F14 | 3261 | goose3 cow9 sheep5; W25 S33 |  | Farmers Market |
| 19 | 55843 | 10 | 3 | W6 |  | W6 | 17/8 | 20 | W3 S8 E6 Mk15 Wl1 F9 | 6220 | goose3 cow9 sheep5; W25 S33 |  |  |
| 20 | 64868 | 11 | 3 | W6 |  | W6 | 17/16 | 26 | W6 S10 Mk6 Wl1 F6 | 4329 | goose3 cow9 sheep5; W25 S33 |  |  |
| 21 | 72840 | 11 | 3 | W11 |  | W11 | 17/3 | 35 | W186 S6 E12 Mk9 Wl4 F13 | 12692 | goose3 cow9 sheep5; W30 S28 |  | Pizza |
| 22 | 83760 | 11 | 3 | W8 |  | W8 | 17/9 | 27 | W211 S16 E9 Mk15 Wl3 F18 | 17575 | goose3 cow9 sheep5; W31 S27 | 1 |  |
| 23 | 92739 | 11 | 3 | W14 |  | W14 | 17/6 | 31 | W235 S17 E5 Mk15 Wl2 F19 | 18526 | goose3 cow9 sheep5; W38 S20 | 7 |  |
| 24 | 102153 | 12 | 3 | W9 C4 |  | W9 C4 | 17/26 | 24 | W24 S22 E9 Mk9 Wl7 F5 | 8743 | goose3 cow9 sheep5; W37 C4 S17 | 3 | Pet Cafe |
| 25 | 109948 | 11 | 3 | C14 |  | C14 | 17/8 | 29 | W149 S10 E4 Mk21 F16 | 14279 | goose3 cow9 sheep5; W27 C18 S13 | 4 |  |
| 26 | 118709 | 11 | 3 | W1 C20 |  | C12 | 17/6 | 18 | W237 S21 Mk9 Wl3 F13 | 17187 | goose3 cow9 sheep5; W15 C30 S13 |  |  |
| 27 | 126667 | 11 | 3 | W8 C2 |  | C10 | 17/7 | 33 | W42 E2 Mk12 Wl4 F18 | 5045 | goose3 cow9 sheep5; W9 C35 S4 |  |  |
| 28 | 133377 | 11 | 3 |  | coop 1 |  | 15/0 | 28 | W17 C17 S20 Mk19 Wl5 F10 | 11370 | goose3 cow9 sheep5; W1 C22; empty pens 1 | 4 |  |
| 29 | 145418 | 11 | 3 |  |  |  | 4/0 | 33 | W47 C38 E8 Mk1 F8 | 4138 | goose3 cow9 sheep5; empty pens 1 |  |  |

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 2 (50%) | 2 (50%) | 2 (50%) | 2 (50%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 6 (50%) | 8 (34%) | 34 (16%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 2 (50%) | 2 (50%) | 2 (50%) | 2 (50%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 5 (50%) | 9 (34%) | 34 (12%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 2 (50%) | 2 (50%) | 2 (50%) | 2 (50%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 6 (50%) | 10 (34%) | 32 (16%) | 50 (2%) |

Current submission (52 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 35 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (96%), then branching (3 lines at turn 136, 35 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (96%), then branching (3 lines at turn 136, 33 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 50 | 96.2 |
| 48 | 2 | 3 | 50 | 96.2 |
| 100 | 4 | 3 | 50 | 96.2 |
| 136 | 5 | 3 | 50 | 96.2 |
| 200 | 8 | 6 | 26 | 50 |
| 300 | 12 | 9 | 18 | 34.6 |
| 400 | 16 | 35 | 9 | 17.3 |
| 719 | 29 | 52 | 1 | 1.9 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 1 | 100 | 49.0 |
| opponent off its modal line at turn 136 | 26 | 42.3 | 57.7 |
| played seat 1 | 32 | 50 | 50 |
| lost the game | 5 | 80 | 46.8 |
| first shop (day 3) is not Bakery | 40 | 47.5 | 58.3 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 50 | 115531.5 | 12 | 7.5 | 5.5 | 4 | 3 | 6 | 33 | 135.5 | 12 | 12 | 129.5 | 70 | 2 | 2 |
| C0 | 50 | 92 | 106007.5 | 12 | 7 | 6 | 3 | 3 | 6 | 33 | 158 | 12 | 12 | 101 | 84 | 34 | 34 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108992350 | ManasviSharma | 2744.9 | 83290 | 84734 | -1444 | 9b0c82fd | strawberry sold: they 117 vs me 138; milk sold: they 91 vs me 76; units sold last 3 days: they 271 vs me 263 |
| C0 | 108995432 | TIM | 2781.2 | 145778 | 145873 | -95 | 9b0c82fd | wheat planted: they 163 vs me 154; strawberry sold: they 141 vs me 144; milk sold: they 167 vs me 164 |
| C0 | 108996452 | Phi | 2713.5 | 81166 | 81310 | -144 | 9b0c82fd | wool sold: they 197 vs me 280; units sold last 3 days: they 228 vs me 278; FERTILIZE ops: they 61 vs me 105 |
| C0 | 109001674 | alcanta | 2848.5 | 90609 | 91472 | -863 | 9b0c82fd | units sold last 3 days: they 274 vs me 269; strawberry sold: they 141 vs me 138; CARE ops: they 397 vs me 400 |
| L | 109051739 | Artem The Farmer 🍅 | 3021.3 | 74976 | 87865 | -12889 | d6cc83df | CARE ops: they 321 vs me 405; FERTILIZE ops: they 153 vs me 113; strawberry sold: they 99 vs me 134 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 2 | 0 |
| 16622198 | 4 | 1 | 0 |
| 16622349 | 5 | 2 | 0 |
| 16633100 | 0 | 1 | 0 |
| 16637255 | 1 | 3 | 0 |
| 16640510 | 3 | 3 | 0 |
| 16644724 | 0 | 8 | 1 |
| 16675778 | 1 | 2 | 0 |
| 16719123 | 6 | 3 | 1 |
| 16725899 | 1 | 1 | 0 |
| 16730612 | 0 | 2 | 0 |
| 16730761 | 1 | 3 | 0 |
| 16732403 | 0 | 1 | 0 |
| 16732521 | 4 | 7 | 0 |
| 16732748 | 1 | 0 | 0 |
| 16758882 | 1 | 3 | 0 |
| 16760569 | 1 | 1 | 0 |
| 16773026 | 1 | 1 | 0 |
| 16777134 | 2 | 0 | 0 |
| 16778640 | 3 | 0 | 0 |
| 16805699 | 2 | 4 | 0 |
| 16833141 | 2 | 0 | 0 |
| 16845367 | 0 | 1 | 0 |
| 16858228 | 2 | 1 | 0 |

## Episodes behind each window

- **L** (2): 109041867, 109051739
- **C0** (50): 108961224, 108962536, 108963273, 108964259, 108965302, 108966322, 108967367, 108968352, 108969385, 108970418, 108971435, 108972472, 108973498, 108974522, 108975553, 108976583, 108977649, 108978675, 108979717, 108980797, 108981816, 108982887, 108983928, 108984958, 108986007, 108987035, 108987707, 108988092, 108988434, 108989410, 108990187, 108991230, 108991534, 108992276, 108992350, 108993328, 108994368, 108994522, 108995432, 108996452, 108997477, 108997500, 108998525, 108999567, 109000611, 109000667, 109001103, 109001674, 109002693, 109003739
