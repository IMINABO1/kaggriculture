# Pai (rank 121, score 2820.2, silver)

- team id 16658554; current submission 56234285 (165 public games)
- 16 submissions found; 3386 public games from 2026-08-29 to 2026-09-15; 16 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 43-7-0 | 86 | 94496 | 100988.9 | 2268.4 | 42 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 713, game 10: 1622, game 25: 2649, game 50: 2836, game 100: 2883, game last: 2817

![rating](figs/pai_rating.png)

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
| FERTILIZE ops | 116 |
| CARE ops | 405 |
| melon sold | 12 |
| strawberry sold | 128 |
| milk sold | 105 |
| wool sold | 57.5 |
| wheat sold | 342 |
| fertilizer sold | 280 |
| units sold last 3 days | 271.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/pai_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 8 (46%) | 18 (26%) | 37 (12%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 9 (46%) | 19 (26%) | 37 (16%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 10 (46%) | 20 (26%) | 38 (12%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 37 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 37 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 38 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 8 | 23 | 46 |
| 300 | 12 | 18 | 13 | 26 |
| 400 | 16 | 37 | 6 | 12 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 1 | 100 | 53.1 |
| opponent off its modal line at turn 136 | 22 | 59.1 | 50 |
| played seat 1 | 29 | 48.3 | 61.9 |
| lost the game | 7 | 57.1 | 53.5 |
| first shop (day 3) is not Smoothie Shop | 40 | 62.5 | 20 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 86 | 94496 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 105 | 57.5 | 37 | 37 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108986102 | 芳村 愛支 | 2775.3 | 83894 | 84219 | -325 | 9b0c82fd | strawberry sold: they 121 vs me 124; units sold last 3 days: they 267 vs me 270; milk sold: they 98 vs me 96 |
| C0 | 108989273 | yuto083 | 2831.0 | 120396 | 132109 | -11713 | 9b0c82fd | milk sold: they 123 vs me 73; FERTILIZE ops: they 89 vs me 122; wool sold: they 93 vs me 78 |
| C0 | 108989568 | maco-macoo | 2790.2 | 90477 | 93269 | -2792 | 9b0c82fd | strawberry sold: they 103 vs me 125; wool sold: they 118 vs me 131; milk sold: they 75 vs me 79 |
| C0 | 108993391 | carlos-tagosaku | 2768.8 | 90852 | 92249 | -1397 | 9b0c82fd | strawberry sold: they 148 vs me 129; FERTILIZE ops: they 127 vs me 113; CARE ops: they 417 vs me 405 |
| C0 | 108997559 | Weverton Guedes | 2742.9 | 93299 | 93845 | -546 | 9b0c82fd |  |
| C0 | 108998582 | Driz Lo | 2897.6 | 93140 | 95061 | -1921 | 9b0c82fd | weeds spawned: they 30 vs me 19; CARE ops: they 400 vs me 405; FERTILIZE ops: they 117 vs me 122 |
| C0 | 108999644 | Utkarsh #2 | 2850.9 | 81496 | 82125 | -629 | 9b0c82fd | strawberry sold: they 97 vs me 98 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 1 | 0 |
| 16622198 | 1 | 2 | 0 |
| 16622459 | 1 | 2 | 0 |
| 16626191 | 1 | 0 | 0 |
| 16633100 | 1 | 1 | 0 |
| 16637255 | 0 | 3 | 0 |
| 16640467 | 0 | 1 | 0 |
| 16640510 | 2 | 0 | 0 |
| 16641710 | 0 | 2 | 0 |
| 16644724 | 0 | 2 | 0 |
| 16655383 | 3 | 2 | 0 |
| 16657100 | 2 | 0 | 0 |
| 16660726 | 0 | 1 | 0 |
| 16664246 | 3 | 2 | 0 |
| 16671741 | 0 | 1 | 0 |
| 16675778 | 0 | 1 | 0 |
| 16684093 | 3 | 3 | 0 |
| 16706321 | 0 | 5 | 0 |
| 16719123 | 1 | 1 | 0 |
| 16725899 | 0 | 1 | 0 |
| 16728071 | 1 | 2 | 0 |
| 16730612 | 1 | 1 | 0 |
| 16730761 | 1 | 2 | 0 |
| 16731186 | 0 | 1 | 0 |
| 16731275 | 1 | 1 | 0 |
| 16732403 | 0 | 1 | 0 |
| 16732521 | 0 | 6 | 0 |
| 16732748 | 0 | 2 | 0 |
| 16741542 | 1 | 2 | 0 |
| 16758882 | 0 | 1 | 1 |
| 16760569 | 1 | 1 | 0 |
| 16773026 | 2 | 1 | 0 |
| 16777134 | 3 | 5 | 0 |
| 16778640 | 3 | 1 | 0 |
| 16781445 | 0 | 2 | 0 |
| 16805699 | 0 | 1 | 0 |
| 16810299 | 1 | 0 | 0 |
| 16811307 | 1 | 6 | 0 |
| 16833141 | 0 | 2 | 0 |
| 16845367 | 1 | 1 | 0 |
| 16848479 | 1 | 1 | 0 |
| 16848532 | 2 | 0 | 0 |
| 16858228 | 1 | 3 | 0 |
| 16879253 | 1 | 1 | 0 |
| 16880773 | 1 | 0 | 0 |
| 16888254 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108953971, 108955044, 108955987, 108957020, 108958041, 108959079, 108960077, 108960778, 108961141, 108962131, 108963174, 108964216, 108965219, 108966247, 108967280, 108968313, 108969399, 108970328, 108970452, 108971536, 108972572, 108973613, 108974675, 108975700, 108977237, 108977808, 108978848, 108979885, 108980921, 108981951, 108982981, 108983366, 108984018, 108985060, 108986102, 108987126, 108988178, 108989273, 108989568, 108990272, 108991325, 108992361, 108993391, 108994436, 108995494, 108996518, 108997559, 108998582, 108998637, 108999644
