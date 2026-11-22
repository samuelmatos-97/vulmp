# VulMP — Codex Development Guidelines

## Project Overview

VulMP is a cloud-native DevSecOps Vulnerability Management Platform.

The project is developed incrementally to learn backend engineering, DevOps, DevSecOps, and cloud-native technologies through practical implementation.

## Development Principles

- Work on one task at a time.
- Prioritize learning and understanding over development speed.
- Explain the purpose of each proposed change before implementing it.
- Keep changes small, clear, and easy to review.
- Follow the existing project architecture and conventions.
- Avoid unnecessary complexity and premature optimization.

## Code Guidelines

- Write clean and readable Python code.
- Add simple English comments explaining important operations.
- Use short docstrings to describe the purpose of functions.
- Follow existing FastAPI, SQLAlchemy, and Pydantic patterns.
- Reuse existing functions and dependencies whenever possible.
- Preserve existing API behavior unless a change is explicitly requested.

## Database Guidelines

- Use Alembic for all database schema changes.
- Do not use `Base.metadata.create_all()` to manage the schema.
- Review migration scripts before applying them.
- Never delete database volumes or existing data without explicit approval.
- Use the existing `get_db()` dependency for database sessions.

## Docker Guidelines

- Preserve the existing Docker Compose architecture.
- Maintain health checks and service dependencies.
- Explain changes to Dockerfiles and Compose configuration.
- Do not execute destructive Docker commands without explicit approval.
- Never run `docker compose down --volumes` or `docker compose down -v` without the user's explicit approval for that exact invocation.
- Before requesting approval, enumerate every volume that the command can remove, identify the data stored in each volume, prove that each target is disposable or backed up, and state the recovery impact.
- Treat uncertainty as a stop condition. Use non-destructive alternatives such as `docker compose stop`, `docker compose down` without volume removal, or targeted container recreation.
- Never infer permission to delete volumes from permission to stop, rebuild, test, clean, or reset containers.

## Security Guidelines

- Never expose passwords, tokens, or sensitive information.
- Never commit `.env` or other files containing secrets.
- Use environment variables for application configuration.
- Follow the existing `.gitignore` and `.gitattributes` rules.

## Git Guidelines

- Review changes before committing.
- Use clear and descriptive commit messages.
- Inspect the working tree before making changes and preserve unrelated work. Never include unrelated changes in task commits; stage only the relevant files or hunks.
- For an authorized implementation task, Codex may create or select a dedicated task branch, modify task-related files, execute appropriate tests, stage and commit task changes, push the task branch, and create or update the associated Pull Request without repeated human approval.
- Task authorization covers additional edits, tests, commits, pushes, and Pull Request updates necessary to complete the same assigned scope.
- Rewriting existing Git history or force-pushing requires separate explicit human approval.
- Destructive operations, changing repository settings or label definitions, and managing existing Issues require separate explicit human approval. The stricter rules for `main` below always apply.
- Preserve all existing security, database, Docker, testing, and learning requirements when using these workflows.

## Main Branch Protection — Mandatory

Without explicit human authorization for the specific operation, Codex must never:

- Commit directly to `main`.
- Push directly to `main`.
- Merge any Pull Request into `main`.
- Rebase, reset, force-push, or rewrite `main` history.
- Delete or recreate `main`.
- Perform any other operation that directly modifies the local or remote `main` branch, including advancing local `main` through a pull or merge.

- General development authorization, automatic tool approval, or permission for an earlier operation never authorizes a later modification of `main`. Obtain explicit human authorization for each specific operation on `main`.
- Reading or comparing against `main` does not require approval. Creating or updating a Pull Request targeting `main` is permitted within an authorized task because it does not modify the target branch.
- All merges into `main` require explicit human authorization for the specific Pull Request and reviewed head commit SHA under the review and merge policy below. Never enable automatic merging.

## Authorized Development Workflow

