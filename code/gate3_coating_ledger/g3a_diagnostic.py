#!/usr/bin/env python3
"""
Gate 3a DIAGNOSTIC v2 — can GFN2-xTB rank C-O heterolysis? (SCF-robust)

v1 crashed with "SCF did not converge" on methanol's first scan point. That is
the signature of xTB struggling with the charged, bond-breaking electronic
structure -- but it CAN sometimes be fixed with electronic-temperature smearing.
This version:
  * adds electronic_temperature (Fermi smearing) to aid SCF convergence on the
    near-degenerate charged/stretched species;
  * wraps every single point so one failed point -> NaN, never a crash;
  * tries each scan point at escalating smearing if the first attempt fails;
  * reports how many points converged, so we can tell "method works" from
    "method cannot converge this chemistry at all."

VERDICT LOGIC:
  - If scans converge AND reproduce t-butanol < isopropanol < ethanol < methanol
    -> method works; our fragment problem was geometry. Fixable.
  - If many points won't converge even with smearing, or the order is scrambled
    -> METHOD CEILING for charged C-O heterolysis. Stop; go to DFT (as the
       coating report advised).

Run in `triboic`. Paste stdout.
"""
import numpy as np
from ase import Atoms
from ase.optimize import BFGS
from ase.constraints import FixBondLength
from xtb.ase.calculator import XTB
from rdkit import Chem
from rdkit.Chem import AllChem

HARTREE_TO_EV = 27.211386245988

def lowest_conf(smi, n=20, seed=42):
    m = Chem.MolFromSmiles(smi); m = Chem.AddHs(m)
    cids = AllChem.EmbedMultipleConfs(m, numConfs=n, randomSeed=seed)
    if len(cids) == 0: AllChem.EmbedMolecule(m, randomSeed=seed); cids = [0]
    best = (1e30, cids[0])
    for c in cids:
        p = AllChem.MMFFGetMoleculeProperties(m)
        ff = AllChem.MMFFGetMoleculeForceField(m, p, confId=c)
        if ff: ff.Minimize(maxIts=2000); e = ff.CalcEnergy()
        if e < best[0]: best = (e, c)
    return m, best[1]

def get_sp(m, c):
    conf = m.GetConformer(c)
    sym = [a.GetSymbol() for a in m.GetAtoms()]
    pos = np.array([list(conf.GetAtomPosition(i)) for i in range(m.GetNumAtoms())])
    return sym, pos

def proton_index(sym, pos):
    o = [i for i, s in enumerate(sym) if s == "O"]
    best = (1e9, len(sym) - 1)
    for i, s in enumerate(sym):
        if s != "H": continue
        d = min(np.linalg.norm(pos[i] - pos[j]) for j in o)
        if 0.9 < d < 1.1 and d < best[0]: best = (d, i)
    return best[1]

def energy_fixed(sym, pos, charge, pair, etemp, fmax=0.08, steps=120):
    """Constrained relax + energy at a given electronic temperature.
    Returns energy in Hartree or None if it fails."""
    a = Atoms(symbols=sym, positions=pos)
    q = np.zeros(len(a))
    if charge != 0: q[proton_index(sym, pos)] = charge
    a.set_initial_charges(q); a.set_initial_magnetic_moments(np.zeros(len(a)))
    a.set_constraint([FixBondLength(*pair)])
    try:
        a.calc = XTB(method="GFN2-xTB", accuracy=1.0,
                     electronic_temperature=etemp, max_iterations=500)
        BFGS(a, logfile=None).run(fmax=fmax, steps=steps)
        return a.get_potential_energy() / HARTREE_TO_EV
    except Exception:
        return None

def energy_robust(sym, pos, charge, pair):
    """Try escalating electronic temperatures until SCF converges."""
    for etemp in [300.0, 1000.0, 3000.0, 6000.0]:
        e = energy_fixed(sym, pos, charge, pair, etemp)
        if e is not None:
            return e, etemp
    return None, None

