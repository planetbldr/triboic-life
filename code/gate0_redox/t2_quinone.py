#!/usr/bin/env python
"""
T2 — Quinone redox energetics (the core electronic test)
Sealed-Core Tribowhip redox-core test plan, Step T2.

QUESTION
--------
Does a biological quinone have electron-accepting energetics consistent with
acting as the tribonegative charge-trap in the gel core?

WHAT IT COMPUTES (thorough version)
-----------------------------------
For each molecule, the full redox/protonation ladder:
    Q  (neutral)           charge  0, singlet
    Q-* (semiquinone)      charge -1, doublet   <- 1e- radical anion
    Q2- (dianion)          charge -2, singlet   <- 2e- (gas-phase: often unbound!)
    QH* (neutral semiq.)   protonated 1e- form  (added H)         [PROTON-COUPLED]
    QH2 (hydroquinone)     protonated 2e- form  (added 2 H)       [PROTON-COUPLED]
plus VERTICAL and ADIABATIC electron affinities (anion @ neutral geom vs relaxed),
plus implicit solvent (ALPB) on charged states, plus multi-conformer sampling.

MOLECULES
---------
  benzoquinone     -- ANCHOR. Known gas-phase adiabatic EA ~1.86 eV (NIST).
                      Doubles as the organic calibration reference (T1 showed
                      xTB absolute redox energies are unreliable; benzoquinone
                      is the like-for-like organic anchor the metallocene wasn't).
  1,4-naphthoquinone -- CANDIDATE, menaquinone (vitamin K2) class head group.

HONEST LIMITATIONS (NOT fixable with more compute -- see chat):
  1. GFN2-xTB absolute-redox-energy ceiling (T1: ferrocene IP +4.5 eV high).
     -> read everything COMPARATIVELY, anchored to benzoquinone.
  2. Gas-phase dianion is often genuinely unbound; its energy is partly artifact.
     -> script FLAGS this explicitly (positive 2nd-EA = unbound).
  3. Gas-phase + implicit solvent is a MODEL of a condensed ionic-liquid gel.
  4. Open-shell semiquinone may carry multireference character xTB misses.

Run in the `triboic` env. Paste full stdout back.
"""

import sys, itertools
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from ase import Atoms
from ase.optimize import BFGS
from xtb.ase.calculator import XTB

HARTREE_TO_EV = 27.211386245988

MOLS = {
    "benzoquinone (ANCHOR)":  "O=C1C=CC(=O)C=C1",
    "1,4-naphthoquinone (CANDIDATE)": "O=C1C=CC(=O)c2ccccc12",
}

# Reference anchors (gas-phase, experimental, for COMPARATIVE reading only)
EA_REF = {
    "benzoquinone (ANCHOR)": 1.86,   # eV, adiabatic EA, well established (NIST)
    "1,4-naphthoquinone (CANDIDATE)": 1.81,  # eV, literature ~1.7-1.8
}


def conformers(smiles, n=8, seed=0xC0FFEE):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    p = AllChem.ETKDGv3(); p.randomSeed = seed
    cids = AllChem.EmbedMultipleConfs(m, numConfs=n, params=p)
    AllChem.MMFFOptimizeMoleculeConfs(m, maxIters=1000)
    syms = [a.GetSymbol() for a in m.GetAtoms()]
    out = []
    for c in cids:
        out.append(Atoms(symbols=syms, positions=m.GetConformer(c).GetPositions()))
    return out


def protonate(smiles, n_h):
    """Add n_h protons to carbonyl O's -> semiquinone(QH)/hydroquinone(QH2) skeleton.
    We build the protonated SMILES directly for the 1,4 quinones."""
    table = {
        ("O=C1C=CC(=O)C=C1", 1): "OC1=CC=C([O])C=C1",      # benzo semiquinone radical (QH*)
        ("O=C1C=CC(=O)C=C1", 2): "Oc1ccc(O)cc1",            # hydroquinone (QH2)
        ("O=C1C=CC(=O)c2ccccc12", 1): "OC1=CC=C([O])c2ccccc12",  # naphtho semiquinone
        ("O=C1C=CC(=O)c2ccccc12", 2): "Oc1ccc(O)c2ccccc12",      # naphthohydroquinone
    }
    return table.get((smiles, n_h))


def set_state(atoms, charge, uhf):
    a = atoms.copy()
    q = np.zeros(len(a)); q[0] = charge; a.set_initial_charges(q)
    s = np.zeros(len(a)); s[0] = uhf;    a.set_initial_magnetic_moments(s)
    assert abs(a.get_initial_charges().sum()-charge) < 1e-9
    assert abs(a.get_initial_magnetic_moments().sum()-uhf) < 1e-9
    return a


def calc(atoms, charge, uhf, solvent=None):
    a = set_state(atoms, charge, uhf)
    kw = dict(method="GFN2-xTB")
    if solvent:
        kw["solvent"] = solvent
    a.calc = XTB(**kw)
    return a


def sp(atoms, charge, uhf, solvent=None):
    return calc(atoms, charge, uhf, solvent).get_potential_energy()


def opt(atoms, charge, uhf, solvent=None, fmax=0.05, steps=500):
    a = calc(atoms, charge, uhf, solvent)
    BFGS(a, logfile=None).run(fmax=fmax, steps=steps)
    return a, a.get_potential_energy()


