---
title: "Always-on Hermes: Moving a desktop AI agent into the homelab"
date: 2026-09-24
project: "Hermes on Proxmox"
summary: "A detailed account of moving Hermes Agent from one workstation to an always-on Debian VM, preserving its working state, cutting messaging over safely, and keeping every remote service private."
tags: ["Hermes Agent", "Proxmox", "Debian", "Tailscale", "systemd", "Homelab", "Migration"]
draft: false
---

Hermes originally ran only on my Omarchy workstation. That was convenient for changing local files and desktop settings, but it tied scheduled work, messaging, and long-running tasks to one machine. If the workstation was asleep, rebooting, or away from the network, the agent was unavailable.

The goal of this project was to make Hermes an **always-on homelab service** without losing the ability to use a local Hermes instance for workstation-specific work. The result is a hybrid design: a Debian virtual machine handles persistent services, while the workstation keeps its own local installation for tasks that need direct access to the desktop.

No private network addresses, hostnames, usernames, credentials, message targets, or authentication material are included in these notes.

## What I wanted from the migration

The project had several requirements beyond simply installing Hermes on another computer:

- Keep the remote agent available continuously, including after logout or reboot.
- Preserve conversations, memory, skills, scheduled jobs, project files, and Git history.
- Preserve untracked work and project configuration instead of copying only committed files.
- Avoid wasting transfer time and storage on dependencies, caches, virtual environments, and build output that could be regenerated.
- Keep Omarchy, Hyprland, local applications, and workstation files under the local Hermes instance.
- Move messaging without allowing two gateways to consume the same account at once.
- Keep the dashboard and backend off the public internet.
- Store secrets separately from public configuration and prevent them from appearing in command history or logs.
- Make every major step reversible.

## Final architecture

```text
Proxmox homelab
└── Debian 13 virtual machine
    ├── Hermes Agent runtime
    ├── Browser dashboard and remote backend
    ├── Messaging gateway
    ├── Skills, memory, sessions, cron jobs, and projects
    ├── systemd user services
    └── Tailscale private networking

Omarchy workstation
├── Hermes Desktop
├── Local Hermes backend
├── Local files and desktop configuration
└── Tailscale private networking
```

This split establishes a clear boundary. The VM is responsible for always-on work, messaging, remote sessions, and homelab integrations. The workstation installation remains responsible for local desktop settings, local applications, and files that should not be managed indirectly.

## Why I used a VM instead of an LXC

The Proxmox host is intentionally modest, so an LXC was considered. I chose a VM because Hermes may need a full Linux userspace, browser automation, Node sidecars, user-level systemd services, SSH, and future container workloads. A conventional Debian guest provides stronger isolation and avoids LXC-specific friction around device access, service management, and browser tooling.

The VM disk lives on the host's larger data storage rather than its small boot device. I started with conservative CPU and memory allocations and left room to adjust them from observed use instead of overcommitting the host.

## Building the server foundation

I installed a minimal Debian 13 guest with no desktop environment. The base system included OpenSSH, Git, certificate tools, the QEMU guest agent, and the packages required by Hermes. Hermes ran under an unprivileged user rather than `root`.

The runtime was installed fresh on the VM rather than copying a workstation installation byte for byte. At the time of migration, the validated stack included Hermes 0.21.4, Python 3.13, and Node 26. Installing the runtime first made it possible to run health checks before introducing old state.

User lingering was enabled so the Hermes services could start during boot and continue running after the service account logged out.

## Private networking and authentication

Tailscale provides the only remote path to the VM. The Hermes service is bound to the private overlay network and is not forwarded through the router or exposed on a public interface.

The non-loopback dashboard requires authentication. The server retains a password hash rather than recoverable plaintext. A recovery copy is stored separately in an owner-readable file on the workstation, and operational secrets are excluded from this repository and from these public notes.

SSH also uses dedicated key-based authentication. Service credentials are entered through hidden prompts and stored in owner-only files instead of being placed in shell arguments, scripts, or chat messages.

## Separating the Hermes services

One useful lesson was that Hermes has multiple service surfaces with different jobs:

- The **remote backend** supports desktop and API clients.
- The **browser dashboard** serves the web interface together with the backend.
- The **messaging gateway** runs channel adapters independently of the dashboard.

These were configured as separate systemd user services where appropriate. Keeping the gateway independent means the dashboard can be restarted or changed without interrupting messaging.

The dashboard's static web assets were built before the noninteractive service was enabled. Health checks then confirmed that the authenticated login page was being served instead of the headless backend's expected “web UI disabled” response.

## Deciding what to migrate

I did not copy the entire Hermes home directory blindly. The migration separated durable state from machine-specific or regenerable data.

### Preserved

- Agent memory and user profile data
- Conversation and session databases
- Custom skills and reusable procedures
- Scheduled jobs
- Messaging gateway state
- Relevant configuration
- Project source directories
- Complete Git repositories and history
- Untracked project files
- Project-specific configuration and secrets, transferred privately

### Regenerated or left behind

- Dependency directories such as `node_modules`
- Python virtual environments
- Build output
- Caches and temporary files
- Logs that were not needed for continuity
- Workstation-only application state