- An authorized implementation task is an explicit user assignment to implement a defined change. An audit, review, discussion, or newly created Issue alone does not authorize implementation.
- Task authorization includes the ordinary development operations listed below, subject to any explicit restrictions in the current task. Do not request repeated approval while work remains within the authorized scope.
- Do not expand beyond the assigned task or begin additional implementation tasks without user authorization. Ask for separate explicit human approval before destructive operations or decisions outside the assigned scope.

For each authorized development task:

1. Understand the task and inspect the relevant code.
2. Check existing Issues and Pull Requests when appropriate.
3. Create or select a dedicated task branch.
4. Explain the objective and proposed changes, then implement the required changes.
5. Execute appropriate validation.
6. Review the final diff and exclude unrelated changes.
7. Commit and push the task branch.
8. Open or update the associated Pull Request.
9. Review the published Pull Request and perform appropriate validation under the review and merge policy below. Fix authorized blocking issues and repeat the review after each update.
10. Present the final review report and, when ready, request explicit human merge authorization. Stop before merging until that authorization is received and verified.

## Sandbox and Tool Permissions

- Apply this workflow consistently in Codex CLI and Codex Desktop.
- Keep the Codex sandbox enabled and use automatic approval review when available. Full Access mode is not required.
- Request eligible operations outside the sandbox through the configured approval mechanism. Technical approval does not replace explicit human authorization where these instructions require it.
- Use GitHub CLI or supported GitHub integrations as appropriate. The GitHub MCP server is not required.
- These instructions do not override technical sandbox restrictions, GitHub permissions, configured approval mechanisms, or approval decisions. Do not bypass a denial; use a materially safer alternative or report the blocker and request human intervention.

## GitHub Issues Workflow

- Evaluate nonblocking bugs, technical debt, security concerns, missing tests, documentation gaps, and useful improvements as potential Issues during reviews and task or milestone completion.
- Codex may autonomously create new GitHub Issues for actionable bugs, vulnerabilities, improvements, or development tasks without additional human approval, subject to the evidence, duplicate-check, and publication safeguards below and any explicit restrictions in the current task.
- Before creation, review the current implementation, relevant milestone history, and existing open and closed Issues. Avoid trivial, already resolved, speculative, or low-value tickets; group overlapping findings when they share one coherent outcome.
- Clearly distinguish confirmed defects, unverified concerns, known limitations, and proposed enhancements. An unverified concern requires concrete evidence and a defined validation task, not speculation.
- Never publish secrets, credentials, sensitive vulnerability details, or confidential information. Escalate sensitive cases for private user review instead of publishing them.

Each new Issue should include:

- An informative English title.
- Technical context, impact, and relevant repository files or references.
- The originating milestone, if applicable, distinguished from the planned delivery milestone.
- One existing type label and one existing priority label, when available, with a brief priority justification.
- Evidence, the finding classification, and reproduction or validation performed or still required.
- A proposed approach and measurable acceptance criteria.
- Dependencies or related Issues, where relevant.

Use these type labels: `type:bug`, `type:enhancement`, `type:documentation`, `type:testing`, `type:security`, and `type:tech-debt`.

Use these priority labels, assessed in the current deployment context:

- `priority:P1`: urgent or high-impact security, data-loss, correctness, or blocking work.
- `priority:P2`: meaningful corrective work, technical debt, or validation gaps.
- `priority:P3`: optional future improvements.

Apply these Issue management rules:

- Do not create repository labels automatically. If a label is missing, record the intended type or priority in the Issue body and propose label creation for user approval.
- After creating Issues, report their numbers, URLs, and reasons for creation.
- Issue creation does not authorize implementation. Managing existing Issues, including comments, metadata updates, closing, reopening, reprioritizing, or deleting, requires explicit human approval.

## Branch Workflow

