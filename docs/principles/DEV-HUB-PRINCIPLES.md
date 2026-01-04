# Dev Hub Principles

## Document metadata
- Version: v1
- Date: 2026-01-01
- Summary: Consolidated baseline principles for the Dev Hub, bootstrap, devcontainers, tooling, editor baseline, repository structure, and AI usage.

## 1. Purpose and Scope

The Dev Hub exists to support how I build software over the long term.

Its purpose is to remove unnecessary friction, reduce repeated decision-making, and provide a stable, reproducible foundation for developing software products that are intended to live and evolve over years rather than weeks.

This document defines the core principles and high-level decisions that govern the Dev Hub. It focuses on *why* certain choices are made and *what* constraints they impose, not on detailed implementation steps.

These principles apply to all software development activities that take place within the Dev Hub, regardless of the specific product or project.

Execution behavior is defined in WORKFLOW.md.

---

## 2. Guiding Philosophy

I optimize for long-term sustainability over short-term convenience.

This means accepting slightly higher upfront effort in exchange for:
- lower cognitive load over time,
- easier re-entry after long breaks,
- predictable behavior across projects,
- and the ability to rebuild the development environment without loss of context.

I assume that tools, hardware, and even preferences will change. The Dev Hub is designed to absorb that change without forcing constant re-evaluation of fundamentals.

Consistency, clarity, and explicit decisions are valued more than novelty or experimentation at the infrastructure level.

---

## 3. Long-Term Goals

The Dev Hub is designed with the following long-term goals in mind:

- **Longevity**  
  Projects should remain understandable, runnable, and evolvable years after their creation.

- **Rebuildability**  
  A complete development environment must be recoverable after hardware replacement or failure, without relying on undocumented local state.

- **Low Decision Fatigue**  
  Common choices (tooling, structure, conventions) are decided once and reused.

- **AI-Assisted Development**  
  The environment and conventions should enable effective collaboration with AI tooling while preserving architectural coherence.

- **Scalability of Scope**  
  The Dev Hub should support growth from small personal projects to larger, more complex systems without requiring a fundamental redesign.

---

## 4. Core Decisions (Locked)

The following decisions are considered foundational and are not expected to change frequently. Deviating from them is allowed only with a clear reason and explicit documentation.

### 4.1 Development Mindset

- I focus on building a small number of serious, long-lived products.
- The Dev Hub is treated as a long-term asset, not a disposable setup.

### 4.2 Operating System

- The primary development environment runs on **bare-metal Linux**.
- Hardware is considered replaceable; the environment is not.
- Rebuildability is a first-class requirement.

### 4.3 Repository Strategy

- A **mono-repo** approach is used to maximize reuse, consistency, and refactorability.
- Shared tooling, conventions, and types are preferred over duplication.

### 4.4 Language and Type Discipline

- **TypeScript** is the primary language.
- Strict typing is enabled from the start.
- Explicitness and readability are preferred over cleverness.

### 4.5 Containers as the Environment

- The real development environment lives inside containers.
- The host operating system exists primarily to run containers and provide an editor and browser.

### 4.6 Container Runtime

- Docker is the standard container runtime for development.
- The Dev Hub is Docker-first and assumes Docker semantics.
- Alternative runtimes are not actively supported, but unnecessary coupling is avoided where reasonable.

### 4.7 AI as a Development Actor

- AI is used as an implementation and refactoring partner.
- Architectural and structural decisions are made consciously by me.
- AI is not allowed to define system architecture or long-term direction.

---

## 5. Non-Goals and Explicit Exclusions

The Dev Hub explicitly does **not** aim to:

- Maximize experimentation with tooling or frameworks.
- Serve as a generic or one-size-fits-all development environment.
- Optimize for rapid throwaway prototypes.
- Mirror enterprise-scale processes without clear benefit.

Personal preferences such as visual theming, shell aesthetics, or editor appearance are considered out of scope unless they directly affect productivity or reproducibility.

---

## 6. Governance and Change Discipline

The Dev Hub evolves deliberately.

Changes to foundational decisions are expected to be:
- intentional,
- justified,
- and documented.

When deviations or exceptions are necessary, they are recorded where they occur along with a brief rationale and scope. The format is intentionally lightweight.

