# CaliforniaDog (rank 752, score 2526.2, bronze)

- team id 16888254; current submission 56239445 (159 public games)
- 2 submissions found; 421 public games from 2026-09-13 to 2026-09-15; 0 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 34-11-5 | 68 | 103913 | 107667.9 | 2154.3 | 42 | 1.32.7 | 2026-09-14 | 2026-09-15 |

## Rating path of the current submission

game 1: 728, game 10: 1572, game 25: 2545, game 50: 2592, game 100: 2587, game last: 2505

![rating](figs/californiadog_rating.png)

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
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 133 |
| milk sold | 132 |
| wool sold | 79 |
| wheat sold | 324 |
| fertilizer sold | 291 |
| units sold last 3 days | 267.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/californiadog_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 3 (84%) | 9 (58%) | 30 (14%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (84%) | 9 (58%) | 24 (24%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 5 (84%) | 10 (58%) | 32 (14%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (100%), then branching (1 lines at turn 136, 30 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 24 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (100%), then branching (1 lines at turn 136, 32 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 1 | 50 | 100 |
| 136 | 5 | 1 | 50 | 100 |
| 200 | 8 | 3 | 42 | 84 |
| 300 | 12 | 9 | 29 | 58 |
| 400 | 16 | 30 | 7 | 14 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 0 |  | 16 |
| opponent off its modal line at turn 136 | 23 | 4.3 | 25.9 |
| played seat 1 | 29 | 6.9 | 28.6 |
| lost the game | 11 | 27.3 | 12.8 |
| first shop (day 3) is not Smoothie Shop | 38 | 18.4 | 8.3 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 68 | 103913 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 132 | 79 | 30 | 24 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109070592 | yt0914 | 2463.9 | 119861 | 122057 | -2196 | d6b925bb | milk sold: they 173 vs me 176; wool sold: they 89 vs me 90; wheat planted: they 161 vs me 162 |
| C0 | 109080032 | kta_jpn | 2653.8 | 91363 | 92580 | -1217 | 9b0c82fd | units sold last 3 days: they 250 vs me 254; weeds spawned: they 22 vs me 20; wheat planted: they 163 vs me 162 |
| C0 | 109081148 | Kirderf | 2596.5 | 93725 | 95336 | -1611 | 9b0c82fd | strawberry sold: they 126 vs me 132; wool sold: they 51 vs me 56; units sold last 3 days: they 275 vs me 272 |
| C0 | 109086147 | Jingxiang | 2571.2 | 54049 | 54757 | -708 | 9b0c82fd | milk sold: they 152 vs me 106; wool sold: they 107 vs me 84; FERTILIZE ops: they 104 vs me 124 |
| C0 | 109088094 | Ali Alghaithi | 2648.8 | 149198 | 149239 | -41 | 9b0c82fd | weeds spawned: they 19 vs me 20 |
| C0 | 109091185 | tq1d | 2681.5 | 141201 | 141942 | -741 | 9b0c82fd | FERTILIZE ops: they 86 vs me 106; units sold last 3 days: they 268 vs me 284; wool sold: they 160 vs me 151 |
| C0 | 109092417 | kawauso9n | 2647.4 | 147960 | 148326 | -366 | 9b0c82fd | strawberry sold: they 130 vs me 146; milk sold: they 116 vs me 110; units sold last 3 days: they 250 vs me 251 |
| C0 | 109094663 | AQiDA19 | 2658.6 | 99283 | 99286 | -3 | 9b0c82fd | wheat planted: they 163 vs me 162; weeds spawned: they 20 vs me 19 |
| C0 | 109094681 | track | 2608.2 | 107729 | 109855 | -2126 | 9b0c82fd | FERTILIZE ops: they 125 vs me 103; units sold last 3 days: they 268 vs me 252; CARE ops: they 405 vs me 417 |
| C0 | 109095990 | Blu3s | 2636.0 | 134352 | 136503 | -2151 | d6b925bb | FERTILIZE ops: they 94 vs me 113; milk sold: they 191 vs me 173; strawberry sold: they 119 vs me 132 |
| C0 | 109096489 | hidsaito | 2622.9 | 111931 | 111932 | -1 | 9b0c82fd |  |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16626191 | 0 | 0 | 1 |
| 16633944 | 0 | 1 | 0 |
| 16640467 | 0 | 1 | 0 |
| 16657100 | 0 | 1 | 0 |
| 16658554 | 1 | 0 | 0 |
| 16706321 | 1 | 0 | 0 |
| 16730761 | 1 | 0 | 0 |
| 16731186 | 0 | 1 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16765807 | 0 | 0 | 1 |
| 16802867 | 1 | 0 | 1 |
| 16848532 | 0 | 1 | 0 |
| 16879253 | 1 | 2 | 0 |
| 16880773 | 0 | 1 | 0 |
| 16891058 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 109050994, 109052019, 109053055, 109054076, 109055107, 109056132, 109057165, 109058190, 109059223, 109060253, 109061280, 109062312, 109063340, 109064361, 109065394, 109065683, 109066455, 109067498, 109068540, 109069572, 109070592, 109070955, 109071656, 109072713, 109073762, 109074800, 109076055, 109077492, 109078569, 109080032, 109081148, 109082318, 109083553, 109084887, 109085577, 109086147, 109087557, 109088040, 109088094, 109088823, 109090067, 109091185, 109092417, 109093518, 109093914, 109094663, 109094681, 109095990, 109096489, 109097364
