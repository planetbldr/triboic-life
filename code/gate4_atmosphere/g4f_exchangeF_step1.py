#!/usr/bin/env python3
"""
GATE 4 - Exchange F, Step 1 (forward chemistry -> spectrograph target)
======================================================================
PREDATOR EXCREMENT chemistry. A predator eats the creature, absorbs the
usable fraction, excretes the rest. We predict ONLY the excrement chemistry.
NO other claim about the predator (metabolism, body, biochemistry) is made.

The ONE assumed principle [SPEC-CHOICE]:
  Predators concentrate the LEAST-DIGESTIBLE fraction. Whatever the predator's
  metabolism, the material surviving passage is the fraction most resistant to
  being broken down/absorbed. So excrement is ENRICHED in recalcitrant prey
  components and DEPLETED in labile/nutritive ones. Nothing else is assumed.

Recalcitrance ranking [SPEC-CHOICE], anchored to the project's established
material chemistry (acid/enzymatic resistance as the proxy for digestive
resistance - the only anchor available):
  MOST recalcitrant (CONCENTRATES): sporopollenin coat - established resistant
    to enzymatic digestion + fossil-preserved 10^8 yr [LAB qualitative]; its
    C-C aromatic bonds 'most resistant, not hydrolyzable' (coating report).
    Already-charred/sulfonated shed fraction (Exchange A) is even more inert.
  INTERMEDIATE: silk (resistant peptides Gly-Gly/His-His persist; rest cleaves),
    cellulose/alginate (dehydrates to char).
  MOST labile (DEPLETES - predator absorbs): quinone redox gel (metabolically
    VALUABLE - a predator would harvest it), interior biomolecules (nucleobases,
    amino acids, lipids = the nutritive fraction), soluble small molecules.

CONTRAST WITH A & E: those were DIRECT shedding (raw material). F is PROCESSED:
same starting inventory minus the labile/nutritive fraction, further condensed
by digestion + acid. => a haze-organic sub-population that is N-DEPLETED,
quinone-depleted, MORE charred/aromatic, enriched in sporopollenin residue.
The SIGNATURE is the DIFFERENCE from direct shed - a processing GRADIENT.

PURELY FORWARD. No comparison to known Venus data (Step 2). No kill-conditions.
Compute: bounded numpy. No DFT. Tags [LAB]/[SIM]/[SPEC]/[SPEC-CHOICE].
"""

import numpy as np

print("="*72)
print("GATE 4 - EXCHANGE F - STEP 1: predator excrement = recalcitrant residue")
print("="*72)

# ===================================================================
# PART 1 - THE RECALCITRANCE LEDGER: what concentrates vs depletes
# ===================================================================
print("\n" + "-"*72)
print("PART 1 - RECALCITRANCE LEDGER (digestive assimilation by component)")
print("-"*72)

# Prey whole-body composition (reuse Exchange E cell split + add coating).
# Exchange E cell split was: silk 0.40, polysacc 0.25, quinone 0.20, interior 0.15
# Here we include the SPOROPOLLENIN COATING as part of the whole prey body.
# [SPEC-CHOICE] whole-prey mass split including coat:
prey = {
  "sporopollenin_coat": 0.30,   # the resistant barrier (whips+body coat)
  "silk_protein":       0.28,   # structure, N-bearing
  "polysaccharide":     0.17,   # cellulose/alginate skins
  "quinone_gel":        0.14,   # redox core - nutritive
  "interior_biomol":    0.11,   # nucleobases/AA/lipids - nutritive, N-bearing
}
# [SPEC-CHOICE] DIGESTIVE ASSIMILATION fraction per component (fraction the
#   predator ABSORBS; 1 - this = fraction EXCRETED). Ranked by recalcitrance.
#   These are bounded SPEC values; only the RANKING is load-bearing.
assim = {
  "sporopollenin_coat": 0.05,   # almost indigestible -> excreted
  "silk_protein":       0.45,   # partly digestible (labile peptides), resistant rest
  "polysaccharide":     0.40,   # partly (char-prone)
  "quinone_gel":        0.90,   # valuable redox cofactor -> harvested
  "interior_biomol":    0.92,   # nutritive -> harvested
}
# N content by mass per component (from Exchange E):
Nfrac = {"sporopollenin_coat":0.0, "silk_protein":0.16, "polysaccharide":0.0,
         "quinone_gel":0.0, "interior_biomol":0.20}

