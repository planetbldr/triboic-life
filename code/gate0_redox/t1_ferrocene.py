#!/usr/bin/env python
"""
T1 — Method calibration on ferrocene (Fc / Fc+)   [CHARGE-FIX REVISION]
Sealed-Core Tribowhip redox-core test plan, Step T1.

WHY THIS REVISION EXISTS
------------------------
The xtb-python ASE calculator does NOT read charge/uhf from its constructor
arguments. It reads them off the Atoms object:
    charge -> atoms.get_initial_charges().sum()
    uhf    -> atoms.get_initial_magnetic_moments().sum()
(see grimme-lab/xtb-python calculator.py and issue #58). The previous version
passed XTB(charge=1, uhf=1), which was silently ignored, so all three energies
came out identical (neutral computed three times) and the ionization energy was
0.000 eV. This version sets charge/spin ON THE ATOMS, and prints guard checks
that make a silent neutral-only run impossible to miss.

Run inside the `triboic` conda env. Paste full stdout back.
"""

import sys
import numpy as np

from ase import Atoms
from ase.optimize import BFGS
from xtb.ase.calculator import XTB

HARTREE_TO_EV = 27.211386245988


def build_ferrocene_fallback():
    """Idealized eclipsed (D5h) ferrocene built from geometry.
    xTB relaxes bond lengths; this is only a starting geometry."""
    symbols, pos = [], []
    r_c, r_h, z_ring = 1.21, 2.27, 1.66
    for sign in (+1, -1):
        for k in range(5):
            ang = 2 * np.pi * k / 5
            symbols.append("C")
            pos.append([r_c*np.cos(ang), r_c*np.sin(ang), sign*z_ring])
        for k in range(5):
            ang = 2 * np.pi * k / 5
            symbols.append("H")
            pos.append([r_h*np.cos(ang), r_h*np.sin(ang), sign*z_ring])
    symbols.append("Fe")
    pos.append([0.0, 0.0, 0.0])
    return Atoms(symbols=symbols, positions=np.array(pos))


def build_ferrocene():
    """RDKit-from-SMILES (plan default); fall back to idealized geometry.
    RDKit can't kekulize the organometallic sandwich, so in practice the
    fallback is used -- which is fine: it gives a clean 2.05 A start."""
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
        smiles = "[Fe]1234567([cH]8[cH]1[cH]2[cH]3[cH]48)[cH]1[cH]5[cH]6[cH]7[cH]1"
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("SMILES parse failed")
        mol = Chem.AddHs(mol)
        p = AllChem.ETKDGv3(); p.randomSeed = 0xC0FFEE
        if AllChem.EmbedMolecule(mol, p) != 0:
            raise ValueError("embed failed")
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
        conf = mol.GetConformer()
        symbols = [a.GetSymbol() for a in mol.GetAtoms()]
        return Atoms(symbols=symbols, positions=conf.GetPositions())
    except Exception as e:
        print(f"  [build] RDKit path unavailable ({e}); using idealized geometry.")
        return build_ferrocene_fallback()


def fe_ring_carbon_distances(atoms):
    sym = atoms.get_chemical_symbols()
    pos = atoms.get_positions()
    fe = pos[sym.index("Fe")]
    d = [np.linalg.norm(pos[i]-fe) for i, s in enumerate(sym) if s == "C"]
    return np.array(sorted(d))


def prep(atoms, charge, uhf):
    """Return a copy with charge/spin set the way xtb-python actually reads them."""
    a = atoms.copy()
    init = np.zeros(len(a)); init[0] = charge          # net charge -> initial_charges
    a.set_initial_charges(init)
    mag = np.zeros(len(a)); mag[0] = uhf               # unpaired electrons -> moments
    a.set_initial_magnetic_moments(mag)
    # guard: confirm what xtb will actually see
    seen_q = a.get_initial_charges().sum()
    seen_s = a.get_initial_magnetic_moments().sum()
    assert abs(seen_q - charge) < 1e-9, f"charge not set (saw {seen_q})"
    assert abs(seen_s - uhf) < 1e-9, f"uhf not set (saw {seen_s})"
    a.calc = XTB(method="GFN2-xTB")
    return a


