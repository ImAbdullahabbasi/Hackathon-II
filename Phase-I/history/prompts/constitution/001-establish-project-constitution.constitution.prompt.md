---
id: 001
title: Establish Project Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["governance", "spec-driven-development", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

# Project Constitution: Evolution of Todo Hackathon II

This Markdown Constitution governs the entire "Evolution of Todo" project. All development must strictly follow **Spec-Driven Development** using Claude Code and Spec-Kit Plus.

## Core Rules
- **Spec-First**: Every feature, phase, component, and change begins with a detailed Markdown spec in `/specs/` folder.
- **No Manual Coding**: Never write code by hand. Write/refine spec → feed to Claude Code → generate implementation → iterate spec until correct.
- **Mandatory Tools**:
  - Use **UV** for all Python project management (`uv init`, `uv add`, `uv sync`, etc.).
  - Use **Claude Code** exclusively for code generation.
  - Use **Spec-Kit Plus** for spec organization and referencing.

## Project Phases & Progression
1. **Phase I** (Due Dec 7, 2025): In-Memory Python Console App (Basic features)
2. **Phase II** (Due Dec 14, 2025): Full-Stack Web App with Next.js + FastAPI + Neon DB + Better Auth (JWT)
3. **Phase III** (Due Dec 21, 2025): AI Chatbot using OpenAI ChatKit, Agents SDK, Official MCP SDK
4. **Phase IV** (Due Jan 4, 2026): Local Kubernetes deployment (Minikube, Docker, Helm, kubectl-ai, kagent)
5. **Phase V** (Due Jan 18, 2026): Cloud deployment (DOKS/GKE/AKS) + Kafka (Redpanda) + Dapr + Advanced features

Phases must be completed sequentially; each builds on URLs for each phase
- 90-second demo video per submission
- WhatsApp number for live presentation invites

## Enforcement
All Claude Code prompts must reference relevant specs using `@specs/path/to/file.md`. This constitution is the supreme governing document. Any deviation requires explicit spec update approved via Claude Code iteration.

Adopted: December 30, 2025

## Response snapshot

**Constitution v1.0.0 established successfully.**

Updated `.specify/memory/constitution.md` with:
- **5 Core Principles**: Spec-First Development, No Manual Coding, Mandatory Tooling, Phased Delivery, Spec-Driven Verification
- **5 Project Phases** with scope and deliverables (Phase I completed; Phase II–V planned through Jan 18, 2026)
- **Technology Stack**: FastAPI, Next.js, UV, Docker, Kubernetes, Neon DB, Better Auth
- **Code Quality Standards**: Acceptance scenarios, Claude Code generation, integration testing, no hardcoded secrets
- **Enforcement & Compliance**: Code review checklist, amendment process, runtime guidance references
- **Deliverables & Submission**: Per-phase format (demo video, live presentation, code repo, deployment URL, README)
- **Governance**: Constitution is supreme; compliance review required per phase

Version 1.0.0 | Ratified: 2025-12-30 | Inaugural document.

## Outcome

- ✅ Impact: Project constitution established as governing document; provides clear guidance for Spec-Driven Development workflow across all five phases
- 🧪 Tests: None (governance document; no executable tests)
- 📁 Files: `.specify/memory/constitution.md` (1 file created/modified)
- 🔁 Next prompts: Execute `/sp.specify` to create Phase II feature specs; execute `/sp.plan` for Phase II planning
- 🧠 Reflection: Constitution successfully consolidates project vision, tooling decisions, and phase progression into a single authoritative document. All templates (spec, plan, tasks, phr) already align with constitutional principles.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS (all placeholder tokens replaced, no unresolved brackets, dates in ISO format, version semantic versioning applied, file exists at expected path under history/prompts/constitution/)
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None; constitution is complete and ready for Phase II feature specification work
