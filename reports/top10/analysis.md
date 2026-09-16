# Analysis: what the zone study says once the mechanisms are read

Built by `scripts/top10/deep.py` on the rebuilt traces (trace version 2, see P18). Groups and zones as in `groups.md` (snapshot 2026-09-15T1342Z). Sections 1-6 read mechanisms behind the study's statistics; sections 7-10 use the corrected sales data.

## 1. Day 1: two purchase lists run the plateau, and nobody reads the opponent

The study's branch-driver table said the #1 and Orbital Terraformer "leave their usual day-1
opening when the opponent's opening is unusual". Reading the openings shows what the branch
is. Every team whose games split on day 1 has **one** purchase list; the lines differ only in
the number of wheat seeds planted at the end of the day, because the list spends the $3,000
down to the last few dollars and the final wheat seeds are bought one at a time while the
wheat price (moved by a dollar or two by the opponent's turn-0 wheat trades) decides how many
fit. Checked turn by turn in three replays of the #1 (107673304, 107674293, 107682064: $7, $6,
$5 left; 12, 11, 9 wheat planted; identical farmer actions). The table lists every day-1 line
with at least two games among the teams ranked 50 or better.

| rank | team | day-1 line | games | win % | seat 0 % | $ left at day end | bought | planted / built |
|---|---|---|---|---|---|---|---|---|
| 2 | Majkel1337 | 422a8637 | 47 | 85 | 60 | 7 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 12 plant wheat |
| 2 | Majkel1337 | 88cd11eb | 46 | 91 | 41 | 7 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 11 plant wheat |
| 2 | Majkel1337 | c4901de3 | 9 | 89 | 56 | 3.50 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 9 plant wheat |
| 3 | Unknown Mother-Goose | 91eafbf9 | 3 | 67 | 0 | 1 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 5 plant wheat |
| 3 | Unknown Mother-Goose | cfefcbaa | 79 | 91 | 44 | 25 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 4 | DSM | 422a8637 | 43 | 98 | 56 | 8 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 12 plant wheat |
| 4 | DSM | 88cd11eb | 36 | 94 | 42 | 6.50 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 11 plant wheat |
| 4 | DSM | c4901de3 | 3 | 100 | 67 | 5 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 10 seed wheat | 5 pasture, 8 plant melon, 9 plant wheat |
| 7 | Orbital Terraformer | 826802ff | 46 | 93 | 39 | 7 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 11 seed wheat | 5 pasture, 8 plant melon, 10 plant wheat |
| 7 | Orbital Terraformer | 91618c54 | 4 | 50 | 50 | 0 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 12 seed wheat | 5 pasture, 8 plant melon, 23 plant wheat |
| 7 | Orbital Terraformer | a87c2093 | 24 | 75 | 42 | 7.50 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 11 seed wheat | 5 pasture, 8 plant melon, 11 plant wheat |
| 7 | Orbital Terraformer | c1ef4ad1 | 2 | 100 | 50 | 8 | 2 animal cow, 3 animal sheep, 4 hire, 6 seed melon, 11 seed wheat | 5 pasture, 8 plant melon, 9 plant wheat |
| 8 | Sida Zuo | 06c2d08a | 33 | 88 | 45 | 16.50 | 3 animal cow, 2 animal sheep, 5 hire, 8 seed melon, 2 seed wheat | 7 pasture, 8 plant melon, 2 plant wheat |
| 8 | Sida Zuo | 69320dff | 2 | 100 | 100 | 17.50 | 3 animal cow, 2 animal sheep, 5 hire, 8 seed melon, 1 seed wheat | 7 pasture, 8 plant melon, 1 plant wheat |
| 8 | Sida Zuo | e991c339 | 15 | 100 | 40 | 12 | 3 animal cow, 2 animal sheep, 5 hire, 8 seed melon, 3 seed wheat | 7 pasture, 8 plant melon, 3 plant wheat |
| 12 | Mengfei Li | 2eb37790 | 6 | 83 | 17 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 30b011c0 | 11 | 64 | 45 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 3bc18d7a | 7 | 86 | 43 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 3f773371 | 6 | 100 | 67 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 461f4863 | 10 | 100 | 60 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 72dc56e3 | 7 | 86 | 71 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | 992d5b35 | 3 | 67 | 33 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | b32241c1 | 3 | 100 | 33 | 29 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | b478e1df | 8 | 75 | 75 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | d6fbdade | 6 | 83 | 33 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | d87910c1 | 12 | 67 | 42 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 12 | Mengfei Li | ed9091fa | 6 | 67 | 83 | 25.50 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 14 | Catalyst | 9b0c82fd | 76 | 79 | 49 | 21.50 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 14 | Catalyst | a6a57513 | 9 | 89 | 67 | 26 | 2 animal cow, 2 animal sheep, 5 hire, 11 seed melon, 7 seed wheat | 4 pasture, 11 plant melon, 7 plant wheat |
| 19 | carbonapi | 922fd52d | 2 | 100 | 0 | 40 | 2 animal cow, 2 animal sheep, 5 hire, 11 seed melon, 8 seed wheat | 4 pasture, 11 plant melon, 8 plant wheat |
| 19 | carbonapi | b2e0fb8e | 51 | 84 | 49 | 28 | 2 animal cow, 2 animal sheep, 5 hire, 11 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 31 | redblackbst | 1985e1fb | 3 | 0 | 67 | 7 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 4 seed wheat | 4 pasture, 12 plant melon, 4 plant wheat |
| 31 | redblackbst | 5b73fb26 | 4 | 100 | 100 | 5 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 6 seed wheat | 4 pasture, 12 plant melon, 6 plant wheat |
| 31 | redblackbst | 9e6ec2e8 | 4 | 100 | 75 | 12.50 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 5 seed wheat | 4 pasture, 12 plant melon, 5 plant wheat |
| 31 | redblackbst | cfefcbaa | 86 | 77 | 50 | 23 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 31 | redblackbst | d8986986 | 7 | 71 | 71 | 25.50 | 2 animal cow, 2 animal sheep, 5 hire, 11 seed melon, 7 seed wheat | 4 pasture, 11 plant melon, 7 plant wheat |
| 32 | Kilupy | 9b0c82fd | 73 | 81 | 44 | 24 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 32 | Kilupy | a6a57513 | 3 | 67 | 67 | 51 | 2 animal cow, 2 animal sheep, 5 hire, 11 seed melon, 7 seed wheat | 4 pasture, 11 plant melon, 7 plant wheat |
| 35 | Kaggriculture Agent | 9b0c82fd | 64 | 73 | 64 | 28.50 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 35 | Kaggriculture Agent | bf60412b | 6 | 83 | 50 | 9 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 6 plant wheat |
| 38 | elmo | 9b0c82fd | 69 | 84 | 41 | 19 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |
| 38 | elmo | d6b925bb | 2 | 100 | 100 | 9 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 5 seed wheat | 4 pasture, 12 plant melon, 5 plant wheat |
| 46 | Emile Andrieu | 9b0c82fd | 68 | 75 | 59 | 21 | 2 animal cow, 2 animal sheep, 5 hire, 12 seed melon, 7 seed wheat | 4 pasture, 12 plant melon, 7 plant wheat |

Two lists cover the plateau: **2 cows, 3 sheep, 5 pastures, 8 melon, 10-11 wheat, 4 hands**
(Majkel1337, DSM and Orbital Terraformer, byte-identical between the first two) and
**2 cows, 2 sheep, 4 pastures, 12 melon, 7 wheat, 5 hands** (the public family, Unknown
Mother-Goose, redblackbst, Mengfei Li, Catalyst, yomogii, Kaggriculture Agent). Mengfei Li's
twelve day-1 lines have identical purchases and identical money at day end: walking order.
HowardLeeTW (5 cows, 1 sheep, 18 wheat, 1 melon, 7 hands) and Sida Zuo (3 cows, 2 sheep,
7 pastures, 8 melon) are the only different day-1 plans in the top 50. Consequence for the
memo: finding 4 and "layer 2, a day-1 opponent read" have no evidence behind them (P17).

## 2. "Standing weeds" are exhausted strawberries, and a full farm cannot grow a weed

Tile-level pass over 144 current-submission replays of 18 teams
(`scripts/top10/weed_tiles.py`, 2837 weed events). The engine rolls the 0.5% weed chance only on
**empty** unlocked tiles; the plateau farm keeps every tile occupied from day 8, so weeds that
spawn are rare (107 of 2837 events, 0.1 to 2 a game). Everything else counted as a "weed"
in the feature table is a plant that reached the end of its life and decayed in place: a
strawberry after its fourth yield (82% of decay events), or wheat,
tomato and carrot left unharvested by the leaders. The public family digs every one within
about 0.6 days; the leaders leave 5-27% of the mid-game ones standing for a day or two while
they have spare empty tiles, and most of the ones that decay in the last three days forever.

| rank | team | group | games | spawned weeds / game | decayed plants / game (day < 27) | of which strawberry % | cleared % | median days standing | empty tiles at that day end | decayed / game (day 27-29) | of which cleared % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 8 | 0.20 | 7 | 61 | 95 | 0.90 | 1 | 4.10 | 12 |
| 2 | Majkel1337 | top-14 | 8 | 2 | 14 | 42 | 83 | 1.60 | 4 | 6.10 | 27 |
| 3 | Unknown Mother-Goose | gold | 8 | 0.40 | 7.90 | 49 | 98 | 0.80 | 1 | 9.60 | 3 |
| 4 | DSM | top-14 | 8 | 0.50 | 12.40 | 52 | 84 | 0.80 | 1 | 5.50 | 5 |
| 5 | SpaTaro | top-14 | 8 | 1.80 | 20.90 | 90 | 72 | 1 | 4 | 2.40 | 0 |
| 6 | THIRD FARM CLUB | gold | 8 | 0.20 | 11.80 | 99 | 97 | 1.70 | 0 | 5.80 | 22 |
| 7 | Orbital Terraformer | top-14 | 8 | 0.90 | 11.80 | 48 | 74 | 1.90 | 3.50 | 5.20 | 10 |
| 9 | ymg_aq | top-14 | 8 | 0.80 | 8.60 | 45 | 97 | 0.60 | 0 | 3.90 | 13 |
| 10 | leave you | gold | 8 | 0.90 | 15 | 100 | 100 | 0.70 | 0 | 4 | 100 |
| 12 | Mengfei Li | top-14 | 8 | 0.10 | 24.10 | 85 | 99 | 0.70 | 0 | 16 | 3 |
| 13 | HowardLeeTW | top-14 | 8 | 0.50 | 6.40 | 69 | 98 | 0.50 | 4 | 1.40 | 55 |
| 14 | Catalyst | top-14 | 8 | 0.10 | 15 | 100 | 100 | 0.60 | 0 | 4 | 100 |
| 22 | アルモンド | top-14 | 8 | 0.80 | 17.50 | 97 | 100 | 0.70 | 1 | 5.80 | 83 |
| 28 | kyy666 | gold | 8 | 1.60 | 15 | 100 | 100 | 0.70 | 0 | 4 | 100 |
| 32 | Kilupy | silver | 8 | 0.80 | 15 | 100 | 100 | 0.60 | 0 | 4 | 100 |
| 41 | Thomas Tschinkel | top-14 | 8 | 1 | 15 | 100 | 100 | 0.70 | 0 | 4.20 | 97 |
| 601 | Cyrus | bronze | 8 | 0.60 | 15 | 100 | 100 | 0.70 | 0 | 4 | 100 |
| 881 | Toru59er | bronze | 8 | 0.20 | 15 | 100 | 100 | 0.60 | 0 | 4 | 100 |

So memo finding 14 ("the top 7 tolerate weeds") describes an executor that digs when it needs
the tile, not a labour strategy: an exhausted plant costs one DIG whether it is removed before
or after it turns into a weed, which is why the DIG counts match. Finding 5 (weeds coupled to
the opponent through the shared random stream) stands, but it bites only while a farm has
empty tiles: the first week, and the leaders' spare tiles.

## 3. Everyone on the plateau reacts to the shop draw; the leaders react to more of it

The town unlocks eight shop instances at days 3, 6, 9, ... 24, drawn with replacement, and each
instance consumes one of every product it lists every four turns (12 a day; a single-product
shop 24 a day) against a town centre that takes one of each a day. A premium product's whole
demand curve is therefore decided by the draw. Conditioning each team's current-submission
games on the shops unlocked by day 9 (the first three entries of `shops`):

| group | teams | sheep: shop / none | cows: shop / none | geese: shop / none | carrot plantings: shop / none | tomato plantings: shop / none |
|---|---|---|---|---|---|---|
| top-14 | 14 | 11.0 / 4.0 | 8.0 / 5.0 | 3.0 / 2.0 | 49.0 / 28.0 | 5.0 / 5.0 |
| gold | 14 | 11.0 / 6.0 | 8.0 / 6.0 | 3.0 / 2.0 | 35.0 / 31.0 | 0.0 / 0.0 |
| silver | 21 | 11.0 / 6.0 | 8.0 / 6.0 | 3.0 / 3.0 | 31.0 / 31.0 | 0.0 / 0.0 |
| bronze | 10 | 11.0 / 6.0 | 8.0 / 8.0 | 3.0 / 3.0 | 31.0 / 31.0 | 0.0 / 0.0 |

Every one of the profiled teams, from the #1 to the last bronze team, buys 10-14 sheep when a
Yarn Store is among the first three shops and 4-6 otherwise, and 8-9 cows against 5-7 with a
milk shop (Pizza, Ice Cream, Smoothie). The public family is therefore not a pure tape: it is
one shared agent whose herd follows the demand the town reveals, which is what the "shop"
branch driver in `groups.md` was measuring. The leaders differ in the breadth of the response:

| rank | team | group | games | sheep: shop / none | cows: shop / none | geese: shop / none | carrot plantings: shop / none | tomato plantings: shop / none |
|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 88 | 12.9 / 4.8 | 8.5 / 5.0 | 2.6 / 1.4 | 65.0 / 22.0 | 11.8 / 10.8 |
| 2 | Majkel1337 | top-14 | 103 | 11.5 / 3.8 | 9.2 / 5.6 | 2.3 / 1.1 | 71.3 / 24.6 | 9.1 / 7.3 |
| 3 | Unknown Mother-Goose | gold | 82 | 11.4 / 4.7 | 8.1 / 4.7 | 4.4 / 1.8 | 48.1 / 25.6 | 9.7 / 8.2 |
| 4 | DSM | top-14 | 82 | 11.6 / 3.6 | 9.5 / 5.7 | 2.2 / 1.0 | 76.2 / 34.4 | 9.3 / 7.2 |
| 5 | SpaTaro | top-14 | 93 | 11.9 / 4.7 | 9.4 / 4.3 | 0.0 / 0.1 | 95.0 / 23.5 | 0.0 / 0.0 |
| 6 | THIRD FARM CLUB | gold | 55 | 13.9 / 5.4 | 11.2 / 7.7 | 6.9 / 4.9 | 62.9 / 29.6 | 10.7 / 10.1 |
| 7 | Orbital Terraformer | top-14 | 79 | 12.0 / 4.2 | 8.7 / 5.2 | 1.9 / 0.6 | 81.3 / 33.0 | 8.3 / 9.7 |
| 8 | Sida Zuo | gold | 51 | 12.6 / 3.8 | 7.0 / 5.5 | 5.4 / 2.5 | 75.3 / 19.1 | 9.1 / 7.0 |
| 9 | ymg_aq | top-14 | 77 | 10.3 / 4.4 | 8.6 / 5.4 | 1.3 / 0.2 | 58.5 / 19.4 | 8.3 / 6.4 |
| 10 | leave you | gold | 85 | 12.5 / 5.2 | 8.6 / 7.5 | 2.9 / 1.2 | 36.5 / 30.7 | 2.4 / 3.2 |
| 12 | Mengfei Li | top-14 | 85 | 12.5 / 5.1 | 8.2 / 6.6 | 2.3 / 1.8 | 69.7 / 19.4 | 7.7 / 6.5 |
| 13 | HowardLeeTW | top-14 | 81 | 11.5 / 3.9 | 7.5 / 5.0 | 2.3 / 1.0 | 54.5 / 34.0 | 9.4 / 8.7 |
| 14 | Catalyst | top-14 | 86 | 10.5 / 5.7 | 7.7 / 7.1 | 2.3 / 2.1 | 30.8 / 30.8 | 2.6 / 0.6 |
| 15 | feel the agi | top-14 | 88 | 13.3 / 3.8 | 9.9 / 4.1 | 7.5 / 4.3 | 55.7 / 3.4 | 2.1 / 0.4 |
| 16 | local | gold | 52 | 11.2 / 5.8 | 7.6 / 6.0 | 3.6 / 1.4 | 40.4 / 30.7 | 1.0 / 0.8 |
| 17 | lumen | gold | 50 | 12.1 / 5.6 | 8.4 / 5.5 | 2.9 / 2.2 | 38.0 / 30.5 | 1.9 / 2.0 |
| 19 | carbonapi | gold | 53 | 12.1 / 6.5 | 8.0 / 5.7 | 2.8 / 1.6 | 41.7 / 31.3 | 3.7 / 4.5 |
| 20 | Cow Boy | gold | 71 | 10.7 / 5.7 | 7.7 / 7.5 | 2.6 / 1.8 | 34.6 / 30.9 | 1.3 / 2.4 |
| 21 | Ebi | gold | 55 | 14.1 / 4.2 | 8.4 / 4.3 | 5.3 / 2.1 | 43.6 / 15.6 | 5.8 / 6.8 |
| 22 | アルモンド | top-14 | 87 | 11.0 / 5.6 | 7.8 / 5.2 | 2.7 / 2.3 | 54.1 / 35.9 | 3.7 / 4.8 |
| 23 | AI是我的豆包 | gold | 50 | 11.1 / 3.2 | 9.2 / 3.4 | 3.8 / 1.6 | 43.1 / 5.7 | 7.9 / 7.7 |
| 24 | fog flower | gold | 51 | 12.5 / 5.3 | 8.8 / 6.9 | 3.3 / 1.4 | 38.7 / 30.6 | 4.3 / 2.9 |
| 25 | Otter Vibe | top-14 | 162 | 11.6 / 4.1 | 8.5 / 3.9 | 7.1 / 4.3 | 50.8 / 24.6 | 18.6 / 18.9 |
| 26 | nilochan | gold | 56 | 10.7 / 5.8 | 7.5 / 6.1 | 3.1 / 2.1 | 30.9 / 30.7 | 1.1 / 1.7 |
| 27 | yjshyfy | gold | 57 | 12.9 / 5.3 | 8.1 / 6.9 | 3.2 / 1.4 | 35.0 / 30.0 | 5.7 / 2.7 |
| 28 | kyy666 | gold | 86 | 11.4 / 5.6 | 7.7 / 6.2 | 2.8 / 2.1 | 31.1 / 30.8 | 1.2 / 0.9 |
| 29 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | silver | 76 | 9.8 / 5.6 | 7.6 / 6.3 | 2.8 / 2.6 | 31.4 / 30.8 | 2.4 / 0.0 |
| 31 | redblackbst | top-14 | 104 | 12.1 / 4.2 | 8.2 / 4.1 | 4.7 / 1.5 | 47.9 / 42.1 | 4.0 / 5.5 |
| 32 | Kilupy | silver | 77 | 10.8 / 5.6 | 7.6 / 6.4 | 2.7 / 1.8 | 31.3 / 30.7 | 1.4 / 0.0 |
| 35 | Kaggriculture Agent | silver | 71 | 12.3 / 5.4 | 7.9 / 5.6 | 3.2 / 2.1 | 46.0 / 19.7 | 1.7 / 0.8 |
| 36 | Zhenghongshuang | silver | 80 | 11.7 / 5.5 | 8.0 / 6.7 | 3.0 / 1.8 | 38.0 / 31.8 | 2.9 / 3.5 |
| 38 | elmo | silver | 73 | 11.5 / 5.5 | 7.8 / 6.0 | 2.6 / 2.0 | 51.5 / 36.9 | 1.6 / 2.4 |
| 41 | Thomas Tschinkel | top-14 | 78 | 11.3 / 5.7 | 8.0 / 6.3 | 2.9 / 1.8 | 32.2 / 30.1 | 1.5 / 2.9 |
| 45 | mtmr_s1 | silver | 74 | 12.6 / 5.4 | 8.8 / 6.6 | 2.8 / 1.9 | 53.4 / 26.5 | 1.5 / 0.9 |
| 46 | Emile Andrieu | silver | 69 | 11.1 / 5.1 | 8.1 / 6.3 | 2.6 / 2.5 | 37.7 / 25.1 | 1.3 / 0.7 |
| 49 | THUNDER THUNDER | silver | 75 | 11.1 / 5.0 | 9.5 / 4.9 | 3.1 / 2.2 | 58.0 / 15.8 | 5.3 / 3.2 |
| 72 | doubao | silver | 77 | 11.1 / 5.7 | 7.7 / 6.2 | 2.7 / 1.9 | 31.0 / 31.0 | 1.0 / 2.4 |
| 74 | yomogii | silver | 78 | 10.8 / 5.6 | 7.8 / 6.0 | 3.1 / 2.4 | 30.7 / 30.2 | 3.0 / 2.8 |
| 75 | Tom&Jerry | silver | 79 | 11.6 / 5.8 | 7.5 / 5.8 | 3.1 / 2.4 | 31.1 / 30.7 | 2.0 / 0.6 |
| 120 | Navier-stokes | silver | 50 | 10.2 / 5.7 | 7.9 / 6.4 | 3.5 / 2.5 | 30.9 / 31.0 | 1.9 / 2.2 |
| 121 | Pai | silver | 53 | 12.1 / 5.7 | 7.9 / 5.8 | 3.2 / 2.9 | 31.2 / 30.7 | 1.4 / 3.0 |
| 122 | Munal Singh | silver | 55 | 10.7 / 5.5 | 7.8 / 5.8 | 3.0 / 1.9 | 30.9 / 30.5 | 1.6 / 0.0 |
| 227 | ElephtAI | silver | 76 | 11.9 / 5.7 | 7.9 / 6.6 | 2.0 / 1.9 | 30.9 / 30.8 | 1.6 / 1.4 |
| 250 | Bldr2 | silver | 53 | 10.1 / 5.7 | 7.8 / 6.4 | 2.9 / 2.9 | 31.4 / 30.8 | 1.8 / 0.0 |
| 251 | let cats farm | silver | 51 | 10.5 / 5.9 | 8.1 / 7.1 | 1.9 / 1.5 | 30.8 / 30.8 | 2.6 / 1.5 |
| 252 | kevin park | silver | 50 | 10.5 / 5.7 | 7.5 / 6.0 | 3.1 / 2.1 | 30.9 / 30.7 | 2.1 / 0.0 |
| 400 | peppersaltman | silver | 50 | 11.1 / 5.7 | 7.7 / 7.0 | 2.3 / 1.9 | 30.9 / 30.5 | 2.1 / 1.7 |
| 401 | Win Suthar | silver | 51 | 10.5 / 5.7 | 7.7 / 7.8 | 2.4 / 1.8 | 31.0 / 30.2 | 1.5 / 4.5 |
| 402 | spencersi123 | silver | 50 | 11.9 / 5.6 | 7.3 / 5.8 | 3.1 / 2.0 | 31.3 / 30.7 | 1.3 / 0.9 |
| 470 | Naru041104 | bronze | 51 | 9.5 / 4.4 | 8.7 / 6.1 | 2.5 / 2.1 | 30.9 / 30.9 | 1.9 / 1.1 |
| 473 | Jacky Chan | bronze | 52 | 10.4 / 5.6 | 7.7 / 6.0 | 3.1 / 2.3 | 31.5 / 30.6 | 1.0 / 1.8 |
| 600 | 最强扫地僧 | bronze | 50 | 10.5 / 5.6 | 7.8 / 7.0 | 2.1 / 2.3 | 30.9 / 30.7 | 1.4 / 0.0 |
| 601 | Cyrus | bronze | 50 | 12.1 / 5.7 | 8.0 / 6.7 | 2.3 / 2.2 | 30.9 / 30.8 | 1.1 / 2.1 |
| 602 | matcha110 | bronze | 50 | 11.0 / 5.8 | 7.5 / 6.9 | 1.8 / 2.4 | 30.9 / 30.3 | 1.7 / 0.0 |
| 750 | Daiki Takahashi | bronze | 51 | 9.8 / 5.6 | 7.9 / 6.7 | 2.4 / 1.8 | 30.9 / 30.9 | 1.5 / 0.9 |
| 751 | ansheng jhang | bronze | 50 | 11.9 / 5.7 | 7.6 / 7.1 | 2.2 / 1.9 | 30.8 / 30.6 | 0.9 / 0.0 |
| 752 | CaliforniaDog | bronze | 50 | 10.7 / 5.7 | 8.0 / 7.6 | 2.7 / 2.3 | 31.0 / 30.7 | 1.8 / 1.0 |
| 881 | Toru59er | bronze | 50 | 10.0 / 5.7 | 7.9 / 7.1 | 2.2 / 2.4 | 31.0 / 30.6 | 2.1 / 0.0 |
| 882 | broccoli | bronze | 51 | 10.0 / 5.7 | 8.1 / 7.6 | 2.5 / 2.8 | 30.9 / 30.6 | 1.1 / 2.9 |

Carrots and tomatoes are where the leaders react and the family does not (the family plants
31 carrots and no tomatoes whatever the draw). SpaTaro goes furthest on herds (20 sheep with a
Yarn Store, 13 cows with a milk shop). The reactive layer that exists on the ladder is
"produce what the town is buying", and the study's reactivity gradient is a gradient in the
breadth of that response, not in whether a team reacts. Counting, per team, how many of the
five products its plan follows (thresholds: 3 sheep, 1.5 cows, 1 goose, 10 carrots, 3
tomatoes between games with and without the shop by day 9):

| group | median | mean | AUC vs next zone |
|---|---|---|---|
| top-14 | 1 | 1 | 0.50 (p=1.00) |
| gold | 1 | 1 | 0.50 (p=1.00) |
| silver | 1 | 1 | 0.50 (p=1.00) |
| bronze | 1 | 1 | 0.50 (p=1.00) |

| rank | team | group | d sheep | d cows | d geese | d carrots | d tomatoes | breadth (0-5) |
|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 8.10 | 3.50 | 1.20 | 43 | 7.30 | 1 |
| 2 | Majkel1337 | top-14 | 7.70 | 3.60 | 1.20 | 46.70 | 7.50 | 1 |
| 3 | Unknown Mother-Goose | gold | 6.60 | 3.40 | 2.60 | 22.50 | 5.20 | 1 |
| 4 | DSM | top-14 | 8 | 3.80 | 1.10 | 41.80 | 7.30 | 1 |
| 5 | SpaTaro | top-14 | 7.30 | 5.10 | -0.10 | 71.50 | 0 | 1 |
| 6 | THIRD FARM CLUB | gold | 8.60 | 3.50 | 1.90 | 33.30 | 3.90 | 1 |
| 7 | Orbital Terraformer | top-14 | 7.80 | 3.50 | 1.20 | 48.30 | 0.40 | 1 |
| 8 | Sida Zuo | gold | 8.80 | 1.50 | 2.90 | 56.30 | 10.50 | 1 |
| 9 | ymg_aq | top-14 | 5.90 | 3.20 | 1.10 | 39.10 | 7 | 1 |
| 10 | leave you | gold | 7.30 | 1.20 | 1.70 | 5.80 | 4.40 | 1 |
| 12 | Mengfei Li | top-14 | 7.40 | 1.60 | 0.50 | 50.20 | 9.90 | 1 |
| 13 | HowardLeeTW | top-14 | 7.60 | 2.50 | 1.30 | 20.50 | 8.30 | 1 |
| 14 | Catalyst | top-14 | 4.80 | 0.60 | 0.10 | 0 | 3.30 | 1 |
| 15 | feel the agi | top-14 | 9.60 | 5.80 | 3.20 | 52.30 | 3.10 | 1 |
| 16 | local | gold | 5.50 | 1.60 | 2.30 | 9.70 | 1.80 | 1 |
| 17 | lumen | gold | 6.50 | 2.80 | 0.70 | 7.50 | 3.30 | 1 |
| 19 | carbonapi | gold | 5.60 | 2.30 | 1.30 | 10.40 | 2 | 1 |
| 20 | Cow Boy | gold | 4.90 | 0.20 | 0.80 | 3.70 | 2.80 | 1 |
| 21 | Ebi | gold | 9.80 | 4.10 | 3.20 | 28 | 8.70 | 1 |
| 22 | アルモンド | top-14 | 5.40 | 2.60 | 0.40 | 18.20 | 6.20 | 1 |
| 23 | AI是我的豆包 | gold | 7.90 | 5.90 | 2.10 | 37.40 | 1.60 | 1 |
| 24 | fog flower | gold | 7.20 | 2 | 1.90 | 8.10 | 7.10 | 1 |
| 25 | Otter Vibe | top-14 | 7.50 | 4.60 | 2.80 | 26.30 | 11.30 | 1 |
| 26 | nilochan | gold | 4.90 | 1.40 | 1 | 0.20 | 1.90 | 1 |
| 27 | yjshyfy | gold | 7.70 | 1.20 | 1.80 | 5.10 | 5.80 | 1 |
| 28 | kyy666 | gold | 5.80 | 1.60 | 0.70 | 0.30 | 2.40 | 1 |
| 29 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | silver | 4.20 | 1.30 | 0.30 | 0.60 | 3.70 | 1 |
| 31 | redblackbst | top-14 | 7.90 | 4.10 | 3.20 | 5.80 | 2.40 | 1 |
| 32 | Kilupy | silver | 5.20 | 1.20 | 0.90 | 0.60 | 2 | 1 |
| 35 | Kaggriculture Agent | silver | 6.90 | 2.30 | 1.10 | 26.20 | 2.50 | 1 |
| 36 | Zhenghongshuang | silver | 6.20 | 1.30 | 1.10 | 6.10 | 4.70 | 1 |
| 38 | elmo | silver | 5.90 | 1.80 | 0.70 | 14.60 | 3.50 | 1 |
| 41 | Thomas Tschinkel | top-14 | 5.60 | 1.70 | 1.10 | 2.10 | 2.70 | 1 |
| 45 | mtmr_s1 | silver | 7.30 | 2.20 | 0.90 | 26.90 | 2.10 | 1 |
| 46 | Emile Andrieu | silver | 6 | 1.90 | 0.10 | 12.60 | 2 | 1 |
| 49 | THUNDER THUNDER | silver | 6.20 | 4.60 | 0.80 | 42.20 | 7.20 | 1 |
| 72 | doubao | silver | 5.50 | 1.50 | 0.80 | 0 | 2.20 | 1 |
| 74 | yomogii | silver | 5.20 | 1.90 | 0.70 | 0.50 | 3.70 | 1 |
| 75 | Tom&Jerry | silver | 5.80 | 1.70 | 0.70 | 0.40 | 2.70 | 1 |
| 120 | Navier-stokes | silver | 4.40 | 1.40 | 0.90 | -0.10 | 3.10 | 1 |
| 121 | Pai | silver | 6.40 | 2.10 | 0.30 | 0.50 | 3.10 | 1 |
| 122 | Munal Singh | silver | 5.20 | 2 | 1.10 | 0.40 | 2.80 | 1 |
| 227 | ElephtAI | silver | 6.30 | 1.40 | 0.10 | 0.10 | 3.20 | 1 |
| 250 | Bldr2 | silver | 4.40 | 1.40 | 0 | 0.60 | 3 | 1 |
| 251 | let cats farm | silver | 4.60 | 1 | 0.30 | 0 | 3.70 | 1 |
| 252 | kevin park | silver | 4.80 | 1.50 | 1 | 0.20 | 3.50 | 1 |
| 400 | peppersaltman | silver | 5.40 | 0.70 | 0.40 | 0.40 | 3.30 | 1 |
| 401 | Win Suthar | silver | 4.80 | -0.20 | 0.60 | 0.80 | 3.10 | 1 |
| 402 | spencersi123 | silver | 6.30 | 1.50 | 1.10 | 0.70 | 2.40 | 1 |
| 470 | Naru041104 | bronze | 5.20 | 2.60 | 0.40 | 0.10 | 3.20 | 1 |
| 473 | Jacky Chan | bronze | 4.80 | 1.70 | 0.80 | 0.90 | 1.90 | 1 |
| 600 | 最强扫地僧 | bronze | 4.80 | 0.80 | -0.20 | 0.20 | 2.20 | 1 |
| 601 | Cyrus | bronze | 6.40 | 1.30 | 0.10 | 0.10 | 2.60 | 1 |
| 602 | matcha110 | bronze | 5.20 | 0.60 | -0.70 | 0.50 | 2.90 | 1 |
| 750 | Daiki Takahashi | bronze | 4.20 | 1.20 | 0.50 | 0 | 2.50 | 1 |
| 751 | ansheng jhang | bronze | 6.20 | 0.50 | 0.30 | 0.10 | 1.40 | 1 |
| 752 | CaliforniaDog | bronze | 5 | 0.40 | 0.40 | 0.30 | 2.70 | 1 |
| 881 | Toru59er | bronze | 4.30 | 0.80 | -0.10 | 0.40 | 2.40 | 1 |
| 882 | broccoli | bronze | 4.30 | 0.50 | -0.40 | 0.30 | 2.80 | 1 |