def single_point(atoms, charge, uhf):
    a = prep(atoms, charge, uhf)
    return a.get_potential_energy()


def optimize(atoms, charge, uhf, label, fmax=0.05, steps=300):
    a = prep(atoms, charge, uhf)
    BFGS(a, logfile=None).run(fmax=fmax, steps=steps)
    e = a.get_potential_energy()
    print(f"  [opt {label}] charge={charge} uhf={uhf}  "
          f"E = {e:.6f} eV ({e/HARTREE_TO_EV:.6f} Ha)")
    return a, e


def main():
    print("="*64)
    print("T1 — Ferrocene Fc/Fc+ calibration  (GFN2-xTB)  [charge-fix]")
    print("="*64)

    print("\n[1] Building ferrocene (RDKit default, idealized fallback)...")
    fc0 = build_ferrocene()
    print(f"    atoms: {len(fc0)}  formula: {fc0.get_chemical_formula()}")
    d0 = fe_ring_carbon_distances(fc0)
    print(f"    pre-opt Fe-C (A): min {d0.min():.2f} max {d0.max():.2f} "
          f"(real ~2.04-2.07)")

    print("\n[2] Optimizing NEUTRAL Fc (charge 0, singlet)...")
    fc_opt, e_neu = optimize(fc0, 0, 0, "Fc")
    d1 = fe_ring_carbon_distances(fc_opt)
    print(f"    post-opt Fe-C (A): min {d1.min():.2f} max {d1.max():.2f} "
          f"mean {d1.mean():.2f}")
    if d1.max() > 3.5:
        print("    WARNING: ring carbon far from Fe -- sandwich may have broken.")

    print("\n[3] VERTICAL ionization: Fc+ single-point at neutral geom "
          "(charge +1, doublet)...")
    e_cat_vert = single_point(fc_opt, 1, 1)
    print(f"    E(Fc+ // Fc geom) = {e_cat_vert:.6f} eV")

    print("\n[4] ADIABATIC ionization: optimizing Fc+ (charge +1, doublet)...")
    _, e_cat_adi = optimize(fc_opt, 1, 1, "Fc+")

    ie_vert = e_cat_vert - e_neu
    ie_adi  = e_cat_adi - e_neu

    # ---- guard against the silent-neutral failure mode ----
    print("\n[guard] Sanity checks on the energies:")
    distinct = abs(e_cat_vert - e_neu) > 1e-3
    print(f"    cation != neutral?  {'YES' if distinct else 'NO -- CHARGE STILL IGNORED'}")
    if not distinct:
        print("    >>> The +1 run produced the neutral energy again. STOP and tell me;")
        print("    >>> the charge is still not reaching xtb on your build.")

    print("\n"+"="*64)
    print("RESULTS")
    print("="*64)
    print(f"  E(Fc, neutral, opt)    = {e_neu:.6f} eV")
    print(f"  E(Fc+, vertical)       = {e_cat_vert:.6f} eV")
    print(f"  E(Fc+, adiabatic, opt) = {e_cat_adi:.6f} eV")
    print(f"\n  Vertical  IE (Fc -> Fc+) = {ie_vert:.3f} eV")
    print(f"  Adiabatic IE (Fc -> Fc+) = {ie_adi:.3f} eV")
    print(f"  Relaxation (vert - adi)  = {ie_vert - ie_adi:.3f} eV")
    print("\n  Reference anchors (gas-phase ferrocene):")
    print("    experimental adiabatic IE ~ 6.7-6.9 eV (PES literature)")
    print("    Checking ORDERING + MAGNITUDE are sane (semi-empirical, gas phase),")
    print("    not chasing 3-decimal agreement.")
    print("="*64)


if __name__ == "__main__":
    sys.exit(main())