If a principle no longer serves its purpose, it may be changed, but the reasoning behind that change must be recorded so that future decisions remain understandable.

Automation is preferred over personal discipline wherever possible, especially for enforcing formatting, consistency, and baseline standards.

---

## 7. Structure of the Dev Hub

The Dev Hub is organized into clearly defined domains, each with a specific responsibility. At a high level, these domains include:

- environment bootstrap and recovery,
- container definitions,
- development standards and conventions,
- and essential tooling configuration.

Each domain exists to answer a specific class of questions and should remain focused on that responsibility.

---

## 8. Relationship to Projects

Projects live *within* the Dev Hub but are not the Dev Hub itself.

The Dev Hub defines the environment and rules under which projects operate. Projects may have additional constraints or tooling, but they inherit the foundational decisions defined here by default.

---

## 9. Status and Evolution of This Document

This document is a living but stable reference.

It is expected to grow as additional domains (such as bootstrap procedures, container definitions, and tooling standards) are defined in more detail.

Sections may be expanded, but existing principles should not be casually weakened or contradicted. When changes are necessary, they should be explicit and traceable.

---

*Status: Foundational principles, incorporated into consolidated v1 document.*

## 10. Operational Conventions

DevHub-wide operational conventions are documented separately and apply to all DevHub-managed projects.

Port allocation is defined in `docs/DEVHUB-PORT-ALLOCATION.md`.

## Bootstrap: Host Environment Foundations

### Purpose

Bootstrap defines the minimal and explicit steps required to bring a fresh host operating system to a state where the Dev Hub can operate as intended.

Its purpose is not convenience, but **reliability**:
- to ensure the development environment can be rebuilt predictably,
- to minimize hidden assumptions,
- and to provide confidence that the host system is in a known, supportable state.

Bootstrap exists to make hardware replaceable and environment loss recoverable.

---

### Scope and Responsibility

Bootstrap is responsible only for preparing the **host operating system** to run the Dev Hub.

It explicitly does **not**:
- install language runtimes,
- configure project-specific tooling,
- manage development dependencies,
- or perform any product setup.

All development environments, runtimes, and tooling live inside containers. The host exists to support them.

---

### Supported Operating System

The Dev Hub standardizes on **Ubuntu Long-Term Support (LTS)** releases.

Interim or non-LTS releases are not supported. This choice prioritizes:
- stability over novelty,
- predictable upgrade cycles,
- and long-lived documentation.

---

### Host-Level Tooling Policy

Only a minimal, well-defined set of tools is allowed on the host operating system.

Allowed host-level tools are limited to:
- system fundamentals provided by the OS,
- core utilities such as Git, SSH, and network tools,
- the container runtime,
- a code editor and terminal,
- and a web browser for documentation and authentication.

Language runtimes, build tools, databases, and project-specific CLIs are explicitly excluded from the host.

If a tool is required for development, it belongs in a container.

Where a host tool can be installed through multiple channels, the chosen channel should be noted in Dev Hub documentation to avoid drift.

---

### Package Management

Bootstrap uses the system package manager (`apt`) exclusively.

Alternative installation mechanisms (such as snaps or ad-hoc installers) are not used for Dev Hub requirements, in order to preserve predictability and auditability.

---

### Privilege Model

Bootstrap scripts may invoke elevated privileges via `sudo` where required.

Scripts are expected to be:
- explicit about privilege use,
- safe to re-run,
- and to fail clearly if prerequisites are not met.

Bootstrap does not assume root login and does not manage user accounts.

---

### Container Runtime

Docker is the standard container runtime for the Dev Hub.

Bootstrap is responsible for:
- installing Docker,
- ensuring the Docker daemon is operational,
- and enabling non-root usage for the primary user.

Deep daemon customization is out of scope unless explicitly documented as a deliberate decision.

---

### Network Assumptions

An active internet connection is required during bootstrap.

Bootstrap does not attempt to support offline installation or degraded connectivity scenarios. This constraint is intentional and simplifies both scripts and documentation.

---

### Failure and Verification

Bootstrap follows a **fail-fast** philosophy.

If a required condition is not met, bootstrap stops and reports the issue clearly rather than attempting partial recovery.

