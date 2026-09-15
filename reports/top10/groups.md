# Top-14 vs next-15

Snapshot 2026-09-15T0033Z. The top-14 are the teams that were top-10 in Iminabo's screenshot or on the live board on 2026-09-14; the next-15 are chunks of the gold zone outside them (ranks 8-48 at snapshot time, 15 teams with replays). Under Kaggle's medal rule for 9,066 teams (gold = top 10 + 0.2% = rank 28, silver = top 5%), ranks 8-23 of the batch are gold and 29-48 silver; under the top-50 working assumption all are gold. Every number below is a per-team median over every sampled game of the current submission (C0 plus its games in L), compared across teams: 'P(top > next)' is the chance that a random top-14 team's value is above a random next-15 team's (0.5 = no separation), 'p' is the two-sided Mann-Whitney test. Numbers are per game unless stated. Teams with fewer than 10 sampled games of their current submission are left out of the comparison.

## Who is in each group

| rank | team | group | score | public_games | current_sub_games | Kaggle medal zone | sampled current-sub games |
|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top-14 | 3216.9 | 1497 | 331 | gold | 96 |
| 2 | DSM | top-14 | 3062.9 | 8825 | 80 | gold | 80 |
| 3 | Artem The Farmer 🍅 | top-14 | 3043.9 | 2070 | 86 | gold | 86 |
| 4 | Orbital Terraformer | top-14 | 3022.2 | 1831 | 187 | gold | 73 |
| 5 | SpaTaro | top-14 | 3014.1 | 4642 | 456 | gold | 86 |
| 6 | Mengfei Li | top-14 | 3014 | 10390 | 374 | gold | 74 |
| 7 | ymg_aq | top-14 | 3011.7 | 5367 | 178 | gold | 73 |
| 8 | Unknown Mother-Goose | next-15 | 3007 | 3035 | 107 | gold | 81 |
| 9 | HowardLeeTW | top-14 | 2991.1 | 2348 | 194 | gold | 74 |
| 10 | アルモンド | top-14 | 2977.2 | 3153 | 82 | gold | 82 |
| 11 | leave you | next-15 | 2971.6 | 9900 | 112 | gold | 73 |
| 13 | Thomas Tschinkel | top-14 | 2970.2 | 8950 | 110 | gold | 69 |
| 14 | Catalyst | top-14 | 2968.2 | 906 | 105 | gold | 80 |
| 15 | redblackbst | top-14 | 2966.9 | 5329 | 115 | gold | 100 |
| 16 | feel the agi | top-14 | 2961.4 | 3449 | 562 | gold | 71 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | next-15 | 2950.3 | 728 | 136 | gold | 64 |
| 18 | Otter Vibe | top-14 | 2949.6 | 2511 | 721 | gold | 152 |
| 19 | Zhenghongshuang | next-15 | 2945.8 | 5279 | 144 | gold | 72 |
| 20 | kyy666 | next-15 | 2938.3 | 1600 | 116 | gold | 82 |
| 21 | Kilupy | next-15 | 2934.9 | 890 | 86 | gold | 76 |
| 22 | elmo | next-15 | 2932.4 | 3469 | 102 | gold | 73 |
| 23 | ElephtAI | next-15 | 2932.1 | 5736 | 141 | gold | 72 |
| 29 | Emile Andrieu | next-15 | 2912.9 | 3653 | 120 | silver | 63 |
| 30 | mtmr_s1 | next-15 | 2912.3 | 5969 | 113 | silver | 71 |
| 31 | Kaggriculture Agent | next-15 | 2912 | 8989 | 116 | silver | 63 |
| 38 | THUNDER THUNDER | next-15 | 2899.3 | 7231 | 395 | silver | 70 |
| 39 | yomogii | next-15 | 2897.5 | 2690 | 96 | silver | 78 |
| 47 | doubao | next-15 | 2885.7 | 1630 | 226 | silver | 75 |
| 48 | Tom&Jerry | next-15 | 2884.9 | 5368 | 154 | silver | 76 |

## What separates the groups

