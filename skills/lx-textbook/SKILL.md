---
name: lx-textbook
description: Build or revise an interactive textbook with continuous explanatory prose, concept prerequisites, meaningful experiments, prediction before reveal, and transfer assessment. Use for browser-based learning modules and reusable learning-experience workflows, rather than ordinary websites or slide decks.
---

# LX Textbook

Create a coherent explanation that the learner can read from beginning to end. Place diagrams, animations and experiments where they resolve a question raised by the text. Keep the explanation understandable when the learner skips an optional visual; do not substitute captions, cards or slogans for reasoning.

## Establish scope

Read the project's brief and applicable AGENTS.md. Preserve the requested topic, audience, language, format and authorization. Ask only blocking questions. For an existing module, keep working interactions and update only the necessary artifacts. An instruction to finish or build authorizes implementation after the planning gates pass; do not introduce a new approval checkpoint. If the user requests planning only, stop after the plan.

For a new project, optionally run `scripts/new_module.py DESTINATION --topic TOPIC`. It creates a brief, project instructions, a ready-to-paste start prompt and this portable skill. Use `--help` for audience, language, time and planning-only options. It refuses a nonempty destination. It does not generate domain claims, publish anything or install global skills.

## Design before rendering

Produce or update these reviewable files, then report their gates before implementing:

- `docs/knowledge-map.md`: concepts, prerequisites (or foundational), typed relationships, misconceptions, source-to-claim mapping and evidence gaps. Allowed relationship types: prerequisite, causes, regulates, part-of, contrasts-with, analogy.
- `docs/learning-path.md`: observable learning objectives, progressive sequence, one continuous example, worked example, prediction tasks, assessment rubric and transfer tasks.
- `docs/storyboard.md`: text sequence and embedded components. Every scene explains why the mechanism matters, how it works and what changes; every movement has an educational purpose.
- `docs/quality-gates.md`: pass/fail/pending with evidence. Distinguish a passed plan from validated implementation.

Read [references/pedagogy.md](references/pedagogy.md) when drafting the explanatory prose and interaction specification.

Use verified authoritative sources for factual claims. Label illustrative numbers and uncertainty; do not manufacture citations. A model must specify its assumptions, valid inputs, rules, outputs and limits before implementation. Do not describe a qualitative diagram as a validated physiological or physical simulation.

## Implement and extend

Begin with a self-contained 5–10 minute vertical slice with a meaningful model, prediction before reveal and assessment. Once that exists, extend to the full requested scope when authorized. Do not keep delivering the first slice when the user asks for the complete module.

Keep domain content and models separate from the renderer. Prefer React, TypeScript and Vite for a new application; retain a working stack for an existing one. Choose extra graphics libraries only for a demonstrated requirement. When dependencies are unavailable, use a runnable fallback and record the reason rather than shipping code that cannot be built.

Use continuous prose, readable line length, modest headings and an optional table of contents. Before an experiment, explain what to predict and observe; after it, interpret the mechanism and connect it to the next paragraph. Do not expand the curriculum because of a convenient animation or tool. Preserve keyboard access, visible focus, text equivalents, reduced motion and mobile reading.

## Verify and hand off

Test model invariants and consequential interaction state transitions. Attempt desktop and mobile browser checks and inspect screenshots; revise observed failures. Record checks that could not run as blocked, never as passed. Keep runtime and hosting restrictions local to the report, not universal skill rules.

Provide the runnable artifact and a short validation report with produced files, remaining assumptions, failed or blocked gates and the next action. Offer a standalone offline artifact when it materially helps reuse. Publishing or messaging others requires authorization for that action; this skill provides none.
