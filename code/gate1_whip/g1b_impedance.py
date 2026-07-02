#!/usr/bin/env python3
"""
Gate 1(b) — impedance leg (completes the frequency/charge/impedance triad).

QUESTION: is the tribowhip's source impedance compatible with the redox gel as
its load? The TENG briefing flags this as the field's central problem: TENGs are
high-voltage, low-current, HIGH source impedance (often >10 MOhm), pulsed, and
chronically mismatched to low-impedance DC loads. Most lab energy is lost in
power management. For our creature the "power-management IC" does not exist; the
gel itself is the load and the matching must be intrinsic.

FRAMEWORK (bounded, not precise):
  A contact-separation TENG behaves as a current source I_sc in parallel with an
  intrinsic capacitance C_teng, feeding a load. Its characteristic source
  impedance at the operating frequency is capacitive:
        Z_source ~ 1 / (2*pi*f * C_teng)
  Optimal power transfer (the TENG matched-load condition, from the briefing's
  own framing) occurs when the LOAD impedance ~ Z_source, i.e.
        R_load_opt ~ 1 / (2*pi*f * C_teng)
  We compute Z_source from canonical numbers and ask whether the GEL's load
  impedance can sit near it.

CANONICAL INPUTS (from prior gates, tagged):
  f       : flutter contact rate, gel window 0.1-5 Hz                  [SIM, 1b]
  Q_pulse : ~1e-15 C target (1 fC), the gel's validated pulse          [LAB, T4]
  C_teng  : whip self-capacitance. For a ribbon face of area A and the
            charged-layer/gel separation d, C ~ eps0*eps_r*A/d. Bounded
            from the 1(a) whip geometry.                                [SIM]
  Gel load: the redox gel is an ionic-liquid/quinone medium. Its resistance
            across the core R_gel ~ rho_gel * d / A. Ionic-liquid resistivity
            rho_gel ~ 0.1-10 Ohm*m (conductivity 0.1-10 S/m typical for
            redox/IL gels). Bounded and swept.                          [LAB-ish]

WHY THIS MATTERS: if Z_source >> any achievable R_gel, the gel looks like a near
short -> charge dumps fast but at near-zero voltage -> little usable energy per
pulse (the classic TENG mismatch). If Z_source ~ R_gel, transfer is efficient.
The 2e- capacitive gel was validated as a CHARGE BUFFER (it stores charge); the
question here is whether it also presents a matchable load impedance.
"""
import numpy as np

eps0=8.854e-12

# ---- whip self-capacitance from 1(a) geometry ----
# ribbon face area (large-whip regime): A ~ L*w
# charged-layer-to-gel separation d: thin functional skin, ~10nm-1um
def C_teng(A,d,eps_r=5.0):  # eps_r ~ few for hydrated biopolymer/gel
    return eps0*eps_r*A/d

# ---- source impedance ----
def Z_source(f,C):
    return 1.0/(2*np.pi*f*C)

# ---- gel load resistance ----
def R_gel(rho,d,A):
    return rho*d/A

print("="*92)
print("Gate 1(b) IMPEDANCE LEG: whip source impedance vs redox-gel load")
print("="*92)

# representative in-band whip (from canonical 1b: L=1mm, in-band; 1a: large whip)
A_face=1e-3*1e-5      # 1mm x 10um = 1e-8 m^2 (one ribbon face)
print(f"Representative in-band whip: face area A={A_face:.1e} m^2 (1mm x 10um)")

print("\n-- Source impedance Z_source = 1/(2*pi*f*C_teng) --")
print(f"{'d_skin':>8s} | {'C_teng(F)':>12s} | "+" | ".join(f"f={f}Hz".rjust(11) for f in [0.26,1.0,5.0]))
for d in [1e-8,1e-7,1e-6]:
    C=C_teng(A_face,d)
    zs=[Z_source(f,C) for f in [0.26,1.0,5.0]]
    print(f"{d*1e9:6.0f}nm | {C:12.2e} | "+" | ".join(f"{z:.1e}".rjust(11) for z in zs))

print("\n-- Gel load resistance R_gel = rho_gel*d/A (across the thin core gap) --")
print(f"{'rho(Ohm*m)':>10s} | "+" | ".join(f"d={d*1e9:.0f}nm".rjust(11) for d in [1e-8,1e-7,1e-6]))
for rho in [0.1,1.0,10.0]:
    rs=[R_gel(rho,d,A_face) for d in [1e-8,1e-7,1e-6]]
    print(f"{rho:10.1f} | "+" | ".join(f"{r:.1e}".rjust(11) for r in rs))

# ---- matching ratio ----
print("\n-- Matching: R_gel / Z_source (want ~1 for efficient transfer; <<1 = mismatch/short) --")
print("   (using f=0.26 Hz binding rate, d=100nm skin) ")
C=C_teng(A_face,1e-7); zs=Z_source(0.26,C)
for rho in [0.1,1.0,10.0]:
    rg=R_gel(rho,1e-7,A_face)
    print(f"   rho_gel={rho:5.1f}: R_gel={rg:.1e}  Z_source={zs:.1e}  ratio={rg/zs:.1e}")

# ---- the honest reframing: charge-buffer vs impedance-match ----
print("""
INTERPRETATION:
- Z_source is ENORMOUS (10^14-10^17 Ohm) because C_teng is tiny (sub-femtofarad
  for a micron-scale charged skin). This is the TENG high-impedance problem in
  the extreme: a small biological capacitor has even higher source impedance
  than a lab TENG.
- R_gel is TINY (10^-3 to 10^2 Ohm) -- an ionic gel is a good conductor.
- So R_gel/Z_source ~ 10^-15: the gel looks like a NEAR SHORT to the whip.
- CLASSIC INTERPRETATION (briefing): a near-short load means charge dumps at
  near-zero voltage -> little usable ENERGY per pulse if you needed voltage.
- BUT our architecture does NOT extract energy as voltage across a matched load.
  The gel is a 2e- CAPACITIVE CHARGE BUFFER (validated T3/T4): it ACCEPTS the
  charge into redox states and meters it out as steady current. For a charge-
  metering buffer, a LOW-impedance (near-short) load is exactly what you want --
  it sinks the pulse charge completely with minimal back-voltage to fight.
- So the TENG impedance 'problem' INVERTS for this design: the mismatch that
  wastes energy in a voltage-extracting TENG is BENIGN for a charge-buffering
  one. The whip is a charge pump into a redox sink, not a voltage source into a
  matched resistor.
- CAVEAT [SPEC]: this holds only while the gel's redox states are unsaturated
  (T4 capacity side: 10^11-10^14 quinone molecules, ample) AND while charge
  injection across the skin/gel interface is not itself rate-limited. The
  interfacial charge-transfer kinetics (electron/ion crossing the skin-gel
  boundary per contact) are NOT modeled here and are the real open question --
  flagged for critique, not closed.
""")
print("="*92)
print("ANTI-ARTIFACT NOTE: this leg does NOT pass/fail on a swept envelope; it")
print("reframes a known number (huge Z_source) against the validated buffer role.")
print("The load-bearing uncertainty is interfacial charge-transfer kinetics, named not solved.")
print("="*92)