Every bronze team follows the Yarn Store and nothing else; the family agent ships with
switches its users set differently (Catalyst 2, Kaggriculture Agent 4, feel the agi 5 on the
same day-1 line).

## 4. The plateau is a sequence of public lines, each replacing the last within a week

Grouping every sampled seat (both players of every sampled game, 14788 seats) by its
farmer-and-hand action line through day 5 (`field_h136`) and keeping the lines with at least
100 seats gives the public generations of the tape. Medians per line:

| seats | teams | first | last | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank | line | current subs on it |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 114 | 37 | 08-03 | 09-14 | 12 | 8 | 6 | 0 | 44 | 66 | 21 | 0 | 0 | 308 | 107 | 120528 | G1 |  |
| 190 | 82 | 08-08 | 09-15 | 14 | 8 | 6 | 0 | 42 | 92 | 24 | 0 | 0 | 322 | 80 | 79038 | G2 |  |
| 493 | 145 | 08-13 | 09-15 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 87052 | G3 |  |
| 123 | 76 | 08-14 | 09-15 | 14 | 8 | 4 | 0 | 37 | 143 | 19 | 0 | 0 | 967 | 72 | 90862 | G4 |  |
| 303 | 175 | 08-14 | 09-15 | 12 | 8 | 4 | 0 | 42 | 125 | 12 | 5 | 0 | 318 | 70 | 84647 | G5 |  |
| 152 | 107 | 08-14 | 09-15 | 14 | 9 | 4 | 0 | 37 | 143 | 19 | 0 | 0 | 285 | 72 | 85130 | G6 |  |
| 258 | 103 | 08-23 | 09-15 | 15 | 11 | 4 | 0 | 41 | 134 | 11 | 20 | 0 | 343 | 80 | 86494 | G7 |  |
| 190 | 85 | 08-30 | 09-14 | 12 | 9 | 5 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 88170 | G8 |  |
| 111 | 79 | 09-01 | 09-15 | 12 | 9 | 5 | 0 | 38 | 185 | 12 | 9 | 0 | 351 | 62 | 90946 | G9 |  |
| 822 | 335 | 09-02 | 09-15 | 12 | 9 | 6 | 1 | 33 | 185 | 12 | 9 | 0 | 381 | 92 | 93177 | G10 | feel the agi |
| 4895 | 1088 | 09-09 | 09-15 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 415 | 106 | 98859 | G11 | Thomas Tschinkel, Tom&Jerry, Catalyst, 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔, mtmr_s1, アルモンド (+27) |
| 342 | 17 | 09-10 | 09-15 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 367 | 104 | 101258 | G12 | leave you, Zhenghongshuang, yjshyfy, fog flower |
| 112 | 8 | 09-11 | 09-14 | 11 | 8 | 5 | 3 | 32 | 163 | 12.50 | 41 | 0 | 347 | 84 | 99896 | G13 | redblackbst |
| 196 | 2 | 09-11 | 09-15 | 13 | 7 | 6 | 2 | 26.50 | 145 | 13 | 37 | 9 | 307 | 149 | 101040 | G14 | Artem The Farmer 🍅 |
| 187 | 166 | 09-12 | 09-15 | 12 | 6 | 5 | 3 | 33 | 163 | 12 | 31 | 0 | 414 | 87 | 90672 | G15 | spencersi123 |
| 158 | 19 | 09-13 | 09-15 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 400 | 117 | 103788 | G16 | doubao |

Share of sampled seats on each line by game date (percent; the sample over-weights the
studied teams' windows, so read the columns as when a line appeared and when it went, not as
ladder-wide shares):

| day | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | G9 | G10 | G11 | G12 | G13 | G14 | G15 | G16 | other | seats |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 07-30 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 100 | 50 |
| 07-31 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 100 | 126 |
| 08-02 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 100 | 70 |
| 08-03 | 46 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 54 | 114 |
| 08-04 | 52 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 48 | 98 |
| 08-08 | 2 | 62 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 100 |
| 08-14 |  | 3 | 36 | 16 |  | 13 |  |  |  |  |  |  |  |  |  |  | 32 | 296 |
| 08-15 |  | 3 | 61 | 2 |  | 7 |  |  |  |  |  |  |  |  |  |  | 27 | 150 |
| 08-18 |  | 24 | 42 | 1 | 13 | 1 |  |  |  |  |  |  |  |  |  |  | 19 | 86 |
| 08-19 |  | 13 | 39 |  | 11 |  |  |  |  |  |  |  |  |  |  |  | 37 | 110 |
| 08-22 |  | 1 | 9 | 3 | 12 | 4 |  |  |  |  |  |  |  |  |  |  | 71 | 200 |
| 08-23 |  | 3 | 6 | 4 | 6 | 4 | 22 |  |  |  |  |  |  |  |  |  | 57 | 200 |
| 08-24 |  | 1 | 6 | 4 | 18 | 2 | 30 |  |  |  |  |  |  |  |  |  | 39 | 100 |
| 08-26 |  | 1 | 7 | 3 | 20 | 12 | 25 |  |  |  |  |  |  |  |  |  | 32 | 378 |
| 08-27 |  | 5 | 23 | 5 | 5 | 1 | 1 |  |  |  |  |  |  |  |  |  | 60 | 220 |
| 08-28 |  | 1 | 2 | 2 | 4 |  | 1 |  |  |  |  |  |  |  |  |  | 90 | 184 |
| 09-01 |  | 10 | 14 |  | 3 | 1 | 6 | 34 | 3 |  |  |  |  |  |  |  | 28 | 158 |
| 09-02 |  |  | 1 |  | 2 | 2 | 3 | 5 | 1 | 2 |  |  |  |  |  |  | 82 | 212 |
| 09-03 |  | 1 | 1 | 1 | 2 | 1 | 1 | 16 | 3 | 2 |  |  |  |  |  |  | 72 | 440 |
| 09-04 |  |  | 2 |  | 2 | 1 | 3 | 7 | 3 | 9 |  |  |  |  |  |  | 73 | 276 |
| 09-05 |  |  |  |  |  |  |  |  | 5 | 40 |  |  |  |  |  |  | 54 | 372 |
| 09-06 |  |  |  |  |  |  |  |  | 7 | 47 |  |  |  |  |  |  | 45 | 200 |
| 09-07 |  |  |  |  | 14 |  | 7 | 4 | 2 | 7 |  |  |  |  |  |  | 66 | 286 |
| 09-08 |  |  | 2 |  | 6 |  | 1 | 1 | 2 | 22 |  |  |  |  |  |  | 66 | 280 |
| 09-09 |  |  |  |  | 2 |  | 1 | 1 | 2 | 22 | 12 |  |  |  |  |  | 59 | 598 |
| 09-10 |  | 1 |  |  | 2 |  | 1 |  | 1 | 31 | 38 |  |  |  |  |  | 25 | 238 |
| 09-11 |  |  |  | 1 |  |  |  |  | 1 | 6 | 25 | 1 | 1 | 7 |  |  | 58 | 688 |
| 09-12 |  |  | 1 |  | 1 | 1 |  |  |  | 4 | 41 | 1 | 1 |  | 2 |  | 48 | 396 |
| 09-13 |  | 1 |  |  |  | 1 |  |  |  | 3 | 37 |  |  | 6 |  | 6 | 45 | 828 |
| 09-14 |  |  |  |  |  |  |  |  |  | 3 | 55 | 4 | 2 | 2 | 3 | 1 | 29 | 6286 |
| 09-15 |  |  |  |  | 1 |  |  |  |  | 2 | 68 | 7 |  |  | 1 | 2 | 18 | 946 |

The line that runs the medal plateau today (G with 33 strawberry, 163 wheat, 12 melon, 31
carrot, 8 cows, 6 sheep, 3 geese) first appears on 2026-09-09 and is on two thirds of sampled
seats by 09-15; the line before it (33 strawberry, 185 wheat, 9 carrots, 1 goose) appeared
on 09-02 and peaked on 09-05/06; before that, lines from 08-30, 08-23, 08-14 and 08-03 each
had their week. A new public line every seven to ten days is the ladder's clock, and the
final tournament (games after 2026-09-30) will be played against whatever line is public by
then, not against today's. The one line in the table that belongs to a leader is Artem The
Farmer's (26.5 strawberry, 145 wheat, 37 carrot, 9 tomato, land on days 6 and 8, 149
fertilize), on three teams' seats.

## 5. Trajectories: everyone climbed in the same week, on new submissions

![rating paths](figs/an_rating_paths_top15.png)

One line per submission, rating after each public game, teams ranked 1-15. The picture is the
same for almost every team: weeks of submissions between 1,000 and 2,500, then a new
submission between 2026-09-06 and 09-13 that goes to 3,000 within its first hundred games.
Ratings are relative, so a 2,900 in early August (DSM, Mengfei Li, leave you, Thomas
Tschinkel, Kaggriculture Agent, THUNDER THUNDER, fog flower, Jacky Chan, Cyrus, kevin park,
Emile Andrieu, local) meant less than a 2,900 now; the table dates each team's first game
rated 2,900 or more and how many submissions it took.

| rank | team | group | first public game | submissions found | first game rated 2900+ | submissions before it | days to it |
|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 08-19 | 21 | 09-11 | 15 | 22.90 |
| 2 | Majkel1337 | top-14 | 08-27 | 10 | 09-10 | 8 | 14.20 |
| 3 | Unknown Mother-Goose | gold | 08-23 | 25 | 09-09 | 10 | 17.80 |
| 4 | DSM | top-14 | 08-12 | 73 | 08-15 | 8 | 3.50 |
| 5 | SpaTaro | top-14 | 08-22 | 19 | 09-08 | 16 | 16.50 |
| 6 | THIRD FARM CLUB | gold | 08-18 | 59 | 09-11 | 51 | 23.50 |
| 7 | Orbital Terraformer | top-14 | 08-28 | 7 | 09-13 | 6 | 16.30 |
| 8 | Sida Zuo | gold | 08-05 | 24 | 09-15 | 24 | 41.10 |
| 9 | ymg_aq | top-14 | 08-22 | 34 | 09-07 | 22 | 16.10 |
| 10 | leave you | gold | 08-01 | 107 | 08-15 | 22 | 14 |
| 11 | 现实是个乐子 | gold | 08-06 | 60 | 09-07 | 42 | 32.40 |
| 12 | Mengfei Li | top-14 | 08-01 | 104 | 08-07 | 16 | 5.50 |
| 13 | HowardLeeTW | top-14 | 08-08 | 12 | 09-06 | 4 | 29 |
| 14 | Catalyst | top-14 | 09-12 | 7 | 09-12 | 2 | 0.30 |
| 15 | feel the agi | top-14 | 09-02 | 21 | 09-09 | 19 | 7.90 |
| 16 | local | gold | 08-15 | 50 | 08-16 | 1 | 0.70 |
| 17 | lumen | gold | 09-05 | 30 | 09-15 | 29 | 9.80 |
| 18 | Excluding | gold | 08-06 | 51 | 09-15 | 51 | 39.80 |
| 19 | carbonapi | gold | 08-24 | 25 | 09-13 | 21 | 20.30 |
| 20 | Cow Boy | gold | 08-23 | 28 | 09-13 | 27 | 21.70 |
| 21 | Ebi | gold | 09-13 | 1 | 09-15 | 1 | 1.10 |
| 22 | アルモンド | top-14 | 08-29 | 29 | 09-13 | 26 | 14.50 |
| 23 | AI是我的豆包 | gold | 08-16 | 105 | 09-14 | 102 | 29.10 |
| 24 | fog flower | gold | 08-09 | 79 | 08-11 | 4 | 2.10 |
| 25 | Otter Vibe | top-14 | 08-27 | 13 | 09-08 | 12 | 12 |
| 26 | nilochan | gold | 09-08 | 29 | 09-13 | 24 | 5 |
| 27 | yjshyfy | gold | 08-02 | 48 | 09-13 | 45 | 42.30 |
| 28 | kyy666 | gold | 09-08 | 17 | 09-12 | 10 | 4.20 |
| 29 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | silver | 09-02 | 10 | 09-14 | 8 | 11.70 |
| 31 | redblackbst | top-14 | 08-26 | 47 | 09-10 | 29 | 14.50 |
| 32 | Kilupy | silver | 09-02 | 13 | 09-14 | 13 | 12.10 |
| 35 | Kaggriculture Agent | silver | 07-31 | 106 | 08-13 | 18 | 13.20 |
| 36 | Zhenghongshuang | silver | 08-15 | 25 | 09-14 | 25 | 29.50 |
| 38 | elmo | silver | 09-04 | 23 | 09-14 | 23 | 10.50 |
| 41 | Thomas Tschinkel | top-14 | 08-13 | 88 | 08-14 | 4 | 0.80 |
| 45 | mtmr_s1 | silver | 08-22 | 32 | 09-09 | 22 | 18.20 |
| 46 | Emile Andrieu | silver | 08-03 | 14 | 08-14 | 5 | 10.60 |
| 49 | THUNDER THUNDER | silver | 07-30 | 47 | 08-08 | 21 | 9.20 |
| 72 | doubao | silver | 09-09 | 6 | 09-14 | 5 | 5.50 |
| 74 | yomogii | silver | 09-05 | 21 | 09-15 | 21 | 10 |
| 75 | Tom&Jerry | silver | 08-26 | 24 | 09-13 | 22 | 17.30 |
| 120 | Navier-stokes | silver | 09-14 | 5 | never |  |  |
| 121 | Pai | silver | 08-29 | 16 | never |  |  |
| 122 | Munal Singh | silver | 08-26 | 39 | 09-14 | 39 | 19.10 |
| 227 | ElephtAI | silver | 08-20 | 41 | 09-14 | 36 | 25.10 |
| 250 | Bldr2 | silver | 09-12 | 9 | never |  |  |
| 251 | let cats farm | silver | 08-23 | 63 | 09-10 | 54 | 18.30 |
| 252 | kevin park | silver | 07-31 | 86 | 08-07 | 16 | 6.90 |
| 400 | peppersaltman | silver | 09-07 | 9 | never |  |  |
| 401 | Win Suthar | silver | 09-09 | 8 | never |  |  |
| 402 | spencersi123 | silver | 09-03 | 30 | never |  |  |
| 470 | Naru041104 | bronze | 08-18 | 70 | 09-10 | 60 | 22.70 |
| 472 | Roman Katasonov | bronze | 09-13 | 2 | never |  |  |
| 473 | Jacky Chan | bronze | 08-05 | 37 | 08-08 | 6 | 3.10 |
| 600 | 最强扫地僧 | bronze | 09-12 | 7 | never |  |  |
| 601 | Cyrus | bronze | 08-07 | 55 | 08-11 | 7 | 3.70 |
| 602 | matcha110 | bronze | 09-08 | 7 | never |  |  |
| 750 | Daiki Takahashi | bronze | 08-30 | 7 | never |  |  |
| 751 | ansheng jhang | bronze | 09-09 | 10 | never |  |  |
| 752 | CaliforniaDog | bronze | 09-13 | 2 | never |  |  |
| 880 | MtN | bronze | 08-05 | 81 | never |  |  |
| 881 | Toru59er | bronze | 08-01 | 60 | never |  |  |
| 882 | broccoli | bronze | 09-14 | 1 | never |  |  |

