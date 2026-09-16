# matcha110 (rank 602, score 2586.0, bronze)

- team id 16802867; current submission 56225054 (171 public games)
- 7 submissions found; 1147 public games from 2026-09-08 to 2026-09-15; 1 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 46-3-1 | 92 | 109357 | 112457 | 2057.1 | 62 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 702, game 10: 1549, game 25: 2361, game 50: 2646, game 100: 2658, game last: 2607

![rating](figs/matcha110_rating.png)

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
| FERTILIZE ops | 96 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 133 |
| milk sold | 126.5 |
| wool sold | 108 |
| wheat sold | 314 |
| fertilizer sold | 291 |
| units sold last 3 days | 270 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/matcha110_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 3 (66%) | 12 (54%) | 31 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (66%) | 12 (54%) | 24 (20%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (66%) | 12 (54%) | 28 (16%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 31 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 24 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (100%), then branching (1 lines at turn 136, 28 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 3 | 33 | 66 |
| 300 | 12 | 12 | 27 | 54 |
| 400 | 16 | 31 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 0 |  | 34 |
| opponent off its modal line at turn 136 | 32 | 31.2 | 38.9 |
| played seat 1 | 19 | 26.3 | 38.7 |
| lost the game | 3 | 0 | 36.2 |
| first shop (day 3) is not Bakery | 43 | 34.9 | 28.6 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 92 | 109357 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 126.5 | 108 | 31 | 24 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108844194 | Jun_value | 2032.5 | 82716 | 84010 | -1294 | 9b0c82fd | milk sold: they 100 vs me 120; strawberry sold: they 124 vs me 132; units sold last 3 days: they 265 vs me 268 |
| C0 | 108854232 | york1to | 2504.4 | 129917 | 130234 | -317 | 9b0c82fd | wool sold: they 110 vs me 56; FERTILIZE ops: they 104 vs me 120; CARE ops: they 406 vs me 417 |
| C0 | 108867629 | Hanserong | 2607.1 | 122952 | 125938 | -2986 | 9b0c82fd | FERTILIZE ops: they 84 vs me 120; milk sold: they 182 vs me 155; wool sold: they 90 vs me 76 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622459 | 0 | 1 | 0 |
| 16626191 | 0 | 1 | 0 |
| 16633100 | 2 | 0 | 0 |
| 16633944 | 1 | 1 | 1 |
| 16637255 | 1 | 0 | 0 |
| 16640510 | 0 | 1 | 0 |
| 16644724 | 0 | 1 | 0 |
| 16655383 | 0 | 1 | 0 |
| 16660726 | 1 | 0 | 0 |
| 16671741 | 0 | 1 | 0 |
| 16675778 | 1 | 0 | 0 |
| 16684093 | 2 | 2 | 0 |
| 16723379 | 0 | 1 | 0 |
| 16730720 | 0 | 0 | 1 |
| 16731186 | 0 | 1 | 0 |
| 16732748 | 0 | 2 | 0 |
| 16741542 | 0 | 1 | 0 |
| 16758882 | 0 | 1 | 0 |
| 16765807 | 0 | 0 | 1 |
| 16773026 | 0 | 1 | 0 |
| 16809332 | 0 | 1 | 0 |
| 16811307 | 0 | 1 | 0 |
| 16848479 | 0 | 1 | 0 |
| 16888254 | 0 | 1 | 1 |

## Episodes behind each window

- **C0** (50): 108830623, 108831636, 108832027, 108832639, 108833652, 108834665, 108835698, 108836705, 108837731, 108838797, 108839766, 108840783, 108841797, 108842812, 108843835, 108844194, 108844884, 108845938, 108846333, 108846978, 108847290, 108848072, 108848436, 108848802, 108849138, 108850181, 108851202, 108852240, 108853266, 108854232, 108855346, 108856423, 108857432, 108858500, 108859505, 108860397, 108861340, 108861763, 108862394, 108863418, 108863428, 108864483, 108865524, 108866581, 108867629, 108867882, 108868673, 108869725, 108870147, 108870769
