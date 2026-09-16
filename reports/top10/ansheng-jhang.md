# ansheng jhang (rank 751, score 2526.4, bronze)

- team id 16809332; current submission 56241164 (127 public games)
- 10 submissions found; 1880 public games from 2026-09-09 to 2026-09-15; 12 of them with a known rating
- sampled games with a replay: 50

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 45-5-0 | 90 | 113235.5 | 112863.9 | 2008.0 | 40 | 1.32.7 | 2026-09-15 | 2026-09-15 |

## Rating path of the current submission

game 1: 730, game 10: 1666, game 25: 2228, game 50: 2483, game 100: 2535, game last: 2533

![rating](figs/ansheng-jhang_rating.png)

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
| FERTILIZE ops | 99 |
| CARE ops | 417 |
| melon sold | 12 |
| strawberry sold | 134 |
| milk sold | 128.5 |
| wool sold | 97 |
| wheat sold | 316.5 |
| fertilizer sold | 291 |
| units sold last 3 days | 267 |
| shed peak | 45 |
| weeds spawned | 19 |
| unexecutable market orders | 1 |

![money by day](figs/ansheng-jhang_money.png)

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (96%) | 3 (94%) | 3 (94%) | 3 (94%) | 10 (66%) | 17 (48%) | 37 (12%) | 49 (4%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (96%) | 2 (96%) | 2 (96%) | 2 (96%) | 10 (68%) | 17 (50%) | 29 (16%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 2 (96%) | 3 (94%) | 3 (94%) | 3 (94%) | 12 (66%) | 18 (48%) | 38 (12%) | 50 (2%) |

Current submission (50 sampled games): field is **one line through turn 136 (94%), then branching (3 lines at turn 136, 37 at turn 400)**; market is **one line through turn 136 (96%), then branching (2 lines at turn 136, 29 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (94%), then branching (3 lines at turn 136, 38 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 2 | 48 | 96 |
| 48 | 2 | 3 | 47 | 94 |
| 100 | 4 | 3 | 47 | 94 |
| 136 | 5 | 3 | 47 | 94 |
| 200 | 8 | 10 | 33 | 66 |
| 300 | 12 | 17 | 24 | 48 |
| 400 | 16 | 37 | 6 | 12 |
| 719 | 29 | 49 | 2 | 4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 2 | 100 | 31.2 |
| opponent off its modal line at turn 136 | 33 | 42.4 | 17.6 |
| played seat 1 | 30 | 23.3 | 50 |
| lost the game | 5 | 0 | 37.8 |
| first shop (day 3) is not Bakery | 37 | 32.4 | 38.5 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 50 | 90 | 113235.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 12 | 128.5 | 97 | 37 | 29 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| C0 | 109099516 | HojunLee | 1916.8 | 92318 | 96108 | -3790 | 9b0c82fd | CARE ops: they 407 vs me 417; units sold last 3 days: they 274 vs me 266; wool sold: they 50 vs me 56 |
| C0 | 109103115 | Le Viet | 1933.3 | 96121 | 97568 | -1447 | 9b0c82fd | milk sold: they 124 vs me 144; units sold last 3 days: they 271 vs me 257; strawberry sold: they 120 vs me 132 |
| C0 | 109106924 | try | 2020.3 | 120647 | 125508 | -4861 | b3aed51d | milk sold: they 175 vs me 133; FERTILIZE ops: they 89 vs me 116; units sold last 3 days: they 249 vs me 263 |
| C0 | 109121256 | Bruce | 2427.0 | 86400 | 86557 | -157 | 9b0c82fd | weeds spawned: they 20 vs me 19 |
| C0 | 109135976 | ALLAI | 2523.5 | 119481 | 120039 | -558 | 9b0c82fd | milk sold: they 155 vs me 176; FERTILIZE ops: they 122 vs me 103; wool sold: they 71 vs me 83 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 1 | 0 |
| 16622459 | 1 | 0 | 0 |
| 16626191 | 0 | 1 | 0 |
| 16633100 | 1 | 0 | 0 |
| 16633178 | 0 | 1 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 0 | 2 | 0 |
| 16671741 | 0 | 1 | 0 |
| 16683936 | 0 | 1 | 0 |
| 16706321 | 1 | 1 | 0 |
| 16725899 | 0 | 1 | 0 |
| 16732748 | 0 | 1 | 0 |
| 16741542 | 0 | 2 | 0 |
| 16758882 | 0 | 1 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16765807 | 2 | 1 | 0 |
| 16773026 | 0 | 1 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16810299 | 1 | 0 | 0 |
| 16811307 | 1 | 1 | 0 |
| 16848532 | 2 | 1 | 0 |
| 16858228 | 0 | 2 | 0 |
| 16862666 | 0 | 1 | 0 |
| 16879253 | 0 | 1 | 0 |
| 16880773 | 0 | 1 | 0 |
| 16891058 | 0 | 1 | 0 |

## Episodes behind each window

- **C0** (50): 109086083, 109087440, 109088697, 109089911, 109091024, 109092236, 109093319, 109093549, 109094455, 109095764, 109097135, 109098230, 109099516, 109100550, 109101909, 109103115, 109104160, 109105327, 109106376, 109106924, 109107430, 109108571, 109109196, 109109723, 109110785, 109112075, 109113370, 109114489, 109115555, 109116778, 109116825, 109117913, 109118452, 109119047, 109120130, 109121256, 109122318, 109123524, 109124642, 109125896, 109127010, 109128112, 109129222, 109130402, 109131001, 109131514, 109132637, 109133750, 109134865, 109135976