Per-window farm and determinism for the teams with history windows (F first 50 games, Q1-Q3
quarter points, L last 50, C0 current submission's first 50; windows are frozen at the
sample dates in `METHOD.md`). "Modal line share" is the share of the window's games on its
most common farmer-and-hand line at day 4; "distinct" the share of distinct lines at day 16.

**Artem The Farmer 🍅** (rank 1)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-19 | 50 | 1 | 52 | 1114 | 78 | 98 | 12 | 8 | 5 | 0 | 34 | 142 | 17 | 6 | 0 | 242 | 48.50 | 76407 |
| Q1 | 09-07 | 50 | 1 | 40 | 1475 | 90 | 80 | 12 | 10 | 4 | 0 | 39 | 123 | 12 | 13.50 | 5 | 262 | 82 | 92988 |
| Q2 | 09-11 | 50 | 3 | 86 | 2542 | 94 | 100 | 13 | 7.50 | 4 | 0 | 30 | 138 | 12 | 55 | 13 | 286 | 127 | 102444 |
| Q3 | 09-13 | 50 | 2 | 90 | 2497 | 92 | 100 | 13 | 7 | 7 | 2 | 24 | 154 | 13 | 30.50 | 8 | 308 | 156 | 101644 |
| L | 09-14 | 50 | 1 | 92 | 2853 | 94 | 100 | 13 | 7 | 6 | 2 | 25 | 146 | 13 | 45.50 | 9 | 310 | 153 | 95925 |
| C0 | 09-14 | 50 | 1 | 98 | 2115 | 98 | 100 | 13 | 7.50 | 4 | 2 | 29 | 142 | 13 | 28 | 10 | 310 | 159 | 109196 |

**Majkel1337** (rank 2)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-28 | 50 | 2 | 72 | 1172 | 2 | 100 | 11 | 8 | 7 | 0 | 36 | 13.50 | 13 | 0 | 0 | 264 | 65.50 | 87165 |
| Q1 | 09-07 | 50 | 1 | 30 | 1368 | 24 | 100 | 11 | 9 | 6 | 0 | 38 | 8 | 13 | 0 | 0 | 286 | 76.50 | 82722 |
| Q2 | 09-10 | 50 | 3 | 86 | 2545 | 16 | 100 | 11 | 8 | 4 | 2 | 29.50 | 190 | 14 | 21.50 | 1 | 322 | 150 | 107964 |
| Q3 | 09-12 | 50 | 2 | 56 | 3078 | 8 | 100 | 11 | 9 | 4.50 | 2 | 31 | 187 | 14 | 23.50 | 4 | 342 | 157 | 114608 |
| L | 09-14 | 50 | 2 | 90 | 2991 | 6 | 100 | 11 | 8.50 | 5 | 0 | 30.50 | 174 | 13 | 43 | 8 | 326 | 159 | 108936 |
| C0 | 09-11 | 50 | 1 | 98 | 2118 | 22 | 100 | 11 | 8 | 4 | 2 | 31 | 178 | 14 | 37 | 7.50 | 309 | 150 | 118371 |

**Unknown Mother-Goose** (rank 3)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-23 | 50 | 2 | 74 | 1411 | 94 | 36 | 15 | 11 | 4 | 0 | 41 | 134 | 11 | 20 | 0 | 343 | 80 | 88618 |
| L | 09-14 | 50 | 2 | 80 | 2956 | 72 | 100 | 11 | 7 | 5 | 3 | 29.50 | 149 | 14 | 29 | 8.50 | 311 | 180 | 111262 |
| C0 | 09-14 | 50 | 1 | 100 | 2015 | 94 | 100 | 11 | 7 | 6 | 3 | 29.50 | 141 | 14 | 26.50 | 8 | 338 | 181 | 119640 |

**DSM** (rank 4)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-14 | 50 | 1 | 86 | 1761 | 82 | 32 | 14 | 8 | 4 | 0 | 37 | 143 | 19 | 0 | 0 | 967 | 72 | 103782 |
| Q1 | 08-26 | 50 | 4 | 30 | 1916 | 60 | 50 | 12 | 9 | 5 | 0 | 42 | 126 | 12 | 5 | 0 | 320 | 66 | 84702 |
| Q2 | 09-04 | 50 | 2 | 80 | 1720 | 96 | 14 | 12 | 9 | 5 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 94450 |
| L | 09-14 | 50 | 1 | 96 | 2827 | 26 | 100 | 11 | 8 | 4 | 2 | 30 | 188 | 14 | 50.50 | 8 | 334 | 154 | 100325 |
| C0 | 09-14 | 50 | 1 | 100 | 2128 | 20 | 100 | 11 | 9 | 5 | 2 | 30 | 187 | 14 | 36.50 | 7 | 350 | 157 | 109152 |

**SpaTaro** (rank 5)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-23 | 50 | 1 | 70 | 1240 | 100 | 16 | 12 | 10 | 7 | 0 | 24 | 154 | 11 | 0 | 0 | 278 | 59 | 93937 |
| Q1 | 09-02 | 50 | 4 | 76 | 1527 | 10 | 92 | 12 | 8 | 5 | 0 | 23 | 173 | 11 | 4.50 | 0 | 282 | 93.50 | 98947 |
| Q2 | 09-05 | 50 | 2 | 50 | 2437 | 2 | 100 | 12 | 8 | 4 | 0 | 28 | 176 | 12 | 47.50 | 0 | 245 | 99 | 88826 |
| Q3 | 09-09 | 42 | 2 | 74 | 2872 | 2 | 100 | 12 | 10.50 | 8 | 0 | 27 | 168 | 11 | 56.50 | 0 | 278 | 119 | 98494 |
| L | 09-14 | 50 | 2 | 46 | 3008 | 2 | 100 | 11 | 13 | 8 | 0 | 28 | 184 | 11 | 38.50 | 0 | 286 | 111 | 96397 |
| C0 | 09-11 | 50 | 1 | 98 | 1420 | 2 | 100 | 11 | 10 | 8 | 0 | 25.50 | 188 | 11 | 59 | 0 | 267 | 83 | 96824 |

**Orbital Terraformer** (rank 7)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-28 | 50 | 1 | 74 | 889 | 30 | 98 | 14 | 8 | 4 | 0 | 34 | 140 | 17 | 0 | 0 | 930 | 72 | 89616 |
| Q1 | 09-09 | 50 | 3 | 72 | 2004 | 16 | 90 | 12 | 15.50 | 13 | 0 | 78.50 | 228 | 16 | 40 | 0 | 254 | 146 | 94542 |
| Q2 | 09-11 | 50 | 2 | 40 | 2463 | 54 | 58 | 12 | 8 | 9 | 0 | 33 | 154 | 12 | 40 | 0 | 399 | 61 | 90448 |
| L | 09-14 | 50 | 2 | 68 | 2955 | 8 | 100 | 11 | 9 | 5 | 2 | 32 | 192 | 14 | 45 | 8 | 333 | 156 | 98386 |
| C0 | 09-13 | 50 | 1 | 98 | 1905 | 42 | 100 | 11 | 7.50 | 5 | 2 | 31 | 187 | 14 | 42 | 9 | 332 | 152 | 104433 |

**ymg_aq** (rank 9)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-22 | 50 | 1 | 80 | 1873 | 88 | 28 | 12 | 8 | 6 | 0 | 42 | 125 | 12 | 5 | 0 | 318 | 70 | 86963 |
| Q1 | 09-02 | 50 | 2 | 88 | 1694 | 32 | 18 | 12 | 9 | 5 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 83642 |
| Q2 | 09-06 | 50 | 4 | 74 | 2116 | 22 | 100 | 12 | 8 | 5 | 0 | 36 | 152 | 15 | 13.50 | 7 | 287 | 77 | 102225 |
| L | 09-14 | 50 | 2 | 62 | 2996 | 14 | 100 | 13 | 7 | 7 | 0 | 32 | 150 | 15 | 26.50 | 4.50 | 254 | 134 | 97628 |
| C0 | 09-13 | 50 | 1 | 96 | 2270 | 14 | 100 | 13 | 7 | 3.50 | 1 | 32 | 154 | 15 | 27.50 | 6 | 252 | 136 | 105736 |

**leave you** (rank 10)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-01 | 50 | 3 | 58 | 831 | 40 | 68 | 10 | 8 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 310 | 0 | 56042 |
| L | 09-14 | 50 | 2 | 68 | 2803 | 50 | 78 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 419 | 105 | 94477 |
| C0 | 09-14 | 50 | 1 | 98 | 2190 | 100 | 54 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 364 | 108 | 106720 |

**Mengfei Li** (rank 12)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-02 | 50 | 2 | 92 | 1884 | 62 | 30 | 12 | 8 | 6 | 0 | 44 | 66 | 21 | 0 | 0 | 308 | 107 | 139844 |
| Q1 | 08-14 | 50 | 2 | 94 | 1794 | 100 | 34 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 97810 |
| Q2 | 08-26 | 50 | 3 | 58 | 1367 | 54 | 54 | 14 | 9 | 4 | 0 | 37 | 143 | 19 | 0 | 0 | 285 | 72 | 91772 |
| Q3 | 09-05 | 50 | 2 | 80 | 2678 | 100 | 18 | 12 | 9 | 5 | 0 | 33 | 188 | 12 | 5 | 0 | 381 | 96 | 100182 |
| L | 09-14 | 50 | 2 | 56 | 2933 | 52 | 100 | 13 | 9 | 5 | 3 | 33 | 101 | 13 | 32 | 12 | 268 | 176 | 101506 |
| C0 | 09-11 | 50 | 1 | 98 | 2207 | 2 | 100 | 13 | 9 | 5 | 3 | 33 | 115 | 13 | 37 | 4.50 | 281 | 189 | 104204 |

**HowardLeeTW** (rank 13)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-08 | 50 | 1 | 76 | 1501 | 100 | 14 | 14 | 8 | 6 | 0 | 42 | 92 | 23 | 0 | 0 | 322 | 80 | 80186 |
| Q1 | 08-18 | 50 | 2 | 30 | 1940 | 60 | 34 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 80973 |
| Q2 | 08-30 | 50 | 2 | 28 | 1295 | 54 | 34 | 12 | 8 | 5 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 79810 |
| Q3 | 09-07 | 38 | 1 | 95 | 2831 | 8 | 100 | 12 | 7.50 | 4.50 | 2 | 31 | 143 | 13 | 37 | 7.50 | 288 | 176 | 109334 |
| L | 09-14 | 50 | 2 | 60 | 2528 | 26 | 100 | 12 | 6 | 4 | 2 | 37 | 118 | 13 | 34 | 8 | 241 | 184 | 102454 |
| C0 | 09-13 | 50 | 1 | 90 | 2178 | 24 | 100 | 12 | 7 | 4.50 | 1 | 31 | 132 | 13 | 39 | 8 | 247 | 192 | 108796 |

**Catalyst** (rank 14)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-12 | 50 | 2 | 96 | 1718 | 94 | 24 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 417 | 99.50 | 105854 |
| Q1 | 09-12 | 50 | 2 | 88 | 2235 | 100 | 24 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 399 | 101 | 98466 |
| Q2 | 09-13 | 50 | 2 | 58 | 2890 | 98 | 36 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 388 | 106 | 102791 |
| Q3 | 09-14 | 50 | 2 | 90 | 2532 | 86 | 64 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 389 | 119 | 100971 |
| L | 09-14 | 50 | 2 | 58 | 2956 | 78 | 76 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 388 | 116 | 101564 |
| C0 | 09-14 | 50 | 1 | 94 | 2196 | 86 | 72 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 389 | 121 | 102170 |

**feel the agi** (rank 15)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-04 | 50 | 2 | 86 | 1672 | 100 | 18 | 12 | 9 | 9 | 0 | 33 | 195 | 12 | 9 | 0 | 384 | 75 | 91116 |
| Q1 | 09-06 | 50 | 1 | 80 | 2533 | 100 | 64 | 12 | 10 | 4.50 | 3 | 33 | 189 | 12 | 9 | 0 | 380 | 75 | 98714 |
| Q2 | 09-09 | 50 | 2 | 68 | 2051 | 98 | 98 | 12 | 7.50 | 4 | 3 | 33 | 128 | 12 | 9 | 0 | 399 | 140 | 99645 |
| Q3 | 09-11 | 2 | 1 | 50 | 3087 | 100 | 100 | 13 | 7.50 | 21 | 2 | 25.50 | 163 | 12 | 9.50 | 0 | 516 | 142 | 137192 |
| L | 09-14 | 50 | 2 | 70 | 2854 | 100 | 100 | 12 | 6 | 3.50 | 6 | 28.50 | 160 | 12 | 10.50 | 0 | 366 | 164 | 102100 |
| C0 | 09-10 | 50 | 1 | 90 | 2144 | 100 | 98 | 13 | 7 | 3 | 5 | 29 | 148 | 12 | 0 | 0 | 394 | 163 | 117751 |

**アルモンド** (rank 22)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-01 | 50 | 1 | 64 | 1728 | 90 | 18 | 12 | 11 | 4 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 89460 |
| Q1 | 09-07 | 50 | 3 | 62 | 1469 | 88 | 40 | 12 | 8.50 | 5 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 89760 |
| Q2 | 09-09 | 50 | 3 | 82 | 1501 | 78 | 34 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 417 | 61 | 98475 |
| L | 09-14 | 50 | 2 | 68 | 2896 | 86 | 100 | 12 | 8 | 6 | 3 | 33 | 135 | 15 | 46 | 0 | 410 | 143 | 98458 |
| C0 | 09-14 | 50 | 1 | 92 | 2200 | 90 | 98 | 12 | 8 | 6 | 3 | 33 | 128 | 15 | 52 | 0 | 410 | 144 | 100353 |

