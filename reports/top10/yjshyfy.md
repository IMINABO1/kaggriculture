# yjshyfy (rank 27, score 2927.9, gold)

- team id 16641710; current submission 56233680 (163 public games)
- 48 submissions found; 8187 public games from 2026-08-02 to 2026-09-15; 96 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 47-3-0 | 94 | 100857 | 103830 | 2183.1 | 42 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 698, game 10: 1618, game 25: 2546, game 50: 2833, game 100: 2917, game last: 2921

![rating](figs/yjshyfy_rating.png)

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
| tomato planted | 1 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 101 |
| CARE ops | 358.5 |
| melon sold | 72 |
| strawberry sold | 246 |
| milk sold | 195 |
| wool sold | 118.5 |
| wheat sold | 375.5 |
| fertilizer sold | 357.5 |
| units sold last 3 days | 403 |
| shed peak | 56 |
| weeds spawned | 21 |
| unexecutable market orders | 0 |

![money by day](figs/yjshyfy_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 3 (96%) | 3 (96%) | 3 (96%) | 8 (54%) | 35 (14%) | 45 (4%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 2 (98%) | 2 (98%) | 7 (28%) | 36 (8%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (96%) | 3 (94%) | 3 (94%) | 8 (52%) | 34 (14%) | 48 (4%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 45 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (98%), then branching (2 lines at turn 136, 50 at turn 400); every game distinct by turn 400**; plan is **one line through turn 136 (94%), then branching (3 lines at turn 136, 48 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 3 | 48 | 96 |
| 100 | 4 | 3 | 48 | 96 |
| 136 | 5 | 3 | 48 | 96 |
| 200 | 8 | 8 | 27 | 54 |
| 300 | 12 | 35 | 7 | 14 |
| 400 | 16 | 45 | 2 | 4 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 5 | 100 | 40 |
| opponent off its modal line at turn 136 | 16 | 56.2 | 41.2 |
| played seat 1 | 29 | 41.4 | 52.4 |
| lost the game | 3 | 66.7 | 44.7 |
| first shop (day 3) is not Pet Cafe | 40 | 52.5 | 20 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 94 | 100857 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 72 | 195 | 118.5 | 45 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108977881 | JeremiahMannings | 2715.0 | 144803 | 145854 | -1051 | 9b0c82fd | FERTILIZE ops: they 106 vs me 99; wool sold: they 273 vs me 278; CARE ops: they 397 vs me 393 |
| C0 | 108986172 | DSM | 2812.2 | 112273 | 120928 | -8655 | 422a8637 | FERTILIZE ops: they 164 vs me 86; strawberry sold: they 309 vs me 249; CARE ops: they 301 vs me 359 |
| C0 | 108990365 | quantara.cv | 2760.3 | 123750 | 124187 | -437 | 9b0c82fd | milk sold: they 245 vs me 320; wool sold: they 161 vs me 139; units sold last 3 days: they 392 vs me 411 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 5 | 0 |
| 16622198 | 3 | 4 | 0 |
| 16622349 | 8 | 14 | 0 |
| 16622459 | 4 | 7 | 0 |
| 16626191 | 2 | 2 | 0 |
| 16633100 | 3 | 0 | 0 |
| 16633178 | 3 | 1 | 1 |
| 16633944 | 6 | 3 | 1 |
| 16637255 | 5 | 12 | 0 |
| 16640467 | 1 | 3 | 0 |
| 16640510 | 0 | 7 | 0 |
| 16644724 | 4 | 15 | 0 |
| 16655383 | 0 | 3 | 0 |
| 16657100 | 4 | 4 | 0 |
| 16658554 | 2 | 0 | 0 |
| 16660726 | 5 | 11 | 0 |
| 16664246 | 2 | 0 | 0 |
| 16671741 | 2 | 4 | 0 |
| 16675778 | 1 | 3 | 0 |
| 16683936 | 1 | 3 | 0 |
| 16684093 | 6 | 6 | 3 |
| 16690867 | 2 | 2 | 0 |
| 16706321 | 1 | 2 | 0 |
| 16718819 | 0 | 3 | 0 |
| 16719123 | 8 | 9 | 0 |
| 16723379 | 10 | 7 | 0 |
| 16725899 | 7 | 8 | 0 |
| 16728071 | 1 | 9 | 0 |
| 16730524 | 4 | 12 | 0 |
| 16730612 | 1 | 5 | 0 |
| 16730761 | 5 | 3 | 0 |
| 16731186 | 1 | 7 | 0 |
| 16731275 | 7 | 7 | 0 |
| 16732403 | 1 | 3 | 0 |
| 16732521 | 1 | 6 | 0 |
| 16732748 | 5 | 4 | 0 |
| 16741542 | 7 | 9 | 0 |
| 16758882 | 7 | 7 | 0 |
| 16760569 | 3 | 1 | 0 |
| 16765807 | 0 | 1 | 0 |
| 16773026 | 6 | 3 | 0 |
| 16777134 | 6 | 4 | 0 |
| 16778640 | 3 | 0 | 0 |
| 16781445 | 1 | 3 | 0 |
| 16805699 | 3 | 4 | 0 |
| 16810299 | 2 | 3 | 0 |
| 16811307 | 3 | 3 | 0 |
| 16833141 | 3 | 3 | 0 |
| 16845367 | 5 | 3 | 0 |
| 16848479 | 6 | 5 | 0 |
| 16848532 | 2 | 0 | 0 |
| 16858228 | 0 | 1 | 0 |
| 16879253 | 1 | 0 | 0 |
| 16880773 | 0 | 2 | 0 |
| 16882725 | 0 | 2 | 0 |

## Episodes behind each window

- **C0** (50): 108945818, 108946696, 108947704, 108948717, 108949787, 108950767, 108951775, 108952800, 108953833, 108954868, 108955904, 108956931, 108957974, 108958314, 108959001, 108960033, 108961063, 108962133, 108963222, 108964412, 108965356, 108965406, 108966424, 108967453, 108968551, 108969603, 108970598, 108971617, 108972652, 108973694, 108974737, 108975042, 108975807, 108977464, 108977881, 108978917, 108979167, 108979955, 108980990, 108982032, 108982579, 108983059, 108984115, 108985150, 108986172, 108986407, 108987229, 108988255, 108989169, 108990365
