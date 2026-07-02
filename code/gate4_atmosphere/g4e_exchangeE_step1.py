#!/usr/bin/env python3
"""
GATE 4 - Exchange E, Step 1 (forward chemistry -> spectrograph target)
======================================================================
Central-body CELL shedding/lysis -> release of the cell structural +
interior inventory into H2SO4 droplets -> what forms, what a probe sees.

KEY CONTRAST WITH EXCHANGE A:
  A shed the COATING only: a phenolic/aliphatic crosslinked network = C/H/O.
  E sheds WHOLE CELLS: adds (1) NITROGEN (nucleobases, amino-acid backbones)
  and (2) redox-active QUINONE. Both are chemically distinct routes with
  distinct products and distinct spectral signatures. Nitrogen-bearing
  organics are the central new discriminator (abiotic Venus red oil is
  C/H/O/S, not N-rich).

PURELY FORWARD. No comparison to known Venus data (that is Step 2).
No kill-conditions. Output = a probe target list.

Compute: bounded numpy. Reuses Exchange A optics. No DFT (compute wall).
Tags: [LAB] literature, [SIM] computed, [SPEC] reasoned, [SPEC-CHOICE] a
chemistry choice this gate makes + justifies.
"""

import numpy as np

print("="*72)
print("GATE 4 - EXCHANGE E - STEP 1: cell shedding -> N + quinone channels")
print("="*72)

# ===================================================================
# PART 1 - SOURCE TERM: how much cell mass sheds, of what composition
# ===================================================================
print("\n" + "-"*72)
print("PART 1 - SOURCE TERM (cell mass shed/lysed, by component)")
print("-"*72)

# --- Anchored geometry (canonized, GATE3 consolidation) -------------
# Body: ~0.5-1.0 mm fluffball, ~1-50 cells. Take the body as the cell mass
# reservoir. Estimate body solid mass from a bounded volume * fill * density.
body_diam_m   = 0.75e-3        # [LAB/SIM canon] mid of 0.5-1.0 mm
body_radius_m = body_diam_m/2
body_vol_m3   = (4/3)*np.pi*body_radius_m**3

# [SPEC-CHOICE] solid volume fraction of the fluffball.
#   A "fluffball" is mostly void/whip array, not solid. Take solid fraction
#   0.05 (5%) as central, band 0.01-0.20. Rationale: the morphology is an
#   open aggregate of thin ribbons + sparse cell bodies; most of the envelope
#   is gas/acid space, so solid fill is low. Carried as explicit band.
solid_frac = np.array([0.01, 0.05, 0.20])
solid_lbl  = ["fluffy(1%)","central(5%)","dense(20%)"]

# [SPEC-CHOICE] mean condensed-organic density ~1.3 g/cm3.
#   Justification: silk ~1.3, cellulose ~1.5, quinone gel ~1.1-1.3,
#   sporopollenin 1.4 -> a mixed-organic mean ~1.3e3 kg/m3 is defensible.
rho_cell = 1.3e3   # kg/m3 [SPEC]

body_solid_mass = body_vol_m3 * solid_frac * rho_cell
print(f"  body volume (0.75 mm sphere): {body_vol_m3:.3e} m^3")
for L,f,m in zip(solid_lbl, solid_frac, body_solid_mass):
    print(f"    solid frac {L:12s}: cell solid mass = {m:.3e} kg ({m*1e9:.2f} ng)")

# --- Composition split of the shed CELL material -------------------
# [SPEC-CHOICE] mass fractions of the shed cell inventory.
#   The whips (sporopollenin coat etc.) are Exchange A; here we count the
#   CELL BODY material that is NOT the whip coat. Defensible split:
#     silk fibroin (structure)        0.40   <- protein, N-bearing
#     cellulose-ether/alginate skin   0.25   <- polysaccharide, C/H/O
#     quinone redox gel               0.20   <- redox chromophore
#     cell interior biomolecules      0.15   <- nucleobases/amino acids/lipids,
#                                                the most N-rich, most labile
#   Rationale: structure dominates by mass (silk load-bearing); interior
#   biomolecule pool is small but carries the strongest N signal. Bounded;
#   the DISCRIMINATORS do not depend on the exact split, only on N and quinone
#   being present at all.
frac = {"silk_protein":0.40, "polysaccharide":0.25, "quinone_gel":0.20, "interior_biomol":0.15}
print("\n  [SPEC-CHOICE] shed cell-material composition (mass fraction):")
for k,v in frac.items():
    print(f"    {k:18s}: {v:.2f}")