**Otter Vibe** (rank 25)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-27 | 50 | 1 | 64 | 1101 | 94 | 100 | 15 | 9 | 8 | 4 | 40 | 153 | 24 | 10 | 0 | 318 | 76 | 98829 |
| Q1 | 09-02 | 50 | 2 | 72 | 1425 | 86 | 100 | 13 | 8 | 2 | 0 | 31 | 168 | 11 | 2 | 0 | 268 | 62 | 108394 |
| Q2 | 09-09 | 50 | 2 | 58 | 2478 | 48 | 100 | 14 | 7 | 7 | 7 | 27.50 | 102 | 15 | 31 | 15.50 | 385 | 190 | 106307 |
| Q3 | 09-11 | 26 | 1 | 50 | 3004 | 65 | 100 | 15 | 8 | 6 | 5 | 27 | 108 | 16 | 33 | 14 | 378 | 185 | 104153 |
| L | 09-14 | 50 | 1 | 58 | 2950 | 36 | 100 | 14.50 | 7 | 6.50 | 6 | 23.50 | 104 | 15 | 29 | 20.50 | 368 | 188 | 100312 |
| C0 | 09-08 | 50 | 1 | 98 | 2156 | 50 | 100 | 15 | 7 | 7 | 6 | 23 | 104 | 16 | 30.50 | 17.50 | 360 | 194 | 106756 |

**kyy666** (rank 28)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-09 | 50 | 1 | 54 | 1387 | 56 | 100 | 12 | 7 | 6 | 0 | 39.50 | 106 | 20 | 27.50 | 5.50 | 367 | 111 | 100074 |
| L | 09-14 | 50 | 2 | 60 | 2880 | 62 | 84 | 12 | 6 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 403 | 110 | 93802 |
| C0 | 09-14 | 50 | 1 | 94 | 2173 | 100 | 72 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 397 | 116 | 109058 |

**𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔** (rank 29)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-02 | 50 | 1 | 42 | 618 | 32 | 98 | 11 | 13 | 8 | 0 | 39.50 | 145 | 12 | 163 | 0 | 236 | 93 | 66872 |
| Q3 | 09-14 | 3 | 1 | 0 | 2948 | 67 | 100 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 405 | 119 | 84694 |
| L | 09-14 | 50 | 2 | 54 | 2909 | 100 | 72 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 405 | 113 | 102716 |
| C0 | 09-14 | 50 | 1 | 96 | 2246 | 100 | 68 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 405 | 110 | 103297 |

**redblackbst** (rank 31)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-26 | 50 | 1 | 82 | 1125 | 88 | 54 | 15 | 11 | 4 | 0 | 41 | 132 | 11 | 20 | 0 | 343 | 80 | 83125 |
| Q1 | 09-03 | 50 | 2 | 36 | 1885 | 88 | 16 | 12 | 9 | 5 | 0 | 38 | 187 | 12 | 6 | 0 | 333 | 62 | 77714 |
| Q2 | 09-08 | 50 | 1 | 44 | 1942 | 100 | 22 | 12 | 9 | 7 | 2 | 33 | 195 | 12 | 9 | 0 | 376 | 75 | 80478 |
| Q3 | 09-11 | 5 | 2 | 60 | 3006 | 100 | 100 | 11 | 8 | 2 | 0 | 33 | 163 | 12 | 38 | 0 | 357 | 77 | 93761 |
| L | 09-14 | 50 | 1 | 64 | 2948 | 68 | 100 | 11 | 7 | 4 | 4.50 | 32 | 162 | 13 | 42 | 1 | 334 | 87.50 | 106054 |
| C0 | 09-14 | 50 | 1 | 92 | 2227 | 94 | 98 | 12 | 7 | 5 | 2 | 32 | 162 | 13 | 44 | 1 | 344 | 86.50 | 101342 |

**Kilupy** (rank 32)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-03 | 50 | 1 | 50 | 822 | 48 | 100 | 12 | 5 | 8 | 0 | 39 | 107 | 15 | 11 | 1 | 470 | 76 | 79794 |
| L | 09-14 | 50 | 2 | 58 | 2872 | 94 | 76 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 405 | 106 | 94846 |
| C0 | 09-14 | 50 | 1 | 90 | 2319 | 96 | 76 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 405 | 110 | 101670 |

**Kaggriculture Agent** (rank 35)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 07-31 | 50 | 2 | 56 | 952 | 78 | 72 | 10 | 12 | 0 | 0 | 0.50 | 8.50 | 14 | 0 | 0 | 240 | 0 | 68558 |
| L | 09-14 | 50 | 2 | 80 | 2690 | 50 | 74 | 12 | 7.50 | 5 | 4 | 33 | 153 | 12 | 41 | 0 | 406 | 117 | 95476 |
| C0 | 09-14 | 50 | 1 | 90 | 2251 | 46 | 54 | 12 | 8 | 6 | 3 | 33 | 158 | 12 | 36 | 0 | 408 | 116 | 99096 |

**Zhenghongshuang** (rank 36)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-15 | 50 | 1 | 90 | 1549 | 100 | 24 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 89718 |
| L | 09-14 | 50 | 2 | 54 | 2537 | 98 | 64 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 400 | 81 | 99818 |
| C0 | 09-14 | 50 | 1 | 96 | 2153 | 98 | 66 | 12 | 8 | 6 | 3 | 33 | 156 | 12 | 38 | 0 | 356 | 113 | 100892 |

**elmo** (rank 38)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-04 | 50 | 1 | 88 | 1496 | 88 | 20 | 12 | 8 | 9 | 0 | 34 | 194 | 12 | 9 | 0 | 373 | 75 | 93357 |
| L | 09-14 | 50 | 2 | 70 | 2838 | 90 | 68 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 405 | 116 | 91042 |
| C0 | 09-14 | 50 | 1 | 92 | 2185 | 96 | 68 | 12 | 7 | 6 | 3 | 33 | 158 | 12 | 35 | 0 | 405 | 112 | 106008 |

**Thomas Tschinkel** (rank 41)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-13 | 50 | 1 | 86 | 1754 | 100 | 28 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 94520 |
| Q1 | 08-24 | 50 | 2 | 76 | 1747 | 50 | 52 | 15 | 11 | 4 | 0 | 39.50 | 134 | 11 | 19.50 | 0 | 343 | 80 | 81245 |
| Q2 | 09-03 | 50 | 3 | 62 | 2022 | 46 | 100 | 12 | 7 | 4 | 0 | 33 | 124 | 11 | 15 | 3.50 | 278 | 136 | 99503 |
| L | 09-14 | 50 | 2 | 68 | 2815 | 100 | 86 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 417 | 114 | 97730 |
| C0 | 09-14 | 50 | 1 | 90 | 2239 | 100 | 70 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 405 | 121 | 93960 |

**mtmr_s1** (rank 45)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-22 | 50 | 1 | 54 | 1448 | 98 | 40 | 12 | 9 | 3 | 0 | 36 | 148 | 11 | 0 | 0 | 246 | 72 | 97769 |
| Q3 | 09-10 | 10 | 1 | 20 | 2954 | 100 | 20 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 417 | 61 | 104898 |
| L | 09-14 | 50 | 2 | 68 | 2870 | 100 | 88 | 13 | 9 | 6 | 3 | 33 | 155 | 12 | 42.50 | 0 | 405 | 122 | 105096 |
| C0 | 09-14 | 50 | 1 | 94 | 2157 | 100 | 100 | 12 | 8 | 6 | 3 | 33 | 148 | 12 | 50 | 0 | 398 | 128 | 101994 |

**Emile Andrieu** (rank 46)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-03 | 50 | 1 | 68 | 1712 | 100 | 12 | 12 | 8 | 6 | 0 | 44 | 66 | 21 | 0 | 0 | 308 | 107 | 118749 |
| Q1 | 08-15 | 25 | 1 | 36 | 3011 | 100 | 28 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 94274 |
| L | 09-14 | 50 | 2 | 64 | 2803 | 98 | 94 | 12 | 8 | 6 | 3 | 33 | 156 | 12 | 38 | 0 | 424 | 110 | 93072 |
| C0 | 09-14 | 50 | 1 | 86 | 2204 | 98 | 84 | 12 | 8 | 6 | 3 | 33 | 166 | 12 | 28 | 0 | 440 | 114 | 102305 |

**THUNDER THUNDER** (rank 49)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 07-30 | 50 | 2 | 48 | 811 | 46 | 100 | 10 | 0 | 0 | 0 | 5 | 82 | 18 | 84.50 | 17.50 | 0 | 0 | 38584 |
| Q3 | 09-08 | 6 | 1 | 0 | 2871 | 100 | 100 | 12 | 10 | 8 | 2 | 33 | 118 | 13 | 48 | 4 | 336 | 164 | 75254 |
| L | 09-14 | 50 | 2 | 60 | 2798 | 86 | 100 | 12 | 8 | 8 | 2 | 34 | 130 | 13 | 50.50 | 4.50 | 289 | 178 | 106105 |
| C0 | 09-11 | 50 | 1 | 90 | 2011 | 88 | 100 | 12 | 9 | 3 | 2 | 33 | 145 | 13 | 21 | 5 | 302 | 182 | 101158 |

**doubao** (rank 72)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-09 | 50 | 2 | 86 | 1660 | 98 | 8 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 417 | 61 | 95556 |
| Q3 | 09-13 | 9 | 1 | 100 | 1046 | 100 | 100 | 12 | 6 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 400 | 109 | 86756 |
| L | 09-14 | 50 | 2 | 40 | 2701 | 50 | 86 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 414 | 108 | 101211 |
| C0 | 09-13 | 50 | 1 | 88 | 2074 | 98 | 76 | 12 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 400 | 124 | 110695 |

**yomogii** (rank 74)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 09-05 | 50 | 2 | 62 | 916 | 42 | 76 | 13 | 7.50 | 9 | 0 | 33 | 142 | 12 | 13 | 0 | 312 | 142 | 82039 |
| L | 09-14 | 50 | 2 | 74 | 2817 | 90 | 76 | 11 | 8 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 403 | 108 | 98686 |
| C0 | 09-14 | 50 | 1 | 94 | 2135 | 76 | 82 | 12 | 6.50 | 6 | 3 | 33 | 163 | 12 | 31 | 0 | 403 | 108 | 102744 |

**Tom&Jerry** (rank 75)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-26 | 50 | 1 | 86 | 1435 | 94 | 44 | 15 | 11 | 4 | 0 | 41 | 134 | 11 | 20 | 0 | 343 | 80 | 90280 |
| L | 09-14 | 50 | 2 | 62 | 2837 | 94 | 72 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 405 | 117 | 90408 |
| C0 | 09-14 | 50 | 1 | 92 | 2204 | 96 | 74 | 12 | 6 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 405 | 110 | 106862 |

**ElephtAI** (rank 227)

| window | from | games | subs | win | opp rating | modal line share @day4 | distinct @day16 | hands | cows | sheep | geese | strawberry | wheat | melon | carrot | tomato | care | fertilize | bank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F | 08-27 | 50 | 2 | 74 | 1338 | 86 | 42 | 12 | 10 | 4 | 0 | 34 | 127 | 20 | 6 | 0 | 318 | 64 | 95660 |
| L | 09-14 | 50 | 2 | 64 | 2891 | 92 | 62 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 417 | 105 | 99438 |
| C0 | 09-14 | 50 | 1 | 96 | 2282 | 94 | 70 | 12 | 8 | 6 | 3 | 33 | 162 | 12 | 31 | 0 | 417 | 103 | 99152 |

