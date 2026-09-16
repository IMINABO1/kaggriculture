# elmo (rank 38, score 2910.7, silver)

- team id 16811307; current submission 56234758 (168 public games)
- 23 submissions found; 3678 public games from 2026-09-04 to 2026-09-15; 32 of them with a known rating
- sampled games with a replay: 150

## Ladder record by window

| window | games | W-L-T | win % | median bank | mean bank | opp rating (mean) | seat 0 % | engines | from | to |
|---|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 44-6-0 | 88 | 93357 | 91050.5 | 1495.9 | 44 | 1.32.7 | 2026-09-04 | 2026-09-04 |
| L | 50 | 35-15-0 | 70 | 91041.5 | 95898.2 | 2837.7 | 62 | 1.32.7 | 2026-09-14 | 2026-09-15 |
| C0 | 50 | 46-4-0 | 92 | 106007.5 | 109760.8 | 2184.5 | 38 | 1.32.7 | 2026-09-14 | 2026-09-14 |

## Rating path of the current submission

game 1: 697, game 10: 1566, game 25: 2564, game 50: 2826, game 100: 2928, game last: nan

![rating](figs/elmo_rating.png)

## Farm plan by window (median per game)

| median per game | F | L | C0 |
|---|---|---|---|
| hands (peak) | 12 | 12 | 12 |
| quadrants | 3 | 3 | 3 |
| land day 1 | 6 | 6 | 6 |
| land day 2 | 11 | 11 | 11 |
| cows bought | 8 | 8 | 7 |
| sheep bought | 9 | 6 | 6 |
| geese bought | 0 | 3 | 3 |
| first cow day | 0 | 0 | 0 |
| wheat planted | 194 | 162 | 158 |
| carrot planted | 9 | 31 | 35 |
| tomato planted | 0 | 0 | 0 |
| strawberry planted | 34 | 33 | 33 |
| melon planted | 12 | 12 | 12 |
| FERTILIZE ops | 75 | 116 | 112.5 |
| CARE ops | 373 | 405 | 405 |
| melon sold | 72 | 72 | 72 |
| strawberry sold | 262 | 250 | 250 |
| milk sold | 240 | 192 | 191 |
| wool sold | 216 | 136.5 | 139 |
| wheat sold | 393 | 1289 | 1251.5 |
| fertilizer sold | 360 | 329 | 329 |
| units sold last 3 days | 353 | 386.5 | 387.5 |
| shed peak | 64 | 45 | 45 |
| weeds spawned | 27 | 19 | 19 |
| unexecutable market orders | 0 | 1 | 1 |

![money by day](figs/elmo_money.png)

## A typical recent game, day by day

Episode 109055944 (the median-bank game of the latest window): seat 1, bank 91669 vs 90590 (MMN0222), seed 1579934942. Letters: W wheat, C carrot, T tomato, S strawberry, M melon, E egg, Mk milk, Wl wool, F fertilizer.