- **distinct % at 400**: top-14 median 100 vs next-15 69; a random top-14 team is above a random next-15 team 85% of the time (p = 0.001)
- **strawberry first sell day**: top-14 median 15.5 vs next-15 19; a random top-14 team is above a random next-15 team 15% of the time (p = 0.001)
- **weed tile-days per weed**: top-14 median 0.6 vs next-15 0; a random top-14 team is above a random next-15 team 85% of the time (p = 0.001)
- **weed tile-days**: top-14 median 10.5 vs next-15 0; a random top-14 team is above a random next-15 team 85% of the time (p = 0.001)
- **weed tiles standing (peak)**: top-14 median 4.5 vs next-15 0; a random top-14 team is above a random next-15 team 83% of the time (p = 0.001)
- **strawberry planted**: top-14 median 32 vs next-15 33; a random top-14 team is above a random next-15 team 20% of the time (p = 0.002)
- **melon last sell day**: top-14 median 19 vs next-15 11; a random top-14 team is above a random next-15 team 80% of the time (p = 0.002)
- **CARE ops**: top-14 median 334 vs next-15 403; a random top-14 team is above a random next-15 team 20% of the time (p = 0.006)
- **field branch turn**: top-14 median 36 vs next-15 200; a random top-14 team is above a random next-15 team 21% of the time (p = 0.004)
- **wool first sell day**: top-14 median 8.5 vs next-15 6; a random top-14 team is above a random next-15 team 77% of the time (p = 0.007)
- **melon planted**: top-14 median 13 vs next-15 12; a random top-14 team is above a random next-15 team 77% of the time (p = 0.006)
- **FERTILIZE ops**: top-14 median 154 vs next-15 111; a random top-14 team is above a random next-15 team 76% of the time (p = 0.016)
- **unexecutable market orders**: top-14 median 0 vs next-15 1; a random top-14 team is above a random next-15 team 25% of the time (p = 0.012)
- **land day 2**: top-14 median 9.5 vs next-15 11; a random top-14 team is above a random next-15 team 26% of the time (p = 0.006)
- **plan branch turn**: top-14 median 36 vs next-15 200; a random top-14 team is above a random next-15 team 26% of the time (p = 0.020)
- **milk first sell day**: top-14 median 11 vs next-15 12; a random top-14 team is above a random next-15 team 27% of the time (p = 0.030)
- **sheep bought**: top-14 median 5 vs next-15 6; a random top-14 team is above a random next-15 team 28% of the time (p = 0.019)
- **opp rating**: top-14 median 2453 vs next-15 2394; a random top-14 team is above a random next-15 team 72% of the time (p = 0.045)
- **rating after game 10**: top-14 median 1491 vs next-15 1583; a random top-14 team is above a random next-15 team 28% of the time (p = 0.045)
- **melon sold**: top-14 median 18 vs next-15 12; a random top-14 team is above a random next-15 team 71% of the time (p = 0.037)

## What does not separate them (p >= 0.2 and P(top > next) within 0.35-0.65)

- quadrants (3 vs 3)
- units sold total (1162 vs 1118)
- hands (peak) (12 vs 12)
- rating after game 25 (2551 vs 2559)
- units sold last 3 days (266 vs 265)
- rating after game 50 (2860 vs 2839)
- wheat planted (157 vs 162)
- weeds spawned (19.2 vs 20)
- win % (84 vs 83)
- land day 1 (6 vs 6)
- games to 2900 (58 vs 70)
- melon first sell day (11 vs 11)
- cows bought (8 vs 8)
- wool sold (64 vs 74)
- final money (103828 vs 102744)
- milk sold (129 vs 109)

![rating paths by group](figs/group_rating.png)

![per-team medians by group](figs/group_strip.png)

## Determinism and branch point (current submissions)

Branch turn: the first cut at which fewer than 90% of a team's games share one line (720 = one line to the end). Driver: the condition whose presence moves the off-line rate by 25+ points at that cut (weed on own farm before that day, opponent off its own modal line at the previous cut, seat, first shop draw).