What the windows say, team by team: the leaders' current farms are recognisable in their
first windows (Artem's fixed five-day opening and 13 hands from 08-19; Majkel1337's 11 hands,
8 cows and 13-14 melon from 08-28; Otter Vibe's geese and tomatoes from 08-27), and what
changed between the early windows and now is wheat (from 8-140 to 140-190 plantings),
carrots and tomatoes (from none to 30-50 and 8-10), fertilizer (from 50-80 to 150-190 ops),
and geese. The family teams' windows show the public generations of section 4 one after
another (Zhenghongshuang, Thomas Tschinkel, ElephtAI and Emile Andrieu's first windows are
the 08-13 line; アルモンド's and redblackbst's the 09-01 line; every family C0 the 09-09
line). The "tape to runtime" story of the memo is therefore two different stories: the
leaders were runtime agents from their first window and improved their economy; the family
teams replaced one public line with the next.

## 6. Who beats whom at the top

Current submissions on both sides, teams ranked 1-15 at the full snapshot (W-L, row beats column):

| row beats column | Artem The  | Majkel1337 | Unknown Mo | DSM | SpaTaro | THIRD FARM | Orbital Te | Sida Zuo | ymg_aq | leave you | 现实是个乐子 | Mengfei Li | HowardLeeT | Catalyst | feel the a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Artem The Farm |  | 19-11 | 7-4 | 1-0 |  | 2-0 | 3-1 |  | 2-3 | 0-1 |  | 2-1 | 2-0 | 1-0 | 2-0 |
| Majkel1337 | 11-18 |  | 4-4 | 4-0 | 10-0 |  | 5-0 |  | 3-1 |  |  | 21-2 | 3-0 |  | 14-2 |
| Unknown Mother | 4-7 | 4-4 |  | 3-2 | 4-0 | 2-0 | 4-0 |  | 1-4 | 2-0 |  | 4-1 | 3-0 | 0-1 | 1-0 |
| DSM | 0-1 | 0-4 | 2-3 |  | 2-0 |  | 3-1 |  | 2-0 | 1-0 |  | 3-0 | 2-0 | 1-0 |  |
| SpaTaro |  | 0-10 | 0-4 | 0-2 |  | 2-2 | 0-1 |  | 2-3 | 1-1 |  | 8-3 | 6-0 | 3-1 | 4-1 |
| THIRD FARM CLU | 0-2 |  | 0-2 |  | 2-2 |  | 0-1 |  |  | 2-0 |  | 1-1 | 2-0 | 2-0 | 0-2 |
| Orbital Terraf | 1-3 | 0-5 | 0-4 | 1-3 | 1-0 | 1-0 |  |  | 1-0 | 0-3 |  | 3-4 | 4-3 | 1-2 | 5-0 |
| Sida Zuo |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ymg_aq | 3-2 | 1-3 | 4-1 | 0-2 | 3-2 |  | 0-1 |  |  |  |  | 12-3 | 2-3 |  | 6-0 |
| leave you | 1-0 |  | 0-2 | 0-1 | 1-1 | 0-2 | 3-0 |  |  |  |  | 0-2 | 3-3 | 2-2 | 1-0 |
| 现实是个乐子 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Mengfei Li | 1-2 | 2-21 | 1-4 | 0-3 | 3-8 | 1-1 | 4-3 |  | 3-12 | 2-0 |  |  | 2-0 | 1-1 | 2-7 |
| HowardLeeTW | 0-2 | 0-3 | 0-3 | 0-2 | 0-6 | 0-2 | 3-4 |  | 3-2 | 3-3 |  | 0-2 |  | 3-1 | 3-3 |
| Catalyst | 0-1 |  | 1-0 | 0-1 | 1-3 | 0-2 | 2-1 |  |  | 2-2 |  | 1-1 | 1-3 |  | 1-2 |
| feel the agi | 0-2 | 2-14 | 0-1 |  | 1-4 | 2-0 | 0-5 |  | 0-6 | 0-1 |  | 7-2 | 3-3 | 2-1 |  |

All public games between the same teams, any submission:

| row beats column | Artem The  | Majkel1337 | Unknown Mo | DSM | SpaTaro | THIRD FARM | Orbital Te | Sida Zuo | ymg_aq | leave you | 现实是个乐子 | Mengfei Li | HowardLeeT | Catalyst | feel the a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Artem The Farm |  | 58-54 | 28-16 | 6-2 | 24-10 | 12-8 | 18-5 | 0-1 | 21-19 | 3-3 | 3-3 | 16-6 | 6-2 | 7-0 | 15-8 |
| Majkel1337 | 54-57 |  | 36-25 | 19-1 | 87-9 | 12-2 | 15-0 | 1-0 | 106-13 | 0-1 | 1-0 | 42-12 | 3-0 | 3-1 | 35-9 |
| Unknown Mother | 16-28 | 25-36 |  | 9-5 | 34-25 | 14-17 | 16-3 | 0-1 | 12-54 | 7-1 | 2-5 | 22-8 | 6-0 | 7-3 | 40-5 |
| DSM | 2-6 | 1-19 | 5-9 |  | 9-5 | 10-11 | 14-4 | 2-2 | 18-8 | 6-11 | 8-3 | 12-7 | 6-2 | 9-1 | 5-1 |
| SpaTaro | 10-24 | 9-87 | 25-34 | 5-9 |  | 10-10 | 11-8 | 4-0 | 49-52 | 7-1 | 16-18 | 45-41 | 9-5 | 11-2 | 58-34 |
| THIRD FARM CLU | 8-12 | 2-12 | 17-14 | 11-10 | 10-10 |  | 2-11 | 3-2 | 17-7 | 4-2 | 9-4 | 16-15 | 4-0 | 12-2 | 33-20 |
| Orbital Terraf | 5-18 | 0-15 | 3-16 | 4-14 | 8-11 | 11-2 |  | 3-3 | 15-8 | 4-6 | 1-0 | 7-5 | 5-6 | 6-6 | 11-4 |
| Sida Zuo | 1-0 | 0-1 | 1-0 | 2-2 | 0-4 | 2-3 | 3-3 |  |  | 5-6 | 0-5 | 1-2 | 2-1 | 1-6 | 0-1 |
| ymg_aq | 19-21 | 13-106 | 54-12 | 8-18 | 52-49 | 7-17 | 8-15 |  |  | 4-2 | 21-10 | 52-42 | 5-24 | 25-1 | 58-22 |
| leave you | 3-3 | 1-0 | 1-7 | 11-6 | 1-7 | 2-4 | 6-4 | 6-5 | 2-4 |  | 5-16 | 4-11 | 5-3 | 3-4 | 4-4 |
| 现实是个乐子 | 3-3 | 0-1 | 5-2 | 3-8 | 18-16 | 4-9 | 0-1 | 5-0 | 10-21 | 16-5 |  | 13-19 | 5-8 | 4-6 | 7-6 |
| Mengfei Li | 6-16 | 12-42 | 8-22 | 7-12 | 41-45 | 15-16 | 5-7 | 2-1 | 42-52 | 11-4 | 19-13 |  | 14-47 | 8-10 | 9-34 |
| HowardLeeTW | 2-6 | 0-3 | 0-6 | 2-6 | 5-9 | 0-4 | 6-5 | 1-2 | 24-5 | 3-5 | 8-5 | 65-22 |  | 4-3 | 5-4 |
| Catalyst | 0-7 | 1-3 | 3-7 | 1-9 | 2-11 | 2-12 | 6-6 | 6-1 | 1-25 | 4-3 | 6-4 | 10-8 | 3-4 |  | 1-10 |
| feel the agi | 8-15 | 9-35 | 5-40 | 1-5 | 34-58 | 20-33 | 4-11 | 1-0 | 22-58 | 4-4 | 6-7 | 34-9 | 4-5 | 10-1 |  |

Artem The Farmer beats Majkel1337 19-11 on current submissions (58-54 all-time); Majkel1337
beats everyone else by wide margins (21-2 Mengfei Li, 14-2 feel the agi, 10-0 SpaTaro, 5-0
Orbital Terraformer, 4-0 DSM) and is level with Unknown Mother-Goose (4-4). Of 643
current-submission games among these teams the median bank margin is 4113, a quarter
are within 1883. There is no seat effect: seat 0 wins 60.9% and seat 1 60.8%
of the studied teams' 309,306 games.

## 7. The market, measured correctly

Every number here comes from the rebuilt traces (P18): executed units and revenue per sale as
the engine computed them, checked against the recorded money in every turn of every game.
Seats where that check fails are excluded from every sales column before any median is taken
(`research/features.py`): 410 of 14788 seat rows in the whole sample, of which
8 are current-submission rows (final-step
mismatches of at most $466, see P18); the rest are historical windows played on engine
versions 1.32.2-1.32.6, whose market this replica does not model (Emile Andrieu's,
Thomas Tschinkel's and THUNDER THUNDER's first-50 windows and Mengfei Li's first quarter
window in full). Medians of per-team medians by group, with the chance that a random top-14
team is above a random gold team:

| median of per-team medians | top-14 | gold | silver | bronze | P(top-14 > gold) | P(gold > silver) |
|---|---|---|---|---|---|---|
| teams | 14 | 14 | 21 | 10 |  |  |
| final_money | 104086 | 104942 | 101994 | 105365 | 0.42 (p=0.46) | 0.73 (p=0.02) |
| revenue_total | 133117 | 134650 | 136489 | 135617 | 0.39 (p=0.33) | 0.48 (p=0.87) |
| revenue_premium | 86035 | 88467 | 86390 | 92414 | 0.36 (p=0.21) | 0.57 (p=0.48) |
| revenue_staple | 43656 | 41642 | 41587 | 40095 | 0.64 (p=0.20) | 0.55 (p=0.59) |
| revenue_last_3_days | 21624 | 21134 | 21345 | 21454 | 0.52 (p=0.85) | 0.53 (p=0.79) |
| last3_share_pct | 16.33 | 15.98 | 15.70 | 16.05 | 0.56 (p=0.61) | 0.65 (p=0.13) |
| hire_spend | 4929 | 4605 | 4496 | 4663 | 0.65 (p=0.17) | 0.65 (p=0.15) |
| sold_melon | 75 | 72 | 72 | 72 | 0.64 (p=0.18) | 0.52 (p=0.76) |
| price_melon | 185 | 198 | 198 | 198 | 0.30 (p=0.06) | 0.38 (p=0.12) |
| sold_strawberry | 222 | 248 | 249 | 248 | 0.25 (p=0.02) | 0.40 (p=0.29) |
| price_strawberry | 125 | 116 | 113 | 118 | 0.69 (p=0.08) | 0.58 (p=0.42) |
| sold_milk | 182 | 191 | 192 | 205 | 0.35 (p=0.19) | 0.31 (p=0.06) |
| price_milk | 92.43 | 84.13 | 80.23 | 85.49 | 0.63 (p=0.25) | 0.59 (p=0.38) |
| sold_wool | 113 | 126 | 130 | 138 | 0.44 (p=0.57) | 0.39 (p=0.26) |
| price_wool | 117 | 105 | 99.34 | 111 | 0.71 (p=0.05) | 0.58 (p=0.42) |
| sold_egg | 77 | 83.50 | 82 | 72.50 | 0.36 (p=0.21) | 0.61 (p=0.28) |
| sold_wheat | 434 | 382 | 394 | 375 | 0.68 (p=0.10) | 0.39 (p=0.28) |
| price_wheat | 38.84 | 39.37 | 39.14 | 39.26 | 0.34 (p=0.15) | 0.51 (p=0.95) |
| sold_carrot | 96.75 | 91.50 | 94 | 88 | 0.64 (p=0.21) | 0.39 (p=0.28) |
| sold_tomato | 39 | 0 | 0 | 0 | 0.61 (p=0.31) | 0.70 (p=0.01) |
| sold_fertilizer | 218 | 342 | 342 | 352 | 0.19 (p=0.01) | 0.45 (p=0.64) |
| premium_cheap_pct | 28.28 | 34.28 | 35.13 | 33.27 | 0.36 (p=0.20) | 0.34 (p=0.11) |

Per team, ranks 1-31:

| rank | team | group | final_money | revenue_premium | revenue_staple | revenue_last_3_days | sold_melon | price_melon | sold_strawberry | price_strawberry | sold_milk | price_milk | sold_wool | price_wool | sold_egg | sold_carrot | sold_tomato | premium_cheap_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 101286 | 82766 | 43294 | 21292 | 78 | 186 | 196 | 123 | 190 | 80.70 | 123 | 98.31 | 63 | 98.50 | 65.50 | 32.85 |
| 2 | Majkel1337 | top-14 | 113359 | 95073 | 43052 | 24261 | 72 | 184 | 218 | 169 | 180 | 99.97 | 109 | 132 | 74 | 92 | 47 | 20.74 |
| 3 | Unknown Mother-Goose | gold | 117671 | 95461 | 45640 | 23931 | 83 | 189 | 204 | 125 | 178 | 108 | 150 | 136 | 112 | 81.50 | 57.50 | 22.56 |
| 4 | DSM | top-14 | 104556 | 85110 | 45298 | 21363 | 72 | 179 | 226 | 130 | 188 | 93.34 | 106 | 130 | 80 | 102 | 52 | 24.07 |
| 5 | SpaTaro | top-14 | 96835 | 80338 | 45530 | 14772 | 60 | 203 | 183 | 143 | 170 | 91.51 | 124 | 138 | 0 | 152 | 0 | 24.41 |
| 6 | THIRD FARM CLUB | gold | 115275 | 88793 | 48527 | 30915 | 86.50 | 168 | 208 | 149 | 174 | 93.31 | 65 | 130 | 168 | 148 | 69.50 | 26.14 |
| 7 | Orbital Terraformer | top-14 | 103874 | 87353 | 42824 | 18613 | 72 | 178 | 214 | 130 | 170 | 94.95 | 102 | 116 | 62 | 76 | 34 | 29.79 |
| 8 | Sida Zuo | gold | 106280 | 79050 | 47123 | 18618 | 48 | 219 | 207 | 132 | 167 | 83.80 | 82 | 104 | 149 | 201 | 88 | 26.01 |
| 9 | ymg_aq | top-14 | 105855 | 86548 | 71000 | 23872 | 84 | 165 | 237 | 118 | 189 | 94.33 | 87 | 114 | 0 | 93 | 44 | 29.66 |
| 10 | leave you | gold | 101830 | 82984 | 39995 | 19495 | 72 | 198 | 249 | 114 | 213 | 84.46 | 103 | 80.01 | 77 | 89 | 0 | 36.38 |
| 12 | Mengfei Li | top-14 | 104299 | 85771 | 45738 | 21720 | 78 | 191 | 215 | 128 | 167 | 82.15 | 98 | 108 | 99 | 90 | 48 | 25.98 |
| 13 | HowardLeeTW | top-14 | 107917 | 90768 | 41469 | 21940 | 78 | 162 | 244 | 125 | 171 | 103 | 88 | 130 | 34 | 128 | 63 | 25.68 |
| 14 | Catalyst | top-14 | 102193 | 87900 | 43186 | 21528 | 72 | 203 | 249 | 120 | 201 | 78.37 | 141 | 109 | 74 | 95 | 0 | 37.06 |
| 15 | feel the agi | top-14 | 112062 | 88539 | 54124 | 25616 | 72 | 196 | 217 | 137 | 184 | 78.62 | 86.50 | 118 | 171 | 24.50 | 0 | 26.90 |
| 16 | local | gold | 105971 | 87103 | 40731 | 19981 | 72 | 198 | 247 | 117 | 191 | 79.33 | 126 | 77.16 | 86 | 93.50 | 0 | 35.97 |
| 17 | lumen | gold | 102415 | 84887 | 43514 | 21618 | 72 | 198 | 250 | 95.07 | 191 | 69.62 | 126 | 112 | 87 | 91 | 0 | 34.68 |
| 19 | carbonapi | gold | 103912 | 91771 | 47456 | 22107 | 72 | 198 | 249 | 133 | 199 | 88.30 | 142 | 82.08 | 74 | 123 | 0 | 33.38 |
| 20 | Cow Boy | gold | 100465 | 89566 | 41032 | 20889 | 72 | 198 | 251 | 114 | 203 | 81.32 | 139 | 105 | 78 | 91 | 0 | 36.59 |
| 21 | Ebi | gold | 106031 | 92191 | 238857 | 56314 | 84 | 160 | 248 | 121 | 182 | 91.97 | 96 | 102 | 134 | 72 | 28 | 28.94 |
| 22 | アルモンド | top-14 | 101116 | 85390 | 43170 | 21448 | 90 | 174 | 250 | 124 | 226 | 68.40 | 143 | 88.19 | 89 | 140 | 0 | 39.20 |
| 23 | AI是我的豆包 | gold | 107738 | 81174 | 42253 | 25018 | 71 | 187 | 256 | 107 | 160 | 85.95 | 98 | 108 | 80 | 57.50 | 47.50 | 25.29 |
| 24 | fog flower | gold | 109250 | 90234 | 40796 | 21379 | 72 | 198 | 249 | 109 | 203 | 65 | 106 | 80.57 | 78 | 94 | 0 | 33.91 |
| 25 | Otter Vibe | top-14 | 104610 | 82920 | 58357 | 23716 | 90 | 152 | 185 | 125 | 166 | 104 | 132 | 128 | 230 | 101 | 134 | 25.76 |
| 26 | nilochan | gold | 100990 | 87160 | 40882 | 20154 | 72 | 198 | 249 | 103 | 191 | 82.49 | 136 | 107 | 81 | 93.50 | 0 | 36.46 |
| 27 | yjshyfy | gold | 101704 | 88969 | 40038 | 19828 | 72 | 198 | 246 | 116 | 191 | 63.58 | 130 | 91.44 | 78 | 88 | 4 | 36.66 |
| 28 | kyy666 | gold | 103610 | 88140 | 40350 | 19805 | 72 | 198 | 248 | 120 | 191 | 85.98 | 139 | 115 | 87 | 92 | 0 | 34.65 |
| 29 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | silver | 103297 | 92352 | 42956 | 21070 | 72 | 203 | 250 | 96.31 | 203 | 93.81 | 123 | 87.68 | 82 | 94 | 0 | 33.04 |
| 31 | redblackbst | top-14 | 102460 | 86298 | 44018 | 23218 | 78 | 196 | 235 | 110 | 172 | 93.38 | 117 | 121 | 99 | 122 | 6 | 30.88 |

![units sold per day](figs/an_sales_by_day.png)

Median units sold per day by group (solid), with Majkel1337 (dashed) and Artem The Farmer
(dotted). Revenue conditional on the shops unlocked by day 9 (medians, "with / without"):

| who | games | wool revenue: Yarn Store early / not | milk revenue: milk shop early / not | egg revenue: egg shop early / not | carrot revenue: carrot shop early / not | bank: Yarn Store early / not |
|---|---|---|---|---|---|---|
| top-14 | 1293 | 37,320 / 6,561 | 21,740 / 5,378 | 4,961 / 2,815 | 7,616 / 2,836 | 110,000 / 101,527 |
| gold | 854 | 41,976 / 6,396 | 22,806 / 5,320 | 4,847 / 3,422 | 6,392 / 2,987 | 111,145 / 102,866 |
| silver | 1368 | 37,419 / 6,495 | 21,318 / 5,970 | 4,538 / 3,655 | 5,888 / 3,318 | 110,226 / 98,954 |
| bronze | 505 | 38,004 / 6,346 | 25,761 / 6,212 | 4,135 / 3,453 | 5,468 / 3,262 | 114,292 / 103,527 |
| #1 Artem The Farmer 🍅 | 88 | 31,493 / 6,396 | 19,025 / 6,723 | 3,980 / 1,948 | 8,172 / 1,798 | 105,559 / 98,992 |
| #2 Majkel1337 | 103 | 40,649 / 9,084 | 22,982 / 4,788 | 4,572 / 0 | 7,723 / 877 | 122,248 / 112,076 |
| #3 Unknown Mother-Goose | 82 | 39,518 / 8,986 | 23,634 / 6,078 | 8,213 / 1,614 | 7,830 / 1,956 | 127,244 / 114,726 |
| #4 DSM | 82 | 46,477 / 6,763 | 25,825 / 4,711 | 4,447 / 0 | 7,103 / 2,828 | 109,241 / 104,515 |
| #5 SpaTaro | 93 | 37,696 / 6,287 | 23,129 / 5,394 | 0 / 0 | 10,680 / 378 | 105,550 / 93,166 |
| #6 THIRD FARM CLUB | 55 | 30,580 / 6,265 | 20,163 / 4,474 | 10,762 / 6,630 | 10,345 / 2,447 | 132,220 / 107,211 |
| #7 Orbital Terraformer | 79 | 35,071 / 8,285 | 21,544 / 7,114 | 4,309 / 0 | 7,127 / 1,759 | 110,808 / 100,361 |
| #8 Sida Zuo | 51 | 46,326 / 5,886 | 16,400 / 5,188 | 10,437 / 3,584 | 11,767 / 0 | 111,745 / 104,890 |
| #9 ymg_aq | 77 | 37,902 / 7,390 | 23,300 / 5,060 | 1,764 / 0 | 10,583 / 1,574 | 105,050 / 105,855 |
| #10 leave you | 85 | 34,961 / 6,015 | 25,706 / 5,384 | 4,302 / 0 | 6,372 / 3,261 | 104,710 / 99,935 |

**What the corrected numbers say.** The zones do not differ in what they sell or in what
they bank: total revenue is 133-136k and the final bank 102-105k in every group, and the
top-14 sell *fewer* premium units than the family (strawberry 222 against 248, milk 182
against 191, wool 113 against 126, melon 75 against 72) at higher prices (strawberry $125
against $116, milk $93 against $84, wool $117 against $105). The family sells 342 fertilizer
a game against the leaders' 218, because the leaders spread it on the fields. Every earlier
"the #1 sells four times the melon" statement was the P18 undercount. The leaders' edge is
relative, and section 9b shows where it comes from; the per-day tables behind the figure
(mean units and revenue per day, computed from `market.parquet`) give the mechanism:

- **The public line's clock is fixed.** Melon: 60 units on day 10 and the last 12 on day 11.
  No shop demands melon, so the town removes one a day and a 72-melon dump takes the price
  from $250 to about $200 (the glut curve is quadratic, 3.6 times base over 300 units); two
  farms dumping in the same hours take it near the floor. Strawberries: days 15-29 with the
  bulk on days 20-24 at 20-29 a day, sold late in the day (hours 13 and 19-23) in orders of
  six. Milk about 10 a day from day 8; wool 8-16 every third day from day 6; wheat rising
  to 61 on day 29; fertilizer 10-20 a day all season.
- **The town's drain sets the price-holding rate.** Median units removed per day across the
  sampled games: strawberry 7 before the shops accumulate and 22-36 from day 18; milk 14;
  wool 12; carrot 13; egg 7; tomato 7; wheat 32; melon 1. Strawberry's price falls by 1.6
  times base for every 100 units above the anchor and milk's by the same for every 122, so
  whoever sells faster than the drain crashes the price for both farms.
- **Out-earning = metering.** Majkel1337 sells strawberries in orders of two spread over the
  day (67 orders a game against the line's 40 of six): 18-21 a day on days 16-18 at about
  $190 like everyone, then 9-10 a day from day 20 while the line sells 20-29. It holds
  $144-170 a unit through day 28 while the line's own units fetch $67-75 on days 22-24, and
  sells its last 20 at $150 on day 29. Milk goes out in bursts of 18-19 on days 14 and 16,
  ahead of the line's day-15 burst. Result: $169 a strawberry, $100 a milk, $132 a wool on
  fewer units, and a bank of 113k against the family's 101-105k.
- **Starving = selling first and selling every day.** 29% of Artem's strawberries and 23% of
  ymg_aq's leave at hour 0, from the previous day's harvest, before the line's evening
  orders; both then sell every premium product every day to the end (Artem 10-14 milk,
  6-9 wool, 7-12 strawberries a day through day 29) so the price never recovers, and they
  replace the late premium income with staples (Artem 44k, ymg_aq 71k, of which 48k is
  1,270 wheat at $38: wheat's glut curve is logarithmic and 400 units cost $5). The line's
  late dump then meets a loaded market: its strawberry price falls to $93 against Artem and
  $77 against ymg_aq (reference $110), its milk to $70 and $69 (reference $82).
- **Melon timing is worthless.** Spreading melon (Majkel1337 29 on day 10 and a trickle to
  day 22; ymg_aq days 16-19) earns 13.9k against the dump's 14.6k, because the glut never
  clears. The "melon last sell day 20 against 11" separator in `groups.md` is real and means
  nothing for the bank.

## 8. Labour: what an action buys

Yields per animal-day and per planting, and ops per unit of work, from the corrected sales
and the day-end farm censuses. An animal-day is one animal present at one day end; a
cow yields base 1 milk every second day plus its banked CARE days, a sheep 1 wool every third
day plus CARE, a goose 1 egg a day plus CARE (all capped by `max_held`).

| median of per-team medians | top-14 | gold | silver | bronze | P(top-14 > gold) |
|---|---|---|---|---|---|
| teams | 14 | 14 | 21 | 10 |  |
| milk_per_cow_day | 1.01 | 1.04 | 1.05 | 1.08 | 0.41 (p=0.43) |
| wool_per_sheep_day | 0.98 | 0.96 | 0.96 | 1.01 | 0.60 (p=0.36) |
| egg_per_goose_day | 1.58 | 1.47 | 1.37 | 1.27 | 0.70 (p=0.07) |
| care_per_animal_day | 0.86 | 0.88 | 0.98 | 1.01 | 0.41 (p=0.42) |
| feed_per_animal_day | 0.84 | 0.80 | 0.81 | 0.81 | 0.74 (p=0.03) |
| fert_per_strawberry | 5.06 | 3.52 | 3.36 | 3.12 | 0.69 (p=0.08) |
| strawberry_per_planting | 7.43 | 7.55 | 7.55 | 7.52 | 0.31 (p=0.09) |
| wheat_per_planting | 2.79 | 2.37 | 2.43 | 2.31 | 0.74 (p=0.03) |
| melon_per_planting | 6 | 6 | 6 | 6 | 0.48 (p=0.77) |
| revenue_per_hand_day | 477 | 484 | 485 | 492 | 0.41 (p=0.43) |
| water_per_tile_day | 0.99 | 0.94 | 0.93 | 0.93 | 0.68 (p=0.10) |
| dig_ops | 36 | 35.50 | 37 | 36 | 0.45 (p=0.65) |
| pass_ops | 536 | 528 | 496 | 484 | 0.39 (p=0.33) |
| hire_spend | 4929 | 4605 | 4496 | 4663 | 0.65 (p=0.17) |

Per team, ranks 1-31:

| rank | team | group | milk_per_cow_day | wool_per_sheep_day | egg_per_goose_day | care_per_animal_day | feed_per_animal_day | fert_per_strawberry | strawberry_per_planting | wheat_per_planting | melon_per_planting | revenue_per_hand_day | water_per_tile_day | dig_ops | pass_ops | hire_spend |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | top-14 | 1.01 | 1.01 | 1.58 | 0.83 | 0.80 | 5.59 | 7.38 | 2.70 | 6 | 447 | 1.14 | 37 | 656 | 5650 |
| 2 | Majkel1337 | top-14 | 1.00 | 1.02 | 1.67 | 0.87 | 0.85 | 5.11 | 6.94 | 2.50 | 5.14 | 492 | 1.23 | 36 | 61 | 4929 |
| 3 | Unknown Mother-Goose | gold | 1.04 | 0.99 | 1.65 | 0.80 | 0.82 | 6.28 | 7.15 | 2.87 | 5.93 | 512 | 0.94 | 37 | 817 | 4769 |
| 4 | DSM | top-14 | 0.98 | 0.98 | 1.67 | 0.87 | 0.86 | 5.13 | 7.19 | 2.48 | 5.14 | 455 | 1.24 | 35 | 58 | 4929 |
| 5 | SpaTaro | top-14 | 0.96 | 0.89 |  | 0.83 | 0.82 | 3.35 | 7.12 | 3.86 | 6 | 464 | 1.07 | 24 | 920 | 3905 |
| 6 | THIRD FARM CLUB | gold | 0.92 | 0.84 | 1.57 | 0.73 | 0.80 | 5.49 | 6.42 | 2.23 | 5.82 | 523 | 1.07 | 46 | 995 | 5039 |
| 7 | Orbital Terraformer | top-14 | 1 | 0.99 | 1.62 | 0.90 | 0.88 | 5 | 7.04 | 2.54 | 5.14 | 450 | 1.26 | 35 | 69 | 4929 |
| 8 | Sida Zuo | gold | 0.97 | 1.02 | 1.69 | 0.80 | 0.81 | 5.27 | 7.81 | 2.38 | 6 | 445 | 1.03 | 40 | 711 | 4934 |
| 9 | ymg_aq | top-14 | 1 | 0.91 | 1.63 | 0.72 | 0.76 | 4.24 | 7.47 | 7.80 | 6 | 585 | 1.08 | 37 | 351 | 6345 |
| 10 | leave you | gold | 1.10 | 0.84 | 1.32 | 0.88 | 0.78 | 3.30 | 7.55 | 2.34 | 6 | 470 | 0.93 | 35 | 535 | 4274 |
| 12 | Mengfei Li | top-14 | 0.95 | 0.81 | 1.70 | 0.77 | 0.78 | 5.40 | 6.76 | 3.57 | 6 | 495 | 0.95 | 33 | 672 | 4646 |
| 13 | HowardLeeTW | top-14 | 0.97 | 0.94 | 1.55 | 0.72 | 0.81 | 5.50 | 7.67 | 2.71 | 6 | 421 | 0.92 | 38 | 1311 | 8277 |
| 14 | Catalyst | top-14 | 1.07 | 0.98 | 1.29 | 0.94 | 0.79 | 3.59 | 7.55 | 2.88 | 6 | 483 | 0.95 | 36 | 425 | 4562 |
| 15 | feel the agi | top-14 | 1.07 | 1.06 | 1.53 | 0.84 | 0.89 | 5.75 | 7.48 | 3.90 | 6 | 516 | 0.88 | 24 | 648 | 7052 |
| 16 | local | gold | 1.03 | 0.90 | 1.46 | 1.01 | 0.79 | 3.45 | 7.48 | 2.35 | 6 | 486 | 0.93 | 36 | 488 | 4541 |
| 17 | lumen | gold | 0.99 | 0.96 | 1.51 | 0.93 | 0.79 | 3.53 | 7.58 | 2.75 | 6 | 469 | 0.92 | 35 | 508 | 5189 |
| 19 | carbonapi | gold | 1.04 | 0.98 | 1.26 | 0.98 | 0.80 | 3.88 | 7.50 | 3.49 | 6 | 505 | 0.99 | 40 | 354 | 4559 |
| 20 | Cow Boy | gold | 1.08 | 0.96 | 1.32 | 1.01 | 0.78 | 3.12 | 7.61 | 2.54 | 6 | 472 | 0.94 | 35 | 449 | 4533 |
| 21 | Ebi | gold | 1.06 | 0.93 | 1.66 | 0.80 | 0.84 | 4.85 | 7.72 | 43.43 | 6 | 1206 | 0.86 | 35 | 784 | 5361 |
| 22 | アルモンド | top-14 | 1.15 | 1.05 | 1.51 | 1.00 | 0.86 | 4.35 | 7.55 | 2.90 | 6 | 470 | 0.95 | 35 | 586 | 5371 |
| 23 | AI是我的豆包 | gold | 1.01 | 0.98 | 1.59 | 0.81 | 0.81 | 4.56 | 7.40 | 1.99 | 5.92 | 453 | 1.11 | 32.50 | 734 | 4929 |
| 24 | fog flower | gold | 1.04 | 0.90 | 1.32 | 0.88 | 0.78 | 3.18 | 7.55 | 2.36 | 6 | 506 | 0.94 | 35 | 522 | 4418 |
| 25 | Otter Vibe | top-14 | 1.02 | 0.90 | 1.72 | 0.82 | 0.90 | 7.63 | 7.88 | 3.93 | 6 | 507 | 1.02 | 46 | 615 | 10308 |
| 26 | nilochan | gold | 1.07 | 0.98 | 1.37 | 0.98 | 0.81 | 3.52 | 7.55 | 2.44 | 6 | 482 | 0.93 | 37 | 509 | 4452 |
| 27 | yjshyfy | gold | 1.06 | 0.93 | 1.32 | 0.87 | 0.78 | 3 | 7.55 | 2.31 | 6 | 480 | 0.95 | 35 | 552 | 4651 |
| 28 | kyy666 | gold | 1.08 | 1.00 | 1.47 | 0.96 | 0.81 | 3.39 | 7.52 | 2.34 | 6 | 503 | 0.93 | 37 | 484 | 4444 |
| 29 | 𝕯𝖊𝖔𝖉𝖎𝖒𝖘 & 𝕮𝖔 | silver | 1.09 | 0.89 | 1.39 | 0.98 | 0.81 | 3.36 | 7.56 | 2.66 | 6 | 508 | 0.93 | 37 | 490 | 4424 |
| 31 | redblackbst | top-14 | 1.11 | 1.03 | 1.53 | 0.89 | 0.86 | 2.83 | 7.38 | 2.22 | 6 | 511 | 0.97 | 36 | 437 | 3342 |

## 9. Structure: one dense public point and two leader clusters

PCA over 4020 current-submission games of 59 teams on 36 standardised features
(farm plan, ops, corrected sales and prices). The first three components carry
41% of the variance. PC1 runs from the family's signature (fertilizer sold rather
than used, CARE every day, land bought late, wool) to the leaders' (fertilizer used, tomatoes
and eggs, geese); PC2 separates the two leader groups (cows, strawberries and milk against
sheep, carrots and wool):

| component | variance % | negative end | positive end |
|---|---|---|---|
| PC1 | 17.80 | sold_fertilizer (-0.27), op_care (-0.25), price_melon (-0.23), land_day_2 (-0.20), sold_wool (-0.19) | op_fertilize (0.28), sold_tomato (0.27), plants_tomato (0.27), sold_egg (0.25), bought_goose (0.21) |
| PC2 | 12 | sold_milk (-0.30), sold_strawberry (-0.29), bought_cow (-0.27), plants_strawberry (-0.27), price_strawberry (-0.23) | op_plant (0.31), plants_carrot (0.25), sold_wool (0.24), bought_sheep (0.23), sold_carrot (0.22) |
| PC3 | 11.30 | op_water (-0.31), op_plant (-0.30), plants_wheat (-0.20), land_day_1 (-0.17), price_melon (-0.17) | bought_sheep (0.34), sold_wool (0.33), peak_hands (0.29), price_wool (0.25), op_pass (0.22) |

![pca](figs/an_pca.png)

Group medians of the team centroids:

| group | PC1 | PC2 | PC3 |
|---|---|---|---|
| top-14 | 1.33 | 0.19 | -0.67 |
| gold | -0.99 | -0.21 | -0.62 |
| silver | -1.16 | -0.21 | -0.52 |
| bronze | -1.55 | -0.34 | -0.54 |

k-means on the 59 team medians (standardised the same way), for k = 2 to 5, with the zone
make-up of each cluster:

| k | cluster | teams | top-14 | gold | silver | bronze | who (by rank) |
|---|---|---|---|---|---|---|---|
| 2 | 0 | 44 | 5 | 9 | 20 | 10 | leave you, Catalyst, feel the agi, local, lumen, carbonapi, Cow Boy, アルモンド ... |
| 2 | 1 | 15 | 9 | 5 | 1 | 0 | Artem The Farmer 🍅, Majkel1337, Unknown Mother-Goose, DSM, SpaTaro, THIRD FARM CLUB, Orbital Terraformer, Sida Zuo ... |
| 3 | 0 | 7 | 3 | 3 | 1 | 0 | Unknown Mother-Goose, THIRD FARM CLUB, Mengfei Li, HowardLeeTW, Ebi, Otter Vibe, THUNDER THUNDER |
| 3 | 1 | 44 | 5 | 9 | 20 | 10 | leave you, Catalyst, feel the agi, local, lumen, carbonapi, Cow Boy, アルモンド ... |
| 3 | 2 | 8 | 6 | 2 | 0 | 0 | Artem The Farmer 🍅, Majkel1337, DSM, SpaTaro, Orbital Terraformer, Sida Zuo, ymg_aq, AI是我的豆包 |
| 4 | 0 | 7 | 5 | 2 | 0 | 0 | Artem The Farmer 🍅, Majkel1337, DSM, SpaTaro, Orbital Terraformer, Sida Zuo, AI是我的豆包 |
| 4 | 1 | 7 | 4 | 2 | 1 | 0 | Unknown Mother-Goose, THIRD FARM CLUB, ymg_aq, Mengfei Li, HowardLeeTW, Otter Vibe, THUNDER THUNDER |
| 4 | 2 | 2 | 0 | 1 | 1 | 0 | Ebi, Kaggriculture Agent |
| 4 | 3 | 43 | 5 | 9 | 19 | 10 | leave you, Catalyst, feel the agi, local, lumen, carbonapi, Cow Boy, アルモンド ... |
| 5 | 0 | 7 | 6 | 1 | 0 | 0 | Artem The Farmer 🍅, Majkel1337, DSM, SpaTaro, Orbital Terraformer, ymg_aq, AI是我的豆包 |
| 5 | 1 | 6 | 3 | 2 | 1 | 0 | Unknown Mother-Goose, THIRD FARM CLUB, Mengfei Li, HowardLeeTW, Otter Vibe, THUNDER THUNDER |
| 5 | 2 | 2 | 0 | 1 | 1 | 0 | Ebi, Kaggriculture Agent |
| 5 | 3 | 1 | 0 | 1 | 0 | 0 | Sida Zuo |
| 5 | 4 | 43 | 5 | 9 | 19 | 10 | leave you, Catalyst, feel the agi, local, lumen, carbonapi, Cow Boy, アルモンド ... |

The picture is not a continuum: 44 of the 59 teams form one tight cluster (every silver and
bronze team, nine of the fourteen gold, and the five family members of the top-14) with a
within-team spread of about 0.5 on PC1; the other 15 teams split into two stable groups, the
2-cow-3-sheep code base and its relatives (Majkel1337, DSM, Orbital Terraformer, SpaTaro,
Artem The Farmer, ymg_aq, Sida Zuo) and the goose-and-tomato agents (Unknown Mother-Goose,
THIRD FARM CLUB, Mengfei Li, HowardLeeTW, Otter Vibe, THUNDER THUNDER). The zone medians of
PC1 differ only because the zones contain different numbers of leaders: a silver team is
not "between" gold and bronze, it is on the public point like most of gold.

## 9b. Two ways to beat the plateau: out-earn it, or starve it

A seat on the current public line banks a median 98.9k over all sampled games
(101.2k against opponents off the line, 96.4k in mirror matches). Each leader's
games against opponents on that line, current submissions:

| rank | team | games vs the line | win % | median margin | own bank vs the line | own bank, all games | line opponent's bank | line's bank vs others |
|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | 54 | 96 | 11586 | 97662 | 101286 | 87520 | 101160 |
| 2 | Majkel1337 | 30 | 93 | 10494 | 114018 | 113359 | 101808 | 101160 |
| 3 | Unknown Mother-Goose | 32 | 97 | 10400 | 112681 | 117671 | 105500 | 101160 |
| 4 | DSM | 51 | 98 | 10954 | 103550 | 104556 | 95094 | 101160 |
| 5 | SpaTaro | 11 | 91 | 4892 | 90769 | 96835 | 85944 | 101160 |
| 6 | THIRD FARM CLUB | 30 | 93 | 13374 | 114670 | 115275 | 98416 | 101160 |
| 7 | Orbital Terraformer | 37 | 92 | 8038 | 103874 | 103874 | 97530 | 101160 |
| 8 | Sida Zuo | 36 | 89 | 7246 | 102382 | 106280 | 97500 | 101160 |
| 9 | ymg_aq | 28 | 96 | 13854 | 97816 | 105855 | 81622 | 101160 |
| 10 | leave you | 50 | 92 | 3291 | 101572 | 101830 | 95396 | 101160 |
| 12 | Mengfei Li | 37 | 95 | 9200 | 95026 | 104299 | 88156 | 101160 |
| 13 | HowardLeeTW | 47 | 85 | 4477 | 107917 | 107917 | 106195 | 101160 |
| 14 | Catalyst | 37 | 95 | 5619 | 97942 | 102193 | 92839 | 101160 |
| 15 | feel the agi | 36 | 83 | 7880 | 115032 | 112062 | 107526 | 101160 |
| 32 | Kilupy | 46 | 85 | 1600 | 90176 | 100353 | 87410 | 101160 |
| 41 | Thomas Tschinkel | 39 | 87 | 2973 | 94311 | 96968 | 92220 | 101160 |
| 601 | Cyrus | 21 | 76 | 367 | 113636 | 112238 | 103630 | 101160 |
| 881 | Toru59er | 21 | 14 | 0 | 100646 | 111330 | 100654 | 101160 |

Majkel1337, THIRD FARM CLUB, Unknown Mother-Goose, feel the agi and HowardLeeTW **out-earn**
the line: the opponent keeps roughly its usual bank and they finish 108-115k. Artem The
Farmer, ymg_aq and Mengfei Li **starve** it: their own banks are ordinary (95-98k) and the
opponent's falls to 82-88k. The memo's "the #1 wins on the market" was half right in the
wrong way: the top of the ladder is a market-denial contest, and Artem is #1 (19-11 over
Majkel1337) because denial also hurts the out-earners, whose banks rest on premium prices.
Section 7 names the two mechanisms: metering premium sales at the town's drain rate in small
orders across the day (out-earn), and selling first each day from the previous day's
harvest, every product, every day to the end, with staples covering the late income
(starve).

