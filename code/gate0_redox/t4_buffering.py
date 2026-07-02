#!/usr/bin/env python
"""
T4 — I2-a charge-buffering feasibility  [REVERSED / ANCHORED FRAMING]
Sealed-Core Tribowhip redox-core test plan, Step T4.

FRAMING (from project lead, this chat)
--------------------------------------
Do NOT guess the flutter frequency / charge-per-pulse and check if the gel
copes. REVERSE it: what electrical profile does the CHEMISTRY need, and could a
tribowhip plausibly evolve to deliver it? The creature evolves whip length,
stiffness, geometry to land in the viable region (cf. chlorophyll tuning to a
niche). Different sub-regions = different whip types.

So the ANCHORED, well-posed question this script answers:
  Given a REALISTIC cofactor loading (LAB: ~0.4-2 M redox gels) and a cell-scale
  gel volume, what is the gel's charge-buffering CAPACITY, and therefore the
  ENVELOPE of pulsed electrical profiles it can smooth to steady output?
  Report that envelope; judge whether it is physically REACHABLE for a
  micron-to-mm appendage. Leave the flutter-mechanics derivation (does a ribbon
  of length L actually produce that profile?) to the separate whip-mechanics
  effort it is explicitly scoped to.

THE PHYSICS COLLAPSES TO ONE DIMENSIONLESS NUMBER
-------------------------------------------------
  N = Q_store / q_percycle
      Q_store    = C_cof * 1000 * n_e * F * V_gel      (coulombs the pool holds)
      q_percycle = charge deposited per pulse (= q_pulse), the thing evolved
  Capacitor smoothing: output ripple ~ 1/N. So:
      <10% ripple  <=>  N >= 10
      <1%  ripple  <=>  N >= 100
  This threshold is NOT tuned -- it is the standard ripple relation. We report
  several ripple targets so the SHAPE is visible, not a single hand-picked line.

  Inverting: q_pulse_max(ripple) = Q_store / N_required(ripple)
  This is the MAX charge-per-pulse the gel can buffer at that ripple. Multiply
  by an (evolvable) pulse rate to get bufferable average current. The creature
  evolves a whip whose (q_pulse, f) lands under this ceiling.

EVIDENCE TAGS (project rule): loadings = [LAB]; capacity/N = [SIM]; reachability
of the implied whip = [SPEC] (depends on out-of-scope flutter mechanics).

PROVENANCE CAVEAT (pinned project limitation): TENG charge densities come from
dry macroscopic lab devices (plasma/corona/electrospinning) a CELL CANNOT do.
Any q_pulse compared to lab TENG numbers is an OPTIMISTIC ceiling, flagged.
"""

import sys
import numpy as np

F = 96485.0  # C/mol

# ---- anchored inputs (real) ----
C_cof = np.array([0.01, 0.1, 0.4, 1.0, 2.0])   # M; 0.4-2.0 are LAB-real gel loadings
N_E   = 2                                       # 2e- per quinone (T3 capacitive reading)
# cell-scale gel volumes: micron to ~100 micron core, the "micron-to-mm appendage" base
V_GEL = {"(5 um)^3": (5e-6)**3,
         "(10 um)^3": (10e-6)**3,
         "(50 um)^3": (50e-6)**3}

# ripple targets -> required N (NOT tuned; ripple ~ 1/N)
RIPPLE_TARGETS = {"10% ripple": 10.0, "1% ripple": 100.0}

# for reachability context only (flagged, NOT used to pass/fail):
# TENG lab surface charge densities, briefing: ~50-150 uC/m^2 bare, up to mC/m^2 engineered
SIGMA_LAB = {"bare CE ~100 uC/m^2": 100e-6,
             "engineered ~1 mC/m^2": 1e-3}   # C/m^2 -- OPTIMISTIC, fab-lab provenance


def q_store(c_molar, v_gel):
    return c_molar * 1000.0 * N_E * F * v_gel   # coulombs


