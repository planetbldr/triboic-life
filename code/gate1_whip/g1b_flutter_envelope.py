#!/usr/bin/env python3
"""
Gate 1(b) — The flutter envelope.
Triboic Life · Phase 2 · sealed-core tribowhip.

QUESTION (plan v3, Gate 1b):
  What flutter frequency / charge-per-pulse / impedance does an evolvable
  micron-to-millimetre whip produce in the Venus cloud-deck regime? Treat as a
  SWEPT parameter space; report the viable envelope, not assumed values.

SCOPE-SHARPENED BY GATE 1(a):
  1(a) showed the whip must be LARGE (hundreds-of-um to mm) to carry the gel's
  1 fC pulse; micron whips are excluded dimensionally. So 1(b) asks specifically
  whether LARGE whips flutter at the sub-Hz-to-few-Hz the gel buffer wants, and
  whether their source impedance is compatible.

GEL TARGET WINDOW (from redox-core T4, [LAB]-anchored):
  flutter (contact) rate f_contact in the sub-Hz to ~5 Hz band; the binding
  maintenance regime needs ~0.26 Hz at 1 fC/contact. A whip that flutters in
  ~0.1-5 Hz lands in the validated window. Too fast (>>5 Hz) overshoots the
  gel's buffering assumption; too slow (<<0.1 Hz) undersupplies.

VENUS CLOUD-DECK PARAMETERS (~50-54 km, the Seager habitable zone) [LAB]:
  - density rho: 0.87-1.74 kg/m^3 (derived from sourced P,T,MW via ideal gas;
    1 bar/300K -> 1.74; 0.5 bar/300K -> 0.87). NOTE: this is COMPARABLE TO or
    DENSER THAN Earth air -- the regime is NOT "thin." (Correction to the
    project's "thin air" wording; thin applies ~70+ km, not the habitable zone.)
  - dynamic viscosity mu: ~1.5e-5 Pa s (CO2 at ~300 K).
  - horizontal (zonal) wind: 66-69 m/s (VeGa balloons, 54 km) [LAB].
  - vertical gusts / turbulence: -4 to +2 m/s, convective cells hundreds-m to
    tens-km (VeGa, Linkin 1986) [LAB].
  - composition 96.5% CO2, MW 43.45 g/mol.

FLUTTER PHYSICS (flag/ribbon limit-cycle flutter):
  A flexible cantilever ribbon in cross-flow flutters above a critical reduced
  velocity. Once fluttering, the limit-cycle frequency is set by the structural
  bending dynamics modulated by added-fluid mass. We DO NOT assume the cell sits
  at one wind speed; we sweep ribbon length L, thickness h, and effective
  modulus E, and compute:

  (1) Structural first-mode (in-vacuo) cantilever frequency:
        f_struct = (beta1^2 / (2*pi)) * sqrt(E*I / (rho_s * A_x * L^4))
      with beta1 = 1.875 (first cantilever mode), I = w*h^3/12, A_x = w*h.
      => f_struct = (1.875^2/(2pi)) * (h/L^2) * sqrt(E/(12*rho_s))
      (width w cancels -- frequency set by L, h, E, material density.)

  (2) Added-mass correction for dense surrounding fluid (matters here because
      Venus cloud air is NOT thin): the fluid loads the ribbon, lowering the
      wet frequency:
        f_wet = f_struct / sqrt(1 + (pi*rho_f*w)/(4*rho_s*h))   [thin-blade
      added-mass estimate; the bracket is the fluid-to-structure mass loading].

  (3) Flutter onset check via reduced velocity U* = U /(f_struct * L):
      flag flutter switches on for U* above ~3-10 (Reynolds/mass-ratio
      dependent). We just check the regime is reachable at Venus winds, not the
      precise onset (that needs a stability eigensolve -- out of scope; flagged).

  The contact/flutter frequency the GEL sees ~ f_wet (one charge deposition per
  flutter cycle, possibly x2 if both faces contact per cycle -- bounded).

EVOLVABLE RIBBON PARAMETER RANGES [SPEC, swept]:
  L : 1e-4 .. 2e-3 m   (100 um .. 2 mm -- the LARGE-whip regime 1a requires)
  h : 1e-7 .. 1e-6 m   (0.1 .. 1 um thick ribbon -- biofilm/membrane-like)
  E : 1e6 .. 1e9 Pa    (soft gel/membrane 1 MPa .. stiff silk-backing ~GPa;
                        the 4-layer sandwich spans this -- swept)
  rho_s ~ 1200 kg/m^3  (hydrated biopolymer, ~water-to-protein density)

ANTI-ARTIFACT DISCIPLINE: a model where every ribbon flutters in-band, or none
  does, is an artifact. We report WHERE in (L,h,E) the wet frequency lands in
  the gel's 0.1-5 Hz window, and confirm the window is reached by SOME but not
  ALL of the swept space.
"""
import numpy as np