| rank | team | group | games | field branch turn | plan branch turn | distinct % at 400 | driver | driver gap | field branch |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top-14 | 96 | 24 | 24 | 100 | opponent | -49.8 | day 1 |
| 2 | DSM | top-14 | 80 | 24 | 24 | 100 | none | -19.5 | day 1 |
| 3 | Artem The Farmer 🍅 | top-14 | 86 | 200 | 200 | 100 | none | 22.2 | day 8-16 |
| 4 | Orbital Terraformer | top-14 | 73 | 24 | 24 | 100 | opponent | 45.6 | day 1 |
| 5 | SpaTaro | top-14 | 86 | 24 | 24 | 100 | none | 4.5 | day 1 |
| 6 | Mengfei Li | top-14 | 74 | 24 | 200 | 100 | none | -7.3 | day 1 |
| 7 | ymg_aq | top-14 | 73 | 100 | 100 | 100 | none | -13.3 | day 4-6 |
| 8 | Unknown Mother-Goose | next-15 | 81 | 48 | 48 | 100 | weed | 89.7 | day 2 |
| 9 | HowardLeeTW | top-14 | 74 | 48 | 48 | 100 | seat | 89.7 | day 2 |
| 10 | アルモンド | top-14 | 82 | 100 | 100 | 98.8 | none | 14.7 | day 4-6 |
| 11 | leave you | next-15 | 73 | 200 | 200 | 46.6 | weed | 77.3 | day 8-16 |
| 13 | Thomas Tschinkel | top-14 | 69 | 200 | 200 | 66.7 | weed | 46.0 | day 8-16 |
| 14 | Catalyst | top-14 | 80 | 24 | 24 | 68.8 | none | -20 | day 1 |
| 15 | redblackbst | top-14 | 100 | 24 | 24 | 98 | none | -16.6 | day 1 |
| 16 | feel the agi | top-14 | 71 | 200 | 24 | 98.6 | shop | -33.9 | day 8-16 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | next-15 | 64 | 200 | 200 | 64.1 | none | -23.1 | day 8-16 |
| 18 | Otter Vibe | top-14 | 152 | 100 | 100 | 100 | none | 14.9 | day 4-6 |
| 19 | Zhenghongshuang | next-15 | 72 | 200 | 200 | 59.7 | weed | 71.6 | day 8-16 |
| 20 | kyy666 | next-15 | 82 | 200 | 200 | 70.7 | shop | 27.5 | day 8-16 |
| 21 | Kilupy | next-15 | 76 | 200 | 200 | 68.4 | shop | 34.3 | day 8-16 |
| 22 | elmo | next-15 | 73 | 200 | 200 | 65.8 | weed | 52.9 | day 8-16 |
| 23 | ElephtAI | next-15 | 72 | 200 | 100 | 61.1 | none | -11.7 | day 8-16 |
| 29 | Emile Andrieu | next-15 | 63 | 200 | 200 | 82.5 | shop | 41.2 | day 8-16 |
| 30 | mtmr_s1 | next-15 | 71 | 200 | 100 | 95.8 | weed | 53.0 | day 8-16 |
| 31 | Kaggriculture Agent | next-15 | 63 | 24 | 24 | 58.7 | none | -15.2 | day 1 |
| 38 | THUNDER THUNDER | next-15 | 70 | 100 | 100 | 100 | none | 17.5 | day 4-6 |
| 39 | yomogii | next-15 | 78 | 48 | 24 | 70.5 | none | -16.5 | day 2 |
| 47 | doubao | next-15 | 75 | 200 | 200 | 69.3 | shop | 38.8 | day 8-16 |
| 48 | Tom&Jerry | next-15 | 76 | 200 | 200 | 69.7 | weed | 40.8 | day 8-16 |

| first field branch | top-14 teams | next-15 teams |
|---|---|---|
| day 1 | 7 | 1 |
| day 2 | 1 | 2 |
| day 4-6 | 3 | 1 |
| day 8-16 | 3 | 11 |
| end-game only | 0 | 0 |
| fixed | 0 | 0 |

| dominant driver at the first branch | top-14 teams | next-15 teams |
|---|---|---|
| opponent | 2 | 0 |
| weed | 1 | 6 |
| seat | 1 | 0 |
| shop | 1 | 4 |
| none | 9 | 5 |

Teams whose modal field line (farmer and hand actions) is byte-identical to another studied team's through the cut, i.e. members of a shared plan family, and the size of the largest family at that cut:

| turn | day | top-14 on a shared line | next-15 on a shared line | largest family |
|---|---|---|---|---|
| 24 | 1 | 7 of 14 | 13 of 15 | 13 |
| 48 | 2 | 3 of 14 | 12 of 15 | 13 |
| 100 | 4 | 3 of 14 | 11 of 15 | 12 |
| 136 | 5 | 3 of 14 | 11 of 15 | 12 |
| 200 | 8 | 2 of 14 | 11 of 15 | 7 |
| 300 | 12 | 2 of 14 | 8 of 15 | 5 |
| 400 | 16 | 1 of 14 | 1 of 15 | 2 |

## Feature comparison

**Outcome**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| win % | 83.77 | 69.7 to 97.5 | 83.33 | 74.7 to 90.1 | 0.55 | 0.62 |
| opp rating | 2453.25 | 2081 to 2688.6 | 2393.94 | 2262.7 to 2517.3 | 0.72 | 0.04 |
| final money | 103827.75 | 97042 to 114473 | 102744.50 | 97905 to 117836 | 0.62 | 0.26 |

**Determinism**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| field branch turn | 36 | 24 to 200 | 200 | 24 to 200 | 0.21 | 0.00 |
| plan branch turn | 36 | 24 to 200 | 200 | 24 to 200 | 0.26 | 0.02 |
| distinct % at 400 | 100 | 66.7 to 100 | 69.33 | 46.6 to 100 | 0.85 | 0.00 |

**Farm plan**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| hands (peak) | 12 | 11 to 15 | 12 | 11 to 12 | 0.49 | 0.90 |
| quadrants | 3 | 3 to 3 | 3 | 3 to 3 | 0.50 | 1 |
| land day 1 | 6 | 3 to 6 | 6 | 4 to 6 | 0.43 | 0.27 |
| land day 2 | 9.50 | 8 to 11 | 11 | 8 to 11 | 0.26 | 0.01 |
| cows bought | 8 | 6 to 11.5 | 8 | 7 to 9 | 0.40 | 0.29 |
| sheep bought | 5 | 3 to 8.5 | 6 | 6 to 6.5 | 0.28 | 0.02 |
| geese bought | 2.50 | 0 to 6 | 3 | 2 to 3 | 0.34 | 0.09 |
| strawberry planted | 31.50 | 24 to 33 | 33 | 30 to 34 | 0.20 | 0.00 |
| wheat planted | 157 | 104.5 to 192 | 162 | 138.5 to 163 | 0.45 | 0.64 |
| melon planted | 13 | 11 to 15 | 12 | 12 to 14 | 0.77 | 0.01 |
| CARE ops | 334.25 | 247 to 410 | 403 | 299 to 439 | 0.20 | 0.01 |
| FERTILIZE ops | 154 | 87 to 190 | 111 | 103.5 to 181 | 0.76 | 0.02 |

**Market**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| melon sold | 18 | 0 to 72 | 12 | 12 to 23.5 | 0.71 | 0.04 |
| strawberry sold | 172.50 | 42 to 224 | 129 | 122 to 217 | 0.70 | 0.06 |
| milk sold | 129.25 | 29 to 180.5 | 109 | 96.5 to 155 | 0.63 | 0.22 |
| wool sold | 64 | 20.5 to 109 | 74 | 49 to 109 | 0.40 | 0.34 |
| units sold last 3 days | 265.50 | 198.5 to 368 | 265 | 223.5 to 574 | 0.52 | 0.88 |
| units sold total | 1162.25 | 754.5 to 1612 | 1117.50 | 1074 to 4713 | 0.49 | 0.93 |
| melon first sell day | 11 | 10 to 22 | 11 | 11 to 18 | 0.40 | 0.24 |
| melon last sell day | 19 | 11 to 28 | 11 | 11 to 22 | 0.80 | 0.00 |
| strawberry first sell day | 15.50 | 13 to 19 | 19 | 15 to 19 | 0.15 | 0.00 |
| milk first sell day | 11 | 8 to 14 | 12 | 9 to 15 | 0.27 | 0.03 |
| wool first sell day | 8.50 | 6 to 16 | 6 | 6 to 7 | 0.77 | 0.01 |

