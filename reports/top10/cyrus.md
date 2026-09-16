# Cyrus (rank 601, score 2587.9, bronze)

- team id 16683936; current submission 56226118 (190 public games)
- 55 submissions found; 8954 public games from 2026-08-07 to 2026-09-15; 128 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 43-6-1 | 86 | 112238.5 | 112686.8 | 2130.3 | 48 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 708, game 10: 1654, game 25: 2464, game 50: 2661, game 100: 2694, game last: 2550

![rating](figs/cyrus_rating.png)

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
| FERTILIZE ops | 104.5 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 134 |
| milk sold | 126.5 |
| wool sold | 88.5 |
| wheat sold | 330 |
| fertilizer sold | 291 |
| units sold last 3 days | 268.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/cyrus_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 11 (70%) | 17 (48%) | 38 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 9 (72%) | 15 (50%) | 28 (18%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 13 (70%) | 17 (48%) | 37 (12%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 38 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (98%), then branching (2 lines at turn 136, 28 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 37 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 49 | 98 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 11 | 35 | 70 |
| 300 | 12 | 17 | 24 | 48 |
| 400 | 16 | 38 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 23.9 |
| opponent off its modal line at turn 136 | 29 | 34.5 | 23.8 |
| played seat 1 | 26 | 34.6 | 25 |
| lost the game | 6 | 50 | 27.3 |
| first shop (day 3) is not Pet Cafe | 41 | 31.7 | 22.2 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 86 | 112238.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 126.5 | 88.5 | 38 | 28 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108857582 | iring58 | 1802.1 | 150820 | 150821 | -1 | 9b0c82fd |  |
| C0 | 108875786 | Kifine | 2584.5 | 71303 | 74676 | -3373 | a6a57513 | wool sold: they 102 vs me 56; strawberry sold: they 120 vs me 132; CARE ops: they 410 vs me 417 |
| C0 | 108877881 | Shuwen(Shawn) Ge | 2697.7 | 114869 | 116051 | -1182 | 9b0c82fd | CARE ops: they 494 vs me 506 |
| C0 | 108879862 | Le Trong Hieu | 2661.4 | 110841 | 111800 | -959 | 9b0c82fd | milk sold: they 122 vs me 123; units sold last 3 days: they 277 vs me 276 |
| C0 | 108880995 | mogura2.0 | 2652.3 | 115557 | 118242 | -2685 | 9b0c82fd | units sold last 3 days: they 316 vs me 274; FERTILIZE ops: they 93 vs me 119; milk sold: they 155 vs me 152 |
| C0 | 108887225 | StephaneB7899 | 2765.1 | 76558 | 80786 | -4228 | 9b0c82fd | wool sold: they 169 vs me 129; milk sold: they 113 vs me 93; units sold last 3 days: they 266 vs me 277 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622198 | 4 | 1 | 1 |
| 16622349 | 5 | 3 | 0 |
| 16622459 | 0 | 3 | 0 |
| 16626191 | 3 | 4 | 0 |
| 16633100 | 1 | 0 | 0 |
| 16633178 | 0 | 1 | 0 |
| 16633944 | 1 | 0 | 2 |
| 16637255 | 3 | 7 | 0 |
| 16640510 | 1 | 1 | 0 |
| 16641710 | 3 | 1 | 0 |
| 16644724 | 6 | 7 | 2 |
| 16655383 | 4 | 2 | 0 |
| 16657100 | 3 | 3 | 2 |
| 16660726 | 7 | 0 | 2 |
| 16664246 | 1 | 2 | 0 |
| 16671741 | 1 | 2 | 0 |
| 16684093 | 1 | 6 | 3 |
| 16690867 | 1 | 0 | 0 |
| 16706321 | 1 | 0 | 0 |
| 16719123 | 1 | 7 | 0 |
| 16723379 | 3 | 5 | 0 |
| 16725899 | 2 | 3 | 0 |
| 16728071 | 0 | 7 | 0 |
| 16730524 | 0 | 5 | 0 |
| 16730761 | 3 | 5 | 0 |
| 16731186 | 1 | 1 | 0 |
| 16731275 | 1 | 2 | 0 |
| 16732403 | 3 | 0 | 0 |
| 16732521 | 2 | 0 | 0 |
| 16732748 | 10 | 7 | 0 |
| 16741542 | 1 | 5 | 0 |
| 16758882 | 0 | 1 | 1 |
| 16765807 | 2 | 0 | 0 |
| 16777134 | 3 | 3 | 0 |
| 16805699 | 0 | 3 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16811307 | 1 | 4 | 0 |
| 16848479 | 0 | 3 | 0 |
| 16891058 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108843966, 108844998, 108845999, 108846976, 108848013, 108849036, 108850033, 108851079, 108852074, 108853100, 108854121, 108855145, 108856171, 108857190, 108857513, 108857582, 108858240, 108859310, 108860353, 108861182, 108862237, 108863292, 108864347, 108865394, 108866434, 108867048, 108867506, 108868542, 108869586, 108870625, 108871651, 108872691, 108873729, 108874780, 108875786, 108875808, 108876853, 108877278, 108877881, 108878929, 108879486, 108879862, 108879967, 108880995, 108882053, 108883104, 108884121, 108885149, 108886190, 108887225
