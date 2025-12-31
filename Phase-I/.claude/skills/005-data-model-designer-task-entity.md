# Skill: Task Entity Data Model Design

**Skill ID**: DMD-001
**Agent Owner**: data-model-designer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Design the Task entity data model for Phase 1 in-memory todo application. This skill defines all required and optional fields, data types, constraints, validation rules, and field semantics. The Task entity is the core domain object; its design directly impacts all features (create, list, delete, mark complete, filter, search, edit). The data model must be simple enough for in-memory storage while remaining extensible for future phases (web app, database, cloud).

---

## When to Use

- **Specification phase**: After acceptance criteria (PA-001) are defined, before implementation
- **Architecture planning**: Designing data structures for in-memory storage
- **Feature dependency mapping**: Understanding what fields each feature requires
- **API contract design**: When Phase II web API is planned, Task model becomes API contract
- **Database schema planning**: When Phase II moves to Neon PostgreSQL, Task model informs schema
- **Data migration planning**: When upgrading storage (memory → database → cloud), Task model ensures backward compatibility

---

## Inputs

1. **User stories** (list): Stories from requirements-analyst (RA-001) that define what task information users need
2. **Functional specifications** (document): Specifications from cli-ux-designer (CLI-001) showing what inputs/outputs each feature requires
3. **Acceptance criteria** (document): Criteria from product-architect (PA-001) showing what data must be present
4. **Business rules** (optional): Rules from business-logic-engineer (BLE-001) that constrain data values
5. **Phase II/III requirements** (optional): Forward compatibility considerations (will this work for web? API? Cloud?)

---

## Step-by-Step Process

### Step 1: Identify All Data Requirements
Review all features and extract what data must be stored for each task.

**Data Requirements Analysis**:

For **Create Task** feature:
- Task must have: unique ID, title, creation timestamp
- Task may have: due date, priority, description

For **List Tasks** feature:
- Task must display: ID, title, status, due date (if set)
- Task must be sortable by: creation date, due date, priority

For **Mark Complete** feature:
- Task must track: completion status, completion timestamp

For **Delete Task** feature:
- Task must have: unique ID (for deletion by ID)

For **Filter/Search** feature:
- Task must support filtering by: status, priority, due date range, search by title

**Example Data Requirements Table**:
```
Feature              | Required Fields        | Optional Fields
-------------------- | ---------------------- | ----------------------
Create Task         | id, title, created_at  | due_date, priority
List Tasks          | id, title, status      | due_date, priority
Mark Complete       | status, completed_at   | (none)
Delete Task         | id                     | (none)
Filter Tasks        | status, priority, due_date | (none)
Search Tasks        | title                  | (none)
```

### Step 2: Define Core Required Fields
These fields MUST exist for every task; no task is valid without them.

**Required Field Pattern**:
```
Field: [field_name]
  Type: [data_type]
  Purpose: [why this field is required]
  Constraints: [validation rules, format, allowed values]
  Example: [concrete example value]
  Phase 1: [mandatory/nice-to-have]
```

**Examples of Required Fields**:

```
Field: id
  Type: string (UUID or sequential string)
  Purpose: Unique identifier to reference, retrieve, update, delete task
  Constraints: Non-empty, unique across all tasks, immutable (never changes)
  Format: "task-001", "task-002", ... (sequential pattern)
  Example: "task-001"
  Phase 1: Mandatory

Field: title
  Type: string (text)
  Purpose: Human-readable task description; what user needs to do
  Constraints: Non-empty, max 255 characters, trimmed (no leading/trailing whitespace)
  Validation: Cannot be null, empty, or whitespace-only
  Example: "Buy groceries"
  Phase 1: Mandatory

Field: status
  Type: enum {pending, completed}
  Purpose: Track whether task is done or not
  Constraints: Must be one of: pending, completed
  Default Value: "pending" (when task created)
  Example: "pending"
  Phase 1: Mandatory

Field: created_timestamp
  Type: datetime (ISO 8601 format)
  Purpose: Record when task was created (for sorting, archiving, debugging)
  Constraints: Immutable, set to system time at creation
  Format: "2025-12-30T10:30:45Z" (UTC, ISO 8601)
  Example: "2025-12-30T10:30:45Z"
  Phase 1: Mandatory
```

### Step 3: Define Optional Fields
These fields enhance task functionality but aren't required for basic use.

**Optional Field Pattern** (same as required, but with default values):

