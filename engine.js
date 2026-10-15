var BlowerMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var NOMINAL = 0.9;
  function batteryPlan(maxVolts, ah) {
    if (!pos(maxVolts)) return { error: "the sticker volts must be above zero" };
    if (!pos(ah)) return { error: "the amp-hours must be above zero" };
    var nominal = maxVolts * NOMINAL;
    return { nominal: r1(nominal), wh: r1(nominal * ah) };
  }
  function renderBattery(r, maxVolts, ah) {
    return "The " + jsnum(maxVolts) + " on the battery names the charge peak, not the running voltage; the pack runs at about "
      + jsnum(r.nominal) + " volts, so the " + jsnum(ah) + " amp-hour sticker holds about " + jsnum(r.wh) + " watt-hours.";
  }
  function runtimePlan(wh, watts, claimed) {
    if (!pos(wh)) return { error: "the watt-hours must be above zero" };
    if (!pos(watts)) return { error: "the turbo draw must be above zero" };
    if (!pos(claimed)) return { error: "the claimed minutes must be above zero" };
    var minutes = wh / watts * 60;
    var ratio = minutes / claimed * 100;
    var verdict = ratio >= 90 ? "the box is nearly honest"
      : ratio >= 60 ? "the box rounds in its own favor"
      : "the box is marketing first";
    return { minutes: r1(minutes), pctOfClaim: r1(ratio), verdict: verdict };
  }
  function renderRuntime(r, wh, watts, claimed) {
    return "A pack holding " + jsnum(wh) + " watt-hours feeding " + jsnum(watts) + " turbo watts lasts about " + jsnum(r.minutes)
      + " minutes, not the " + jsnum(claimed) + " on the box - " + jsnum(r.pctOfClaim) + "% of the claim, and " + r.verdict + ".";
  }
  function movePlan(cfm, mph) {
    if (!pos(cfm)) return { error: "the CFM must be above zero" };
    if (!pos(mph)) return { error: "the MPH must be above zero" };
    var band = cfm >= 550 ? "wet mats and stuck-down leaves"
      : cfm >= 350 ? "ordinary yard piles"
      : "light sweeping off hard surfaces";
    return { band: band };
  }
  function renderMove(r, cfm, mph) {
    return "At " + jsnum(cfm) + " CFM the blower moves " + r.band + "; the " + jsnum(mph)
      + " MPH was measured at the tip of the narrowest nozzle, where almost no air flows.";
  }
  return { batteryPlan: batteryPlan, renderBattery: renderBattery, runtimePlan: runtimePlan, renderRuntime: renderRuntime, movePlan: movePlan, renderMove: renderMove };
})();
if (typeof module !== "undefined" && module.exports) module.exports = BlowerMath;
