#!/usr/bin/env python3
"""
Gate 1(a) — The buildable-pulse / fab-lab provenance gap.
Triboic Life · Phase 2 · sealed-core tribowhip (silk-fibroin tribopositive layer
vs quinone/ionic-liquid redox-gel tribonegative core).

QUESTION (verbatim from plan v3, Gate 1a):
  Can a *biologically buildable* whip — no plasma, no corona poling, no
  electrospinning, no vacuum-evaporated electrodes, no LiCl/His doping — deliver
  the charge-per-pulse the validated gel needs?

PASS TARGET (from redox_core T4, the validated gel envelope):
  The closed buffering loop was demonstrated assuming a whip depositing
  ~1e-15 C (1 fC) per contact at sub-Hz-to-few-Hz. The binding maintenance
  regime is P. aeruginosa anaerobic maintenance: 2.6e-16 A, which 1 fC/pulse
  meets at 0.26 Hz. So the gel needs, per pulse:
      Q_pulse  >=  ~1e-15 C   (with flutter rate then setting the current)
  We report Q_pulse as a function of buildable-σ and ribbon geometry, and locate
  where it crosses the 1 fC line and the sub-fC neighbourhood the gel still
  tolerates at higher flutter rates.

MODEL (deliberately minimal — one equation, no hidden generosity):
      Q_pulse = sigma * A_geom * f_overlap
  sigma     : triboelectric surface charge density actually transferred per
              contact, BARE contact-electrification only (no fab process).
  A_geom    : geometric area of one ribbon face (length * width).
  f_overlap : fraction of geometric area making real microscopic contact per
              flutter cycle. Real contact area << geometric area for any
              non-engineered surface; this is the honest discount that the
              fab-lab texturing (micro-pyramids, electrospun mats) exists to
              defeat — and which a cell cannot perform. Swept low on purpose.

SOURCING OF THE SWEEP (every input tagged):
  sigma  [LAB, provenance-capped]:
    - TENG briefing 4.3 "bare contact electrification (typical)": ~50-150 uC/m^2.
      This is the ONLY rung needing no fab process — but it is still measured on
      pristine flat films against liquid metal in a glove box. Treat 150 uC/m^2
      as an optimistic ceiling, not an expected value.
    - Silk-fibroin TENG primary paper (project PDF, OCR'd): the *unenhanced*
      device delivers ~6 V; the headline 172 V / 1.2 W/m^2 needs LiCl + His
      doping + poly-L-lysine + PTFE counter-layer + vacuum-evaporated
      electrodes — none bio-accessible. And it is run against PTFE; the
      sealed-core pairs silk against a quinone gel (smaller series separation),
      so the bio pairing is weaker still.
    => We sweep sigma across 3 decades: 0.5 .. 150 uC/m^2, flagging sub-bands:
         optimistic lab-bare-CE corner : 50-150  uC/m^2
         plausible bio-accessible band : 1-50    uC/m^2  (weaker pair, dusty,
                                                           acid-fouled, no texture)
         pessimistic floor             : <1      uC/m^2
  A_geom [SPEC, swept]: evolvable micron-to-millimetre ribbon.
    length 1e-6 .. 1e-3 m, width 1e-7 .. 1e-4 m  ->  A_geom ~1e-13 .. 1e-7 m^2.
  f_overlap [SPEC, swept]: 1e-3 .. 1.0. (1.0 is the unphysical "perfect contact"
    corner, included only to show the ceiling; the honest region is <~0.1.)

ANTI-ARTIFACT DISCIPLINE (carried from the redox-core T4 lesson):
  A model that trivially passes (everything >> 1 fC) or trivially fails
  (everything << 1 fC) is an artifact, not physics. We therefore report the
  full crossing surface and check that 1 fC lands INSIDE the swept space, not
  off either edge. If it sits off an edge, the sweep bounds — not the physics —
  are wrong, and we widen them rather than report a verdict.
"""

import numpy as np

