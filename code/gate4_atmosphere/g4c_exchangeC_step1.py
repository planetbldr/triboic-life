#!/usr/bin/env python3
"""
GATE 4 - Exchange C, Step 1 (forward chemistry -> spectrograph target)
======================================================================
Sulfur/proton MAINTENANCE chemistry. The creature uses triboelectric
electrons to run a low-voltage sulfur redox idle. We CHOOSE the couple
(design phase left it functional, not specific) and justify the choice.

[SPEC-CHOICE] PRIMARY MAINTENANCE COUPLE: SO2 -> elemental sulfur (S0).
  The creature reduces SO2 (S^4+) toward S^0 using harvested electrons.
  Justification (canonized):
   (1) SO2 ~130 ppm is the most abundant reactive sulfur gas in the cloud
       deck - a maintenance idle should run on the most available substrate.
   (2) The organism is an electron PUMP; the natural maintenance sink is
       REDUCING an oxidized substrate. SO2->S0 is a 4-electron reduction at
       modest potential (fits the 0.3-0.93 V envelope, GATE3).
   (3) The product, elemental sulfur (S8/Sn), is a KNOWN Venus species and a
       leading UV-absorber suspect -> independently observable.
   (4) It runs COUNTER to the dominant abiotic OXIDATIVE cycle
       (SO2->SO3->H2SO4) -> a reductive sink is what could leave a
       distinguishable fingerprint.
  SECONDARY (carried, not run): sulfate/bisulfate -> sulfite reduction using
  the medium. Noted as alternative; not primary (substrate = solvent makes
  'consumption' ambiguous, and it is higher cost).

PURELY FORWARD. No comparison to known Venus data (Step 2). No kill-conditions.
Compute: bounded numpy. No DFT. Tags [LAB]/[SIM]/[SPEC]/[SPEC-CHOICE].
"""

import numpy as np

print("="*72)
print("GATE 4 - EXCHANGE C - STEP 1: sulfur maintenance  SO2 -> S0")
print("="*72)

# ===================================================================
# PART 1 - THE HALF-REACTION and per-creature consumption/excretion
# ===================================================================
print("\n" + "-"*72)
print("PART 1 - REACTION STOICHIOMETRY + per-creature sulfur turnover")
print("-"*72)
print("""  Chosen maintenance half-reaction (acid medium) [SPEC-CHOICE]:
     SO2 + 4 H+ + 4 e-  ->  S(0) + 2 H2O
  Consumes: SO2 (S^4+) + protons + 4 electrons per S atom.
  Excretes/produces: elemental sulfur S0 (-> Sn/S8) + water.
  This is the 'sulfur/proton chemistry' of GATE3 made specific: it consumes
  protons (acid) and SO2, produces S0 and H2O. [SPEC-CHOICE]
""")

# --- Anchored electrical input (GATE3 consolidation) ----------------
I_maint = 1e-16          # A per creature, maintenance current [SIM canon, GATE3]
e_charge = 1.602176634e-19
N_A = 6.02214076e23
n_e_per_S = 4            # electrons per SO2 reduced to S0

# electron flux -> mol SO2 reduced per second per creature
e_per_s = I_maint / e_charge                    # electrons/s
S_atoms_per_s = e_per_s / n_e_per_S             # S atoms (=SO2 consumed)/s
mol_SO2_per_s = S_atoms_per_s / N_A
mol_SO2_per_day = mol_SO2_per_s * 86400
# masses
M_SO2 = 64.07e-3   # kg/mol
M_S   = 32.06e-3   # kg/mol
kg_SO2_per_day = mol_SO2_per_day * M_SO2
kg_S_per_day   = mol_SO2_per_day * M_S          # 1 S0 per SO2

print(f"  maintenance current        : {I_maint:.1e} A  [SIM canon]")
print(f"  electrons/s                : {e_per_s:.3e}")
print(f"  SO2 consumed (=S0 made)    : {S_atoms_per_s:.3e} atoms/s")
print(f"                             : {mol_SO2_per_day:.3e} mol/day/creature")
print(f"  SO2 mass consumed          : {kg_SO2_per_day:.3e} kg/day ({kg_SO2_per_day*1e18:.3f} attogram/day)")
print(f"  S0 mass produced           : {kg_S_per_day:.3e} kg/day")

# ===================================================================
# PART 2 - SIZING THE SINK against the SO2 background
# ===================================================================
print("\n" + "-"*72)
print("PART 2 - DISTRIBUTED SINK vs SO2 BACKGROUND (how big a dent?)")
print("-"*72)

# Canonical cloud-deck SO2 [LAB]: ~130 ppm at/below cloud base (Bezard 1993);
# we use 130 ppm as the canonized cloud-deck value (GATE2 inventory).
SO2_ppm = 130.0
# Atmospheric number density at ~52 km: use P,T from GATE2 (P~0.5-1 atm, T~300-330K)
P_atm = 0.75 * 101325.0   # Pa [SIM mid]
T_K   = 315.0             # K  [SIM mid]
kB    = 1.380649e-23
n_air = P_atm/(kB*T_K)                  # molecules/m3 total
n_SO2 = n_air * SO2_ppm*1e-6            # SO2 molecules/m3
mol_SO2_per_m3 = n_SO2 / N_A
print(f"  cloud-deck SO2             : {SO2_ppm:.0f} ppm [LAB]")
print(f"  air number density (52 km) : {n_air:.3e} /m3  (P={P_atm/101325:.2f} atm, T={T_K:.0f} K)")
print(f"  SO2 number density         : {n_SO2:.3e} /m3 = {mol_SO2_per_m3:.3e} mol/m3")

