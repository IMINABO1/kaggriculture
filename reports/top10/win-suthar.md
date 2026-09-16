# Win Suthar (rank 401, score 2674.8, silver)

- team id 16765807; current submission 56229200 (191 public games)
- 8 submissions found; 1845 public games from 2026-09-09 to 2026-09-15; 26 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 43-4-3 | 86 | 105322.5 | 105588.3 | 1938.1 | 48 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 730, game 10: 1620, game 25: 2211, game 50: 2410, game 100: 2536, game last: 2440

![rating](figs/win-suthar_rating.png)

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
| FERTILIZE ops | 102.5 |
| CARE ops | 417 |
| melon sold | 72 |
| strawberry sold | 247 |
| milk sold | 197 |
| wool sold | 130 |
| wheat sold | 373 |
| fertilizer sold | 350 |
| units sold last 3 days | 395.5 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/win-suthar_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 9 (66%) | 13 (44%) | 38 (8%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 6 (72%) | 12 (46%) | 26 (16%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (98%) | 2 (98%) | 2 (98%) | 2 (98%) | 10 (66%) | 14 (44%) | 37 (8%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (98%), then branching (2 lines at turn 136, 38 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (98%), then branching (2 lines at turn 136, 26 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (98%), then branching (2 lines at turn 136, 37 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 49 | 98 |
| 48 | 2 | 2 | 49 | 98 |
| 100 | 4 | 2 | 49 | 98 |
| 136 | 5 | 2 | 49 | 98 |
| 200 | 8 | 9 | 33 | 66 |
| 300 | 12 | 13 | 22 | 44 |
| 400 | 16 | 38 | 4 | 8 |
| 719 | 29 | 50 | 1 | 2 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 4 | 100 | 28.3 |
| opponent off its modal line at turn 136 | 34 | 35.3 | 31.2 |
| played seat 1 | 26 | 38.5 | 29.2 |
| lost the game | 4 | 75 | 30.4 |
| first shop (day 3) is not Yarn Store | 41 | 19.5 | 100 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 86 | 105322.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 72 | 197 | 130 | 38 | 26 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 108893823 | Snorlax | 1637.1 | 105770 | 106308 | -538 | cfefcbaa | milk sold: they 263 vs me 205; wool sold: they 139 vs me 102; CARE ops: they 399 vs me 417 |
| C0 | 108910591 | parv goyal2 | 2280.3 | 83628 | 87673 | -4045 | 422a8637 | CARE ops: they 267 vs me 417; FERTILIZE ops: they 147 vs me 83; wool sold: they 75 vs me 129 |
| C0 | 108916853 | Eesh saxena | 2344.8 | 115821 | 119071 | -3250 | 9b0c82fd | wool sold: they 272 vs me 254; FERTILIZE ops: they 100 vs me 92; units sold last 3 days: they 393 vs me 390 |
| C0 | 108925173 | Tavuk Master | 2476.4 | 110854 | 112994 | -2140 | 9b0c82fd | CARE ops: they 405 vs me 417; FERTILIZE ops: they 124 vs me 115; units sold last 3 days: they 386 vs me 388 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16626191 | 0 | 1 | 0 |
| 16633100 | 1 | 1 | 0 |
| 16633178 | 0 | 1 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16641710 | 1 | 0 | 0 |
| 16655383 | 2 | 0 | 0 |
| 16671741 | 0 | 2 | 0 |
| 16683936 | 0 | 2 | 0 |
| 16684093 | 0 | 1 | 0 |
| 16690867 | 0 | 2 | 0 |
| 16706321 | 0 | 3 | 0 |
| 16719123 | 0 | 2 | 0 |
| 16725899 | 0 | 1 | 0 |
| 16728071 | 0 | 1 | 0 |
| 16730612 | 0 | 1 | 0 |
| 16731186 | 1 | 0 | 0 |
| 16731275 | 0 | 2 | 0 |
| 16732748 | 0 | 2 | 0 |
| 16758882 | 0 | 1 | 0 |
| 16760569 | 1 | 0 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16802867 | 0 | 0 | 1 |
| 16809332 | 1 | 2 | 0 |
| 16810299 | 0 | 1 | 0 |
| 16833141 | 0 | 1 | 0 |
| 16848479 | 0 | 3 | 0 |
| 16848532 | 1 | 1 | 0 |
| 16888254 | 0 | 0 | 1 |
| 16891058 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 108883922, 108884913, 108885930, 108886939, 108886966, 108887970, 108888982, 108890002, 108890759, 108891769, 108892791, 108893537, 108893823, 108894869, 108895912, 108896969, 108898073, 108899086, 108899497, 108900165, 108901225, 108902278, 108902808, 108903304, 108904370, 108905405, 108906457, 108907505, 108908542, 108909585, 108910591, 108911652, 108912687, 108913728, 108914764, 108915817, 108916853, 108917904, 108918949, 108919981, 108921019, 108922055, 108923079, 108924133, 108925173, 108926219, 108927269, 108928307, 108929351, 108930396
