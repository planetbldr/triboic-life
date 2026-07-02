#!/usr/bin/env python3
"""
GATE 4 - Exchange A, Step 1 (forward chemistry -> spectrograph target)
======================================================================
Shed sporopollenin-class coating -> acid-processed conjugated organics ->
predicted UV/visible absorption band a probe spectrograph would see.

PURELY FORWARD. No comparison to known Venus data here (that is Step 2).
No kill-conditions. Output = a target list: species, bands, discriminators.

Compute discipline: bounded numpy only. No DFT (compute wall, documented g3a).
Chromophore optics done analytically (free-electron particle-in-a-box, FEMO)
plus a simple Hückel/Lewis-Calvin empirical check. Minutes, not overnight.

Evidence tags in comments: [LAB] literature, [SIM] computed here,
[SPEC] reasoned, [SPEC-CHOICE] a chemistry choice this gate makes + justifies.

All ANCHORED inputs trace to canonized project numbers (g3a, g3b, refs).
"""

import numpy as np

print("="*72)
print("GATE 4 - EXCHANGE A - STEP 1: shed coating -> chromophores -> spectrum")
print("="*72)

# ===================================================================
# PART 1 - SOURCE TERM: how much coating material sheds, as what
# ===================================================================
print("\n" + "-"*72)
print("PART 1 - SOURCE TERM (shed mass flux of coating fragments)")
print("-"*72)

# --- Anchored geometry (canonized, GATE3 consolidation + g3a) -------
# Whip: 1-2 mm long, ~10 um wide, ~100 nm thick, 4 layers, one is the
# sporopollenin coat. Array ~1.6e3 whips per creature (g3b).
whip_len_m      = 1.5e-3      # [LAB/SIM canon] mid of 1-2 mm
whip_wid_m      = 10e-6       # [LAB/SIM canon] ~10 um
coat_thick_m    = 100e-9      # [SPEC-CHOICE] coat ~ one ~100nm-class layer.
#   Justification: consolidation gives whole-whip ~100 nm thick across 4
#   layers; the sporopollenin coat is the outer barrier. Taking the coat as
#   a full ~100 nm OVER-counts coat mass (it is one of four layers) -> this
#   is a deliberately GENEROUS source term, so the predicted signal is an
#   upper-ish bound, not an underestimate. Canonized as [SPEC-CHOICE].
n_whips         = 1.6e3       # [SIM canon, g3b] array size
rho_sporo       = 1.4e3       # kg/m3 [LAB] sporopollenin density (coating report)

# Coat surface area per whip: outer envelope of the ribbon (2 faces dominate)
# ribbon face area (one side) ~ len*wid; coat wraps -> ~2 faces + edges ~ 2.2x face
face_area_m2    = whip_len_m * whip_wid_m
coat_area_m2    = 2.2 * face_area_m2            # [SPEC] wrap factor
coat_vol_m3     = coat_area_m2 * coat_thick_m
coat_mass_kg    = coat_vol_m3 * rho_sporo
coat_mass_per_creature = coat_mass_kg * n_whips

print(f"  whip face area           : {face_area_m2:.3e} m^2  [matches g3a 1.5e-8]")
print(f"  coat mass / whip         : {coat_mass_kg:.3e} kg")
print(f"  coat mass / creature     : {coat_mass_per_creature:.3e} kg  ({coat_mass_per_creature*1e12:.2f} pg)")

# --- Shed RATE: from irreversible-channel surface loss -------------
# g3a KEY FINDING: reversible cleavage re-forms in place (NO net shed);
# the SHED comes from IRREVERSIBLE channels (sulfonation + oxocarbenium->
# dehydration->Friedel-Crafts->charring) that accumulate per acid impact
# REGARDLESS of duty cycle. So Exchange A's source IS the irreversible
# surface-charring/sulfonation loss. This is the project-internal anchor.
#
# Turnover of the whip material (g3b ledger): 0.3%/day (durable corner) to
# 3%/day (pessimistic), central 1%/day. The coat sheds as the whip renews.
turnover_per_day = np.array([0.003, 0.01, 0.03])  # [SIM canon g3b] low/cen/high
labels           = ["durable(0.3%/d)", "central(1%/d)", "pessimistic(3%/d)"]

shed_kg_per_day_per_creature = coat_mass_per_creature * turnover_per_day
print(f"\n  Shed coating mass flux per creature (coat turnover):")
for L, q in zip(labels, shed_kg_per_day_per_creature):
    print(f"    {L:20s}: {q:.3e} kg/day  ({q*1e12:.3f} pg/day)")

