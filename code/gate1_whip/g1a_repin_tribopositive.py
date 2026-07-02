#!/usr/bin/env python3
"""
Gate 1(a) RE-PIN — corrected triboelectric pairing.

WHY THIS EXISTS
  The first pin used SILK FIBROIN as the tribo-positive layer (per v3 S2). But
  the quantified biopolymer series (Meng et al., Matter 2023 — the same 40-BP
  series v3 names for S2) places silk fibroin in the NEGATIVE half of the
  protein group (order, +->-: PGA > zein > pig-gelatin > DNA > polylysine >
  SF > fish-gelatin > SELP > collagen). Pairing silk (tribo-negative-ish)
  against a quinone gel (also tribo-negative) is a same-sign pair -> minimal
  charge transfer -> pinned sigma collapsed to ~0-7 uC/m^2 and the buildable
  pulse fell at/below the gel's 1 fC target. That is a real architecture error
  the data forced, not drift.

  FIX (hub-approved): use a genuinely tribo-POSITIVE biopolymer as the charge
  layer, chosen by the series' electron-donating end (carboxylate/amino/ether
  side groups): PEO-like ethers, HPC/HEC (cellulose ethers), sodium PGA,
  alginate, polylysine, chitosan, zein.

STRUCTURAL-LAYER DECOUPLING (user point, folded in)
  In a sealed-core sandwich the tribo-positive layer is a thin FUNCTIONAL SKIN.
  If a separate stiff backing/coat (sporopollenin S3, or a silk backing — silk
  is mechanically strong even though triboelectrically mediocre) carries the
  whip's bending/drag load, then the charge layer may be chosen for SIGMA ALONE,
  even if it is soft or weak (e.g. a gel-like polysaccharide). The mechanical
  cost of the extra layer is a Gate-2 build-ledger item, NOT a Gate-1(a)
  constraint. So under the ideal-conditions question asked here, the structural
  layer is "free" and sigma is unconstrained by mechanics.
  => This script tests sigma-vs-gap under IDEAL conditions, decoupled from
     structure, exactly as requested.

SIGMA RE-PIN (sourced, tagged)
  Series anchor [LAB]: PEO = 12.31 nC = 100% positive, films 2x2 cm vs common
  PTFE counter, contact-separation, short-circuit transferred charge.
    backbone-group means: polyether 100%, polysaccharide 78.22%,
                          protein 62.96%, poly(a-ester) 57.03%.
    explicit point value [LAB]: sodium PGA = 9.66 nC.
  Pair separation against the quinone gel = |Q_positive - Q_gel| on the common
  vs-PTFE scale [SIM: difference-of-references, O(1) uncertainty].
  The gel is the tribo-NEGATIVE partner; its exact series position is unknown
  [SPEC], so we SWEEP the gel from "mildly negative" to "strongly negative".
"""
import numpy as np

A_film = 2e-2*2e-2          # 4e-4 m^2 (series film size)
Q_PEO  = 12.31e-9           # C, 100% anchor

# --- tribo-POSITIVE charge-layer candidates, vs-PTFE charge (from series) ---
# % of PEO -> Q -> implied sigma_vsPTFE (= Q/A_film)
positives = {
    "PEO (ether, most +)":        100.0,
    "HPC/HEC (cellulose ether)":   92.0,   # text: most-positive BPs, ~just under PEO
    "sodium PGA (9.66 nC)":        9.66e-9/Q_PEO*100,
    "polysaccharide mean":         78.22,
    "alginate (top of polysacc.)": 80.0,   # "most positive in group 2"
    "polylysine (protein +half)":  68.0,   # above SF, below PGA in protein band
}

# --- gel tribo-NEGATIVE partner position, swept (% of PEO scale) ---
# lower % = more negative = larger separation from a positive partner.
gel_positions = {"gel mildly negative (55%)":55.0,
                 "gel moderately neg (45%)":45.0,
                 "gel strongly neg (35%)":35.0,
                 "gel PTFE-like floor (10%)":10.0}