Verification distinguishes between:
- **critical requirements**, which must be satisfied to proceed,
- and **non-critical conditions**, which may generate warnings but do not block progress.

A system that passes bootstrap verification is considered a valid host for the Dev Hub.

---

### Change Discipline

The scope and responsibilities of bootstrap are intentionally narrow.

Expanding or altering bootstrap behavior is allowed only through explicit, documented decisions. Bootstrap should remain focused on host preparation and must not evolve into a general-purpose setup mechanism.

---


## Base Devcontainer: Canonical Development Environment

### Purpose

The Base Devcontainer defines the **canonical development environment** for all projects within the Dev Hub.

Its purpose is to provide:
- a predictable and reproducible execution environment,
- a shared baseline across projects,
- and a stable foundation that supports long-term maintenance and AI-assisted development.

The Base Devcontainer is the primary point where development standards are enforced. The host operating system exists only to run it.

---

### Role of the Base Devcontainer

The Base Devcontainer is responsible for:
- providing language runtimes and core development tooling,
- enforcing baseline conventions and standards,
- defining the default execution context for development,
- and ensuring consistent behavior across projects and machines.

Projects do not redefine these fundamentals. They build upon them.

---

### Scope and Boundaries

The Base Devcontainer deliberately occupies a **middle ground** between minimalism and convenience.

It is not:
- a project-specific environment,
- a fully generic “one size fits all” container,
- or a dumping ground for experimental tools.

It is:
- opinionated,
- stable,
- and intentionally conservative.

Anything added to the Base Devcontainer must justify its presence across *most* projects and over a *long* time horizon.

---

### Language and Runtime Policy

The Base Devcontainer provides the primary language runtime(s) used across the Dev Hub.

For this Dev Hub:
- TypeScript is the primary development language.
- The Node.js runtime is provided by the Base Devcontainer.
- Runtime versions are explicitly defined and controlled.

Language runtimes are never installed on the host. The container defines reality.

---

### Package Manager Standard

- pnpm 10.x is the standard package manager for this Dev Hub.
- The Base Devcontainer provides and pins pnpm; projects must not substitute it without explicit justification.

---

### Tooling Philosophy

The Base Devcontainer includes only tooling that meets **at least one** of the following criteria:
- required by nearly all projects,
- enforces shared standards,
- or significantly reduces cognitive overhead.

Examples include:
- language tooling,
- formatting and linting tools,
- test runners,
- and essential CLI utilities.

Convenience tools that are rarely used or project-specific are excluded and belong in project-level containers.

---

### Enforcement of Standards

The Base Devcontainer is the primary mechanism for enforcing:
- formatting rules,
- linting rules,
- baseline project structure expectations,
- and language strictness.

Wherever possible, standards are enforced automatically rather than relying on personal discipline.

If a standard cannot be enforced programmatically, its value should be questioned.

---

### Relationship to Project Devcontainers

All project devcontainers must be **derived from the Base Devcontainer**.

Projects may:
- add services (e.g. databases),
- add project-specific tools,
- or extend configuration where necessary.

Projects may not:
- weaken or bypass base standards,
- redefine language versions arbitrarily,
- or contradict core Dev Hub principles.

This inheritance model ensures consistency while allowing controlled specialization.

---

### AI-Assisted Development Considerations

The Base Devcontainer is designed to support effective AI-assisted development.

This includes:
- predictable tooling versions,
- consistent project structure,
- explicit boundaries between concerns,
- and clarity in configuration.

The goal is to make AI behavior more reliable by reducing ambiguity in the environment.

---

### Stability and Change Discipline

The Base Devcontainer is treated as a **stable contract**.

Changes to it:
- are intentional and infrequent,
- consider impact across all projects,
- and are documented when they alter behavior or expectations.

When a change is necessary, it is preferred to evolve the Base Devcontainer gradually rather than introduce breaking shifts.

---

### Non-Goals

The Base Devcontainer explicitly does not aim to:
- include every possible development tool,
- track the latest runtime versions aggressively,
- or optimize for short-lived experiments.

Its value lies in stability, clarity, and shared understanding.

---


## Project Devcontainers: Controlled Specialization

### Purpose

Project Devcontainers exist to extend the Base Devcontainer with **project-specific requirements** while preserving the guarantees and constraints defined at the Dev Hub level.