```
Field: due_date
  Type: date (ISO 8601 date format)
  Purpose: When task should be completed; enables deadline-driven organization
  Constraints: Optional, valid date, can be past or future
  Format: "YYYY-MM-DD" (2026-01-15)
  Default Value: null (no due date)
  Example: "2026-01-15"
  Phase 1: Nice-to-have (support in create, but not required)
  Phase II+: Mandatory (important for web/calendar integration)

Field: priority
  Type: enum {low, normal, high}
  Purpose: Indicate task importance; enables prioritization and filtering
  Constraints: One of three values
  Default Value: "normal" (medium priority)
  Example: "high"
  Phase 1: Nice-to-have (support in create, but not required)
  Phase II+: Mandatory (important for UI sorting)

Field: description
  Type: string (text, multiline)
  Purpose: Additional details about task (notes, context, steps)
  Constraints: Optional, max 2000 characters
  Default Value: null (no description)
  Example: "Buy: milk, bread, eggs, cheese"
  Phase 1: Not included (defer to Phase II)
  Phase II+: Nice-to-have (add in web UI, optional field)

Field: completed_timestamp
  Type: datetime (ISO 8601 format)
  Purpose: Record when task was marked complete (for analytics, archiving)
  Constraints: Optional, null until task is marked complete, immutable after set
  Default Value: null (not yet completed)
  Example: "2025-12-31T15:22:10Z"
  Phase 1: Nice-to-have (track completion time when mark-complete feature used)
  Phase II+: Mandatory (important for reporting, time tracking)

Field: tags
  Type: array of strings
  Purpose: Categorize task (e.g., "work", "shopping", "urgent")
  Constraints: Optional, each tag max 50 characters, no duplicates
  Default Value: empty array []
  Example: ["shopping", "urgent"]
  Phase 1: Not included (defer to Phase II)
  Phase II+: Nice-to-have (enable filtering and organization)
```

### Step 4: Define Field Validation Rules
For each field, specify constraints that prevent invalid data.

**Validation Rule Pattern**:
```
Field: [field_name]
  Rule 1: [Constraint]
    - If violated: [Error message]
    - Why: [Reason this matters]
  Rule 2: [Constraint]
    - If violated: [Error message]
    - Why: [Reason this matters]
```

**Examples**:

```
Field: title
  Rule 1: Must not be empty (length > 0)
    - If violated: "Task title cannot be empty"
    - Why: Empty tasks are useless; prevent data quality issues
  Rule 2: Must not be whitespace-only
    - If violated: "Task title cannot contain only whitespace"
    - Why: Whitespace-only titles appear empty; confusing to users
  Rule 3: Max length 255 characters
    - If violated: "Task title too long (N chars). Max: 255"
    - Why: Prevents data bloat, ensures consistent display
  Rule 4: Must be trimmed (no leading/trailing whitespace)
    - If violated: [Auto-trim; this is corrective, not error]
    - Why: Whitespace at boundaries doesn't affect title semantically

Field: due_date
  Rule 1: If provided, must be valid date (YYYY-MM-DD format)
    - If violated: "Invalid date format. Expected YYYY-MM-DD, got 'X'"
    - Why: Date format ambiguity is major source of errors
  Rule 2: If provided, must be parseable date (not Feb 30, etc.)
    - If violated: "Invalid date. [reason: e.g., 'February has 28 days']"
    - Why: Prevents storing impossible dates
  Rule 3: Can be past or future (no restriction)
    - If violated: [No error; past dates allowed]
    - Why: Users need to track overdue tasks; backlog items may have old dates

Field: priority
  Rule 1: Must be one of: {low, normal, high}
    - If violated: "Invalid priority. Allowed: low, normal, high"
    - Why: Only these three values are meaningful for filtering/sorting
  Rule 2: If not provided, defaults to "normal"
    - If violated: [Auto-default; not an error]
    - Why: Consistent default behavior

Field: status
  Rule 1: Must be one of: {pending, completed}
    - If violated: "Invalid status. Allowed: pending, completed"
    - Why: Only these two states are valid in Phase 1
  Rule 2: Defaults to "pending"
    - If violated: [Auto-default; not an error]
    - Why: New tasks start as pending
  Rule 3: Can only transition pending → completed (or completed → pending for edit)
    - If violated: [No error in Phase 1; allow any transition. Phase II: enforce]
    - Why: Future phases may enforce strict state machine
```

### Step 5: Design Data Structure (In-Memory Representation)
Define how the Task entity is represented in memory for Phase 1.

