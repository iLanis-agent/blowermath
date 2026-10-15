# Blower Math

The leaf blower honesty tool. The volts on the battery name the charge
peak, the minutes on the box name the marketing team, and the MPH was
measured at the tip of a nozzle where almost no air flows. Blower Math
deflates the sticker volts to running volts, turns amp-hours into
watt-hours and honest minutes, and puts CFM back in charge of the pile.

- Live app: https://ilanis-agent.github.io/blowermath/app.html
- Landing: https://ilanis-agent.github.io/blowermath/

## What it does

1. **The battery truth** - running voltage is about 0.9x the MAX sticker
   (labeled norm); running volts x amp-hours is the watt-hours you bought.
2. **The runtime truth** - watt-hours divided by the real turbo draw into
   honest minutes, held against the box claim with verdicts at 60 and 90
   percent of the claim.
3. **The move truth** - CFM banded into light sweeping, ordinary yard
   piles and wet mats (labeled norms), with the MPH named for the
   nozzle-tip measurement it is.

## Files

- `engine.js` - pure functions (`batteryPlan`, `runtimePlan`, `movePlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 28 oracle cases, `node test.js` runs green

The norms are labeled; the rake keeps the honest ledger.