# ---- pass target from the validated gel (redox_core T4) ---------------------
Q_TARGET = 1e-15            # C per pulse, the T4 working assumption (1 fC)
Q_SUBFC  = 1e-16            # C, still tolerable at higher flutter rate (gel
                            # meets P. aeruginosa 2.6e-16 A if ~few Hz)

# ---- swept inputs (all bounded, all tagged in the docstring) ----------------
sigma_uC   = np.array([0.5, 1, 5, 10, 50, 100, 150])      # uC/m^2
sigma      = sigma_uC * 1e-6                                # C/m^2

# representative evolvable ribbon geometries (length_m, width_m, label)
ribbons = [
    (1e-6, 1e-7, "micro  1um x 0.1um"),
    (1e-5, 1e-6, "small  10um x 1um"),
    (1e-4, 1e-5, "mid    100um x 10um"),
    (5e-4, 5e-5, "large  500um x 50um"),
    (1e-3, 1e-4, "max    1mm x 100um"),
]

f_overlap  = np.array([1e-3, 1e-2, 1e-1, 1.0])             # real-contact fraction

def fmt(q):
    return f"{q:.2e}"

print("="*78)
print("Gate 1(a) — buildable charge-per-pulse  Q = sigma * A_geom * f_overlap")
print(f"PASS target (gel T4): Q_pulse >= {fmt(Q_TARGET)} C  (1 fC); sub-fC floor {fmt(Q_SUBFC)} C")
print("="*78)

# full surface + crossing check
any_pass = False
any_fail = False
crossing_inside = False

for (L, W, lab) in ribbons:
    A = L * W
    print(f"\nRibbon {lab:22s}  A_geom = {fmt(A)} m^2")
    print(f"  {'sigma(uC/m2)':>12s} | " + " | ".join(f"f={f:g}".rjust(11) for f in f_overlap))
    for s, suC in zip(sigma, sigma_uC):
        row = []
        for f in f_overlap:
            Q = s * A * f
            row.append(Q)
            if Q >= Q_TARGET: any_pass = True
            if Q <  Q_SUBFC:  any_fail = True
        # mark cells: P >=1fC, ~ between subfC and 1fC, x <subfC
        cells = []
        for Q in row:
            if   Q >= Q_TARGET: cells.append(f"P {fmt(Q)}")
            elif Q >= Q_SUBFC:  cells.append(f"~ {fmt(Q)}")
            else:               cells.append(f"x {fmt(Q)}")
        print(f"  {suC:>12g} | " + " | ".join(c.rjust(11) for c in cells))

# locate the 1 fC crossing in (sigma, A) at the honest overlap f=0.01
print("\n" + "="*78)
print("Crossing locator: minimum A_geom to reach 1 fC, per sigma, at f_overlap=0.01")
f_hon = 0.01
for s, suC in zip(sigma, sigma_uC):
    A_need = Q_TARGET / (s * f_hon)
    # express as a square ribbon side for intuition
    side = np.sqrt(A_need)
    flag = "(within swept A)" if 1e-13 <= A_need <= 1e-7 else "(OUTSIDE swept A -> widen, not verdict)"
    if 1e-13 <= A_need <= 1e-7: crossing_inside = True
    print(f"  sigma={suC:>5g} uC/m2 -> need A_geom={fmt(A_need)} m^2  (~{side*1e6:7.1f} um square)  {flag}")

print("\n" + "="*78)
print("ANTI-ARTIFACT CHECK")
print(f"  some cells PASS (>=1fC): {any_pass}")
print(f"  some cells FAIL (<0.1fC): {any_fail}")
print(f"  1 fC crossing lands inside swept (sigma,A) at honest f=0.01: {crossing_inside}")
if any_pass and any_fail and crossing_inside:
    print("  => GOOD: target sits INSIDE the bounded envelope, not off an edge.")
    print("     The result is a real boundary, not a trivially-pass/fail artifact.")
else:
    print("  => WARNING: target off an edge of the sweep. Widen bounds before any verdict.")
print("="*78)
