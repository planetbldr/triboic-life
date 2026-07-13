# Adjunct: Sulfur Chemistry, Electric Current, and Two Triboic Creatures

**An action document. What is already demonstrated on Earth, what is not yet known, and the specific bench and field work that would let someone design either of two sulfur-powered triboic creatures.**

*A supplement to "Life Powered Like Lightning" and the Triboic Life Technical Companion (Report B), extending the catalogue entries in The Triboic Frontier. It is a direction, not a result. Nothing here is a claim that either creature exists.*

---

## Purpose and how to read this

Two of the triboic candidates run on sulfur: the Venus sulfur creature and the deep-sea vent creature. Both are **tribochemoautotrophs**, a sluggish sulfur redox metabolism with a triboelectric current supplement paying for the complexity the chemistry alone cannot fund. They share one foundation, a real terrestrial demonstration that a sulfur cycle and an electric current already operate together on an electrode. Past that foundation they diverge sharply, and the divergence is the useful finding: one faces a long chemistry-benchmark road, the other a short observational one.

This document is organized around what is **not yet known**. Each section states what is demonstrated, then lists the open items and the kind of work (wet lab, bench electrochemistry, field survey, culturing) that would close them. Two items, one per creature, are flagged as the most likely to be tested by real science in the near term.

**Evidence tiers**, applied to every load-bearing claim, following the project convention:

- **[LAB]** traceable to a published laboratory or field result. Where load-bearing, the primary paper is cited.
- **[SIM]** computed in the project environment.
- **[SPEC]** reasoned, no empirical anchor.
- **[SPEC-CHOICE]** a modeling choice that was justified but not derived.

A tag travels with its claim. A [SPEC] is never promoted to fact by appearing in a confident sentence. Two disciplines from the project apply throughout. First, numeric optima do not generalize: where the literature reports a best-performing electrode potential, it is organism- and system-specific, so the honest claim is that applied potential tunes a metabolism, never that the optimum is a transferable number. Second, citations were checked against primaries in a verification pass; anything not confirmable is marked **[citation needs verification]** rather than presented as settled.

---

## PART A — The shared foundation

### A1. A sulfur cycle and a current already run together on an electrode [LAB]

The foundation both creatures stand on is demonstrated, not speculated. In benthic and sediment microbial fuel cells, and in engineered bioelectrochemical desulfurization used for wastewater and gas treatment, a microbial sulfur cycle transfers electrons to an electrode as current.

The cycle has two halves. Sulfate-reducing bacteria (SRB) reduce sulfate to sulfide using organic carbon. Sulfide-oxidizing bacteria (SOB) then oxidize that sulfide back toward elemental sulfur, and the electrons released can be routed to an anode. A co-biofilm of the two runs sulfate to sulfide to S⁰ with electron transfer to the electrode [LAB, Lee et al. 2014, and a 2012 precursor; citation needs verification on exact volume/pages]. Sulfide-oxidizing communities drawn from desulfurization reactors shuttle electrons from sulfide directly to an anode at measurable current densities, on the order of 0.2 to 0.5 A/m² in the reported systems [LAB, de Rink et al. 2018]. The point is not any single current figure, which is system-specific, but that the sulfur cycle closes through an electrode at all.

The electron-transfer machinery is the same extracellular electron transfer (EET) studied in the canonical electrogens. *Geobacter sulfurreducens* respires an electrode as its sole electron acceptor [LAB, Bond and Lovley 2003]. Directly relevant to the sulfur case, EET has been characterized in a model sulfate-reducing bacterium, *Desulfovibrio vulgaris* Hildenborough, which was shown in microbial fuel cells to transfer electrons to a carbon electrode by both direct and indirect (shuttle-mediated) routes operating together during dissimilatory sulfate reduction [LAB, Hou et al. 2024]. (The paper reports co-occurring direct and indirect transfer; it does not resolve the full molecular identity of either route, noting that no outer-membrane c-type cytochromes of this organism have yet been identified, so the specific carriers should not be overstated.) This is the terrestrial anchor most important to the vent creature, because it is ordinary anoxic-water sulfur chemistry doing exactly the electron export the vent design assumes, in the applied setting of sulfate-containing wastewater treatment.

