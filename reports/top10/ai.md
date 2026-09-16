# AI是我的豆包 (rank 23, score 2943.5, gold)

- team id 16728071; current submission 56237149 (160 public games)
- 105 submissions found; 10299 public games from 2026-08-16 to 2026-09-15; 94 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 46-4-0 | 92 | 107738 | 111956.1 | 2037.1 | 48 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 726, game 10: 1498, game 25: 2402, game 50: 2671, game 100: 2822, game last: 2940

![rating](figs/ai_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 11 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 9 |
| cows bought | 7 |
| sheep bought | 3 |
| geese bought | 2 |
| first cow day | 0 |
| wheat planted | 172 |
| carrot planted | 21.5 |
| tomato planted | 7 |
| strawberry planted | 34 |
| melon planted | 12 |
| FERTILIZE ops | 151.5 |
| CARE ops | 301 |
| melon sold | 71 |
| strawberry sold | 256 |
| milk sold | 159.5 |
| wool sold | 98 |
| wheat sold | 339.5 |
| fertilizer sold | 201 |
| units sold last 3 days | 369.5 |
| shed peak | 55 |
| weeds spawned | 17 |
| unexecutable market orders | 0 |

![money by day](figs/ai_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 4 (50%) | 4 (50%) | 36 (10%) | 48 (4%) | 49 (4%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (54%) | 3 (50%) | 3 (50%) | 35 (10%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 2 (98%) | 2 (98%) | 34 (16%) | 50 (2%) | 50 (2%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 48 (100%), then branching (4 lines at turn 136, 49 at turn 400); every game distinct by turn 719**; market is **one line through turn 24 (100%), then branching (3 lines at turn 136, 50 at turn 400); every game distinct by turn 300**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 50 at turn 400); every game distinct by turn 300**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 4 | 25 | 50 |
| 136 | 5 | 4 | 25 | 50 |
| 200 | 8 | 36 | 5 | 10 |
| 300 | 12 | 48 | 2 | 4 |
| 400 | 16 | 49 | 2 | 4 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 100 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 4 | 1 | 100 | 49.0 |
| opponent off its modal line at turn 48 | 13 | 30.8 | 56.8 |
| played seat 1 | 26 | 50 | 50 |
| lost the game | 4 | 50 | 50 |
| first shop (day 3) is not Pizza Shop | 39 | 51.3 | 45.5 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 92 | 107738 | 11 | 7 | 3 | 2 | 3 | 6 | 34 | 172 | 12 | 71 | 159.5 | 98 | 49 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109017917 | nikotin55 | 2384.9 | 82568 | 84687 | -2119 | 9b0c82fd | CARE ops: they 417 vs me 264; milk sold: they 245 vs me 98; FERTILIZE ops: they 80 vs me 144 |
| C0 | 109024531 | bpbpbpbpb | 2384.5 | 130790 | 131714 | -924 | 9b0c82fd | CARE ops: they 417 vs me 296; FERTILIZE ops: they 83 vs me 162; strawberry sold: they 249 vs me 324 |
| C0 | 109030483 | Arman Tuganbaev | 2535.7 | 127138 | 128760 | -1622 | 9b0c82fd | units sold last 3 days: they 472 vs me 358; CARE ops: they 459 vs me 387; FERTILIZE ops: they 104 vs me 154 |
| C0 | 109036686 | Odyssey | 2587.1 | 89656 | 95309 | -5653 | 9b0c82fd | CARE ops: they 417 vs me 296; FERTILIZE ops: they 80 vs me 158; wool sold: they 161 vs me 113 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 1 | 0 |
| 16622198 | 5 | 7 | 0 |
| 16622349 | 4 | 10 | 0 |
| 16622459 | 4 | 2 | 0 |
| 16626191 | 7 | 2 | 0 |
| 16633100 | 3 | 0 | 0 |
| 16633178 | 4 | 2 | 0 |
| 16633944 | 9 | 3 | 0 |
| 16637255 | 12 | 6 | 3 |
| 16640467 | 2 | 1 | 0 |
| 16640510 | 4 | 9 | 0 |
| 16641710 | 9 | 1 | 0 |
| 16644724 | 13 | 8 | 2 |
| 16655383 | 9 | 2 | 0 |
| 16657100 | 10 | 2 | 0 |
| 16658554 | 2 | 1 | 0 |
| 16660726 | 4 | 7 | 0 |
| 16664246 | 2 | 1 | 0 |
| 16671741 | 3 | 2 | 0 |
| 16675778 | 3 | 2 | 0 |
| 16683936 | 7 | 0 | 0 |
| 16684093 | 12 | 3 | 0 |
| 16690867 | 2 | 1 | 0 |
| 16706321 | 2 | 0 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 8 | 7 | 0 |
| 16723379 | 7 | 7 | 0 |
| 16725899 | 11 | 1 | 0 |
| 16730524 | 0 | 8 | 1 |
| 16730612 | 0 | 1 | 0 |
| 16730761 | 9 | 0 | 0 |
| 16731186 | 8 | 2 | 0 |
| 16731275 | 6 | 9 | 0 |
| 16732403 | 1 | 7 | 0 |
| 16732521 | 4 | 5 | 1 |
| 16732748 | 11 | 4 | 0 |
| 16741542 | 11 | 11 | 0 |
| 16758882 | 12 | 6 | 1 |
| 16760569 | 1 | 2 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 2 | 2 | 0 |
| 16777134 | 3 | 6 | 0 |
| 16778640 | 4 | 0 | 0 |
| 16781445 | 1 | 1 | 0 |
| 16805699 | 6 | 5 | 0 |
| 16810299 | 1 | 1 | 0 |
| 16811307 | 7 | 3 | 0 |
| 16833141 | 1 | 1 | 0 |
| 16845367 | 2 | 0 | 0 |
| 16848479 | 7 | 4 | 0 |
| 16848532 | 1 | 1 | 0 |
| 16858228 | 3 | 0 | 0 |
| 16879253 | 1 | 0 | 0 |
| 16880773 | 1 | 0 | 0 |
| 16891058 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108999414, 109000419, 109001457, 109002466, 109003501, 109004522, 109005556, 109006587, 109007620, 109008634, 109009663, 109010695, 109011712, 109012747, 109012755, 109013773, 109014798, 109015829, 109016858, 109017673, 109017917, 109019027, 109020068, 109021098, 109022142, 109023203, 109024220, 109024531, 109025295, 109026320, 109026888, 109027360, 109028403, 109028504, 109029443, 109030483, 109031507, 109032543, 109034041, 109034619, 109035652, 109036686, 109037715, 109038747, 109039780, 109040812, 109040978, 109041850, 109042885, 109043919