Their purpose is to allow individual projects to:
- add the tools and services they need,
- remain isolated from other projects,
- and evolve independently,

without fragmenting the overall development environment.

---

### Relationship to the Base Devcontainer

Every Project Devcontainer **must be derived from the Base Devcontainer**.

The Base Devcontainer defines:
- language runtimes,
- core tooling,
- baseline standards,
- and shared assumptions.

Project Devcontainers may extend this foundation, but they may not replace or bypass it.

This inheritance model is intentional and non-negotiable.

---

### Scope of Project-Level Customization

Project Devcontainers are the correct place for:
- project-specific dependencies,
- supporting services (e.g. databases, caches, message brokers),
- domain-specific CLIs or build tools,
- and configuration that is irrelevant outside the project.

They are not the place for:
- redefining language versions,
- disabling linting or formatting rules,
- or introducing alternative toolchains without explicit justification.

---

### Service Inclusion Policy

Project Devcontainers may include additional services required for development, such as:
- relational or non-relational databases,
- in-memory caches,
- background workers,
- or local emulations of external systems.

Services included at the project level must:
- be declared explicitly,
- be scoped to the project,
- and not introduce cross-project dependencies.

If a service is needed by many projects, it should be evaluated for inclusion at the Base Devcontainer level instead.

---

### Isolation and Independence

Each Project Devcontainer is treated as an **independent environment**.

Projects must not:
- rely on services running in other project containers,
- assume shared state outside their own container context,
- or depend on host-level tooling.

This isolation ensures that:
- projects can be paused and resumed independently,
- multiple projects can coexist without interference,
- and failures remain localized.

---

### Configuration and Secrets

Project Devcontainers may define configuration and secrets required for development.

However:
- secrets must never be hard-coded,
- sensitive values must not be committed to version control,
- and defaults should be safe and non-production.

The goal is to enable development realism without compromising security or portability.

---

### Evolution and Lifecycle

Project Devcontainers are expected to evolve alongside their projects.

Changes to a Project Devcontainer should be:
- intentional,
- documented when non-obvious,
- and evaluated for alignment with Dev Hub principles.

Projects may eventually be retired. Their Devcontainers should be disposable without affecting other projects or the Base Devcontainer.

---

### Anti-Patterns

The following patterns are explicitly discouraged:
- copying tooling into projects that already exists in the Base Devcontainer,
- diverging language versions between projects without strong justification,
- “just this once” overrides that silently become permanent,
- or using project containers to experiment with core infrastructure decisions.

Experiments that affect foundational assumptions belong in the Dev Hub, not in individual projects.

---

### Change Discipline

If a project repeatedly requires a deviation from the Base Devcontainer, this is treated as a **signal**, not an exception.

Such cases should trigger a deliberate evaluation:
- either the Base Devcontainer should evolve,
- or the project should explicitly document why it is an outlier.

---


## Tooling and Enforcement: Making the Right Thing the Default

### Purpose

Tooling exists to **enforce standards**, not to express personal preference.

The purpose of tooling and enforcement within the Dev Hub is to:
- reduce reliance on personal discipline,
- eliminate repeated subjective decisions,
- and ensure that projects remain consistent and maintainable over time.

Wherever possible, correctness and consistency are enforced automatically.

---

### Enforcement Philosophy

I assume that:
- people forget,
- context switches happen,
- and standards degrade without reinforcement.

Therefore:
- enforcement is preferred over convention,
- automation is preferred over manual review,
- and failure should be immediate and explicit.

If a rule matters, it should be enforceable.  
If it cannot be enforced, its value should be questioned.

---

### Scope of Tooling

Tooling within the Dev Hub operates at three distinct levels:

1. **Base Devcontainer level**  
   Enforces universal rules that apply to all projects.

2. **Project Devcontainer level**  
   Adds project-specific tooling without weakening base guarantees.

3. **Repository-level automation**  
   Ensures consistency at commit, build, and validation time.

Each level has a clear responsibility and should not overlap unnecessarily with others.

---

### Formatting and Code Style

Code formatting is enforced automatically.

Formatting rules are:
- consistent across all projects,
- deterministic,
- and non-negotiable.

