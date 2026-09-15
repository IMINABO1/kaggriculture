# Kaggriculture Agent (rank 31, score 2912.0, next-15)

- team id 16644724; current submission 56230957 (116 public games)
- 76 submissions found; 8989 public games from 2026-07-31 to 2026-09-15; 89 of them with a known rating
- sampled games with a replay: 51

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 0-1-0 | 0 | 59081 | 59081 | 1140.1 | 100 | 1.32.2 | 2026-07-31 | 2026-07-31 |
| C0 | 50 | 45-5-0 | 90 | 99096 | 104391.4 | 2250.5 | 64 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 715, game 10: 1608, game 25: 2658, game 50: 2873, game 100: 2917, game last: 2907

![rating](figs/kaggriculture-agent_rating.png)

## Farm plan by window (median per game)

| median per game | F | C0 |
|---|---|---|
| hands (peak) | 10 | 12 |
| quadrants | 2 | 3 |
| land day 1 | 11 | 6 |
| land day 2 |  | 11 |
| cows bought | 14 | 8 |
| sheep bought | 0 | 6 |
| geese bought | 0 | 3 |
| first cow day | 0 | 0 |
| wheat planted | 4 | 158 |
| carrot planted | 0 | 36 |
| tomato planted | 0 | 0 |
| strawberry planted | 2 | 33 |
| melon planted | 10 | 12 |
| FERTILIZE ops | 0 | 116 |
| CARE ops | 241 | 408 |
| melon sold | 48 | 12 |
| strawberry sold | 0 | 139 |
| milk sold | 307 | 154 |
| wool sold | 0 | 109 |
| wheat sold | 18 | 3870.5 |
| fertilizer sold | 105 | 270 |
| units sold last 3 days | 77 | 569 |
| shed peak | 23 | 58 |
| weeds spawned | 13 | 20 |
| unexecutable market orders | 0 | 45 |

![money by day](figs/kaggriculture-agent_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| C0 | 50 | 3 (88%) | 7 (46%) | 7 (46%) | 7 (46%) | 19 (28%) | 25 (20%) | 27 (18%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| C0 | 50 | 7 (50%) | 9 (32%) | 9 (32%) | 9 (32%) | 28 (18%) | 40 (8%) | 48 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| C0 | 50 | 5 (50%) | 9 (32%) | 9 (32%) | 9 (32%) | 26 (22%) | 37 (8%) | 46 (4%) | 50 (2%) |

Current submission (50 sampled games): field is **reactive from day 1: 3 openings at turn 24 (largest 88%), 7 lines at turn 100; every game distinct by turn 719**; market is **reactive from day 1: 7 openings at turn 24 (largest 50%), 9 lines at turn 100; every game distinct by turn 719**; plan is **reactive from day 1: 5 openings at turn 24 (largest 50%), 9 lines at turn 100; every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 44 | 88 |
| 48 | 2 | 7 | 23 | 46 |
| 100 | 4 | 7 | 23 | 46 |
| 136 | 5 | 7 | 23 | 46 |
| 200 | 8 | 19 | 14 | 28 |
| 300 | 12 | 25 | 10 | 20 |
| 400 | 16 | 27 | 9 | 18 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 24 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 1 | 0 |  | 12 |
| opponent off its modal line at turn 24 | 11 | 0 | 15.4 |
| played seat 1 | 18 | 22.2 | 6.2 |
| lost the game | 5 | 20 | 11.1 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 0 | 59081 | 10 | 14 | 0 | 0 | 2 | 11 | 2 | 4 | 10 | 48 | 307 | 0 | 1 | 1 |
| C0 | 50 | 90 | 99096 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 158 | 12 | 12 | 154 | 109 | 27 | 48 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| F | 89061335 | Danilo_Malbashich | 1140.1 | 59081 | 78212 | -19131 | 4ca76d17 | milk sold: they 112 vs me 307; units sold last 3 days: they 208 vs me 77; CARE ops: they 366 vs me 241 |
| C0 | 108931203 | makishis | 2695.2 | 77686 | 77705 | -19 | 9b0c82fd | units sold last 3 days: they 266 vs me 553; milk sold: they 93 vs me 155; wheat planted: they 162 vs me 189 |
| C0 | 108934575 | Friedhelm Winter | 2695.9 | 64109 | 66541 | -2432 | 9b0c82fd | units sold last 3 days: they 266 vs me 574; milk sold: they 105 vs me 152; strawberry sold: they 135 vs me 150 |
| C0 | 108938524 | Bernardus | 2774.7 | 79091 | 79302 | -211 | 9b0c82fd | units sold last 3 days: they 264 vs me 584; wool sold: they 42 vs me 68; FERTILIZE ops: they 124 vs me 115 |
| C0 | 108945959 | kaggricodex | 2808.5 | 81101 | 81434 | -333 | 9b0c82fd | units sold last 3 days: they 244 vs me 581; wool sold: they 56 vs me 109; milk sold: they 115 vs me 158 |
| C0 | 108949771 | nilochan | 2915.4 | 170502 | 171838 | -1336 | 9b0c82fd | units sold last 3 days: they 257 vs me 581; milk sold: they 99 vs me 158; wool sold: they 54 vs me 109 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 4 | 0 |
| 16622198 | 6 | 5 | 1 |
| 16622349 | 11 | 27 | 0 |
| 16633100 | 3 | 1 | 0 |
| 16637255 | 14 | 7 | 2 |
| 16640467 | 6 | 8 | 0 |
| 16640510 | 3 | 6 | 0 |
| 16644724 | 0 | 0 | 2 |
| 16675778 | 0 | 4 | 0 |
| 16690867 | 2 | 2 | 0 |
| 16718819 | 0 | 2 | 0 |
| 16719123 | 8 | 10 | 0 |
| 16725899 | 5 | 3 | 0 |
| 16730612 | 3 | 5 | 0 |
| 16730761 | 8 | 6 | 2 |
| 16732403 | 7 | 10 | 0 |
| 16732521 | 3 | 11 | 1 |
| 16732748 | 3 | 2 | 0 |
| 16758882 | 5 | 7 | 0 |
| 16760569 | 4 | 5 | 0 |
| 16773026 | 7 | 5 | 0 |
| 16777134 | 3 | 3 | 0 |
| 16778640 | 2 | 0 | 0 |
| 16781445 | 1 | 1 | 0 |
| 16805699 | 8 | 8 | 0 |
| 16811307 | 8 | 0 | 1 |
| 16833141 | 10 | 0 | 0 |
| 16845367 | 12 | 1 | 0 |
| 16858228 | 2 | 1 | 0 |

## Episodes behind each window

- **F** (1): 89061335
- **C0** (50): 108908450, 108909458, 108910563, 108911501, 108912504, 108913510, 108914540, 108915557, 108916582, 108917616, 108918628, 108919657, 108920675, 108921703, 108922696, 108922746, 108923792, 108924823, 108925660, 108925937, 108926974, 108928041, 108929079, 108930142, 108931203, 108932268, 108933314, 108933709, 108934341, 108934575, 108935405, 108936457, 108937489, 108938524, 108939573, 108940618, 108941666, 108942700, 108943735, 108944824, 108945959, 108946868, 108947912, 108948960, 108949771, 108951147, 108952634, 108953569, 108954232, 108955246
