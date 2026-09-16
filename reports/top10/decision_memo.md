# Decision memo: what the top 10 actually do, and what we should build

Built from `summary.md`, the 14 dossiers (3,431 sampled games with replays: every team's
first 50, last 50, current submission's first 50, and the 25% and 50% quarter windows; the
75% window is partial because Kaggle rations replay downloads), and, since 2026-09-15,
`groups.md`, which compares the 14 with the next 15 teams of the gold zone on the same
features. Every number below is in those files.

## The question

Iminabo asked whether our agent should be one deterministic plan, or something that switches
strategy in the middle of a game. The forum consensus said the ladder is full of replayed
"tapes". The 14 teams that were top-10 in the screenshot or on the live board tell a
different story, and the answer is neither of the two options as posed.

## What the evidence says

**1. The head of the ladder moved from tapes to runtime agents in the last three weeks.**
In their first 50 games most of these teams replayed one line: ymg_aq's 25% window has 9
field lines and a single market line across 50 games; Mengfei Li's first window 15 field
lines; DSM 16; HowardLeeTW 7; アルモンド 9; feel the agi 9; Thomas Tschinkel 14; Catalyst 12.
In their last 50 games, every team's games are all distinct by turn 400. Two teams were
reactive from their first window (Artem The Farmer, Otter Vibe). So "first 50 vs last 50"
has one answer for almost everyone: they started by replaying, and they climbed by reacting.

**2. Everyone converged on the same economic skeleton.** Medians of the current submissions
(`summary.md`, "Farm plan"): three quadrants, never the fourth; first land purchase on day
5-6 and the second on day 8-11; 11-15 hands a day; 7-11 cows; 3-8 sheep; 0-6 geese; 24-33
strawberry tiles; 100-190 wheat plantings; 11-16 melons; 250-420 CARE ops; 90-190 FERTILIZE
ops; a hard liquidation in the last three days. Over the windows the field shifted from
about 40 strawberry and 100 wheat plantings to about 30 strawberry and 150-190 wheat, and
geese appeared. Herd sizes barely move between windows. Nobody switches macro-strategy inside
a game; nobody plays a different economy.

**3. Nobody plays one fixed plan to the end, and the best teams branch earliest.** The
order-insensitive plan fingerprint (unit ops with arguments plus executable market orders,
movement ignored) shows where each current submission's games stop being identical:

| plan stops being one line at | teams |
|---|---|
| day 1 (turn 24) | Majkel1337 (#1), DSM, Orbital Terraformer, redblackbst, SpaTaro, feel the agi, Catalyst |
| day 2 (turn 48) | ymg_aq (#2), Otter Vibe, HowardLeeTW, アルモンド |
| day 5-6 (turn 136) | Mengfei Li, Artem The Farmer, Thomas Tschinkel |
| day 16 (turn 400) | every game of every team is distinct |

**4. What the branching tracks: the shop draw, not the opponent.** (Rewritten 2026-09-16
after reading the branches, `analysis.md` sections 1 and 3, P17.) The earlier version of this
finding said Majkel1337 and Orbital Terraformer "read the first hours of the opponent's farm
and change their own day" because their off-line rate on day 1 tracked the opponent's. The
day-1 lines are one purchase list each; they differ only in the last one to three wheat
seeds the budget allows, which the wheat price (moved a dollar by the opponent's turn-0
trades) decides. Nobody on the plateau changes its day-1 plan for the opponent. What every
studied team, from the #1 to the last bronze team, does react to is the town's shop draw:
a Yarn Store among the first three unlocks means 10-14 sheep instead of 4-6, a milk shop
8-9 cows instead of 5-7. The leaders react to more products (carrots 50-95 with a Pet Cafe
or Farmers Market against the family's fixed 31; tomatoes 8-12 with a milk shop against
none) and by more (SpaTaro 20 sheep, 13 cows). The "reactivity gradient" across the zones is
the breadth of that response: top-14 follow 4.5 of 5 products (median), gold 3.5, silver 2,
bronze 1 (the Yarn Store alone). HowardLeeTW's seat-dependent day 2 stands. From mid-game
every game is unique for everyone.

**5. Weeds are coupled to the opponent through the random stream.** Majkel1337's recorded
game reproduces exactly against its original opponent and collapses from 113k to 52k against
a passive one, because the weeds land on different days; five other recordings of the same
submission bank 116k-175k against the passive baseline because nobody competes in the
market. A fixed action list is not a plan; a plan that is not weed-aware is not one either.

**6. The #2's edge is the price it gets, not the volume it sells.** (Rewritten 2026-09-16
after P18: the traces had undercounted most teams' sales by 35-50%, which made Majkel1337
look like it sold four times everyone's melon.) On corrected sales Majkel1337 sells the same
72 melons as the public line and *fewer* strawberries, milk and wool (218 / 180 / 109 against
248 / 191 / 126), but receives $169 a strawberry, $100 a milk and $132 a wool against the
line's $116 / $84 / $105, for a bank of 113k against 101-105k. The mechanism (`analysis.md`
section 7) is metering: strawberries in two-unit orders spread across the day, 9-10 a day
from day 20 while the line dumps 20-29, so its price holds at $144-170 while the line's own
units fetch $67-75; milk in bursts on days 14 and 16, ahead of the line's day-15 burst. Its
farm is slightly smaller (11 hands, 4 sheep). Its rating path: 651 after game 1, 2,543 after
25, 2,875 after 50, 3,097 after 100, 3,247 after 200.

**7. The #1 beats the #2 by starving the market, not by out-earning it.** (Rewritten
2026-09-16.) Artem The Farmer is 19-11 against Majkel1337 on current submissions (58-54
all-time) and beats the public line 96% of the time by 11.6k with an ordinary bank of its
own (98k against the line): the line's bank falls to 87.5k against it (82k against ymg_aq,
88k against Mengfei Li, the other two starvers) from 101k against everyone else. The
mechanism: 29% of its strawberries go out at hour 0 from the previous day's harvest, before
the line's evening orders, and it sells every premium product every day to the end (10-14
milk, 6-9 wool, 7-12 strawberries a day through day 29), so the line's late dump meets a
market that never recovered (its strawberry price $93 against a reference $110, milk $70
against $82); Artem's own late income comes from staples (44k: carrots, tomatoes, eggs,
wheat). Denial hurts the out-earners too, whose banks rest on premium prices, which is why
the #1 is #1. Artem sells 78 melons a game, not 6.

**8. Three teams run the identical public plan.** アルモンド, Catalyst, and Thomas Tschinkel
share one field line through turn 200 and the same medians to the unit (33 strawberry, 163
wheat, 12 melon, 8 cows, 6 sheep, 3 geese). They sit at ranks 9-14 with 81-84% sampled win
rates. The group comparison below shows that line is what most of the rest of the gold zone
runs: it is the ceiling of the public tape-plus-router family, prize band, not the top.

**9. One team manufactures noise.** SpaTaro pads every game with a median of 238 market
orders the engine cannot execute (buying carrots, milk, wool). Its valid plan also varies in
every game. Cloning it from replays is deliberately hard, and it is still the third-best
economy on the board.

## Top-14 vs the next 15: what separates the prize band from the rest of gold

Iminabo's second question: is there a reason the other gold medalists are not top-10? The
next 15 are chunks of ranks 8-48 at the 2026-09-15T0033Z snapshot (Kaggle's medal rule puts
gold at rank 28 for 9,066 teams, so ranks 8-23 of the batch are gold under any rule and
29-48 only under the top-50 assumption). This section measures every one of the 29 teams
on every sampled game of its current submission (its first 50 plus its games among the
team's last 50), 50 to 126 games per team. The batch's earlier history windows are still
downloading under Kaggle's replay quota; they feed the dossiers, not this comparison.
Numbers are per-team medians, and "AUC" is the chance that a random top-14 team is above a
random next-15 team on that feature (0.5 = no separation). The same comparison run on the
first-50 window alone (the interim build) gave the same picture and nearly the same numbers.

**10. The next 15 are mostly one public tape family; the top 7 are all unique.** At turn 100
(day 4), 11 of the 15 batch teams sit on a field line byte-identical to another studied
team's. Three of the 14 top teams do: アルモンド, Thomas Tschinkel, and Catalyst, the bottom
of the top-14, on the same line as nine batch teams. Through day 8 the largest family still
has seven members, and at day 12 eight of the 15 batch teams are still on a line shared
with someone (two of the 14 top teams). None of the top 7 shares a line with anyone from
turn 24 on.

**11. The batch branches late and for the weather; the leaders branch on day 1 for the
opponent.** First field branch on day 1: 7 of 14 top teams, 1 of 15 batch; on day 8 or
later: 3 of 14 top, 11 of 15 batch. Opponent-driven branching exists only in the top group
(Majkel1337, Orbital Terraformer). Weed-driven branching is the batch's usual mode (6
teams, plus 4 that branch on the first shop draw): a tape with weed repair. At turn 400 the
median top team has 100% distinct games, the median batch team 69%.

