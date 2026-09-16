# Ebi (rank 21, score 2949.2, gold)

- team id 16882725; current submission 56215426 (252 public games)
- 1 submissions found; 252 public games from 2026-09-13 to 2026-09-15; 0 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 42-8-0 | 84 | 106327 | 107087.9 | 2058.3 | 58 | 1.32.7 | 2026-09-13 | 2026-09-14 |

## Rating path of the current submission

game 1: 716, game 10: 1589, game 25: 2306, game 50: 2551, game 100: 2719, game 200: 2917, game last: 2960

![rating](figs/ebi_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 14 |
| quadrants | 3 |
| land day 1 | 5 |
| land day 2 | 8 |
| cows bought | 6 |
| sheep bought | 5.5 |
| geese bought | 4 |
| first cow day | 0 |
| wheat planted | 101 |
| carrot planted | 22.5 |
| tomato planted | 3.5 |
| strawberry planted | 32 |
| melon planted | 14 |
| FERTILIZE ops | 153 |
| CARE ops | 333 |
| melon sold | 84 |
| strawberry sold | 241 |
| milk sold | 181.5 |
| wool sold | 107 |
| wheat sold | 4530.5 |
| fertilizer sold | 266 |
| units sold last 3 days | 1060.5 |
| shed peak | 2 |
| weeds spawned | 15.5 |
| unexecutable market orders | 0 |

![money by day](figs/ebi_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 22 (24%) | 31 (12%) | 49 (4%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (78%) | 23 (22%) | 29 (12%) | 47 (4%) | 49 (4%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (78%) | 23 (22%) | 31 (12%) | 49 (4%) | 50 (2%) | 50 (2%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 48 (100%), then branching (31 lines at turn 136, 50 at turn 400); every game distinct by turn 300**; market is **one line through turn 24 (100%), then branching (29 lines at turn 136, 50 at turn 400); every game distinct by turn 400**; plan is **one line through turn 24 (100%), then branching (31 lines at turn 136, 50 at turn 400); every game distinct by turn 300**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 1 | 50 | 100 |
| 100 | 4 | 22 | 12 | 24 |
| 136 | 5 | 31 | 6 | 12 |
| 200 | 8 | 49 | 2 | 4 |
| 300 | 12 | 50 | 1 | 2 |
| 400 | 16 | 50 | 1 | 2 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 100 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 4 | 0 |  | 76 |
| opponent off its modal line at turn 48 | 15 | 93.3 | 68.6 |
| played seat 1 | 21 | 85.7 | 69.0 |
| lost the game | 8 | 62.5 | 78.6 |
| first shop (day 3) is not Bakery | 41 | 73.2 | 88.9 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 84 | 106327 | 14 | 6 | 5.5 | 4 | 3 | 5 | 32 | 101 | 14 | 84 | 181.5 | 107 | 50 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108699094 | Suneeth reddy | 2063.0 | 96880 | 98224 | -1344 | 9b0c82fd | units sold last 3 days: they 374 vs me 1457; milk sold: they 284 vs me 180; CARE ops: they 416 vs me 330 |
| C0 | 108701495 | DieByTheSword | 2313.5 | 83890 | 84331 | -441 | 9b0c82fd | units sold last 3 days: they 362 vs me 1116; milk sold: they 245 vs me 138; FERTILIZE ops: they 61 vs me 146 |
| C0 | 108702542 | yukino | 2249.4 | 95861 | 99110 | -3249 | 9b0c82fd | units sold last 3 days: they 366 vs me 475; wool sold: they 161 vs me 61; FERTILIZE ops: they 61 vs me 141 |
| C0 | 108718018 | Abhijit Pise | 2558.0 | 108657 | 123827 | -15170 | 9b0c82fd | wool sold: they 160 vs me 107; wheat planted: they 163 vs me 114; strawberry sold: they 248 vs me 287 |
| C0 | 108721101 | TIM | 2633.8 | 98227 | 98318 | -91 | 9b0c82fd | wheat planted: they 163 vs me 63; CARE ops: they 405 vs me 340; wool sold: they 161 vs me 207 |
| C0 | 108722173 | Shiji Zheng | 2574.7 | 85078 | 87377 | -2299 | 9b0c82fd | units sold last 3 days: they 422 vs me 1317; CARE ops: they 417 vs me 297; strawberry sold: they 248 vs me 175 |
| C0 | 108724196 | Vanshika #2 | 2539.5 | 106560 | 107807 | -1247 | 9b0c82fd | units sold last 3 days: they 426 vs me 1080; strawberry sold: they 249 vs me 167; CARE ops: they 525 vs me 467 |
| C0 | 108728288 | 洛希边际 | 2543.9 | 95934 | 96385 | -451 | 9b0c82fd | units sold last 3 days: they 375 vs me 1320; CARE ops: they 417 vs me 270; strawberry sold: they 248 vs me 353 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 2 | 0 |
| 16622198 | 1 | 0 | 0 |
| 16622349 | 2 | 1 | 0 |
| 16622459 | 0 | 1 | 0 |
| 16626191 | 1 | 0 | 0 |
| 16633100 | 0 | 2 | 0 |
| 16633178 | 2 | 1 | 0 |
| 16637255 | 0 | 1 | 0 |
| 16640467 | 0 | 1 | 0 |
| 16640510 | 2 | 1 | 0 |
| 16641710 | 2 | 0 | 0 |
| 16644724 | 0 | 1 | 0 |
| 16675778 | 0 | 1 | 0 |
| 16684093 | 1 | 0 | 0 |
| 16690867 | 1 | 0 | 0 |
| 16706321 | 2 | 0 | 0 |
| 16723379 | 1 | 1 | 0 |
| 16730524 | 0 | 1 | 0 |
| 16730612 | 1 | 1 | 0 |
| 16731275 | 1 | 0 | 0 |
| 16732521 | 2 | 1 | 0 |
| 16732748 | 0 | 1 | 0 |
| 16760569 | 0 | 5 | 0 |
| 16773026 | 1 | 1 | 0 |
| 16777134 | 1 | 0 | 0 |
| 16778640 | 1 | 0 | 0 |
| 16781445 | 3 | 1 | 0 |
| 16805699 | 1 | 0 | 0 |
| 16811307 | 1 | 0 | 0 |
| 16833141 | 2 | 0 | 0 |
| 16845367 | 3 | 1 | 0 |
| 16848479 | 2 | 1 | 0 |
| 16858228 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108684240, 108685246, 108686268, 108687293, 108688292, 108689290, 108690304, 108691326, 108692333, 108693345, 108694347, 108695364, 108696378, 108696849, 108697401, 108698412, 108699094, 108699442, 108700477, 108701495, 108701536, 108702542, 108703567, 108704608, 108705642, 108706680, 108707673, 108708707, 108709736, 108710752, 108711779, 108712796, 108712910, 108713825, 108714498, 108714840, 108715946, 108716981, 108718018, 108719039, 108720077, 108720214, 108721101, 108722173, 108723166, 108724196, 108725208, 108726140, 108727271, 108728288