def main():
    print("=" * 72)
    print("T4 — Charge-buffering capacity  [reversed/anchored framing]")
    print("  Q: what electrical profile can a REAL gel buffer? (chemistry-first)")
    print("=" * 72)
    print("  N = Q_store / q_per_pulse ; ripple ~ 1/N ; N>=10 => <10% ripple")
    print("  loadings 0.4-2 M = [LAB] real redox gels; capacity = [SIM];")
    print("  whip reachability = [SPEC] (out-of-scope flutter mechanics)")

    for vname, vgel in V_GEL.items():
        print("\n" + "=" * 72)
        print(f"GEL VOLUME {vname} = {vgel:.2e} m^3")
        print("=" * 72)
        print(f"{'loading':>9} {'Q_store(C)':>12} "
              f"{'qmax@10%(C)':>13} {'qmax@1%(C)':>12} "
              f"{'#quinones':>11}")
        for c in C_cof:
            Qs = q_store(c, vgel)
            qmax10 = Qs / RIPPLE_TARGETS["10% ripple"]
            qmax1  = Qs / RIPPLE_TARGETS["1% ripple"]
            n_mol  = c * 1000.0 * vgel * 6.022e23   # molecules of cofactor
            tag = " [LAB-real]" if c >= 0.4 else ""
            print(f"{c:>7.2f}M {Qs:>12.2e} {qmax10:>13.2e} {qmax1:>12.2e} "
                  f"{n_mol:>11.2e}{tag}")

    # ---- reachability context: what whip AREA would deliver qmax in one contact? ----
    print("\n" + "=" * 72)
    print("REACHABILITY CONTEXT (flagged [SPEC], fab-lab provenance caveat)")
    print("=" * 72)
    print("If one flutter contact deposits q = sigma * A_contact, what whip area A")
    print("would match the gel's qmax@10%? (smaller A = easier to evolve).")
    print("Using a mid case: 0.4 M loading, (10 um)^3 gel.")
    Qs = q_store(0.4, V_GEL["(10 um)^3"])
    qmax10 = Qs / 10.0
    print(f"  Q_store = {Qs:.2e} C ; qmax@10% = {qmax10:.2e} C per pulse")
    for sname, sigma in SIGMA_LAB.items():
        A = qmax10 / sigma                      # m^2
        side = np.sqrt(A) * 1e6                  # equivalent square side, microns
        print(f"  sigma {sname:24s}: A = {A:.2e} m^2  (~{side:.1f} um square) "
              f"{'<- ceiling: cell cannot hit lab sigma' if 'engineered' in sname else ''}")

    print("\n" + "=" * 72)
    print("READING / VERDICT LOGIC")
    print("=" * 72)
    print("  * qmax columns = the MAX charge-per-pulse a real gel buffers at that")
    print("    ripple. A whip evolved to deposit <= qmax per contact is buffered")
    print("    to steady output. Higher loading / bigger gel => bigger qmax ceiling.")
    print("  * The creature evolves (q_pulse, f) to sit UNDER the qmax ceiling; many")
    print("    (loading, whip-area, rate) combos do so => different whip types.")
    print("  * PHYSICAL PLAUSIBILITY: if matching qmax needs only a small whip area")
    print("    (microns), the profile is reachable for a micron-to-mm appendage.")
    print("    If it needed square-millimetres of contact per pulse, it would not be.")
    print("  * CAVEATS (pinned): sigma values are dry-lab fab-process ceilings a cell")
    print("    cannot reach [SPEC]; flutter f itself is OUT OF SCOPE here (separate")
    print("    whip-mechanics effort). This shows the gel side CLOSES and bounds what")
    print("    the whip must deliver -- it does not derive the whip.")
    print("=" * 72)

    # close the loop with the LAB-anchored metabolic draw
    closed_loop()


# main() is invoked from the guard at the end of the file (after closed_loop is defined)