def protonate_O(sym, pos, o_idx, nbrs):
    d = pos[o_idx] - nbrs.mean(axis=0); d /= np.linalg.norm(d) + 1e-9
    h = pos[o_idx] + 0.98 * d
    return sym + ["H"], np.vstack([pos, h])

def scan(smiles, c_idx, o_idx, label, r0=1.40, r1=3.10, n=14):
    m, c = lowest_conf(smiles); sym, pos = get_sp(m, c)
    o_atom = m.GetAtomWithIdx(o_idx)
    nbrs = np.array([pos[nb.GetIdx()] for nb in o_atom.GetNeighbors()])
    symp, posp = protonate_O(sym, pos, o_idx, nbrs)
    rs = np.linspace(r0, r1, n); Es = []; etemps = []; n_conv = 0
    for r in rs:
        p = posp.copy()
        v = p[o_idx] - p[c_idx]; nn = np.linalg.norm(v)
        if nn > 1e-3: p[o_idx] = p[c_idx] + v / nn * r
        e, et = energy_robust(symp, p, 1, (c_idx, o_idx))
        if e is None:
            Es.append(np.nan); etemps.append(None)
        else:
            Es.append(e); etemps.append(et); n_conv += 1
    Es = np.array(Es, dtype=float)
    if np.all(np.isnan(Es)):
        return np.nan, 0, len(rs)
    e0 = Es[np.where(~np.isnan(Es))[0][0]]
    dE = (Es - e0) * HARTREE_TO_EV
    dE = np.where(np.abs(dE) > 10, np.nan, dE)
    return np.nanmax(dE), n_conv, len(rs)

print("=" * 72)
print("DIAGNOSTIC v2 (SCF-robust): can GFN2-xTB rank C-O heterolysis?")
print("Known SN1 order: t-butanol < isopropanol < ethanol < methanol")
print("=" * 72)

cases = [
    ("methanol",    "CO",         0, 1),
    ("ethanol",     "CCO",        1, 2),
    ("isopropanol", "CC(C)O",     1, 3),
    ("t-butanol",   "CC(C)(C)O",  1, 4),
]

results = []
for name, smi, ci, oi in cases:
    bar, nconv, ntot = scan(smi, ci, oi, name)
    results.append((name, bar, nconv, ntot))
    status = "OK" if nconv == ntot else f"{nconv}/{ntot} converged"
    print(f"  {name:12s}: barrier = {bar:+.3f} eV   ({status})")

print("\n" + "=" * 72)
print("VERDICT")
print("=" * 72)
valid = [(n, b) for n, b, nc, nt in results if not np.isnan(b)]
total_conv = sum(nc for _, _, nc, _ in results)
total_pts = sum(nt for _, _, _, nt in results)
print(f"  SCF convergence: {total_conv}/{total_pts} scan points")

if len(valid) < 4:
    print("\n  RESULT: xTB could not converge several heterolysis points even with")
    print("  electronic-temperature smearing up to 6000 K.")
    print("  => METHOD CEILING. GFN2-xTB cannot reliably treat this charged C-O")
    print("     heterolysis. Stop here; the committed cleavage steps need DFT,")
    print("     exactly as the coating report (1.4 'Method suitability') advised.")
else:
    order = [n for n, _ in sorted(valid, key=lambda x: x[1])]
    print(f"  xTB order (easiest->hardest): {' < '.join(order)}")
    print(f"  EXPECTED                    : t-butanol < isopropanol < ethanol < methanol")
    if order == ["t-butanol", "isopropanol", "ethanol", "methanol"]:
        print("\n  RESULT: EXACT match. Method works for ranking.")
        print("  => Step 1/2 problem was GEOMETRY in our fragments. Fixable; rebuild & rerun.")
    elif order[0] == "t-butanol" and order[-1] in ("methanol", "ethanol"):
        print("\n  RESULT: trend roughly right (tertiary easiest, methyl/ethyl hardest).")
        print("  => Method usable for RANKING; tighten fragment geometries.")
    else:
        print("\n  RESULT: order SCRAMBLED vs known chemistry.")
        print("  => METHOD CEILING for charged C-O heterolysis ranking. Go to DFT.")
print("=" * 72)