# Compute excreted composition
excr_mass = {k: prey[k]*(1-assim[k]) for k in prey}
excr_total = sum(excr_mass.values())
excr_frac  = {k: excr_mass[k]/excr_total for k in prey}

print(f"  {'component':20s} {'in prey':>8s} {'assim':>6s} {'excreted':>9s} {'excr frac':>10s}")
for k in prey:
    print(f"  {k:20s} {prey[k]:8.2f} {assim[k]:6.2f} {excr_mass[k]:9.3f} {excr_frac[k]:10.3f}")
print(f"  {'TOTAL excreted':20s} {'':8s} {'':6s} {excr_total:9.3f} {1.0:10.3f}")
print(f"\n  => excrement is {excr_total*100:.0f}% of ingested mass (predator absorbs the rest)")

# ===================================================================
# PART 2 - THE COMPOSITION SHIFT vs DIRECT SHED (the signature)
# ===================================================================
print("\n" + "-"*72)
print("PART 2 - COMPOSITION SHIFT: excrement vs direct shed (A/E)")
print("-"*72)

# Nitrogen content of direct-shed cell material (Exchange E) vs excrement:
N_in_prey = sum(prey[k]*Nfrac[k] for k in prey)
N_in_excr = sum(excr_frac[k]*Nfrac[k] for k in prey)
# quinone fraction:
q_in_prey = prey["quinone_gel"]
q_in_excr = excr_frac["quinone_gel"]
# sporopollenin (recalcitrant char precursor) fraction:
s_in_prey = prey["sporopollenin_coat"]
s_in_excr = excr_frac["sporopollenin_coat"]

print(f"  Nitrogen content:   prey body {N_in_prey*100:5.1f}%  ->  excrement {N_in_excr*100:5.1f}%"
      f"   ({'DEPLETED' if N_in_excr<N_in_prey else 'enriched'})")
print(f"  Quinone fraction:   prey body {q_in_prey*100:5.1f}%  ->  excrement {q_in_excr*100:5.1f}%"
      f"   ({'DEPLETED' if q_in_excr<q_in_prey else 'enriched'})")
print(f"  Sporopollenin frac: prey body {s_in_prey*100:5.1f}%  ->  excrement {s_in_excr*100:5.1f}%"
      f"   ({'ENRICHED' if s_in_excr>s_in_prey else 'depleted'})")
print(f"""
  => The excrement is quinone-DEPLETED (~5.6x down) and sporopollenin-ENRICHED
     relative to the whole prey (and to Exchange E direct cell-shed). Nitrogen
     is only MILDLY depleted (6.7->4.7%) because silk protein is both N-bearing
     AND only partly digestible, so resistant-peptide N rides along - the
     cleaner markers are the QUINONE loss, the SPOROPOLLENIN enrichment, and the
     CHANGE IN N FORM (labile nucleobase N removed, resistant-peptide N kept;
     see F2), not the raw N quantity. Combined with digestion + acid
     condensation, the residue sits FURTHER along the charring/aromatic
     (red-oil) axis than direct shed.
""")