What the line's opponent receives per unit when it plays each leader, against what a seat on
the line receives against non-family opponents ("ref"), corrected sales:

| rank | team | n | opp strawberry $ / ref | opp melon $ / ref | opp milk $ / ref | opp wool $ / ref | opp wheat $ / ref | opp carrot $ / ref | opp tomato $ / ref | opp egg $ / ref | opp premium revenue / ref | own premium revenue | own staple revenue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Artem The Farmer 🍅 | 54 | 93 / 110 | 202 / 200 | 70 / 82 | 89 / 93 | 38 / 39 | 46 / 49 | 87 / 143 | 54 / 54 | 77k / 88k | 80k | 44k |
| 2 | Majkel1337 | 30 | 132 / 110 | 227 / 200 | 87 / 82 | 86 / 93 | 39 / 39 | 48 / 49 | 122 / 143 | 52 / 54 | 90k / 88k | 94k | 42k |
| 3 | Unknown Mother-Goose | 32 | 118 / 110 | 198 / 200 | 83 / 82 | 125 / 93 | 39 / 39 | 43 / 49 | 102 / 143 | 52 / 54 | 93k / 88k | 93k | 47k |
| 4 | DSM | 51 | 84 / 110 | 226 / 200 | 89 / 82 | 104 / 93 | 37 / 39 | 45 / 49 | 110 / 143 | 52 / 54 | 82k / 88k | 86k | 44k |
| 5 | SpaTaro | 11 | 88 / 110 | 218 / 200 | 42 / 82 | 110 / 93 | 37 / 39 | 48 / 49 | 314 / 143 | 56 / 54 | 73k / 88k | 76k | 48k |
| 6 | THIRD FARM CLUB | 30 | 113 / 110 | 219 / 200 | 94 / 82 | 86 / 93 | 41 / 39 | 47 / 49 | 120 / 143 | 47 / 54 | 86k / 88k | 84k | 50k |
| 7 | Orbital Terraformer | 37 | 96 / 110 | 227 / 200 | 82 / 82 | 84 / 93 | 38 / 39 | 47 / 49 | 208 / 143 | 54 / 54 | 86k / 88k | 88k | 42k |
| 8 | Sida Zuo | 36 | 108 / 110 | 216 / 200 | 74 / 82 | 106 / 93 | 40 / 39 | 43 / 49 | 127 / 143 | 51 / 54 | 85k / 88k | 77k | 46k |
| 9 | ymg_aq | 28 | 77 / 110 | 239 / 200 | 69 / 82 | 87 / 93 | 38 / 39 | 45 / 49 | 123 / 143 | 56 / 54 | 76k / 88k | 80k | 73k |
| 10 | leave you | 50 | 118 / 110 | 198 / 200 | 99 / 82 | 71 / 93 | 38 / 39 | 49 / 49 | 155 / 143 | 55 / 54 | 84k / 88k | 84k | 39k |
| 12 | Mengfei Li | 37 | 114 / 110 | 198 / 200 | 58 / 82 | 70 / 93 | 39 / 39 | 47 / 49 | 83 / 143 | 54 / 54 | 77k / 88k | 76k | 49k |
| 13 | HowardLeeTW | 47 | 114 / 110 | 242 / 200 | 84 / 82 | 99 / 93 | 35 / 39 | 50 / 49 | 98 / 143 | 53 / 54 | 92k / 88k | 85k | 42k |
| 14 | Catalyst | 37 | 103 / 110 | 212 / 200 | 70 / 82 | 99 / 93 | 38 / 39 | 55 / 49 | 169 / 143 | 51 / 54 | 82k / 88k | 88k | 44k |
| 15 | feel the agi | 36 | 142 / 110 | 200 / 200 | 79 / 82 | 132 / 93 | 39 / 39 | 45 / 49 | 114 / 143 | 47 / 54 | 96k / 88k | 92k | 53k |