- Keep `main` stable and use short-lived branches for small, focused changes.
- Create task branches from a reviewed, up-to-date remote `main` reference, such as `origin/main`, without updating local `main`. Fetch remote references as needed through permitted tools without modifying the local or remote `main` branch.
- Inspect the working tree first and preserve unrelated changes.
- Use `<prefix>/<issue-number>-<short-description>` when an Issue exists, or `<prefix>/<short-description>` otherwise. Use lowercase words separated by hyphens.
- Suggested prefixes are `fix`, `feat`, `docs`, `test`, `security`, and `chore`; examples are `fix/123-database-port-settings` and `docs/github-workflow`.
- Keep each branch focused on one Issue or coherent outcome. Explain when related Issues belong in the same change.
- Creating or switching to a dedicated task branch is permitted within an authorized implementation task without repeated approval. A branch naming convention alone does not authorize implementation.
- Push with an explicit task-branch destination so that an implicit push cannot update `main`.

## Pull Request Workflow

- For an authorized implementation task, Codex may automatically create or update the associated Pull Request after reviewing the changes, performing appropriate validation or clearly reporting outstanding validation, and committing and pushing the task branch.
- Existing task authorization covers further task-related edits, tests, staging, commits, pushes, and associated Pull Request updates without repeated approval. It does not authorize merging, modifying `main`, or managing existing Issues.
- Target `main` unless another target has been explicitly agreed. Keep changes small and reviewable; exclude unrelated cleanup.
- Use a Draft Pull Request when implementation or validation is incomplete. Never report unexecuted tests as passed.
- Review all published content for secrets, credentials, sensitive vulnerability details, and confidential information. Escalate sensitive cases for private user review instead of publishing them.

Every Pull Request should include:

- A clear English title and summary of the problem and solution.
- Linked Issues, when applicable.
- Test commands and actual results, plus checks not performed and why.
- Known limitations, security considerations, and relevant database, API, configuration, or deployment impacts.

Manage references and review as follows:

- Use plain references such as `Refs #N` for partial work. Use `Closes #N` in the Pull Request description only when the change fully satisfies the Issue's approved acceptance criteria and validation supports closure.
- Closing keywords take effect when the Pull Request merges into the default branch. Opening a Pull Request does not complete or close an Issue; approval to open it does not authorize Issue closure.
- Avoid automatic-closing keywords in commit messages and automatic-closing Development links for partial work.
- Before requesting merge approval, complete the final review report below and identify every Issue the merge would close. Obtain approval for those closures as part of the merge scope.
- Every merge requires explicit human authorization for the specific Pull Request and reviewed head commit SHA. Never enable automatic merging.
- Do not assume GitHub Actions or branch protection are enabled. Respect configured requirements and accurately report unavailable or unexecuted checks; a documented self-review is appropriate for solo development unless repository rules require another reviewer.
- After opening or updating a Pull Request, report its number, URL, purpose, Draft status, and actual validation results.
- After an authorized merge, verify the resulting branch, linked Issue states, and repository status. Merging does not replace the existing milestone-completion requirements.

## Pull Request Review and Merge Policy

- The default merge strategy is **Squash and merge**. Use a different strategy only when the user explicitly requests it for the specific Pull Request; include that strategy in the merge authorization.
- After creating or updating a Pull Request, record its full head commit SHA and review the complete diff at that commit. Assess correctness, security, regressions, test coverage, actual test results, available CI results, acceptance criteria, and compliance with project requirements.
- If blocking issues are found, fix them on the task branch when the fix is within the authorized scope, perform appropriate validation, push the changes, and repeat the review. Report blockers outside the assigned scope and request authorization before expanding the task.
- Confirm that the published head SHA still matches the reviewed commit before presenting the final report. Do not describe a different or unreviewed commit as ready to merge.

The final review report must include:

- Repository, Pull Request number and URL, target branch, and the full reviewed head commit SHA.
- Findings, distinguishing blocking issues from nonblocking observations, or an explicit statement that no findings were identified.
- Validation commands and actual results, tests not performed and why, and available CI results, including failed, pending, or unavailable checks.
- Outstanding risks or limitations, acceptance-criteria status, and any Issues that the merge would close.
- A clear merge recommendation and its reasons. A positive recommendation does not authorize a merge.

Human authorization and merge execution must follow these rules:

- When the Pull Request is ready, explicitly ask whether the user authorizes merging that specific Pull Request and reviewed commit into `main` using Squash and merge. Include the PR number or URL, full reviewed head SHA, and any Issue closures in the request. If another target or strategy has been explicitly agreed, state it instead.
- Only execute the merge after receiving explicit human authorization for that specific Pull Request, reviewed head SHA, target branch, merge strategy, and any listed Issue closures.
- Never interpret successful tests, a positive review, automatic tool approval, general development authorization, or permission for an earlier merge as authorization to merge.
- If the PR changes after review or approval, including its head commit, target, description, or Issue-closure scope, repeat the review and appropriate validation, present an updated report, and request authorization again for the current PR and head commit.
- Immediately before merging, re-read the PR state, target branch, current head SHA, mergeability, and applicable CI and repository requirements. Verify that the PR is open, the target matches the authorization, the head SHA matches the approved commit, and the PR remains mergeable with all required checks and approvals satisfied. Stop and report a blocker if any of these conditions fails or cannot be verified.
- When supported, use `gh pr merge <number> --repo samuelmatos-97/vulmp --squash --match-head-commit <approved-head-sha>`. For an explicitly requested alternative strategy, use its corresponding flag while preserving the approved head-SHA guard. If the tool lacks an equivalent conditional head-SHA check, use a supported integration that enforces it or report the limitation instead of merging unchecked.
- Never enable automatic merging or use `--auto`. Do not bypass repository requirements with `--admin`. If a merge queue or tool behavior would enable automatic merging or defer the merge, stop and report the limitation rather than enqueueing it.
- For unattended or scheduled executions, stop before merging and report that explicit human authorization is required.
- Merge authorization does not authorize branch deletion, updating local `main`, changing repository settings, or other actions outside the approved merge scope.
- Explicit restrictions in the current task, including instructions not to merge, remain binding even when the Pull Request is otherwise ready.

## Initial Workflow Bootstrap

- If the first collaboration-workflow Pull Request is still pending, keep it scoped to `AGENTS.md` on `docs/github-workflow`. This bootstrap-specific scope does not restrict later task branches or authorize operations prohibited by the current task.
- It does not require an existing Issue; explain the bootstrap purpose in the Pull Request description.
- New backlog Issues follow the same autonomous Issue creation rules, including evidence and duplicate checks; no separate candidate-list approval is required.
- Repository labels, Issue and Pull Request templates, GitHub Actions, and repository protection remain separate tasks. Issue or Pull Request creation does not authorize changes to them.
- Authorized task permissions apply, and explicit restrictions in the current task take precedence, including read-only or no-publication instructions.

## Testing and Validation

- Explain which tests should be executed and why.
- Prefer non-destructive validation commands.
- Verify that existing functionality remains operational.
- Report errors clearly and explain their possible causes.
- Never claim that tests passed unless they were actually executed.

## Learning Workflow

For each development task:

1. Explain the objective.
2. Identify the relevant files.
3. Present the proposed implementation.
4. If implementation is already authorized, proceed within its scope without renewed approval. Otherwise obtain user authorization before modifying files.
5. Implement the approved changes.
6. Explain the code and important decisions.
7. Validate the implementation.
8. Review the results with the user.

## Milestone Completion

When milestone completion is part of the authorized task scope:

1. Validate the implemented functionality.
2. Update `README.md` while preserving its formatting.
3. Review Git changes.
4. Commit the task-related changes on the dedicated task branch under the existing task authorization.
5. Push the task branch and open or update its Pull Request under the existing task authorization.
6. Confirm that no task-related changes remain uncommitted and report any preserved unrelated changes.

Do not modify `main` or merge the Pull Request without separate explicit human approval. Do not expand an assigned fix into milestone completion without authorization.

## Important

This is a learning-focused project.

Codex should explain objectives, implementation decisions, and validation while autonomously completing authorized tasks on dedicated task branches. Keep work focused on the assigned scope, preserve human control over destructive operations and every modification of `main`, and do not undertake additional milestone work without authorization.
