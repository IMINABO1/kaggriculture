# Sida Zuo (rank 8, score 2996.3, gold)

- team id 16664246; current submission 56235662 (112 public games)
- 24 submissions found; 3657 public games from 2026-08-05 to 2026-09-15; 27 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 46-4-0 | 92 | 107532.5 | 107988.3 | 2081.5 | 46 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 667, game 10: 1534, game 25: 2330, game 50: 2671, game 100: 2823, game last: 2842

![rating](figs/sida-zuo_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 11 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 8 |
| cows bought | 7 |
| sheep bought | 4 |
| geese bought | 4 |
| first cow day | 0 |
| wheat planted | 129 |
| carrot planted | 58.5 |
| tomato planted | 14 |
| strawberry planted | 26 |
| melon planted | 8 |
| FERTILIZE ops | 150 |
| CARE ops | 317 |
| melon sold | 0 |
| strawberry sold | 191 |
| milk sold | 112.5 |
| wool sold | 47 |
| wheat sold | 212 |
| fertilizer sold | 111 |
| units sold last 3 days | 242 |
| shed peak | 47 |
| weeds spawned | 13.5 |
| unexecutable market orders | 0 |

![money by day](figs/sida-zuo_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 4 (66%) | 10 (50%) | 12 (50%) | 15 (48%) | 42 (4%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 4 (66%) | 10 (50%) | 13 (50%) | 15 (48%) | 42 (4%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 4 (66%) | 10 (50%) | 13 (50%) | 15 (48%) | 42 (4%) | 50 (2%) | 50 (2%) | 50 (2%) |

Current submission (50 sampled games): field is **reactive from day 1: 4 openings at turn 24 (largest 66%), 12 lines at turn 100; every game distinct by turn 300**; market is **reactive from day 1: 4 openings at turn 24 (largest 66%), 13 lines at turn 100; every game distinct by turn 300**; plan is **reactive from day 1: 4 openings at turn 24 (largest 66%), 13 lines at turn 100; every game distinct by turn 300**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 4 | 33 | 66 |
| 48 | 2 | 10 | 25 | 50 |
| 100 | 4 | 12 | 25 | 50 |
| 136 | 5 | 15 | 24 | 48 |
| 200 | 8 | 42 | 2 | 4 |
| 300 | 12 | 50 | 1 | 2 |
| 400 | 16 | 50 | 1 | 2 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 24 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 1 | 0 |  | 34 |
| opponent off its modal line at turn 24 | 12 | 58.3 | 26.3 |
| played seat 1 | 27 | 33.3 | 34.8 |
| lost the game | 4 | 0 | 37.0 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 92 | 107532.5 | 11 | 7 | 4 | 4 | 3 | 6 | 26 | 129 | 8 | 0 | 112.5 | 47 | 50 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108991067 | torvile | 2387.6 | 89459 | 98623 | -9164 | 9b0c82fd | CARE ops: they 417 vs me 332; FERTILIZE ops: they 83 vs me 153; wheat planted: they 163 vs me 103 |
| C0 | 108993143 | Sho Saga | 2144.1 | 111745 | 112911 | -1166 | 9b0c82fd | FERTILIZE ops: they 61 vs me 137; wool sold: they 150 vs me 102; strawberry sold: they 151 vs me 193 |
| C0 | 108995246 | Octavi Grau | 2167.8 | 117981 | 119138 | -1157 | 9b0c82fd | strawberry sold: they 138 vs me 233; FERTILIZE ops: they 86 vs me 173; CARE ops: they 417 vs me 335 |
| C0 | 109015072 | xiao xiongwei | 2651.7 | 117188 | 117315 | -127 | 9b0c82fd | CARE ops: they 505 vs me 427; FERTILIZE ops: they 61 vs me 131; wheat planted: they 163 vs me 122 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 0 | 0 |
| 16622198 | 2 | 2 | 0 |
| 16622349 | 1 | 2 | 0 |
| 16622459 | 2 | 0 | 0 |
| 16626191 | 0 | 1 | 0 |
| 16633100 | 2 | 0 | 0 |
| 16633178 | 2 | 2 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 5 | 6 | 0 |
| 16640467 | 1 | 6 | 0 |
| 16640510 | 0 | 4 | 0 |
| 16641710 | 0 | 2 | 0 |
| 16644724 | 5 | 0 | 0 |
| 16655383 | 4 | 0 | 0 |
| 16657100 | 1 | 0 | 0 |
| 16658554 | 2 | 3 | 0 |
| 16660726 | 0 | 5 | 0 |
| 16671741 | 1 | 3 | 0 |
| 16675778 | 3 | 3 | 0 |
| 16683936 | 2 | 1 | 0 |
| 16684093 | 1 | 3 | 0 |
| 16690867 | 2 | 1 | 0 |
| 16706321 | 1 | 1 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 2 | 0 | 0 |
| 16723379 | 2 | 0 | 0 |
| 16725899 | 0 | 2 | 0 |
| 16728071 | 1 | 2 | 0 |
| 16730524 | 2 | 3 | 0 |
| 16730612 | 1 | 0 | 0 |
| 16730761 | 1 | 0 | 0 |
| 16731186 | 1 | 2 | 0 |
| 16731275 | 1 | 1 | 0 |
| 16732521 | 0 | 4 | 0 |
| 16732748 | 2 | 2 | 0 |
| 16741542 | 1 | 3 | 0 |
| 16758882 | 2 | 1 | 0 |
| 16760569 | 3 | 2 | 0 |
| 16773026 | 4 | 3 | 0 |
| 16777134 | 3 | 2 | 0 |
| 16778640 | 2 | 1 | 0 |
| 16781445 | 1 | 0 | 0 |
| 16805699 | 0 | 1 | 0 |
| 16810299 | 2 | 0 | 0 |
| 16811307 | 3 | 0 | 0 |
| 16833141 | 3 | 2 | 0 |
| 16845367 | 3 | 1 | 0 |
| 16848479 | 2 | 1 | 0 |
| 16858228 | 1 | 0 | 0 |
| 16880773 | 2 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108974650, 108975660, 108977022, 108977721, 108978732, 108979745, 108980788, 108981798, 108982803, 108983842, 108984855, 108985878, 108986908, 108987945, 108988976, 108990009, 108991067, 108992113, 108993143, 108994206, 108995246, 108996320, 108997359, 108998394, 108999439, 109000472, 109001514, 109002551, 109003584, 109004622, 109005655, 109006697, 109007743, 109007814, 109008794, 109009835, 109010875, 109011652, 109011907, 109012951, 109013989, 109015026, 109015072, 109016062, 109017104, 109017428, 109018134, 109019222, 109020256, 109021240
