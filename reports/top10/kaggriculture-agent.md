# Kaggriculture Agent (rank 31, score 2912.0, next-15)

- team id 16644724; current submission 56230957 (116 public games)
- 76 submissions found; 8989 public games from 2026-07-31 to 2026-09-15; 89 of them with a known rating
- sampled games with a replay: 101

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 0-1-0 | 0 | 59081 | 59081 | 1140.1 | 100 | 1.32.2 | 2026-07-31 | 2026-07-31 |
| L | 50 | 40-10-0 | 80 | 95476 | 97707.6 | 2690.2 | 62 | 1.32.7 | 2026-09-14 | 2026-09-15 |
| C0 | 50 | 45-5-0 | 90 | 99096 | 104391.4 | 2250.5 | 64 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 715, game 10: 1608, game 25: 2658, game 50: 2873, game 100: 2917, game last: 2907

![rating](figs/kaggriculture-agent_rating.png)

## Farm plan by window (median per game)

| median per game | F | L | C0 |
|---|---|---|---|
| hands (peak) | 10 | 12 | 12 |
| quadrants | 2 | 3 | 3 |
| land day 1 | 11 | 6 | 6 |
| land day 2 |  | 11 | 11 |
| cows bought | 14 | 7.5 | 8 |
| sheep bought | 0 | 5 | 6 |
| geese bought | 0 | 4 | 3 |
| first cow day | 0 | 0 | 0 |
| wheat planted | 4 | 153 | 158 |
| carrot planted | 0 | 41 | 36 |
| tomato planted | 0 | 0 | 0 |
| strawberry planted | 2 | 33 | 33 |
| melon planted | 10 | 12 | 12 |
| FERTILIZE ops | 0 | 117 | 116 |
| CARE ops | 241 | 406 | 408 |
| melon sold | 48 | 12 | 12 |
| strawberry sold | 0 | 138.5 | 139 |
| milk sold | 307 | 142 | 154 |
| wool sold | 0 | 94 | 109 |
| wheat sold | 18 | 3949.5 | 3870.5 |
| fertilizer sold | 105 | 271 | 270 |
| units sold last 3 days | 77 | 585.5 | 569 |
| shed peak | 23 | 58 | 58 |
| weeds spawned | 13 | 20 | 20 |
| unexecutable market orders | 0 | 45 | 45 |

![money by day](figs/kaggriculture-agent_money.png)

## A typical recent game, day by day

Episode 109080085 (the median-bank game of the latest window): seat 0, bank 96400 vs 86191 (NonCaffeine), seed 871198338. Letters: W wheat, C carrot, T tomato, S strawberry, M melon, E egg, Mk milk, Wl wool, F fertilizer.