# Nitrogen-bearing fraction (the discriminator-relevant mass):
#   silk protein: ~N from peptide backbone; protein is ~16% N by mass [LAB].
#   interior biomol: nucleobases ~ up to ~5 N per base, amino acids N-bearing;
#     take interior pool as ~20% N by mass [SPEC, high-N pool].
#   polysaccharide + quinone: ~0% N.
N_massfrac_in = {"silk_protein":0.16, "interior_biomol":0.20, "polysaccharide":0.0, "quinone_gel":0.0}
def N_fraction_of_cell():
    return sum(frac[k]*N_massfrac_in[k] for k in frac)
print(f"\n  => Nitrogen content of shed cell material ~ {N_fraction_of_cell()*100:.1f}% by mass [SPEC]")
print(f"     (vs Exchange A coating: ~0% N - this is the key compositional contrast)")

# --- Shed RATE: cell turnover / lysis ------------------------------
# [SPEC-CHOICE] cell shedding/lysis rate. GATE3 PARKED reproduction & life
#   cycle entirely, so no design number exists. We bound it by analogy to
#   the whip turnover band (0.3-3%/day) since cells and whips are renewed by
#   the same starved metabolism; central 1%/day. Carried as the dominant
#   rate uncertainty, explicit and isolated. Linear scale on all fluxes.
cell_turnover = np.array([0.003, 0.01, 0.03])
turn_lbl      = ["durable(0.3%/d)","central(1%/d)","high(3%/d)"]

# Use central solid fraction (5%) for the headline flux; band reported.
m_cell_central = body_vol_m3 * 0.05 * rho_cell
print(f"\n  Shed cell mass flux per creature (central solid frac 5%):")
for L,t in zip(turn_lbl, cell_turnover):
    q = m_cell_central * t
    print(f"    {L:16s}: {q:.3e} kg/day ({q*1e9:.3f} ng/day total cell material)")
    qN = q * N_fraction_of_cell()
    print(f"         of which nitrogen-bearing organic flux: {qN*1e9:.4f} ng/day")

# ===================================================================
# PART 2 - PRODUCT CHEMISTRY: four parallel acid-fate channels
# ===================================================================
print("\n" + "-"*72)
print("PART 2 - PRODUCT CHEMISTRY (four parallel channels in conc. H2SO4)")
print("-"*72)
print("""  CHANNEL 1 - SILK (protein) [LAB anchor: Seager peptide-stability]
    In conc. H2SO4 most peptide bonds solvolyze over weeks (sequence-
    dependent; Gly-Gly, His-His persist months). Products: released
    amino-acid backbones (Seager: 19/20 backbones ENDURE; side chains may
    sulfonate/modify) + short resistant peptides. NET: a pool of N-bearing
    small molecules (amino acids) + sulfonated aromatic side chains
    (Phe/Tyr/Trp -> sulfonated/charred). KEEPS NITROGEN in solution.

  CHANNEL 2 - POLYSACCHARIDE (cellulose ether / alginate) [LAB class]
    Classic H2SO4-on-sugar: dehydration -> furfural / 5-HMF -> further
    condensation/carbonization ("sugar char"). C/H/O only. Feeds the SAME
    conjugated-carbon / red-oil pool as Exchange A's charring channel.
    -> overlaps Exchange A optically; not a new discriminator by itself.

  CHANNEL 3 - QUINONE redox gel [LAB: quinones are redox chromophores]
    Protonation of carbonyls; possible ring sulfonation (EAS). Quinones
    carry characteristic n->pi* / pi->pi* bands AND are redox-active
    (quinone<->hydroquinone). A surviving quinone/hydroquinone couple in
    the aerosol is a redox-active organic signature distinct from inert
    red oil. Aromatic + carbonyl IR signatures.

  CHANNEL 4 - INTERIOR BIOMOLECULES (nucleobases, amino acids, lipids)
    [LAB anchor: Seager nucleic-acid-base + amino-acid stability in conc acid]
    Nucleobases (A,C,G,T,U) are STABLE in conc. H2SO4 (Seager 2023/2024) ->
    they can PERSIST as released N-heterocycles rather than fully charring.
    Lipids: fatty-acid-type stable (Seager/Szostak). NET: the strongest,
    most DIAGNOSTIC channel - persistent N-heterocyclic aromatics with
    defined masses. KEEPS NITROGEN, and as identifiable molecules.

  SUMMARY: channels 2 feeds A's red-oil pool; channels 1,3,4 add what A
  lacked - NITROGEN (1,4), REDOX QUINONE (3), and PERSISTENT N-HETEROCYCLES
  (4, Seager-stable). The nitrogen + quinone are the Exchange-E signature.
""")

# ===================================================================
# PART 3 - OPTICS: reuse A's saturating model + add N/quinone bands
# ===================================================================
print("-"*72)
print("PART 3 - OPTICS (carbonized pool reuses A; N-heterocycle + quinone add)")
print("-"*72)