# --- Scale to a population (column number density) -----------------
# [SPEC-CHOICE] population density envelope. No design number exists for
# how many creatures per m^3. We bound it by analogy to terran cloud
# microbial loads (1e2-1e6 cells/m^3 in Earth clouds [LAB-class]) but the
# creature is mm-scale multicellular, far larger than a microbe, so a
# Venus population must be FAR sparser. We canonize a deliberately wide,
# conservative band and carry it as the dominant [SPEC] uncertainty.
#   low  : 1e-3 creatures/m^3  (1 per 1000 m^3 - very sparse)
#   mid  : 1e0  creatures/m^3
#   high : 1e2  creatures/m^3  (dense bloom)
# Justification: the optical signal scales linearly with this, so we report
# the per-creature chemistry firmly and let the column density float on this
# explicit band. The DISCRIMINATOR (Part 3) does NOT depend on it.
pop_per_m3 = np.array([1e-3, 1e0, 1e2])
pop_labels = ["sparse(1e-3/m3)", "moderate(1/m3)", "bloom(1e2/m3)"]

# Cloud-deck layer thickness for a column (50-54 km -> ~4 km path) [LAB]
path_m = 4e3

print(f"\n  [SPEC-CHOICE] population band (linear scale on signal):")
for L, p in zip(pop_labels, pop_per_m3):
    # shed mass per m3 per day, central turnover
    shed_central = coat_mass_per_creature * 0.01 * p
    print(f"    {L:18s}: {shed_central:.2e} kg shed / m^3 / day (central turnover)")

# ===================================================================
# PART 2 - WHAT FORMS: the conjugated-polyene product slate
# ===================================================================
print("\n" + "-"*72)
print("PART 2 - PRODUCT CHEMISTRY (forward route in concentrated H2SO4)")
print("-"*72)
print("""  Forward route [LAB class, Spacek&Benner organics-in-acid; g3a irreversible
  channel]:  shed phenolic/aliphatic fragment
     --(protonation)--> oxocarbenium/acylium
     --(dehydration, -H2O to the acid)--> increasingly unsaturated chain
     --(intramolecular Friedel-Crafts / cation-olefin cyclization)-->
        progressively CONJUGATED polyene / fused polyaromatic ("red oil")
     --(sulfonation of activated rings, EAS)--> -SO3H decorated chromophore
  Net products to track:
    (i)   conjugated polyenes  C=C-C=C-... of growing length N (double bonds)
    (ii)  fused polyaromatics (red-oil end member)
    (iii) sulfonated aromatics (heteroatom-bearing chromophore)  <- KEY discriminator
    (iv)  the leaving water (-> feeds the droplet, negligible vs bulk H2O sink)
""")

# The chromophore that sets the OPTICAL signature is the conjugation length.
# We compute absorption edge vs number of conjugated double bonds N.

# ===================================================================
# PART 3 - THE OPTICS: conjugation length -> absorption wavelength
# ===================================================================
print("-"*72)
print("PART 3 - CHROMOPHORE OPTICS (the spectrograph target)")
print("-"*72)

# METHOD NOTE (why not FEMO): the naive free-electron particle-in-a-box has
# NO bond-length alternation, so its gap -> 0 and lambda -> infinity as N grows
# (it predicted 1360 nm at N=11 vs ~450 nm measured - off by 3x). Real polyenes
# SATURATE to a finite limit because alternation pins a minimum HOMO-LUMO gap.
# So FEMO is discarded. We use two saturating models instead:
#   (1) PRIMARY [SIM/LAB]: empirical 1/lambda = a + b/N, fit DIRECTLY to the
#       experimental polyene series. Linear, saturating, data-anchored.
#   (2) CHECK   [SIM]: Hueckel tight-binding WITH bond alternation - confirms
#       saturation qualitatively but is NOT used for quantitative lambda (bare
#       one-electron gaps run too red; electron correlation, absent here,
#       lowers the real transition). Division of labor canonized.

# --- Experimental anchor series (LAB approx, polyene/carotenoid-class) ---
anchor_N   = np.array([3.,   5.,   7.,   9.,   11.])
anchor_lam = np.array([268., 330., 380., 420., 450.])  # nm [LAB approx]

# --- PRIMARY model: empirical saturating fit 1/lambda = a + b/N ----------
# Fit to the anchors (this is the quantitative model we stand behind).
_x = 1.0/anchor_N; _y = 1.0/anchor_lam
_b, _a = np.polyfit(_x, _y, 1)          # 1/lam = _a + _b*(1/N)
lam_inf = 1.0/_a                        # infinite-chain saturation limit (nm)

def lam_emp_nm(N):
    """absorption lambda (nm) vs N conjugated C=C - empirical saturating fit."""
    return 1.0/(_a + _b/np.asarray(N, float))

