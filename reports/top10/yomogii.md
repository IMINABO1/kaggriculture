# yomogii (rank 39, score 2897.5, next-15)

- team id 16833141; current submission 56235642 (96 public games)
- 20 submissions found; 2690 public games from 2026-09-05 to 2026-09-15; 17 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 47-3-0 | 94 | 102744.5 | 105255.2 | 2134.5 | 54 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 685, game 10: 1520, game 25: 2489, game 50: 2805, game last: 2901

![rating](figs/yomogii_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 12 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 11 |
| cows bought | 6.5 |
| sheep bought | 6 |
| geese bought | 3 |
| first cow day | 0 |
| wheat planted | 163 |
| carrot planted | 31 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 108 |
| CARE ops | 403 |
| melon sold | 12 |
| strawberry sold | 129 |
| milk sold | 95.5 |
| wool sold | 74.5 |
| wheat sold | 358 |
| fertilizer sold | 287 |
| units sold last 3 days | 266 |
| shed peak | 58 |
| weeds spawned | 20 |
| unexecutable market orders | 1 |

![money by day](figs/yomogii_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (76%) | 2 (76%) | 2 (76%) | 16 (32%) | 26 (18%) | 41 (10%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (76%) | 2 (76%) | 2 (76%) | 2 (76%) | 20 (32%) | 31 (12%) | 45 (6%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (76%) | 2 (76%) | 2 (76%) | 2 (76%) | 21 (32%) | 31 (12%) | 43 (10%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 24 (100%), then branching (2 lines at turn 136, 41 at turn 400); every game distinct by turn 719**; market is **reactive from day 1: 2 openings at turn 24 (largest 76%), 2 lines at turn 100; every game distinct by turn 719**; plan is **reactive from day 1: 2 openings at turn 24 (largest 76%), 2 lines at turn 100; every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 38 | 76 |
| 100 | 4 | 2 | 38 | 76 |
| 136 | 5 | 2 | 38 | 76 |
| 200 | 8 | 16 | 16 | 32 |
| 300 | 12 | 26 | 9 | 18 |
| 400 | 16 | 41 | 5 | 10 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 48 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 2 | 0 |  | 24 |
| opponent off its modal line at turn 24 | 18 | 11.1 | 31.2 |
| played seat 1 | 23 | 21.7 | 25.9 |
| lost the game | 3 | 0 | 25.5 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 94 | 102744.5 | 12 | 6.5 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 95.5 | 74.5 | 41 | 45 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109009851 | 自己找差距 | 2805.1 | 119515 | 131802 | -12287 | 3bc18d7a | strawberry sold: they 324 vs me 133; CARE ops: they 272 vs me 403; FERTILIZE ops: they 202 vs me 102 |
| C0 | 109012954 | Lucien de Rubempre | 2787.0 | 105533 | 114643 | -9110 | 9b0c82fd | strawberry sold: they 131 vs me 344; CARE ops: they 405 vs me 266; units sold last 3 days: they 268 vs me 149 |
| C0 | 109015027 | honjousetuna | 2731.1 | 102788 | 106652 | -3864 | 9b0c82fd | CARE ops: they 506 vs me 396; FERTILIZE ops: they 61 vs me 103; units sold last 3 days: they 250 vs me 275 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622198 | 2 | 2 | 0 |
| 16633100 | 1 | 0 | 0 |
| 16637255 | 3 | 5 | 0 |
| 16640467 | 0 | 2 | 0 |
| 16640510 | 1 | 1 | 0 |
| 16644724 | 0 | 10 | 0 |
| 16675778 | 3 | 3 | 0 |
| 16718819 | 0 | 3 | 0 |
| 16719123 | 2 | 2 | 0 |
| 16725899 | 0 | 3 | 0 |
| 16730612 | 0 | 3 | 0 |
| 16730761 | 2 | 3 | 0 |
| 16732403 | 1 | 0 | 0 |
| 16732521 | 1 | 2 | 0 |
| 16758882 | 3 | 3 | 0 |
| 16773026 | 0 | 8 | 0 |
| 16777134 | 5 | 4 | 0 |
| 16778640 | 3 | 1 | 0 |
| 16805699 | 0 | 3 | 0 |
| 16811307 | 0 | 2 | 0 |
| 16845367 | 3 | 4 | 0 |
| 16858228 | 1 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108974647, 108975697, 108976683, 108977717, 108978734, 108979750, 108980762, 108981795, 108982799, 108983838, 108984854, 108985887, 108986915, 108987948, 108988985, 108990016, 108990158, 108991055, 108991626, 108992115, 108992138, 108993174, 108993684, 108994222, 108995287, 108996323, 108997339, 108997362, 108998403, 108999451, 109000477, 109001536, 109002561, 109003593, 109004631, 109005673, 109006711, 109007758, 109008804, 109009851, 109010991, 109011920, 109012954, 109013990, 109015027, 109016054, 109016617, 109017095, 109018140, 109019223