**Weeds and repair**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| weeds spawned | 19.25 | 4 to 41 | 20 | 17 to 21 | 0.45 | 0.62 |
| weed tile-days | 10.50 | 0 to 48.5 | 0 | 0 to 18 | 0.85 | 0.00 |
| weed tiles standing (peak) | 4.50 | 0 to 16 | 0 | 0 to 9 | 0.83 | 0.00 |
| DIG ops | 36 | 23.5 to 45.5 | 37 | 35 to 40 | 0.33 | 0.11 |
| weed tile-days per weed | 0.64 | 0 to 2.2 | 0 | 0 to 1.1 | 0.85 | 0.00 |

**Noise**

| feature | top-14 median | top-14 range | next-15 median | next-15 range | P(top > next) | p |
|---|---|---|---|---|---|---|
| unexecutable market orders | 0 | 0 to 239.5 | 1 | 0 to 45 | 0.25 | 0.01 |

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
| top-14 | 205 | -4478 | 34.1 | 57.6 | 8.3 | 34.1 |
| next-15 | 189 | -2319 | 58.2 | 5.8 | 15.9 | 78.3 |

| group | biggest scaled difference in the loss | losses | share % |
|---|---|---|---|
| top-14 | strawberry sold, opponent higher | 23 | 11.2 |
| top-14 | FERTILIZE ops, opponent lower | 19 | 9.3 |
| top-14 | milk sold, opponent higher | 18 | 8.8 |
| top-14 | weeds spawned, opponent lower | 13 | 6.3 |
| next-15 | milk sold, opponent higher | 23 | 12.2 |
| next-15 | wool sold, opponent higher | 21 | 11.1 |
| next-15 | FERTILIZE ops, opponent lower | 16 | 8.5 |
| next-15 | FERTILIZE ops, opponent higher | 16 | 8.5 |

## Per-team profile