**12. The economy is the same.** Nothing that measures farm size separates the groups:
3 quadrants, first land on day 6, 12 hands, 8 cows, about 160 wheat plantings, about 1,150
units sold, about 265 units in the last three days, final money 104k vs 103k, rating after
25 and 50 games. The batch buys its second land two days later (day 11 vs 9.5), plants one
more strawberry tile (33 vs 32), buys one more sheep, CAREs more (403 vs 334 ops) and
fertilizes less (111 vs 154).

**13. Market timing: everyone dumps melon on day 10, and the separators are prices, not
days.** (Rewritten 2026-09-16 on corrected sales.) Every zone sells its first melon on day
10 and its first strawberry on day 14-15; the family sells its last melon on day 11, the
top-14 on day 20 (a trickle worth nothing: the town removes one melon a day and no shop
buys it, so spreading melon earns 13.9k against the dump's 14.6k). Units sold in the last
three days are 393-399 everywhere. What separates the top-14 from the rest of gold is the
price received (strawberry $125 against $116, wool $117 against $105, milk $93 against $84,
AUC 0.70 / 0.71 / 0.62) on fewer units, and fertilizer sold (218 against 342, AUC 0.19:
the leaders use it on the fields).

**14. "Standing weeds" are exhausted strawberries, not a labour strategy.** (Rewritten
2026-09-16 from the tile-level pass, `analysis.md` section 2.) The engine rolls the weed
chance only on empty unlocked tiles, and the plateau farm keeps every tile occupied from day
8, so weeds that spawn are rare (0.1-2 a game). What the feature table counted as weed
tile-days is plants that finished their life and decayed in place, 74-100% of them
strawberries after the fourth yield. The public line digs every one within about 0.6 days;
the leaders leave 5-27% of the mid-game ones standing for a day or two while they have
spare empty tiles, and most of the ones that decay in the last three days forever. An
exhausted plant costs one DIG either way, which is why the DIG counts match. The labour
signal that does separate the zones is the end game: the leaders stop caring for and
feeding animals whose next yield cannot be sold before day 29 (CARE per animal 0.56 / 0.27 /
0 on days 27-29 against 0.94 / 0.88 / 0 for the family) and fertilize about 30% more per
crop tile-day (0.115 against 0.079-0.089); every other op per unit of work is the same in
every zone.

**15. Head to head, ratings, and losses.** All-time the top-14 beat the batch 663-439 (60%);
current submissions against current submissions 60-13 (82%). Sampled win rates are the
same (84% vs 83%) against slightly different opposition (mean opponent rating 2,453 vs
2,394). Both groups climb identically to about 2,850 by game 50; after game 200 the top-14
median is 3,043 and the batch's 2,882 (few batch teams have 200 games yet). The losses
differ in kind: the top-14 lose mostly to each other (58% of their sampled losses, median
margin 4.5k), the batch mostly to unstudied teams (78%, median margin 2.3k). Unknown
Mother-Goose (rank 8 at snapshot, a runtime agent by every measure above: unique line,
weed-driven branch on day 2, standing weeds tolerated) is the one batch team with a winning
all-time record against the top-14 (150-135).

**What this changes:** nothing in the architecture, and it removes a doubt. The gap between
gold and the prize band is not the economy, which the public plan already has right. It is
(a) not being a tape: react from day 1; (b) the market clock: spread melon sales, sell
strawberries earlier; and (c) labour discipline, of which weed handling is the visible sign.
A plan that merely equals the public family's economy lands around rank 15-30; the three
adaptive layers below are the difference to the top 7.

## Gold, silver, bronze: the zone comparison

Added 2026-09-16 from the full-leaderboard snapshot (2026-09-15T1342Z, 9,125 teams; gold to
rank 28, silver to 456, bronze to 912). Groups: the top-14; every other gold team the crawl
could seed (14 profiled of 16); silver, the first-batch teams now in silver plus chunks at
ranks 120, 250 and 400 (21); bronze, chunks at 470, 600, 750 and 880 (10 profiled of 12).
The 34 teams added for this comparison have only their current submission's first 50
games, so their win rates and opponent ratings are entry-phase numbers; four teams with
fewer than 10 games are left out. Full tables and all pairwise tests in `groups.md`.

**16. One tape family runs the whole medal plateau.** At turn 24, 34 of the 59 profiled
teams share one byte-identical field line: 7 of the top-14, 7 of 14 gold, 20 of 21 silver,
10 of 10 bronze. At day 8 the family still has 16 members, and 18 of 21 silver and 10 of 10
bronze teams remain on a line shared with someone, against 5 of 14 gold and 2 of 14 top-14.
Tape membership rises monotonically down the zones.

**17. Branching and its drivers follow the same gradient.** First field branch on day 8 or
later: 3 of 14 top-14, 10 of 14 gold, 18 of 21 silver, 10 of 10 bronze. Opponent-driven
branching: 2 top-14 teams, 2 gold, none in silver or bronze; below gold it is weeds and the
first shop draw. Distinct games at turn 400: 100%, 89%, 74%, 64% by zone.

**18. Neither the farm nor the sales change down the zones; the response to the town and
the end game do.** (Revised 2026-09-16.) Final money is 104k, 105k, 102k, 105k, total
revenue 133-136k and units sold in the last three days 393-399 in every zone; premium units
sold are the same or higher below the top-14 (strawberry 222, 248, 249, 248). CARE ops rise
334, 363, 405, 417 because the leaders stop caring for and feeding animals in the last three
days; FERTILIZE ops fall 154, 117, 111, 103 and fertilizer *sold* rises 218, 342, 342, 352.
The weed tile-days gradient (10.5, 0.2, 0, 0) is exhausted strawberries left standing
(finding 14). The first strawberry sale is day 14.5-15 everywhere, the first milk sale day 8
and the first wool sale day 6 everywhere.

**19. Outcomes: the rest of gold is close to the top-14; gold to silver is the real step.**
Current submissions head to head: top-14 over gold 99-89 (53%), gold over silver 76-37
(67%), all-time 55% and 59%. Rating after 100 games: 2,967, 2,922, 2,888, 2,622; after 200
games gold 2,944 against silver 2,838. Bronze banks as much as anyone (105.6k) against
weaker opponents and its rating stops near 2,620: a zone is decided by who a team can beat,
not by the size of its farm. The first batch's 60-13 record against the top-14 looked lopsided
because that batch was mostly silver.

**What this changes:** (revised 2026-09-16) the zones are graded by how much of the town's
demand a team's plan follows and by how it plays the market against the public line, not by
the farm. Breadth of shop response goes 4.5 / 3.5 / 2 / 1 products down the zones (finding
4); the leaders fertilize more and stop paying for animals in the last days (finding 14);
and every zone's margin over the current public line tells the same story: the top-14 beat
it 89% of the time by 7k, gold 88% by 4k, silver 80% by 2k, bronze 58% by nothing
(`analysis.md` section 9b). Below gold the public agent runs with fewer of its switches on
and the rating plateaus where its margin over its own copies runs out.

## The answer

Not "deterministic" and not "strategy switching". **One plan, adaptive execution:** a fixed
economic skeleton (the converged three-quadrant cow-and-sheep farm with strawberry, wheat,
and a day-10 melon cash-in), driven by a runtime controller that re-plans the details every
turn. Revised 2026-09-16 from `analysis.md`: the three layers that separate the leaders from
the public line are not the three named before.

1. **Follow the town.** Every agent on the plateau, bronze included, buys 10-14 sheep instead
   of 4-6 when a Yarn Store unlocks by day 9; the leaders also follow milk shops (cows,
   tomatoes), egg shops (geese) and carrot shops (carrots), and further. This is a table of
   per-shop increments applied on days 3, 6 and 9, and it is the only reactive layer with
   evidence behind it. Nobody reads the opponent on day 1 (P17).
2. **Sell against the public line's clock.** The line dumps melon on day 10 and strawberries
   at 20-29 a day on days 20-24, late in the day. Two things beat that: meter premium goods
   at the town's drain rate in small orders across the day and hold the rest in the shed
   (Majkel1337, $169 a strawberry against the line's $116), and sell first each day from
   the previous day's harvest, every product, every day, so the line's dump meets a loaded
   market while staples carry the last ten days (Artem, the line's strawberry price falls
   to $93). The #1 uses the second and beats the user of the first 19-11.
3. **An end game that stops paying for unsellable yield.** From day 27 the leaders taper
   CARE and FEED and let the herd escape; they also fertilize about 30% more per crop
   tile-day all season. Every other op per unit of work is the same in every zone, and
   weed repair is a non-issue on a full farm (finding 14).

## Architecture we will build

- `agent/plan.py`: the skeleton as day-indexed targets (land days, herd sizes, crop mix,
  hire counts), parameterised so variants can be A/B tested.
- `agent/executor.py`: per-turn assignment of unit actions to the farmer and hands from the
  plan and the live farm state (BFS routing; priorities feed > water > harvest > plant >
  build > care > fertilize > dig), with weed repair and feed-cash reservation.
- `agent/market.py`: buys funded in queue order; premium sales metered at the town's drain
  rate (from `unlocked_shops`) in small orders, the first of each day at hour 0 from the
  shed; a denial mode that keeps selling every premium product daily once the opponent's
  bulk sales start; melon dumped on day 10; end-game liquidation.
- `agent/town.py`: the per-shop increment table (sheep, cows, geese, carrots, tomatoes)
  applied when a shop unlocks. Replaces the opening classifier, which the data does not
  support.
- Every layer switchable, so the arena can measure each one's contribution.

## The build plan (rewritten 2026-09-16, amended the same day by Iminabo)

1. **Yardstick and floor (Phase 1).** The public line's own code is the arena opponent:
   yhay81's Shop Router 0909 and aurax7's reactive v5 and v6, pulled from Kaggle under
   `data/notebooks/` and run as `scripts/arena.py --b line:v5` (journal 2026-09-16). A
   runtime clone of the line's economy (`agent/`) is the skeleton every later layer needs,
   because a tape cannot follow the town, taper the end game, or meter and deny. Acceptance:
   production against the pass agent within a few percent of v5's, and a paired-seat record
   near even against v5 on fixed seeds, both seats. Gates: `scripts/eval.sh`; every executor
   change is bisected alone (journal 2026-09-16).
2. **The three layers (Phase 2), one at a time,** each gated by paired-seat win rate and
   margin against v5 and v6 on fixed seeds: (a) follow the town beyond the Yarn Store
   (carrots, tomatoes, geese at the leaders' breadth); (b) the end game and fertilizer
   (taper CARE and FEED from day 27, let the herd escape, fertilize about 30% more per crop
   tile-day); (c) the market: sell premium goods first each day from the previous day's
   harvest, meter at the town's drain rate in small orders, keep selling every premium
   product daily once the opponent's bulk sales start, dump melon on day 10, let staples
   carry the last ten days. Whether metering and denial combine is an arena question.
3. **No submission until the gauntlet says we stand a chance (Iminabo, 2026-09-16).** Many
   rounds against the top five and against three randomly chosen gold teams outside the top
   ten, through their recorded games (`scripts/top10/export_tapes.py`, `--b tape:`), knowing
   that a recording derails once the weeds differ (METHOD.md section 6), so the gauntlet is
   a floor. The early entry before 2026-09-23 is cancelled; the entry deadline still binds.

## Limits of this study

- The 75% quarter window is partial for the top-14 and the batch's F and quarter windows
  are still downloading (Kaggle rations replays to roughly 120 an hour). The group
  comparison uses only the current submissions, which are complete for all 29 teams; the
  history windows feed the dossiers' evolution tables and complete as the fetch continues.
- With 14 and 15 teams, a p-value near 0.05 is weak evidence; the findings above lean on
  the features where the AUC is beyond 0.75 or below 0.25 and on the family and
  head-to-head counts, which need no test.
- Ratings come from the community index plus one refresh of the public endpoint (99% of
  sampled games covered); a few teams' older windows are thinner.
- The API reports only the two active submissions per team, so lifetime submission counts
  cannot be verified; the crawl found 6-77 submissions per team.
- Windows before 2026-08-15 ran on older engine versions (labelled per window in the
  dossiers) and are read from recorded observations only.
- Plan fingerprints ignore movement, so two games that differ only in walking order look
  identical; that is intended.
- Until 2026-09-16 the traces capped each sale by the shed as observed *before* the turn's
  unit actions, although the engine applies DROP and PLACE first (P18). Every sales figure
  in this memo, `groups.md`, `summary.md` and the dossiers was rebuilt from an
  engine-faithful market replica (`research/market_replay.py`) that reconciles to the
  recorded money in every turn; `bought_*` columns now count executed rather than requested
  purchases, which lowered a few herd medians by one animal.