| day | money | hands | quads | bought | built | planted | care/fert | harvest | sold | revenue | farm at day end | new weeds | shop unlock |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3000 | 5 | 1 | cow2 sheep2 \| W7 M12 | pasture 4  | W7 M12 | 3/0 | 0 | W15 | 430 | cow2 sheep2; W7 M12 |  |  |
| 1 | 22 | 3 | 1 |  | pasture 2  |  | 4/0 | 0 | F3 | 299 | cow2 sheep2; W7 M12; empty pens 2 |  |  |
| 2 | 81 | 4 | 1 | cow1 \| W3 |  | W3 | 5/0 | 3 | W2 F5 | 550 | cow3 sheep2; W7 M12; empty pens 1 |  |  |
| 3 | 194 | 5 | 1 | cow1 \| W4 |  | W4 | 6/0 | 4 | W5 F4 | 535 | cow3 sheep2; W7 M12; empty pens 1 |  | Pizza |
| 4 | 277 | 4 | 1 | W3 |  | W3 | 6/0 | 3 | W2 F6 | 625 | cow4 sheep2; W7 M12 |  |  |
| 5 | 682 | 4 | 1 | S4 |  | S4 | 7/0 | 4 | W2 F5 | 522 | cow4 sheep2; W3 S4 M12 |  |  |
| 6 | 797 | 7 | 2 | cow2 \| W5 S8 | pasture 7  | W5 S8 | 8/0 | 5 | W9 Wl12 F9 | 3509 | cow6 sheep2; W6 S12 M12; empty pens 5 |  | Farmers Market |
| 7 | 1118 | 7 | 2 | cow2 \| W4 S4 |  | W4 S4 | 11/0 | 0 | F9 | 780 | cow8 sheep2; W8 S16 M12; empty pens 3 |  |  |
| 8 | 538 | 8 | 2 | sheep2 \| W1 S4 |  | W1 S4 | 13/0 | 7 | W2 Mk12 F10 | 3385 | cow8 sheep4; W5 S20 M12; empty pens 1 |  |  |
| 9 | 1646 | 8 | 2 | sheep2 \| W4 |  | W4 | 15/0 | 6 | W2 Wl8 F14 | 2564 | cow8 sheep5; W5 S20 M12 |  | Bakery |
| 10 | 2370 | 11 | 2 | goose2 \| W7 | pasture 1 coop 4 | W7 | 16/0 | 15 | W3 M60 Mk12 F9 | 16225 | goose2 cow8 sheep6; W12 S20; empty pens 2 |  |  |
| 11 | 16020 | 10 | 3 | goose1 \| W11 S13 |  | W11 S13 | 18/0 | 4 | W9 M12 Mk6 F14 | 3781 | goose3 cow8 sheep6; W21 S33; empty pens 1 |  |  |
| 12 | 15009 | 9 | 3 | W8 |  | W8 | 17/0 | 8 | W9 Mk6 Wl8 F16 | 3542 | goose3 cow8 sheep6; W24 S33; empty pens 1 |  | Farmers Market |
| 13 | 18383 | 9 | 3 | W6 |  | W6 | 19/2 | 8 | W19 Mk6 F17 | 2795 | goose3 cow8 sheep6; W24 S33; empty pens 1 |  |  |
| 14 | 21030 | 9 | 3 | W7 |  | W7 | 16/5 | 16 | Mk12 Wl12 F15 | 2923 | goose3 cow8 sheep6; W24 S33; empty pens 1 |  |  |
| 15 | 23594 | 10 | 3 | W8 |  | W7 | 17/8 | 19 | W8 S8 E6 Mk24 F16 | 4787 | goose3 cow8 sheep6; W24 S33 |  | Brunch Spot |
| 16 | 27959 | 11 | 3 | W8 |  | W8 | 18/4 | 23 | W6 S16 E6 Mk12 Wl17 F11 | 4449 | goose3 cow8 sheep6; W25 S33 |  |  |
| 17 | 32052 | 11 | 3 | W7 |  | W7 | 17/4 | 22 | W7 S16 E4 Mk3 F10 | 4057 | goose3 cow8 sheep6; W25 S33 |  |  |
| 18 | 35807 | 13 | 4 | W7 T10 |  | W7 T10 | 17/4 | 28 | W9 S16 E4 Mk5 Wl4 F14 | 4178 | goose3 cow8 sheep6; W25 T10 S33 |  | Pet Cafe |
| 19 | 34771 | 11 | 4 | W6 |  | W6 | 17/8 | 20 | W3 S18 E6 Mk7 Wl2 F9 | 3962 | goose3 cow8 sheep6; W25 T10 S33; weeds 1 | 1 |  |
| 20 | 38441 | 12 | 4 | W6 |  | W6 | 17/16 | 26 | W6 S26 E8 Mk4 Wl1 F6 | 5069 | goose3 cow8 sheep6; W25 T10 S33; weeds 1 |  |  |
| 21 | 42921 | 12 | 4 | W11 |  | W11 | 17/3 | 35 | W186 S28 E7 Mk3 Wl4 F13 | 12382 | goose3 cow8 sheep6; W30 T10 S28; weeds 1 |  | Farmers Market |
| 22 | 48062 | 12 | 4 | W8 C11 |  | W5 C3 | 17/9 | 27 | W211 S22 E6 Mk7 Wl3 F18 | 11425 | goose3 cow8 sheep6; W28 C3 T10 S27; weeds 1 | 1 |  |
| 23 | 49262 | 13 | 4 | W14 |  | W6 C8 | 17/6 | 31 | W240 S21 E6 Mk4 Wl4 F19 | 12057 | goose3 cow8 sheep6; W27 C11 T10 S20; weeds 2 | 8 |  |
| 24 | 50776 | 13 | 4 | W9 C4 |  | W9 C4 | 17/29 | 24 | W30 S22 E8 Mk4 Wl7 F5 | 2172 | goose3 cow8 sheep6; W26 C15 T10 S17; weeds 2 | 3 | Pizza |
| 25 | 51851 | 13 | 4 | C15 |  | C14 | 17/8 | 29 | W150 S11 E4 Mk9 Wl1 F16 | 7480 | goose3 cow8 sheep6; W19 C26 T10 S13; weeds 2 | 4 |  |
| 26 | 53254 | 14 | 4 | W1 C19 |  | C12 | 17/6 | 28 | W230 C10 T12 S15 E2 Mk6 Wl3 F13 | 15786 | goose3 cow8 sheep6; W15 C30 T10 S13; weeds 2 |  |  |
| 27 | 58606 | 13 | 4 | W8 C2 |  | C10 | 17/10 | 43 | W13 C28 T28 S12 E2 Mk7 Wl4 F20 | 12407 | goose2 cow8 sheep6; W9 C35 T10 S4; weeds 2 empty pens 1 |  |  |
| 28 | 70155 | 13 | 4 |  | coop 1 |  | 15/0 | 38 | W33 C20 T20 S20 E4 Mk4 Wl4 F15 | 9751 | goose2 cow8 sheep6; W1 C22 T10; weeds 2 empty pens 2 | 4 |  |
| 29 | 79297 | 13 | 4 |  |  |  | 4/0 | 43 | W44 C85 T20 E7 Mk17 Wl5 F8 | 12995 | goose2 cow8 sheep6; T10; weeds 2 empty pens 2 |  |  |

