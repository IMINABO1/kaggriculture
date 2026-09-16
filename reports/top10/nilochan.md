# nilochan (rank 26, score 2928.5, gold)

- team id 16848479; current submission 56237232 (150 public games)
- 29 submissions found; 3188 public games from 2026-09-08 to 2026-09-15; 19 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 47-3-0 | 94 | 102002 | 105666.4 | 2215.7 | 58 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 712, game 10: 1656, game 25: 2561, game 50: 2832, game 100: 2929, game last: 2921

![rating](figs/nilochan_rating.png)

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
| FERTILIZE ops | 116.5 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 126 |
| milk sold | 95 |
| wool sold | 65.5 |
| wheat sold | 341.5 |
| fertilizer sold | 285 |
| units sold last 3 days | 252 |
| shed peak | 45 |
| weeds spawned | 20 |
| unexecutable market orders | 1 |

![money by day](figs/nilochan_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 11 (34%) | 19 (22%) | 36 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (88%) | 2 (88%) | 5 (44%) | 5 (44%) | 16 (20%) | 31 (12%) | 45 (6%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (88%) | 3 (86%) | 5 (44%) | 5 (44%) | 19 (18%) | 32 (10%) | 44 (6%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 36 at turn 400); every game distinct by turn 719**; market is **reactive from day 1: 2 openings at turn 24 (largest 88%), 5 lines at turn 100; every game distinct by turn 719**; plan is **reactive from day 1: 2 openings at turn 24 (largest 88%), 5 lines at turn 100; every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 11 | 17 | 34 |
| 300 | 12 | 19 | 11 | 22 |
| 400 | 16 | 36 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 63.0 |
| opponent off its modal line at turn 136 | 23 | 60.9 | 70.4 |
| played seat 1 | 21 | 61.9 | 69.0 |
| lost the game | 3 | 100 | 63.8 |
| first shop (day 3) is not Bakery | 37 | 64.9 | 69.2 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 94 | 102002 | 12 | 6.5 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 95 | 65.5 | 36 | 45 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109022223 | forever young | 2604.2 | 101698 | 101765 | -67 | 0fbf44b1 | units sold last 3 days: they 262 vs me 241; strawberry sold: they 103 vs me 120; wool sold: they 142 vs me 126 |
| C0 | 109027389 | Roman Svet | 2643.3 | 105809 | 113266 | -7457 | 74cb8b5b | milk sold: they 338 vs me 157; melon sold: they 102 vs me 12; units sold last 3 days: they 324 vs me 248 |
| C0 | 109038773 | yuto083 | 2794.9 | 94203 | 96055 | -1852 | 9b0c82fd | wool sold: they 114 vs me 54; milk sold: they 121 vs me 75; wheat planted: they 152 vs me 163 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 7 | 0 |
| 16622198 | 3 | 4 | 0 |
| 16622349 | 2 | 5 | 0 |
| 16622459 | 3 | 0 | 0 |
| 16626191 | 1 | 0 | 0 |
| 16633178 | 5 | 7 | 0 |
| 16637255 | 9 | 2 | 0 |
| 16640467 | 1 | 7 | 0 |
| 16640510 | 0 | 5 | 0 |
| 16641710 | 5 | 6 | 0 |
| 16644724 | 4 | 11 | 0 |
| 16658554 | 1 | 1 | 0 |
| 16660726 | 3 | 4 | 0 |
| 16664246 | 1 | 2 | 0 |
| 16671741 | 1 | 4 | 0 |
| 16675778 | 2 | 9 | 0 |
| 16683936 | 3 | 0 | 0 |
| 16684093 | 1 | 3 | 0 |
| 16690867 | 0 | 3 | 0 |
| 16706321 | 2 | 1 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 5 | 5 | 0 |
| 16723379 | 2 | 1 | 0 |
| 16725899 | 2 | 4 | 0 |
| 16728071 | 4 | 7 | 0 |
| 16730524 | 0 | 9 | 0 |
| 16730612 | 3 | 8 | 0 |
| 16730761 | 8 | 3 | 0 |
| 16731186 | 1 | 3 | 0 |
| 16731275 | 2 | 9 | 0 |
| 16732403 | 0 | 5 | 0 |
| 16732521 | 1 | 8 | 0 |
| 16732748 | 1 | 6 | 0 |
| 16741542 | 3 | 2 | 0 |
| 16758882 | 1 | 3 | 0 |
| 16760569 | 0 | 2 | 0 |
| 16765807 | 3 | 0 | 0 |
| 16773026 | 4 | 8 | 0 |
| 16777134 | 5 | 0 | 0 |
| 16778640 | 6 | 1 | 0 |
| 16781445 | 3 | 4 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 0 | 7 | 0 |
| 16810299 | 1 | 1 | 0 |
| 16811307 | 3 | 0 | 0 |
| 16833141 | 10 | 3 | 0 |
| 16845367 | 7 | 7 | 0 |
| 16848532 | 2 | 0 | 0 |
| 16858228 | 0 | 2 | 0 |
| 16879253 | 2 | 0 | 0 |
| 16882725 | 1 | 2 | 0 |

## Episodes behind each window

- **C0** (50): 109000438, 109001455, 109002489, 109003497, 109004527, 109005561, 109006589, 109007622, 109008633, 109009651, 109010686, 109011707, 109012297, 109012734, 109013765, 109014793, 109015845, 109016915, 109017951, 109019037, 109020083, 109021119, 109022169, 109022223, 109023207, 109023527, 109023746, 109024280, 109024411, 109025312, 109026353, 109027389, 109028431, 109029466, 109030499, 109031528, 109031836, 109032561, 109033370, 109034133, 109034633, 109035174, 109035676, 109036705, 109037736, 109038773, 109039807, 109040839, 109041869, 109042228