Two caveats belong with the foundation, not beneath it. First, in SRB-only anodes a substantial part of the current can come from abiotic oxidation of the biologically produced sulfide, so biology makes the sulfide and chemistry sometimes makes the electron [LAB, bioelectrochemical-systems reviews; citation needs verification]. Second, elemental sulfur deposited at an electrode tends to passivate it and block further current, a recurring failure mode in sulfur bioelectrochemistry [LAB, sulfide-oxidation literature; citation needs verification]. The foundation shows the coupling can be built and run in real systems. It does not show it runs cleanly or without cost.

**What A1 establishes.** In ordinary water, at near-neutral pH, a sulfur cycle and an electric current operate together on an electrode using known organisms and known EET machinery, in systems already deployed for wastewater and gas treatment. That is the floor. The two creatures differ in how far their target environment sits from it.

### A2. Why the current matters energetically [LAB, then SPEC for the extrapolation]

Sulfur-based energy metabolisms are low-yield. Sulfate reduction in particular sits near the bottom of the redox tower, with a small free-energy change per electron relative to aerobic respiration or denitrification [LAB, Thauer, Jungermann and Decker 1977]. Organisms living this low grow slowly because little energy is available per reaction. That is the metabolic gap a triboelectric supplement is meant to close.

The demonstrated effect is that poising the anode potential changes microbial activity. Controlling the anode potential sets both the theoretical energy available to the organisms and the electrical output; in a continuous acetate-fed system, the reactor held at the more favorable potential produced about 15% more charge over a 31-day run, though all three reactors converged to the same power density by the end [LAB, Aelterman et al. 2008]. In a sulfur-lineage organism, *Desulfuromonas acetexigens* (a dissimilatory sulfur reducer), anode potential strongly affected current and coulombic efficiency and shifted expression of the outer-membrane cytochromes that carry EET [LAB, Sysoev et al. 2025].

Two qualifications travel with this, and they are the reason it is a foundation and not a result:

- **The optima do not generalize.** Across these studies the best operating potential ranges widely with organism and system (the acetate study centered near −200 mV vs Ag/AgCl; the *D. acetexigens* study peaked near −0.4 V vs Ag/AgCl), and in the acetate study the potential advantage disappeared by the end of the run. "Applied potential tunes the metabolism" is [LAB]. "The optimum is a specific voltage" is not transferable.
- **The model organisms are not running the target metabolism.** *D. acetexigens* reduces elemental sulfur and is fed acetate; it is not a chemolithotrophic sulfur-oxide cycle. It shows a sulfur-lineage EET organism is potential-tunable. It does not show that current lifts a marginal sulfur-oxide metabolism into viability.

**The extrapolation, marked [SPEC].** If a sulfur metabolism sits just below the energy it needs, and applied potential raises the driving force on related electrode-coupled metabolisms, then a current-supplemented sulfur metabolism is thermodynamically coherent. A tribowhip is a current source. So a tribochemoautotroph is a coherent architecture. The lift itself has been shown for acetate and for sulfur reduction in water, not for the sulfur-oxide chemistry or the media the two creatures actually face. Everything past this point is the work that has not been done.

---

## PART B — Where the two creatures diverge

The foundation is common. The gap between each creature and that foundation is not.

The **Venus sulfur creature** drifts in Venus's CO₂/N₂ atmosphere and is struck by concentrated sulfuric-acid droplets. It is not immersed in acid; its deepest problem is building and maintaining a body from a meager feedstock (CO₂, N₂, trace dust, sparse and acidic water) while tolerating acid on contact. Its sulfur chemistry, the reductive SO₂ to S⁰ couple, would run in a setting with no liquid water, no free oxygen, extreme acidity on contact, and sulfur present as gases and aerosol (SO₂, OCS, S₈) rather than dissolved sulfate. Almost none of that chemistry has been measured. Its to-do list is long, and gated on one keystone measurement.