Discussions about formatting preferences are intentionally avoided.  
Once defined, formatting exists to eliminate debate, not create it.

---

### Linting and Static Analysis

Linting is used to:
- enforce correctness,
- surface potential bugs early,
- and reinforce shared conventions.

Linting rules should:
- favor clarity over cleverness,
- prioritize correctness and maintainability,
- and avoid excessive noise.

Warnings that are routinely ignored indicate a problem with the rules, not with developer behavior.

---

### Type Discipline Enforcement

Strict typing is enforced consistently.

Type-related rules are not treated as optional guidance.  
If code compiles, it should do so without suppressing meaningful type checks.

Type escapes (e.g. unsafe casts or disabling checks) are allowed only when:
- the reason is understood,
- alternatives are not viable,
- and the deviation is localized and explicit.

---

### Test and Validation Expectations

Automated validation exists to protect long-term confidence.

At minimum:
- projects must be able to validate themselves in isolation,
- validation must be repeatable and deterministic,
- and failures must be actionable.

The goal of validation is not exhaustive coverage, but **trust**:
- trust that changes did not silently break fundamentals,
- trust that refactors are safe,
- and trust that AI-generated code behaves as intended.

---

### Pre-Commit and Pre-Execution Checks

Checks that prevent bad state from entering the repository are preferred over post-hoc correction.

This includes, where appropriate:
- formatting checks,
- linting checks,
- and fast validation steps.

Blocking checks should be:
- fast,
- reliable,
- and clearly explained when they fail.

Slow or flaky checks undermine trust and should be avoided.

---

### Continuous Enforcement Over Time

Tooling is expected to evolve, but enforcement principles remain stable.

Changes to enforcement:
- are deliberate,
- consider the impact on existing projects,
- and are documented when behavior changes.

Relaxing enforcement is treated with the same seriousness as strengthening it.

---

### Relationship to AI-Assisted Development

Tooling acts as a **guardrail** for AI-assisted development.

Consistent formatting, strict typing, and deterministic validation:
- reduce ambiguity for AI tools,
- make generated code easier to review,
- and surface errors early.

AI-generated code is expected to pass the same enforcement rules as human-written code.

---

### Non-Goals

Tooling and enforcement explicitly do not aim to:
- enforce stylistic perfection,
- optimize for the shortest feedback loop at all costs,
- or replicate enterprise-scale CI processes unnecessarily.

The focus remains on **long-term sustainability**, not short-term velocity.

---


## VS Code Baseline: Editor as a Controlled Interface

### Purpose

VS Code is the standard editor interface for the Dev Hub.

Its purpose is not to define the development environment, but to **interact with it**:
- attach to devcontainers,
- edit code and documentation,
- run and inspect tooling,
- and collaborate effectively with AI-assisted workflows.

VS Code is treated as a **controlled interface**, not a personal playground.

---

### Role of the Editor

Within the Dev Hub, VS Code is responsible for:
- providing a consistent editing experience,
- integrating with the containerized environment,
- surfacing enforcement feedback early,
- and supporting structured, focused development.

The editor does not define runtime behavior.  
It reflects and interacts with the environment defined elsewhere.

---

### Standardization Level

VS Code usage is standardized to reduce friction and ambiguity.

This standardization is intentionally limited to:
- behavior that affects correctness,
- behavior that affects consistency,
- and behavior that affects collaboration or AI-assisted development.

Aesthetic preferences and purely personal ergonomics are not governed by the Dev Hub.

---

### Mandatory vs Recommended Configuration

VS Code configuration is divided into three categories:

1. **Mandatory**  
   Required for all projects. These settings and extensions are necessary for:
   - container integration,
   - enforcement feedback,
   - and baseline functionality.

2. **Recommended**  
   Useful defaults that improve productivity but are not strictly required.

3. **Personal**  
   Individual preferences that do not affect project behavior and remain out of scope.

Only Mandatory and Recommended items are documented by the Dev Hub.

---

### Container-Centric Workflow

VS Code is expected to be used primarily **attached to devcontainers**.

Projects are opened and worked on within their container context.  
Host-level execution of project tooling is explicitly discouraged.

This ensures:
- environment consistency,
- correct dependency resolution,
- and alignment with the Dev Hub execution model.

