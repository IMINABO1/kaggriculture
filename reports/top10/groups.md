# Top-14 vs next-15

Snapshot 2026-09-15T0033Z. The top-14 are the teams that were top-10 in Iminabo's screenshot or on the live board on 2026-09-14; the next-15 are chunks of the gold zone outside them (ranks 8-48 at snapshot time, 15 teams with replays). Under Kaggle's medal rule for 9,066 teams (gold = top 10 + 0.2% = rank 28, silver = top 5%), ranks 8-23 of the batch are gold and 29-48 silver; under the top-50 working assumption all are gold. Every number below is a per-team median over the C0 window only (the current submission's first 50 games), compared across teams: 'P(top > next)' is the chance that a random top-14 team's value is above a random next-15 team's (0.5 = no separation), 'p' is the two-sided Mann-Whitney test. Numbers are per game unless stated. Teams with fewer than 10 sampled games of their current submission are left out of the comparison.

## Who is in each group

| rank | team | group | score | public_games | current_sub_games | Kaggle medal zone | sampled current-sub games |
|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top-14 | 3216.9 | 1497 | 331 | gold | 50 |
| 2 | DSM | top-14 | 3062.9 | 8825 | 80 | gold | 50 |
| 3 | Artem The Farmer 🍅 | top-14 | 3043.9 | 2070 | 86 | gold | 50 |
| 4 | Orbital Terraformer | top-14 | 3022.2 | 1831 | 187 | gold | 50 |
| 5 | SpaTaro | top-14 | 3014.1 | 4642 | 456 | gold | 50 |
| 6 | Mengfei Li | top-14 | 3014 | 10390 | 374 | gold | 50 |
| 7 | ymg_aq | top-14 | 3011.7 | 5367 | 178 | gold | 50 |
| 8 | Unknown Mother-Goose | next-15 | 3007 | 3035 | 107 | gold | 50 |
| 9 | HowardLeeTW | top-14 | 2991.1 | 2348 | 194 | gold | 50 |
| 10 | アルモンド | top-14 | 2977.2 | 3153 | 82 | gold | 50 |
| 11 | leave you | next-15 | 2971.6 | 9900 | 112 | gold | 50 |
| 13 | Thomas Tschinkel | top-14 | 2970.2 | 8950 | 110 | gold | 50 |
| 14 | Catalyst | top-14 | 2968.2 | 906 | 105 | gold | 50 |
| 15 | redblackbst | top-14 | 2966.9 | 5329 | 115 | gold | 50 |
| 16 | feel the agi | top-14 | 2961.4 | 3449 | 562 | gold | 50 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | next-15 | 2950.3 | 728 | 136 | gold | 50 |
| 18 | Otter Vibe | top-14 | 2949.6 | 2511 | 721 | gold | 50 |
| 19 | Zhenghongshuang | next-15 | 2945.8 | 5279 | 144 | gold | 50 |
| 20 | kyy666 | next-15 | 2938.3 | 1600 | 116 | gold | 50 |
| 21 | Kilupy | next-15 | 2934.9 | 890 | 86 | gold | 50 |
| 22 | elmo | next-15 | 2932.4 | 3469 | 102 | gold | 50 |
| 23 | ElephtAI | next-15 | 2932.1 | 5736 | 141 | gold | 50 |
| 29 | Emile Andrieu | next-15 | 2912.9 | 3653 | 120 | silver | 50 |
| 30 | mtmr_s1 | next-15 | 2912.3 | 5969 | 113 | silver | 50 |
| 31 | Kaggriculture Agent | next-15 | 2912 | 8989 | 116 | silver | 50 |
| 38 | THUNDER THUNDER | next-15 | 2899.3 | 7231 | 395 | silver | 50 |
| 39 | yomogii | next-15 | 2897.5 | 2690 | 96 | silver | 50 |
| 47 | doubao | next-15 | 2885.7 | 1630 | 226 | silver | 50 |
| 48 | Tom&Jerry | next-15 | 2884.9 | 5368 | 154 | silver | 50 |

## What separates the groups

- **weed tile-days per weed**: top-14 median 0.6 vs next-15 0; a random top-14 team is above a random next-15 team 85% of the time (p = 0.001)
- **weed tile-days**: top-14 median 10.5 vs next-15 0; a random top-14 team is above a random next-15 team 85% of the time (p = 0.001)
- **strawberry first sell day**: top-14 median 15.5 vs next-15 19; a random top-14 team is above a random next-15 team 15% of the time (p = 0.001)
- **weed tiles standing (peak)**: top-14 median 4.5 vs next-15 0; a random top-14 team is above a random next-15 team 84% of the time (p = 0.001)
- **strawberry planted**: top-14 median 31 vs next-15 33; a random top-14 team is above a random next-15 team 18% of the time (p = 0.001)
- **distinct % at 400**: top-14 median 100 vs next-15 74; a random top-14 team is above a random next-15 team 81% of the time (p = 0.003)
- **CARE ops**: top-14 median 338 vs next-15 403; a random top-14 team is above a random next-15 team 20% of the time (p = 0.005)
- **melon last sell day**: top-14 median 20 vs next-15 11; a random top-14 team is above a random next-15 team 79% of the time (p = 0.003)
- **wool first sell day**: top-14 median 8.5 vs next-15 6; a random top-14 team is above a random next-15 team 77% of the time (p = 0.007)
- **melon planted**: top-14 median 13 vs next-15 12; a random top-14 team is above a random next-15 team 77% of the time (p = 0.006)
- **FERTILIZE ops**: top-14 median 151 vs next-15 113; a random top-14 team is above a random next-15 team 75% of the time (p = 0.021)
- **land day 2**: top-14 median 9.5 vs next-15 11; a random top-14 team is above a random next-15 team 26% of the time (p = 0.006)
- **unexecutable market orders**: top-14 median 0 vs next-15 1; a random top-14 team is above a random next-15 team 26% of the time (p = 0.016)
- **field branch turn**: top-14 median 74 vs next-15 200; a random top-14 team is above a random next-15 team 26% of the time (p = 0.013)
- **milk first sell day**: top-14 median 11 vs next-15 12; a random top-14 team is above a random next-15 team 28% of the time (p = 0.034)
- **rating after game 10**: top-14 median 1491 vs next-15 1583; a random top-14 team is above a random next-15 team 28% of the time (p = 0.045)
- **plan branch turn**: top-14 median 74 vs next-15 200; a random top-14 team is above a random next-15 team 29% of the time (p = 0.039)
- **melon sold**: top-14 median 18.2 vs next-15 12; a random top-14 team is above a random next-15 team 71% of the time (p = 0.037)
- **sheep bought**: top-14 median 5 vs next-15 6; a random top-14 team is above a random next-15 team 30% of the time (p = 0.038)
- **geese bought**: top-14 median 2 vs next-15 3; a random top-14 team is above a random next-15 team 31% of the time (p = 0.042)

## What does not separate them (p >= 0.2 and P(top > next) within 0.35-0.65)

- quadrants (3 vs 3)
- cows bought (7.8 vs 8)
- rating after game 25 (2551 vs 2559)
- units sold total (1161 vs 1121)
- rating after game 50 (2860 vs 2839)
- final money (105084 vs 102744)
- wheat planted (158 vs 162)
- hands (peak) (12 vs 12)
- wool sold (67 vs 74)
- weeds spawned (19 vs 20)
- land day 1 (6 vs 6)
- units sold last 3 days (260 vs 266)
- opp rating (2167 vs 2185)
- games to 2900 (58 vs 70)
- melon first sell day (11 vs 11)
- milk sold (125 vs 112)
- DIG ops (36 vs 37)

![rating paths by group](figs/group_rating.png)

![per-team medians by group](figs/group_strip.png)

## Determinism and branch point (current submissions)

Branch turn: the first cut at which fewer than 90% of a team's games share one line (720 = one line to the end). Driver: the condition whose presence moves the off-line rate by 25+ points at that cut (weed on own farm before that day, opponent off its own modal line at the previous cut, seat, first shop draw).

| rank | team | group | games | field branch turn | plan branch turn | distinct % at 400 | driver | driver gap | field branch |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top-14 | 50 | 24 | 24 | 100 | opponent | 56.5 | day 1 |
| 2 | DSM | top-14 | 50 | 24 | 24 | 100 | none | 15.1 | day 1 |
| 3 | Artem The Farmer 🍅 | top-14 | 50 | 200 | 200 | 100 | opponent | 30 | day 8-16 |
| 4 | Orbital Terraformer | top-14 | 50 | 24 | 24 | 100 | opponent | 60.9 | day 1 |
| 5 | SpaTaro | top-14 | 50 | 24 | 24 | 100 | none | 3.8 | day 1 |
| 6 | Mengfei Li | top-14 | 50 | 24 | 200 | 100 | none | -8.1 | day 1 |
| 7 | ymg_aq | top-14 | 50 | 100 | 100 | 100 | none | -17.1 | day 4-6 |
| 8 | Unknown Mother-Goose | next-15 | 50 | 200 | 136 | 100 | weed | 43.5 | day 8-16 |
| 9 | HowardLeeTW | top-14 | 50 | 48 | 48 | 100 | seat | 87.1 | day 2 |
| 10 | アルモンド | top-14 | 50 | 200 | 100 | 98 | weed | 32.5 | day 8-16 |
| 11 | leave you | next-15 | 50 | 200 | 200 | 54 | seat | -27.0 | day 8-16 |
| 13 | Thomas Tschinkel | top-14 | 50 | 200 | 200 | 70 | weed | 52.2 | day 8-16 |
| 14 | Catalyst | top-14 | 50 | 24 | 24 | 72 | none | -24 | day 1 |
| 15 | redblackbst | top-14 | 50 | 200 | 200 | 98 | none | -17.5 | day 8-16 |
| 16 | feel the agi | top-14 | 50 | 200 | 24 | 98 | shop | -30 | day 8-16 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | next-15 | 50 | 200 | 200 | 68 | shop | -30 | day 8-16 |
| 18 | Otter Vibe | top-14 | 50 | 100 | 100 | 100 | shop | -40.8 | day 4-6 |
| 19 | Zhenghongshuang | next-15 | 50 | 200 | 200 | 66 | weed | 70.2 | day 8-16 |
| 20 | kyy666 | next-15 | 50 | 200 | 200 | 72 | seat | -35.9 | day 8-16 |
| 21 | Kilupy | next-15 | 50 | 200 | 200 | 76 | none | -24.1 | day 8-16 |
| 22 | elmo | next-15 | 50 | 200 | 200 | 68 | none | -20 | day 8-16 |
| 23 | ElephtAI | next-15 | 50 | 200 | 100 | 70 | none | -21.4 | day 8-16 |
| 29 | Emile Andrieu | next-15 | 50 | 200 | 200 | 84 | weed | 36.4 | day 8-16 |
| 30 | mtmr_s1 | next-15 | 50 | 200 | 100 | 100 | weed | 55.3 | day 8-16 |
| 31 | Kaggriculture Agent | next-15 | 50 | 24 | 24 | 54 | none | 16.0 | day 1 |
| 38 | THUNDER THUNDER | next-15 | 50 | 100 | 100 | 100 | none | 14.6 | day 4-6 |
| 39 | yomogii | next-15 | 50 | 48 | 24 | 82 | none | -20.1 | day 2 |
| 47 | doubao | next-15 | 50 | 200 | 200 | 76 | shop | 45.7 | day 8-16 |
| 48 | Tom&Jerry | next-15 | 50 | 200 | 200 | 74 | weed | 31.1 | day 8-16 |

| first field branch | top-14 teams | next-15 teams |
|---|---|---|
| day 1 | 6 | 1 |
| day 2 | 1 | 1 |
| day 4-6 | 2 | 1 |
| day 8-16 | 5 | 12 |
| end-game only | 0 | 0 |
| fixed | 0 | 0 |

| dominant driver at the first branch | top-14 teams | next-15 teams |
|---|---|---|
| opponent | 3 | 0 |
| weed | 2 | 5 |
| seat | 1 | 2 |
| shop | 2 | 2 |
| none | 6 | 6 |

Teams whose modal field line (farmer and hand actions) is byte-identical to another studied team's through the cut, i.e. members of a shared plan family, and the size of the largest family at that cut:

| turn | day | top-14 on a shared line | next-15 on a shared line | largest family |
|---|---|---|---|---|
| 24 | 1 | 5 of 14 | 13 of 15 | 13 |
| 48 | 2 | 3 of 14 | 12 of 15 | 13 |
| 100 | 4 | 3 of 14 | 11 of 15 | 12 |
| 136 | 5 | 3 of 14 | 11 of 15 | 12 |
| 200 | 8 | 2 of 14 | 11 of 15 | 7 |
| 300 | 12 | 2 of 14 | 9 of 15 | 4 |
| 400 | 16 | 1 of 14 | 3 of 15 | 2 |

## Feature comparison

**Outcome**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| win % | 97 | 90 to 100 | 94 | 86 to 100 | 0.66 | 0.14 |
| opp rating | 2166.67 | 1420.2 to 2269.7 | 2184.52 | 2010.7 to 2319.3 | 0.42 | 0.48 |
| final money | 105084.50 | 93960 to 118371 | 102744.50 | 99096 to 119640 | 0.55 | 0.63 |

**Determinism**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| field branch turn | 74 | 24 to 200 | 200 | 24 to 200 | 0.26 | 0.01 |
| plan branch turn | 74 | 24 to 200 | 200 | 24 to 200 | 0.29 | 0.04 |
| distinct % at 400 | 100 | 70 to 100 | 74 | 54 to 100 | 0.81 | 0.00 |

**Farm plan**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| hands (peak) | 12 | 11 to 15 | 12 | 11 to 12 | 0.56 | 0.53 |
| quadrants | 3 | 3 to 3 | 3 | 3 to 3 | 0.50 | 1 |
| land day 1 | 6 | 3 to 6 | 6 | 4 to 6 | 0.43 | 0.27 |
| land day 2 | 9.50 | 8 to 11 | 11 | 8 to 11 | 0.26 | 0.01 |
| cows bought | 7.75 | 7 to 10 | 8 | 6 to 9 | 0.49 | 0.93 |
| sheep bought | 5 | 3 to 8 | 6 | 3 to 6 | 0.30 | 0.04 |
| geese bought | 2 | 0 to 6 | 3 | 2 to 3 | 0.31 | 0.04 |
| strawberry planted | 31 | 23 to 33 | 33 | 29.5 to 33 | 0.18 | 0.00 |
| wheat planted | 158.25 | 103.5 to 188.5 | 162 | 141 to 166 | 0.44 | 0.60 |
| melon planted | 13 | 11 to 16 | 12 | 12 to 14 | 0.77 | 0.01 |
| CARE ops | 338 | 247 to 410 | 403 | 301.5 to 440 | 0.20 | 0.01 |
| FERTILIZE ops | 151.25 | 83 to 193.5 | 113 | 103 to 182 | 0.75 | 0.02 |

**Market**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| melon sold | 18.25 | 0 to 72 | 12 | 12 to 24 | 0.71 | 0.04 |
| strawberry sold | 170.50 | 50 to 224.5 | 129 | 121 to 216.5 | 0.71 | 0.06 |
| milk sold | 125.25 | 23 to 188.5 | 111.50 | 95.5 to 154 | 0.62 | 0.26 |
| wool sold | 67.25 | 26.5 to 109 | 74.50 | 29.5 to 109 | 0.44 | 0.56 |
| units sold last 3 days | 260 | 196.5 to 362.5 | 266 | 227.5 to 569 | 0.43 | 0.51 |
| units sold total | 1161 | 774.5 to 1586.5 | 1121 | 1077.5 to 4682 | 0.49 | 0.90 |
| melon first sell day | 11 | 10 to 22 | 11 | 11 to 17.5 | 0.40 | 0.24 |
| melon last sell day | 20.25 | 11 to 28 | 11 | 11 to 22 | 0.79 | 0.00 |
| strawberry first sell day | 15.50 | 13 to 19 | 19 | 15 to 19 | 0.15 | 0.00 |
| milk first sell day | 11 | 8 to 14 | 12 | 9 to 15 | 0.28 | 0.03 |
| wool first sell day | 8.50 | 6 to 16 | 6 | 6 to 7 | 0.77 | 0.01 |

**Weeds and repair**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| weeds spawned | 19 | 3.5 to 40 | 20 | 16 to 21 | 0.43 | 0.52 |
| weed tile-days | 10.50 | 0 to 49 | 0 | 0 to 17.5 | 0.85 | 0.00 |
| weed tiles standing (peak) | 4.50 | 0 to 16 | 0 | 0 to 9 | 0.84 | 0.00 |
| DIG ops | 36 | 23.5 to 47.5 | 37 | 35 to 40 | 0.37 | 0.24 |
| weed tile-days per weed | 0.62 | 0 to 2.2 | 0 | 0 to 1.1 | 0.85 | 0.00 |

**Noise**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| unexecutable market orders | 0 | 0 to 241 | 1 | 0 to 45 | 0.26 | 0.02 |

**Rating path**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| rating after game 1 | 690.74 | 650.7 to 736.6 | 701.27 | 683.6 to 768.4 | 0.34 | 0.14 |
| rating after game 10 | 1491.07 | 1169.7 to 1724.7 | 1583.20 | 1332 to 1716.4 | 0.28 | 0.04 |
| rating after game 25 | 2551.23 | 1588.1 to 2691.1 | 2559.32 | 2249 to 2719.2 | 0.51 | 0.90 |
| rating after game 50 | 2859.58 | 1846.4 to 2967 | 2838.65 | 2558.7 to 2942.2 | 0.54 | 0.69 |
| rating after game 100 | 2958.35 | 2079.4 to 3096.7 | 2916.69 | 2729.6 to 2987.2 | 0.72 | 0.07 |
| rating after game 200 | 3043.21 | 2490.5 to 3247 | 2881.88 | 2872.8 to 2890.9 | 0.80 | 0.25 |
| games to 2900 | 58 | 38 to 358 | 70 | 36 to 226 | 0.41 | 0.41 |

## Head to head between the groups

All public games between the groups, seen from the top-14 side: **663-439-4** (60% wins over 1106 games); current submissions of both sides only: **60-13-0** (73 games).

Top-14 teams against the next-15:

| rank | team | games vs next-15 | W-L-T | win % | current subs W-L-T |
|---|---|---|---|---|---|
| 1 | Majkel1337 | 48 | 32-16-0 | 66.7 | 0-0-0 |
| 2 | DSM | 56 | 31-25-0 | 55.4 | 5-0-0 |
| 3 | Artem The Farmer 🍅 | 54 | 43-11-0 | 79.6 | 5-0-0 |
| 4 | Orbital Terraformer | 41 | 25-16-0 | 61.0 | 2-4-0 |
| 5 | SpaTaro | 123 | 74-49-0 | 60.2 | 6-0-0 |
| 6 | Mengfei Li | 148 | 86-62-0 | 58.1 | 3-0-0 |
| 7 | ymg_aq | 122 | 93-27-2 | 76.2 | 4-0-0 |
| 9 | HowardLeeTW | 24 | 15-9-0 | 62.5 | 7-3-0 |
| 10 | アルモンド | 58 | 34-24-0 | 58.6 | 5-2-0 |
| 13 | Thomas Tschinkel | 112 | 63-48-1 | 56.2 | 8-2-0 |
| 14 | Catalyst | 49 | 30-19-0 | 61.2 | 5-1-0 |
| 15 | redblackbst | 109 | 71-37-1 | 65.1 | 7-0-0 |
| 16 | feel the agi | 105 | 41-64-0 | 39.0 | 1-1-0 |
| 18 | Otter Vibe | 57 | 25-32-0 | 43.9 | 2-0-0 |

Next-15 teams against the top-14:

| rank | team | games vs top-14 | W-L-T | win % | current subs W-L-T |
|---|---|---|---|---|---|
| 8 | Unknown Mother-Goose | 285 | 150-135-0 | 52.6 | 0-0-0 |
| 11 | leave you | 87 | 38-49-0 | 43.7 | 3-9-0 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | 18 | 2-16-0 | 11.1 | 1-7-0 |
| 19 | Zhenghongshuang | 44 | 10-34-0 | 22.7 | 2-6-0 |
| 20 | kyy666 | 48 | 16-32-0 | 33.3 | 1-1-0 |
| 21 | Kilupy | 20 | 4-16-0 | 20 | 0-0-0 |
| 22 | elmo | 48 | 24-23-1 | 50 | 0-0-0 |
| 23 | ElephtAI | 71 | 23-48-0 | 32.4 | 1-11-0 |
| 29 | Emile Andrieu | 24 | 3-21-0 | 12.5 | 0-4-0 |
| 30 | mtmr_s1 | 112 | 41-70-1 | 36.6 | 1-1-0 |
| 31 | Kaggriculture Agent | 160 | 62-97-1 | 38.8 | 1-3-0 |
| 38 | THUNDER THUNDER | 96 | 34-61-1 | 35.4 | 3-10-0 |
| 39 | yomogii | 31 | 8-23-0 | 25.8 | 0-0-0 |
| 47 | doubao | 9 | 2-7-0 | 22.2 | 0-3-0 |
| 48 | Tom&Jerry | 53 | 22-31-0 | 41.5 | 0-5-0 |

## Losses of the current submissions

Sampled losses per group: how close they were, who inflicted them, and which feature the winner differed in most (in pooled standard deviations of the feature).

| group | losses | median margin | within 3k % | to top-14 % | to next-15 % | to others % |
|---|---|---|---|---|---|---|
| top-14 | 34 | -1697.5 | 61.8 | 2.9 | 5.9 | 91.2 |
| next-15 | 52 | -1585 | 67.3 | 1.9 | 3.8 | 94.2 |

| group | biggest scaled difference in the loss | losses | share % |
|---|---|---|---|
| top-14 | FERTILIZE ops, opponent lower | 11 | 32.4 |
| top-14 | milk sold, opponent lower | 4 | 11.8 |
| top-14 | strawberry sold, opponent lower | 3 | 8.8 |
| top-14 | land day 1, opponent higher | 2 | 5.9 |
| next-15 | wool sold, opponent higher | 10 | 19.2 |
| next-15 | FERTILIZE ops, opponent lower | 7 | 13.5 |
| next-15 | units sold last 3 days, opponent lower | 6 | 11.5 |
| next-15 | milk sold, opponent higher | 4 | 7.7 |

## Per-team profile

| rank | team | group | games | win % | opp rating | field branch turn | plan branch turn | distinct % at 400 | driver | final money | hands (peak) | quadrants | land day 1 | land day 2 | cows bought | sheep bought | geese bought | strawberry planted | wheat planted | melon planted | CARE ops | FERTILIZE ops | DIG ops | melon sold | strawberry sold | milk sold | wool sold | units sold total | units sold last 3 days | melon first sell day | melon last sell day | strawberry first sell day | milk first sell day | wool first sell day | weeds spawned | weed tile-days | weed tiles standing (peak) | unexecutable market orders | weed tile-days per weed | rating after game 1 | rating after game 10 | rating after game 25 | rating after game 50 | rating after game 100 | rating after game 200 | games to 2900 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top | 50 | 98 | 2118.3 | 24 | 24 | 100 | opponent | 118371 | 11 | 3 | 6 | 9 | 8 | 4 | 2 | 31 | 177.5 | 14 | 309 | 150.5 | 37 | 72 | 219.5 | 181.5 | 109 | 1506 | 362.5 | 10 | 20.5 | 14 | 8 | 6 | 18.5 | 23 | 7.5 | 0 | 1.3 | 650.7 | 1446.2 | 2543.1 | 2875.1 | 3096.7 | 3247.0 | 54 |
| 2 | DSM | top | 50 | 100 | 2127.8 | 24 | 24 | 100 | none | 109152 | 11 | 3 | 6 | 9 | 9 | 5 | 2 | 30 | 187 | 14 | 349.5 | 157 | 35 | 64 | 224.5 | 188.5 | 107.5 | 1496.5 | 361 | 10 | 23 | 13 | 8 | 6 | 19 | 30.5 | 8 | 0 | 1.5 | 697.2 | 1479.3 | 2521.9 | 2865.1 |  |  | 58 |
| 3 | Artem The Farmer 🍅 | top | 50 | 98 | 2115.1 | 200 | 200 | 100 | opponent | 109196.5 | 13 | 3 | 6 | 8 | 7.5 | 4 | 2 | 29 | 142 | 13 | 310.5 | 159 | 38.5 | 6 | 146 | 106 | 26.5 | 1023.5 | 257 | 11 | 11 | 16 | 12 | 16 | 11 | 10 | 4 | 0 | 0.9 | 718.2 | 1459.7 | 2515.7 | 2854.1 |  |  | 58 |
| 4 | Orbital Terraformer | top | 50 | 98 | 1905.0 | 24 | 24 | 100 | opponent | 104433 | 11 | 3 | 6 | 9 | 7.5 | 5 | 2 | 31 | 187 | 14 | 332 | 152 | 35 | 72 | 201 | 158.5 | 99 | 1505 | 334 | 10 | 13 | 14 | 8 | 6 | 16 | 31.5 | 7 | 0 | 2.2 | 677.1 | 1328.1 | 2243.0 | 2700.5 | 2910.0 |  | 92 |
| 5 | SpaTaro | top | 50 | 98 | 1420.2 | 24 | 24 | 100 | none | 96824.5 | 11 | 3 | 6 | 8 | 10 | 8 | 0 | 25.5 | 188.5 | 11 | 267 | 83 | 23.5 | 18.5 | 117.5 | 123 | 59 | 1483.5 | 272 | 10 | 13 | 14.5 | 11 | 12 | 23 | 28.5 | 7 | 241 | 1.5 | 684.3 | 1169.7 | 1588.1 | 1846.4 | 2079.4 | 2490.5 | 358 |
| 6 | Mengfei Li | top | 50 | 98 | 2206.6 | 24 | 200 | 100 | none | 104204.5 | 13 | 3 | 6 | 11 | 9 | 5 | 3 | 33 | 115 | 13 | 281 | 189 | 33 | 18 | 171 | 82.5 | 36 | 1045.5 | 208 | 11 | 23 | 16 | 13 | 7 | 40 | 49 | 16 | 0 | 1.2 | 736.6 | 1712.8 | 2565.4 | 2868.2 | 2965.2 | 3051.3 | 59 |
| 7 | ymg_aq | top | 50 | 96 | 2269.7 | 100 | 100 | 100 | none | 105736 | 13 | 3 | 5 | 8 | 7 | 3.5 | 1 | 32 | 154.5 | 15 | 252 | 136.5 | 37 | 30 | 190 | 131.5 | 66.5 | 1586.5 | 255.5 | 17 | 28 | 14 | 11 | 10 | 12.5 | 8 | 4 | 0 | 0.7 | 663.5 | 1605.0 | 2691.1 | 2967.0 | 3007.2 |  | 38 |
| 8 | Unknown Mother-Goose | batch | 50 | 100 | 2015.4 | 200 | 136 | 100 | weed | 119640 | 11 | 3 | 6 | 11 | 7 | 6 | 3 | 29.5 | 141 | 14 | 337.5 | 181 | 37.5 | 22 | 149.5 | 125 | 85 | 1164.5 | 286 | 11 | 22 | 16 | 13 | 7 | 17 | 14 | 9 | 7 | 0.8 | 683.6 | 1332.0 | 2342.0 | 2809.3 | 2987.2 |  | 63 |
| 9 | HowardLeeTW | top | 50 | 90 | 2177.8 | 48 | 48 | 100 | seat | 108796 | 12 | 3 | 3 | 8 | 7 | 4.5 | 1 | 31 | 131.5 | 13 | 247 | 192.5 | 38 | 49.5 | 202.5 | 134.5 | 55 | 998 | 231 | 11 | 24 | 15 | 8 | 10 | 8 | 2.5 | 1 | 0 | 0.4 | 669.5 | 1569.9 | 2559.3 | 2797.1 | 2928.6 |  | 81 |
| 10 | アルモンド | top | 50 | 92 | 2200.4 | 200 | 100 | 98 | weed | 100353 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 127.5 | 15 | 410 | 144 | 35 | 30 | 144.5 | 127.5 | 101 | 1209.5 | 287.5 | 11 | 20 | 16 | 11 | 14 | 20 | 1.5 | 1 | 1 | 0.1 | 656.4 | 1489.5 | 2662.4 | 2894.6 |  |  | 51 |
| 11 | leave you | batch | 50 | 98 | 2189.8 | 200 | 200 | 54 | seat | 106719.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 364.5 | 108.5 | 35 | 12 | 152 | 149.5 | 61 | 1154 | 271.5 | 11 | 11 | 16 | 11 | 6 | 20 | 0 | 0 | 0 | 0 | 691.8 | 1583.2 | 2559.3 | 2894.1 | 2954.8 |  | 51 |
| 13 | Thomas Tschinkel | top | 50 | 90 | 2239.4 | 200 | 200 | 70 | weed | 93960 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 405 | 121 | 38 | 12 | 121 | 113.5 | 68 | 1105 | 263 | 11 | 11 | 19 | 14 | 6 | 20 | 0 | 0 | 1 | 0 | 699.5 | 1492.6 | 2686.5 | 2916.0 | 2969.0 |  | 46 |
| 14 | Catalyst | top | 50 | 94 | 2196.4 | 24 | 24 | 72 | none | 102170.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 389 | 121 | 36 | 12 | 170 | 151 | 84.5 | 1181.5 | 281 | 11 | 11 | 16 | 11 | 7 | 19 | 0 | 0 | 1 | 0 | 703.2 | 1480.3 | 2608.4 | 2834.4 | 2958.4 |  | 61 |
| 15 | redblackbst | top | 50 | 92 | 2227.3 | 200 | 200 | 98 | none | 101342.5 | 12 | 3 | 6 | 11 | 7 | 5 | 2 | 32 | 162 | 13 | 344 | 86.5 | 36 | 18 | 162.5 | 109.5 | 82 | 1140.5 | 254.5 | 11 | 21 | 17 | 11 | 14.5 | 26 | 11 | 5 | 0.5 | 0.5 | 697.7 | 1547.7 | 2618.9 | 2885.2 | 2991.0 |  | 52 |
| 16 | feel the agi | top | 50 | 90 | 2144.4 | 200 | 24 | 98 | shop | 117751 | 13 | 3 | 6 | 11 | 7 | 3 | 5 | 29 | 148.5 | 12 | 394.5 | 163 | 24 | 12 | 204.5 | 89 | 39.5 | 1052.5 | 225 | 11 | 11 | 16 | 11 | 7 | 29 | 16 | 8 | 0 | 0.6 | 735.6 | 1724.7 | 2470.0 | 2658.6 | 2841.7 | 3043.2 | 118 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | batch | 50 | 96 | 2245.8 | 200 | 200 | 68 | shop | 103297 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 405 | 110.5 | 37 | 12 | 126 | 99.5 | 69 | 1084.5 | 258 | 11 | 11 | 19 | 15 | 6 | 20 | 0 | 0 | 1 | 0 | 701.3 | 1686.6 | 2607.5 | 2894.9 | 2946.6 |  | 49 |
| 18 | Otter Vibe | top | 50 | 98 | 2155.5 | 100 | 100 | 100 | shop | 106756.5 | 15 | 3 | 5 | 10 | 7 | 7 | 6 | 23 | 103.5 | 16 | 359.5 | 193.5 | 47.5 | 0 | 50 | 23 | 30 | 774.5 | 196.5 | 22 | 22 | 15 | 14 | 14 | 3.5 | 1 | 1 | 0 | 0.4 | 678.7 | 1508.8 | 2542.6 | 2848.9 | 2947.6 | 3026.3 | 58 |
| 19 | Zhenghongshuang | batch | 50 | 96 | 2153.2 | 200 | 200 | 66 | weed | 100891.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 155.5 | 12 | 356.5 | 113 | 35 | 12 | 152 | 125.5 | 86 | 1155 | 273 | 11 | 11 | 16 | 11 | 6 | 20 | 0 | 0 | 0 | 0 | 701.6 | 1642.7 | 2564.2 | 2855.8 | 2946.5 |  | 59 |
| 20 | kyy666 | batch | 50 | 94 | 2173.1 | 200 | 200 | 72 | seat | 109057.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 397 | 116 | 38 | 12 | 125.5 | 120.5 | 67.5 | 1088.5 | 259 | 11 | 11 | 19 | 14 | 6 | 20 | 0 | 0 | 1 | 0 | 703.6 | 1533.3 | 2550.0 | 2845.6 | 2927.5 |  | 74 |
| 21 | Kilupy | batch | 50 | 90 | 2319.3 | 200 | 200 | 76 | none | 101670 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 405 | 110 | 37 | 12 | 122 | 103 | 73 | 1079.5 | 264 | 11 | 11 | 19 | 15 | 6 | 19 | 0 | 0 | 1 | 0 | 694.9 | 1698.1 | 2719.2 | 2926.6 |  |  | 36 |
| 22 | elmo | batch | 50 | 92 | 2184.5 | 200 | 200 | 68 | none | 106007.5 | 12 | 3 | 6 | 11 | 7 | 6 | 3 | 33 | 158 | 12 | 405 | 112.5 | 37.5 | 12 | 131 | 101 | 84 | 2001.5 | 266 | 11 | 11 | 19 | 12 | 6 | 19 | 0 | 0 | 1 | 0 | 697.1 | 1565.6 | 2563.7 | 2826.4 | 2928.4 |  | 70 |
| 23 | ElephtAI | batch | 50 | 96 | 2281.6 | 200 | 100 | 70 | none | 99151.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 417 | 103 | 36 | 12 | 126 | 113 | 84 | 1084 | 268 | 11 | 11 | 18 | 11 | 7 | 19 | 0 | 0 | 1 | 0 | 768.4 | 1679.9 | 2642.5 | 2942.2 | 2900.9 |  | 42 |
| 29 | Emile Andrieu | batch | 50 | 86 | 2204.4 | 200 | 200 | 84 | weed | 102305 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 166 | 12 | 440 | 113.5 | 37 | 12 | 124.5 | 108 | 57 | 1077.5 | 257.5 | 11 | 11 | 19 | 15 | 6 | 20 | 0 | 0 | 1 | 0 | 718.2 | 1572.2 | 2671.2 | 2789.1 | 2896.7 |  | 85 |
| 30 | mtmr_s1 | batch | 50 | 94 | 2156.9 | 200 | 100 | 100 | weed | 101994.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 148.5 | 12 | 398 | 127.5 | 40 | 12 | 153 | 111.5 | 76 | 1194 | 257 | 11 | 11 | 16 | 11 | 7 | 21 | 1 | 1 | 45 | 0.0 | 694.6 | 1473.9 | 2484.5 | 2838.6 | 2896.1 |  | 76 |
| 31 | Kaggriculture Agent | batch | 50 | 90 | 2250.5 | 24 | 24 | 54 | none | 99096 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 158 | 12 | 408 | 116 | 35 | 12 | 139 | 154 | 109 | 4682 | 569 | 11 | 11 | 18 | 11 | 6 | 20 | 0 | 0 | 45 | 0 | 714.8 | 1608.1 | 2657.9 | 2872.9 | 2916.7 |  | 60 |
| 38 | THUNDER THUNDER | batch | 50 | 90 | 2010.7 | 100 | 100 | 100 | none | 101158 | 12 | 3 | 4 | 8 | 9 | 3 | 2 | 33 | 145 | 13 | 301.5 | 182 | 39 | 24 | 216.5 | 118 | 29.5 | 1258 | 227.5 | 17.5 | 21 | 15 | 9 | 7 | 16 | 17.5 | 4 | 0 | 1.1 | 696.6 | 1555.9 | 2249.0 | 2569.2 | 2729.6 | 2872.8 | 226 |
| 39 | yomogii | batch | 50 | 94 | 2134.5 | 48 | 24 | 82 | none | 102744.5 | 12 | 3 | 6 | 11 | 6.5 | 6 | 3 | 33 | 163 | 12 | 403 | 108 | 37 | 12 | 129 | 95.5 | 74.5 | 1121 | 266 | 11 | 11 | 19 | 13 | 6 | 20 | 0 | 0 | 1 | 0 | 685.0 | 1519.9 | 2489.5 | 2805.2 |  |  | 95 |
| 47 | doubao | batch | 50 | 88 | 2074.4 | 200 | 200 | 76 | shop | 110695 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 400 | 123.5 | 37 | 12 | 129 | 101 | 87.5 | 1110 | 273 | 11 | 11 | 19 | 12 | 7 | 20 | 0 | 0 | 1 | 0 | 714.7 | 1716.4 | 2290.8 | 2558.7 | 2774.5 | 2890.9 | 212 |
| 48 | Tom&Jerry | batch | 50 | 92 | 2204.3 | 200 | 200 | 74 | weed | 106862 | 12 | 3 | 6 | 11 | 6 | 6 | 3 | 33 | 162 | 12 | 405 | 110 | 37 | 12 | 121 | 102 | 62.5 | 1079.5 | 263 | 11 | 11 | 19 | 15 | 6 | 19 | 0 | 0 | 1 | 0 | 736.2 | 1711.6 | 2506.0 | 2799.3 | 2887.6 |  | 104 |

