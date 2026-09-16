# broccoli (rank 882, score 2470.0, bronze)

- team id 16730720; current submission 56228585 (205 public games)
- 1 submissions found; 205 public games from 2026-09-14 to 2026-09-15; 0 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 40-9-1 | 80 | 101990.5 | 104645.1 | 2020.8 | 52 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 750, game 10: 1664, game 25: 2287, game 50: 2468, game 100: 2574, game 200: 2456, game last: 2462

![rating](figs/broccoli_rating.png)

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
| FERTILIZE ops | 105.5 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 133 |
| milk sold | 123 |
| wool sold | 67.5 |
| wheat sold | 325.5 |
| fertilizer sold | 291 |
| units sold last 3 days | 268 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/broccoli_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 4 (92%) | 4 (92%) | 4 (92%) | 8 (80%) | 11 (56%) | 40 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 7 (82%) | 11 (56%) | 28 (14%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 3 (96%) | 4 (92%) | 4 (92%) | 4 (92%) | 8 (80%) | 11 (56%) | 37 (6%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (92%), then branching (4 lines at turn 136, 40 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (96%), then branching (3 lines at turn 136, 28 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (92%), then branching (4 lines at turn 136, 37 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 48 | 96 |
| 48 | 2 | 4 | 46 | 92 |
| 100 | 4 | 4 | 46 | 92 |
| 136 | 5 | 4 | 46 | 92 |
| 200 | 8 | 8 | 40 | 80 |
| 300 | 12 | 11 | 28 | 56 |
| 400 | 16 | 40 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 3 | 100 | 14.9 |
| opponent off its modal line at turn 136 | 32 | 12.5 | 33.3 |
| played seat 1 | 24 | 20.8 | 19.2 |
| lost the game | 9 | 33.3 | 17.1 |
| first shop (day 3) is not Pet Cafe | 42 | 19.0 | 25 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 80 | 101990.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 123 | 67.5 | 40 | 28 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108887985 | daulettoibazar | 2083.6 | 93168 | 94326 | -1158 | 9b0c82fd | wool sold: they 107 vs me 112; strawberry sold: they 137 vs me 141; milk sold: they 152 vs me 155 |
| C0 | 108890776 | Gigrise | 2287.2 | 110650 | 110911 | -261 | 9b0c82fd | milk sold: they 155 vs me 89; FERTILIZE ops: they 100 vs me 120; strawberry sold: they 150 vs me 133 |
| C0 | 108897051 | cm391 | 2306.8 | 110106 | 111426 | -1320 | 9b0c82fd | weeds spawned: they 19 vs me 20 |
| C0 | 108900199 | yt0914 | 2233.8 | 73631 | 77329 | -3698 | d6b925bb | strawberry sold: they 134 vs me 138; milk sold: they 106 vs me 109; wool sold: they 143 vs me 144 |
| C0 | 108900468 | yt0914 | 2243.7 | 95079 | 95247 | -168 | d6b925bb | wheat planted: they 161 vs me 162; weeds spawned: they 20 vs me 19 |
| C0 | 108904402 | Sadettin Şamil Verdil | 2392.6 | 102086 | 103977 | -1891 | 9b0c82fd | CARE ops: they 366 vs me 417; units sold last 3 days: they 238 vs me 264; wool sold: they 37 vs me 56 |
| C0 | 108904415 | hidenov | 2323.8 | 120064 | 124700 | -4636 | 9b0c82fd | CARE ops: they 400 vs me 417; milk sold: they 164 vs me 176; strawberry sold: they 122 vs me 133 |
| C0 | 108914845 | BOB | 2409.7 | 70961 | 71636 | -675 | 9b0c82fd | FERTILIZE ops: they 63 vs me 106; units sold last 3 days: they 241 vs me 276; milk sold: they 107 vs me 81 |
| C0 | 108917819 | CrazyML | 2428.4 | 64669 | 66559 | -1890 | 9b0c82fd | strawberry sold: they 138 vs me 136; units sold last 3 days: they 267 vs me 269; milk sold: they 110 vs me 109 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16633944 | 0 | 0 | 1 |
| 16655383 | 0 | 1 | 0 |
| 16684093 | 0 | 1 | 0 |
| 16802867 | 0 | 0 | 1 |
| 16810299 | 0 | 0 | 1 |
| 16833141 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108874640, 108874666, 108875642, 108876655, 108877663, 108878693, 108879214, 108879700, 108880728, 108881742, 108882761, 108883770, 108884781, 108885802, 108886836, 108887876, 108887985, 108888945, 108890776, 108891817, 108892886, 108893908, 108894967, 108895999, 108897051, 108898150, 108899160, 108900199, 108900468, 108901267, 108902329, 108903363, 108904402, 108904415, 108905464, 108906494, 108907539, 108908607, 108909640, 108910678, 108911719, 108912739, 108913356, 108913793, 108914845, 108915878, 108916924, 108917819, 108917970, 108918905