---

### Enforcement Visibility

VS Code is the first line of feedback for enforcement.

Formatting issues, lint warnings, and type errors should be visible:
- immediately,
- clearly,
- and in context.

The editor is expected to surface these signals early, reducing reliance on later validation steps.

---

### Relationship to Tooling and Automation

VS Code integrates with, but does not replace, tooling and automation.

Passing editor checks does not guarantee correctness.  
Failing editor checks is treated as a signal that issues should be addressed before progressing.

The editor supports enforcement; it does not redefine it.

---

### AI-Assisted Development in the Editor

VS Code is the primary interface for AI-assisted development.

This implies:
- predictable project structure,
- consistent file organization,
- and stable configuration.

AI-assisted actions are expected to respect the same standards and constraints as manual edits.

The presence of AI tooling does not relax enforcement expectations.

---

### Change Discipline

Changes to the VS Code baseline are treated as **behavioral changes**.

They are:
- deliberate,
- documented when non-obvious,
- and evaluated for impact across projects.

The baseline is expected to evolve slowly and intentionally.

---

### Non-Goals

The VS Code baseline explicitly does not aim to:
- mandate visual themes or fonts,
- standardize keybindings,
- optimize for every personal workflow variation,
- or replace developer judgment.

Its role is to provide a stable, predictable interface — not to eliminate individuality.

---


## Repository Structure and Templates: Enabling Consistent Growth

### Purpose

The repository structure defines how code, configuration, and documentation are organized within the Dev Hub.

Its purpose is to:
- reduce structural decision-making,
- enable safe reuse of shared components,
- support long-term evolution,
- and provide predictable locations for both humans and AI to reason about the system.

Structure is treated as a tool for clarity, not as an expression of creativity.

---

### Mono-Repo as the Default Model

The Dev Hub uses a **mono-repo** as its default repository model.

All projects, shared components, and supporting services live within a single repository. This enables:
- atomic refactoring across projects,
- consistent tooling and standards,
- shared type definitions and utilities,
- and improved context for AI-assisted development.

The mono-repo is considered a long-lived asset and is expected to grow over time in a controlled manner.

---

### High-Level Repository Layout

The repository is organized into **clear functional domains**, each with a distinct responsibility.

At a conceptual level, the repository distinguishes between:
- **applications** (end-user products or services),
- **shared packages** (reusable code),
- **infrastructure and configuration** (Dev Hub-related assets),
- and **documentation**.

The exact directory names may evolve, but the separation of concerns must remain explicit.

---

### Applications

Applications represent complete, runnable products or services.

Each application:
- has a clear ownership and purpose,
- is independently buildable and testable,
- and is developed within its own Project Devcontainer.

Applications do not directly depend on each other’s internal implementation details. Shared functionality is extracted into reusable packages instead.

---

### Shared Packages

Shared packages contain reusable code such as:
- domain models,
- shared utilities,
- UI components,
- or cross-cutting logic.

Packages are designed to:
- have clear public APIs,
- minimize implicit coupling,
- and evolve deliberately.

Shared code exists to reduce duplication, not to centralize everything prematurely.

---

### Infrastructure and Dev Hub Assets

Infrastructure-related content includes:
- devcontainer definitions,
- tooling configuration,
- scripts related to bootstrap or enforcement,
- and other assets that support development rather than product logic.

These assets are clearly separated from application and package code to preserve conceptual clarity.

---

### Documentation Placement

Documentation lives alongside the code it describes.

High-level governance and principles are documented at the repository root.  
Project- or package-specific documentation lives close to its subject.

Documentation structure should make it obvious:
- where to find intent,
- where to find constraints,
- and where to find usage guidance.

---

### Templates and Scaffolding

Templates exist to reduce repetitive setup and enforce consistency.

Templates may be provided for:
- new applications,
- new shared packages,
- or other recurring structural elements.

Templates are:
- opinionated,
- minimal,
- and aligned with Dev Hub principles.

Scaffolding is intended to establish a correct starting point, not to generate complete solutions.

---

### Creating New Projects

Creating a new project should:
- follow a predictable process,
- result in a structure that already conforms to standards,
- and require minimal manual cleanup.