This kept the transfer smaller while still preserving the parts that could not be reconstructed from a package manager or Git remote.

## Migration and verification strategy

The transfer was staged rather than treated as one large copy operation:

1. Create a clean VM and a pre-migration backup.
2. Install Hermes and its runtimes from known sources.
3. Run Hermes health checks on the empty installation.
4. Inventory project roots and durable Hermes state.
5. Transfer source, Git metadata, untracked files, configuration, and selected agent state.
6. Exclude caches, dependencies, virtual environments, and generated output.
7. Rebuild or reinstall dependencies on the VM where required.
8. Validate file manifests, database integrity, permissions, and available disk space.
9. Start the remote backend and verify authenticated access over Tailscale.
10. Leave the local messaging gateway active until the remote gateway was ready for an explicit cutover.

The original workstation installation remained intact throughout the migration. It provided a rollback point and continues to serve machine-local work.

## The messaging cutover

Messaging was the highest-risk part of the move. Starting the new gateway before stopping the old one could create duplicate consumers, conflicting sessions, or corrupted provider state.

I built the cutover as an atomic operation with automatic rollback:

1. Back up both sides.
2. Copy the latest gateway state to the VM.
3. Disable and stop the local gateway.
4. Start the remote gateway.
5. Confirm that the real adapter processes are running.
6. Confirm that every required adapter reports a connected state.
7. Test outbound delivery.
8. Keep the remote gateway only if every check succeeds; otherwise restore the local gateway.

Several edge cases appeared during testing. The migrated configuration contained both legacy and current platform settings, and both had to agree. Process-ID checks were too broad and could mistake an SSH command for a real adapter, so verification was changed to match the actual child-process command lines. Adapter connection events were not reliably available through the system journal, so the readiness check moved to Hermes's canonical gateway-state file.

One provider also advanced its local credential state after connecting. The final synchronization had to preserve that newer remote state instead of overwriting it with an older snapshot. The reconnection window was lengthened to accommodate slower adapters.

The final cutover passed with the remote gateway enabled, the local gateway disabled, all required adapters connected, outbound delivery verified, and the migrated database healthy.

## Least-privilege homelab integrations

After the core migration, I added a restricted integration for selected media-management services. Instead of giving Hermes broad shell access to every application, I created a small client with a fixed set of read-only operations:

- Service status and version checks
- Health warnings
- Library lookup
- Download-queue inspection
- Missing-item reports
- Indexer status

API credentials are stored in an owner-only configuration file and are never printed by the client. The tool uses approved read-only endpoints and cannot add media, remove items, change settings, or trigger downloads. Mutating capabilities can be added later, but only as separately reviewed operations with explicit confirmation.

This pattern is now the model for future homelab integrations: private networking, a dedicated credential, the smallest practical permission set, a constrained wrapper, and verifiable output.

## Verification completed

The finished system was tested beyond checking whether processes appeared in a service list:

- Hermes health checks passed on the VM.
- The dashboard returned the authenticated sign-in experience over the private network.
- systemd services survived restarts and did not depend on an interactive login.
- The gateway spawned the genuine messaging adapter processes.
- Adapter state reported connected through Hermes's own state data.
- Outbound messaging tests succeeded after cutover.
- The local gateway remained stopped, preventing duplicate consumers.
- Session database integrity checks passed after transfer.
- Project repositories retained Git history, branches, working files, and untracked content.
- Read-only homelab commands were exercised against live services without exposing credentials.

## Problems solved along the way

### Headless backend versus browser dashboard

The initial remote endpoint was healthy but returned a message saying the web UI was disabled. The problem was not networking; the service was running the headless backend. Replacing that unit with the dashboard command and prebuilding the web assets produced the expected login interface.

### Configuration compatibility during upgrade

The migrated gateway contained settings from more than one configuration generation. A newer `gateway.platforms` section said the adapters were enabled, while older top-level flags still disabled them. Updating both locations resolved the conflict.

### False-positive process detection

A broad process search matched the command performing the check. The cutover now verifies exact adapter command lines and confirms application-level connection state separately.

### Logs were not the source of truth

Connection messages appeared in Hermes's application logs rather than the system journal. More importantly, the canonical state file was a better readiness signal than searching text logs, so the automation was redesigned around structured state.

### Provider state changed during testing

One messaging provider refreshed its credentials after a successful connection. A later rollback could have replaced those newer files with stale copies. The migration logic was changed to preserve remotely advanced provider state.

## Result

Hermes is now an always-on service in the homelab rather than an application tied to one desktop session. Scheduled work and messaging can continue when the workstation is unavailable, while local Hermes remains available for Omarchy and file-management tasks.

The project also produced a repeatable migration pattern: build the runtime cleanly, classify durable state, transfer projects without generated bulk, isolate secrets, stage risky cutovers, verify application state instead of assuming process health, and keep a tested rollback path until the new host has proven itself.

## Next steps

- Add Proxmox monitoring through a dedicated read-only API token.
- Add more narrowly scoped homelab tools instead of broad administrative access.
- Test backup restoration, not just backup creation.
- Add service-level monitoring and alerts for gateway or dashboard failures.
- Document resource use over time and right-size the VM from real measurements.