# [SPEC-CHOICE] population band (same as Exchange A, carried):
pop_per_m3 = np.array([1e-3, 1e0, 1e2])
pop_lbl    = ["sparse(1e-3/m3)","moderate(1/m3)","bloom(1e2/m3)"]
print(f"\n  Consumption as fraction of local SO2 inventory PER DAY:")
print(f"  (population-scaled; the question: can the creature dent 130 ppm?)")
for L,p in zip(pop_lbl, pop_per_m3):
    consumed_mol_m3_day = mol_SO2_per_day * p
    frac_per_day = consumed_mol_m3_day / mol_SO2_per_m3
    # also a replenishment-free e-folding time
    if frac_per_day>0:
        tau_days = 1.0/frac_per_day
    else:
        tau_days = np.inf
    print(f"    {L:16s}: {consumed_mol_m3_day:.2e} mol/m3/day  = {frac_per_day:.2e} of SO2/day"
          f"  (depletion e-fold ~ {tau_days:.2e} day, no resupply)")

print("""
  Reading: maintenance sulfur turnover is TINY per creature (a maintenance
  IDLE, ~1e-16 A). Whether it dents the 130 ppm SO2 background depends
  entirely on population density (the [SPEC-CHOICE] band). The forward fact to
  canonize is the PER-CREATURE rate and the SCALING, not a verdict.
""")

# ===================================================================
# PART 3 - THE PRODUCT: elemental sulfur, allotrope & fate
# ===================================================================
print("-"*72)
print("PART 3 - PRODUCT FATE: elemental sulfur in the cloud deck")
print("-"*72)
print("""  S0 produced by the creature enters a medium that ALREADY hosts sulfur
  allotrope chemistry [LAB]:
   - At cloud-deck T (~300-330 K) elemental sulfur favors rings; S8 is the
     thermodynamic sink, with S3/S4 (the colored, UV-absorbing short chains)
     in temperature/▽-dependent equilibrium. [LAB]
   - Biologically-produced S0 would CONDENSE into / onto the aerosol or form
     colloidal sulfur (the classic 'biogenic sulfur' habit on Earth is fine
     colloidal S0 spheres from sulfur-oxidizing/reducing microbes). [LAB analog]
   - In concentrated H2SO4 the S0 can also re-enter the abiotic cycle
     (oxidation back toward SO2/sulfate on long timescales), so the creature
     is a LOCAL reductive shunt on a cycle that abiotically runs oxidative.

  Forward products to track:
   (i)  elemental sulfur S8 (and S3/S4/Sn) - itself a UV-absorber candidate
   (ii) the proton consumption (local, tiny acid neutralization)
   (iii) water co-product (negligible vs bulk)
""")

# ===================================================================
# PART 4 - PROBE TARGETS + the sulfur-isotope biosignature
# ===================================================================
print("-"*72)
print("PART 4 - PROBE TARGETS (incl. the classic S-isotope biosignature)")
print("-"*72)
print("""  C1. LOCAL SO2 DEPLETION + S0 ENHANCEMENT, CO-LOCATED.
      A reductive SO2->S0 sink predicts paired anomalies AT THE CREATURE
      LAYER (50-54 km): slightly depleted SO2 and enhanced elemental sulfur
      / colloidal S, co-located and possibly patchy with population.
      -> TARGET: correlated SO2-down / Sn-up at 50-54 km. (Magnitude is
      population-dependent; the CO-LOCATION/correlation is the signature.)

  C2. ELEMENTAL-SULFUR HABIT.
      Biogenic S0 on Earth is characteristically FINE COLLOIDAL SPHERES,
      distinct from abiotic condensation habits. -> TARGET: sulfur particle
      morphology/size distribution in the aerosol (a nephelometer/imaging
      target), not just bulk abundance.

  C3. SULFUR ISOTOPE FRACTIONATION  <-- the strongest discriminator.
      Biological sulfur redox on Earth fractionates 34S/32S: enzymatic
      reduction preferentially processes the lighter isotope, leaving product
      sulfur ISOTOPICALLY LIGHT (depleted in 34S) relative to substrate, by
      up to tens of per-mil. Abiotic photochemistry fractionates differently
      (and can show mass-INDEPENDENT signatures). -> TARGET: delta-34S of
      elemental sulfur vs SO2. A mass-spectrometer isotope-ratio measurement
      is the classic, hard-to-fake biosignature. (Direction: biogenic S0
      should be 34S-DEPLETED relative to source SO2 for reductive metabolism.)

  C4. PROTON / LOCAL ACIDITY MICRO-SINK.
      The half-reaction consumes 4 H+ per S. A distributed proton sink could
      very slightly RAISE local droplet pH where the population is dense.
      -> TARGET: droplet pH heterogeneity correlated with population (a VLF
      Mode-3 pH target). Weak/population-dependent; recorded for completeness.

  The headline discriminator is C3 (S-isotopes): independent of abundance,
  hard to mimic abiotically, and measurable by a descent mass spectrometer.
""")

print("="*72)
print("STEP 1 COMPLETE - Exchange C forward prediction generated.")
print("Canonize: the SO2->S0 [SPEC-CHOICE] couple + half-reaction; per-creature")
print("SO2/S0 turnover (Part 1); sink-vs-background scaling (Part 2); S0 fate")
print("(Part 3); probe targets C1-C4 with S-isotopes as headline (Part 4).")
print("Step 2 compares dispassionately to today's limited Venus data.")
print("="*72)
