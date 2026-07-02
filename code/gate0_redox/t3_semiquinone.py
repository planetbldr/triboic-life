#!/usr/bin/env python
"""
T3 — Two-electron / semiquinone stability (the 2e<->1e bridge)
Sealed-Core Tribowhip redox-core test plan, Step T3.

QUESTION
--------
Is the one-electron semiquinone intermediate thermodynamically stable enough
to support a stepwise 2e<->1e handoff (favoring the I2-c biological cascade),
or does it disproportionate (favoring a pure 2e- capacitive mode, I2-a)?

DISPROPORTIONATION:   2 SQ  ->  Q  +  Q(2e-reduced)
  bare-anion form:    2 Q-* ->  Q  +  Q2-          (gas Q2- is artifact-prone)
  proton-coupled:     2 QH* ->  Q  +  QH2          (TRUSTWORTHY -- no bare dianion)

  dE_disp = E(Q) + E(reduced)  -  2*E(SQ)
    dE_disp >> 0  : disproportionation UNFAVORABLE -> semiquinone STABLE
                    -> comparable 1e- steps -> stepwise cascade (I2-c) viable
    dE_disp << 0  : disproportionation FAVORABLE   -> semiquinone UNSTABLE
                    -> clean 2e- capacitive mode (I2-a) preferred

  INFORMATIVE EITHER WAY (per the test plan) -- not pass/fail.

This script RECOMPUTES the needed states (cheap) so it is self-contained and
does not depend on T2 having cached anything. It mirrors T2's settings exactly
(same SMILES, same charge/spin handling, same solvent) so energies are
comparable. Run in the `triboic` env. Paste full stdout.
"""

import sys
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from ase import Atoms
from ase.optimize import BFGS
from xtb.ase.calculator import XTB

MOLS = {
    "benzoquinone (ANCHOR)": {
        "Q":   "O=C1C=CC(=O)C=C1",
        "QH":  "OC1=CC=C([O])C=C1",   # neutral semiquinone radical (protonated 1e-)
        "QH2": "Oc1ccc(O)cc1",        # hydroquinone (protonated 2e-)
    },
    "1,4-naphthoquinone (CANDIDATE)": {
        "Q":   "O=C1C=CC(=O)c2ccccc12",
        "QH":  "OC1=CC=C([O])c2ccccc12",
        "QH2": "Oc1ccc(O)c2ccccc12",
    },
}


def conformers(smiles, n=8, seed=0xC0FFEE):
    m = Chem.AddHs(Chem.MolFromSmiles(smiles))
    p = AllChem.ETKDGv3(); p.randomSeed = seed
    cids = AllChem.EmbedMultipleConfs(m, numConfs=n, params=p)
    AllChem.MMFFOptimizeMoleculeConfs(m, maxIters=1000)
    syms = [a.GetSymbol() for a in m.GetAtoms()]
    return [Atoms(symbols=syms, positions=m.GetConformer(c).GetPositions())
            for c in cids]


def set_state(atoms, charge, uhf):
    a = atoms.copy()
    q = np.zeros(len(a)); q[0] = charge; a.set_initial_charges(q)
    s = np.zeros(len(a)); s[0] = uhf;    a.set_initial_magnetic_moments(s)
    assert abs(a.get_initial_charges().sum() - charge) < 1e-9
    assert abs(a.get_initial_magnetic_moments().sum() - uhf) < 1e-9
    return a


def opt(atoms, charge, uhf, solvent=None, fmax=0.05, steps=500):
    a = set_state(atoms, charge, uhf)
    kw = dict(method="GFN2-xTB")
    if solvent:
        kw["solvent"] = solvent
    a.calc = XTB(**kw)
    BFGS(a, logfile=None).run(fmax=fmax, steps=steps)
    return a.get_potential_energy()


def best(smiles, charge, uhf, solvent=None, n=8):
    return min(opt(c, charge, uhf, solvent) for c in conformers(smiles, n))


