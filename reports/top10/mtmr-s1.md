# mtmr_s1 (rank 30, score 2912.3, next-15)

- team id 16758882; current submission 56232460 (113 public games)
- 31 submissions found; 5969 public games from 2026-08-22 to 2026-09-15; 38 of them with a known rating
- sampled games with a replay: 60

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| Q3 | 10 | 2-8-0 | 20 | 104898 | 96423.2 | 2953.9 | 60 | 1.32.7 | 2026-09-10 | 2026-09-10 |
| C0 | 50 | 47-3-0 | 94 | 101994.5 | 104403.5 | 2156.9 | 46 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 695, game 10: 1474, game 25: 2485, game 50: 2839, game 100: 2896, game last: 2921

![rating](figs/mtmr-s1_rating.png)

## Farm plan by window (median per game)

| median per game | Q3 | C0 |
|---|---|---|
| hands (peak) | 11 | 12 |
| quadrants | 3 | 3 |
| land day 1 | 6 | 6 |
| land day 2 | 11 | 11 |
| cows bought | 8 | 8 |
| sheep bought | 6 | 6 |
| geese bought | 3 | 3 |
| first cow day | 0 | 0 |
| wheat planted | 163 | 148.5 |
| carrot planted | 31 | 50 |
| tomato planted | 0 | 0 |
| strawberry planted | 33 | 33 |
| melon planted | 12 | 12 |
| FERTILIZE ops | 61 | 127.5 |
| CARE ops | 417 | 398 |
| melon sold | 12 | 12 |
| strawberry sold | 166 | 153 |
| milk sold | 169 | 111.5 |
| wool sold | 106.5 | 76 |
| wheat sold | 262 | 407.5 |
| fertilizer sold | 289 | 259.5 |
| units sold last 3 days | 256.5 | 257 |
| shed peak | 61 | 61 |
| weeds spawned | 20 | 21 |
| unexecutable market orders | 45 | 45 |

![money by day](figs/mtmr-s1_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| Q3 | 10 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 2 (90%) | 2 (90%) |
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 9 (52%) | 27 (20%) | 50 (2%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| Q3 | 10 | 1 (100%) | 1 (100%) | 2 (80%) | 2 (80%) | 2 (80%) | 2 (80%) | 10 (10%) | 10 (10%) |
| C0 | 50 | 1 (100%) | 2 (98%) | 3 (62%) | 3 (62%) | 15 (34%) | 39 (8%) | 48 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| Q3 | 10 | 1 (100%) | 1 (100%) | 2 (80%) | 2 (80%) | 2 (80%) | 2 (80%) | 10 (10%) | 10 (10%) |
| C0 | 50 | 1 (100%) | 2 (98%) | 3 (62%) | 3 (62%) | 15 (32%) | 40 (8%) | 49 (4%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 50 at turn 400); every game distinct by turn 400**; market is **one line through turn 48 (98%), then branching (3 lines at turn 136, 48 at turn 400); every game distinct by turn 719**; plan is **one line through turn 48 (98%), then branching (3 lines at turn 136, 49 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 9 | 26 | 52 |
| 300 | 12 | 27 | 10 | 20 |
| 400 | 16 | 50 | 1 | 2 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 3 | 100 | 44.7 |
| opponent off its modal line at turn 136 | 14 | 64.3 | 41.7 |
| played seat 1 | 27 | 59.3 | 34.8 |
| lost the game | 3 | 0 | 51.1 |
| first shop (day 3) is not Farmers Market | 38 | 52.6 | 33.3 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q3 | 10 | 20 | 104898 | 11 | 8 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 169 | 106.5 | 2 | 10 |
| C0 | 50 | 94 | 101994.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 148.5 | 12 | 12 | 111.5 | 76 | 50 | 48 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108949791 | r13721 | 2423.1 | 85583 | 85948 | -365 | 9b0c82fd | CARE ops: they 417 vs me 389; FERTILIZE ops: they 99 vs me 125; wheat planted: they 163 vs me 142 |
| C0 | 108951833 | Satoshi_SsSs | 2589.1 | 90062 | 90603 | -541 | 9b0c82fd | strawberry sold: they 129 vs me 152; wheat planted: they 163 vs me 142; FERTILIZE ops: they 110 vs me 128 |
| C0 | 108971130 | Syed Asad Ali | 2851.2 | 85279 | 111712 | -26433 | 9b0c82fd | milk sold: they 146 vs me 51; wool sold: they 101 vs me 27; strawberry sold: they 162 vs me 90 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 1 | 0 |
| 16622198 | 3 | 3 | 1 |
| 16622349 | 7 | 8 | 0 |
| 16633100 | 2 | 0 | 0 |
| 16637255 | 5 | 1 | 0 |
| 16640467 | 1 | 0 | 0 |
| 16640510 | 10 | 13 | 0 |
| 16644724 | 7 | 5 | 0 |
| 16675778 | 1 | 2 | 0 |
| 16690867 | 1 | 0 | 0 |
| 16718819 | 0 | 4 | 0 |
| 16719123 | 3 | 5 | 0 |
| 16725899 | 4 | 1 | 0 |
| 16730612 | 2 | 10 | 0 |
| 16730761 | 8 | 5 | 0 |
| 16732403 | 1 | 8 | 1 |
| 16732521 | 6 | 10 | 0 |
| 16732748 | 2 | 5 | 0 |
| 16760569 | 3 | 3 | 0 |
| 16773026 | 4 | 1 | 0 |
| 16777134 | 4 | 3 | 0 |
| 16778640 | 1 | 0 | 0 |
| 16781445 | 0 | 2 | 0 |
| 16805699 | 5 | 12 | 0 |
| 16811307 | 3 | 1 | 0 |
| 16833141 | 3 | 3 | 0 |
| 16845367 | 1 | 3 | 0 |
| 16858228 | 3 | 0 | 0 |

## Episodes behind each window

- **Q3** (10): 107448458, 107448662, 107451645, 107468198, 107473909, 107479702, 107484742, 107486520, 107487540, 107493480
- **C0** (50): 108929087, 108930107, 108931133, 108932151, 108933191, 108934238, 108935242, 108936281, 108937294, 108938314, 108939345, 108940371, 108941395, 108942418, 108943448, 108944472, 108945496, 108946561, 108947622, 108948683, 108949791, 108950207, 108950798, 108951833, 108952945, 108954007, 108955055, 108956052, 108957111, 108958203, 108959260, 108960454, 108961335, 108962671, 108962450, 108962993, 108963650, 108964720, 108965658, 108965812, 108966580, 108967622, 108968029, 108968671, 108969765, 108971130, 108971809, 108972829, 108973939, 108974921