| day | money | hands | quads | bought | built | planted | care/fert | harvest | sold | revenue | farm at day end | new weeds | shop unlock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3000 | 5 | 1 | cow2 sheep2 \| W7 M12 | pasture 4  | W7 M12 | 3/0 | 0 | W14 | 405 | cow2 sheep2; W7 M12 |  |  |
| 1 | 12 | 3 | 1 |  | pasture 2  |  | 4/0 | 0 | W1 | 29 | cow2 sheep2; W7 M12; empty pens 2 |  |  |
| 2 | 102 | 4 | 1 | cow1 \| W3 |  | W3 | 5/0 | 3 | W1 F1 | 129 | cow3 sheep2; W7 M12; empty pens 1 |  |  |
| 3 | 185 | 5 | 1 | cow1 \| W4 |  | W4 | 6/0 | 4 | W3 | 90 | cow3 sheep2; W7 M12; empty pens 1 |  | Smoothie |
| 4 | 237 | 4 | 1 | W3 |  | W3 | 6/0 | 3 | W2 F1 | 153 | cow4 sheep2; W7 M12 |  |  |
| 5 | 647 | 4 | 1 | S4 |  | S4 | 7/0 | 4 | W2 F1 | 153 | cow4 sheep2; W3 S4 M12 |  |  |
| 6 | 760 | 7 | 2 | cow2 \| W5 S8 | pasture 7  | W5 S8 | 8/0 | 5 | W9 F8 | 1006 | cow6 sheep2; W6 S12 M12; empty pens 5 |  | Yarn Store |
| 7 | 763 | 8 | 2 | sheep2 \| W4 S4 |  | W4 S4 | 10/0 | 0 | Wl2 F5 | 853 | cow6 sheep4; W9 S16 M12; empty pens 3 |  |  |
| 8 | 292 | 9 | 2 | sheep2 \| W1 S4 |  | W1 S4 | 12/0 | 7 | W2 F4 | 403 | cow6 sheep6; W5 S20 M12; empty pens 1 |  |  |
| 9 | 1507 | 8 | 2 | sheep2 \| W4 |  | W4 | 14/0 | 6 | W2 F11 | 942 | cow6 sheep7; W5 S20 M12 |  | Farmers Market |
| 10 | 2619 | 11 | 2 | sheep2 \| W7 | pasture 4 coop 1 | W7 | 16/0 | 15 | F2 | 152 | cow6 sheep10; W12 S20; empty pens 2 |  |  |
| 11 | 16343 | 11 | 3 | sheep1 \| W11 S13 |  | W11 S13 | 17/0 | 4 | M12 F11 | 2408 | cow6 sheep11; W20 S33; empty pens 1 |  |  |
| 12 | 14637 | 11 | 4 | sheep6 \| W8 | pasture 6  | W8 | 23/0 | 9 | W9 F18 | 1599 | cow6 sheep17; W24 S33; empty pens 1 |  | Yarn Store |
| 13 | 11645 | 12 | 4 | W6 |  | W6 | 23/0 | 9 | W323 Mk3 F17 | 15173 | cow6 sheep17; W24 S33; empty pens 1 |  |  |
| 14 | 13644 | 12 | 4 | W7 |  | W7 | 23/4 | 16 | W240 Mk6 Wl4 F16 | 12536 | cow6 sheep17; W24 S33; empty pens 1 |  |  |
| 15 | 19340 | 13 | 4 | W8 |  | W8 | 23/8 | 18 | W342 Mk3 Wl7 F20 | 17418 | cow6 sheep17; W24 S33 |  | Bakery |
| 16 | 26611 | 14 | 4 | W8 |  | W8 | 23/4 | 24 | W170 S4 Wl12 F15 | 11587 | cow6 sheep17; W25 S33 | 1 |  |
| 17 | 34923 | 13 | 4 | W7 |  | W7 | 23/4 | 21 | W280 Mk3 Wl4 F13 | 13550 | cow6 sheep17; W25 S33 |  |  |
| 18 | 42130 | 14 | 4 | W7 |  | W7 | 23/4 | 34 | W269 S8 Mk3 Wl6 F13 | 15015 | cow6 sheep17; W25 S33 |  | Pet Cafe |
| 19 | 56742 | 13 | 4 | W6 |  | W6 | 23/15 | 21 | W361 Mk9 Wl8 F9 | 17671 | cow6 sheep17; W25 S33 |  |  |
| 20 | 60828 | 13 | 4 | W6 |  | W6 | 23/13 | 26 | W363 Mk3 Wl16 F10 | 19016 | cow6 sheep17; W25 S33 |  |  |
| 21 | 66528 | 13 | 4 | W11 |  | W11 | 23/3 | 39 | W192 Mk9 Wl12 F12 | 10627 | cow6 sheep17; W30 S28 |  | Yarn Store |
| 22 | 72562 | 13 | 4 | W8 |  | W8 | 23/9 | 27 | W294 S14 Mk6 Wl4 F20 | 13885 | cow6 sheep17; W31 S27 | 1 |  |
| 23 | 72746 | 13 | 4 | W14 |  | W14 | 23/7 | 30 | W226 S20 Mk9 Wl16 F21 | 12701 | cow6 sheep17; W38 S20 | 7 |  |
| 24 | 74600 | 13 | 4 | W9 C4 |  | W9 C4 | 23/11 | 31 | W352 S21 Mk3 Wl20 F10 | 18972 | cow6 sheep17; W37 C4 S17; weeds 1 | 4 | Pizza |
| 25 | 77864 | 13 | 4 | C14 |  | C14 | 23/8 | 29 | W236 S13 Mk18 Wl8 F16 | 10800 | cow6 sheep17; W27 C18 S13; weeds 1 | 4 |  |
| 26 | 78937 | 13 | 4 | W1 C11 |  | W1 C11 | 23/7 | 18 | W206 S10 Mk3 Wl11 F16 | 9899 | cow6 sheep17; W16 C29 S13; weeds 1 |  |  |
| 27 | 80416 | 12 | 4 | W2 C8 |  | W2 C8 | 23/0 | 39 | W167 S14 Mk12 F17 | 7567 | cow6 sheep17; W12 C32 S4; weeds 1 |  |  |
| 28 | 84792 | 12 | 4 |  | coop 1 |  | 15/0 | 29 | W119 C17 S4 Mk13 Wl21 F10 | 7805 | cow6 sheep17; W4 C19; weeds 2 empty pens 1 | 5 |  |
| 29 | 88145 | 9 | 4 |  |  |  | 0/0 | 33 | W42 C31 S16 Mk1 Wl4 F7 | 4294 | cow6 sheep17; weeds 3 empty pens 1 | 1 |  |

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| L | 50 | 2 (98%) | 5 (50%) | 5 (50%) | 5 (50%) | 18 (26%) | 32 (12%) | 37 (12%) | 50 (2%) |
| C0 | 50 | 3 (88%) | 7 (46%) | 7 (46%) | 7 (46%) | 19 (28%) | 25 (20%) | 27 (18%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| L | 50 | 6 (46%) | 7 (46%) | 7 (46%) | 7 (46%) | 20 (22%) | 40 (6%) | 47 (4%) | 50 (2%) |
| C0 | 50 | 7 (50%) | 9 (32%) | 9 (32%) | 9 (32%) | 28 (18%) | 40 (8%) | 48 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) |
| L | 50 | 4 (52%) | 6 (50%) | 6 (50%) | 6 (50%) | 19 (26%) | 40 (8%) | 45 (6%) | 50 (2%) |
| C0 | 50 | 5 (50%) | 9 (32%) | 9 (32%) | 9 (32%) | 26 (22%) | 37 (8%) | 46 (4%) | 50 (2%) |

