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

## Security Guidelines

- Never expose passwords, tokens, or sensitive information.
- Never commit `.env` or other files containing secrets.
- Use environment variables for application configuration.
- Follow the existing `.gitignore` and `.gitattributes` rules.

## Git Guidelines

- Review changes before committing.
- Never create commits or push changes without explicit approval.
- Do not create branches or modify Git history without approval.
- Use clear and descriptive commit messages.

- Require explicit user approval before editing files, creating or switching branches, staging, committing, pushing, merging Pull Requests, changing repository settings or label definitions, or managing existing Issues.
- Approval covers only the stated actions and scope. Approval to implement a change does not authorize staging, committing, pushing, or merging. An approval may explicitly cover a defined group of actions.
- The approved exceptions are automatic creation of qualifying new Issues and automatic opening of qualifying Pull Requests, as described below. Neither exception authorizes implementation or merging.
- Preserve all existing security, database, Docker, testing, and learning requirements when using these workflows.

## GitHub Issues Workflow

- Evaluate nonblocking bugs, technical debt, security concerns, missing tests, documentation gaps, and useful improvements as potential Issues during reviews and task or milestone completion.
- Codex may automatically create a relevant, actionable, non-duplicate Issue supported by adequate technical evidence, subject to the safeguards below.
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
- Issue creation does not authorize implementation. Managing existing Issues, including comments, metadata updates, closing, reopening, or reprioritizing, requires explicit user approval.
- For the initial Milestones 1–9 backlog only, obtain review and approval of the candidate list before bulk Issue creation. This bootstrap exception prevents publication of an unreviewed backlog.

## Branch Workflow

- Keep `main` stable and use short-lived branches for small, focused changes.
- Create branches from a reviewed, up-to-date `main`. Inspect the working tree first and preserve unrelated changes.
- Use `<prefix>/<issue-number>-<short-description>` when an Issue exists, or `<prefix>/<short-description>` otherwise. Use lowercase words separated by hyphens.
- Suggested prefixes are `fix`, `feat`, `docs`, `test`, `security`, and `chore`; examples are `fix/123-database-port-settings` and `docs/github-workflow`.
- Keep each branch focused on one Issue or coherent outcome. Explain when related Issues belong in the same change.
- Creating or switching branches requires explicit user approval. A naming convention does not authorize either action.

## Pull Request Workflow

- Codex may automatically open an associated Pull Request after the implementation and intended scope have been explicitly approved, changes have been reviewed, appropriate validation has been performed or outstanding validation clearly reported, and the branch has been committed and pushed with explicit user authorization.
- An approved push of an implementation branch permits opening the associated Pull Request without separate approval. It does not authorize further file edits, staging, commits, pushes, or merges, or modification of existing Issues.
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
- Before requesting merge approval, review the final diff, available CI checks, acceptance criteria, known limitations, and every Issue the merge would close. Obtain approval for those closures as part of the merge scope.
- Every merge requires explicit user approval. Never enable automatic merging.
- Do not assume GitHub Actions or branch protection are enabled. Respect configured requirements and accurately report unavailable or unexecuted checks; a documented self-review is appropriate for solo development unless repository rules require another reviewer.
- After opening a Pull Request, report its number, URL, purpose, and Draft status.
- After an authorized merge, verify the resulting branch, linked Issue states, and repository status. Merging does not replace the existing milestone-completion requirements.

## Initial Workflow Bootstrap

- The first collaboration-workflow Pull Request changes only `AGENTS.md` and uses the already approved branch `docs/github-workflow`.
- It does not require an existing Issue; explain the bootstrap purpose in the Pull Request description.
- Initial backlog triage and creation, repository labels, Issue and Pull Request templates, GitHub Actions, and repository protection are separate tasks.
- Normal approval requirements continue to apply. Automatic Issue or Pull Request creation remains subject to explicit restrictions in the current task.

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
4. Wait for approval before modifying files.
5. Implement the approved changes.
6. Explain the code and important decisions.
7. Validate the implementation.
8. Review the results with the user.

## Milestone Completion

When a milestone is completed:

1. Validate the implemented functionality.
2. Update `README.md` while preserving its formatting.
3. Review Git changes.
4. Create a commit only after user approval.
5. Push changes only after user approval.
6. Confirm that the working tree is clean.

## Important

This is a learning-focused project.

Codex should act as a development assistant, helping the user understand and implement each change rather than completing entire milestones without supervision.
