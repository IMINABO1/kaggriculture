# local (rank 16, score 2964.1, gold)

- team id 16723379; current submission 56236614 (142 public games)
- 50 submissions found; 7601 public games from 2026-08-15 to 2026-09-15; 405 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 105971 | 104407.8 | 2128.0 | 38 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 707, game 10: 1549, game 25: 2449, game 50: 2713, game 100: 2911, game last: 2968

![rating](figs/local_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 12 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 11 |
| cows bought | 6 |
| sheep bought | 6 |
| geese bought | 3 |
| first cow day | 0 |
| wheat planted | 163 |
| carrot planted | 31 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 114 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 125 |
| milk sold | 107 |
| wool sold | 72 |
| wheat sold | 327 |
| fertilizer sold | 280 |
| units sold last 3 days | 262.5 |
| shed peak | 45 |
| weeds spawned | 20 |
| unexecutable market orders | 1 |

![money by day](figs/local_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (94%) | 2 (94%) | 2 (94%) | 10 (38%) | 17 (28%) | 38 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 2 (96%) | 2 (96%) | 10 (44%) | 18 (28%) | 43 (8%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (94%) | 3 (90%) | 3 (90%) | 13 (36%) | 19 (28%) | 44 (10%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (94%), then branching (2 lines at turn 136, 38 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (96%), then branching (2 lines at turn 136, 43 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (90%), then branching (3 lines at turn 136, 44 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 47 | 94 |
| 100 | 4 | 2 | 47 | 94 |
| 136 | 5 | 2 | 47 | 94 |
| 200 | 8 | 10 | 19 | 38 |
| 300 | 12 | 17 | 14 | 28 |
| 400 | 16 | 38 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 5 | 100 | 57.8 |
| opponent off its modal line at turn 136 | 17 | 52.9 | 66.7 |
| played seat 1 | 31 | 58.1 | 68.4 |
| lost the game | 5 | 80 | 60 |
| first shop (day 3) is not Brunch Spot | 41 | 61.0 | 66.7 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 105971 | 12 | 6 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 107 | 72 | 38 | 43 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109008665 | l'rug | 2293.5 | 129554 | 133075 | -3521 | 9b0c82fd | milk sold: they 176 vs me 122; wool sold: they 90 vs me 56; FERTILIZE ops: they 99 vs me 115 |
| C0 | 109019131 | Blu3s | 2615.4 | 76489 | 76604 | -115 | 9b0c82fd | strawberry sold: they 119 vs me 139; FERTILIZE ops: they 102 vs me 122; milk sold: they 137 vs me 128 |
| C0 | 109020166 | Ruslan Akhmetov | 2590.2 | 101081 | 102575 | -1494 | 9b0c82fd | milk sold: they 125 vs me 102; strawberry sold: they 134 vs me 122; FERTILIZE ops: they 100 vs me 109 |
| C0 | 109026600 | 失忆的海_ | 2648.2 | 113224 | 118189 | -4965 | 9b0c82fd | milk sold: they 110 vs me 86; strawberry sold: they 140 vs me 117; units sold last 3 days: they 277 vs me 269 |
| C0 | 109028487 | parv goyal2 | 2637.2 | 72412 | 76590 | -4178 | 422a8637 | CARE ops: they 279 vs me 415; units sold last 3 days: they 346 vs me 261; strawberry sold: they 205 vs me 132 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 4 | 0 |
| 16622198 | 2 | 2 | 0 |
| 16622349 | 7 | 3 | 0 |
| 16622459 | 3 | 2 | 0 |
| 16626191 | 1 | 1 | 0 |
| 16633100 | 1 | 0 | 0 |
| 16633178 | 4 | 2 | 0 |
| 16633944 | 4 | 2 | 0 |
| 16637255 | 7 | 5 | 0 |
| 16640467 | 1 | 3 | 0 |
| 16640510 | 3 | 4 | 0 |
| 16641710 | 7 | 10 | 0 |
| 16644724 | 2 | 8 | 0 |
| 16655383 | 5 | 5 | 0 |
| 16657100 | 1 | 4 | 0 |
| 16660726 | 3 | 6 | 0 |
| 16664246 | 0 | 2 | 0 |
| 16671741 | 0 | 2 | 0 |
| 16675778 | 1 | 3 | 0 |
| 16683936 | 5 | 3 | 0 |
| 16684093 | 6 | 2 | 0 |
| 16690867 | 1 | 3 | 0 |
| 16718819 | 0 | 2 | 0 |
| 16719123 | 10 | 12 | 0 |
| 16725899 | 3 | 3 | 0 |
| 16728071 | 7 | 7 | 0 |
| 16730524 | 5 | 6 | 0 |
| 16730612 | 2 | 4 | 0 |
| 16730761 | 3 | 1 | 0 |
| 16731186 | 2 | 11 | 0 |
| 16731275 | 3 | 1 | 0 |
| 16732403 | 1 | 1 | 0 |
| 16732521 | 1 | 2 | 0 |
| 16732748 | 11 | 7 | 0 |
| 16741542 | 5 | 5 | 0 |
| 16758882 | 3 | 3 | 0 |
| 16760569 | 2 | 2 | 0 |
| 16773026 | 1 | 3 | 0 |
| 16777134 | 3 | 3 | 0 |
| 16778640 | 1 | 0 | 0 |
| 16781445 | 4 | 1 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 3 | 3 | 0 |
| 16810299 | 2 | 4 | 0 |
| 16811307 | 2 | 3 | 0 |
| 16833141 | 0 | 4 | 0 |
| 16845367 | 5 | 4 | 0 |
| 16848479 | 1 | 2 | 0 |
| 16848532 | 0 | 2 | 0 |
| 16879253 | 0 | 2 | 0 |
| 16880773 | 0 | 2 | 0 |
| 16882725 | 1 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108990115, 108991131, 108992145, 108993184, 108994198, 108995230, 108996253, 108997272, 108998300, 108999332, 109000368, 109001382, 109002413, 109003435, 109004469, 109005497, 109006560, 109007597, 109008665, 109009694, 109010743, 109011816, 109012854, 109013897, 109013936, 109014934, 109015530, 109015974, 109017004, 109018055, 109019131, 109019783, 109020166, 109020352, 109021169, 109022238, 109022670, 109023283, 109023369, 109024383, 109025373, 109026413, 109026600, 109027451, 109028487, 109029525, 109030566, 109031596, 109031958, 109032632
