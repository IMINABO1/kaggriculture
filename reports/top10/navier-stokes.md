# Navier-stokes (rank 120, score 2820.3, silver)

- team id 16891058; current submission 56248784 (94 public games)
- 5 submissions found; 472 public games from 2026-09-14 to 2026-09-15; 0 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 103187 | 104025.4 | 2180.9 | 48 | 1.32.7 | 2026-09-15 | 2026-09-15 |

## Rating path of the current submission

game 1: 744, game 10: 1562, game 25: 2566, game 50: 2801, game last: 2823

![rating](figs/navier-stokes_rating.png)

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
| FERTILIZE ops | 117 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 129 |
| milk sold | 107.5 |
| wool sold | 63.5 |
| wheat sold | 345 |
| fertilizer sold | 287 |
| units sold last 3 days | 266.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/navier-stokes_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 7 (44%) | 15 (32%) | 37 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 10 (44%) | 20 (20%) | 33 (12%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 10 (44%) | 20 (20%) | 38 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 37 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 33 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (100%), then branching (1 lines at turn 136, 38 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 7 | 22 | 44 |
| 300 | 12 | 15 | 16 | 32 |
| 400 | 16 | 37 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 0 |  | 56 |
| opponent off its modal line at turn 136 | 22 | 50 | 60.7 |
| played seat 1 | 26 | 61.5 | 50 |
| lost the game | 5 | 60 | 55.6 |
| first shop (day 3) is not Farmers Market | 40 | 50 | 80 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 103187 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 107.5 | 63.5 | 37 | 33 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109241128 | KouFu | 2732.6 | 111931 | 112868 | -937 | 9b0c82fd | milk sold: they 137 vs me 128; units sold last 3 days: they 278 vs me 269; strawberry sold: they 126 vs me 131 |
| C0 | 109241991 | weichy7 | 2817.3 | 76165 | 77038 | -873 | 9b0c82fd | strawberry sold: they 129 vs me 97; FERTILIZE ops: they 117 vs me 100; wool sold: they 212 vs me 196 |
| C0 | 109245165 | Rasmus Hulthe | 2803.8 | 116335 | 120968 | -4633 | 9b0c82fd | strawberry sold: they 143 vs me 125; wool sold: they 153 vs me 136; milk sold: they 110 vs me 125 |
| C0 | 109249942 | Erfan Eshratifar | 2774.7 | 90824 | 91311 | -487 | 3bc18d7a | milk sold: they 116 vs me 73; wool sold: they 72 vs me 50; wheat planted: they 148 vs me 162 |
| C0 | 109250505 | Keisuke | 2863.6 | 132952 | 134435 | -1483 | 5738b34d | wool sold: they 42 vs me 26; units sold last 3 days: they 268 vs me 257; milk sold: they 152 vs me 149 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622198 | 1 | 2 | 0 |
| 16622459 | 1 | 0 | 0 |
| 16633100 | 0 | 1 | 0 |
| 16633178 | 0 | 1 | 0 |
| 16637255 | 0 | 1 | 0 |
| 16683936 | 1 | 0 | 0 |
| 16728071 | 0 | 1 | 0 |
| 16730761 | 1 | 0 | 0 |
| 16731186 | 0 | 1 | 0 |
| 16731275 | 0 | 1 | 0 |
| 16732521 | 0 | 1 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16833141 | 0 | 1 | 0 |
| 16858228 | 0 | 1 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16880773 | 0 | 1 | 0 |
| 16888254 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 109208388, 109209389, 109210464, 109211497, 109212517, 109213554, 109214592, 109215627, 109216671, 109217718, 109218762, 109218941, 109219790, 109220828, 109221870, 109222902, 109222906, 109223986, 109224225, 109225118, 109226131, 109227206, 109228250, 109229320, 109230377, 109231426, 109232096, 109232476, 109233444, 109234595, 109235653, 109236747, 109237304, 109237762, 109238837, 109239882, 109241128, 109241991, 109243031, 109244107, 109244338, 109245151, 109245165, 109246203, 109247274, 109248321, 109249461, 109249942, 109250505, 109251569
