# Evolution of Todo Hackathon II Constitution

<!--
SYNC IMPACT REPORT (v1.0.0 → v1.0.0)
- Constitution version: NEW (inaugural document)
- Principles established: 5 (Spec-First, No Manual Coding, Mandatory Tools, Phased Delivery, Spec-Driven Verification)
- Sections: Core Principles, Project Phases & Progression, Enforcement & Compliance, Technology Stack, Deliverables, Governance
- All dependent templates (spec, plan, tasks, phr) MUST reference this constitution in headers
- NOTE: Phase I deadline (Dec 7, 2025) has passed; constitutionalized for historical record and Phase II+ compliance
- Follow-up: Update README.md to reference this constitution document
-->

## Core Principles

### I. Spec-First Development
Every feature, phase, component, and change begins with a detailed Markdown specification in the `/specs/` folder. Specifications MUST include user scenarios, functional requirements, acceptance criteria, and success metrics before any code is written. Specifications are the source of truth; code must conform to spec, never the reverse.

**Rationale**: Prevents rework, ensures alignment with stakeholder intent, and enables asynchronous review and approval before engineering effort.

### II. No Manual Coding
Code is NEVER written by hand outside of Claude Code. The workflow is: write/refine spec → feed to Claude Code → generate implementation → iterate spec until correct. Hand-written code is prohibited except for configuration files and CLI commands executed within Claude Code sessions.

**Rationale**: Ensures consistency, traceability, and auditability; all code generation is logged and reversible.

### III. Mandatory Tooling
- **UV** is the ONLY Python package manager and project initialization tool (`uv init`, `uv add`, `uv sync`, etc.).
- **Claude Code** is the ONLY code generation and task execution tool.
- **Spec-Kit Plus** is the ONLY specification organization and templating framework.

**Rationale**: Single toolchain prevents tool fragmentation, ensures reproducible builds, and centralizes decision-making via spec review.

### IV. Phased Delivery with Sequential Completion
Development proceeds through five phases, each building on the previous. Phases MUST be completed in order; earlier phases are prerequisites for later ones. Each phase has explicit scope, acceptance criteria, and scheduled deadline.

**Rationale**: Reduces risk via incremental integration; allows course correction based on learnings from each phase.

### V. Spec-Driven Verification & Compliance
All Claude Code prompts MUST reference relevant specs using `@specs/path/to/file.md` syntax. Code reviews validate conformance to spec. This constitution is the supreme governing document; deviations require explicit spec update approved via Claude Code iteration.

**Rationale**: Traceability and audit trail; prevents scope creep and undocumented changes.

## Project Phases & Progression

### Phase I: In-Memory Python Console App (Due Dec 7, 2025)
**Status**: Completed (deadline passed)
**Scope**: Basic todo functionality in-memory, console interface
**Deliverables**: 90-second demo video, executable CLI binary, code repository

### Phase II: Full-Stack Web App (Due Dec 14, 2025)
**Scope**: React/Next.js frontend, FastAPI backend, Neon PostgreSQL database, JWT authentication via Better Auth
**Deliverables**: Deployed web application (URL), 90-second demo video, live presentation via WhatsApp

### Phase III: AI Chatbot Integration (Due Dec 21, 2025)
**Scope**: OpenAI ChatKit integration, Anthropic Agents SDK, Official MCP (Model Context Protocol) SDK
**Deliverables**: Chatbot-enabled application, AI-driven todo suggestions/automation, 90-second demo

### Phase IV: Local Kubernetes Deployment (Due Jan 4, 2026)
**Scope**: Minikube, Docker containerization, Helm charts, kubectl-ai, kagent integration
**Deliverables**: Kubernetes manifests, local deployment runbook, multi-container orchestration demo

### Phase V: Cloud Deployment & Advanced Features (Due Jan 18, 2026)
**Scope**: DOKS/GKE/AKS cloud deployment, Kafka/Redpanda streaming, Dapr (Distributed Application Runtime)
**Deliverables**: Production deployment on chosen cloud platform, event-driven architecture, advanced observability

## Technology Stack

### Mandatory Technologies
- **Language**: Python (backend), JavaScript/TypeScript (frontend)
- **Backend Framework**: FastAPI
- **Frontend Framework**: Next.js with React
- **Database**: Neon PostgreSQL (Phase II+)
- **Authentication**: Better Auth with JWT tokens
- **Package Management**: UV (Python), npm/yarn (Node.js)
- **AI Integrations**: OpenAI ChatKit, Anthropic Agents SDK, MCP SDK (Phase III+)
- **Containerization**: Docker (Phase IV+)
- **Orchestration**: Kubernetes/Minikube (Phase IV+), DOKS/GKE/AKS (Phase V+)
- **Streaming**: Redpanda/Kafka (Phase V+)
- **Service Mesh**: Dapr (Phase V+)

### Code Quality Standards
- Specifications MUST include acceptance scenarios (Given-When-Then format).
- All code MUST be generated via Claude Code; manual edits only for configuration.
- Testing: Integration tests required for new features; unit tests recommended where applicable.
- Security: No hardcoded secrets; use `.env` files and documented secret management.
- Observability: Structured logging, metrics collection (Phase III+), distributed tracing (Phase IV+).

## Enforcement & Compliance

### Code Review Checklist
All pull requests MUST verify:
1. ✅ Spec exists and is approved before code implementation
2. ✅ Code is generated via Claude Code (commit message includes attribution)
3. ✅ All referenced specs are linked in commit message using `@specs/path/to/file.md`
4. ✅ Tests pass (integration tests for multi-service changes)
5. ✅ No manual edits outside of Claude Code sessions
6. ✅ Constitution compliance verified (tooling, phase scope, deliverables)

### Amendment Process
This constitution may be amended to reflect:
- Regulatory or compliance changes
- Major architectural decisions (document as ADR per `@specs/*/adr/`)
- Phase scope adjustments (with Phase Lead approval)
- Tooling changes (with justification and migration plan)

Amendments are tracked in the "Last Amended" field and incremented per semantic versioning rules (MAJOR for principle removals, MINOR for additions, PATCH for clarifications).

### Runtime Guidance
For day-to-day development decisions, refer to:
- Feature specs in `/specs/<feature>/` (priority 1)
- Architecture Decision Records (ADRs) in `/history/adr/` (priority 2)
- Prompt History Records (PHRs) in `/history/prompts/` (priority 3, for context and learning)

## Deliverables & Submission

### Per-Phase Submission Format
Each phase submission includes:
1. **90-second demo video** (MP4, uploaded to shared drive or submitted link)
2. **Live presentation invite** via WhatsApp with demo walkthrough
3. **Code repository** with all commits referencing specs
4. **Deployment URL** (for web/cloud phases) or runbook (for containerized phases)
5. **README.md** with phase summary, getting started guide, and next steps

### Metrics & Success
- All acceptance scenarios (per spec) MUST pass
- No blocked/failing tests before submission
- Spec conformance verified in PR review
- Phase completion enables unblocking next phase

## Governance

This constitution is the supreme governing document for the Evolution of Todo project. All development practices, tooling choices, and delivery decisions MUST align with this constitution.

**Authority**: Constitution supersedes all other guidelines, templates, or conventions. Any practice not explicitly permitted by this constitution is prohibited.

**Scope**: Applies to all code, specifications, infrastructure, and documentation generated for any phase of this project.

**Compliance Review**: Every Phase Lead MUST confirm constitution compliance before marking a phase as complete.

---

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
