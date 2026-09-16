# Jacky Chan (rank 473, score 2649.6, bronze)

- team id 16657100; current submission 56237899 (158 public games)
- 37 submissions found; 7900 public games from 2026-08-05 to 2026-09-15; 133 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 43-5-2 | 86 | 102570.5 | 105025.4 | 2188.7 | 54 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 683, game 10: 1647, game 25: 2591, game 50: 2750, game 100: 2729, game last: 2643

![rating](figs/jacky-chan_rating.png)

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
| FERTILIZE ops | 115.5 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 130.5 |
| milk sold | 117.5 |
| wool sold | 82 |
| wheat sold | 328 |
| fertilizer sold | 287 |
| units sold last 3 days | 270 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/jacky-chan_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 14 (40%) | 22 (22%) | 37 (10%) | 49 (4%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 15 (42%) | 23 (24%) | 39 (12%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 17 (40%) | 24 (22%) | 37 (10%) | 49 (4%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 37 at turn 400)**; market is **one line through turn 136 (96%), then branching (3 lines at turn 136, 39 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (96%), then branching (3 lines at turn 136, 37 at turn 400)**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 48 | 96 |
| 48 | 2 | 3 | 48 | 96 |
| 100 | 4 | 3 | 48 | 96 |
| 136 | 5 | 3 | 48 | 96 |
| 200 | 8 | 14 | 20 | 40 |
| 300 | 12 | 22 | 11 | 22 |
| 400 | 16 | 37 | 5 | 10 |
| 719 | 29 | 49 | 2 | 4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 2 | 100 | 58.3 |
| opponent off its modal line at turn 136 | 21 | 61.9 | 58.6 |
| played seat 1 | 23 | 65.2 | 55.6 |
| lost the game | 5 | 80 | 57.8 |
| first shop (day 3) is not Smoothie Shop | 40 | 65 | 40 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 86 | 102570.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 117.5 | 82 | 37 | 39 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109044861 | cm391 | 2702.7 | 70486 | 71806 | -1320 | 9b0c82fd |  |
| C0 | 109045903 | HireMe | 2703.0 | 63819 | 65109 | -1290 | 9b0c82fd | milk sold: they 110 vs me 78; wool sold: they 164 vs me 135; FERTILIZE ops: they 97 vs me 111 |
| C0 | 109046944 | magic101 | 2781.8 | 120811 | 121888 | -1077 | 9b0c82fd | weeds spawned: they 19 vs me 21; wheat planted: they 162 vs me 161 |
| C0 | 109047441 | Harshini Reddy | 2746.8 | 88575 | 90683 | -2108 | 9b0c82fd | milk sold: they 161 vs me 76; wool sold: they 107 vs me 66; CARE ops: they 417 vs me 398 |
| C0 | 109058365 | MMN0222 | 2819.7 | 60330 | 61290 | -960 | 9b0c82fd | CARE ops: they 484 vs me 405; strawberry sold: they 115 vs me 124; milk sold: they 110 vs me 118 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 3 | 1 | 0 |
| 16622198 | 3 | 4 | 0 |
| 16622349 | 2 | 5 | 0 |
| 16622459 | 2 | 0 | 1 |
| 16626191 | 2 | 3 | 1 |
| 16633100 | 2 | 2 | 0 |
| 16633178 | 2 | 0 | 0 |
| 16633944 | 3 | 2 | 0 |
| 16637255 | 1 | 4 | 0 |
| 16641710 | 4 | 4 | 0 |
| 16644724 | 3 | 6 | 0 |
| 16655383 | 1 | 2 | 0 |
| 16658554 | 0 | 2 | 0 |
| 16660726 | 2 | 0 | 1 |
| 16664246 | 0 | 1 | 0 |
| 16671741 | 5 | 3 | 0 |
| 16675778 | 1 | 0 | 0 |
| 16683936 | 3 | 3 | 2 |
| 16684093 | 1 | 1 | 1 |
| 16719123 | 2 | 7 | 1 |
| 16723379 | 4 | 1 | 0 |
| 16725899 | 4 | 0 | 0 |
| 16728071 | 2 | 10 | 0 |
| 16730524 | 2 | 8 | 0 |
| 16730761 | 1 | 3 | 0 |
| 16731186 | 2 | 4 | 0 |
| 16731275 | 1 | 0 | 0 |
| 16732403 | 2 | 1 | 0 |
| 16732521 | 1 | 2 | 0 |
| 16732748 | 2 | 0 | 0 |
| 16741542 | 0 | 3 | 0 |
| 16758882 | 0 | 2 | 0 |
| 16761744 | 0 | 2 | 0 |
| 16773026 | 1 | 1 | 0 |
| 16777134 | 0 | 2 | 2 |
| 16781445 | 1 | 1 | 0 |
| 16805699 | 0 | 1 | 0 |
| 16810299 | 0 | 1 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 0 | 2 | 0 |
| 16879253 | 0 | 1 | 1 |
| 16880773 | 1 | 1 | 0 |
| 16888254 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 109015934, 109016963, 109017972, 109019025, 109020044, 109021061, 109022097, 109023112, 109024133, 109025169, 109026196, 109027230, 109028256, 109028470, 109029289, 109030315, 109031371, 109032431, 109033203, 109033450, 109034514, 109035554, 109036595, 109037625, 109038655, 109039689, 109040123, 109040728, 109041770, 109042796, 109043836, 109044861, 109045033, 109045903, 109046944, 109047441, 109047979, 109048040, 109048357, 109049029, 109050053, 109051100, 109052144, 109053172, 109054211, 109055242, 109056277, 109057316, 109058365, 109059410
