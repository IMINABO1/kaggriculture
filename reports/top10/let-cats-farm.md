# let cats farm (rank 251, score 2734.4, silver)

- team id 16741542; current submission 56191450 (403 public games)
- 63 submissions found; 7506 public games from 2026-08-23 to 2026-09-15; 47 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 48-2-0 | 96 | 100482.5 | 105861.6 | 2029.8 | 40 | 1.32.7 | 2026-09-12 | 2026-09-12 |

## Rating path of the current submission

game 1: 720, game 10: 1497, game 25: 2321, game 50: 2691, game 100: 2832, game 200: 2838, game last: 2747

![rating](figs/let-cats-farm_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 12 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 11 |
| cows bought | 8 |
| sheep bought | 6 |
| geese bought | 2 |
| first cow day | 0 |
| wheat planted | 163 |
| carrot planted | 31 |
| tomato planted | 0 |
| strawberry planted | 33 |
| melon planted | 12 |
| FERTILIZE ops | 95 |
| CARE ops | 338 |
| melon sold | 72 |
| strawberry sold | 249 |
| milk sold | 191.5 |
| wool sold | 125 |
| wheat sold | 579 |
| fertilizer sold | 343 |
| units sold last 3 days | 375 |
| shed peak | 59 |
| weeds spawned | 20 |
| unexecutable market orders | 193 |

![money by day](figs/let-cats-farm_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 6 (54%) | 12 (28%) | 34 (10%) | 49 (4%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 11 (46%) | 26 (14%) | 47 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 9 (50%) | 21 (24%) | 40 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 34 at turn 400)**; market is **one line through turn 136 (100%), then branching (1 lines at turn 136, 47 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 40 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 6 | 27 | 54 |
| 300 | 12 | 12 | 14 | 28 |
| 400 | 16 | 34 | 5 | 10 |
| 719 | 29 | 49 | 2 | 4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 2 | 100 | 43.8 |
| opponent off its modal line at turn 136 | 41 | 48.8 | 33.3 |
| played seat 1 | 30 | 46.7 | 45 |
| lost the game | 2 | 100 | 43.8 |
| first shop (day 3) is not Pizza Shop | 40 | 50 | 30 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 96 | 100482.5 | 12 | 8 | 6 | 2 | 3 | 6 | 33 | 163 | 12 | 72 | 191.5 | 125 | 34 | 47 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108287792 | ultimatum_game | 1939.0 | 111027 | 123141 | -12114 | 9b0c82fd | milk sold: they 391 vs me 250; CARE ops: they 392 vs me 353; FERTILIZE ops: they 64 vs me 89 |
| C0 | 108305009 | 薄荷喵呜 | 2575.7 | 98727 | 105014 | -6287 | e41e7f8e | CARE ops: they 386 vs me 335; wool sold: they 324 vs me 279; milk sold: they 101 vs me 128 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 1 | 2 | 0 |
| 16622198 | 6 | 1 | 0 |
| 16622349 | 7 | 18 | 0 |
| 16622459 | 6 | 1 | 0 |
| 16626191 | 0 | 3 | 0 |
| 16633100 | 5 | 0 | 0 |
| 16633178 | 1 | 1 | 0 |
| 16633944 | 2 | 1 | 0 |
| 16637255 | 15 | 5 | 0 |
| 16640467 | 0 | 4 | 0 |
| 16640510 | 6 | 14 | 0 |
| 16641710 | 9 | 7 | 0 |
| 16644724 | 10 | 11 | 0 |
| 16655383 | 4 | 6 | 0 |
| 16657100 | 3 | 0 | 0 |
| 16658554 | 2 | 1 | 0 |
| 16660726 | 11 | 11 | 0 |
| 16664246 | 3 | 1 | 0 |
| 16675778 | 1 | 0 | 0 |
| 16683936 | 5 | 1 | 0 |
| 16684093 | 12 | 4 | 0 |
| 16690867 | 0 | 9 | 0 |
| 16718819 | 1 | 1 | 0 |
| 16719123 | 9 | 7 | 0 |
| 16723379 | 5 | 5 | 0 |
| 16725899 | 4 | 2 | 0 |
| 16728071 | 11 | 11 | 0 |
| 16730524 | 8 | 3 | 0 |
| 16730612 | 3 | 2 | 0 |
| 16730761 | 10 | 5 | 0 |
| 16731186 | 4 | 10 | 0 |
| 16731275 | 3 | 10 | 0 |
| 16732403 | 5 | 20 | 0 |
| 16732521 | 7 | 8 | 0 |
| 16732748 | 2 | 2 | 0 |
| 16758882 | 11 | 8 | 0 |
| 16760569 | 1 | 3 | 0 |
| 16773026 | 4 | 1 | 0 |
| 16777134 | 7 | 0 | 0 |
| 16778640 | 0 | 1 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 14 | 9 | 0 |
| 16809332 | 2 | 0 | 0 |
| 16810299 | 3 | 0 | 0 |
| 16811307 | 6 | 4 | 0 |
| 16833141 | 2 | 2 | 0 |
| 16845367 | 2 | 2 | 0 |
| 16848479 | 2 | 3 | 0 |
| 16858228 | 2 | 1 | 0 |
| 16880773 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108272845, 108273846, 108274820, 108275834, 108276824, 108277820, 108278817, 108279801, 108280804, 108281798, 108282798, 108283790, 108284123, 108284789, 108285784, 108286789, 108287792, 108288797, 108289824, 108290839, 108291860, 108292875, 108293876, 108294901, 108295907, 108296922, 108297939, 108298938, 108299950, 108300963, 108301978, 108302989, 108304001, 108305009, 108306025, 108307037, 108308054, 108309057, 108310044, 108311075, 108312089, 108313103, 108314101, 108315117, 108316135, 108317150, 108318152, 108319167, 108319601, 108320176
