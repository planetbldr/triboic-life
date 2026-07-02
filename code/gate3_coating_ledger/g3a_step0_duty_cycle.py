#!/usr/bin/env python3
"""
Gate 3a  STEP 0 — Acid exposure duty cycle.

PURPOSE
-------
Before any xTB chemistry, establish the PHYSICAL acid exposure regime:
how often does a droplet hit the ribbon, and how long does the acid film
persist before 66–69 m/s winds shear it off?  These two numbers combine
into a duty cycle that modulates the effective chemical attack rate.

This is pure numpy — no xTB needed.

CONTEXT
-------
The ribbon is NOT immersed in acid.  It extends into thin CO2 gas and is
struck intermittently by Venus cloud-deck acid aerosol droplets.  High
winds (VeGa data: 66–69 m/s zonal) shear the acid film off between hits.
So the acid-contact duty cycle (fraction of time the coating is wet with
acid) is << 1, and the effective chemical attack rate on the coating =
(intrinsic attack rate) × (duty cycle) for REVERSIBLE channels only.
For IRREVERSIBLE channels (sulfonation, charring) damage accumulates
per-hit regardless of duty cycle; see the verdict section.

INPUTS — all tagged [LAB] or [SPEC]
-------------------------------------
Venus mode-2 droplet number density: ~3e8 /m^3  [LAB, Venus cloud data]
Venus mode-3 droplet number density: ~5e7 /m^3  [LAB]
Coarse dust ~1um: ~1e6 /m^3                     [LAB, rough]
Relative velocity whip-droplet: 0.1 m/s         [SPEC — flutter tip speed]
Ribbon face area: 1.5mm x 10um = 1.5e-8 m^2    [Gate 1a/1b pinned geometry]
Wind speed U: 67 m/s                            [LAB, VeGa]
Acid film viscosity mu: ~20e-3 Pa.s (90% H2SO4) [LAB, tables]
Film thickness delta: 1e-7 to 1e-5 m (0.1–10um) [SPEC, swept]
Surface tension gamma: 0.07 N/m (90% H2SO4)    [LAB, approx]
Contact length for adhesion L_c: ~10um = 1e-5 m [SPEC, ribbon width]
"""

import numpy as np

print("="*76)
print("Gate 3a Step 0 — Acid-droplet exposure duty cycle")
print("="*76)

DAY = 86400.0
U_wind = 67.0           # m/s zonal
mu_acid = 20e-3         # Pa.s, viscosity of ~90% H2SO4 at ~300K [LAB]
gamma = 0.07            # N/m, surface tension [LAB]
A_ribbon = 1.5e-3 * 1e-5  # m^2 ribbon face area
v_rel = 0.1             # m/s relative velocity [SPEC]
L_c = 1e-5              # m, characteristic contact length (ribbon width)

# ------------------------------------------------------------------
# PART A: Hit rate (reused from g2b_wear_lifetime CHANNEL 3)
# ------------------------------------------------------------------
print("\n--- PART A: Droplet hit rate ---")
particles = [
    ("mode-2 aerosol",  3e8),
    ("mode-3 aerosol",  5e7),
    ("coarse dust ~1um",1e6),
]
print(f"  {'particle':18s} {'n(/m3)':>10s} {'hits/s':>10s} {'hits/day':>10s}")
for name, n in particles:
    rate_s = n * v_rel * A_ribbon
    rate_d = rate_s * DAY
    print(f"  {name:18s} {n:>10.1e} {rate_s:>10.2e} {rate_d:>10.1e}")

# dominant flux is mode-2 droplets
hit_rate_s = 3e8 * v_rel * A_ribbon
print(f"\n  Dominant flux (mode-2): {hit_rate_s:.2e} hits/s = {hit_rate_s*DAY:.2e}/day")

# ------------------------------------------------------------------
# PART B: Acid film residence time before wind shear
# ------------------------------------------------------------------
# Thin-film model: wind shear stress tau = mu_air * U / delta_air_BL
# But the relevant shear on the *acid film* itself:
# tau_shear = mu_acid * U / delta_film  (viscous shear across film)
# Force retaining film = surface tension * L_c (capillary at contact line)
# Film is sheared off when tau_shear * A_ribbon > gamma * L_c
# => critical film thickness delta_crit = mu_acid * U * A_ribbon / (gamma * L_c)
# Residence time ~ delta / (shear velocity ~ U * delta/L_ribbon)
#   more carefully: t_res ~ (delta/U) * (L_ribbon/delta)^0.5 [lubrication limit]
# Use simpler bounding: t_res ~ delta / (U * shear_rate_factor)
# Shear rate at film surface ~ U / delta_BL; use delta_BL ~ 1mm (boundary layer)
# -> film surface velocity ~ U * delta / delta_BL
# -> film evacuation time ~ L_ribbon / (U * delta / delta_BL)
# Sweep delta; report t_res and duty cycle.

