# Triboic Life

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21155313.svg)](https://doi.org/10.5281/zenodo.21155313)

**Could a living thing power itself from static electricity — the charge made by moving air or water — the same effect as the spark at a winter doorknob?**

This project takes that question seriously and tests it the hard way. It proposes a class of life, *triboic life*, that harvests electrical charge from its own fluttering parts (*tribowhips*) driven by the flow of the fluid it lives in. Then, rather than leaving the idea as a pleasant possibility, it builds one concrete creature — **Fulgorax**, a millimetre-scale carbon-based organism — drops it into a simulation of the clouds of Venus, and works the chemistry forward to see whether it can actually pay for itself.

The honest answer is the interesting part. On the project's own accounting, Fulgorax *just barely* closes its energy budget — and only on a knife-edge. Placed on Venus and worked forward, it fails to explain the one real sulfur anomaly the planet is actually showing us. That failure is not hidden. It is the most useful result here, because it points directly at the creature the project did **not** build: a sulfur-based one, which is the road left open for others.

![Fulgorax, full body](images/Fulgorax_Full_body.png)

---

## Why this exists

This is an open, buildable invitation, not a finished claim. The goal is for other people — especially graduate students and early-career researchers in astrobiology, geochemistry, and biophysics — to read it, run it through an LLM to get oriented fast, critique it, and build on it. Everything needed to check the work or extend it is here: the reports, the reasoning, and the code that produced the numbers.

If you came here from an email or a link and want the fastest possible orientation: **download a report below, paste it into any large language model, and ask it to summarize the argument and where it is weakest.** Then read further only if it still interests you. That is the intended entry point.

---

## Start here — the three reports

**1. [Life Powered Like Lightning](reports/Life_Powered_Like_Lightning.md)** — *the accessible essay.*
The main idea told plainly, start to finish: what triboelectric life is, how Fulgorax was designed, how it was tested on Venus, and what the test showed. Read this first. No specialist background needed.

**2. [Report B — Triboic Life Technical Companion](reports/ReportB_Triboic_Life_Technical_Companion.md)** — *the full technical spine.*
The rigorous version. The gated method (cheapest-decisive-test-first), the forward-chemistry rule, every module's claim/evidence/limit, the falsifiable predictions matched against real planned Venus instruments (DAVINCI), and a collected, unflinching list of the work's own weakest points. This is where a skeptic should push.

**3. [The Triboic Frontier — An Open Catalogue](reports/The_Triboic_Frontier_Catalogue.md)** — *the handoff.*
The open design space. Where else the mechanism could go — other chemistries, other worlds, other flows — with the leading unbuilt candidate (a Venus sulfur creature) argued in detail. Each candidate is a named seed someone can claim and develop. **This is the to-do list for collaborators.**

An additional adjunct, [Current and the Sulfate Energy Cycle](reports/Adjunct_Current_and_the_Sulfate_Energy_Cycle.pdf), explores the sulfate-energy direction in more depth.

---

## The code

The `code/` folder holds the scripts behind every quantitative result, organized by the project's gate structure — the sequence of make-or-break tests each ordered so the cheapest decisive one runs first:

- `code/gate0_redox/` — the redox core (can a cofactor buffer pulsed charge into steady current?)
- `code/gate1_whip/` — whip electromechanics (does a buildable whip produce a usable pulse?)
- `code/gate3_coating_ledger/` — the acid-resistant coating and the full energy ledger
- `code/gate4_atmosphere/` — the atmospheric trace-chemistry exchanges and forward predictions

Most of the numerical work runs in a plain `numpy` environment and is re-runnable anywhere. Two campaigns (the xTB and DFT chemistry) need a compiled toolchain; their canonical outputs are preserved in the reports. Full environment details are documented alongside the code.

---

## How to engage, critique, or build on this

The whole point is for other people to take this further. Three ways in:

- **Ask a question or start a discussion** — open an [Issue](../../issues) on this repository. No email needed, and the conversation stays visible so others can join it.
- **Correct or extend the work** — spot a wrong citation, a flawed assumption, a step that doesn't hold? That is a real contribution. Open an Issue or a Pull Request.
- **Claim a frontier candidate** — pick one of the unbuilt candidates from the Frontier Catalogue and design it to the same standard Fulgorax was held to. That is the invitation this project most wants taken up.

---

## License

This work is released under [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](LICENSE).

You are free to share and adapt all of it — including for your own research and publications — for any purpose, as long as you give appropriate credit. Building on this work is not just allowed, it is the goal. Please cite it so others can trace the lineage of the idea.

---

*A speculative-biology project pursued with the discipline of a real one: built to be caught being wrong, and handed off honestly at its edges.*