| rank | team | group | games | win % | opp rating | field branch turn | plan branch turn | distinct % at 400 | driver | final money | hands (peak) | quadrants | land day 1 | land day 2 | cows bought | sheep bought | geese bought | strawberry planted | wheat planted | melon planted | CARE ops | FERTILIZE ops | DIG ops | melon sold | strawberry sold | milk sold | wool sold | units sold total | units sold last 3 days | melon first sell day | melon last sell day | strawberry first sell day | milk first sell day | wool first sell day | weeds spawned | weed tile-days | weed tiles standing (peak) | unexecutable market orders | weed tile-days per weed | rating after game 1 | rating after game 10 | rating after game 25 | rating after game 50 | rating after game 100 | rating after game 200 | games to 2900 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Majkel1337 | top | 96 | 87.5 | 2557.9 | 24 | 24 | 100 | opponent | 113284 | 11 | 3 | 6 | 9 | 8 | 4 | 2 | 31 | 177.5 | 14 | 326.5 | 154 | 36 | 72 | 218.5 | 180.5 | 109 | 1515 | 368 | 10 | 18 | 14 | 8 | 6 | 19.5 | 26 | 7 | 0 | 1.3 | 650.7 | 1446.2 | 2543.1 | 2875.1 | 3096.7 | 3247.0 | 54 |
| 2 | DSM | top | 80 | 97.5 | 2417.0 | 24 | 24 | 100 | none | 104556.5 | 11 | 3 | 6 | 9 | 9 | 4 | 2 | 30 | 187.5 | 14 | 340.5 | 154.5 | 35 | 64 | 224 | 177.5 | 92.5 | 1509.5 | 361.5 | 10 | 23 | 13 | 8 | 6 | 19 | 28 | 8 | 0 | 1.4 | 697.2 | 1479.3 | 2521.9 | 2865.1 |  |  | 58 |
| 3 | Artem The Farmer 🍅 | top | 86 | 94.2 | 2441.8 | 200 | 200 | 100 | none | 102655 | 13 | 3 | 6 | 8 | 7 | 6 | 2 | 27 | 143.5 | 13 | 311 | 156.5 | 37 | 6 | 143 | 103.5 | 35 | 1058 | 269 | 11 | 11 | 16 | 12 | 16 | 11 | 10 | 4 | 0 | 0.9 | 718.2 | 1459.7 | 2515.7 | 2854.1 |  |  | 58 |
| 4 | Orbital Terraformer | top | 73 | 87.7 | 2238.6 | 24 | 24 | 100 | opponent | 103266 | 11 | 3 | 6 | 9 | 8 | 5 | 2 | 31 | 188 | 14 | 332 | 154 | 35 | 72 | 202 | 170 | 101 | 1512 | 339 | 10 | 13 | 14 | 8 | 6 | 15 | 31 | 7 | 0 | 2.2 | 677.1 | 1328.1 | 2243.0 | 2700.5 | 2910.0 |  | 92 |
| 5 | SpaTaro | top | 86 | 79.1 | 2081.0 | 24 | 24 | 100 | none | 97042 | 11 | 3 | 6 | 8 | 11.5 | 8.5 | 0 | 26 | 192 | 11 | 272.5 | 95 | 23.5 | 18 | 115.5 | 131 | 62.5 | 1482 | 277 | 10 | 13 | 14 | 11 | 12 | 23 | 25 | 7 | 239.5 | 1.2 | 684.3 | 1169.7 | 1588.1 | 1846.4 | 2079.4 | 2490.5 | 358 |
| 6 | Mengfei Li | top | 74 | 83.8 | 2464.7 | 24 | 200 | 100 | none | 103670 | 13 | 3 | 6 | 11 | 9 | 5 | 3 | 33 | 113 | 13 | 286 | 187 | 33 | 18 | 174.5 | 82.5 | 65.5 | 1030 | 204.5 | 11 | 23 | 16 | 13 | 7 | 41 | 48.5 | 16 | 0 | 1.1 | 736.6 | 1712.8 | 2565.4 | 2868.2 | 2965.2 | 3051.3 | 59 |
| 7 | ymg_aq | top | 73 | 86.3 | 2502.1 | 100 | 100 | 100 | none | 105617 | 13 | 3 | 5 | 8 | 7 | 3 | 0 | 33 | 152 | 15 | 249 | 135 | 37 | 30 | 196 | 144 | 53 | 1612 | 262 | 17 | 28 | 14 | 11 | 10 | 13 | 9 | 4 | 0 | 0.7 | 663.5 | 1605.0 | 2691.1 | 2967.0 | 3007.2 |  | 38 |
| 8 | Unknown Mother-Goose | batch | 81 | 90.1 | 2380.4 | 48 | 48 | 100 | weed | 117836 | 11 | 3 | 6 | 11 | 7 | 6 | 3 | 30 | 143 | 14 | 332 | 180 | 37 | 22 | 151 | 121 | 81 | 1156 | 286 | 11 | 22 | 16 | 13 | 7 | 17 | 14 | 9 | 7 | 0.8 | 683.6 | 1332.0 | 2342.0 | 2809.3 | 2987.2 |  | 63 |
| 9 | HowardLeeTW | top | 74 | 77.0 | 2428.1 | 48 | 48 | 100 | seat | 107674 | 12 | 3 | 3 | 8 | 6 | 4.5 | 1 | 32 | 131.5 | 13 | 247 | 190 | 39 | 48 | 203.5 | 127.5 | 55 | 998 | 229 | 11 | 24 | 15 | 8 | 10 | 7.5 | 2 | 1 | 0 | 0.4 | 669.5 | 1569.9 | 2559.3 | 2797.1 | 2928.6 |  | 81 |
| 10 | アルモンド | top | 82 | 85.4 | 2485.8 | 100 | 100 | 98.8 | none | 101879.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 130.5 | 15 | 410 | 144 | 35 | 30 | 148 | 134.5 | 94 | 1206 | 287 | 11 | 20 | 16 | 11 | 14 | 20 | 1 | 1 | 1 | 0.1 | 656.4 | 1489.5 | 2662.4 | 2894.6 |  |  | 51 |
| 11 | leave you | batch | 73 | 87.7 | 2421.7 | 200 | 200 | 46.6 | weed | 102283 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 364 | 109 | 35 | 12 | 152 | 135 | 61 | 1150 | 272 | 11 | 11 | 16 | 11 | 6 | 20 | 0 | 0 | 0 | 0 | 691.8 | 1583.2 | 2559.3 | 2894.1 | 2954.8 |  | 51 |
| 13 | Thomas Tschinkel | top | 69 | 81.2 | 2431.4 | 200 | 200 | 66.7 | weed | 98229 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 405 | 121 | 37 | 12 | 120 | 112 | 68 | 1107 | 262 | 11 | 11 | 19 | 14 | 6 | 20 | 0 | 0 | 1 | 0 | 699.5 | 1492.6 | 2686.5 | 2916.0 | 2969.0 |  | 46 |
| 14 | Catalyst | top | 80 | 83.8 | 2474.3 | 24 | 24 | 68.8 | none | 102193 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 389 | 119.5 | 36 | 12 | 170.5 | 143.5 | 103.5 | 1176 | 279 | 11 | 11 | 16 | 11 | 7 | 19 | 0 | 0 | 1 | 0 | 703.2 | 1480.3 | 2608.4 | 2834.4 | 2958.4 |  | 61 |
| 15 | redblackbst | top | 100 | 78 | 2587.4 | 24 | 24 | 98 | none | 104306 | 11 | 3 | 6 | 11 | 7 | 5 | 3 | 32 | 162 | 13 | 336.5 | 87 | 36 | 18 | 164 | 109 | 62 | 1148.5 | 259 | 11 | 23.5 | 17 | 11 | 15 | 25 | 11 | 5 | 0 | 0.5 | 697.7 | 1547.7 | 2618.9 | 2885.2 | 2991.0 |  | 52 |
| 16 | feel the agi | top | 71 | 80.3 | 2388.4 | 200 | 24 | 98.6 | shop | 114473 | 12 | 3 | 6 | 11 | 7 | 3 | 6 | 29 | 151 | 12 | 389 | 163 | 24 | 12 | 202 | 88 | 40 | 1054 | 228 | 11 | 11 | 16 | 11 | 7 | 29 | 16 | 7 | 0 | 0.6 | 735.6 | 1724.7 | 2470.0 | 2658.6 | 2841.7 | 3043.2 | 118 |
| 17 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | batch | 64 | 84.4 | 2397.3 | 200 | 200 | 64.1 | none | 103297 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 405 | 111 | 37 | 12 | 126 | 102.5 | 71 | 1085.5 | 258 | 11 | 11 | 19 | 15 | 6 | 20 | 0 | 0 | 1 | 0 | 701.3 | 1686.6 | 2607.5 | 2894.9 | 2946.6 |  | 49 |
| 18 | Otter Vibe | top | 152 | 69.7 | 2688.6 | 100 | 100 | 100 | none | 103985.5 | 15 | 3 | 5 | 10 | 7 | 7 | 6 | 24 | 104.5 | 15 | 369 | 188.5 | 45.5 | 0 | 42 | 29 | 20.5 | 754.5 | 198.5 | 22 | 22 | 15 | 14 | 14 | 4 | 1 | 1 | 0 | 0.4 | 678.7 | 1508.8 | 2542.6 | 2848.9 | 2947.6 | 3026.3 | 58 |
| 19 | Zhenghongshuang | batch | 72 | 83.3 | 2388.1 | 200 | 200 | 59.7 | weed | 97905 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 157 | 12 | 355.5 | 110 | 35 | 12 | 151 | 127.5 | 86 | 1149 | 272.5 | 11 | 11 | 16 | 11 | 6 | 20 | 0 | 0 | 0 | 0 | 701.6 | 1642.7 | 2564.2 | 2855.8 | 2946.5 |  | 59 |
| 20 | kyy666 | batch | 82 | 82.9 | 2462.6 | 200 | 200 | 70.7 | shop | 103416.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 397 | 112.5 | 37 | 12 | 123 | 108 | 74 | 1088 | 259 | 11 | 11 | 19 | 13 | 6 | 20 | 0 | 0 | 1 | 0 | 703.6 | 1533.3 | 2550.0 | 2845.6 | 2927.5 |  | 74 |
| 21 | Kilupy | batch | 76 | 80.3 | 2517.3 | 200 | 200 | 68.4 | shop | 100873 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 405 | 110 | 37 | 12 | 122 | 102.5 | 85 | 1079.5 | 265 | 11 | 11 | 19 | 15 | 6 | 19 | 0 | 0 | 1 | 0 | 694.9 | 1698.1 | 2719.2 | 2926.6 |  |  | 36 |
| 22 | elmo | batch | 73 | 83.6 | 2413.7 | 200 | 200 | 65.8 | weed | 105124 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 153 | 12 | 405 | 115 | 38 | 12 | 131 | 101 | 85 | 1998 | 265 | 11 | 11 | 19 | 12 | 6 | 19 | 0 | 0 | 1 | 0 | 697.1 | 1565.6 | 2563.7 | 2826.4 | 2928.4 |  | 70 |
| 23 | ElephtAI | batch | 72 | 84.7 | 2468.1 | 200 | 100 | 61.1 | none | 99151.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 417 | 103.5 | 36 | 12 | 126 | 113 | 74 | 1074 | 267 | 11 | 11 | 18 | 11 | 7 | 19 | 0 | 0 | 1 | 0 | 768.4 | 1679.9 | 2642.5 | 2942.2 | 2900.9 |  | 42 |
| 29 | Emile Andrieu | batch | 63 | 79.4 | 2348.8 | 200 | 200 | 82.5 | shop | 102162 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 439 | 111 | 37 | 12 | 128 | 109 | 72 | 1076 | 258 | 11 | 11 | 19 | 15 | 6 | 20 | 0 | 0 | 1 | 0 | 718.2 | 1572.2 | 2671.2 | 2789.1 | 2896.7 |  | 85 |
| 30 | mtmr_s1 | batch | 71 | 87.3 | 2369.4 | 200 | 100 | 95.8 | weed | 102829 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 151 | 12 | 402 | 124 | 40 | 12 | 153 | 119 | 74 | 1190 | 257 | 11 | 11 | 16 | 11 | 7 | 21 | 1 | 1 | 45 | 0.0 | 694.6 | 1473.9 | 2484.5 | 2838.6 | 2896.1 |  | 76 |
| 31 | Kaggriculture Agent | batch | 63 | 79.4 | 2387.7 | 24 | 24 | 58.7 | none | 99763 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 159 | 12 | 408 | 116 | 35 | 12 | 140 | 155 | 109 | 4713 | 574 | 11 | 11 | 18 | 11 | 6 | 20 | 0 | 0 | 45 | 0 | 714.8 | 1608.1 | 2657.9 | 2872.9 | 2916.7 |  | 60 |
| 38 | THUNDER THUNDER | batch | 70 | 78.6 | 2262.7 | 100 | 100 | 100 | none | 103235.5 | 12 | 3 | 4 | 8 | 9 | 6.5 | 2 | 34 | 138.5 | 13 | 299 | 181 | 39 | 23.5 | 217 | 116.5 | 49 | 1253.5 | 223.5 | 18 | 21 | 15 | 9 | 7 | 17 | 18 | 5 | 0 | 1.1 | 696.6 | 1555.9 | 2249.0 | 2569.2 | 2729.6 | 2872.8 | 226 |
| 39 | yomogii | batch | 78 | 85.9 | 2393.9 | 48 | 24 | 70.5 | none | 102744.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 403 | 108 | 36.5 | 12 | 129 | 96.5 | 75 | 1117.5 | 266 | 11 | 11 | 19 | 15 | 6 | 20 | 0 | 0 | 1 | 0 | 685.0 | 1519.9 | 2489.5 | 2805.2 |  |  | 95 |
| 47 | doubao | batch | 75 | 74.7 | 2345.6 | 200 | 200 | 69.3 | shop | 111169 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 400 | 119 | 37 | 12 | 129 | 101 | 90 | 1105 | 273 | 11 | 11 | 19 | 12 | 7 | 20 | 0 | 0 | 1 | 0 | 714.7 | 1716.4 | 2290.8 | 2558.7 | 2774.5 | 2890.9 | 212 |
| 48 | Tom&Jerry | batch | 76 | 76.3 | 2432.9 | 200 | 200 | 69.7 | weed | 101110.5 | 12 | 3 | 6 | 11 | 8 | 6 | 3 | 33 | 162 | 12 | 405 | 111 | 37 | 12 | 122 | 100 | 62.5 | 1080 | 264 | 11 | 11 | 19 | 15 | 6 | 19 | 0 | 0 | 1 | 0 | 736.2 | 1711.6 | 2506.0 | 2799.3 | 2887.6 |  | 104 |

