# Dev Hub Host Contract

This document defines the **explicit contract** for the Dev Hub host machine.

It exists to eliminate ambiguity, prevent drift, and make it clear when the host is *done*.  
It translates intent into boundaries and replaces judgment calls with defaults.

This contract is intentionally strict. Its purpose is not flexibility, but **long-term calm**.

---

## 1. Purpose of the Dev Hub Host

The Dev Hub host exists for one reason only:

> **To run reproducible development environments defined by the Dev Hub.**

It is not:
- a personal computer
- a daily driver
- a storage location
- a place to experiment
- an object of optimization

The host is infrastructure.

---

## 2. Replaceability and disposability

The Dev Hub host is considered **fully disposable**.

- Reinstalling the OS is an acceptable response to failure.
- Local data loss is acceptable if not committed to version control.
- Emotional attachment to the host is explicitly discouraged.

The expected recovery time after total loss is **one evening**.

If recovery takes longer, the setup has violated this contract.

---

## 3. Data ownership and backups

The Dev Hub host has **no automatic backups**.

- Git remotes are the primary and sufficient backup mechanism.
- No cloud sync services are allowed on the host.
- No local data is considered critical unless explicitly pushed.

If data is lost that was not pushed, the loss is accepted without remediation.

---

## 4. Scope discipline: host vs environments

The host must remain minimal.

### Allowed on the host:
- Operating system
- System updates
- Docker
- VS Code
- SSH
- Basic system utilities required by the OS

### Explicitly forbidden on the host:
- Language runtimes (Node, Python, etc.)
- Build tools
- Compilers
- Package managers
- Project-specific tooling

If a tool is needed for development, it belongs **inside a container**.

Exceptions are allowed only if:
- the tool cannot reasonably run in a container
- the exception is documented explicitly

---

## 5. Identity and usage boundaries

This OS is used **only** for Dev Hub work.

- No personal email accounts
- No social media
- No media consumption
- No casual browsing
- No personal documents

Booting into this OS signals a clear mental state: *I am here to build.*

---

## 6. Customization policy

Customization is minimized by default.

- Default UI choices are accepted.
- Shell customization is avoided unless strictly necessary.
- Extensions and plugins are added only when there is real, repeated pain.

Comfort is achieved through stability, not personalization.

---

## 7. Updates and maintenance

The host favors **predictable, infrequent updates**.

- LTS releases are preferred.
- Rolling-release behavior is explicitly rejected.
- Updates are applied deliberately, not continuously.

The system should surprise as little as possible.

---

## 8. Failure and recovery posture

When problems occur:

- Reinstallation is preferred over deep debugging.
- Host-level debugging is considered a last resort.
- Logs and diagnostics are used only to support fast recovery.

Time spent debugging the host itself is considered high-cost and low-value.

---

## 9. Completion criteria (“host is done”)

The host is considered **done** when:

- The OS is installed and updated
- Docker is installed and working
- VS Code is installed and can open devcontainers
- SSH keys are configured
- The Dev Hub baseline repository opens successfully in a container

Once these criteria are met:
- the host is frozen
- further changes are discouraged
- improvements require explicit justification

---

## 10. Change discipline

Changes to the host are:
- rare
- intentional
- documented when non-obvious

The default answer to “should I change the host?” is **no**, unless there is real pain.

---

## Closing statement

This contract exists to protect focus.

The Dev Hub host should fade into the background,  
so attention can remain on building meaningful software — not maintaining the machine that hosts it.

If this contract ever feels restrictive, that is a signal to revisit *how the work is done*, not the contract itself.