The **vent creature** is anchored to rock in ordinary anoxic seawater, fluttered by volcanic upwelling. Its medium is water at near-neutral pH. It faces no exotic-solvent problem, and the electron-transfer biology it would use is close to the *Desulfovibrio* EET already demonstrated in A1. Its blocker is not chemistry. It is that the anoxic subsurface upflow where it would live has barely been surveyed. Its to-do list is short and mostly observational.

So: shared foundation, then a long chemistry-benchmark ladder for one creature and a short go-look-and-culture program for the other.

---

## PART C — The Venus sulfur creature: the chemistry-benchmark ladder

### C1. What the creature is, in canon [SPEC, resting on LAB atmospheric facts]

A tribochemoautotroph whose primary business is sulfur, running the reductive reactions Venus is visibly doing, with triboelectric current as the supplement that pushes an otherwise-marginal sulfur metabolism into positive budget. The chosen couple is the four-electron reduction SO₂ + 4H⁺ + 4e⁻ → S⁰ + 2H₂O [SPEC-CHOICE, per Report B module III-C]. The habitable band for a Fulgorax-like drifter is 50 to 54 km [SIM over LAB atmospheric structure]. The sulfur anomaly this creature is aimed at, the SO₂ inversion where mixing ratio rises with altitude, sits higher and colder, at roughly 70 to 75 km, requiring an unidentified sulfur reservoir that no photochemical model explains [LAB].

One mechanism could connect the two altitudes. Friction heat from the fluttering whips could warm the body enough to make the colder inversion layer livable, so the same flutter that powers the metabolism could buy access to the layer where the anomaly is [SPEC]. This is a hypothesis to be checked, not a result.

The honest constraint is that this creature cannot be resolved on a computer. Where the carbon creature (Fulgorax) had a laboratory anchor at nearly every step, the sulfur-oxide cycle has almost none. The entire design is gated on wet-lab electrochemistry and sulfur photochemistry that nobody has run. That is why the tractable carbon version was built first, and it is what the ladder below itemizes.

### C2. The benchmark ladder: what must be measured, and the work it takes

Items are grouped from most foundational (without which no metabolism can even be written) to most design-specific. Nearly every item is Earth-bound and pre-Venus, and nearly every one is wet-lab or bench-electrochemistry, not computation. The keystone is item 1: until the sulfur redox tower is measured in concentrated sulfuric acid, "a marginal metabolism that current could lift" has no quantitative meaning, because there is no measured free-energy change to lift.

**Tier I. Foundational chemistry.**

1. **Sulfur redox thermodynamics in concentrated H₂SO₄.** *Work: physical/analytical electrochemistry.* Measure the relative free energies of the sulfur couples (SO₂, OCS, S₈/Sₓ, sulfite, thiosulfate, sulfate) at Venus acidity and water activity, rather than extrapolating from aqueous tables. This is the keystone; almost everything below depends on it.
2. **Speciation and kinetics of the sulfur oxides in concentrated acid.** *Work: physical chemistry.* Determine what SO₂, OCS, and elemental sulfur actually are in concentrated H₂SO₄ (dissolved, protonated, complexed, polymerized) and how fast they interconvert. The abiotic cloud network is defined for the gas phase; the condensed-acid-phase chemistry a droplet-struck organism meets is far less characterized.
3. **Stability and turnover of sulfur intermediates in acid.** *Work: physical chemistry.* Establish which intermediates persist long enough to be metabolically useful and which are destroyed or abiotically short-circuited. A metabolism cannot run on an intermediate the medium consumes faster than an enzyme could.
4. **Water as reactant, not only solvent.** *Work: physical/biochemistry.* Determine whether any sulfur cycle can be written that does not depend on abundant water as a proton shuttle and reactant, and if water is required, what minimum water activity permits it. This gates whether a low-water-activity organism can use this chemistry at all.

**Tier II. Electron-transfer machinery in a hostile medium.**