Current submission (63 sampled games): field is **reactive from day 1: 3 openings at turn 24 (largest 89%), 8 lines at turn 100; every game distinct by turn 719**; market is **reactive from day 1: 7 openings at turn 24 (largest 49%), 9 lines at turn 100; every game distinct by turn 719**; plan is **reactive from day 1: 5 openings at turn 24 (largest 49%), 10 lines at turn 100; every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 3 | 56 | 88.9 |
| 48 | 2 | 7 | 29 | 46.0 |
| 100 | 4 | 8 | 29 | 46.0 |
| 136 | 5 | 8 | 29 | 46.0 |
| 200 | 8 | 24 | 17 | 27.0 |
| 300 | 12 | 33 | 11 | 17.5 |
| 400 | 16 | 37 | 10 | 15.9 |
| 719 | 29 | 63 | 1 | 1.6 |

What goes with being off the modal field line at turn 24 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 1 | 0 |  | 11.1 |
| opponent off its modal line at turn 24 | 17 | 0 | 15.2 |
| played seat 1 | 23 | 17.4 | 7.5 |
| lost the game | 13 | 7.7 | 12 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 1 | 0 | 59081 | 10 | 14 | 0 | 0 | 2 | 11 | 2 | 4 | 10 | 48 | 307 | 0 | 1 | 1 |
| L | 50 | 80 | 95476 | 12 | 7.5 | 5 | 4 | 3 | 6 | 33 | 153 | 12 | 12 | 142 | 94 | 37 | 47 |
| C0 | 50 | 90 | 99096 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 158 | 12 | 12 | 154 | 109 | 27 | 48 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| F | 89061335 | Danilo_Malbashich | 1140.1 | 59081 | 78212 | -19131 | 4ca76d17 | milk sold: they 112 vs me 307; units sold last 3 days: they 208 vs me 77; CARE ops: they 366 vs me 241 |
| C0 | 108931203 | makishis | 2695.2 | 77686 | 77705 | -19 | 9b0c82fd | units sold last 3 days: they 266 vs me 553; milk sold: they 93 vs me 155; wheat planted: they 162 vs me 189 |
| C0 | 108934575 | Friedhelm Winter | 2695.9 | 64109 | 66541 | -2432 | 9b0c82fd | units sold last 3 days: they 266 vs me 574; milk sold: they 105 vs me 152; strawberry sold: they 135 vs me 150 |
| C0 | 108938524 | Bernardus | 2774.7 | 79091 | 79302 | -211 | 9b0c82fd | units sold last 3 days: they 264 vs me 584; wool sold: they 42 vs me 68; FERTILIZE ops: they 124 vs me 115 |
| C0 | 108945959 | kaggricodex | 2808.5 | 81101 | 81434 | -333 | 9b0c82fd | units sold last 3 days: they 244 vs me 581; wool sold: they 56 vs me 109; milk sold: they 115 vs me 158 |
| C0 | 108949771 | nilochan | 2915.4 | 170502 | 171838 | -1336 | 9b0c82fd | units sold last 3 days: they 257 vs me 581; milk sold: they 99 vs me 158; wool sold: they 54 vs me 109 |
| L | 109064807 | HowardLeeTW | 2988.7 | 80966 | 81737 | -771 | 997b20f5 | units sold last 3 days: they 244 vs me 628; CARE ops: they 189 vs me 407; FERTILIZE ops: they 207 vs me 75 |
| L | 109069079 | Mengfei Li | 2913.1 | 111322 | 117731 | -6409 | 3bc18d7a | units sold last 3 days: they 215 vs me 582; CARE ops: they 214 vs me 409; FERTILIZE ops: they 200 vs me 109 |
| L | 109069251 | redblackbst | 2956.4 | 119956 | 121827 | -1871 | cfefcbaa | units sold last 3 days: they 283 vs me 591; strawberry sold: they 235 vs me 147; CARE ops: they 326 vs me 405 |
| L | 109073392 | kobq | 2909.8 | 99763 | 100278 | -515 | 9b0c82fd | units sold last 3 days: they 263 vs me 590; milk sold: they 119 vs me 165; wheat planted: they 163 vs me 149 |
| L | 109081211 | Umataro Tenma | 2638.6 | 74859 | 76227 | -1368 | 9b0c82fd | units sold last 3 days: they 262 vs me 559; milk sold: they 96 vs me 155; wool sold: they 73 vs me 90 |
| L | 109083105 | Cow Boy | 2958.8 | 77226 | 78720 | -1494 | 83322aec | units sold last 3 days: they 277 vs me 585; milk sold: they 109 vs me 158; wheat planted: they 162 vs me 147 |
| L | 109084045 | アルモンド | 2979.5 | 103361 | 123534 | -20173 | 9b0c82fd | units sold last 3 days: they 286 vs me 509; CARE ops: they 486 vs me 398; wool sold: they 247 vs me 205 |
| L | 109084389 | Catalyst | 2956.2 | 127435 | 129082 | -1647 | 9b0c82fd | units sold last 3 days: they 276 vs me 601; strawberry sold: they 180 vs me 147; milk sold: they 209 vs me 176 |
| L | 109091524 | keiz | 2890.1 | 116667 | 116830 | -163 | 01b4205d | units sold last 3 days: they 197 vs me 576; milk sold: they 48 vs me 170; strawberry sold: they 214 vs me 146 |
| L | 109093815 | THUNDER THUNDER | 2756.8 | 87689 | 91029 | -3340 | 24a0cda8 | units sold last 3 days: they 239 vs me 650; CARE ops: they 166 vs me 402; FERTILIZE ops: they 214 vs me 68 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 4 | 0 |
| 16622198 | 6 | 5 | 1 |
| 16622349 | 11 | 27 | 0 |
| 16633100 | 3 | 1 | 0 |
| 16637255 | 14 | 7 | 2 |
| 16640467 | 6 | 8 | 0 |
| 16640510 | 3 | 6 | 0 |
| 16644724 | 0 | 0 | 2 |
| 16675778 | 0 | 4 | 0 |
| 16690867 | 2 | 2 | 0 |
| 16718819 | 0 | 2 | 0 |
| 16719123 | 8 | 10 | 0 |
| 16725899 | 5 | 3 | 0 |
| 16730612 | 3 | 5 | 0 |
| 16730761 | 8 | 6 | 2 |
| 16732403 | 7 | 10 | 0 |
| 16732521 | 3 | 11 | 1 |
| 16732748 | 3 | 2 | 0 |
| 16758882 | 5 | 7 | 0 |
| 16760569 | 4 | 5 | 0 |
| 16773026 | 7 | 5 | 0 |
| 16777134 | 3 | 3 | 0 |
| 16778640 | 2 | 0 | 0 |
| 16781445 | 1 | 1 | 0 |
| 16805699 | 8 | 8 | 0 |
| 16811307 | 8 | 0 | 1 |
| 16833141 | 10 | 0 | 0 |
| 16845367 | 12 | 1 | 0 |
| 16858228 | 2 | 1 | 0 |

