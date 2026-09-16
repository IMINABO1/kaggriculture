# Bldr2 (rank 250, score 2734.8, silver)

- team id 16879253; current submission 56228838 (185 public games)
- 9 submissions found; 1194 public games from 2026-09-12 to 2026-09-15; 4 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 95980 | 99705.9 | 2169.0 | 52 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 680, game 10: 1643, game 25: 2513, game 50: 2741, game 100: 2804, game last: 2738

![rating](figs/bldr2_rating.png)

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
| wheat planted | 163 |
| carrot planted | 31 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 118 |
| CARE ops | 405 |
| melon sold | 72 |
| strawberry sold | 248 |
| milk sold | 195.5 |
| wool sold | 107 |
| wheat sold | 397.5 |
| fertilizer sold | 342 |
| units sold last 3 days | 393 |
| shed peak | 45 |
| weeds spawned | 20 |
| unexecutable market orders | 1 |

![money by day](figs/bldr2_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 3 (96%) | 3 (96%) | 3 (96%) | 10 (56%) | 16 (36%) | 39 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 9 (60%) | 16 (36%) | 30 (12%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (96%) | 2 (96%) | 2 (96%) | 13 (56%) | 17 (36%) | 38 (12%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 39 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 30 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (96%), then branching (2 lines at turn 136, 38 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 3 | 48 | 96 |
| 100 | 4 | 3 | 48 | 96 |
| 136 | 5 | 3 | 48 | 96 |
| 200 | 8 | 10 | 28 | 56 |
| 300 | 12 | 16 | 18 | 36 |
| 400 | 16 | 39 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 39.1 |
| opponent off its modal line at turn 136 | 22 | 54.5 | 35.7 |
| played seat 1 | 24 | 33.3 | 53.8 |
| lost the game | 5 | 80 | 40 |
| first shop (day 3) is not Pet Cafe | 40 | 37.5 | 70 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 95980 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 72 | 195.5 | 107 | 39 | 30 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108896325 | Hiro Nomo | 2439.0 | 78845 | 83608 | -4763 | 9b0c82fd | wheat planted: they 143 vs me 163; FERTILIZE ops: they 132 vs me 121; CARE ops: they 415 vs me 405 |
| C0 | 108903984 | parv goyal2 | 2571.5 | 85343 | 93967 | -8624 | 88cd11eb | CARE ops: they 312 vs me 405; strawberry sold: they 166 vs me 241; wheat planted: they 232 vs me 163 |
| C0 | 108907547 | Chris Deotte | 2657.1 | 126581 | 126940 | -359 | 9b0c82fd | milk sold: they 143 vs me 152; strawberry sold: they 244 vs me 239; units sold last 3 days: they 395 vs me 393 |
| C0 | 108908602 | Xiaoyong Zhu | 2776.8 | 118566 | 119256 | -690 | 8008c86c | units sold last 3 days: they 400 vs me 398; weeds spawned: they 20 vs me 21; CARE ops: they 404 vs me 405 |
| C0 | 108913789 | 自己找差距 | 2706.1 | 90793 | 96316 | -5523 | 3bc18d7a | CARE ops: they 259 vs me 405; FERTILIZE ops: they 205 vs me 92; wheat planted: they 80 vs me 156 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622459 | 0 | 4 | 0 |
| 16626191 | 0 | 0 | 1 |
| 16633178 | 1 | 0 | 0 |
| 16633944 | 1 | 0 | 0 |
| 16637255 | 0 | 2 | 0 |
| 16640467 | 0 | 2 | 0 |
| 16640510 | 0 | 1 | 0 |
| 16641710 | 0 | 1 | 0 |
| 16657100 | 1 | 0 | 1 |
| 16658554 | 1 | 1 | 0 |
| 16660726 | 0 | 1 | 0 |
| 16675778 | 0 | 1 | 0 |
| 16706321 | 1 | 1 | 0 |
| 16719123 | 0 | 1 | 0 |
| 16723379 | 2 | 0 | 0 |
| 16728071 | 0 | 1 | 0 |
| 16730524 | 0 | 2 | 0 |
| 16730761 | 1 | 3 | 0 |
| 16731186 | 1 | 0 | 0 |
| 16731275 | 1 | 2 | 0 |
| 16732521 | 0 | 2 | 0 |
| 16732748 | 0 | 1 | 0 |
| 16758882 | 0 | 1 | 0 |
| 16760569 | 0 | 1 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16773026 | 1 | 1 | 0 |
| 16777134 | 0 | 1 | 0 |
| 16778640 | 2 | 0 | 0 |
| 16781445 | 2 | 1 | 0 |
| 16805699 | 0 | 1 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16810299 | 0 | 1 | 0 |
| 16811307 | 0 | 1 | 0 |
| 16845367 | 1 | 1 | 0 |
| 16848479 | 0 | 2 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 2 | 0 | 0 |
| 16880773 | 1 | 2 | 0 |
| 16888254 | 2 | 1 | 0 |
| 16891058 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108877746, 108878761, 108879783, 108880775, 108881800, 108882814, 108883841, 108884836, 108885855, 108886874, 108887893, 108888922, 108889959, 108890717, 108891564, 108891767, 108892521, 108892833, 108893900, 108894953, 108895660, 108896018, 108896325, 108897071, 108898154, 108899169, 108900222, 108901265, 108902316, 108903357, 108903984, 108904410, 108905458, 108906427, 108906490, 108907103, 108907547, 108908602, 108909664, 108910699, 108911734, 108911994, 108912767, 108913789, 108913799, 108914865, 108915905, 108916959, 108918009, 108919037