5. **Whether any electron-transfer structure works in concentrated H₂SO₄.** *Work: biochemistry / bioelectrochemistry.* Every demonstrated EET conduit (c-type cytochromes, multiheme proteins, conductive filaments) is aqueous-evolved. Test whether any conductive biological or biomimetic structure keeps its conductivity and integrity in concentrated acid. A negative result would be as decisive here as the biosynthesis-from-feedstock wall is for Fulgorax.
6. **Acid-stable charge-transfer chemistry, biomimetic allowed.** *Work: synthetic / materials chemistry.* If natural cytochromes fail, determine whether a synthetic or hybrid charge-transfer moiety can shuttle electrons at the needed potentials in this medium. The project's redox-core work on quinone/semiquinone and ferrocene couples is the natural starting point, and this is the most tractable bench entry.
7. **Electrode and bio-electrode behavior, including sulfur passivation, in acid.** *Work: electrochemistry.* Characterize whether elemental sulfur deposits, dissolves, or re-speciates at a charge surface in concentrated acid, and whether a metabolism can avoid fouling itself. This is a directly runnable bench experiment.
8. **Coupling current to a sulfur-oxide redox step.** *Work: bioelectrochemistry.* The keystone biological demonstration: show, in water first and then toward acid, that an applied current measurably raises the rate or yield of an SO₂ or OCS transformation, reproducing the A2 driving-force effect on the target chemistry rather than on acetate or on sulfur reduction. Nothing in the current literature does this for sulfur oxides.

**Tier III. Closing the energy cycle without oxygen.**

9. **An O₂-free terminal acceptor.** *Work: microbiology / electrochemistry.* Terrestrial systems close on oxygen or nitrate. Identify an acceptor that exists on Venus (another sulfur oxidation state, a CO₂-derived species, or the triboelectric circuit itself) that can close a sulfur loop anaerobically, and at what yield.
10. **Whole-cycle energy balance with the supplement included.** *Work: bioenergetics.* Once items 1, 8, and 9 exist, measure whether primary sulfur turnover plus a current supplement nets positive over maintenance, the sulfur analogue of the project's Gate-3b ledger, which for Fulgorax closed only on a knife-edge. Without the measured tower from item 1, this ledger cannot be written.
11. **Maintenance and repair cost under acid attack.** *Work: biochemistry / materials.* The acid degrades structure continuously, so the cycle must out-earn that degradation. The repair-versus-degradation rate is the term that decides the ledger's sign, and it is unmeasured for any sulfur system exposed to this medium.

**Tier IV. Distinguishability and organism-level design.**

12. **A biotic-versus-abiotic discriminator for the products.** *Work: isotope / analytical geochemistry.* Elemental sulfur from SO₂ is already produced abiotically on Venus, so establish in the lab what isotopic (δ³⁴S, Δ³³S) or morphological signature a current-supplemented sulfur metabolism would leave that the abiotic cycle does not. Without this, even a working organism would be undetectable.
13. **Light-element fractionation under current supplementation.** *Work: isotope geochemistry.* Measure whether driving a metabolism with external current changes its isotopic fractionation relative to an unforced one. This determines whether the headline δ³⁴S discriminator survives the very supplement that defines the creature.
14. **Population and throughput limits in a droplet medium.** *Work: microbial ecology / transport.* Cell-to-cell sulfide shuttling set the current in the terrestrial co-biofilm; measure the analogous transport limits (density, rate, spacing) for organisms living on or in acid aerosol droplets. This bounds any organism-scale design.

### C3. The most testable item for this creature

Of the fourteen, one is reachable with an instrument already en route rather than a lab program: **item 12, the δ³⁴S discriminator.** Biological reduction of SO₂ to S⁰ would leave product sulfur depleted in ³⁴S, mass-dependently, by up to tens of per-mil, distinct from the often mass-independent pattern of abiotic photochemistry [SPEC for the biological magnitude, LAB for the abiotic contrast]. DAVINCI's tunable laser spectrometer is designed to measure triple-sulfur isotope ratios (³²S/³³S/³⁴S) in SO₂ at about 1‰ precision, finer than the expected biological signal [LAB, DAVINCI instrument papers; the project earlier carried a ~2‰ figure that the verification pass corrected to ~1‰].

