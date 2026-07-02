#!/usr/bin/env python3
"""
GATE 4 - Exchange B, Step 1 (forward chemistry -> spectrograph target)
======================================================================
CO2-FIXATION growth metabolism. The creature fixes CO2 (growth, ~1e-12 A,
full whip array). Two outputs: (a) CO2 draw-down itself; (b) the LEAK/waste
products of the fixation pathway. Design phase PARKED the detailed pathway,
so we CHOOSE it and justify the choice.

[SPEC-CHOICE] PRIMARY FIXATION PATHWAY: Wood-Ljungdahl (reductive acetyl-CoA).
  CO2 --> CO --> formyl --> ... --> acetyl-CoA --> acetate.
  Justification (canonized):
   (1) Lowest ATP-cost C-fixation known -> fits an organism GATE3 showed runs
       at its energetic LIMIT (Calvin is ATP-expensive by comparison).
   (2) Native to acetogens living on ELECTRONS + CO2, no O2 -> matches the
       Bose/Guzman electrotrophy anchor and the anaerobic cloud deck.
   (3) Leak/intermediate slate is SPECIFIC and VOLATILE: CO and formate/
       formic acid (intermediates), acetate/acetic acid (end-product overflow)
       -> CO and OCS are already tracked Venus species, so CO is probe-measured.
   (4) Lands in Spacek&Benner's demonstrated acid carbon chemistry (formate/
       formaldehyde/glycolic acid in conc. H2SO4) -> clean biotic-vs-abiotic Q.
  ALTERNATIVE (carried, not run): Calvin cycle (RuBisCO, Guzman 2019 anchor).
  Noted; not primary (higher ATP cost, less fitting an energy-limited cell).

PURELY FORWARD. No comparison to known Venus data (Step 2). No kill-conditions.
Compute: bounded numpy. No DFT. Tags [LAB]/[SIM]/[SPEC]/[SPEC-CHOICE].
"""

import numpy as np

print("="*72)
print("GATE 4 - EXCHANGE B - STEP 1: CO2 fixation leak products (Wood-Ljungdahl)")
print("="*72)

# constants
e_charge = 1.602176634e-19
N_A = 6.02214076e23

# ===================================================================
# PART 1 - CO2 DRAW-DOWN: on the record, then set aside
# ===================================================================
print("\n" + "-"*72)
print("PART 1 - CO2 DRAW-DOWN (quantify, confirm negligible, set aside)")
print("-"*72)

I_growth = 1e-12     # A per creature, growth current [SIM canon, GATE3]
# Wood-Ljungdahl net: 2 CO2 + 8 H+ + 8 e- -> CH3COOH (acetate) + 2 H2O
#   i.e. 8 electrons per acetate, fixing 2 carbons. electrons per C fixed = 4.
n_e_per_C = 4
e_per_s = I_growth/e_charge
C_fixed_per_s = e_per_s/n_e_per_C          # carbon atoms fixed/s (=CO2 consumed)
mol_CO2_per_s = C_fixed_per_s/N_A
mol_CO2_per_day = mol_CO2_per_s*86400
M_CO2 = 44.01e-3
kg_CO2_per_day = mol_CO2_per_day*M_CO2

# background CO2 at 52 km
P_atm = 0.75*101325.0; T_K=315.0; kB=1.380649e-23
n_air = P_atm/(kB*T_K)
n_CO2 = n_air*0.965
mol_CO2_per_m3 = n_CO2/N_A

print(f"  growth current             : {I_growth:.1e} A [SIM canon]")
print(f"  CO2 fixed per creature     : {mol_CO2_per_day:.3e} mol/day ({kg_CO2_per_day*1e15:.3f} femtogram/day)")
print(f"  background CO2 (96.5%)      : {mol_CO2_per_m3:.3e} mol/m3")
pop = np.array([1e-3,1e0,1e2]); poplbl=["sparse","moderate","bloom"]
for L,p in zip(poplbl,pop):
    frac = mol_CO2_per_day*p/mol_CO2_per_m3
    print(f"    {L:9s} ({p:.0e}/m3): draws down {frac:.2e} of local CO2 / day")
print("""  => CO2 draw-down is utterly negligible against a 96.5% reservoir at every
  population. CONFIRMED non-signal. Set aside; the signature is the LEAK slate.
""")

# ===================================================================
# PART 2 - THE LEAK SLATE: CO, formate, acetate production rates
# ===================================================================
print("-"*72)
print("PART 2 - LEAK / EXCRETION SLATE (Wood-Ljungdahl intermediates + overflow)")
print("-"*72)
print("""  Wood-Ljungdahl carbon flow and where each leak comes from:
    CO2 -> [CO]  (carbonyl branch; CO is a bound intermediate that can LEAK)
    CO2 -> formate (HCOO-) -> formyl-... (methyl branch; formate can LEAK)
    methyl + CO + CoA -> acetyl-CoA -> ACETATE (end product; OVERFLOW excretion)
  We assign [SPEC-CHOICE] leak fractions of the fixed-carbon flux:
    CO leak     : 1% of C flux   (tight intermediate, small leak)
    formate leak: 2% of C flux   (soluble, more leak-prone in acid)
    acetate     : 5% of C flux   (overflow metabolism excretion)
  Rationale: real cells leak/overflow a few % of throughput; exact values are
  unpinnable, carried as an explicit small band. The DISCRIMINATOR (Part 4)
  does not depend on the precise %.
""")

