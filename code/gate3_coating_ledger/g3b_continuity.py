#!/usr/bin/env python3
"""
Gate 3b — CONTINUITY ANALYSIS: can ONE whip type feed continuity-sensitive
CO2 chemistry, or is a second (tribovoltaic DC) whip type required?

The chemistry split (Gate 2): CO2 fixation is continuity-sensitive (wants
steady current; degrades on choppy pulses), sulfur/proton chemistry is pulse-
tolerant. A conventional TENG whip produces PULSED AC. Three mechanisms could
convert the whip array's pulsed AC into the continuity the CO2 chemistry wants:

  (1) GEL BUFFER   - the redox gel core (Gate 0/T4) is a charge buffer:
                     pulses in -> steady output. Already validated.
  (2) PHASE-STAGGER - hundreds of whips fluttering OUT OF PHASE fill each
                     other's troughs; the AGGREGATE current never hits zero.
                     (multi-phase rectification.) [user's idea]
  (3) The catch: phase-stagger only works if phases are DISTRIBUTED. Coupled
                     oscillators in a shared flow can SYNCHRONIZE (metronomes,
                     fireflies) -> worst case, all peak/trough together ->
                     MAXIMUM ripple. So we must check: does a shared-wind whip
                     array DESYNC (smoothing works) or ENTRAIN (smoothing fails)?

This script:
  A. quantifies aggregate ripple vs number of whips for RANDOM vs SYNCHRONIZED
     phases (bounds the benefit of phase-stagger).
  B. estimates whether whips desync, via the Kuramoto criterion: do the spread
     in natural frequencies (different whip lengths) and turbulent randomizing
     beat the mechanical coupling? coupling K vs frequency spread d_omega.
  C. combines with the gel buffer to give the net continuity verdict.

All [SIM] lumped estimates with bounded inputs; tagged where [SPEC].
"""
import numpy as np

print("="*72)
print("Gate 3b CONTINUITY — can one whip type feed CO2 (continuity-sensitive)?")
print("="*72)

# ------------------------------------------------------------------
# A. Aggregate ripple: random-phase vs synchronized whips
# ------------------------------------------------------------------
# Each whip: rectified sinusoidal current pulse, i_k(t) = |sin(w t + phi_k)|.
# Aggregate I(t) = sum_k i_k(t). Ripple = (max-min)/mean over a cycle.
print("\n[A] Aggregate ripple vs whip count (rectified-AC model)")
print("    ripple = (Imax - Imin)/Imean over a cycle; lower = smoother")
def ripple(n_whips, phases, n_t=400):
    t = np.linspace(0, 2*np.pi, n_t)
    I = np.zeros(n_t)
    for ph in phases:
        I += np.abs(np.sin(t + ph))
    return (I.max()-I.min())/I.mean()

rng = np.random.default_rng(0)
print(f"    {'n_whips':>8s} {'synchronized':>14s} {'random-phase':>14s}")
for n in [1, 10, 100, 1000]:
    sync = ripple(n, np.zeros(n))                 # all in phase (worst)
    rand = np.mean([ripple(n, rng.uniform(0,2*np.pi,n)) for _ in range(5)])  # random
    print(f"    {n:>8d} {sync:>14.3f} {rand:>14.4f}")
print("    => synchronized whips: ripple stays ~1.0 (bad, never smooths).")
print("       random-phase whips: ripple -> ~0 as n grows (excellent smoothing).")
print("    The benefit of phase-stagger is REAL but CONTINGENT on desync (part B).")

# ------------------------------------------------------------------
# B. Do whips desync or entrain? Kuramoto-style criterion
# ------------------------------------------------------------------
# Coupled oscillators synchronize when coupling K > critical Kc ~ frequency
# spread d_omega. If natural-frequency spread (from whip length variation) and
# turbulent randomizing EXCEED coupling, they stay desynchronized (good).
print("\n[B] Desync vs entrainment (Kuramoto criterion)")
# whip natural frequencies: length 1-2 mm -> flutter 0.1-1 Hz (Gate 1b).
# frequency spread across the population:
f_lo, f_hi = 0.1, 1.0
d_omega = 2*np.pi*(f_hi - f_lo)        # rad/s spread in natural freq
omega_mean = 2*np.pi*0.5
print(f"    natural-frequency spread d_omega = {d_omega:.2f} rad/s "
      f"(whip lengths 1-2mm -> 0.1-1 Hz)")
# coupling strength K: mechanical coupling through the soft body. Whips are
# weakly coupled (soft fluffball, each whip semi-independent). Bound K as a
# fraction of omega: weak (0.01), moderate (0.1), strong (1.0) x omega_mean.
print(f"    {'coupling K':>22s} {'K (rad/s)':>10s} {'K/d_omega':>10s} {'regime':>16s}")
for label, frac in [("weak (0.01*omega)",0.01),("moderate (0.1*omega)",0.1),
                    ("strong (1.0*omega)",1.0)]:
    K = frac*omega_mean
    ratio = K/d_omega
    # Kuramoto: sync requires K > Kc ~ d_omega (order 1). ratio<1 => desync.
    regime = "DESYNC (good)" if ratio < 1 else "ENTRAIN (bad)"
    print(f"    {label:>22s} {K:>10.3f} {ratio:>10.2f} {regime:>16s}")
print("    Plus turbulent wind (66-69 m/s, highly unsteady) is a strong")
print("    randomizing drive that further OPPOSES entrainment. [SPEC, favorable]")
print("    => For weak/moderate coupling (expected for a soft fluffball of mixed-")
print("       length whips in turbulent wind), whips DESYNC -> phase-stagger WORKS.")

# ------------------------------------------------------------------
# C. Combine with gel buffer -> net continuity verdict
# ------------------------------------------------------------------
print("\n[C] Net continuity verdict (phase-stagger + gel buffer)")
# Even residual ripple after phase-stagger is smoothed by the gel buffer.
# Gel buffer time constant tau_gel vs whip period T_whip: if tau_gel >> T_whip,
# the gel integrates over many pulses -> output is steady.
T_whip = 1/0.5                 # s, whip period at 0.5 Hz
# gel buffer: from T4, the gel holds/releases charge over a metabolic timescale
# (seconds-to-minutes). Conservatively tau_gel ~ 1-60 s.
for tau_gel in [1, 10, 60]:
    n_pulses_integrated = tau_gel/T_whip
    print(f"    tau_gel={tau_gel:4.0f}s -> integrates ~{n_pulses_integrated:.0f} whip pulses "
          f"-> {'steady DC-like output' if n_pulses_integrated>5 else 'partial smoothing'}")
print()
print("="*72)
print("VERDICT")
print("="*72)
print("Continuity-sensitive CO2 chemistry CAN be fed by ONE whip type (conventional")
print("pulsed-AC), because TWO smoothing mechanisms stack:")
print("  1. PHASE-STAGGER: a desynchronized array (mixed whip lengths + turbulent")
print("     wind defeat entrainment) drives aggregate ripple toward zero as whip")
print("     count grows into the hundreds-thousands we already need for current.")
print("  2. GEL BUFFER: the validated redox-gel core integrates over many whip")
print("     pulses (tau_gel >> whip period), delivering steady DC-like output.")
print("=> NO separate tribovoltaic whip type required. The creature has ONE whip")
print("   type and NO cell specialization for power. (Simplest design, consistent")
print("   with all prior gates.) The tribovoltaic option remains a fallback, not")
print("   a requirement. [SIM; coupling strength + gel tau are SPEC-bounded]")
print("="*72)
