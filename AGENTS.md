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