## Episodes behind each window

- **F** (1): 89061335
- **L** (50): 109061367, 109062089, 109062197, 109062403, 109063431, 109064452, 109064807, 109065508, 109066028, 109066541, 109067582, 109068628, 109069079, 109069251, 109069735, 109070376, 109070817, 109071731, 109072768, 109073392, 109073817, 109074859, 109076118, 109077543, 109078319, 109078615, 109080085, 109081211, 109082377, 109082498, 109083105, 109083613, 109084045, 109084389, 109084948, 109086210, 109086881, 109086927, 109087609, 109088887, 109090132, 109090212, 109090662, 109091252, 109091524, 109092421, 109092489, 109093595, 109093815, 109094736
- **C0** (50): 108908450, 108909458, 108910563, 108911501, 108912504, 108913510, 108914540, 108915557, 108916582, 108917616, 108918628, 108919657, 108920675, 108921703, 108922696, 108922746, 108923792, 108924823, 108925660, 108925937, 108926974, 108928041, 108929079, 108930142, 108931203, 108932268, 108933314, 108933709, 108934341, 108934575, 108935405, 108936457, 108937489, 108938524, 108939573, 108940618, 108941666, 108942700, 108943735, 108944824, 108945959, 108946868, 108947912, 108948960, 108949771, 108951147, 108952634, 108953569, 108954232, 108955246
