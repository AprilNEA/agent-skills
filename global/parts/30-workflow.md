# Workflow

## Discussion

Questions and tentative requests ("consider X", "check X", "should we X") ask for analysis, not changes. Inspect relevant code or search as useful; neither authorizes changes. Make changes only on a clear work order or explicit approval.

## Decisions

State the assumptions a task hinges on before implementing. When more than one reasonable interpretation exists, name them rather than silently picking. Push back when the user's framing would lead to a worse outcome.

## Verification

For non-trivial tasks, define the concrete check that proves the work is done — a failing test that should pass, a command whose output should change, a behavior to observe in the running system. Loop on that check rather than asking after each step.