def best_conformer_opt(confs, charge, uhf, solvent=None):
    """Optimize every conformer in the given electronic state; return lowest E."""
    best_e, best_a = None, None
    for c in confs:
        a, e = opt(c, charge, uhf, solvent)
        if best_e is None or e < best_e:
            best_e, best_a = e, a
    return best_a, best_e


def run_molecule(name, smiles):
    print("\n" + "=" * 68)
    print(f"MOLECULE: {name}")
    print(f"SMILES:   {smiles}")
    print("=" * 68)

    confs = conformers(smiles, n=8)
    print(f"  generated {len(confs)} conformers")

    # --- Neutral (gas phase; this is the reference geometry) ---
    neu_a, e_neu = best_conformer_opt(confs, 0, 0)
    print(f"  [Q   ] neutral      opt E = {e_neu:.4f} eV  (gas)")

    # --- 1e- radical anion: vertical (anion @ neutral geom) and adiabatic ---
    e_an_vert = sp(neu_a, -1, 1)                       # gas, vertical
    an_a, e_an_adi = opt(neu_a, -1, 1)                 # gas, adiabatic
    e_an_adi_solv = opt(neu_a, -1, 1, solvent="acetonitrile")[1]  # implicit solvent (acetonitrile ~ IL-gel dielectric)
    ea1_vert = e_neu - e_an_vert      # EA = E(neutral) - E(anion); +ve = bound
    ea1_adi  = e_neu - e_an_adi
    print(f"  [Q-* ] anion vert   E = {e_an_vert:.4f}   EA1_vert = {ea1_vert:+.3f} eV")
    print(f"  [Q-* ] anion adiab  E = {e_an_adi:.4f}   EA1_adi  = {ea1_adi:+.3f} eV")
    print(f"  [Q-* ] anion adiab (implicit solvent) E = {e_an_adi_solv:.4f} eV")

    # --- 2e- dianion (gas-phase: often UNBOUND -> flag) ---
    di_a, e_di = opt(neu_a, -2, 0)
    e_di_solv  = opt(neu_a, -2, 0, solvent="acetonitrile")[1]
    ea2_adi = e_an_adi - e_di          # 2nd electron affinity; -ve(=E goes up) => unbound
    print(f"  [Q2- ] dianion gas  E = {e_di:.4f}   2nd-EA = {ea2_adi:+.3f} eV "
          f"{'<-- UNBOUND in gas (artifact-prone)' if ea2_adi < 0 else ''}")
    print(f"  [Q2- ] dianion (implicit solvent) E = {e_di_solv:.4f} eV "
          f"(solvent should stabilize the 2nd electron)")

    # --- Proton-coupled forms (the species that actually exist in the gel) ---
    for nh, lbl in [(1, "QH*  semiquinone"), (2, "QH2  hydroquinone")]:
        psm = protonate(smiles, nh)
        if psm:
            pc = conformers(psm, n=6)
            uhf = 1 if nh == 1 else 0
            _, e_p = best_conformer_opt(pc, 0, uhf)
            print(f"  [{lbl}] protonated  opt E = {e_p:.4f} eV  (gas)")

    # --- HOMO-LUMO gap / LUMO (electron-accepting level) on the neutral ---
    a = calc(neu_a, 0, 0)
    a.get_potential_energy()
    try:
        # xtb-python exposes orbital energies via results dict if available
        res = a.calc.results
        homo_lumo = res.get("homo_lumo_gap", None)
    except Exception:
        homo_lumo = None
    print(f"  HOMO-LUMO gap (if exposed): {homo_lumo}")

    return dict(name=name, e_neu=e_neu,
                ea1_vert=ea1_vert, ea1_adi=ea1_adi, ea2=ea2_adi)


def main():
    print("=" * 68)
    print("T2 — Quinone redox energetics  (GFN2-xTB, thorough)")
    print("  READ COMPARATIVELY. Absolute values carry the T1 xTB ceiling.")
    print("=" * 68)

    results = {}
    for name, smi in MOLS.items():
        results[name] = run_molecule(name, smi)

    print("\n" + "=" * 68)
    print("COMPARATIVE SUMMARY  (the part that actually decides T2)")
    print("=" * 68)
    print(f"{'molecule':<34}{'EA1_adi(xTB)':>14}{'EA1_ref(exp)':>14}")
    for name, r in results.items():
        ref = EA_REF.get(name, float('nan'))
        print(f"{name:<34}{r['ea1_adi']:>+14.3f}{ref:>14.3f}")
    print("\nReading guide:")
    print("  * Benzoquinone is the ANCHOR: compare its xTB EA1 to ~1.86 eV exp.")
    print("    A consistent offset there tells us xTB's organic-EA bias, which")
    print("    we then subtract out when reading the naphthoquinone candidate.")
    print("  * PASS (comparative): candidate EA1 >= benzoquinone-class acceptor")
    print("    level AND positive (binds the electron) => can trap charge.")
    print("  * The dianion / 2nd-EA is the LEAST trustworthy number (gas-phase")
    print("    unbound-electron artifact); weight the implicit-solvent value and")
    print("    the proton-coupled QH2 form instead for the 2e- story.")
    print("=" * 68)


if __name__ == "__main__":
    sys.exit(main())