print("="*86)
print("RE-PIN: pair sigma = |Q_positive - Q_gel| / A_film   (vs-PTFE common scale)")
print("="*86)
print(f"{'charge layer':28s} {'gel pos':26s} {'dQ(nC)':>8s} {'sigma_pair(uC/m2)':>18s}")
pair_sigmas=[]
for pl,plpct in positives.items():
    Qpl=Q_PEO*plpct/100
    for gl,glpct in gel_positions.items():
        Qg=Q_PEO*glpct/100
        dQ=abs(Qpl-Qg); sig=dQ/A_film*1e6
        pair_sigmas.append(sig)
        print(f"{pl:28s} {gl:26s} {dQ*1e9:8.2f} {sig:18.1f}")

smin,smax=min(pair_sigmas),max(pair_sigmas)
print(f"\nRe-pinned pair-sigma RANGE: {smin:.1f} .. {smax:.1f} uC/m^2")
print("(compare: silk-vs-gel pin was ~0-7 uC/m^2; bare-CE briefing rung 50-150.)")

# ===========================================================================
# Feed the re-pinned sigma into the SAME buildable-pulse test (decoupled from
# structure: sigma chosen freely). Q_pulse = sigma * A_geom * f_overlap.
# Pass target from gel T4: 1 fC; sub-fC floor 1e-16 C.
# ===========================================================================
Q_TARGET=1e-15; Q_SUBFC=1e-16
ribbons=[("micro 1um x0.1um",1e-13),("small 10um x1um",1e-11),
         ("mid 100um x10um",1e-9),("large 500um x50um",2.5e-8),
         ("max 1mm x100um",1e-7)]
f_overlap=[1e-3,1e-2,1e-1]
# use a representative re-pinned sigma band: conservative / central / optimistic
sigma_band={"conservative 2 uC/m2":2e-6,"central 8 uC/m2":8e-6,"optimistic 25 uC/m2":25e-6}

print("\n"+"="*86)
print("BUILDABLE PULSE with re-pinned sigma (structure decoupled, ideal conditions)")
print("cells: P>=1fC  ~>=0.1fC  x<0.1fC")
print("="*86)
any_pass=any_fail=False; cross_inside=False
for sname,s in sigma_band.items():
    print(f"\n--- sigma = {sname} ---")
    print(f"  {'ribbon':18s} | "+" | ".join(f"f={f:g}".rjust(11) for f in f_overlap))
    for rn,A in ribbons:
        cells=[]
        for f in f_overlap:
            Q=s*A*f
            if Q>=Q_TARGET: any_pass=True; cells.append(f"P {Q:.1e}")
            elif Q>=Q_SUBFC: cells.append(f"~ {Q:.1e}")
            else: any_fail=True; cells.append(f"x {Q:.1e}")
        print(f"  {rn:18s} | "+" | ".join(c.rjust(11) for c in cells))

# crossing locator at honest f=0.01 for the central sigma
print("\nCrossing (f=0.01): min A_geom to hit 1 fC, per re-pinned sigma:")
for sname,s in sigma_band.items():
    A_need=Q_TARGET/(s*0.01); side=np.sqrt(A_need)*1e6
    inside=1e-13<=A_need<=1e-7
    cross_inside|=inside
    tag="(within evolvable whip area)" if inside else "(needs whip bigger/smaller than swept -> flag)"
    print(f"  sigma={s*1e6:5.1f} uC/m2 -> A_need={A_need:.2e} m^2 (~{side:6.1f} um square) {tag}")

print("\n"+"="*86)
print("ANTI-ARTIFACT CHECK")
print(f"  some PASS: {any_pass} | some FAIL: {any_fail} | 1fC crossing inside swept area: {cross_inside}")
print("  GOOD (real boundary)" if (any_pass and any_fail and cross_inside)
      else "  WARNING: trivially pass/fail or off-edge -> revisit bounds")
print("="*86)