# ---- gel target window (Hz) ----
F_LO, F_HI = 0.1, 5.0          # validated buffering band
F_BIND     = 0.26              # P. aeruginosa maintenance binding rate

# ---- Venus cloud-deck fluid (sourced) ----
rho_f_lo, rho_f_hi = 0.87, 1.74    # kg/m^3
U_wind_lo, U_wind_hi = 66.0, 69.0  # m/s zonal (VeGa)
U_gust = 2.0                        # m/s vertical gust scale
mu_f = 1.5e-5                       # Pa s

# ---- ribbon material ----
rho_s = 1200.0                 # kg/m^3 hydrated biopolymer
beta1 = 1.875                  # first cantilever eigenvalue

def f_struct(L,h,E):
    return (beta1**2/(2*np.pi))*(h/L**2)*np.sqrt(E/(12*rho_s))

def f_wet(L,h,E,w,rho_f):
    fs=f_struct(L,h,E)
    loading=(np.pi*rho_f*w)/(4*rho_s*h)
    return fs/np.sqrt(1+loading)

# ---- swept ranges ----
Ls=np.array([1e-4,3e-4,5e-4,1e-3,2e-3])         # 100um..2mm
hs=np.array([1e-7,3e-7,1e-6])                    # 0.1..1um
Es=np.array([1e6,1e7,1e8,1e9])                   # 1MPa..1GPa
w_rep=1e-5                                        # 10 um representative width

print("="*94)
print("Gate 1(b) flutter envelope: wet first-mode frequency vs gel window [%.1f, %.1f] Hz"%(F_LO,F_HI))
print("Venus cloud deck rho_f=%.2f-%.2f kg/m^3 (DENSE, not thin), U_zonal=%d-%d m/s"
      %(rho_f_lo,rho_f_hi,U_wind_lo,U_wind_hi))
print("="*94)

in_band=0; total=0; too_fast=0; too_slow=0
band_cells=[]
for E in Es:
    print(f"\n--- E = {E:.0e} Pa ---")
    print(f"  {'L(um)':>7s} | "+" | ".join(f"h={h*1e9:.0f}nm".rjust(13) for h in hs))
    for L in Ls:
        row=[]
        for h in hs:
            fw=f_wet(L,h,E,w_rep,rho_f_hi)  # densest air = lowest freq (conservative)
            total+=1
            if F_LO<=fw<=F_HI:
                in_band+=1; tag="IN"; band_cells.append((L,h,E,fw))
            elif fw>F_HI: too_fast+=1; tag=">>"
            else: too_slow+=1; tag="<<"
            row.append(f"{tag} {fw:.2e}")
        print(f"  {L*1e6:>7.0f} | "+" | ".join(c.rjust(13) for c in row))

# reduced-velocity flutter-onset reachability at Venus winds
print("\n"+"-"*94)
print("Flutter-onset reachability: U* = U/(f_struct*L); flag flutter onsets ~U*>3-10")
for L in [3e-4,1e-3,2e-3]:
    for E in [1e7,1e9]:
        fs=f_struct(L,1e-7,E)
        Ustar_zonal=U_wind_hi/(fs*L)
        Ustar_gust = U_gust/(fs*L)
        print(f"  L={L*1e6:.0f}um E={E:.0e}: f_struct={fs:.2e}Hz  U*_zonal={Ustar_zonal:.1f}  U*_gust={Ustar_gust:.2f}")

print("\n"+"="*94)
print("ENVELOPE SUMMARY")
print(f"  swept cells: {total} | in gel band [{F_LO},{F_HI}]Hz: {in_band} | too fast: {too_fast} | too slow: {too_slow}")
if band_cells:
    Lb=[c[0] for c in band_cells]; Eb=[c[2] for c in band_cells]
    print(f"  in-band ribbons: L={min(Lb)*1e6:.0f}-{max(Lb)*1e6:.0f}um, E={min(Eb):.0e}-{max(Eb):.0e}Pa")
print("\nANTI-ARTIFACT CHECK")
ok = (in_band>0 and (too_fast>0 or too_slow>0))
print(f"  some IN-band: {in_band>0} | some OUT: {(too_fast+too_slow)>0}")
print("  GOOD: gel window reached by a BOUNDED sub-region, not all/none." if ok
      else "  WARNING: trivial all/none -> revisit bounds.")
print("="*94)