**In-Memory Task Object (Pseudocode)**:

```
Task Object Structure:

{
  // Core Required Fields
  id: string,                           // "task-001"
  title: string,                        // "Buy groceries"
  status: enum(pending|completed),      // "pending"
  created_timestamp: datetime,          // "2025-12-30T10:30:45Z"

  // Optional Fields (Phase 1)
  due_date: date | null,                // "2026-01-15" or null
  priority: enum(low|normal|high),      // "normal"

  // Timestamps (Phase 1 nice-to-have)
  completed_timestamp: datetime | null, // null until completed

  // Reserved for Phase II
  // description: string | null,
  // tags: string[],
  // assigned_to: string | null,
  // recurrence: recurrence_rule | null,
}
```

**Language-Specific Examples**:

Python (Phase 1):
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

@dataclass
class Task:
    id: str                              # "task-001"
    title: str                           # "Buy groceries"
    status: TaskStatus = TaskStatus.PENDING
    created_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Optional fields
    due_date: Optional[str] = None       # "2026-01-15" (ISO format)
    priority: TaskPriority = TaskPriority.NORMAL
    completed_timestamp: Optional[datetime] = None
```

TypeScript (Phase II):
```typescript
enum TaskStatus {
  PENDING = "pending",
  COMPLETED = "completed"
}

enum TaskPriority {
  LOW = "low",
  NORMAL = "normal",
  HIGH = "high"
}

interface Task {
  id: string;                            // "task-001"
  title: string;                         // "Buy groceries"
  status: TaskStatus;                    // TaskStatus.PENDING
  created_timestamp: string;             // ISO 8601 datetime

  // Optional fields
  due_date?: string;                     // ISO 8601 date (YYYY-MM-DD)
  priority?: TaskPriority;               // TaskPriority.NORMAL
  completed_timestamp?: string;          // ISO 8601 datetime
}
```

### Step 6: Design Task Collection/List Storage
Define how multiple tasks are stored and indexed in memory.

**Collection Design**:

```
Task List Storage:

Primary Storage: List/Array of Tasks
  - Insertion order preserved
  - Index 0 is first created task (task-001)
  - Index N is most recent created task (task-N)
  - O(n) list operations (acceptable for Phase 1)

Secondary Index (Optional, for Phase 1 optimization):
  - ID Map: id -> Task
    Purpose: O(1) lookup by ID (for get, delete, update)
    Example: {"task-001": Task, "task-002": Task, ...}
  - Status Map: status -> [Task IDs]
    Purpose: O(1) filtering by status
    Example: {"pending": ["task-001", "task-003"], "completed": ["task-002"]}
  - Priority Map: priority -> [Task IDs]
    Purpose: O(1) filtering by priority
    Example: {"low": ["task-003"], "normal": ["task-001"], "high": ["task-002"]}

Example In-Memory Structure:

{
  tasks: [
    {
      id: "task-001",
      title: "Buy groceries",
      status: "pending",
      created_timestamp: "2025-12-30T10:30:45Z",
      due_date: "2026-01-15",
      priority: "normal",
      completed_timestamp: null
    },
    {
      id: "task-002",
      title: "Submit report",
      status: "completed",
      created_timestamp: "2025-12-30T11:00:00Z",
      due_date: null,
      priority: "high",
      completed_timestamp: "2025-12-30T14:30:00Z"
    },
    ...
  ],
  // Indexes (optional)
  id_map: {
    "task-001": <ref to tasks[0]>,
    "task-002": <ref to tasks[1]>,
    ...
  }
}
```

### Step 7: Plan Backward Compatibility
Design the Task entity so it can evolve to future phases without breaking existing code.

**Backward Compatibility Strategy**:

```
Phase 1 (Current):
  Required: id, title, status, created_timestamp
  Optional: due_date, priority, completed_timestamp

Phase II (Web App):
  New Required: user_id (which user owns task)
  New Optional: description, tags, assigned_to
  Strategy: Add as optional fields; existing Phase I tasks have null values

Phase III (AI/Chatbot):
  New Optional: ai_generated, ai_suggestions, confidence_score
  Strategy: Add as optional fields; Phase I/II tasks have null values

Phase IV (Kubernetes):
  New Optional: backup_id, last_synced_timestamp
  Strategy: Add as optional fields; no impact on existing tasks

