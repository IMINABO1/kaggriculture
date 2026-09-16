# Kaggriculture Agent (rank 35, score 2914.5, silver)

- team id 16644724; current submission 56230957 (170 public games)
- 106 submissions found; 12285 public games from 2026-07-31 to 2026-09-15; 271 of them with a known rating
- sampled games with a replay: 150

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 28-22-0 | 56 | 68557.5 | 77280.0 | 952.3 | 42 | 1.32.2 | 2026-07-31 | 2026-08-02 |
| L | 50 | 40-10-0 | 80 | 95476 | 97707.6 | 2690.2 | 62 | 1.32.7 | 2026-09-14 | 2026-09-15 |
| C0 | 50 | 45-5-0 | 90 | 99096 | 104391.4 | 2250.5 | 64 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 715, game 10: 1608, game 25: 2658, game 50: 2873, game 100: 2917, game last: 2914

![rating](figs/kaggriculture-agent_rating.png)

## Farm plan by window (median per game)

| median per game | F | L | C0 |
|---|---|---|---|
| hands (peak) | 10 | 12 | 12 |
| quadrants | 2 | 3 | 3 |
| land day 1 | 11 | 6 | 6 |
| land day 2 | 12 | 11 | 11 |
| cows bought | 12 | 7.5 | 8 |
| sheep bought | 0 | 5 | 6 |
| geese bought | 0 | 4 | 3 |
| first cow day | 0 | 0 | 0 |
| wheat planted | 8.5 | 153 | 158 |
| carrot planted | 0 | 41 | 36 |
| tomato planted | 0 | 0 | 0 |
| strawberry planted | 0.5 | 33 | 33 |
| melon planted | 14 | 12 | 12 |
| FERTILIZE ops | 0 | 117 | 116 |
| CARE ops | 239.5 | 406 | 408 |
| melon sold | 54 | 72 | 72 |
| strawberry sold | 0 | 249 | 249 |
| milk sold | 276.5 | 224.5 | 245 |
| wool sold | 0 | 140 | 161 |
| wheat sold | 18 | 4007.5 | 3948 |
| fertilizer sold | 127.5 | 328 | 329 |
| units sold last 3 days | 93.5 | 721 | 696.5 |
| shed peak | 25.5 | 58 | 58 |
| weeds spawned | 16 | 20 | 20 |
| unexecutable market orders | 0 | 45 | 45 |

![money by day](figs/kaggriculture-agent_money.png)

## A typical recent game, day by day

Episode 109080085 (the median-bank game of the latest window): seat 0, bank 96400 vs 86191 (NonCaffeine), seed 871198338. Letters: W wheat, C carrot, T tomato, S strawberry, M melon, E egg, Mk milk, Wl wool, F fertilizer.