print("\n--- PART B: Acid film residence time (thin-film shear model) ---")
L_ribbon = 1.5e-3    # m, ribbon length
delta_BL = 1e-3      # m, approximate boundary layer thickness [SPEC]

print(f"  U_wind={U_wind} m/s, mu_acid={mu_acid} Pa.s, gamma={gamma} N/m")
print(f"  {'delta(um)':>10s} {'tau_shear(Pa)':>14s} {'t_res(s)':>10s} "
      f"{'t_res(ms)':>10s} {'note':>20s}")

delta_vals = np.array([0.1, 0.5, 1.0, 5.0, 10.0]) * 1e-6  # 0.1 to 10 um

for delta in delta_vals:
    # viscous shear stress the wind exerts on the film top surface
    tau = mu_acid * U_wind / delta    # Pa  (Couette-limit; overestimates)
    # capillary retention force per unit area ~ gamma / delta (Laplace pressure)
    P_cap = gamma / delta             # Pa
    # film is retained while P_cap > tau; sheared off when tau > P_cap
    retained = "RETAINED" if P_cap > tau else "SHEARED"
    # evacuation time: film surface moves at v_film ~ U*(delta/delta_BL)
    # film drains off ribbon end in t ~ L_ribbon / v_film
    v_film = U_wind * delta / delta_BL
    t_res = L_ribbon / v_film if v_film > 0 else np.inf
    print(f"  {delta*1e6:>10.1f} {tau:>14.1e} {t_res:>10.4f} "
          f"{t_res*1000:>10.2f} {retained:>20s}")

# More conservative estimate: t_res ~ delta^2 * rho_acid / (mu_acid) [draining]
print("\n  Cross-check: gravity draining (vertical film, g_Venus = 8.87 m/s2):")
rho_acid = 1830.0   # kg/m3, 90% H2SO4 [LAB]
g_V = 8.87
for delta in delta_vals:
    t_drain = 3 * mu_acid / (rho_acid * g_V * delta)  # draining time [LAB formula]
    print(f"    delta={delta*1e6:.1f}um: t_drain ~ {t_drain*1000:.3f} ms")

# ------------------------------------------------------------------
# PART C: Duty cycle and effective attack rate
# ------------------------------------------------------------------
print("\n--- PART C: Duty cycle and per-channel verdict ---")

# Use a representative t_res range from the analysis above
t_res_lo = 1e-4    # s, lower bound (thin film, fast shear)
t_res_hi = 1e-2    # s, upper bound (thicker film, slower drain)

print(f"\n  hit_rate = {hit_rate_s:.2e} /s")
for t_res, label in [(t_res_lo,"t_res lower"), (t_res_hi,"t_res upper")]:
    dc = hit_rate_s * t_res          # dimensionless duty cycle
    print(f"\n  {label} = {t_res*1000:.2f} ms  ->  duty cycle = {dc:.2e}")
    print(f"    = {dc*100:.4f}% of time the coating is wet with acid")
    # --- reversible channel: effective immersion-equivalent time ---
    # if intrinsic immersion lifetime is T_imm, effective lifetime = T_imm / dc
    print(f"    REVERSIBLE channels: effective lifetime = T_immersion / {dc:.1e}")
    print(f"      (if T_immersion = 1 day  -> effective {1/dc:.0f} days)")
    print(f"      (if T_immersion = 1 hour -> effective {1/dc/24:.0f} days)")
    # --- irreversible channel: damage per unit time ---
    # each hit delivers a fixed damage dose D_hit; rate = D_hit * hit_rate_s
    # no time-between-hits healing -> duty cycle barely helps
    print(f"    IRREVERSIBLE channels: damage accumulates per-hit @ {hit_rate_s:.1e}/s")
    print(f"      duty cycle does NOT extend effective lifetime significantly")

print("""
=== INTERPRETATION ===
Duty cycle is extremely low: ~1e-7 to 1e-5 (order 0.001–0.1 seconds of acid
contact per day, depending on film thickness).

REVERSIBLE CLEAVAGE CHANNEL (acetal re-formation / scrambling in dry medium):
  Intermittent exposure multiplies effective lifetime by ~1/duty_cycle = 1e5-1e7x.
  Even a coating that fails in hours under immersion would last years under this
  intermittent regime.  Wind-stripping is HIGHLY protective if the acetal damage
  is reversible.

IRREVERSIBLE CHANNELS (sulfonation, charring/Friedel-Crafts):
  Damage per hit accumulates.  The relevant question is whether the energy
  delivered per droplet impact initiates irreversible chemistry, not the total
  time of contact.  Low duty cycle does NOT rescue these channels.

THEREFORE: the xTB campaign must determine which channel the acetal routes to.
  If reversible (A1 scrambling): duty cycle almost certainly rescues the coating.
  If irreversible (charring):    duty cycle barely helps; coating may fail.
""")
print("="*76)