Migration Strategy:
  - Never remove fields (only deprecate)
  - New required fields must have defaults for legacy tasks
  - Use versioning if structure changes significantly
  - Example: Add "version" field to track schema version
    { ..., version: 1 } for Phase 1
    { ..., version: 2, user_id: "user-123" } for Phase II
```

### Step 8: Validate Data Model Completeness
Ensure the Task entity covers all requirements without over-design.

**Validation Checklist**:
- ✅ All Phase 1 features have required fields documented
- ✅ All required fields have validation rules
- ✅ All optional fields have defaults or null values
- ✅ Data types are simple and language-agnostic (string, date, enum, datetime, array)
- ✅ No implementation-specific details (no database columns, no ORM annotations)
- ✅ Backward compatible: Can Phase 1 tasks be read in Phase II? Yes
- ✅ Forward compatible: Can Phase II fields be added to Phase 1 tasks? Yes
- ✅ Field naming is consistent (snake_case or camelCase throughout)
- ✅ Timestamps use ISO 8601 format (portable, human-readable)
- ✅ No circular references or complex object nesting (keep flat)

**Red Flags**:
- "Task has a User object" → Too complex; use user_id string instead
- "Status has 10+ values" → Too many states; Phase 1 only needs pending/completed
- "Priority is 1-100 numeric scale" → Overcomplication; 3 levels sufficient
- "Task can be duplicated" → Design issue; ID ensures uniqueness
- "Timestamps in milliseconds epoch" → Avoid; use ISO 8601 for portability

---

## Output

**Format**: Structured Markdown document with Task entity specification:

```markdown
# Task Entity Data Model

## Overview
[What is a Task? One sentence describing the domain object]

## Required Fields
[All fields that must exist; no task is valid without them]