The caveat that keeps this honest: the planned measurement targets gas-phase SO₂, whereas the discriminating signal would live in aerosol elemental sulfur, which needs aerosol-sampling mass spectrometry that is proposed but not yet manifested. And item 13 sits underneath item 12: if current supplementation changes the fractionation, the discriminator's magnitude is itself unmeasured. So the most testable item is reachable in principle and specifically matched to a funded instrument's precision, with a clear gap between what will be measured (SO₂ isotopes) and what would be diagnostic (aerosol-S isotopes).

---

## PART D — The deep-sea vent creature: a strawman to be overruled

Everything in this part is a proposed design generated to give the vent creature a to-do list at the depth of the sulfur creature's. It is a strawman, marked **[SPEC]** throughout, offered for the person and the field to overrule. It is deliberately more openly speculative than Part C, whose ladder is anchored to real papers. What is [LAB] here is only the environmental setup and the terrestrial EET chemistry; the creature is not.

### D1. The setup, which is real [LAB]

At deep-sea hydrothermal vents the visible animal community (tubeworms, crabs, molluscs, polychaetes) clusters where anoxic vent fluid mixes with oxygenated seawater, and those animals depend on the oxygen, buffered by high-affinity respiratory pigments but not freed from it [LAB, vent-physiology literature]. Pure end-member hydrothermal fluid is anoxic, CO₂-rich, low-pH, and laden with H₂S and reduced metals [LAB]. Push past the mixing boundary into that pure anoxic upflow and the textbook expectation is that only single-celled chemoautotrophs survive; complex multicellular life is thought to stop where the oxygen stops [LAB].

And the reason such a creature could have gone unseen is that the relevant volume has barely been examined. Only a small fraction of Earth's vent systems have been surveyed, and the subsurface conduits that feed the plumes, the anoxic channels where this creature would live, are almost entirely unexplored [LAB].

### D2. The prediction [SPEC]

A triboelectric boost is a way to pay for the complexity an oxygen-free environment cannot otherwise fund. The prediction is therefore a **multicellular organism living in the anoxic vent upflow, deeper than the oxygen boundary should allow**, anchored to rock, its whips fluttered by the upwelling, running a sulfur metabolism that was assumed to require oxygen or to support only single cells. The signature is multicellularity where the map says there should be none. If found, it is the single clearest demonstration of the project's central claim, that triboic current can let complex life exist without oxygen.

Two forms are worth designing, both [SPEC]:

- A **pure triboautotroph**, running entirely on current drawn from the upwelling, the vent-flow analogue of Fulgorax. Hardest ledger.
- A **tribochemoautotroph**, keeping the ordinary sulfur chemosynthesis single-celled vent life already uses and adding a current boost just large enough to fund the leap to multicellularity. This is the gentler ledger and the more likely find, because it extends a metabolism already known to work at vents rather than replacing it.

A note on why this creature is better-anchored on chemistry than the Venus one, and worse-anchored on observation. Its proposed electron-transfer chemistry is close to what is already demonstrated: *Desulfovibrio*-type sulfate/sulfur reducers performing EET to an electrode in anoxic water (A1, Hou et al. 2024). The vent medium is ordinary seawater, so items 1 through 7 of the Venus ladder, the entire concentrated-acid problem, simply do not arise. What is missing is not the chemistry but the look: nobody has been to the place. That asymmetry is why the vent track is short and mostly a survey-and-culture program.

### D3. The vent creature's to-do list [SPEC strawman]

Far shorter than the sulfur ladder, and mostly observational or culturing rather than foundational chemistry.

