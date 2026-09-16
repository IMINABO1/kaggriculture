# THIRD FARM CLUB (rank 6, score 3009.0, gold)

- team id 16730524; current submission 56216318 (236 public games)
- 59 submissions found; 7775 public games from 2026-08-18 to 2026-09-15; 94 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 48-2-0 | 96 | 117769 | 119084.3 | 1837.5 | 50 | 1.32.7 | 2026-09-13 | 2026-09-14 |

## Rating path of the current submission

game 1: 699, game 10: 1370, game 25: 2136, game 50: 2434, game 100: 2688, game 200: 2977, game last: 3009

![rating](figs/third-farm-club_rating.png)

## Farm plan by window (median per game)

| median per game | C0 |
|---|---|
| hands (peak) | 13 |
| quadrants | 3 |
| land day 1 | 6 |
| land day 2 | 9 |
| cows bought | 10 |
| sheep bought | 4 |
| geese bought | 5.5 |
| first cow day | 0 |
| wheat planted | 133.5 |
| carrot planted | 45.5 |
| tomato planted | 10 |
| strawberry planted | 32.5 |
| melon planted | 15 |
| FERTILIZE ops | 184.5 |
| CARE ops | 324 |
| melon sold | 87 |
| strawberry sold | 209 |
| milk sold | 175 |
| wool sold | 63 |
| wheat sold | 283 |
| fertilizer sold | 245 |
| units sold last 3 days | 446 |
| shed peak | 14 |
| weeds spawned | 14.5 |
| unexecutable market orders | 0 |

![money by day](figs/third-farm-club_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 2 (98%) | 2 (98%) | 2 (98%) | 24 (26%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 3 (96%) | 6 (84%) | 7 (82%) | 27 (26%) | 50 (2%) | 50 (2%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 1 (100%) | 3 (96%) | 4 (94%) | 4 (94%) | 25 (26%) | 50 (2%) | 50 (2%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 50 at turn 400); every game distinct by turn 300**; market is **one line through turn 48 (96%), then branching (7 lines at turn 136, 50 at turn 400); every game distinct by turn 300**; plan is **one line through turn 136 (94%), then branching (4 lines at turn 136, 50 at turn 400); every game distinct by turn 300**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 1 | 50 | 100 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 24 | 13 | 26 |
| 300 | 12 | 50 | 1 | 2 |
| 400 | 16 | 50 | 1 | 2 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 2 | 100 | 72.9 |
| opponent off its modal line at turn 136 | 22 | 86.4 | 64.3 |
| played seat 1 | 25 | 64 | 84 |
| lost the game | 2 | 50 | 75 |
| first shop (day 3) is not Farmers Market | 41 | 80.5 | 44.4 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 96 | 117769 | 13 | 10 | 4 | 5.5 | 3 | 6 | 32.5 | 133.5 | 15 | 87 | 175 | 63 | 50 | 50 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108718850 | Hikari_30 | 1592.7 | 89216 | 93923 | -4707 | 9b0c82fd | strawberry sold: they 246 vs me 144; CARE ops: they 417 vs me 327; wool sold: they 125 vs me 58 |
| C0 | 108740575 | elmo | 2371.7 | 95339 | 95758 | -419 | 9b0c82fd | strawberry sold: they 250 vs me 143; FERTILIZE ops: they 114 vs me 180; CARE ops: they 405 vs me 361 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 8 | 12 | 0 |
| 16622198 | 3 | 0 | 0 |
| 16622349 | 16 | 15 | 0 |
| 16622459 | 5 | 2 | 0 |
| 16626191 | 2 | 0 | 0 |
| 16633100 | 3 | 0 | 0 |
| 16633178 | 10 | 4 | 0 |
| 16633944 | 4 | 2 | 1 |
| 16637255 | 4 | 2 | 1 |
| 16640467 | 12 | 2 | 0 |
| 16640510 | 10 | 10 | 0 |
| 16641710 | 12 | 4 | 0 |
| 16644724 | 15 | 5 | 0 |
| 16655383 | 1 | 3 | 0 |
| 16657100 | 8 | 2 | 0 |
| 16660726 | 9 | 4 | 0 |
| 16664246 | 3 | 2 | 0 |
| 16671741 | 2 | 0 | 0 |
| 16675778 | 2 | 11 | 0 |
| 16683936 | 5 | 0 | 0 |
| 16684093 | 8 | 1 | 0 |
| 16690867 | 4 | 0 | 0 |
| 16706321 | 2 | 1 | 0 |
| 16718819 | 2 | 12 | 0 |
| 16719123 | 5 | 11 | 0 |
| 16723379 | 6 | 5 | 0 |
| 16725899 | 3 | 1 | 0 |
| 16728071 | 8 | 0 | 1 |
| 16730612 | 17 | 14 | 0 |
| 16730761 | 4 | 2 | 0 |
| 16731186 | 4 | 1 | 0 |
| 16731275 | 10 | 1 | 0 |
| 16732403 | 17 | 7 | 0 |
| 16732521 | 11 | 6 | 0 |
| 16732748 | 11 | 10 | 0 |
| 16741542 | 3 | 8 | 0 |
| 16758882 | 11 | 6 | 0 |
| 16760569 | 12 | 16 | 0 |
| 16773026 | 10 | 3 | 0 |
| 16777134 | 4 | 4 | 0 |
| 16778640 | 6 | 0 | 0 |
| 16781445 | 3 | 1 | 0 |
| 16805699 | 33 | 20 | 0 |
| 16810299 | 4 | 1 | 0 |
| 16811307 | 1 | 4 | 0 |
| 16833141 | 4 | 1 | 0 |
| 16845367 | 8 | 1 | 0 |
| 16848479 | 9 | 0 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 1 | 2 | 0 |
| 16879253 | 2 | 0 | 0 |
| 16880773 | 1 | 0 | 0 |
| 16882725 | 1 | 0 | 0 |

## Episodes behind each window

- **C0** (50): 108705603, 108706617, 108707637, 108708658, 108709670, 108710739, 108711696, 108712714, 108713723, 108714750, 108715791, 108716823, 108717241, 108717831, 108718850, 108719221, 108719889, 108720923, 108721986, 108723036, 108724053, 108725102, 108725806, 108726078, 108726896, 108727168, 108728192, 108729223, 108730253, 108730761, 108731299, 108732327, 108733349, 108733527, 108733747, 108734385, 108735416, 108736442, 108737468, 108738491, 108739511, 108740575, 108741606, 108741970, 108742755, 108743539, 108743679, 108744093, 108744719, 108745498