leak_frac = {"CO":0.01, "formate":0.02, "acetate":0.05}
# molar carbon flux per creature (atoms C/s -> mol C/day)
mol_C_per_day = C_fixed_per_s/N_A*86400
M = {"CO":28.01e-3, "formate":46.03e-3, "acetate":60.05e-3}  # HCOOH, CH3COOH masses
C_in = {"CO":1, "formate":1, "acetate":2}   # carbons per molecule

print("  Per-creature leak production:")
prod_mol_day = {}
for sp,fr in leak_frac.items():
    mol_sp_day = (mol_C_per_day*fr)/C_in[sp]   # divide by C per molecule
    prod_mol_day[sp]=mol_sp_day
    print(f"    {sp:8s}: {mol_sp_day:.3e} mol/day ({mol_sp_day*M[sp]*1e15:.3f} fg/day)")

# ===================================================================
# PART 3 - ATMOSPHERIC ROUTING of each leak
# ===================================================================
print("\n" + "-"*72)
print("PART 3 - ATMOSPHERIC ROUTING (fate of each leak in the cloud deck)")
print("-"*72)

# CO vs background CO (~70 ppm canon)
CO_ppm = 70.0
n_CO = n_air*CO_ppm*1e-6
mol_CO_per_m3 = n_CO/N_A
print(f"  CO background ~{CO_ppm:.0f} ppm = {mol_CO_per_m3:.3e} mol/m3 [LAB]")
print(f"  CO atmospheric lifetime ~10-100 days [LAB]; photochem source CO2+hv.")
for L,p in zip(poplbl,pop):
    co_src = prod_mol_day["CO"]*p   # mol/m3/day added
    frac = co_src/mol_CO_per_m3
    print(f"    {L:9s}: CO leak adds {co_src:.2e} mol/m3/day = {frac:.2e} of CO/day")
print("""    => CO leak is tiny vs the 70 ppm CO pool AND vs its large photochemical
       source/sink (10-100 day turnover). Not a bulk CO perturbation.

  formate / acetic acid routing [LAB class, Spacek&Benner]:
    - Both are carboxylic acids; in concentrated H2SO4 they PARTITION INTO the
      acid droplets (low volatility as neutral acids; protonated/associated in
      the acid). Formic acid can dehydrate (-> CO + H2O) under strong acid;
      acetic acid is more resistant.
    - This lands them in EXACTLY the Spacek demonstrated regime (formate/
      formaldehyde/glycolic-acid chemistry stable for days in conc. acid).
    => the carboxylic-acid leak is a DROPLET-PHASE organic-carbon signal,
       not a gas-phase one - parallels Exchange A/E droplet organics.
""")

# ===================================================================
# PART 4 - PROBE TARGETS + the 13C biosignature angle
# ===================================================================
print("-"*72)
print("PART 4 - PROBE TARGETS (incl. 13C fractionation, parallel to C's 34S)")
print("-"*72)
print("""  B1. DROPLET-PHASE LIGHT CARBOXYLIC ACIDS (formate + acetate).
      A reductive acetyl-CoA pathway excretes ACETATE and leaks FORMATE into
      the droplets. -> TARGET: formic + acetic acid (and acetate ion) in the
      cloud aerosol, by aerosol/descent mass spec. A SPECIFIC small-acid slate
      (C1 + C2 acids) is more diagnostic than 'organics present'. Note the
      acetate:formate ratio is set by pathway overflow, a structured marker.

  B2. CO CO-LOCATED MICRO-ENHANCEMENT.
      CO leak is tiny vs the 70 ppm pool, but is CO-LOCATED with population and
      with the carboxylic-acid signal. -> TARGET: CO not as a bulk anomaly but
      as a weak correlate of the droplet-acid signal. (Low priority; CO pool
      and photochemistry dominate.)

  B3. CARBON-ISOTOPE FRACTIONATION (13C/12C)  <- headline, parallels C3(34S).
      Wood-Ljungdahl is the MOST strongly 13C-fractionating carbon-fixation
      pathway known on Earth: acetogens via WL produce biomass/acetate strongly
      DEPLETED in 13C (large negative delta-13C, tens of per-mil) relative to
      source CO2. Abiotic CO2 chemistry fractionates far less. -> TARGET:
      delta-13C of droplet acetate/formate (and of CO) vs the CO2 reservoir.
      A strongly 13C-light organic carbon pool is a classic biosignature and is
      measurable by descent mass spectrometry. (Direction: WL products 13C-LIGHT.)

  B4. THE ACID SLATE vs ABIOTIC SPACEK PRODUCTS.
      Abiotic acid chemistry (Spacek) makes glycolic acid from HCHO+CO. A
      WL-excreting cell makes ACETATE + FORMATE preferentially. -> TARGET: the
      RELATIVE abundances of acetate vs glycolate vs formate - a pathway
      fingerprint distinguishing reductive-acetyl-CoA overflow from abiotic
      formose-type chemistry.

  Headline: B3 (13C depletion). Like C3 for sulfur, it is abundance-independent,
  hard to mimic abiotically, and matched to descent mass-spec isotope capability.
""")

print("="*72)
print("STEP 1 COMPLETE - Exchange B forward prediction generated.")
print("Canonize: Wood-Ljungdahl [SPEC-CHOICE]; CO2 draw-down = non-signal (Part1);")
print("leak slate CO/formate/acetate (Part2); droplet-acid routing (Part3);")
print("targets B1-B4 with 13C depletion as headline (Part4).")
print("Step 2 compares dispassionately to today's limited Venus data.")
print("="*72)