## Optional Fields
[Fields that enhance functionality but aren't required]

## Field Specifications
[Detailed specification for each field]

## Validation Rules
[All constraints and validation per field]

## Data Structure
[How Task is represented in memory (pseudocode + language examples)]

## Collection/Storage
[How multiple tasks are stored and indexed]

## Phase Compatibility
[How this design evolves through Phase II, III, IV, V]

## Constraints & Trade-Offs
[Design decisions and rationale]

## Success Criteria
[Checklist for validating the model meets requirements]
```

---

## Failure Handling

### Scenario 1: Missing Required Field in Specification
**Symptom**: Feature requires data (e.g., filtering by due date range) but due_date field is not defined
**Resolution**:
- Review all features again; identify missing field
- Add field to optional or required section (based on Phase 1 scope)
- Ensure validation rules are defined
- Update code examples

### Scenario 2: Over-Design (Too Many Fields)
**Symptom**: Model includes fields not used by any Phase 1 feature (e.g., "recurrence", "tags", "assigned_to")
**Resolution**:
- Remove field or move to "Phase II+" section
- Follow YAGNI principle: only include what Phase 1 needs
- Keep model simple for in-memory implementation
- Document deferred fields for future phases

### Scenario 3: Data Type Ambiguity
**Symptom**: due_date could be string, date object, or timestamp; unclear which
**Resolution**:
- Define one canonical representation: string in ISO 8601 format "YYYY-MM-DD"
- Justify choice: portable across languages, human-readable, no timezone issues
- Document parsing rules (how strings are parsed to dates)
- Provide examples in multiple languages

### Scenario 4: Validation Rules Conflict with Constraints
**Symptom**: Field is "optional" but validation rule says "must not be null"
**Resolution**:
- Clarify: optional = not required at creation, but if provided must be valid
- Example: due_date is optional (user can skip it) but if provided must be valid date
- Update validation language: "If provided, due_date must be valid YYYY-MM-DD format"

### Scenario 5: Phase II Compatibility Issue
**Symptom**: Design assumes single-user, but Phase II needs multi-user (user_id field)
**Resolution**:
- Add user_id field now as optional (Phase 1 tasks have null user_id)
- OR design Phase 1 to use default user_id="system" (backward compatible)
- Plan migration strategy: how do Phase 1 in-memory tasks map to Phase II database?

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Feature implementation**: Developers reference this model to understand what fields to persist
- **API design**: Phase II API contract is directly derived from Task entity
- **Database schema**: Phase II Neon PostgreSQL schema matches Task entity structure
- **Data migration**: When upgrading storage (memory → DB → cloud), Task model is migration guide
- **Frontend design**: Phase II React/Next.js components use Task entity structure
- **Testing**: QA writes test data using Task model specification

---

## Success Metrics

- ✅ All Phase 1 features have required fields defined
- ✅ All required fields have mandatory validation
- ✅ All optional fields have sensible defaults
- ✅ Data types are simple and language-agnostic
- ✅ Validation rules are comprehensive (not just existence checks)
- ✅ Model is backward compatible (Phase 1 tasks work in Phase II)
- ✅ Model is forward compatible (Phase II fields don't break Phase 1)
- ✅ No over-design (only fields actually used are included)
- ✅ Timestamps use ISO 8601 (portable, standard)
- ✅ Field naming is consistent (all snake_case or all camelCase)
- ✅ Data structure examples provided for Python, TypeScript, and pseudocode

---

## Related Skills

- **Functional Analysis (CLI-001)**: Specifies what data each feature needs/produces
- **Acceptance Criteria (PA-001)**: Tests verify Task entity fields are created/stored/retrieved correctly
- **Business Logic Engineer (BLE-001)**: Defines validation rules and constraints for Task fields
- **Edge Case Identification (QA-001)**: Tests verify Task handles edge cases (boundary values, invalid data)

---

## Example: Phase 1 Task Entity Complete Specification

### Task Entity Overview

A **Task** is the core domain object representing a single todo item. Each task has a unique ID, required title, status (pending or completed), and optional due date and priority. Tasks are created by users, optionally assigned deadlines and priority levels, and marked complete when finished. The Task entity is simple, immutable (except status and completion timestamp), and designed for in-memory storage in Phase 1 with forward compatibility for database storage in Phase II+.

### Required Fields

#### Field: id

**Type**: string
**Purpose**: Unique identifier for the task; enables retrieval, update, deletion
**Constraint**: Non-empty, unique across all tasks in current session, immutable
**Format**: Sequential string "task-001", "task-002", "task-003", etc.
**Generated**: Yes (system generates next sequential ID)
**Example**: "task-001"
**Nullable**: No
**Phase 1**: Mandatory

**Rationale**:
- Every task needs a unique identifier to be referenced and retrieved
- Sequential format is human-readable and verifiable (task-1, task-2, etc.)
- Alternative: UUID (too complex for Phase 1 console app)
- Alternative: Timestamp-based ID (not user-friendly, harder to debug)

---

#### Field: title

**Type**: string (text)
**Purpose**: Human-readable description of what the task is; what the user needs to do
**Constraint**: Required, non-empty, max 255 characters, trimmed
**Validation**:
  1. Must not be null or undefined
  2. Must not be empty string ""
  3. Must not be whitespace-only "   "
  4. After trimming, must be between 1-255 characters
  5. Leading/trailing whitespace auto-trimmed
**Error Messages**:
  - "✗ Error: Task title cannot be empty"
  - "✗ Error: Task title too long (300 chars). Max: 255"
**Example**: "Buy groceries"
**Nullable**: No
**Phase 1**: Mandatory

**Rationale**:
- Core of a todo task is the title; without it, task is meaningless
- 255 char limit is standard for short text fields (adequate for task titles)
- Trimming prevents whitespace-only garbage data
- Validation at creation time prevents corrupted data in list

---

#### Field: status

**Type**: enum (string)
**Allowed Values**: "pending", "completed"
**Purpose**: Track whether task is done; enables filtering (show pending, hide completed)
**Constraint**: Must be one of exactly two values
**Default**: "pending" (all new tasks start pending)
**Mutable**: Yes (user can mark complete, or revert completion)
**Validation**:
  1. Must be exactly "pending" or "completed" (case-sensitive)
  2. No other values allowed
  3. If not provided at creation, defaults to "pending"
**Error Message**: "✗ Error: Invalid status. Allowed: pending, completed"
**Example**: "pending"
**Nullable**: No
**Phase 1**: Mandatory

**Rationale**:
- Binary state (done or not done) covers Phase 1 needs
- "pending" term is clear: task is waiting to be done
- "completed" term is clear: task is done
- Alternative: using "active"/"inactive" (less intuitive)
- Phase II+ can add more states (e.g., "in_progress", "blocked", "cancelled")

---

#### Field: created_timestamp

**Type**: datetime (ISO 8601 format, UTC)
**Purpose**: Record when task was created; enables sorting by creation date, debugging, archiving
**Constraint**: Immutable (set once at creation, never changes)
**Format**: "YYYY-MM-DDTHH:MM:SSZ" (2025-12-30T10:30:45Z)
**Set By**: System (automatically set to current time at creation)
**Timezone**: UTC (Z = Zulu = UTC)
**Example**: "2025-12-30T10:30:45Z"
**Nullable**: No
**Phase 1**: Mandatory

**Rationale**:
- ISO 8601 format is standard, portable across languages and systems
- UTC removes timezone ambiguity (all times comparable globally)
- Immutable: creation time never changes (important for data integrity)
- Used for sorting, reporting, and audit trails
- Alternative: Unix timestamp (less human-readable, timezone issues)

---

### Optional Fields

#### Field: due_date

**Type**: date (ISO 8601 format)
**Purpose**: Deadline for task completion; enables deadline-driven prioritization, reminders
**Constraint**: Optional, valid date if provided, can be past or future
**Format**: "YYYY-MM-DD" (2026-01-15)
**Default**: null (no due date)
**Set By**: User (optional at creation, can be updated)
**Mutable**: Yes (user can change due date)
**Validation**:
  1. If not provided, value is null (OK)
  2. If provided, must be valid date (not Feb 30, etc.)
  3. Must be parseable as "YYYY-MM-DD"
  4. Can be past date (e.g., "2020-01-01") — allowed
  5. Can be future date (e.g., "2099-12-31") — allowed
**Error Messages**:
  - "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"
  - "✗ Error: Invalid date. February has only 28 days in 2026"
**Example**: "2026-01-15"
**Nullable**: Yes
**Phase 1**: Nice-to-have (support creation with due date, but not required)
**Phase II+**: Important (web calendar integration, deadline reminders)

**Rationale**:
- Users often think in terms of deadlines; enables deadline-driven todo lists
- ISO format YYYY-MM-DD is unambiguous (avoids MM/DD vs DD/MM confusion)
- No time component (only date) because tasks are daily, not hourly
- Can be past or future (users track both overdue and future tasks)
- Optional: Phase 1 MVP works without due dates (basic filtering still works)

---

#### Field: priority

**Type**: enum (string)
**Allowed Values**: "low", "normal", "high"
**Purpose**: Indicate task importance; enables prioritization and filtered display
**Constraint**: Optional, must be one of three values if provided
**Default**: "normal" (medium priority)
**Set By**: User (optional at creation, can be updated)
**Mutable**: Yes (user can change priority)
**Validation**:
  1. If not provided, defaults to "normal"
  2. If provided, must be exactly "low", "normal", or "high"
  3. No other values allowed
**Error Message**: "✗ Error: Invalid priority. Allowed: low, normal, high"
**Example**: "high"
**Nullable**: No (defaults to "normal" if null)
**Phase 1**: Nice-to-have (support creation with priority, but not required)
**Phase II+**: Important (visual UI indicators, sorting options)

**Rationale**:
- Three-level system (low/normal/high) is cognitively simple
- Users can quickly categorize tasks: "Is this important or not?"
- Alternative: 5-level (1-5) or numeric scale — too granular, not needed
- Alternative: Eisenhower matrix (urgent/important) — too complex for Phase 1
- Default "normal" means users who don't set priority get sorted uniformly
- Phase II can add visual indicators (colors, icons) for priorities

---

#### Field: completed_timestamp

**Type**: datetime (ISO 8601 format, UTC)
**Purpose**: Record when task was marked complete; enables completion analytics, time tracking
**Constraint**: Optional, immutable after set
**Format**: "YYYY-MM-DDTHH:MM:SSZ" (2025-12-31T15:22:10Z)
**Default**: null (task not yet completed)
**Set By**: System (automatically set when status changes to "completed")
**Mutable**: No (immutable once set; changing status back to pending does NOT clear this)
**Validation**:
  1. If task status is "pending", completed_timestamp is null
  2. If task status is "completed", completed_timestamp should be set (not null)
  3. If explicitly null, system can auto-populate (or leave null for Phase 1)
**Example**: "2025-12-31T15:22:10Z"
**Nullable**: Yes (null if task not completed)
**Phase 1**: Nice-to-have (auto-populate when marking complete, but not critical)
**Phase II+**: Important (completion analytics, time tracking, reporting)

**Rationale**:
- Tracks how long task took (completed_timestamp - created_timestamp = time to complete)
- Immutable: once set, never changes (prevents tampering with history)
- Useful for analytics: "How long do tasks typically take?"
- Not strictly required for Phase 1 MVP, but simple to implement
- Phase II: use for productivity metrics and insights

---

### Field Validation Rules (Summary Table)

| Field | Required? | Type | Validation | Error Handling |
|-------|-----------|------|-----------|-----------------|
| id | Yes | string | Unique, sequential, immutable | Cannot change/delete duplicate IDs |
| title | Yes | string | 1-255 chars, non-empty, trimmed | Reject empty/whitespace, reject >255 |
| status | Yes | enum | "pending" \| "completed", default "pending" | Reject invalid values, default on missing |
| created_timestamp | Yes | datetime | ISO 8601 UTC, immutable | Auto-generate at creation, never change |
| due_date | No | date | YYYY-MM-DD, valid date, can be past/future | Reject invalid format, allow null |
| priority | No | enum | "low" \| "normal" \| "high", default "normal" | Reject invalid values, default on missing |
| completed_timestamp | No | datetime | ISO 8601 UTC, immutable after set | Auto-populate on completion, leave null if pending |

---

### In-Memory Data Structure (Python Example)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration (done or not)"""
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(Enum):
    """Task priority enumeration (importance level)"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

@dataclass
class Task:
    """
    Task domain object for Phase 1 in-memory todo application.

    Represents a single todo item with title, status, optional deadline and priority.
    Immutable after creation (except status and completed_timestamp).
    """

    # Required fields
    id: str                                      # "task-001", "task-002", etc.
    title: str                                   # "Buy groceries", "Submit report", etc.
    status: TaskStatus = TaskStatus.PENDING      # Default: pending
    created_timestamp: datetime = field(        # System time at creation
        default_factory=datetime.utcnow
    )

    # Optional fields
    due_date: Optional[str] = None               # "2026-01-15" or None
    priority: TaskPriority = TaskPriority.NORMAL # Default: normal
    completed_timestamp: Optional[datetime] = None  # When marked complete, or None

    def __post_init__(self):
        """Validate task after initialization"""
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 255:
            raise ValueError(f"Task title too long ({len(self.title)} chars). Max: 255")

        # Auto-trim title
        self.title = self.title.strip()

        # Validate due_date if provided
        if self.due_date:
            try:
                datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got '{self.due_date}'")

        # Validate status
        if self.status not in [TaskStatus.PENDING, TaskStatus.COMPLETED]:
            raise ValueError("Invalid status. Allowed: pending, completed")

    def mark_complete(self):
        """Mark task as completed and set completion timestamp"""
        self.status = TaskStatus.COMPLETED
        self.completed_timestamp = datetime.utcnow()

    def mark_pending(self):
        """Revert task back to pending (clears completed_timestamp)"""
        self.status = TaskStatus.PENDING
        # Note: Does NOT clear completed_timestamp (immutable history)

    def to_dict(self) -> dict:
        """Convert task to dictionary for display/serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,  # Enum to string
            "created_timestamp": self.created_timestamp.isoformat() + "Z",
            "due_date": self.due_date,
            "priority": self.priority.value,  # Enum to string
            "completed_timestamp": (
                self.completed_timestamp.isoformat() + "Z"
                if self.completed_timestamp else None
            ),
        }
```

---

### In-Memory Collection Structure

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class TaskList:
    """
    In-memory container for all tasks.
    Maintains primary list and optional indexes for performance.
    """

    # Primary storage: ordered list of tasks
    tasks: List[Task] = field(default_factory=list)

    # Secondary indexes (optional, for O(1) lookup)
    _id_map: Dict[str, Task] = field(default_factory=dict)  # id -> Task
    _next_id_counter: int = 0  # Counter for generating next sequential ID

    def add_task(self, task: Task) -> Task:
        """Add task to list, maintain indexes"""
        self.tasks.append(task)
        self._id_map[task.id] = task
        return task

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID (O(1) with index)"""
        return self._id_map.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """Delete task by ID, return True if deleted"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        del self._id_map[task_id]
        return True

    def get_next_task_id(self) -> str:
        """Generate next sequential task ID"""
        self._next_id_counter += 1
        return f"task-{self._next_id_counter:03d}"  # task-001, task-002, etc.

    def list_tasks(self) -> List[Task]:
        """Return all tasks in insertion order"""
        return self.tasks.copy()

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        """Return tasks filtered by status (O(n))"""
        return [t for t in self.tasks if t.status == status]

    def filter_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Return tasks filtered by priority (O(n))"""
        return [t for t in self.tasks if t.priority == priority]
```

---

### Phase Compatibility Matrix

| Field | Phase 1 | Phase II | Phase III | Phase IV | Phase V | Notes |
|-------|---------|----------|-----------|----------|---------|-------|
| id | Required | Required | Required | Required | Required | Immutable, forever unique |
| title | Required | Required | Required | Required | Required | Immutable, core identity |
| status | Required | Required | Required | Required | Required | May add more states in Phase III (e.g., "in_progress", "blocked") |
| created_timestamp | Required | Required | Required | Required | Required | Immutable, audit trail |
| due_date | Optional | Required | Required | Required | Required | Important for calendar/scheduling |
| priority | Optional | Required | Required | Required | Required | Important for UI sorting |
| completed_timestamp | Optional | Required | Required | Required | Required | Important for analytics |
| user_id | Not included | Required | Required | Required | Required | Phase II adds multi-user support |
| description | Not included | Optional | Optional | Optional | Optional | Phase II adds richer task details |
| tags | Not included | Optional | Optional | Optional | Optional | Phase II adds categorization |
| assigned_to | Not included | Optional | Optional | Optional | Optional | Phase II adds collaboration |
| recurrence_rule | Not included | Not included | Optional | Optional | Optional | Phase III+ for recurring tasks |
| ai_metadata | Not included | Not included | Optional | Optional | Optional | Phase III for AI suggestions |

**Migration Strategy**:
- Phase 1 → Phase II: Add user_id field; existing tasks get user_id=null or user_id="system"
- Phase II → Phase III: Add ai_metadata field; existing tasks get ai_metadata=null
- All new fields default to null (backward compatible)
- Never remove fields (only deprecate if truly obsolete)

---

### Design Trade-Offs & Rationale

**Decision 1: Sequential IDs vs. UUIDs**
- **Chosen**: Sequential string IDs ("task-001", "task-002")
- **Rationale**: Human-readable, easy to debug, sufficient for Phase 1
- **Trade-off**: Not globally unique across sessions; fine for in-memory Phase 1
- **Phase II**: Could migrate to UUID if multi-user/distributed system needed

**Decision 2: Enum Status vs. Numeric Status**
- **Chosen**: String enum ("pending", "completed")
- **Rationale**: Human-readable, no ambiguity about meaning
- **Trade-off**: Slightly more memory than numeric (0, 1); negligible for Phase 1
- **Alternative Rejected**: Numeric (0=pending, 1=completed) — harder to debug, more error-prone

**Decision 3: ISO 8601 Timestamps vs. Unix Epoch**
- **Chosen**: ISO 8601 ("2025-12-30T10:30:45Z")
- **Rationale**: Human-readable, portable across systems, no timezone ambiguity (UTC)
- **Trade-off**: Slightly larger string representation
- **Alternative Rejected**: Unix epoch (1735555045) — not human-readable, requires conversion

**Decision 4: Flat Task Entity vs. Nested Objects**
- **Chosen**: Flat (no nested objects)
- **Rationale**: Simple, easy to serialize/deserialize, no circular references
- **Trade-off**: Cannot embed User or Category objects; use IDs instead
- **Example**: Task has user_id (string), not user (object) in Phase II

**Decision 5: Single Status Field vs. Boolean Flags**
- **Chosen**: Single status enum
- **Rationale**: One source of truth; prevents conflicting states
- **Alternative Rejected**: is_completed (boolean) + is_pending (boolean) — can have conflicting values

---

### Success Criteria for Task Entity

- ✅ All Phase 1 features (create, list, delete, mark complete, filter, search) can be implemented with these fields
- ✅ All required fields have validation rules
- ✅ All optional fields have sensible defaults
- ✅ Data model is simple enough for in-memory storage (no complex objects)
- ✅ Data types are portable (not Python-specific; works with TypeScript, Go, etc.)
- ✅ Backward compatible: Phase 1 tasks can be read in Phase II with new user_id field
- ✅ Forward compatible: Phase II additions don't break Phase 1 code reading old tasks
- ✅ Timestamps use ISO 8601 UTC (portable, standard)
- ✅ No circular references or complex nesting
- ✅ Field naming is consistent (all snake_case)

---

### Summary

The Task entity is the core domain object for Phase 1. It includes four required fields (id, title, status, created_timestamp) and three optional fields (due_date, priority, completed_timestamp). All fields are defined with specific data types, validation rules, and examples. The model is simple enough for in-memory Python implementation but forward-compatible with Phase II database schema, Phase III AI metadata, and Phase IV/V cloud/Kubernetes requirements. Design prioritizes clarity and simplicity over premature optimization.

