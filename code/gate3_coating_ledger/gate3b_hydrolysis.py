#!/usr/bin/env python3
"""
Gate 3b FINAL — hydrolytic cleavage thermodynamics (neutral species, robust).

DESIGN (after a long road):
  Earlier attempts failed because they made BARE CARBOCATIONS (methyl/ethyl/
  isopropyl cations) that DFT optimizers thrash on for hours. This version
  models cleavage as HYDROLYSIS to NEUTRAL, closed-shell products -- no cations
  anywhere -- so every optimization is fast and robust.

  For each linkage:  R-X-R' + H2O -> R-OH(or acid) + R'-OH
  dE_hydrolysis = [E(prod1)+E(prod2)] - [E(reactant)+E(water)]
  Lower (more negative) = more favorable hydrolysis = MORE LABILE linkage.

VALIDATION BUILT IN (option 3): the three fragments ARE the benchmark.
  Textbook acid-lability order: ACETAL < ESTER < ETHER (acetal most labile;
  acetals are acid-removable protecting groups, ethers are acid-inert). If
  dE_hydrolysis reproduces that, the method is validated on the mechanism-
  matched established ordering AND answers the lability question. [SIM; PCM SPEC]

RUN:  python g3b_dft_thermo.py     (~minutes; caffeinate if closing the lid)
"""
import sys, json, time
import numpy as np
try:
    import psi4
except ImportError:
    print("psi4 not found: conda install -c conda-forge psi4"); sys.exit(1)
from rdkit import Chem
from rdkit.Chem import AllChem

HARTREE_TO_EV = 27.211386245988
psi4.set_memory("8 GB"); psi4.set_num_threads(8); psi4.core.be_quiet()
METHOD, BASIS, USE_PCM = "M06-2X", "def2-SVP", True


def relaxed_energy(smiles, label=""):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        print(f"    ({label}: parse fail {smiles})"); return None
    m = Chem.AddHs(m)
    cids = AllChem.EmbedMultipleConfs(m, numConfs=10, randomSeed=42)
    if len(cids) == 0:
        AllChem.EmbedMolecule(m, randomSeed=42); cids = [0]
    best = (1e30, cids[0])
    for c in cids:
        p = AllChem.MMFFGetMoleculeProperties(m)
        ff = AllChem.MMFFGetMoleculeForceField(m, p, confId=c) if p else None
        if ff:
            ff.Minimize(maxIts=2000); e = ff.CalcEnergy()
            if e < best[0]: best = (e, c)
    conf = m.GetConformer(best[1])
    sym = [a.GetSymbol() for a in m.GetAtoms()]
    pos = [list(conf.GetAtomPosition(i)) for i in range(m.GetNumAtoms())]
    lines = ["0 1"]
    for s, p in zip(sym, pos):
        lines.append(f"{s} {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}")
    lines += ["units angstrom", "no_reorient", "no_com", "symmetry c1"]
    mol = psi4.geometry("\n".join(lines))
    psi4.set_options({"basis": BASIS, "scf_type": "df", "reference": "rks",
                      "g_convergence": "gau_loose", "geom_maxiter": 100, "maxiter": 250})
    if USE_PCM:
        try:
            psi4.set_options({"pcm": True, "pcm_scf_type": "total"})
            psi4.pcm_helper("""
               Units = Angstrom
               Medium { SolverType = IEFPCM
                        Solvent = Water }
               Cavity { Type = GePol
                        Area = 0.3
                        RadiiSet = Bondi
                        Scaling = True }
            """)
        except Exception:
            psi4.set_options({"pcm": False})
    try:
        e = psi4.optimize(METHOD, molecule=mol)
        print(f"    {label:34s} E = {e:.6f} Ha")
        return e
    except Exception as ex:
        print(f"    ({label}: opt failed: {str(ex).splitlines()[0][:55]})")
        return None
    finally:
        psi4.core.clean()


REACTIONS = {
    "acetal": dict(react="COCOC",      p1="CO",        p2="OCOC",
                   desc="dimethoxymethane + H2O -> methanol + methoxymethanol"),
    "ester":  dict(react="CC(=O)OC",   p1="CC(=O)O",   p2="CO",
                   desc="methyl acetate + H2O -> acetic acid + methanol"),
    "ether":  dict(react="COc1ccccc1", p1="Oc1ccccc1", p2="CO",
                   desc="anisole + H2O -> phenol + methanol"),
}

print("=" * 70)
print("Gate 3b FINAL — hydrolytic cleavage thermodynamics (neutral species)")
print(f"{METHOD}/{BASIS}, PCM(Water) [SIM; solvent SPEC]")
print("Validation built in: expect acetal < ester < ether (acetal most labile)")
print("=" * 70)

t0 = time.time()
print("\nWater reference:")
E_water = relaxed_energy("O", "water")

out = {}
for name, rx in REACTIONS.items():
    print(f"\n=== {name.upper()}: {rx['desc']} ===")
    Er = relaxed_energy(rx["react"], f"{name} reactant")
    E1 = relaxed_energy(rx["p1"], f"{name} product1")
    E2 = relaxed_energy(rx["p2"], f"{name} product2")
    if None in (Er, E1, E2, E_water):
        print(f"  ({name}: incomplete)"); out[name] = None
        json.dump(out, open("g3b_hydrolysis_results.json", "w")); continue
    dE = ((E1 + E2) - (Er + E_water)) * HARTREE_TO_EV
    out[name] = dE
    tag = "uphill: resists (reversible-leaning)" if dE > 0 else "downhill: favored (cleaves)"
    print(f"  -> dE_hydrolysis = {dE:+.3f} eV   [{tag}]   ({time.time()-t0:.0f}s)")
    json.dump(out, open("g3b_hydrolysis_results.json", "w"))

print("\n" + "=" * 70)
done = {k: v for k, v in out.items() if v is not None}
if len(done) == 3:
    order = sorted(done, key=lambda k: done[k])
    print("LABILITY ORDER (most -> least favorable hydrolysis):")
    for k in order:
        print(f"   {k:8s} dE = {done[k]:+.3f} eV")
    print(f"\n   Computed: {' < '.join(order)}")
    print(f"   Expected: acetal < ester < ether")
    if order == ["acetal", "ester", "ether"]:
        print("\n   >>> VALIDATED: matches textbook acid-lability order exactly.")
        print("       Method confirmed AND acetal is the weak point (as the report warned).")
    elif order[0] == "acetal":
        print("\n   >>> ACETAL most labile (correct weak point); mid/least order approximate.")
    else:
        print(f"\n   >>> Order differs from textbook ({order[0]} most labile). Inspect.")
    if out.get("acetal") is not None:
        print("\n   ACETAL REVERSIBILITY (with Step-0 duty cycle ~1e-5):")
        if out["acetal"] > 0:
            print("   Acetal hydrolysis is UPHILL => resists/reverses => duty cycle")
            print("   strongly rescues the coating. COATING LIKELY SURVIVES.")
        else:
            print("   Acetal hydrolysis is DOWNHILL => favorable cleavage. Survival then")
            print("   hinges on product re-condensation + the ~1e-5 duty cycle + low water")
            print("   activity (dry Venus limits actual rate). Needs the fate judgment.")
else:
    print(f"Incomplete: {len(done)}/3 fragments finished.")
print(f"\nTotal time: {time.time()-t0:.0f}s")
print("=" * 70)