# ============================================================================
# CLOSED-LOOP EXTENSION  — metabolic draw anchored from astrobiology [LAB]
# ============================================================================
def closed_loop():
    e = 1.602e-19  # C per electron

    # --- metabolic draw anchors (LAB), converted to current per cell ---
    # P. aeruginosa anaerobic maintenance: 1.6e3 electrons/s/cell (Ciaccia 2024)
    I_maint = 1.6e3 * e                         # ~2.6e-16 A  [LAB]
    # LaRowe & Amend astrobiology floor ~1 zW/cell; observed 50-3500 zW/cell.
    # Convert a power to a current needs a per-electron energy; redox step ~0.3 V
    # => energy per electron ~0.3 eV = 4.8e-20 J. I = P / (0.3 V * e-charge basis):
    def power_to_current(P_watt, volts=0.3):
        return P_watt / volts                   # A  (P = I*V)
    I_floor   = power_to_current(1e-21)          # ~3.3e-21 A  (absolute floor)
    I_typical = power_to_current(300e-21)        # ~1.0e-18 A  (typical deep-sediment)
    I_lab_low = power_to_current(1e-18)          # lab low maintenance regime

    draws = {
        "absolute floor (~1 zW)":     I_floor,
        "typical deep-sed (~300 zW)": I_typical,
        "lab-low maintenance (~1 aW)":I_lab_low,
        "P.aerug anaerobic [direct e-]": I_maint,
    }

    print("\n" + "=" * 72)
    print("CLOSED LOOP — can an evolvable micron-whip deliver the metabolic draw?")
    print("  metabolic draw anchored from astrobiology/microbial energetics [LAB]")
    print("=" * 72)
    for k, v in draws.items():
        print(f"    draw '{k}': {v:.2e} A")

    # The whip must deliver <I_in> = f * q_pulse >= I_meta (on average), AND
    # q_pulse <= qmax (buffer ripple ok). Use the validated mid gel: 0.4 M, (10um)^3.
    Qs = q_store(0.4, V_GEL["(10 um)^3"])
    qmax10 = Qs / 10.0
    print(f"\n  buffer (0.4 M, (10 um)^3): Q_store={Qs:.2e} C, qmax@10%={qmax10:.2e} C")
    print("  For each draw, what pulse rate f is needed at a SMALL whip q_pulse?")
    print("  (pick q_pulse = 1e-15 C: a tiny per-contact charge, deep under qmax)")
    q_small = 1e-15
    if q_small > qmax10:
        print("   (note: even q_small exceeds qmax; buffer would clip -- not here)")
    print(f"\n  {'draw regime':<32}{'f_needed(Hz)':>14}{'reachable?':>14}")
    for k, I_meta in draws.items():
        f_needed = I_meta / q_small             # Hz to meet draw at this q_pulse
        # 'reachable': flutter regime is sub-Hz to ~5 Hz (TENG briefing). Above
        # ~100 Hz is implausible for a mm appendage in thin air.
        if f_needed <= 5:
            verdict = "YES (<5 Hz)"
        elif f_needed <= 100:
            verdict = "marginal"
        else:
            verdict = "NO (too fast)"
        print(f"  {k:<32}{f_needed:>14.2e}{verdict:>14}")

    print("\n  Interpretation:")
    print("   * f_needed = draw / q_pulse. A tiny 1e-15 C contact (sub-fC) at a few")
    print("     Hz already delivers ~1e-15 A; maintenance draws are 1e-21 to 1e-16 A.")
    print("   * So the whip is delivering current ORDERS above even the P.aeruginosa")
    print("     maintenance draw at trivially low pulse rates -- the loop closes with")
    print("     enormous margin for low-maintenance regimes.")
    print("   * The REAL constraint flips: not 'can it deliver enough' but 'the draw")
    print("     is so low that even a minute whip oversupplies it' -> the buffer's job")
    print("     (smoothing surplus pulses to steady draw) is exactly what's needed.")
    print("   * CAVEATS [SPEC]: q_pulse itself depends on out-of-scope flutter")
    print("     mechanics + the fab-lab sigma provenance gap; the 0.3 V draw->current")
    print("     conversion is order-of-magnitude. This shows the loop CLOSES with")
    print("     wide margin, not a precise operating point.")
    print("=" * 72)


# (closed_loop is invoked from main below)


if __name__ == "__main__":
    sys.exit(main())
