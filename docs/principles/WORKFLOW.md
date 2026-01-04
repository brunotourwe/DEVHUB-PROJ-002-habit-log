# Workflow

## Rationale
This document makes the implicit Dev Hub workflow explicit without changing
existing principles. It separates rules that are already implied by current
docs from rules that need confirmation.

## Workflow Summary (Derived)
- Boot into the Dev Hub host with intent to build.
- Open the repo in VS Code and attach to the project devcontainer.
- Work entirely inside containers using the base toolchain.
- Keep changes incremental and reviewable; rely on enforced tooling.
- Commit and push meaningful work because the remote is the backup.
- Document deviations where they occur.

## Rules

### Derived Rules (Already Implied)
- Containers: all development tooling and execution happens in devcontainers;
  host tooling stays minimal.
- Devcontainers: project devcontainers derive from the base; base standards are
  not bypassed.
- Editor: VS Code is used attached to devcontainers; host-level execution of
  project tooling is discouraged.
- Tooling: formatting, linting, typing, and validation are enforced; failures
  are addressed immediately.
- AI usage: AI can implement and refactor, but humans own intent and
  architecture; AI output is reviewed and must pass the same enforcement.
- AI suggestions are treated as untrusted input until reviewed.
- Documentation: exceptions or changes to foundational behavior are documented
  close to the change.

### Project to GitHub Lifecycle (Host-Level)
- `git init` happens on the host immediately after project creation.
- A GitHub repository is created right after local initialization.
- `gh repo create` is used on the host to create the remote repository.
- A project is not considered real until:
  - a local git repo exists,
  - a GitHub remote exists,
  - and the initial push has succeeded.
- Devcontainers assume the repo and remote already exist; this lifecycle stays
  host-level.

### Proposed Rules (Require Confirmation)
- The following rules are suggestions that require explicit acceptance before
  becoming binding.
- Containers: if new tooling is required, add it to the base or project
  devcontainer, never the host; document base devcontainer changes with a short
  rationale.
- Branching: `main` is the default branch; use short-lived branches for
  non-trivial code changes; direct commits to `main` are acceptable for small 
  documentation or clearly low-risk edits.
- Commits: keep commits scoped to a single intent; avoid mixing unrelated
  changes; commit only after relevant checks pass; push at least once per
  session or after meaningful progress.
- Reviews: before merging or finalizing changes, perform a self-review of the
  diff and confirm AI-generated changes for behavior and structure.
- Validation: run the smallest set of checks that prove the change is safe; if
  a check is skipped, record the reason.
- AI usage: large AI outputs are broken into smaller, reviewable changes before
  integration.

### Opening projects
DevHub is a monorepo.
For development, always open a project directory directly in VS Code.
Devcontainers are project-scoped by design.