| day | money | hands | quads | bought | built | planted | care/fert | harvest | sold | revenue | farm at day end | new weeds | shop unlock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3000 | 5 | 1 | cow2 sheep2 \| W7 M12 | pasture 4  | W7 M12 | 3/0 | 0 | W51 | 1528 | cow2 sheep2; W7 M12 |  |  |
| 1 | 12 | 3 | 1 |  | pasture 2  |  | 4/0 | 0 | W1 F3 | 328 | cow2 sheep2; W7 M12; empty pens 2 |  |  |
| 2 | 102 | 4 | 1 | cow1 \| W3 |  | W3 | 5/0 | 3 | W1 F5 | 520 | cow3 sheep2; W7 M12; empty pens 1 |  |  |
| 3 | 185 | 5 | 1 | cow1 \| W4 |  | W4 | 6/0 | 4 | W4 F4 | 504 | cow3 sheep2; W7 M12; empty pens 1 |  | Smoothie |
| 4 | 237 | 4 | 1 | W3 |  | W3 | 6/0 | 3 | W2 F6 | 623 | cow4 sheep2; W7 M12 |  |  |
| 5 | 647 | 4 | 1 | S4 |  | S4 | 7/0 | 4 | W2 F5 | 520 | cow4 sheep2; W3 S4 M12 |  |  |
| 6 | 760 | 7 | 2 | cow2 \| W5 S8 | pasture 7  | W5 S8 | 8/0 | 5 | W9 Wl10 F8 | 3082 | cow6 sheep2; W6 S12 M12; empty pens 5 |  | Yarn Store |
| 7 | 763 | 8 | 2 | sheep2 \| W4 S4 |  | W4 S4 | 10/0 | 0 | Wl2 F7 | 1023 | cow6 sheep4; W9 S16 M12; empty pens 3 |  |  |
| 8 | 292 | 9 | 2 | sheep2 \| W1 S4 |  | W1 S4 | 12/0 | 7 | W2 Mk12 F10 | 3380 | cow6 sheep6; W5 S20 M12; empty pens 1 |  |  |
| 9 | 1507 | 8 | 2 | sheep2 \| W4 |  | W4 | 14/0 | 6 | W2 Wl8 F12 | 2822 | cow6 sheep7; W5 S20 M12 |  | Farmers Market |
| 10 | 2619 | 11 | 2 | sheep2 \| W7 | pasture 4 coop 1 | W7 | 16/0 | 15 | M60 Mk12 F2 | 15568 | cow6 sheep10; W12 S20; empty pens 2 |  |  |
| 11 | 16343 | 11 | 3 | sheep1 \| W11 S13 |  | W11 S13 | 17/0 | 4 | M12 Mk6 F11 | 3194 | cow6 sheep11; W20 S33; empty pens 1 |  |  |
| 12 | 14637 | 11 | 4 | sheep6 \| W8 | pasture 6  | W8 | 23/0 | 9 | W9 Mk6 Wl8 F18 | 4554 | cow6 sheep17; W24 S33; empty pens 1 |  | Yarn Store |
| 13 | 11645 | 12 | 4 | W6 |  | W6 | 23/0 | 9 | W323 Mk6 F21 | 15423 | cow6 sheep17; W24 S33; empty pens 1 |  |  |
| 14 | 13644 | 12 | 4 | W7 |  | W7 | 23/4 | 16 | W240 Mk18 Wl13 F16 | 15912 | cow6 sheep17; W24 S33; empty pens 1 |  |  |
| 15 | 19340 | 13 | 4 | W8 |  | W8 | 23/8 | 18 | W342 S8 Mk6 Wl21 F24 | 22447 | cow6 sheep17; W24 S33 |  | Bakery |
| 16 | 26611 | 14 | 4 | W8 |  | W8 | 23/4 | 24 | W170 S16 Mk12 Wl18 F21 | 16321 | cow6 sheep17; W25 S33 | 1 |  |
| 17 | 34923 | 13 | 4 | W7 |  | W7 | 23/4 | 21 | W280 S16 Mk3 Wl16 F19 | 19372 | cow6 sheep17; W25 S33 |  |  |
| 18 | 42130 | 14 | 4 | W7 |  | W7 | 23/4 | 34 | W269 S24 Mk9 Wl46 F19 | 26915 | cow6 sheep17; W25 S33 |  | Pet Cafe |
| 19 | 56742 | 13 | 4 | W6 |  | W6 | 23/15 | 21 | W361 S16 Mk9 Wl12 F9 | 20390 | cow6 sheep17; W25 S33 |  |  |
| 20 | 60828 | 13 | 4 | W6 |  | W6 | 23/13 | 26 | W363 S24 Mk6 Wl16 F11 | 21993 | cow6 sheep17; W25 S33 |  |  |
| 21 | 66528 | 13 | 4 | W11 |  | W11 | 23/3 | 39 | W192 S24 Mk9 Wl36 F18 | 14737 | cow6 sheep17; W30 S28 |  | Yarn Store |
| 22 | 72562 | 13 | 4 | W8 |  | W8 | 23/9 | 27 | W294 S22 Mk9 Wl8 F20 | 13827 | cow6 sheep17; W31 S27 | 1 |  |
| 23 | 72746 | 13 | 4 | W14 |  | W14 | 23/7 | 30 | W226 S20 Mk9 Wl16 F21 | 11852 | cow6 sheep17; W38 S20 | 7 |  |
| 24 | 74600 | 13 | 4 | W9 C4 |  | W9 C4 | 23/11 | 31 | W352 S21 Mk3 Wl48 F16 | 18544 | cow6 sheep17; W37 C4 S17; weeds 1 | 4 | Pizza |
| 25 | 77864 | 13 | 4 | C14 |  | C14 | 23/8 | 29 | W236 S14 Mk18 Wl17 F16 | 11200 | cow6 sheep17; W27 C18 S13; weeds 1 | 4 |  |
| 26 | 78937 | 13 | 4 | W1 C11 |  | W1 C11 | 23/7 | 18 | W206 S10 Mk3 Wl21 F16 | 10425 | cow6 sheep17; W16 C29 S13; weeds 1 |  |  |
| 27 | 80416 | 12 | 4 | W2 C8 |  | W2 C8 | 23/0 | 39 | W167 S14 Mk12 Wl24 F24 | 10386 | cow6 sheep17; W12 C32 S4; weeds 1 |  |  |
| 28 | 84792 | 12 | 4 |  | coop 1 |  | 15/0 | 29 | W139 C20 S4 Mk13 Wl21 F21 | 8013 | cow6 sheep17; W4 C19; weeds 2 empty pens 1 | 5 |  |
| 29 | 88145 | 9 | 4 |  |  |  | 0/0 | 33 | W49 C77 S16 Mk10 Wl20 F10 | 8345 | cow6 sheep17; weeds 3 empty pens 1 | 1 |  |

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 2 (78%) | 2 (78%) | 2 (78%) | 2 (78%) | 2 (78%) | 29 (22%) | 36 (22%) | 40 (22%) |
| L | 50 | 2 (98%) | 5 (50%) | 5 (50%) | 5 (50%) | 18 (26%) | 32 (12%) | 37 (12%) | 50 (2%) |
| C0 | 50 | 3 (88%) | 7 (46%) | 7 (46%) | 7 (46%) | 19 (28%) | 25 (20%) | 27 (18%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 2 (78%) | 2 (78%) | 2 (78%) | 2 (78%) | 4 (46%) | 36 (22%) | 38 (22%) | 40 (22%) |
| L | 50 | 6 (46%) | 7 (46%) | 7 (46%) | 7 (46%) | 20 (22%) | 40 (6%) | 47 (4%) | 50 (2%) |
| C0 | 50 | 7 (50%) | 9 (32%) | 9 (32%) | 9 (32%) | 28 (18%) | 40 (8%) | 48 (4%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 2 (78%) | 2 (78%) | 2 (78%) | 2 (78%) | 4 (46%) | 36 (22%) | 38 (22%) | 40 (22%) |
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
| F | 50 | 56 | 68557.5 | 10 | 12 | 0 | 0 | 2 | 11 | 0.5 | 8.5 | 14 | 54 | 276.5 | 0 | 36 | 38 |
| L | 50 | 80 | 95476 | 12 | 7.5 | 5 | 4 | 3 | 6 | 33 | 153 | 12 | 72 | 224.5 | 140 | 37 | 47 |
| C0 | 50 | 90 | 99096 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 158 | 12 | 72 | 245 | 161 | 27 | 48 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| F | 89061335 | Danilo_Malbashich | 1140.1 | 59081 | 78212 | -19131 | 4ca76d17 | milk sold: they 112 vs me 307; units sold last 3 days: they 208 vs me 77; CARE ops: they 366 vs me 241 |
| F | 89062328 | Beisenbek Nurassyl [dsmlkz] | 1036.0 | 25067 | 52179 | -27112 | 6e498144 | wool sold: they 189 vs me 0; milk sold: they 189 vs me 318; units sold last 3 days: they 199 vs me 99 |
| F | 89063307 | Jesse Ferguson | 947.8 | 62004 | 83865 | -21861 | fc77718d | CARE ops: they 452 vs me 177; units sold last 3 days: they 225 vs me 76; wool sold: they 147 vs me 0 |
| F | 89063309 | fgwiebfaoish | 1052.9 | 39965 | 66771 | -26806 | 43b287e3 | melon sold: they 138 vs me 48; units sold last 3 days: they 138 vs me 81; wheat planted: they 91 vs me 38 |
| F | 89063808 | Vlad Kochetov | 1068.7 | 65757 | 96726 | -30969 | 3760ac38 | wool sold: they 226 vs me 0; milk sold: they 83 vs me 249; CARE ops: they 343 vs me 189 |
| F | 89070098 | Jesse Ferguson | 1062.9 | 26226 | 67143 | -40917 | 44bf7b5a | units sold last 3 days: they 309 vs me 87; wool sold: they 169 vs me 0; milk sold: they 192 vs me 296 |
| F | 89081681 | nasubiman | 1041.0 | 26528 | 26693 | -165 | 866496d0 | units sold last 3 days: they 948 vs me 93; CARE ops: they 376 vs me 243; wool sold: they 56 vs me 0 |
| F | 89091739 | Peng Wang | 934.3 | 82573 | 89668 | -7095 | ec989382 | milk sold: they 0 vs me 319; strawberry sold: they 238 vs me 0; CARE ops: they 20 vs me 255 |
| F | 89097060 | Danilo_Malbashich | 921.2 | 55657 | 109338 | -53681 | ea2b06f9 | wool sold: they 144 vs me 0; CARE ops: they 315 vs me 183; units sold last 3 days: they 204 vs me 88 |
| F | 89104371 | Ali | 1072.8 | 21871 | 57843 | -35972 | 2cabfef4 | units sold last 3 days: they 438 vs me 105; CARE ops: they 501 vs me 249; wool sold: they 159 vs me 0 |
| F | 89112229 | Pomiro | 970.1 | 39955 | 49175 | -9220 | f403380f | CARE ops: they 286 vs me 196; units sold last 3 days: they 166 vs me 86; wool sold: they 66 vs me 0 |
| F | 89116671 | BOBQWERA | 1049.8 | 51137 | 71599 | -20462 | 8a9d898c | melon sold: they 155 vs me 42; wheat planted: they 114 vs me 28; units sold last 3 days: they 142 vs me 79 |
| F | 89119107 | smlcr | 927.2 | 69874 | 119107 | -49233 | c8f3ebd2 | strawberry sold: they 150 vs me 3; milk sold: they 120 vs me 267; wool sold: they 107 vs me 0 |
| F | 89119591 | Vlad Kochetov | 945.2 | 60691 | 106090 | -45399 | 3760ac38 | CARE ops: they 353 vs me 145; wool sold: they 142 vs me 0; units sold last 3 days: they 195 vs me 89 |
| F | 89123501 | Raiden.B | 1094.9 | 74307 | 134770 | -60463 | b54a1f3e | strawberry sold: they 178 vs me 0; wool sold: they 154 vs me 0; milk sold: they 168 vs me 313 |
| F | 89125500 | Subin An | 1023.9 | 63626 | 83007 | -19381 | f51370d1 | units sold last 3 days: they 172 vs me 71; milk sold: they 186 vs me 283; wool sold: they 94 vs me 0 |
| F | 89126470 | Vlad Kochetov | 983.8 | 66137 | 116423 | -50286 | 9d792506 | CARE ops: they 435 vs me 180; wool sold: they 248 vs me 0; units sold last 3 days: they 272 vs me 77 |
| F | 89128934 | Raiden.B | 1035.8 | 62856 | 122003 | -59147 | c2c377f7 | strawberry sold: they 165 vs me 0; milk sold: they 114 vs me 276; units sold last 3 days: they 229 vs me 101 |
| F | 89131864 | Kumaran K | 804.0 | 27921 | 32998 | -5077 | dc6fc820 | units sold last 3 days: they 821 vs me 85; melon sold: they 36 vs me 78; wheat planted: they 67 vs me 35 |
| F | 89137321 | RuleCraft | 1104.9 | 50076 | 95522 | -45446 | 42c50837 | wool sold: they 121 vs me 0; strawberry sold: they 113 vs me 7; CARE ops: they 310 vs me 209 |
| F | 89420843 | Alexander Gremyakov | 1428.4 | 112450 | 121935 | -9485 | ced113cf | units sold last 3 days: they 1204 vs me 339; wool sold: they 113 vs me 229; CARE ops: they 234 vs me 338 |
| F | 89420887 | Ali | 1532.7 | 114792 | 120389 | -5597 | aa27ef5f | wool sold: they 163 vs me 229; milk sold: they 225 vs me 187; CARE ops: they 319 vs me 338 |
| C0 | 108931203 | makishis | 2695.2 | 77686 | 77705 | -19 | 9b0c82fd | units sold last 3 days: they 385 vs me 676; milk sold: they 167 vs me 245; wheat planted: they 162 vs me 189 |
| C0 | 108934575 | Friedhelm Winter | 2695.9 | 64109 | 66541 | -2432 | 9b0c82fd | units sold last 3 days: they 386 vs me 697; milk sold: they 198 vs me 245; wool sold: they 144 vs me 161 |
| C0 | 108938524 | Bernardus | 2774.7 | 79091 | 79302 | -211 | 9b0c82fd | units sold last 3 days: they 374 vs me 713; wool sold: they 87 vs me 118; milk sold: they 241 vs me 266 |
| C0 | 108945959 | kaggricodex | 2808.5 | 81101 | 81434 | -333 | 9b0c82fd | units sold last 3 days: they 410 vs me 745; wool sold: they 99 vs me 161; milk sold: they 196 vs me 245 |
| C0 | 108949771 | nilochan | 2915.4 | 170502 | 171838 | -1336 | 9b0c82fd | units sold last 3 days: they 423 vs me 745; wool sold: they 99 vs me 161; milk sold: they 209 vs me 245 |
| L | 109064807 | HowardLeeTW | 2988.7 | 80966 | 81737 | -771 | 997b20f5 | units sold last 3 days: they 400 vs me 738; CARE ops: they 189 vs me 407; FERTILIZE ops: they 207 vs me 75 |
| L | 109069079 | Mengfei Li | 2913.1 | 111322 | 117731 | -6409 | 3bc18d7a | units sold last 3 days: they 379 vs me 747; CARE ops: they 214 vs me 409; FERTILIZE ops: they 200 vs me 109 |
| L | 109069251 | redblackbst | 2956.4 | 119956 | 121827 | -1871 | cfefcbaa | units sold last 3 days: they 397 vs me 715; CARE ops: they 326 vs me 405; strawberry sold: they 325 vs me 260 |
| L | 109073392 | kobq | 2909.8 | 99763 | 100278 | -515 | 9b0c82fd | units sold last 3 days: they 387 vs me 728; milk sold: they 229 vs me 267; wheat planted: they 163 vs me 149 |
| L | 109081211 | Umataro Tenma | 2638.6 | 74859 | 76227 | -1368 | 9b0c82fd | units sold last 3 days: they 386 vs me 679; milk sold: they 183 vs me 245; FERTILIZE ops: they 123 vs me 109 |
| L | 109083105 | Cow Boy | 2958.8 | 77226 | 78720 | -1494 | 83322aec | units sold last 3 days: they 397 vs me 715; milk sold: they 198 vs me 245; wheat planted: they 162 vs me 147 |
| L | 109084045 | アルモンド | 2979.5 | 103361 | 123534 | -20173 | 9b0c82fd | units sold last 3 days: they 426 vs me 617; wool sold: they 452 vs me 315; CARE ops: they 486 vs me 398 |
| L | 109084389 | Catalyst | 2956.2 | 127435 | 129082 | -1647 | 9b0c82fd | units sold last 3 days: they 398 vs me 718; wool sold: they 86 vs me 118; wheat planted: they 162 vs me 193 |
| L | 109091524 | keiz | 2890.1 | 116667 | 116830 | -163 | 01b4205d | units sold last 3 days: they 294 vs me 690; wool sold: they 51 vs me 139; CARE ops: they 353 vs me 408 |
| L | 109093815 | THUNDER THUNDER | 2756.8 | 87689 | 91029 | -3340 | 24a0cda8 | units sold last 3 days: they 426 vs me 769; CARE ops: they 166 vs me 402; FERTILIZE ops: they 214 vs me 68 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 5 | 0 |
| 16622198 | 8 | 5 | 1 |
| 16622349 | 12 | 28 | 0 |
| 16622459 | 5 | 2 | 0 |
| 16626191 | 13 | 8 | 3 |
| 16633100 | 3 | 1 | 0 |
| 16633178 | 7 | 9 | 0 |
| 16633944 | 14 | 5 | 1 |
| 16637255 | 15 | 8 | 2 |
| 16640467 | 6 | 10 | 0 |
| 16640510 | 3 | 7 | 0 |
| 16641710 | 15 | 4 | 0 |
| 16644724 | 0 | 0 | 2 |
| 16655383 | 7 | 3 | 0 |
| 16657100 | 6 | 3 | 0 |
| 16658554 | 2 | 0 | 0 |
| 16660726 | 2 | 9 | 2 |
| 16664246 | 0 | 5 | 0 |
| 16671741 | 4 | 8 | 0 |
| 16675778 | 0 | 4 | 0 |
| 16683936 | 7 | 6 | 2 |
| 16684093 | 10 | 5 | 1 |
| 16690867 | 2 | 2 | 0 |
| 16706321 | 4 | 2 | 0 |
| 16718819 | 0 | 2 | 0 |
| 16719123 | 9 | 11 | 0 |
| 16723379 | 8 | 2 | 0 |
| 16725899 | 5 | 3 | 0 |
| 16728071 | 8 | 13 | 2 |
| 16730524 | 5 | 15 | 0 |
| 16730612 | 3 | 5 | 0 |
| 16730761 | 9 | 6 | 2 |
| 16731186 | 3 | 5 | 0 |
| 16731275 | 6 | 9 | 0 |
| 16732403 | 7 | 11 | 0 |
| 16732521 | 3 | 14 | 1 |
| 16732748 | 3 | 3 | 0 |
| 16741542 | 11 | 10 | 0 |
| 16758882 | 9 | 7 | 0 |
| 16760569 | 4 | 7 | 0 |
| 16761744 | 4 | 0 | 0 |
| 16773026 | 8 | 6 | 0 |
| 16777134 | 4 | 3 | 0 |
| 16778640 | 2 | 0 | 0 |
| 16781445 | 1 | 1 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 9 | 8 | 0 |
| 16810299 | 2 | 1 | 0 |
| 16811307 | 8 | 0 | 1 |
| 16833141 | 12 | 1 | 0 |
| 16845367 | 13 | 1 | 0 |
| 16848479 | 11 | 4 | 0 |
| 16848532 | 1 | 0 | 0 |
| 16858228 | 4 | 1 | 0 |
| 16882725 | 1 | 0 | 0 |

## Episodes behind each window

- **F** (50): 89058344, 89058835, 89059340, 89059867, 89059868, 89059874, 89060363, 89060844, 89061335, 89062328, 89063307, 89063309, 89063808, 89070098, 89071092, 89081681, 89083601, 89084576, 89091739, 89092738, 89095142, 89097060, 89104371, 89112229, 89112239, 89112237, 89113709, 89116185, 89116671, 89119107, 89119591, 89122999, 89123501, 89125500, 89126470, 89128934, 89131864, 89137321, 89141781, 89415993, 89416527, 89417063, 89417613, 89418169, 89418711, 89419241, 89419773, 89420308, 89420843, 89420887
- **L** (50): 109061367, 109062089, 109062197, 109062403, 109063431, 109064452, 109064807, 109065508, 109066028, 109066541, 109067582, 109068628, 109069079, 109069251, 109069735, 109070376, 109070817, 109071731, 109072768, 109073392, 109073817, 109074859, 109076118, 109077543, 109078319, 109078615, 109080085, 109081211, 109082377, 109082498, 109083105, 109083613, 109084045, 109084389, 109084948, 109086210, 109086881, 109086927, 109087609, 109088887, 109090132, 109090212, 109090662, 109091252, 109091524, 109092421, 109092489, 109093595, 109093815, 109094736
- **C0** (50): 108908450, 108909458, 108910563, 108911501, 108912504, 108913510, 108914540, 108915557, 108916582, 108917616, 108918628, 108919657, 108920675, 108921703, 108922696, 108922746, 108923792, 108924823, 108925660, 108925937, 108926974, 108928041, 108929079, 108930142, 108931203, 108932268, 108933314, 108933709, 108934341, 108934575, 108935405, 108936457, 108937489, 108938524, 108939573, 108940618, 108941666, 108942700, 108943735, 108944824, 108945959, 108946868, 108947912, 108948960, 108949771, 108951147, 108952634, 108953569, 108954232, 108955246
