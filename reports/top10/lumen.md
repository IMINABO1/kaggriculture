# lumen (rank 17, score 2961.9, gold)

- team id 16706321; current submission 56241997 (116 public games)
- 30 submissions found; 3030 public games from 2026-09-05 to 2026-09-15; 14 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 48-2-0 | 96 | 102415 | 105160.4 | 2202.6 | 54 | 1.32.7 | 2026-09-15 | 2026-09-15 |

## Rating path of the current submission

game 1: 675, game 10: 1572, game 25: 2626, game 50: 2924, game 100: 2956, game last: 2943

![rating](figs/lumen_rating.png)

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
| FERTILIZE ops | 116.5 |
| CARE ops | 382 |
| melon sold | 72 |
| strawberry sold | 250 |
| milk sold | 191 |
| wool sold | 126 |
| wheat sold | 426.5 |
| fertilizer sold | 346 |
| units sold last 3 days | 392.5 |
| shed peak | 58.5 |
| weeds spawned | 21 |
| unexecutable market orders | 45 |

![money by day](figs/lumen_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 3 (96%) | 3 (96%) | 14 (34%) | 28 (16%) | 46 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 6 (52%) | 6 (52%) | 6 (52%) | 6 (52%) | 29 (16%) | 42 (8%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 6 (52%) | 7 (50%) | 7 (50%) | 7 (50%) | 28 (20%) | 41 (6%) | 49 (4%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 46 at turn 400); every game distinct by turn 719**; market is **reactive from day 1: 6 openings at turn 24 (largest 52%), 6 lines at turn 100; every game distinct by turn 400**; plan is **reactive from day 1: 6 openings at turn 24 (largest 52%), 7 lines at turn 100; every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 3 | 48 | 96 |
| 136 | 5 | 3 | 48 | 96 |
| 200 | 8 | 14 | 17 | 34 |
| 300 | 12 | 28 | 8 | 16 |
| 400 | 16 | 46 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 6 | 100 | 61.4 |
| opponent off its modal line at turn 136 | 26 | 61.5 | 70.8 |
| played seat 1 | 23 | 60.9 | 70.4 |
| lost the game | 2 | 100 | 64.6 |
| first shop (day 3) is not Yarn Store | 42 | 59.5 | 100 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 96 | 102415 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 72 | 191 | 126 | 46 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109133627 | THUNDER THUNDER | 2739.7 | 92690 | 94256 | -1566 | 24a0cda8 | CARE ops: they 281 vs me 376; strawberry sold: they 186 vs me 249; units sold last 3 days: they 351 vs me 406 |
| C0 | 109151473 | Crop Dustas | 2897.1 | 81653 | 86317 | -4664 | 9b0c82fd | milk sold: they 245 vs me 196; units sold last 3 days: they 400 vs me 384; CARE ops: they 396 vs me 383 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 2 | 0 |
| 16622198 | 0 | 2 | 0 |
| 16622349 | 1 | 1 | 0 |
| 16622459 | 0 | 1 | 0 |
| 16626191 | 1 | 0 | 0 |
| 16633100 | 2 | 1 | 0 |
| 16633178 | 2 | 0 | 0 |
| 16633944 | 1 | 1 | 0 |
| 16637255 | 0 | 1 | 0 |
| 16640467 | 0 | 2 | 0 |
| 16640510 | 1 | 4 | 0 |
| 16641710 | 2 | 1 | 0 |
| 16644724 | 2 | 4 | 0 |
| 16655383 | 1 | 1 | 0 |
| 16658554 | 5 | 0 | 0 |
| 16660726 | 0 | 1 | 0 |
| 16664246 | 1 | 1 | 0 |
| 16671741 | 2 | 2 | 0 |
| 16675778 | 0 | 1 | 0 |
| 16683936 | 0 | 1 | 0 |
| 16684093 | 3 | 3 | 0 |
| 16690867 | 3 | 1 | 0 |
| 16719123 | 3 | 1 | 0 |
| 16725899 | 1 | 3 | 0 |
| 16728071 | 0 | 2 | 0 |
| 16730524 | 1 | 2 | 0 |
| 16730612 | 2 | 3 | 0 |
| 16730761 | 0 | 1 | 0 |
| 16731186 | 2 | 0 | 0 |
| 16731275 | 0 | 2 | 0 |
| 16732403 | 0 | 5 | 0 |
| 16732521 | 0 | 2 | 0 |
| 16732748 | 1 | 2 | 0 |
| 16758882 | 2 | 0 | 0 |
| 16760569 | 0 | 1 | 0 |
| 16761744 | 2 | 0 | 0 |
| 16765807 | 3 | 0 | 0 |
| 16773026 | 2 | 1 | 0 |
| 16777134 | 4 | 2 | 0 |
| 16778640 | 2 | 1 | 0 |
| 16781445 | 2 | 0 | 0 |
| 16805699 | 1 | 2 | 0 |
| 16809332 | 1 | 1 | 0 |
| 16810299 | 1 | 0 | 0 |
| 16811307 | 1 | 2 | 0 |
| 16833141 | 1 | 2 | 0 |
| 16845367 | 5 | 1 | 0 |
| 16848479 | 1 | 2 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 2 | 0 | 0 |
| 16879253 | 1 | 1 | 0 |
| 16882725 | 0 | 2 | 0 |
| 16888254 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 109101976, 109103207, 109104212, 109105314, 109106326, 109107355, 109108455, 109109611, 109110633, 109111906, 109113198, 109114312, 109115365, 109116586, 109117696, 109118819, 109119891, 109121031, 109122077, 109123313, 109124150, 109124434, 109125722, 109126819, 109127961, 109129068, 109130264, 109131368, 109132480, 109133627, 109134100, 109134713, 109135837, 109136980, 109138066, 109139168, 109140342, 109141440, 109142550, 109143649, 109144772, 109146383, 109146989, 109148155, 109149259, 109150370, 109151473, 109152567, 109153686, 109154003
