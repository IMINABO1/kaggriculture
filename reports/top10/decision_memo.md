# Decision memo: what the top 10 actually do, and what we should build

Built from `summary.md` and the 14 dossiers (3,431 sampled games with replays: every team's
first 50, last 50, current submission's first 50, and the 25% and 50% quarter windows; the
75% window is partial because Kaggle's API started dropping connections at the end of the
fetch). Every number below is in those files.

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

**4. What the branching tracks differs by team.** Measured at each team's first branch point
(dossiers, "What goes with being off the modal field line"):
- Majkel1337 and Orbital Terraformer leave their usual day-1 opening when the opponent's
  opening is unusual (70% vs 16% for the #1; 60% vs 14% for Orbital). They read the first
  hours of the opponent's farm and change their own day.
- HowardLeeTW's day-2 plan is decided by the seat (100% off the modal line in seat 1, 11% in
  seat 0).
- The fixed-opening teams (Mengfei Li, Artem, Thomas Tschinkel) leave their line by day 5-8;
  a weed before then moves 100% of those games off it, and an unusual first shop is the
  other trigger.
- From mid-game the drivers pile up (weeds, shop draws, prices, the opponent's sales) and
  every game is unique for everyone.

**5. Weeds are coupled to the opponent through the random stream.** Majkel1337's recorded
game reproduces exactly against its original opponent and collapses from 113k to 52k against
a passive one, because the weeds land on different days; five other recordings of the same
submission bank 116k-175k against the passive baseline because nobody competes in the
market. A fixed action list is not a plan; a plan that is not weed-aware is not one either.

**6. The #1's edge is the market, not the farm.** Against the median of the other current
submissions it sells four times the melon (72 vs 18), 40% more milk (182 vs 128), 70% more
wool (109 vs 63), and 40% more units in the last three days (365 vs 262), from a farm that is
slightly smaller (11 hands vs 12, 4 sheep vs 5, 8 cows either way). Its sampled win rate is
94% against 82% for the median team; its bank 113k against 104k. Its rating path: 651 after
game 1, 2,543 after 25, 2,875 after 50, 3,097 after 100, 3,247 after 200.

**7. Its losses are close and specific.** The only studied team with a winning record against
it is Artem The Farmer (28-26), who runs a fixed five-day opening, a sheep-leaning herd, and
sells almost no melon (6 a game). Sampled losses of the #1 are by 0.8k-4.3k to opponents on
the shared public opening that CARE more and fertilize less.

**8. Three teams run the identical public plan.** アルモンド, Catalyst, and Thomas Tschinkel
share one field line through turn 200 and the same medians to the unit (33 strawberry, 163
wheat, 12 melon, 8 cows, 6 sheep, 3 geese). They sit at ranks 9-14 with 81-84% sampled win
rates. That is the ceiling of the public tape-plus-router line: prize band, not the top.

**9. One team manufactures noise.** SpaTaro pads every game with a median of 238 market
orders the engine cannot execute (buying carrots, milk, wool). Its valid plan also varies in
every game. Cloning it from replays is deliberately hard, and it is still the third-best
economy on the board.

## The answer

Not "deterministic" and not "strategy switching". **One plan, adaptive execution:** a fixed
economic skeleton (the converged three-quadrant cow-and-sheep farm with strawberry, wheat,
and an early melon cash-in), driven by a runtime controller that re-plans the details every
turn. Three adaptive layers are what separates the leaders from the public line:

1. **Execution that survives the world**: weed repair, feed and water safety, and tile
   re-assignment when a weed or a failed order breaks the schedule. The fixed-opening teams
   do this from day 5; the #1 does it from day 1.
2. **An opponent read in the first day**: classify the opponent's opening (public line,
   mirror of our own plan, unknown) and choose between two or three openings. This is the
   #1's signature, shared only by Orbital Terraformer among the 14.
3. **A market layer with a clock**: premium sell timing against the opponent's visible
   inventory and sales, staple metering, and a scripted last-three-day liquidation. This is
   where the #1's whole margin over the field sits.

## Architecture we will build

- `agent/plan.py`: the skeleton as day-indexed targets (land days, herd sizes, crop mix,
  hire counts), parameterised so variants can be A/B tested.
- `agent/executor.py`: per-turn assignment of unit actions to the farmer and hands from the
  plan and the live farm state (BFS routing; priorities feed > water > harvest > plant >
  build > care > fertilize > dig), with weed repair and feed-cash reservation.
- `agent/market.py`: buys funded in queue order, sells paced by product curve, end-game
  liquidation, clone-aware front-running.
- `agent/opponent.py`: opening classifier over the opponent's first 24 turns of public state.
- Every layer switchable, so the arena can measure each one's contribution.

## First three experiments

1. **Skeleton only**: reproduce the median top-10 economy as a runtime agent and match its
   median bank (100-110k) against `pass` and `starter` with weeds on, 20 seeds, both seats.
   Until this holds nothing else matters.
2. **Execution robustness**: the same agent against the exported tapes of all 14 teams
   (`opponents/top10/`, recorded seat and seed) and the MIT reference agents. Tapes of
   reactive teams understate them (finding 5), so the target is "never lose to a tape by
   execution failure", not a win rate.
3. **Market layer**: add liquidation and premium pacing and measure paired-seat win rate
   against the skeleton-only agent and the tapes; then the opponent read.

## Limits of this study

- The 75% quarter window is partial (SpaTaro 26 games, feel the agi 1, several teams 0);
  the other five windows are complete for every team. The fetcher can finish it later.
- Ratings come from the community index plus one refresh of the public endpoint (99% of
  sampled games covered); a few teams' older windows are thinner.
- The API reports only the two active submissions per team, so lifetime submission counts
  cannot be verified; the crawl found 6-77 submissions per team.
- Windows before 2026-08-15 ran on older engine versions (labelled per window in the
  dossiers) and are read from recorded observations only.
- Plan fingerprints ignore movement, so two games that differ only in walking order look
  identical; that is intended.
