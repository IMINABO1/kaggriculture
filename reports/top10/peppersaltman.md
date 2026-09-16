# peppersaltman (rank 400, score 2676.9, silver)

- team id 16848532; current submission 56224944 (214 public games)
- 9 submissions found; 1994 public games from 2026-09-07 to 2026-09-15; 34 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 42-8-0 | 84 | 110276.5 | 109347.7 | 2150.7 | 50 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 724, game 10: 1649, game 25: 2477, game 50: 2653, game 100: 2739, game 200: 2566, game last: 2574

![rating](figs/peppersaltman_rating.png)

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
| FERTILIZE ops | 99.5 |
| CARE ops | 417 |
| melon sold | 72 |
| strawberry sold | 248 |
| milk sold | 191 |
| wool sold | 148.5 |
| wheat sold | 366.5 |
| fertilizer sold | 352 |
| units sold last 3 days | 396.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/peppersaltman_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 9 (64%) | 16 (46%) | 40 (10%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 8 (70%) | 14 (50%) | 41 (6%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 10 (64%) | 16 (46%) | 42 (10%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 40 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 41 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 42 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 9 | 32 | 64 |
| 300 | 12 | 16 | 23 | 46 |
| 400 | 16 | 40 | 5 | 10 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 30.4 |
| opponent off its modal line at turn 136 | 31 | 45.2 | 21.1 |
| played seat 1 | 25 | 44 | 28 |
| lost the game | 8 | 25 | 38.1 |
| first shop (day 3) is not Pet Cafe | 40 | 40 | 20 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 84 | 110276.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 72 | 191 | 148.5 | 40 | 41 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108845997 | TOSS | 2230.6 | 134178 | 134929 | -751 | 9b0c82fd | FERTILIZE ops: they 61 vs me 112; units sold last 3 days: they 365 vs me 394; strawberry sold: they 249 vs me 246 |
| C0 | 108856349 | dasfds | 2499.9 | 111257 | 111387 | -130 | 9b0c82fd | strawberry sold: they 246 vs me 247; weeds spawned: they 20 vs me 19 |
| C0 | 108857421 | Datta Dhebe | 2564.8 | 54258 | 54527 | -269 | 9b0c82fd | units sold last 3 days: they 392 vs me 411; FERTILIZE ops: they 103 vs me 117; milk sold: they 218 vs me 209 |
| C0 | 108867640 | gachichan | 2671.8 | 134529 | 136971 | -2442 | 9b0c82fd |  |
| C0 | 108868681 | Keisuke | 2671.2 | 60368 | 63193 | -2825 | 5738b34d | units sold last 3 days: they 361 vs me 377; CARE ops: they 405 vs me 417; FERTILIZE ops: they 123 vs me 112 |
| C0 | 108869726 | Ugnė Miklovaitė | 2664.8 | 82655 | 84243 | -1588 | 9b0c82fd | wheat planted: they 163 vs me 162; weeds spawned: they 20 vs me 19 |
| C0 | 108871800 | quzhihang | 2681.3 | 123189 | 123662 | -473 | 9b0c82fd | CARE ops: they 406 vs me 417; FERTILIZE ops: they 124 vs me 114; strawberry sold: they 248 vs me 245 |
| C0 | 108874908 | Takauchi Suguru | 2659.6 | 113821 | 117587 | -3766 | 9b0c82fd | milk sold: they 191 vs me 158; strawberry sold: they 246 vs me 238; FERTILIZE ops: they 104 vs me 96 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622198 | 0 | 1 | 0 |
| 16626191 | 2 | 0 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 0 | 2 | 0 |
| 16641710 | 0 | 2 | 0 |
| 16644724 | 0 | 1 | 0 |
| 16655383 | 0 | 2 | 0 |
| 16657100 | 0 | 1 | 0 |
| 16658554 | 0 | 2 | 0 |
| 16671741 | 0 | 1 | 0 |
| 16684093 | 0 | 1 | 0 |
| 16690867 | 0 | 1 | 0 |
| 16706321 | 0 | 1 | 0 |
| 16719123 | 0 | 1 | 0 |
| 16723379 | 2 | 0 | 0 |
| 16728071 | 1 | 1 | 0 |
| 16730524 | 0 | 1 | 0 |
| 16730612 | 0 | 2 | 0 |
| 16731186 | 0 | 2 | 0 |
| 16732403 | 0 | 1 | 0 |
| 16732521 | 0 | 1 | 0 |
| 16758882 | 0 | 1 | 0 |
| 16765807 | 1 | 1 | 0 |
| 16809332 | 1 | 2 | 0 |
| 16811307 | 0 | 2 | 0 |
| 16833141 | 0 | 1 | 0 |
| 16848479 | 0 | 2 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16888254 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108828570, 108829580, 108830586, 108831598, 108832616, 108833643, 108834652, 108835683, 108836692, 108837704, 108838781, 108839753, 108840765, 108841784, 108842534, 108842588, 108842833, 108843898, 108844955, 108845997, 108847055, 108848091, 108849121, 108850151, 108851187, 108852188, 108852228, 108853267, 108854231, 108855351, 108856349, 108857421, 108858405, 108859507, 108860394, 108861336, 108862401, 108863419, 108864478, 108864576, 108865518, 108866584, 108867640, 108868681, 108869726, 108870757, 108871800, 108872833, 108873870, 108874908
