#!/usr/bin/env python3
"""
Gate 3b — LEDGER v2: growth inequality with honest overhead costs (CORRECTED).

Refines the Gate 2 aggregation ledger by adding three previously un-costed
overhead terms, then re-runs the knife-edge.

CORRECTION (important, vs first draft): anchoring is NOT a continuous F*v power
drain. A static anchor bearing a steady drag force does ~zero work (no
displacement); the wind's work goes into FLUTTER, which is harvested, not spent.
Anchoring cost is therefore (a) a one-time build cost (anchor strong enough to
bear the drag force -- folded into build cost) plus (b) a small anchor-repair
maintenance term. The first draft wrongly charged F*v continuously and got an
artifact NET-negative by ~1e9%. Fixed here.

THREE OVERHEADS (all turn out comparable, ~1e-13 W):
  (1) POWER-CONDITIONING -- near-zero: smoothing is PASSIVE (phase-stagger
      desync array + gel buffer; no active rectifier). Only residual gel upkeep.
  (2) ANCHORING -- small repair term (static anchors do no work).
  (3) PASSIVE-RIBBON REPAIR -- replaces the Gate-2b axoneme over-estimate;
      a passive ribbon has no motors/IFT, so far cheaper.

RESULT: the three sum to ~the same order as P_chem -> growth sits on a genuine
KNIFE-EDGE (~ -17% at central assumptions, flips NET+ in the favorable corner:
slower turnover, more-hollow whips, lower gel leakage). Honest verdict: growth
feasible but tight; triboic life runs at its energetic limit. [SIM; SPEC inputs]
"""
import numpy as np

e_charge = 1.602e-19
J_ATP = 5e-20
DAY = 86400.0

print("="*74)
print("Gate 3b LEDGER v2 (corrected) — growth inequality with honest overheads")
print("="*74)

# ---- canonical anchors ----
I_growth = 1.6e-12; V_drive = 1.0
P_chem = I_growth * V_drive
N_whip = 1.6e3
print(f"\nAnchors: P_chem(growth)={P_chem:.2e} W, array N={N_whip:.0e}")

# ---- shared build-cost basis (1% solid whip, the viable case) ----
whip_mass = 1e-3*1e-5*1e-7*0.01*1200
n_mono = whip_mass/(150*1.66e-27)
E_build_whip = n_mono*2*J_ATP   # 2 ATP/monomer, polysaccharide-class

# (1) conditioning -- gel upkeep leakage, near-zero
print("\n[1] POWER-CONDITIONING (passive smoothing; only gel upkeep)")
gel_leak_frac = 0.05
P_cond = gel_leak_frac*P_chem
print(f"    phase-stagger free; gel built. Upkeep <= {gel_leak_frac*100:.0f}% P_chem")
print(f"    P_cond = {P_cond:.2e} W  (NEAR-ZERO)")

# (2) anchoring -- static anchor does no work; small repair only
print("\n[2] ANCHORING (static anchor does no work -> repair term only)")
rho_air=1.0; Cd=1.5; A_face=1.5e-3*1e-5
F_drag_gust = 0.5*rho_air*67**2*Cd*A_face
A_anchor = F_drag_gust/5e7   # cross-section at 5e7 Pa yield
E_build_anchor = (A_anchor*1e-5*1200)/(150*1.66e-27)*2*J_ATP
anchor_turnover = 0.01       # 1%/day anchor repair
P_anchor = N_whip*anchor_turnover*E_build_anchor/DAY
print(f"    static drag force/whip (67 m/s gust) = {F_drag_gust:.2e} N (borne, no work)")
print(f"    anchor build/whip = {E_build_anchor:.2e} J; repair {anchor_turnover*100:.0f}%/day")
print(f"    P_anchor = {P_anchor:.2e} W")
print(f"    (a PINNED creature in 67 m/s would spend ~{N_whip*F_drag_gust*67:.1e} W")
print(f"     -- catastrophic. Passive drift is load-bearing for viability.)")

# (3) passive-ribbon repair
print("\n[3] PASSIVE-RIBBON REPAIR (no motors/IFT; replaces axoneme estimate)")
ribbon_turnover = 0.01       # 1%/day, ~100-day ribbon life
P_repair = N_whip*ribbon_turnover*E_build_whip/DAY
print(f"    whip build = {E_build_whip:.2e} J; repair {ribbon_turnover*100:.0f}%/day")
print(f"    P_repair = {P_repair:.2e} W")

# ---- knife-edge ----
print("\n" + "="*74)
print("KNIFE-EDGE RE-RUN")
print("="*74)
P_over = P_cond + P_anchor + P_repair
net = P_chem - P_over
print(f"  P_chem (growth)       = {P_chem:+.2e} W")
print(f"  - conditioning        = {P_cond:.2e} W")
print(f"  - anchoring (repair)  = {P_anchor:.2e} W")
print(f"  - ribbon repair       = {P_repair:.2e} W")
print(f"  {'-'*40}")
print(f"  NET                   = {net:+.2e} W   margin {net/P_chem*100:+.0f}%  "
      f"[{'NET+' if net>0 else 'NET-'}]")

# favorable-corner sensitivity
print("\n  Favorable-corner sensitivity (which way does it flip?):")
for label, gl, at, rt in [("central", 0.05, 0.01, 0.01),
                          ("durable whips (0.3%/day)", 0.05, 0.003, 0.003),
                          ("low leak + durable", 0.01, 0.003, 0.003),
                          ("pessimistic (3%/day)", 0.05, 0.03, 0.03)]:
    pc = gl*P_chem
    pa = N_whip*at*E_build_anchor/DAY
    pr = N_whip*rt*E_build_whip/DAY
    nn = P_chem-(pc+pa+pr)
    print(f"    {label:28s}: NET={nn:+.2e} W  {'NET+' if nn>0 else 'NET-'}")

print("\n" + "="*74)
print("VERDICT (honest):")
print("  Growth sits on a GENUINE KNIFE-EDGE once honest overheads are included.")
print("  At central assumptions it is marginally NET-negative (~ -17%); it flips")
print("  NET-POSITIVE in the favorable (and independently-required) corner of")
print("  durable, mostly-hollow whips with low gel leakage. The un-costed")
print("  overheads were REAL and consume most of the Gate-2 margin.")
print("  => Triboic GROWTH is feasible but runs AT its energetic limit. The")
print("     binding term remains whip DURABILITY (slower turnover = the whole")
print("     ledger closes), tying Gate 3b back to the Gate 2b/3a durability question.")
print("  Conditioning ~0 (passive smoothing) and anchoring ~small (passive drift,")
print("  static anchors) are both consequences of the creature's PASSIVE design --")
print("  the fluffball-drifting-with-the-wind morphology is what keeps overheads low.")
print("="*74)