1. **Survey the anoxic subsurface upflow for multicellularity.** *Work: submersible / ROV field survey.* Sample the pure anoxic vent flow and the shallow subsurface conduits feeding the plumes, specifically looking for multicellular tissue where only single cells are expected. This is the direct test of D2 and the single most testable item for this creature (see D4).
2. **Establish the local oxygen and redox profile at the sampling points.** *Work: in-situ electrochemistry / microsensors.* Confirm that any multicellular find actually sits below the oxygen boundary, since the whole claim is multicellularity in genuinely anoxic flow. Without a measured O₂ profile at the exact find location, a positive is ambiguous.
3. **Characterize flow at the anchoring surfaces.** *Work: field fluid dynamics.* Measure whether the upwelling provides sustained fast flow sufficient to drive a flutter at candidate anchoring sites, the constant-flow gate the mechanism requires.
4. **Culture a candidate sulfur EET organism from the anoxic flow.** *Work: anaerobic microbiology.* Attempt to culture sulfur-cycling organisms from the upflow and test EET to an electrode, extending the *Desulfovibrio* result into vent isolates. This is chemistry the foundation already makes plausible, so it is a confirmation rather than a discovery.
5. **Test a current supplement on vent sulfur chemistry.** *Work: bioelectrochemistry.* In cultured isolates, test whether an applied current raises growth or yield on vent sulfur substrates, the vent analogue of Venus item 8, in the far friendlier medium of anoxic seawater.
6. **Sketch the multicellularity-versus-current ledger.** *Work: bioenergetics [SPEC].* Estimate whether a plausible triboelectric current from vent flow could fund the energetic step from single-celled to multicellular life. This connects to an unresolved tension in the main project: a triboic organism that must be multicellular from the start has no obvious single-celled ancestor. The vent creature inherits that origin question, and it should be stated, not hidden.

### D4. The most testable item for this creature

**Item 1, the survey for multicellularity in the anoxic upflow.** Unlike the Venus creature's best test, which waits on instrument capability and a specific mission, this one needs a submersible and a sampling plan, both of which exist. It is also the most falsifiable target in the entire triboic program: either multicellular tissue is present below the oxygen boundary or it is not. A well-designed survey of the unexplored subsurface conduits could return a clean yes or no. This is the reason the vent creature, though it is the surprising extension rather than the direct descendant of the Venus work, is the more reachable of the two.

The off-world echo is worth one line. Europa is widely suspected to host vent systems like Earth's beneath its ice, so an Earth-testable result here has a direct icy-moon analogue [LAB for the suspicion, SPEC for any Europan creature].

---

## PART E — What this adds up to

Two sulfur-powered triboic creatures share one demonstrated foundation and then diverge as far as two creatures can.

The **shared foundation is real**: a sulfur cycle and an electric current already run together on an electrode, in deployed wastewater and desulfurization systems, using known organisms and known EET machinery [LAB]. The energetic logic that a current supplement could lift a marginal sulfur metabolism is grounded on Earth [LAB], and its extrapolation to either creature is [SPEC].

The **Venus creature faces a long road with a clear first step**. Its fourteen-item ladder is gated on one keystone measurement, the sulfur redox tower in concentrated sulfuric acid (item 1). Its most testable output, the δ³⁴S discriminator (item 12), is matched to DAVINCI's ~1‰ capability, with the honest gap that the funded measurement targets gas-phase SO₂ while the diagnostic signal lives in aerosol sulfur.

The **vent creature faces a short, mostly observational road**. It has no exotic-solvent problem, its chemistry is close to what is already demonstrated in anoxic water, and its blocker is that nobody has surveyed the anoxic subsurface upflow where it would live. Its most testable item, a submersible survey for multicellularity below the oxygen boundary (item 1), is the most reachable and most falsifiable target in the whole triboic program.

Same mechanism and same sulfur-plus-current architecture place these two creatures at opposite ends of readiness: one waits on a decade of wet-lab chemistry, the other on a single well-aimed dive. For a program deciding where to spend effort, that difference is the practical output of this document.

---

## Sources

Verified against primary literature where marked. Items tagged **[citation needs verification]** were not fully confirmable in this pass and should be checked before publication.

