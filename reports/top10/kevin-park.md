# kevin park (rank 252, score 2732.3, silver)

- team id 16626191; current submission 56251510 (86 public games)
- 86 submissions found; 9799 public games from 2026-07-31 to 2026-09-15; 759 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 102818 | 105209.2 | 2094.1 | 36 | 1.32.7 | 2026-09-15 | 2026-09-15 |

## Rating path of the current submission

game 1: 698, game 10: 1512, game 25: 2448, game 50: 2693, game last: 2738

![rating](figs/kevin-park_rating.png)

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
| FERTILIZE ops | 116 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 129 |
| milk sold | 111 |
| wool sold | 77 |
| wheat sold | 342 |
| fertilizer sold | 287 |
| units sold last 3 days | 269 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/kevin-park_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 12 (34%) | 21 (18%) | 39 (8%) | 48 (6%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 11 (38%) | 19 (20%) | 35 (8%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 15 (34%) | 23 (18%) | 39 (8%) | 48 (6%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 39 at turn 400)**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 35 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (100%), then branching (1 lines at turn 136, 39 at turn 400)**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 12 | 17 | 34 |
| 300 | 12 | 21 | 9 | 18 |
| 400 | 16 | 39 | 4 | 8 |
| 719 | 29 | 48 | 3 | 6 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 6 | 100 | 61.4 |
| opponent off its modal line at turn 136 | 18 | 77.8 | 59.4 |
| played seat 1 | 32 | 68.8 | 61.1 |
| lost the game | 5 | 60 | 66.7 |
| first shop (day 3) is not Bakery | 39 | 61.5 | 81.8 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 102818 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 111 | 77 | 39 | 35 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109262730 | morality0707 | 2389.7 | 94968 | 105442 | -10474 | 791b6988 | wool sold: they 229 vs me 136; melon sold: they 72 vs me 12; milk sold: they 132 vs me 80 |
| C0 | 109273411 | The Grower | 2592.3 | 152476 | 152604 | -128 | 9b0c82fd |  |
| C0 | 109281477 | Igor V | 2581.9 | 70774 | 71471 | -697 | 9b0c82fd | units sold last 3 days: they 258 vs me 266; FERTILIZE ops: they 117 vs me 124; milk sold: they 111 vs me 117 |
| C0 | 109282952 | Igor V | 2679.9 | 113344 | 114027 | -683 | 9b0c82fd | wool sold: they 72 vs me 80; strawberry sold: they 120 vs me 125; milk sold: they 86 vs me 81 |
| C0 | 109285070 | yy | 2640.7 | 143771 | 143772 | -1 | 9b0c82fd | wheat planted: they 163 vs me 162; weeds spawned: they 20 vs me 19 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 1 | 0 |
| 16622198 | 5 | 3 | 0 |
| 16622349 | 9 | 5 | 0 |
| 16622459 | 1 | 3 | 0 |
| 16633100 | 4 | 3 | 0 |
| 16633178 | 1 | 0 | 0 |
| 16633944 | 9 | 4 | 0 |
| 16637255 | 4 | 6 | 0 |
| 16641710 | 2 | 2 | 0 |
| 16644724 | 8 | 13 | 3 |
| 16655383 | 5 | 0 | 0 |
| 16657100 | 3 | 2 | 1 |
| 16658554 | 0 | 1 | 0 |
| 16660726 | 4 | 0 | 0 |
| 16664246 | 1 | 0 | 0 |
| 16671741 | 3 | 1 | 0 |
| 16675778 | 2 | 0 | 0 |
| 16683936 | 4 | 3 | 0 |
| 16684093 | 4 | 3 | 0 |
| 16690867 | 4 | 0 | 0 |
| 16706321 | 0 | 1 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 0 | 5 | 0 |
| 16723379 | 1 | 1 | 0 |
| 16725899 | 4 | 3 | 1 |
| 16728071 | 2 | 7 | 0 |
| 16730524 | 0 | 2 | 0 |
| 16730612 | 0 | 1 | 0 |
| 16730761 | 1 | 1 | 0 |
| 16731186 | 3 | 4 | 0 |
| 16731275 | 0 | 2 | 0 |
| 16732521 | 1 | 8 | 0 |
| 16732748 | 3 | 6 | 0 |
| 16741542 | 3 | 0 | 0 |
| 16758882 | 0 | 3 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 1 | 2 | 0 |
| 16777134 | 2 | 2 | 0 |
| 16781445 | 0 | 2 | 1 |
| 16802867 | 1 | 0 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16810299 | 1 | 0 | 0 |
| 16811307 | 0 | 1 | 0 |
| 16833141 | 2 | 2 | 0 |
| 16848479 | 0 | 1 | 0 |
| 16848532 | 0 | 2 | 0 |
| 16879253 | 0 | 0 | 1 |
| 16882725 | 0 | 1 | 0 |
| 16888254 | 0 | 0 | 1 |

## Episodes behind each window

- **C0** (50): 109244981, 109245996, 109247063, 109248111, 109249208, 109250246, 109251268, 109252309, 109253329, 109254376, 109255390, 109256431, 109257455, 109258486, 109259529, 109259960, 109260311, 109260602, 109261650, 109262730, 109262815, 109263783, 109264899, 109264834, 109265931, 109267004, 109268042, 109269192, 109270255, 109271289, 109271956, 109272343, 109272870, 109273411, 109274465, 109274619, 109275518, 109276582, 109277627, 109278693, 109279757, 109280968, 109281477, 109281895, 109282892, 109282952, 109284013, 109285070, 109286213, 109287269