# ===================================================================
# PART 3 - PRODUCT SLATE + optical/mass consequence
# ===================================================================
print("-"*72)
print("PART 3 - EXCREMENT PRODUCT SLATE and its spectral consequence")
print("-"*72)
print("""  The excreted residue is dominated by:
   (i)  sporopollenin-derived recalcitrant char (aromatic C-C, sulfonated
        rings) - the most condensed end of the red-oil axis.
   (ii) resistant peptide relics (Gly-Gly/His-His class) - a SMALL surviving
        N pool (so excrement is N-poor but not N-zero; the N that remains is
        the MOST acid/digestion-resistant N, not the labile nucleobase N).
   (iii) polysaccharide char.
  Depleted/absent: quinone redox chromophore, nucleobase N-heterocycles, free
  amino acids, lipids (the predator took these).

  Optical/mass consequence [reuses A optics; SIM/LAB]:
   - MORE charring/condensation -> chromophore population shifted toward the
     LONGER-conjugation / saturated-blue end (Exchange A's ~450-580 nm edge,
     but weighted redder/more-aromatic than fresh shed).
   - LOSS of the Exchange-E molecular markers: the discrete nucleobase masses
     (135/151/111/112/126 Da) and the quinone bands are SUPPRESSED in excrement.
   - So excrement looks like 'aged/processed red oil' - optically near abiotic
     red oil but reachable, in the same haze, alongside the fresher A/E shed.
""")

# ===================================================================
# PART 4 - PROBE TARGETS: the processing-GRADIENT signature
# ===================================================================
print("-"*72)
print("PART 4 - PROBE TARGETS (the differential / trophic signature)")
print("-"*72)
print("""  F1. TWO CO-EXISTING ORGANIC POPULATIONS (the headline).
      A food web predicts a PAIRED set in the same haze: (a) fresher direct-
      shed organics (A/E) carrying N-heterocycles + quinone, AND (b) more-
      processed excrement residue that is N-depleted, quinone-free, more
      charred. -> TARGET: a BIMODAL / graded organic population - some
      particles molecularly rich (discrete N masses), others condensed/charred
      - co-located. Abiotic chemistry has no reason to produce a PAIR of
      populations related by a digestion-like processing step.

  F2. SELECTIVE NITROGEN DEPLETION WITH RESISTANT-N RESIDUE.
      Excrement keeps only the MOST resistant N (Gly-Gly/His-His-class peptide
      relics), not labile nucleobase N. -> TARGET: an N-poor organic particle
      whose residual N is in resistant-peptide form, not nucleobase form - a
      processed-N fingerprint distinct from both fresh shed and abiotic.

  F3. DOUBLE ISOTOPIC FRACTIONATION.
      A second trophic level adds another biological fractionation step. Earth
      food webs show stepwise isotope shifts per trophic level (e.g. ~+3-4 per
      mil delta-15N enrichment per level; characteristic delta-13C shifts).
      -> TARGET: excrement organic carbon/nitrogen isotopically OFFSET from the
      direct-shed organic pool (not just from the CO2/N source). Two organic
      pools with a SYSTEMATIC isotopic offset between them = a trophic ladder
      signature, abundance-independent and hard to mimic abiotically.
      (N isotopes especially: a 15N pattern across two organic pools.)

  F4. ENRICHED RECALCITRANT CHAR PARTICLES.
      The sporopollenin-derived residue is the haze's most condensed, most
      sulfonated organic particle. -> TARGET: a population of highly aromatic,
      sulfonated, N-poor char particles distinct from the fresher shed - the
      'fecal' end member of the organic size/composition distribution.

  Headline: F1 + F3 - the existence of TWO related organic populations (fresh
  shed vs processed excrement) with a systematic compositional AND isotopic
  offset between them. A single processing gradient across the haze organics is
  the trophic-web signature; no single abiotic process makes a matched pair.
""")

print("="*72)
print("STEP 1 COMPLETE - Exchange F forward prediction generated.")
print("Canonize: recalcitrance ledger [SPEC-CHOICE] (Part1); N/quinone-depleted,")
print("sporopollenin-enriched excrement composition (Part2); aged-red-oil slate")
print("(Part3); targets F1-F4, headline = paired-population processing gradient +")
print("double isotopic offset (Part4). Step 2 compares to today's limited data.")
print("="*72)