## 10. What the data cannot answer, and what it would cost

- **History for the zone teams.** 30 of the 63 teams have only their current submission's
  first 50 games (C0); the per-window trajectories in section 5 exist for the 29 teams of the
  first two batches only. Every "how did silver and bronze get here" statement rests on the
  generations table (section 4), which dates lines by the sampled seats of *both* players and
  therefore does see those teams' earlier submissions as opponents, but not their own first
  games. Fetching F for the 34 zone teams is 1,700 replays, about 14 hours at the quota's
  pace (`fetch.py --windows F`).
- **The last 50 games of the zone teams (L).** Also missing for the same 34 teams; C0 games are
  entry-phase games against weaker opponents, so their win rates and opponent ratings are
  not comparable with the top-14's L windows. 1,700 replays, 14 hours.
- **Ladder-wide shares of the public generations.** The sample over-weights the studied
  teams; the community hash index (`data/community/stream_hashes.csv`, full-stream hashes
  through 2026-09-14) cannot date the family's field lines because its hash includes market
  orders, which vary. A daily sample of 100 random public games from the episode listing
  would give unbiased shares; the listing endpoint is not replay-rationed but the replays
  are (100 a day, about an hour a day).
- **Prices the agents saw when they decided to sell.** The traces carry the price before each
  turn and the revenue per sale; a per-turn price series for every game would need the
  replays again (kept on disk, no quota) and about an hour of extraction.
- **Whether the leaders' extra carrots and tomatoes pay.** Section 7 shows the conditional
  revenue, not the counterfactual. That is an arena question (plant the family's 31 carrots
  vs 60 when a Pet Cafe unlocks, same seeds), not a data question.

## 11. What to clone, what to hybridise, and how to judge it

Layer by layer, which studied version is best and whether they combine:

- **Economy (clone the public line, then Artem's variant of it).** The current public line
  (33 strawberry, 163 wheat, 12 melon, 31 carrot, 8 cows, 6 sheep, 3 geese, land on days 6
  and 11, 12 hands) banks 99-101k against ordinary opponents and is what four fifths of the
  medal plateau runs; matching it is the floor. Artem The Farmer's skeleton differs in the
  second land purchase (day 8, three days earlier), fewer strawberries (24-29), more carrots
  and tomatoes, and 13 hands, and is the only leader line that other teams have copied
  (section 4). The two farms are compatible: same quadrants, same herd order, same melon
  cash-in on day 10-11.
- **Opening (clone the family's or the 2c3s list; no opponent read).** Both day-1 lists
  spend the $3,000 to the last dollar on animals, pastures, melon and wheat and hire 4-5
  hands. Nothing on day 1 depends on the opponent (section 1), so the opening is a fixed
  list with a budget loop for the last wheat seeds.
- **Shop response (clone the leaders' breadth).** Every zone follows the Yarn Store; the
  leaders also follow milk shops (cows and tomatoes), egg shops (geese) and carrot shops
  (carrots) and they follow them further (section 3). This is a table of per-shop
  increments applied when a shop unlocks on days 3, 6 and 9, not a strategy switch, and it
  is the one reactive layer with evidence behind it. The increments are read off the
  conditional means in section 3.
- **Labour (clone the leaders' end game, keep the family's mid game).** Ops per unit of work
  are identical across the zones (section 8) except fertilizer, where the leaders spend 30%
  more per crop tile-day. The leaders' CARE and FEED taper from day 27 and their herds are
  allowed to escape once no yield can be sold: do that, and fertilize more.
- **Market (hybridise Artem's denial with Majkel1337's metering).** Two things beat the
  public line (section 9b): out-earning it (Majkel1337, THIRD FARM CLUB, Unknown
  Mother-Goose finish 108-115k while the opponent keeps its usual 98-108k) and starving it
  (Artem, ymg_aq, Mengfei Li bank an ordinary 95-98k while the opponent falls to 82-88k).
  Artem is #1 and 19-11 over Majkel1337 because denial also works on the out-earners. The
  concrete rules (section 7): sell premium goods first thing each day from the previous
  day's harvest; meter each product at about the town's drain rate (strawberry 7 a day
  before day 18 and 22-36 after, milk 14, wool 12, split with the opponent) in small orders
  across the day, holding the rest in the shed; never let a premium price recover once the
  opponent's bulk sales start (days 20-24 for the current line); dump melon on day 10 with
  everyone else, since no shop buys it and timing earns nothing; and let staples (tomatoes,
  carrots, eggs, and wheat, whose glut curve is flat) carry the last ten days. Whether
  metering and denial combine against a line that also adapts is an arena question.
- **Noise (skip).** SpaTaro's unexecutable orders protect it from cloning and cost nothing,
  but they are not why it wins and it is 5th, not 1st.

**The yardstick.** Everything above is measured against the current public line; the line
changes every seven to ten days (section 4), so the local gate should be paired-seat games on
fixed seeds against (a) the current public line's recorded games (`export_tapes.py` on the
family's C0 windows, both seats), (b) Artem's and Majkel1337's recordings, and (c) whatever
line is public two weeks from now, re-exported then. Win rate is the score; the median margin
over the line (7k for the top-14, 4k for gold, 2k for silver) is the diagnostic.
