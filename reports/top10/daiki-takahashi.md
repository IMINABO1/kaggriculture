# Daiki Takahashi (rank 750, score 2526.6, bronze)

- team id 16761744; current submission 56228647 (206 public games)
- 7 submissions found; 1159 public games from 2026-08-30 to 2026-09-15; 1 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 36-9-5 | 72 | 99677 | 110630.2 | 2113.7 | 48 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 706, game 10: 1567, game 25: 2467, game 50: 2615, game 100: 2660, game 200: 2506, game last: 2484

![rating](figs/daiki-takahashi_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 12 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 11 |
| cows bought | 8 |
| sheep bought | 6 |
| geese bought | 3 |
| first cow day | 0 |
| wheat planted | 162 |
| carrot planted | 31 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 103 |
| CARE ops | 417 |
| melon sold | 72 |
| strawberry sold | 248 |
| milk sold | 211 |
| wool sold | 139 |
| wheat sold | 369.5 |
| fertilizer sold | 352 |
| units sold last 3 days | 396 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/daiki-takahashi_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 5 (70%) | 12 (44%) | 32 (12%) | 49 (4%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 6 (70%) | 14 (44%) | 30 (18%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 6 (70%) | 14 (44%) | 33 (12%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 32 at turn 400)**; market is **one line through turn 136 (98%), then branching (2 lines at turn 136, 30 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 33 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 49 | 98 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 5 | 35 | 70 |
| 300 | 12 | 12 | 22 | 44 |
| 400 | 16 | 32 | 6 | 12 |
| 719 | 29 | 49 | 2 | 4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 0 |  | 30 |
| opponent off its modal line at turn 136 | 27 | 33.3 | 26.1 |
| played seat 1 | 26 | 34.6 | 25 |
| lost the game | 9 | 11.1 | 34.1 |
| first shop (day 3) is not Pizza Shop | 37 | 35.1 | 15.4 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 72 | 99677 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 72 | 211 | 139 | 32 | 30 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108898023 | Max64738CB | 2491.7 | 96292 | 99618 | -3326 | 9b0c82fd | units sold last 3 days: they 369 vs me 401; milk sold: they 245 vs me 216; wool sold: they 158 vs me 133 |
| C0 | 108900260 | magic101 | 2459.5 | 95523 | 95607 | -84 | 9b0c82fd | strawberry sold: they 248 vs me 249 |
| C0 | 108904783 | Maximo Uribarri | 2664.0 | 130106 | 131305 | -1199 | 9b0c82fd | CARE ops: they 348 vs me 417; wool sold: they 68 vs me 99; units sold last 3 days: they 432 vs me 411 |
| C0 | 108905785 | KoRo2_JP | 2673.9 | 96543 | 96549 | -6 | 9b0c82fd |  |
| C0 | 108907530 | yy | 2679.6 | 60319 | 62085 | -1766 | 9b0c82fd | CARE ops: they 405 vs me 417; units sold last 3 days: they 396 vs me 407; FERTILIZE ops: they 117 vs me 113 |
| C0 | 108908582 | 最强扫地僧 | 2597.0 | 98059 | 99325 | -1266 | 9b0c82fd | milk sold: they 266 vs me 239; FERTILIZE ops: they 102 vs me 113; units sold last 3 days: they 402 vs me 396 |
| C0 | 108910746 | Neural Knight | 2575.7 | 58925 | 59059 | -134 | 9b0c82fd | CARE ops: they 486 vs me 417; FERTILIZE ops: they 112 vs me 118; strawberry sold: they 244 vs me 247 |
| C0 | 108914821 | lumen | 2617.5 | 97991 | 99372 | -1381 | 9b0c82fd | milk sold: they 109 vs me 153; units sold last 3 days: they 372 vs me 405; CARE ops: they 385 vs me 401 |
| C0 | 108916912 | Baiqing Wang | 2603.8 | 78288 | 78297 | -9 | 9b0c82fd |  |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16644724 | 0 | 4 | 0 |
| 16657100 | 2 | 0 | 0 |
| 16660726 | 0 | 1 | 0 |
| 16684093 | 1 | 1 | 0 |
| 16706321 | 0 | 2 | 0 |
| 16728071 | 0 | 1 | 0 |
| 16732748 | 0 | 1 | 0 |
| 16760569 | 1 | 0 | 0 |
| 16765807 | 0 | 1 | 0 |
| 16809332 | 0 | 1 | 0 |
| 16811307 | 0 | 1 | 0 |
| 16858228 | 2 | 0 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16880773 | 0 | 4 | 0 |
| 16888254 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108875692, 108876702, 108877721, 108878730, 108879757, 108880770, 108881801, 108882805, 108883836, 108884827, 108885842, 108886867, 108887891, 108888927, 108889956, 108890716, 108891764, 108892831, 108893847, 108894949, 108895973, 108897017, 108898023, 108899134, 108899924, 108900194, 108900260, 108901242, 108902292, 108903006, 108903349, 108904394, 108904783, 108905434, 108905785, 108906486, 108907530, 108907548, 108908582, 108909621, 108910648, 108910746, 108911712, 108912736, 108913116, 108913775, 108914821, 108915877, 108916912, 108917962
