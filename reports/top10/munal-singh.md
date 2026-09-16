# Munal Singh (rank 122, score 2820.0, silver)

- team id 16622459; current submission 56222671 (207 public games)
- 39 submissions found; 5976 public games from 2026-08-26 to 2026-09-15; 69 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 42-8-0 | 84 | 96852.5 | 105138.5 | 2259.4 | 42 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 701, game 10: 1561, game 25: 2695, game 50: 2880, game 100: 2885, game 200: 2817, game last: 2800

![rating](figs/munal-singh_rating.png)

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
| FERTILIZE ops | 110 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 128 |
| milk sold | 107 |
| wool sold | 75.5 |
| wheat sold | 336 |
| fertilizer sold | 283 |
| units sold last 3 days | 268.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/munal-singh_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 4 (94%) | 4 (94%) | 4 (94%) | 15 (34%) | 22 (18%) | 39 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 3 (96%) | 5 (82%) | 5 (82%) | 14 (36%) | 23 (20%) | 40 (8%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 4 (94%) | 5 (82%) | 5 (82%) | 18 (30%) | 25 (18%) | 42 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (94%), then branching (4 lines at turn 136, 39 at turn 400); every game distinct by turn 719**; market is **one line through turn 48 (96%), then branching (5 lines at turn 136, 40 at turn 400); every game distinct by turn 719**; plan is **one line through turn 48 (94%), then branching (5 lines at turn 136, 42 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 48 | 96 |
| 48 | 2 | 4 | 47 | 94 |
| 100 | 4 | 4 | 47 | 94 |
| 136 | 5 | 4 | 47 | 94 |
| 200 | 8 | 15 | 17 | 34 |
| 300 | 12 | 22 | 9 | 18 |
| 400 | 16 | 39 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 6 | 100 | 61.4 |
| opponent off its modal line at turn 136 | 26 | 61.5 | 70.8 |
| played seat 1 | 29 | 62.1 | 71.4 |
| lost the game | 8 | 100 | 59.5 |
| first shop (day 3) is not Ice Cream Shop | 40 | 77.5 | 20 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 84 | 96852.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 107 | 75.5 | 39 | 40 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108834849 | Knight of Favonius | 2889.1 | 96769 | 98820 | -2051 | 9b0c82fd | strawberry sold: they 99 vs me 132; wool sold: they 140 vs me 150; milk sold: they 103 vs me 106 |
| C0 | 108836912 | THIRD FARM CLUB | 2896.0 | 74713 | 91149 | -16436 | 7cb9b079 | CARE ops: they 279 vs me 398; FERTILIZE ops: they 201 vs me 94; wool sold: they 209 vs me 112 |
| C0 | 108838388 | morality0707 | 2892.9 | 59749 | 59998 | -249 | 791b6988 | CARE ops: they 274 vs me 410; melon sold: they 59 vs me 12; strawberry sold: they 100 vs me 120 |
| C0 | 108840031 | Zhenghongshuang | 2944.6 | 61861 | 65544 | -3683 | 3bc18d7a | CARE ops: they 345 vs me 398; strawberry sold: they 139 vs me 118; wheat planted: they 157 vs me 165 |
| C0 | 108841311 | JezzLynn | 2931.5 | 72545 | 73146 | -601 | 9b0c82fd | wool sold: they 96 vs me 103; strawberry sold: they 126 vs me 129; weeds spawned: they 19 vs me 20 |
| C0 | 108845172 | Phoenix750 | 2888.8 | 77629 | 79009 | -1380 | 9b0c82fd | milk sold: they 141 vs me 123; strawberry sold: they 118 vs me 135; units sold last 3 days: they 257 vs me 273 |
| C0 | 108846218 | Unknown Mother-Goose | 2873.1 | 135599 | 143088 | -7489 | cfefcbaa | FERTILIZE ops: they 176 vs me 93; strawberry sold: they 175 vs me 102; wool sold: they 137 vs me 191 |
| C0 | 108846410 | Tom&Jerry | 2877.9 | 112112 | 112179 | -67 | 9b0c82fd | milk sold: they 87 vs me 98; units sold last 3 days: they 270 vs me 273 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 2 | 0 |
| 16622198 | 1 | 1 | 0 |
| 16622349 | 6 | 1 | 0 |
| 16626191 | 3 | 1 | 0 |
| 16633100 | 3 | 0 | 1 |
| 16633178 | 1 | 3 | 0 |
| 16633944 | 1 | 1 | 1 |
| 16637255 | 0 | 5 | 0 |
| 16640467 | 0 | 2 | 0 |
| 16640510 | 2 | 4 | 0 |
| 16641710 | 7 | 4 | 0 |
| 16644724 | 2 | 5 | 0 |
| 16655383 | 1 | 4 | 0 |
| 16657100 | 0 | 2 | 1 |
| 16658554 | 2 | 1 | 0 |
| 16660726 | 1 | 3 | 0 |
| 16664246 | 0 | 2 | 0 |
| 16671741 | 1 | 0 | 0 |
| 16675778 | 2 | 1 | 0 |
| 16683936 | 3 | 0 | 0 |
| 16684093 | 2 | 4 | 0 |
| 16690867 | 1 | 0 | 0 |
| 16706321 | 1 | 0 | 0 |
| 16719123 | 1 | 5 | 0 |
| 16723379 | 2 | 3 | 0 |
| 16725899 | 4 | 2 | 0 |
| 16728071 | 2 | 4 | 0 |
| 16730524 | 2 | 5 | 0 |
| 16730612 | 0 | 4 | 0 |
| 16730761 | 3 | 4 | 0 |
| 16731186 | 1 | 8 | 0 |
| 16731275 | 1 | 0 | 0 |
| 16732403 | 2 | 2 | 0 |
| 16732521 | 4 | 1 | 0 |
| 16732748 | 1 | 3 | 0 |
| 16741542 | 1 | 6 | 0 |
| 16758882 | 3 | 3 | 0 |
| 16760569 | 2 | 1 | 0 |
| 16773026 | 1 | 1 | 0 |
| 16777134 | 3 | 3 | 0 |
| 16778640 | 1 | 0 | 0 |
| 16781445 | 1 | 2 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 1 | 0 | 0 |
| 16809332 | 0 | 1 | 0 |
| 16810299 | 1 | 4 | 0 |
| 16811307 | 2 | 1 | 0 |
| 16833141 | 0 | 7 | 0 |
| 16845367 | 1 | 3 | 0 |
| 16848479 | 0 | 3 | 0 |
| 16879253 | 4 | 0 | 0 |
| 16880773 | 2 | 1 | 0 |
| 16882725 | 1 | 0 | 0 |
| 16891058 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108801910, 108802916, 108803897, 108804950, 108805961, 108806972, 108807989, 108807985, 108809006, 108810013, 108811040, 108812057, 108813078, 108814106, 108814961, 108815137, 108816138, 108817161, 108818229, 108819274, 108819426, 108820309, 108821367, 108822412, 108823464, 108824480, 108825539, 108826564, 108827593, 108828636, 108829676, 108830715, 108831741, 108832783, 108833818, 108834849, 108835885, 108836912, 108837946, 108838388, 108838916, 108840031, 108841054, 108841311, 108842086, 108843116, 108844149, 108845172, 108846218, 108846410
