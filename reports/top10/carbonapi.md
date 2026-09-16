# carbonapi (rank 19, score 2957.1, gold)

- team id 16731275; current submission 56236960 (148 public games)
- 25 submissions found; 4276 public games from 2026-08-24 to 2026-09-15; 22 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 44-5-1 | 88 | 103596.5 | 104051.2 | 2220.2 | 46 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 736, game 10: 1597, game 25: 2633, game 50: 2820, game 100: 2908, game last: 2956

![rating](figs/carbonapi_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 12 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 11 |
| cows bought | 7.5 |
| sheep bought | 7.5 |
| geese bought | 3 |
| first cow day | 0 |
| wheat planted | 154.5 |
| carrot planted | 40 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 124.5 |
| CARE ops | 400 |
| melon sold | 72 |
| strawberry sold | 249 |
| milk sold | 189.5 |
| wool sold | 144 |
| wheat sold | 566.5 |
| fertilizer sold | 345.5 |
| units sold last 3 days | 403 |
| shed peak | 60 |
| weeds spawned | 21.5 |
| unexecutable market orders | 0 |

![money by day](figs/carbonapi_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (96%) | 2 (96%) | 2 (96%) | 2 (96%) | 13 (36%) | 38 (18%) | 44 (10%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (94%) | 3 (94%) | 3 (94%) | 3 (94%) | 36 (8%) | 49 (4%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (94%) | 3 (94%) | 3 (94%) | 3 (94%) | 37 (8%) | 49 (4%) | 50 (2%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (2 lines at turn 136, 44 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (94%), then branching (3 lines at turn 136, 50 at turn 400); every game distinct by turn 400**; plan is **one line through turn 136 (94%), then branching (3 lines at turn 136, 50 at turn 400); every game distinct by turn 400**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 48 | 96 |
| 48 | 2 | 2 | 48 | 96 |
| 100 | 4 | 2 | 48 | 96 |
| 136 | 5 | 2 | 48 | 96 |
| 200 | 8 | 13 | 18 | 36 |
| 300 | 12 | 38 | 9 | 18 |
| 400 | 16 | 44 | 5 | 10 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 60.9 |
| opponent off its modal line at turn 136 | 17 | 76.5 | 57.6 |
| played seat 1 | 27 | 63.0 | 65.2 |
| lost the game | 5 | 100 | 60 |
| first shop (day 3) is not Brunch Spot | 41 | 63.4 | 66.7 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 88 | 103596.5 | 12 | 7.5 | 7.5 | 3 | 3 | 6 | 33 | 154.5 | 12 | 72 | 189.5 | 144 | 44 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109019097 | HireMe | 2709.9 | 91121 | 91287 | -166 | 9b0c82fd | strawberry sold: they 245 vs me 185; milk sold: they 239 vs me 275; units sold last 3 days: they 423 vs me 397 |
| C0 | 109023344 | MMN0222 | 2790.4 | 133707 | 137076 | -3369 | 9b0c82fd | units sold last 3 days: they 379 vs me 408; FERTILIZE ops: they 94 vs me 119; strawberry sold: they 245 vs me 228 |
| C0 | 109025314 | monsaraida | 2718.7 | 103281 | 109007 | -5726 | 9b0c82fd | strawberry sold: they 249 vs me 147; wool sold: they 381 vs me 309; FERTILIZE ops: they 61 vs me 113 |
| C0 | 109027411 | TheMightiestMan | 2704.5 | 72945 | 74971 | -2026 | 9b0c82fd | units sold last 3 days: they 396 vs me 369; milk sold: they 159 vs me 140; wheat planted: they 162 vs me 146 |
| C0 | 109031548 | Otter Vibe | 2794.1 | 75688 | 77801 | -2113 | a4e9ba8d | FERTILIZE ops: they 273 vs me 92; CARE ops: they 263 vs me 400; strawberry sold: they 120 vs me 249 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 3 | 2 | 0 |
| 16622198 | 7 | 7 | 0 |
| 16622349 | 8 | 7 | 0 |
| 16622459 | 0 | 1 | 0 |
| 16626191 | 2 | 0 | 0 |
| 16633100 | 1 | 1 | 0 |
| 16633178 | 4 | 0 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 7 | 7 | 0 |
| 16640467 | 4 | 2 | 0 |
| 16640510 | 0 | 3 | 0 |
| 16641710 | 7 | 7 | 0 |
| 16644724 | 9 | 6 | 0 |
| 16655383 | 1 | 0 | 0 |
| 16657100 | 0 | 1 | 0 |
| 16658554 | 1 | 1 | 0 |
| 16660726 | 4 | 18 | 0 |
| 16664246 | 1 | 1 | 0 |
| 16675778 | 0 | 2 | 0 |
| 16683936 | 2 | 1 | 0 |
| 16684093 | 4 | 2 | 0 |
| 16690867 | 0 | 6 | 0 |
| 16706321 | 2 | 0 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 1 | 5 | 0 |
| 16723379 | 1 | 3 | 0 |
| 16725899 | 6 | 2 | 0 |
| 16728071 | 9 | 6 | 0 |
| 16730524 | 1 | 10 | 0 |
| 16730612 | 0 | 2 | 0 |
| 16730761 | 2 | 3 | 0 |
| 16731186 | 3 | 2 | 0 |
| 16732403 | 2 | 9 | 0 |
| 16732521 | 5 | 12 | 0 |
| 16732748 | 0 | 8 | 0 |
| 16741542 | 10 | 3 | 0 |
| 16758882 | 5 | 5 | 0 |
| 16760569 | 6 | 4 | 0 |
| 16765807 | 2 | 0 | 0 |
| 16773026 | 2 | 1 | 0 |
| 16777134 | 2 | 1 | 0 |
| 16778640 | 3 | 2 | 0 |
| 16781445 | 2 | 2 | 0 |
| 16805699 | 1 | 5 | 0 |
| 16810299 | 0 | 1 | 0 |
| 16811307 | 5 | 3 | 0 |
| 16833141 | 10 | 1 | 0 |
| 16845367 | 8 | 4 | 0 |
| 16848479 | 9 | 2 | 0 |
| 16858228 | 2 | 2 | 0 |
| 16879253 | 2 | 1 | 0 |
| 16882725 | 0 | 1 | 0 |
| 16891058 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108996307, 108997328, 108998351, 108999377, 109000379, 109001415, 109002437, 109002443, 109002731, 109003466, 109004487, 109005514, 109006550, 109007578, 109008605, 109009635, 109010671, 109011735, 109012391, 109012792, 109013855, 109014898, 109015022, 109015176, 109015941, 109016981, 109018019, 109019097, 109020128, 109021205, 109021272, 109022226, 109023262, 109023344, 109024330, 109025314, 109025326, 109026371, 109027411, 109028457, 109029159, 109029492, 109030526, 109031548, 109032591, 109033344, 109034182, 109034666, 109035697, 109036732
