# spencersi123 (rank 402, score 2673.8, silver)

- team id 16810299; current submission 56236723 (173 public games)
- 30 submissions found; 4669 public games from 2026-09-03 to 2026-09-15; 33 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 41-7-2 | 82 | 106474 | 107485.1 | 2125.4 | 54 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 729, game 10: 1527, game 25: 2479, game 50: 2672, game 100: 2734, game last: 2645

![rating](figs/spencersi123_rating.png)

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
| FERTILIZE ops | 110 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 129 |
| milk sold | 110 |
| wool sold | 81 |
| wheat sold | 329 |
| fertilizer sold | 286 |
| units sold last 3 days | 268 |
| shed peak | 45 |
| weeds spawned | 20 |
| unexecutable market orders | 1 |

![money by day](figs/spencersi123_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 8 (30%) | 21 (20%) | 40 (8%) | 49 (4%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 10 (30%) | 25 (20%) | 40 (8%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 12 (30%) | 26 (20%) | 41 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 40 at turn 400)**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 40 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 41 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 8 | 15 | 30 |
| 300 | 12 | 21 | 10 | 20 |
| 400 | 16 | 40 | 4 | 8 |
| 719 | 29 | 49 | 2 | 4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 1 | 100 | 69.4 |
| opponent off its modal line at turn 136 | 22 | 72.7 | 67.9 |
| played seat 1 | 23 | 56.5 | 81.5 |
| lost the game | 7 | 85.7 | 67.4 |
| first shop (day 3) is not Brunch Spot | 41 | 65.9 | 88.9 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 82 | 106474 | 12 | 6 | 6 | 3 | 3 | 6 | 33 | 163 | 12 | 12 | 110 | 81 | 40 | 40 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109009708 | Bruce | 2359.7 | 88745 | 115567 | -26822 | 9b0c82fd | milk sold: they 176 vs me 101; strawberry sold: they 144 vs me 100; wool sold: they 77 vs me 57 |
| C0 | 109018054 | Zenith Ye | 2584.7 | 109784 | 110727 | -943 | 9b0c82fd | strawberry sold: they 120 vs me 129; milk sold: they 111 vs me 117; CARE ops: they 410 vs me 405 |
| C0 | 109025342 | Raef Guizani | 2665.5 | 96806 | 96856 | -50 | 9b0c82fd | wheat planted: they 162 vs me 163; weeds spawned: they 19 vs me 20 |
| C0 | 109027611 | DeeSaa | 2683.8 | 100331 | 103824 | -3493 | 9b0c82fd | wool sold: they 178 vs me 188; units sold last 3 days: they 247 vs me 252; wheat planted: they 160 vs me 163 |
| C0 | 109027929 | Maximo Uribarri | 2724.2 | 75567 | 79266 | -3699 | 9b0c82fd | CARE ops: they 344 vs me 397; milk sold: they 64 vs me 86; strawberry sold: they 127 vs me 137 |
| C0 | 109031567 | Rudra | 2694.6 | 113467 | 120591 | -7124 | 9b0c82fd | FERTILIZE ops: they 101 vs me 122; wool sold: they 83 vs me 66; units sold last 3 days: they 279 vs me 262 |
| C0 | 109032614 | lumen | 2684.8 | 92475 | 95113 | -2638 | 9b0c82fd | strawberry sold: they 80 vs me 137; wool sold: they 93 vs me 121; milk sold: they 61 vs me 86 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622459 | 4 | 1 | 0 |
| 16626191 | 0 | 1 | 0 |
| 16633944 | 0 | 0 | 1 |
| 16637255 | 0 | 1 | 0 |
| 16640510 | 2 | 4 | 0 |
| 16641710 | 3 | 2 | 0 |
| 16644724 | 1 | 2 | 0 |
| 16655383 | 0 | 1 | 0 |
| 16657100 | 1 | 0 | 0 |
| 16658554 | 0 | 1 | 0 |
| 16660726 | 1 | 3 | 0 |
| 16664246 | 0 | 2 | 0 |
| 16671741 | 1 | 0 | 0 |
| 16675778 | 1 | 0 | 0 |
| 16684093 | 2 | 0 | 0 |
| 16690867 | 1 | 0 | 0 |
| 16706321 | 0 | 1 | 0 |
| 16719123 | 0 | 2 | 0 |
| 16723379 | 4 | 2 | 0 |
| 16725899 | 2 | 0 | 0 |
| 16728071 | 1 | 1 | 0 |
| 16730524 | 1 | 4 | 0 |
| 16730612 | 1 | 1 | 0 |
| 16730720 | 0 | 0 | 1 |
| 16730761 | 2 | 5 | 0 |
| 16731186 | 2 | 2 | 0 |
| 16731275 | 1 | 0 | 0 |
| 16732403 | 1 | 1 | 1 |
| 16732521 | 0 | 2 | 0 |
| 16732748 | 3 | 6 | 0 |
| 16741542 | 0 | 3 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 3 | 1 | 0 |
| 16777134 | 4 | 1 | 0 |
| 16805699 | 0 | 1 | 0 |
| 16809332 | 0 | 1 | 0 |
| 16811307 | 0 | 1 | 0 |
| 16848479 | 1 | 1 | 0 |
| 16858228 | 1 | 0 | 0 |
| 16862666 | 1 | 0 | 0 |
| 16879253 | 1 | 0 | 0 |
| 16880773 | 1 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108991155, 108992162, 108993183, 108994215, 108995232, 108996134, 108996267, 108997281, 108998309, 108999338, 109000381, 109001381, 109002418, 109003439, 109004471, 109005499, 109006531, 109007609, 109008640, 109009708, 109010769, 109011818, 109012848, 109013534, 109013886, 109014936, 109015957, 109017005, 109017137, 109017739, 109018054, 109019138, 109020168, 109021167, 109022269, 109023270, 109024248, 109025342, 109025478, 109026411, 109027432, 109027611, 109027929, 109028461, 109029509, 109030544, 109031567, 109032614, 109034245, 109034678