If creating a new project repeatedly involves the same manual corrections, the template or structure is considered insufficient.

---

### Evolution and Refactoring

Repository structure is expected to evolve.

However:
- structural changes are deliberate,
- large-scale refactors are preferred over incremental drift,
- and changes that affect multiple projects are treated with care.

The mono-repo model exists to make such refactors feasible rather than prohibitive.

---

### AI-Assisted Development Considerations

A consistent repository structure improves AI effectiveness.

Clear separation between applications, packages, infrastructure, and documentation:
- reduces ambiguity,
- improves code navigation,
- and makes AI-generated changes easier to review and reason about.

Structure is treated as a shared language between human and AI collaborators.

---

### Non-Goals

The repository structure explicitly does not aim to:
- mirror any specific framework’s conventions without justification,
- optimize for minimal directory depth at all costs,
- or support arbitrary project layouts.

Clarity and consistency take precedence over familiarity or trend alignment.

---


## AI Usage Rules: Human Intent, Machine Leverage

### Purpose

AI is treated as a **development accelerator**, not as a decision-maker.

The purpose of AI usage within the Dev Hub is to:
- increase implementation speed,
- reduce mechanical workload,
- assist with refactoring and explanation,
- and improve overall productivity,

while preserving human ownership of intent, structure, and long-term coherence.

AI is a tool. Responsibility remains human.

---

### Role of AI in the Dev Hub

Within the Dev Hub, AI is explicitly allowed to:
- generate implementation code based on clearly defined intent,
- refactor existing code while preserving behavior,
- suggest improvements to readability and structure,
- assist with test generation,
- explain existing code and documentation,
- and help surface potential issues or edge cases.

AI is not allowed to:
- define system architecture,
- choose foundational technologies,
- introduce new structural patterns without direction,
- or make long-term design decisions implicitly.

---

### Human Responsibilities

The human role in AI-assisted development is explicit and non-delegable.

I remain responsible for:
- defining intent and constraints,
- establishing architecture and boundaries,
- deciding what problems are worth solving,
- reviewing AI-generated output,
- and integrating changes deliberately.

Using AI does not reduce the obligation to understand the code that is produced.

---

### Prompting Discipline

AI output quality is directly influenced by input clarity.

Effective AI usage requires:
- clear articulation of goals,
- explicit constraints and assumptions,
- and incremental, focused requests.

Vague prompts are treated as a signal of unclear intent and are avoided.

When necessary, prompts should explicitly state:
- what must not change,
- what guarantees must be preserved,
- and what trade-offs are acceptable.

---

### Incremental and Reviewable Changes

AI-assisted changes should be:
- incremental,
- scoped,
- and reviewable.

Large, unbounded generations are discouraged.  
Smaller, composable changes improve trust and reduce integration risk.

AI-generated code is reviewed with the same rigor as human-written code.

---

### Relationship to Enforcement and Tooling

AI-generated code is subject to the same enforcement rules as all other code.

Formatting, linting, typing, and validation are not relaxed for AI output.

Tooling exists to surface issues early and to prevent silent degradation of standards, regardless of the source of the code.

---

### Use of AI for Exploration vs Integration

AI may be used freely for:
- exploration,
- ideation,
- and hypothesis generation.

However, exploratory output does not enter the codebase unless it is:
- reviewed,
- aligned with Dev Hub principles,
- and intentionally integrated.

The boundary between exploration and production is explicit.

---

### Avoiding Over-Reliance

AI assistance is used to reduce mechanical effort, not to replace reasoning.

If AI is repeatedly used to solve the same conceptual problem, this is treated as a signal that:
- the underlying design may be unclear,
- or additional documentation or structure is needed.

AI should amplify clarity, not compensate for its absence.

---

### Evolution of AI Usage

AI capabilities and tools are expected to evolve rapidly.

AI usage rules are therefore reviewed periodically, but changes are:
- deliberate,
- documented,
- and evaluated for long-term impact.

New AI capabilities do not automatically justify changes in responsibility boundaries.

---

### Non-Goals

AI usage within the Dev Hub explicitly does not aim to:
- fully automate development,
- remove the need for architectural thinking,
- or optimize for maximum code generation volume.

The goal remains **sustainable, understandable, and intentional software development**.

---
