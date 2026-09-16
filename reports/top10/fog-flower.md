# fog flower (rank 24, score 2942.2, gold)

- team id 16684093; current submission 56240814 (124 public games)
- 79 submissions found; 10155 public games from 2026-08-09 to 2026-09-15; 97 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 47-3-0 | 94 | 109297 | 106206.9 | 2292.7 | 46 | 1.32.7 | 2026-09-15 | 2026-09-15 |

## Rating path of the current submission

game 1: 736, game 10: 1757, game 25: 2640, game 50: 2880, game 100: 2933, game last: 2930

![rating](figs/fog-flower_rating.png)

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
| FERTILIZE ops | 105 |
| CARE ops | 362.5 |
| melon sold | 12 |
| strawberry sold | 152 |
| milk sold | 129 |
| wool sold | 68 |
| wheat sold | 346.5 |
| fertilizer sold | 287 |
| units sold last 3 days | 270 |
| shed peak | 56 |
| weeds spawned | 20 |
| unexecutable market orders | 0 |

![money by day](figs/fog-flower_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (76%) | 15 (30%) | 31 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 8 (64%) | 18 (28%) | 44 (8%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (76%) | 15 (30%) | 36 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 31 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 44 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (100%), then branching (1 lines at turn 136, 36 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 5 | 38 | 76 |
| 300 | 12 | 15 | 15 | 30 |
| 400 | 16 | 31 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 1 | 100 | 22.4 |
| opponent off its modal line at turn 136 | 20 | 30 | 20 |
| played seat 1 | 27 | 29.6 | 17.4 |
| lost the game | 3 | 33.3 | 23.4 |
| first shop (day 3) is not Smoothie Shop | 40 | 30 | 0 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 94 | 109297 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 129 | 68 | 31 | 44 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109119003 | Yuvraj Bhati | 2704.1 | 73781 | 76411 | -2630 | 9b0c82fd | milk sold: they 103 vs me 171; CARE ops: they 405 vs me 357; strawberry sold: they 130 vs me 152 |
| C0 | 109133784 | Munal Singh | 2889.2 | 56554 | 57303 | -749 | 9b0c82fd | CARE ops: they 405 vs me 332; wool sold: they 100 vs me 75; milk sold: they 72 vs me 92 |
| C0 | 109134855 | AI是我的豆包 | 2890.3 | 101201 | 103393 | -2192 | 3bc18d7a | milk sold: they 82 vs me 109; CARE ops: they 330 vs me 320; units sold last 3 days: they 274 vs me 270 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 1 | 0 |
| 16622198 | 2 | 3 | 0 |
| 16622349 | 4 | 10 | 0 |
| 16622459 | 4 | 2 | 0 |
| 16626191 | 3 | 4 | 0 |
| 16633100 | 2 | 1 | 0 |
| 16633178 | 1 | 3 | 0 |
| 16633944 | 4 | 6 | 2 |
| 16637255 | 8 | 8 | 3 |
| 16640467 | 1 | 1 | 0 |
| 16640510 | 2 | 4 | 0 |
| 16641710 | 6 | 6 | 3 |
| 16644724 | 5 | 10 | 1 |
| 16655383 | 3 | 7 | 0 |
| 16657100 | 1 | 1 | 1 |
| 16658554 | 3 | 3 | 0 |
| 16660726 | 7 | 9 | 1 |
| 16664246 | 3 | 1 | 0 |
| 16671741 | 2 | 5 | 0 |
| 16683936 | 6 | 1 | 3 |
| 16690867 | 1 | 1 | 0 |
| 16706321 | 3 | 3 | 0 |
| 16718819 | 1 | 0 | 0 |
| 16719123 | 5 | 6 | 0 |
| 16723379 | 2 | 6 | 0 |
| 16725899 | 3 | 5 | 0 |
| 16728071 | 3 | 12 | 0 |
| 16730524 | 1 | 8 | 0 |
| 16730612 | 0 | 2 | 0 |
| 16730720 | 1 | 0 | 0 |
| 16730761 | 3 | 4 | 0 |
| 16731186 | 4 | 5 | 0 |
| 16731275 | 2 | 4 | 0 |
| 16732403 | 3 | 3 | 1 |
| 16732521 | 1 | 1 | 1 |
| 16732748 | 8 | 4 | 0 |
| 16741542 | 4 | 12 | 0 |
| 16758882 | 1 | 5 | 0 |
| 16760569 | 2 | 0 | 0 |
| 16761744 | 1 | 1 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 1 | 0 | 0 |
| 16777134 | 3 | 1 | 0 |
| 16778640 | 0 | 3 | 0 |
| 16802867 | 2 | 2 | 0 |
| 16805699 | 7 | 5 | 0 |
| 16810299 | 0 | 2 | 0 |
| 16811307 | 4 | 1 | 0 |
| 16833141 | 2 | 1 | 0 |
| 16845367 | 2 | 1 | 0 |
| 16848479 | 3 | 1 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 1 | 1 | 0 |
| 16880773 | 1 | 2 | 0 |
| 16882725 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 109084803, 109086025, 109087403, 109088666, 109089883, 109090988, 109092206, 109093288, 109094426, 109095752, 109097106, 109098220, 109099512, 109100548, 109101884, 109102835, 109103118, 109104180, 109105297, 109106374, 109107397, 109108545, 109109701, 109110757, 109112030, 109113324, 109114466, 109115525, 109116752, 109117378, 109117881, 109119003, 109119174, 109120092, 109121223, 109122266, 109123494, 109124618, 109124963, 109125869, 109126968, 109128092, 109128823, 109129194, 109129354, 109130408, 109131518, 109132641, 109133784, 109134855
