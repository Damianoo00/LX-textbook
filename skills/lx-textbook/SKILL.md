---
name: lx-textbook
description: Interview the user, configure a new project automatically, and build or revise a browser-based interactive textbook with continuous prose, experiments, prediction and transfer. Use for learning modules, including requests without a brief or project configuration.
---

# LX Textbook

Create a coherent explanation that the learner can read from beginning to end. Place diagrams, animations and experiments where they resolve a question raised by the text. Keep the explanation understandable when the learner skips an optional visual; do not substitute captions, cards or slogans for reasoning.

## Establish scope

Read applicable AGENTS.md and the project brief if one exists. If no brief exists, use the guided start below. Preserve the requested topic, audience, language, format and authorization. Ask only blocking questions. For an existing module, keep working interactions and update only the necessary artifacts. An instruction to finish or build authorizes implementation after the planning gates pass; do not introduce a new approval checkpoint. If the user requests planning only, stop after the plan.

## Guided start — no manual configuration

When the user requests a new textbook, gather missing information through conversation and configure the project yourself. Read prior messages first; do not ask again for supplied details. Respond in the user's language.

1. Ask one short batch about missing topic, audience/prior knowledge and the desired outcome. Example: “Jaki temat, dla kogo i co czytelnik ma umieć po lekturze?” If these are known, proceed.
2. Resolve only material scope ambiguity. Offer a concrete proposed scope and continuous example. Default to the user's language, approximately 20 minutes and build mode unless the user requests planning only. Ask about sources only when the user refers to specific materials or verification otherwise cannot proceed. Do not require a technical questionnaire, model choice, adapter selection or manual brief.
3. Infer a writable destination from the workspace and topic, e.g. a new sibling project folder `textbook-<topic>`. State the chosen path. If the destination is ambiguous and changes where work belongs, ask once. Do not initialize inside this skill or overwrite an existing project.
4. Write a temporary UTF-8 JSON intake file yourself with `topic`, `audience`, `goal`, `scope`. Optional fields: `language`, `minutes` (positive integer), `example`, `mode` (`build`/`plan`), `sources`, `exclusions`. Run `python3 <absolute-skill-path>/scripts/bootstrap.py <destination> --intake <json-path>` with proper tool arguments/quoting. The script creates the brief, shared workflow, roles, all three native adapters, a local read-only MCP server and discoverable copies of this skill. Everything needed is bundled in this skill; no repository-root installer is required.
5. Read the generated brief and `core/workflow.md`, set tool working directory to the new project and continue directly with the design gates below, then implementation if authorized. A build request authorizes setup and building; do not insert another approval checkpoint. If the user only asks to prepare the project, stop after setup.

New configuration may require a fresh client session before native agents/MCP become available. Do not claim hot activation. Use current session tools and sequential roles to continue now; do not send the user back to manual installation. No CLI installation, credentials or global configuration is performed. If a required capability is missing, record the blocked check and continue independent work.

For an existing textbook, preserve its configuration and working interactions. Read and update the brief from the conversation, then follow the same planning/build gates; do not run bootstrap on a nonempty folder. If scaffolding must be added, merge only missing files and preserve existing client settings.

Use `scripts/bootstrap.py` for project initialization. The project templates in `assets/project/` are configuration resources, not domain claims; they never grant the scope of another module.

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