def run(name, sm):
    print("\n" + "=" * 68)
    print(f"MOLECULE: {name}")
    print("=" * 68)

    # --- Energies needed for the three disproportionation routes ---
    # Bare-anion route (gas + solvent):
    e_Q_gas   = best(sm["Q"], 0,  0)
    e_SQ_gas  = best(sm["Q"], -1, 1)         # radical anion semiquinone, gas
    e_Q2_gas  = best(sm["Q"], -2, 0)         # dianion, gas (artifact-prone)
    e_SQ_solv = best(sm["Q"], -1, 1, "acetonitrile")
    e_Q2_solv = best(sm["Q"], -2, 0, "acetonitrile")
    e_Q_solv  = best(sm["Q"], 0,  0, "acetonitrile")

    # Proton-coupled route (the trustworthy one): neutral QH* and QH2
    e_QH  = best(sm["QH"],  0, 1)            # neutral semiquinone radical
    e_QH2 = best(sm["QH2"], 0, 0)            # hydroquinone

    # --- Disproportionation energies: 2 SQ -> Q + reduced ---
    d_gas  = (e_Q_gas  + e_Q2_gas)  - 2 * e_SQ_gas
    d_solv = (e_Q_solv + e_Q2_solv) - 2 * e_SQ_solv
    d_pc   = (e_Q_gas  + e_QH2)      - 2 * e_QH      # proton-coupled

    print(f"  E(Q)  gas         = {e_Q_gas:.4f} eV")
    print(f"  E(SQ) gas (Q-*)   = {e_SQ_gas:.4f} eV")
    print(f"  E(Q2-) gas        = {e_Q2_gas:.4f} eV   (artifact-prone)")
    print(f"  E(SQ) solv        = {e_SQ_solv:.4f} eV")
    print(f"  E(Q2-) solv       = {e_Q2_solv:.4f} eV")
    print(f"  E(QH*) neutral SQ = {e_QH:.4f} eV")
    print(f"  E(QH2) hydroq.    = {e_QH2:.4f} eV")
    print(f"\n  dE_disp  (bare anion, GAS)      = {d_gas:+.3f} eV   "
          f"{'[artifact-tainted]' }")
    print(f"  dE_disp  (bare anion, SOLVENT)  = {d_solv:+.3f} eV")
    print(f"  dE_disp  (PROTON-COUPLED) ***   = {d_pc:+.3f} eV   <-- trust this one")

    def verdict(d):
        if d > 0.3:
            return "STABLE semiquinone -> stepwise cascade (I2-c) viable"
        if d < -0.3:
            return "UNSTABLE semiquinone -> 2e- capacitive mode (I2-a) preferred"
        return "BORDERLINE -> both mechanisms accessible; weakly defined well"

    print(f"\n  -> proton-coupled reading: {verdict(d_pc)}")
    return dict(name=name, d_gas=d_gas, d_solv=d_solv, d_pc=d_pc)


def main():
    print("=" * 68)
    print("T3 — Semiquinone stability / disproportionation  (GFN2-xTB)")
    print("  INFORMATIVE, not pass/fail: tells us WHICH coupling mechanism")
    print("  the chemistry prefers (stepwise cascade vs 2e- capacitive).")
    print("=" * 68)

    res = {name: run(name, sm) for name, sm in MOLS.items()}

    print("\n" + "=" * 68)
    print("SUMMARY — disproportionation energy  2 SQ -> Q + reduced")
    print("=" * 68)
    print(f"{'molecule':<34}{'gas':>9}{'solvent':>10}{'proton-coupled':>16}")
    for name, r in res.items():
        print(f"{name:<34}{r['d_gas']:>+9.2f}{r['d_solv']:>+10.2f}"
              f"{r['d_pc']:>+16.2f}")
    print("\nReading guide:")
    print("  positive  -> semiquinone STABLE (well-defined 1e- intermediate)")
    print("               => stepwise 2e<->1e cascade (I2-c) is chemically open")
    print("  negative  -> semiquinone UNSTABLE (disproportionates)")
    print("               => pure 2e- capacitive coupling (I2-a) preferred")
    print("  Trust the PROTON-COUPLED column most (avoids the bare gas-phase")
    print("  dianion artifact flagged in T2). Gas column is shown for contrast.")
    print("=" * 68)


if __name__ == "__main__":
    sys.exit(main())