- Aelterman, P., Freguia, S., Keller, J., Verstraete, W. and Rabaey, K. (2008). The anode potential regulates bacterial activity in microbial fuel cells. *Applied Microbiology and Biotechnology* 78(3), 409–418. doi:10.1007/s00253-007-1327-8. **Verified.**
- Sysoev, M., Katuri, K. P., Rangel Shaw, D., Mandal, P. and Saikaly, P. E. (2025). Effect of anode potential on the physiology and extracellular electron transfer of *Desulfuromonas acetexigens*. *Bioresource Technology Reports* 32, 102448. doi:10.1016/j.biteb.2025.102448. **Verified.**
- Hou, L., Cortez, R., Hagerman, M., Hu, Z. and Majumder, E. L.-W. (2024). Co-occurrence of direct and indirect extracellular electron transfer mechanisms during electroactive respiration in a dissimilatory sulfate-reducing bacterium. *Microbiology Spectrum* 13(1), e01226-24. doi:10.1128/spectrum.01226-24 (PMC11705803). **Verified against the published paper:** first author Liyuan Hou (note: cite as "Hou, L.," not "Hou, Y."); organism *Desulfovibrio vulgaris* Hildenborough; co-occurring direct and indirect EET during sulfate reduction, in the context of sulfate-containing wastewater microbial fuel cells. *(Report B's 2nd draft cites this same paper as "Hou, Y. et al. 2024" at PMC11705803. The PMC number is correct but the initial is wrong; correct Report B to "Hou, L." so the two documents match.)*
- Bond, D. R. and Lovley, D. R. (2003). Electricity production by *Geobacter sulfurreducens* attached to electrodes. *Applied and Environmental Microbiology* 69(3), 1548–1555. doi:10.1128/AEM.69.3.1548-1555.2003. **Verified in prior pass.**
- Thauer, R. K., Jungermann, K. and Decker, K. (1977). Energy conservation in chemotrophic anaerobic bacteria. *Bacteriological Reviews* 41(1), 100–180. doi:10.1128/br.41.1.100-180.1977. **Verified in prior pass.**
- de Rink, R. et al. (2018). Bacteria as an electron shuttle for sulfide oxidation. *Environmental Science & Technology Letters*. doi:10.1021/acs.estlett.8b00319. **Verified in prior pass.**
- Lee, D.-J. et al. (2014). SRB and sulfide-oxidizing co-biofilm anode; sulfate to sulfide to S⁰ with electron transfer. *Bioresource Technology* (with a 2012 precursor study). **[citation needs verification]** on exact volume, pages, and title.
- Bioelectrochemical-systems reviews on abiotic sulfide oxidation at anodes, and on elemental-sulfur electrode passivation. **[citation needs verification]**; used only for the two foundation caveats, which are well established qualitatively.
- DAVINCI / VTLS triple-sulfur isotope capability (~1‰). Mission instrument papers. **[citation needs verification]** on the exact spec; the project corrected an earlier ~2‰ figure to ~1‰ in its verification pass.
- Deep-sea vent environmental and physiological facts (anoxic CO₂-rich low-pH end-member fluid; animals clustering at the oxygen boundary; only single cells expected in the pure anoxic flow; subsurface conduits largely unexplored): drawn from the vent-chemoautotroph and vent-physiology literature. **[citation needs verification]** for specific citations to attach to each claim.

*Cable bacteria (Pfeffer 2012; Nielsen 2010), cited in an earlier draft of this adjunct, are deliberately removed. They close their circuit on oxygen, which muddies the no-free-oxygen argument central to both creatures, and the SRB/SOB and Desulfovibrio examples make the point without that ambiguity.*

---

*Tier summary. Part A: foundation is [LAB], the energetic extrapolation is [SPEC]. Part C: the Venus creature is [SPEC] over LAB atmospheric facts, its ladder is a list of unmeasured chemistry, keystone-gated on item 1; its best test (item 12) is matched to a funded instrument. Part D: the vent creature is a [SPEC] strawman over a [LAB] environmental setup, with a short survey-and-culture list; its best test (item 1) is a reachable, falsifiable dive. This is a direction gated on laboratory and field work, not a result.*