# Reuse Exchange A empirical saturating polyene model (same anchors/fit)
anchor_N   = np.array([3.,5.,7.,9.,11.])
anchor_lam = np.array([268.,330.,380.,420.,450.])
_x=1/anchor_N; _y=1/anchor_lam
_b,_a = np.polyfit(_x,_y,1); lam_inf=1/_a
def lam_emp_nm(N): return 1.0/(_a+_b/np.asarray(N,float))

print(f"  Carbonized fraction (channels 2 + charred 1): SAME saturating")
print(f"  polyene optics as Exchange A -> blue edge converging ~{lam_inf:.0f} nm.")
print(f"  (channel 2 polysaccharide char is optically A-like; not repeated)\n")

# N-heterocycle / quinone reference bands (LAB-class literature values)
print("  Added Exchange-E chromophore/marker bands [LAB-class reference values]:")
bands = [
  ("nucleobase n->pi*/pi->pi* (purine/pyrimidine)", "~260-280 nm UV", "persistent N-heterocycle, Seager-stable"),
  ("quinone pi->pi*",                                "~240-290 nm",    "redox chromophore"),
  ("quinone n->pi* (weak, carbonyl)",               "~330-450 nm",    "redox chromophore, visible tail"),
  ("amino-acid aromatic side chain (Tyr/Trp)",      "~270-280 nm",    "N-bearing aromatic"),
  ("sulfonated aromatic (from side chains)",         "shifted UV + IR","S=O 1030-1200, C-S 600-700 cm^-1"),
]
for name,uv,note in bands:
    print(f"    {name:46s} {uv:16s} | {note}")

print("""
  IR / mass-spec markers unique to Exchange E (not in A, not in abiotic red oil):
    - N-H stretch ~3300-3500 cm^-1 (amine/amide)
    - C=N / aromatic-N ring modes ~1600-1660 cm^-1
    - amide-class C=O if resistant peptides persist ~1650-1690 cm^-1
    - MASS SPECTRUM: peaks at nucleobase masses (e.g. adenine 135, guanine 151,
      cytosine 111, uracil 112, thymine 126 Da) and amino-acid masses, i.e.
      DISCRETE N-bearing masses rather than a smooth hydrocarbon envelope.
""")

# ===================================================================
# PART 4 - DISCRIMINATORS (Exchange-E specific, vs A and vs abiotic)
# ===================================================================
print("-"*72)
print("PART 4 - BIOTIC/CELL-SHED DISCRIMINATORS (the deliverable)")
print("-"*72)
print("""  Exchange E inherits A's D1-D4 for its carbonized fraction, and ADDS the
  following, which distinguish CELL-shed material from BOTH coating-shed (A)
  AND abiotic red oil (C/H/O/S):

  E1. NITROGEN IN THE ORGANIC AEROSOL.
      ~9% N by mass in shed cell material vs ~0% in coating and in abiotic
      red oil. -> TARGET: N-bearing organic masses + N-H/C=N IR. Detecting
      organic nitrogen in the droplets is the single strongest cell-shed
      discriminator. (Note: distinct from inorganic N like NH4+ salts -
      the marker is N inside ORGANIC, aromatic/heterocyclic masses.)

  E2. PERSISTENT, IDENTIFIABLE N-HETEROCYCLES.
      Seager showed nucleobases SURVIVE conc. H2SO4 -> they should appear
      as DISCRETE mass peaks (adenine 135, guanine 151, cytosine 111,
      uracil 112, thymine 126 Da), not a charred continuum. -> TARGET:
      specific m/z lines a mass spectrometer can resolve. A structured,
      "molecular" signature is hard for abiotic chemistry to mimic.

  E3. REDOX-ACTIVE QUINONE COUPLE.
      A quinone/hydroquinone pair in the aerosol is redox-active and
      fluorescent/absorbing in a characteristic way, unlike inert red oil.
      -> TARGET: quinone mass + n->pi* visible tail + redox response.

  E4. AMINO-ACID / PEPTIDE RELICS.
      Released amino-acid backbones (Seager: 19/20 endure) + resistant
      dipeptides (Gly-Gly, His-His). -> TARGET: amino-acid masses and
      amide IR. A second N-bearing molecular family.

  These are ABUNDANCE-INDEPENDENT origin signatures. The headline: Exchange A
  predicts a hydrocarbon/sulfur conjugated absorber; Exchange E predicts that
  PLUS an organic-NITROGEN and quinone molecular fingerprint. Nitrogen (~9%
  by mass) is the thing to look for that A and abiotic chemistry do not provide.
""")

print("="*72)
print("STEP 1 COMPLETE - Exchange E forward prediction generated.")
print("Canonize: cell source term + N-fraction (Part 1), four-channel product")
print("slate (Part 2), N-heterocycle/quinone bands + masses (Part 3), E1-E4 (Part 4).")
print("Step 2 compares dispassionately to today's limited Venus data.")
print("="*72)
