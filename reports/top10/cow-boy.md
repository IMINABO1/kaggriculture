# Cow Boy (rank 20, score 2953.9, gold)

- team id 16633178; current submission 56225347 (200 public games)
- 28 submissions found; 3662 public games from 2026-08-23 to 2026-09-15; 27 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 110421.5 | 112439.7 | 2320.7 | 54 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 802, game 10: 1695, game 25: 2753, game 50: 2928, game 100: 2951, game 200: 2944, game last: 2944

![rating](figs/cow-boy_rating.png)

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
| FERTILIZE ops | 106 |
| CARE ops | 416 |
| melon sold | 72 |
| strawberry sold | 251 |
| milk sold | 206 |
| wool sold | 138.5 |
| wheat sold | 407 |
| fertilizer sold | 351 |
| units sold last 3 days | 396.5 |
| shed peak | 59 |
| weeds spawned | 18 |
| unexecutable market orders | 4 |

![money by day](figs/cow-boy_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 5 (82%) | 12 (48%) | 30 (10%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 4 (84%) | 16 (38%) | 49 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 5 (82%) | 17 (38%) | 42 (6%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 30 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 49 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 42 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 5 | 41 | 82 |
| 300 | 12 | 12 | 24 | 48 |
| 400 | 16 | 30 | 5 | 10 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 1 | 100 | 16.3 |
| opponent off its modal line at turn 136 | 31 | 12.9 | 26.3 |
| played seat 1 | 23 | 21.7 | 14.8 |
| lost the game | 5 | 0 | 20 |
| first shop (day 3) is not Ice Cream Shop | 40 | 17.5 | 20 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 110421.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 72 | 206 | 138.5 | 30 | 49 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108862372 | Subramanya N | 2904.5 | 99404 | 99927 | -523 | 9b0c82fd | wool sold: they 156 vs me 99; milk sold: they 165 vs me 192; FERTILIZE ops: they 103 vs me 120 |
| C0 | 108864419 | Ebi | 2785.8 | 158017 | 169627 | -11610 | 61137e61 | units sold last 3 days: they 1158 vs me 396; milk sold: they 373 vs me 266; strawberry sold: they 339 vs me 249 |
| C0 | 108868631 | yuto083 | 2857.4 | 154337 | 160092 | -5755 | 9b0c82fd | milk sold: they 321 vs me 266; wool sold: they 139 vs me 87; FERTILIZE ops: they 106 vs me 114 |
| C0 | 108874844 | yfy | 2863.0 | 112214 | 112455 | -241 | 3bc18d7a | milk sold: they 285 vs me 266; wool sold: they 106 vs me 120; units sold last 3 days: they 410 vs me 403 |
| C0 | 108875870 | WeAreFarmers | 2893.0 | 102011 | 104312 | -2301 | 9b0c82fd | milk sold: they 144 vs me 184; units sold last 3 days: they 440 vs me 423; FERTILIZE ops: they 122 vs me 106 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 2 | 6 | 0 |
| 16622198 | 3 | 5 | 0 |
| 16622349 | 4 | 4 | 0 |
| 16622459 | 3 | 1 | 0 |
| 16626191 | 0 | 1 | 0 |
| 16633100 | 5 | 0 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 1 | 6 | 0 |
| 16640467 | 0 | 5 | 0 |
| 16640510 | 6 | 8 | 0 |
| 16641710 | 1 | 3 | 1 |
| 16644724 | 9 | 7 | 0 |
| 16655383 | 1 | 0 | 0 |
| 16657100 | 0 | 2 | 0 |
| 16660726 | 0 | 4 | 0 |
| 16664246 | 2 | 2 | 0 |
| 16671741 | 1 | 1 | 0 |
| 16675778 | 1 | 8 | 0 |
| 16683936 | 1 | 0 | 0 |
| 16684093 | 3 | 1 | 0 |
| 16690867 | 1 | 1 | 0 |
| 16706321 | 0 | 2 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 1 | 7 | 0 |
| 16723379 | 2 | 4 | 0 |
| 16725899 | 1 | 2 | 0 |
| 16728071 | 2 | 4 | 0 |
| 16730524 | 4 | 10 | 0 |
| 16730612 | 3 | 4 | 0 |
| 16730761 | 7 | 3 | 0 |
| 16731186 | 1 | 0 | 0 |
| 16731275 | 0 | 4 | 0 |
| 16732403 | 2 | 7 | 0 |
| 16732521 | 0 | 7 | 0 |
| 16732748 | 7 | 7 | 0 |
| 16741542 | 1 | 1 | 0 |
| 16758882 | 5 | 5 | 0 |
| 16760569 | 5 | 1 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 0 | 4 | 0 |
| 16777134 | 5 | 1 | 0 |
| 16778640 | 5 | 2 | 0 |
| 16781445 | 6 | 1 | 0 |
| 16805699 | 3 | 4 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16811307 | 5 | 4 | 0 |
| 16833141 | 2 | 0 | 0 |
| 16845367 | 5 | 3 | 0 |
| 16848479 | 7 | 5 | 0 |
| 16858228 | 2 | 0 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16880773 | 1 | 0 | 0 |
| 16882725 | 1 | 2 | 0 |
| 16891058 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108833707, 108834738, 108835771, 108836754, 108837767, 108838758, 108839801, 108840802, 108840808, 108841818, 108842827, 108843845, 108844871, 108845895, 108846911, 108847940, 108849007, 108850042, 108851104, 108852135, 108853179, 108854263, 108855281, 108856357, 108857348, 108858078, 108858423, 108859446, 108860400, 108861280, 108862372, 108862594, 108863381, 108864419, 108865474, 108866514, 108867583, 108868631, 108869668, 108870699, 108871742, 108872766, 108873806, 108874844, 108875870, 108876904, 108877941, 108878982, 108880018, 108881051