## Determinism

Distinct action lines per window at each turn cut, with the share of the largest line in brackets.

**Field actions (farmer + hands)**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 1 (100%) | 3 (88%) | 3 (88%) | 3 (88%) | 6 (86%) | 9 (82%) | 10 (80%) | 10 (80%) |
| L | 50 | 4 (94%) | 5 (90%) | 5 (90%) | 5 (90%) | 12 (50%) | 18 (34%) | 34 (14%) | 50 (2%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 6 (50%) | 8 (34%) | 34 (16%) | 50 (2%) |

**Market orders**

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 1 (100%) | 1 (100%) | 1 (100%) | 1 (100%) | 2 (60%) | 6 (40%) | 24 (10%) | 49 (4%) |
| L | 50 | 4 (94%) | 4 (94%) | 4 (94%) | 4 (94%) | 8 (52%) | 14 (36%) | 33 (12%) | 50 (2%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 5 (50%) | 9 (34%) | 34 (12%) | 50 (2%) |

**Plans (order-insensitive)**: same multiset of non-movement unit ops and market orders through the cut, regardless of path or hand order.

| window | games | h24 | h48 | h100 | h136 | h200 | h300 | h400 | h719 |
|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 1 (100%) | 3 (88%) | 3 (88%) | 3 (88%) | 6 (86%) | 7 (82%) | 7 (80%) | 7 (80%) |
| L | 50 | 4 (94%) | 5 (90%) | 5 (90%) | 5 (90%) | 12 (50%) | 18 (34%) | 35 (14%) | 50 (2%) |
| C0 | 50 | 3 (96%) | 3 (96%) | 3 (96%) | 3 (96%) | 6 (50%) | 10 (34%) | 32 (16%) | 50 (2%) |

Current submission (73 sampled games): field is **one line through turn 136 (92%), then branching (5 lines at turn 136, 48 at turn 400); every game distinct by turn 719**; market is **one line through turn 136 (95%), then branching (4 lines at turn 136, 46 at turn 400); every game distinct by turn 719**; plan is **one line through turn 136 (92%), then branching (5 lines at turn 136, 45 at turn 400); every game distinct by turn 719**.

Games on the modal field line, by cut (current submission):

| turn | day | distinct lines | on modal line | share % |
|---|---|---|---|---|
| 24 | 1 | 4 | 69 | 94.5 |
| 48 | 2 | 5 | 67 | 91.8 |
| 100 | 4 | 5 | 67 | 91.8 |
| 136 | 5 | 5 | 67 | 91.8 |
| 200 | 8 | 11 | 37 | 50.7 |
| 300 | 12 | 15 | 21 | 28.8 |
| 400 | 16 | 48 | 11 | 15.1 |
| 719 | 29 | 73 | 1 | 1.4 |

What goes with being off the modal field line at turn 200 (the first cut where fewer than 90% of games share one line):

| condition | games with condition | off-line % (condition) | off-line % (without) |
|---|---|---|---|
| weeds on own farm before day 8 | 3 | 100 | 47.1 |
| opponent off its modal line at turn 136 | 36 | 41.7 | 56.8 |
| played seat 1 | 42 | 47.6 | 51.6 |
| lost the game | 12 | 58.3 | 47.5 |
| first shop (day 3) is not Bakery | 60 | 46.7 | 61.5 |

## Evolution across windows

| window | games | win % | median bank | hands | cows | sheep | geese | quadrants | land day 1 | strawberry | wheat | melon | melon sold | milk sold | wool sold | field lines @400 | market lines @400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 50 | 88 | 93357 | 12 | 8 | 9 | 0 | 3 | 6 | 34 | 194 | 12 | 72 | 240 | 216 | 10 | 24 |
| L | 50 | 70 | 91041.5 | 12 | 8 | 6 | 3 | 3 | 6 | 33 | 162 | 12 | 72 | 192 | 136.5 | 34 | 33 |
| C0 | 50 | 92 | 106007.5 | 12 | 7 | 6 | 3 | 3 | 6 | 33 | 158 | 12 | 72 | 191 | 139 | 34 | 34 |

## Losses in the first and last windows

| window | episode | opponent | opp rating | my bank | opp bank | margin | opp opening | biggest differences (opponent vs me) |
|---|---|---|---|---|---|---|---|---|
| F | 105403966 | nvidia fan | 1262.6 | 93254 | 113564 | -20310 | d2e738f9 | CARE ops: they 276 vs me 373; wheat planted: they 105 vs me 194; wool sold: they 128 vs me 216 |
| F | 105409510 | Kaipeng Zheng | 1433.0 | 0 | 120074 | -120074 | 87b52758 | units sold last 3 days: they 334 vs me 0; CARE ops: they 351 vs me 80; milk sold: they 270 vs me 0 |
| F | 105419625 | mandgeee | 1621.0 | 0 | 152372 | -152372 | 87b52758 | units sold last 3 days: they 313 vs me 0; CARE ops: they 351 vs me 80; strawberry sold: they 270 vs me 0 |
| F | 105422966 | philip georgiev | 1791.4 | 0 | 142582 | -142582 | 3bc18d7a | units sold last 3 days: they 335 vs me 0; CARE ops: they 381 vs me 80; strawberry sold: they 254 vs me 0 |
| F | 105423009 | OceFFFF | 1713.1 | 0 | 181635 | -181635 | 3bc18d7a | units sold last 3 days: they 343 vs me 0; CARE ops: they 384 vs me 90; milk sold: they 261 vs me 0 |
| F | 105431752 | Maham Haroon | 1739.5 | 0 | 162770 | -162770 | 3bc18d7a | units sold last 3 days: they 344 vs me 0; CARE ops: they 384 vs me 80; strawberry sold: they 262 vs me 0 |
| C0 | 108992350 | ManasviSharma | 2744.9 | 83290 | 84734 | -1444 | 9b0c82fd | units sold last 3 days: they 389 vs me 371; CARE ops: they 397 vs me 400; FERTILIZE ops: they 106 vs me 109 |
| C0 | 108995432 | TIM | 2781.2 | 145778 | 145873 | -95 | 9b0c82fd | wheat planted: they 163 vs me 154; units sold last 3 days: they 434 vs me 439; FERTILIZE ops: they 125 vs me 122 |
| C0 | 108996452 | Phi | 2713.5 | 81166 | 81310 | -144 | 9b0c82fd | units sold last 3 days: they 363 vs me 411; milk sold: they 114 vs me 160; wool sold: they 411 vs me 367 |
| C0 | 109001674 | alcanta | 2848.5 | 90609 | 91472 | -863 | 9b0c82fd | milk sold: they 154 vs me 178; units sold last 3 days: they 387 vs me 373; CARE ops: they 397 vs me 400 |
| L | 109031094 | ElephtAI | 2915.1 | 93351 | 93529 | -178 | 9b0c82fd | FERTILIZE ops: they 94 vs me 123; units sold last 3 days: they 375 vs me 390; CARE ops: they 417 vs me 405 |
| L | 109035387 | sonny_01 | 2814.4 | 106688 | 107556 | -868 | 9b0c82fd | units sold last 3 days: they 394 vs me 385; strawberry sold: they 249 vs me 251; hands (peak): they 11 vs me 12 |
| L | 109040343 | Cow Boy | 2943.6 | 76897 | 77632 | -735 | 83322aec | units sold last 3 days: they 393 vs me 375; CARE ops: they 397 vs me 400; strawberry sold: they 249 vs me 248 |
| L | 109051739 | Artem The Farmer 🍅 | 3021.3 | 74976 | 87865 | -12889 | d6cc83df | strawberry sold: they 143 vs me 249; CARE ops: they 321 vs me 405; wool sold: they 218 vs me 147 |
| L | 109058929 | Team Amboss | 2754.4 | 89589 | 89600 | -11 | 9b0c82fd | units sold last 3 days: they 383 vs me 377; weeds spawned: they 21 vs me 19 |
| L | 109061964 | feel the agi | 2962.0 | 124321 | 128943 | -4622 | 3bc18d7a | FERTILIZE ops: they 175 vs me 102; CARE ops: they 356 vs me 405; wool sold: they 61 vs me 106 |
| L | 109063107 | Seho.Connect | 2892.7 | 86844 | 90766 | -3922 | 9b0c82fd | milk sold: they 228 vs me 147; units sold last 3 days: they 394 vs me 374; FERTILIZE ops: they 110 vs me 103 |
| L | 109068224 | TIM | 2775.2 | 75542 | 78250 | -2708 | 9b0c82fd | wool sold: they 263 vs me 257; milk sold: they 135 vs me 140; units sold last 3 days: they 386 vs me 389 |
| L | 109070285 | AI是我的豆包 | 2845.6 | 115253 | 115804 | -551 | 3bc18d7a | wool sold: they 219 vs me 152; milk sold: they 192 vs me 242; units sold last 3 days: they 393 vs me 378 |
| L | 109071727 | xiao xiongwei | 2784.8 | 76752 | 80033 | -3281 | 9b0c82fd | units sold last 3 days: they 394 vs me 375; CARE ops: they 397 vs me 400; FERTILIZE ops: they 106 vs me 109 |
| L | 109075428 | Munal Singh | 2884.3 | 76120 | 77131 | -1011 | 9b0c82fd | units sold last 3 days: they 381 vs me 385; strawberry sold: they 249 vs me 251 |
| L | 109077541 | WBF_USA_NYC | 2820.4 | 73183 | 73557 | -374 | 9b0c82fd | FERTILIZE ops: they 61 vs me 95; units sold last 3 days: they 390 vs me 415; CARE ops: they 506 vs me 508 |
| L | 109080105 | xiao xiongwei | 2788.1 | 101842 | 103599 | -1757 | 9b0c82fd | units sold last 3 days: they 399 vs me 387; CARE ops: they 401 vs me 410; FERTILIZE ops: they 123 vs me 117 |
| L | 109086691 | keiz | 2925.6 | 80539 | 96041 | -15502 | 01b4205d | strawberry sold: they 84 vs me 241; milk sold: they 303 vs me 212; units sold last 3 days: they 299 vs me 362 |
| L | 109092825 | Orbital Terraformer | 3020.4 | 135191 | 144788 | -9597 | a87c2093 | FERTILIZE ops: they 174 vs me 102; milk sold: they 326 vs me 266; CARE ops: they 358 vs me 405 |

## Head to head with the other studied teams (all games, not only sampled)

| opp_team_id | W | L | T |
|---|---|---|---|
| 16621799 | 0 | 2 | 0 |
| 16622198 | 5 | 2 | 0 |
| 16622349 | 6 | 2 | 0 |
| 16622459 | 1 | 2 | 0 |
| 16626191 | 1 | 0 | 0 |
| 16633100 | 2 | 1 | 0 |
| 16633178 | 4 | 5 | 0 |
| 16633944 | 0 | 1 | 0 |
| 16637255 | 1 | 4 | 0 |
| 16640510 | 3 | 5 | 0 |
| 16641710 | 3 | 3 | 0 |
| 16644724 | 0 | 8 | 1 |
| 16655383 | 1 | 1 | 0 |
| 16658554 | 6 | 1 | 0 |
| 16660726 | 1 | 5 | 0 |
| 16664246 | 0 | 3 | 0 |
| 16671741 | 0 | 3 | 0 |
| 16675778 | 1 | 2 | 0 |
| 16683936 | 4 | 1 | 0 |
| 16684093 | 1 | 4 | 0 |
| 16706321 | 2 | 1 | 0 |
| 16719123 | 7 | 4 | 1 |
| 16723379 | 3 | 2 | 0 |
| 16725899 | 2 | 1 | 0 |
| 16728071 | 3 | 7 | 0 |
| 16730524 | 4 | 1 | 0 |
| 16730612 | 0 | 2 | 0 |
| 16730761 | 3 | 3 | 0 |
| 16731275 | 3 | 5 | 0 |
| 16732403 | 0 | 1 | 0 |
| 16732521 | 4 | 7 | 0 |
| 16732748 | 1 | 0 | 0 |
| 16741542 | 4 | 6 | 0 |
| 16758882 | 3 | 6 | 0 |
| 16760569 | 1 | 2 | 0 |
| 16761744 | 1 | 0 | 0 |
| 16773026 | 3 | 2 | 0 |
| 16777134 | 2 | 0 | 0 |
| 16778640 | 4 | 1 | 0 |
| 16781445 | 0 | 1 | 0 |
| 16802867 | 1 | 0 | 0 |
| 16805699 | 2 | 4 | 0 |
| 16809332 | 1 | 1 | 0 |
| 16810299 | 1 | 0 | 0 |
| 16833141 | 2 | 1 | 0 |
| 16845367 | 2 | 1 | 0 |
| 16848479 | 0 | 3 | 0 |
| 16848532 | 2 | 0 | 0 |
| 16858228 | 2 | 1 | 0 |
| 16879253 | 1 | 0 | 0 |
| 16882725 | 0 | 1 | 0 |

## Episodes behind each window

- **F** (50): 105398783, 105399659, 105400513, 105401375, 105402246, 105403100, 105403966, 105404835, 105405711, 105406593, 105407538, 105408439, 105409304, 105409510, 105410181, 105411039, 105411903, 105412823, 105413816, 105415021, 105415888, 105416763, 105417644, 105418526, 105419426, 105419625, 105420305, 105421207, 105422080, 105422949, 105422966, 105423009, 105423815, 105424810, 105425640, 105426473, 105427344, 105428231, 105429109, 105429995, 105430874, 105431752, 105432643, 105433525, 105434417, 105435298, 105436175, 105437062, 105437950, 105438839
- **L** (50): 109031094, 109035387, 109036018, 109038953, 109040343, 109041454, 109041867, 109045718, 109046423, 109046453, 109050414, 109050682, 109051739, 109054681, 109055944, 109057418, 109058929, 109059159, 109061964, 109063077, 109063107, 109063667, 109063915, 109064622, 109064815, 109068081, 109068224, 109069376, 109070101, 109070285, 109071727, 109071870, 109072372, 109072377, 109075428, 109076555, 109077541, 109078048, 109078338, 109080105, 109080492, 109081680, 109085374, 109086691, 109086755, 109090535, 109091924, 109092825, 109094777, 109095318
- **C0** (50): 108961224, 108962536, 108963273, 108964259, 108965302, 108966322, 108967367, 108968352, 108969385, 108970418, 108971435, 108972472, 108973498, 108974522, 108975553, 108976583, 108977649, 108978675, 108979717, 108980797, 108981816, 108982887, 108983928, 108984958, 108986007, 108987035, 108987707, 108988092, 108988434, 108989410, 108990187, 108991230, 108991534, 108992276, 108992350, 108993328, 108994368, 108994522, 108995432, 108996452, 108997477, 108997500, 108998525, 108999567, 109000611, 109000667, 109001103, 109001674, 109002693, 109003739