# --- CHECK model: Hueckel with bond alternation (saturation only) --------
def lam_huckel_nm(N, b1=-2.5, b2=-2.1):
    n = 2*int(N)
    H = np.zeros((n, n))
    for i in range(n-1):
        H[i, i+1] = H[i+1, i] = (b1 if i % 2 == 0 else b2)
    E = np.sort(np.linalg.eigvalsh(H))
    gap = abs(E[n//2] - E[n//2 - 1])     # eV
    return 1239.84/gap if gap > 0 else np.inf

print(f"  PRIMARY empirical fit: 1/lambda = {_a:.3e} + {_b:.3e}/N")
print(f"  -> infinite-chain saturation limit lambda_inf = {lam_inf:.0f} nm  [SIM/LAB]")
print(f"  -> fit reproduces experimental anchors to <3% (validated)\n")

print("  N(C=C) | empirical(nm) | exp-anchor(nm) | Huckel-check(nm) | band")
print("  -------+---------------+----------------+------------------+-------------")
for N in [2,3,4,5,6,7,9,11,15,20,30]:
    lam_e = lam_emp_nm(N)
    lam_h = lam_huckel_nm(N)
    if N in anchor_N:
        es = f"{anchor_lam[list(anchor_N).index(N)]:6.0f}"
    else:
        es = "   -  "
    if   lam_e < 320: band = "UV (200-320)"
    elif lam_e < 400: band = "UV/violet edge"
    elif lam_e < 500: band = "blue (the absorber band)"
    else:             band = "vis-green+ (saturated)"
    print(f"   {int(N):4d}  |   {lam_e:7.1f}     |     {es}     |     {lam_h:7.0f}      | {band}")

print(f"""
  Reading the table:
  - The empirical (saturating) model matches the experimental polyene anchors
    to <3% and SATURATES toward ~{lam_inf:.0f} nm - it does NOT run off to the IR.
    This is the physically correct behavior FEMO missed. [SIM/LAB cross-check]
  - The Hueckel-with-alternation column also saturates (finite limit), an
    INDEPENDENT confirmation that the gap floors rather than closing; its
    absolute nm values run red and are used only to confirm saturation, not
    for the quantitative band. [SIM, qualitative only]
  - Result: shed-derived conjugated organics absorb across ~270 nm (short, N~3)
    rising and SATURATING into the ~440-580 nm blue/blue-green window as
    conjugation grows (N~9-15+) - i.e. they naturally populate and PILE UP at
    the UV-blue/violet edge rather than dispersing arbitrarily. The Venus
    'UV-blue absorber' band of interest (~320-500 nm) is squarely inside this
    saturating envelope. [SIM forward prediction; LAB-anchored]
  - SHARPER TARGET than 'reaches the band': the saturation means the chromophore
    population CONVERGES on a blue edge near ~450-580 nm with a rising-then-
    flattening absorption profile - a specific spectral SHAPE to look for.
""")

# ===================================================================
# PART 4 - THE DISCRIMINATOR (biotic-shed vs abiotic red oil)
# ===================================================================
print("-"*72)
print("PART 4 - BIOTIC vs ABIOTIC DISCRIMINATORS (the real deliverable)")
print("-"*72)
print("""  Abiotic red oil (Spacek baseline) and creature-shed organics BOTH make
  conjugated chromophores in this band. So 'UV-blue absorber present' is NOT
  diagnostic. What could distinguish CREATURE-SHED material:

  D1. STRUCTURED CHAIN-LENGTH DISTRIBUTION.
      Abiotic polymerization -> broad statistical (Flory-like) chain-length
      distribution. Shed coating fragments start from a DEFINED biopolymer
      (sporopollenin: repeating C16-coumaroyl + m-dioxane units) -> the
      released chromophore population should be NARROWER / peaked at the
      lengths set by the monomer spacing. A spectrograph sees this as a
      structured absorption profile (resolvable peak(s)) vs a smooth
      featureless rise. -> TARGET: spectral SHAPE, not just magnitude.

  D2. SULFONATION / HETEROATOM FINGERPRINT.
      Shed aromatics carry -SO3H (EAS sulfonation, g3a). -SO3H shifts and
      broadens UV bands AND adds IR signatures: S=O stretches ~1030-1060 and
      ~1150-1200 cm^-1, plus C-S ~600-700 cm^-1. -> TARGET: paired UV(chromo)
      + IR(sulfonate) co-location is hard for pure-hydrocarbon abiotic red oil.

  D3. COUMARATE/FERULATE PHENOLIC RELICS.
      Sporopollenin building blocks (p-coumaric, ferulic acid) carry a
      characteristic phenolic + cinnamoyl chromophore (~290-330 nm) and IR
      C=O ester ~1700-1730, aromatic C=C ~1600, 1510 cm^-1. A surviving relic
      population of these BEFORE full charring = a biosynthetic-precursor
      fingerprint. -> TARGET: a ~310 nm shoulder + ester/aromatic IR triplet.

  D4. SPATIAL/TEMPORAL CORRELATION.
      Creature-shed organics co-locate with the creature population (the
      50-54 km Earth-temperature layer) and would track its drift/blooms,
      whereas abiotic red oil forms wherever feedstock+acid+UV coincide.
      -> TARGET: altitude-confined, possibly patchy/time-variable absorber
      vs smoothly distributed abiotic background.

  These four are what a probe should be told to look for. None of them
  depends on the population density (Part 1 band) - they are signatures of
  ORIGIN, not abundance.
""")

print("="*72)
print("STEP 1 COMPLETE - forward prediction + probe targets generated.")
print("Numbers to canonize: per-creature shed flux (Part 1), the N->lambda")
print("optics cross-check (Part 3), and the D1-D4 discriminators (Part 4).")
print("Step 2 will cross-check the predicted band against today's limited data.")
print("="*72)
