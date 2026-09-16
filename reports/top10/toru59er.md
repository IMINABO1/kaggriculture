# Toru59er (rank 881, score 2470.2, bronze)

- team id 16633944; current submission 56240612 (151 public games)
- 60 submissions found; 9436 public games from 2026-08-01 to 2026-09-15; 106 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 31-9-10 | 62 | 111330.5 | 110979.5 | 2077.6 | 46 | 1.32.7 | 2026-09-14 | 2026-09-15 |

## Rating path of the current submission

game 1: 663, game 10: 1497, game 25: 2555, game 50: 2542, game 100: 2520, game last: 2472

![rating](figs/toru59er_rating.png)

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
| FERTILIZE ops | 103 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 133 |
| milk sold | 124 |
| wool sold | 89.5 |
| wheat sold | 327 |
| fertilizer sold | 291 |
| units sold last 3 days | 269.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/toru59er_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 3 (96%) | 3 (96%) | 3 (96%) | 7 (74%) | 13 (50%) | 32 (10%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 8 (76%) | 12 (52%) | 28 (16%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 3 (96%) | 3 (96%) | 3 (96%) | 9 (74%) | 13 (50%) | 31 (14%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (96%), then branching (3 lines at turn 136, 32 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (98%), then branching (2 lines at turn 136, 28 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (96%), then branching (3 lines at turn 136, 31 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 49 | 98 |
| 48 | 2 | 3 | 48 | 96 |
| 100 | 4 | 3 | 48 | 96 |
| 136 | 5 | 3 | 48 | 96 |
| 200 | 8 | 7 | 37 | 74 |
| 300 | 12 | 13 | 25 | 50 |
| 400 | 16 | 32 | 5 | 10 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 3 | 100 | 21.3 |
| opponent off its modal line at turn 136 | 29 | 27.6 | 23.8 |
| played seat 1 | 27 | 18.5 | 34.8 |
| lost the game | 9 | 11.1 | 29.3 |
| first shop (day 3) is not Farmers Market | 41 | 26.8 | 22.2 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 62 | 111330.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 124 | 89.5 | 32 | 28 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109109703 | Sōsuke Aizen | 2643.7 | 78534 | 78543 | -9 | 9b0c82fd |  |
| C0 | 109110744 | Asem Adnan | 2456.9 | 111870 | 113550 | -1680 | 9b0c82fd | milk sold: they 146 vs me 173; FERTILIZE ops: they 123 vs me 107; CARE ops: they 405 vs me 417 |
| C0 | 109114444 | Aurora | 2569.9 | 97721 | 100654 | -2933 | 9b0c82fd | milk sold: they 75 vs me 125; wool sold: they 43 vs me 56; units sold last 3 days: they 260 vs me 270 |
| C0 | 109121179 | ShoaibSSM | 2582.2 | 66347 | 66397 | -50 | 9b0c82fd | weeds spawned: they 21 vs me 20 |
| C0 | 109121305 | TS | 2602.2 | 87637 | 88017 | -380 | a6a57513 | milk sold: they 105 vs me 154; CARE ops: they 405 vs me 417; strawberry sold: they 123 vs me 132 |
| C0 | 109123463 | Seho.Connect | 2590.6 | 123701 | 124425 | -724 | 9b0c82fd | milk sold: they 96 vs me 134; FERTILIZE ops: they 122 vs me 103; units sold last 3 days: they 260 vs me 246 |
| C0 | 109124561 | MAGMA | 2584.7 | 78743 | 78755 | -12 | 9b0c82fd | weeds spawned: they 20 vs me 19 |
| C0 | 109130440 | winstonton | 2606.9 | 113045 | 114100 | -1055 | 9b0c82fd | strawberry sold: they 139 vs me 133; milk sold: they 118 vs me 113; wool sold: they 113 vs me 112 |
| C0 | 109131440 | Shadowfishes | 2602.7 | 91814 | 91826 | -12 | 9b0c82fd | weeds spawned: they 19 vs me 20 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16622198 | 2 | 5 | 2 |
| 16622349 | 3 | 8 | 0 |
| 16622459 | 1 | 1 | 1 |
| 16626191 | 4 | 9 | 0 |
| 16633100 | 0 | 1 | 1 |
| 16633178 | 1 | 0 | 0 |
| 16637255 | 4 | 8 | 1 |
| 16640510 | 1 | 3 | 0 |
| 16641710 | 3 | 6 | 1 |
| 16644724 | 5 | 14 | 1 |
| 16655383 | 1 | 2 | 2 |
| 16657100 | 2 | 3 | 0 |
| 16660726 | 4 | 7 | 0 |
| 16664246 | 1 | 0 | 0 |
| 16671741 | 0 | 6 | 0 |
| 16683936 | 0 | 1 | 2 |
| 16684093 | 6 | 4 | 2 |
| 16690867 | 1 | 0 | 0 |
| 16706321 | 1 | 1 | 0 |
| 16718819 | 0 | 1 | 0 |
| 16719123 | 1 | 7 | 1 |
| 16723379 | 2 | 4 | 0 |
| 16725899 | 1 | 2 | 0 |
| 16728071 | 3 | 9 | 0 |
| 16730524 | 2 | 4 | 1 |
| 16730720 | 0 | 0 | 1 |
| 16730761 | 1 | 5 | 1 |
| 16731186 | 1 | 6 | 0 |
| 16731275 | 1 | 0 | 0 |
| 16732403 | 1 | 1 | 1 |
| 16732521 | 2 | 2 | 2 |
| 16732748 | 2 | 8 | 0 |
| 16741542 | 1 | 2 | 0 |
| 16758882 | 3 | 1 | 0 |
| 16765807 | 1 | 0 | 0 |
| 16773026 | 1 | 3 | 0 |
| 16777134 | 2 | 3 | 0 |
| 16781445 | 2 | 0 | 0 |
| 16802867 | 1 | 1 | 1 |
| 16805699 | 1 | 1 | 0 |
| 16809332 | 1 | 0 | 0 |
| 16810299 | 0 | 0 | 1 |
| 16811307 | 1 | 0 | 0 |
| 16845367 | 1 | 1 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 2 | 0 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16880773 | 0 | 2 | 0 |
| 16888254 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 109081099, 109082258, 109083476, 109084769, 109086003, 109087393, 109088649, 109089877, 109090979, 109092207, 109093295, 109094431, 109095751, 109097104, 109098229, 109099515, 109100549, 109101839, 109103108, 109104157, 109105298, 109106327, 109107414, 109108012, 109108548, 109109703, 109110744, 109112022, 109113312, 109114444, 109115502, 109116721, 109117844, 109118971, 109120050, 109121179, 109121305, 109122215, 109123445, 109123463, 109124561, 109125811, 109126902, 109127358, 109128031, 109129139, 109130325, 109130440, 109131440, 109132547
