# From explanation to experiment

## Narrative construction

Pick a real-world example that carries the causal chain through the module. Introduce the next concept because the current explanation leaves a specific question unanswered. A productive paragraph sequence is observation → mechanism → consequence → question leading to the next mechanism. It is a writing pattern, not a compulsory heading structure.

Introduce prerequisite terms where they first become necessary. Explain axes, units, signs and comparisons before asking the learner to interpret a graph. Separate the input, internal state, output and whole-system consequence; a single component's output seldom proves the behavior of the whole system.

Draft `docs/lesson-text.md` as a reviewable manuscript if the module has substantial prose. Keep one authoritative source for application text and generate exports where feasible rather than maintaining diverging copies.

## Embedded experience contract

For each component, specify:

- What question in the surrounding paragraph it answers.
- What the learner predicts before seeing the result.
- The independent variable and which factors remain fixed.
- What changes and how the learner observes it in text as well as graphics.
- The mechanism explaining that change.
- A transfer question in a new context and the limits of the inference.

For parameterized models, add valid ranges, step sizes, units, initial conditions, boundary behavior and deterministic rules. Separate illustrative parameter values from measured values. A playback rate must not change the model result. A changed parameter invalidates the old revealed result and prediction while preserving explicitly requested trial history.

For step diagrams, describe them as schematic sequences, including omitted branches and lack of a physical time scale. A moving dot should not accidentally imply that one molecule or packet travels across different cells.

## Assessment

Assess mechanism and prediction, not just terminology. Include a worked example, a new case and transfer. Make correctness and explanatory reasoning separately visible. When using self-assessment for open explanations, expose the rubric and label the score as self-reported; do not claim semantic grading from keyword matching. Feedback should identify the mistaken mechanism and provide a route to review it.

## Gates and verification

Before code: check every prerequisite, relationship type, scene purpose, movement purpose, model limitation, prediction and transfer. Plan approval is separate from implementation validation.

After code: check consequential boundaries and interaction resets, keyboard use, reduced motion, text alternatives and mobile overflow. Capture both initial and revealed states; for long articles, include viewport captures around embedded experiments and assessments rather than only an unreadably tall whole-page screenshot. Note unexecuted checks explicitly. Estimated duration needs learner observation, not a word cap.
