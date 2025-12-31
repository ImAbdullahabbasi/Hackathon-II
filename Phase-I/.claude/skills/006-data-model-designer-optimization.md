# Skill: Data Model Optimization and Normalization

**Skill ID**: DMD-002
**Agent Owner**: data-model-designer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Optimize and normalize the Task entity data model to eliminate redundancy, separate concerns, and ensure extensibility without over-engineering. This skill applies database normalization principles and domain-driven design patterns to keep the model simple, maintainable, and future-proof. Optimization focuses on priority handling, category/tag structures, and recurrence metadata while maintaining Phase 1 simplicity and Phase II+ extensibility.

---

## When to Use

- **Data model refinement**: After initial Task entity design (DMD-001) is complete
- **Feature expansion planning**: When adding priority-based filtering, categories, or recurring tasks
- **Denormalization trade-offs**: Deciding what data should be duplicated for performance vs. normalized for consistency
- **Extension design**: Planning how new features fit into the existing model without bloating the core Task entity
- **Storage optimization**: Reducing memory footprint for Phase 1 in-memory implementation
- **API contract design**: Ensuring JSON serialization is clean and efficient

---

## Inputs

1. **Current Task entity** (document): From DMD-001, the initial Task entity design
2. **Feature requirements** (list): Requirements for priorities, categories, recurrence, filtering
3. **Storage constraints** (text): Phase 1 in-memory storage limitations
4. **Phase II+ vision** (optional): Forward compatibility requirements for web app, database, cloud

---

## Step-by-Step Process

### Step 1: Identify Redundancy in Current Model
Review the current Task entity to find duplicated, derived, or unnecessary data.

**Redundancy Analysis**:

```
Current Task Entity Fields:
├── id (unique identifier)
├── title (task description)
├── status (pending or completed)
├── created_timestamp (immutable creation time)
├── completed_timestamp (when marked complete)
├── due_date (optional deadline)
├── priority (low, normal, high)
└── [future: tags, category, recurrence]

Redundancy Check:
✓ id — Essential (unique identifier)
✓ title — Essential (what is task?)
✓ status — Essential (is it done?)
✓ created_timestamp — Essential (audit trail)
? completed_timestamp — Derived from status (can be inferred)
  → ISSUE: If status=completed, we know task is done
  → VALUE: Records WHEN it was completed (time-tracking, analytics)
  → DECISION: Keep (not truly redundant; adds value)

✓ due_date — Essential (when should it be done?)
✓ priority — Essential (importance level)
? priority — Enum (low, normal, high) vs. Numeric (1-3)
  → ISSUE: Different representations of same concept
  → DECISION: Normalize to single representation (enum string)

? tags/categories — Future field; defer to Phase II
  → ISSUE: Task will accumulate fields for Phase II+
  → DECISION: Extract to separate Category entity; Task references by ID
```

### Step 2: Analyze Concern Separation
Identify where Task entity conflates multiple concerns; separate into focused entities.

**Concern Separation Analysis**:

```
Current Model (Monolithic):
  Task {
    id, title, status, ...
    priority,           ← Concern 1: Task state/management
    due_date,           ← Concern 2: Scheduling
    tags,               ← Concern 3: Organization/categorization
    recurrence_rule,    ← Concern 4: Scheduling pattern
    description,        ← Concern 5: Details/documentation
  }

Problem:
  - Task is doing too much
  - Priority is behavior (how important) vs. metadata (what importance level)
  - Tags are organizational concern, not task concern
  - Recurrence is scheduling rule, not task state
  - Description is optional detail that clutters core entity

Separation Strategy:

Task (Core Entity)
  ├── id, title, status
  ├── created_timestamp, completed_timestamp
  └── due_date (pure scheduling need)

Priority (Separate Enum / Value Object)
  └── (low, normal, high) — embedded in Task as enum, not separate entity

Category (Separate Entity) — Phase II+
  ├── id, name, color
  └── tasks: Task[]

Tags (Separate Entity) — Phase II+
  ├── name
  └── tasks: Task[]

Recurrence (Separate Value Object) — Phase II+
  ├── pattern (daily, weekly, monthly)
  ├── interval (every N days)
  ├── end_date (optional)
  └── next_occurrence (computed)
```

### Step 3: Design Optimized Core Task Entity (Phase 1)
Create a lean, focused Task entity that covers Phase 1 without forward bloat.

**Phase 1 Optimized Task**:

```
Task {
  // Identity
  id: string,                        // "task-001"

  // Core Content
  title: string,                     // "Buy groceries"

  // State Management
  status: TaskStatus,                // "pending" | "completed"
  created_timestamp: datetime,       // When created
  completed_timestamp: datetime?,    // When marked complete

  // Scheduling
  due_date: date?,                   // "2026-01-15"

  // Priority (embedded as enum, not reference)
  priority: TaskPriority,            // "low" | "normal" | "high"
}
```

**Design Rationale**:
- ✅ Minimal fields for Phase 1 features
- ✅ No forward-looking fields cluttering the model
- ✅ Priority is simple enum (not reference to Priority entity)
- ✅ No tags, categories, or recurrence in Phase 1 (defer to Phase II)
- ✅ No description field (Phase II+ feature)

### Step 4: Design Priority Handling (Normalized)
Define priority as a clean value object or enum, not a duplicated or conflated concept.

**Priority Design Pattern**:

#### Option A: Embedded Enum (Chosen for Phase 1)

```
Priority Enum:
  LOW = "low"       // Nice-to-have, non-urgent tasks
  NORMAL = "normal" // Standard tasks, default priority
  HIGH = "high"     // Important, urgent tasks

Task Structure:
  priority: Priority = Priority.NORMAL

Example Task:
  {
    id: "task-001",
    title: "Buy milk",
    priority: "normal"  // Enum value stored as string
  }

Pros:
  + Simple, zero overhead
  + Easy to filter/sort
  + No separate storage needed
  + Backward compatible

Cons:
  - Cannot add new priorities without code change (Phase II: use separate Priority entity if needed)
  - No metadata about priority (e.g., icon, color)
```

#### Option B: Reference to Priority Entity (Phase II+)

```
Priority Entity:
  {
    id: string,           // "priority-1"
    name: string,         // "high"
    level: integer,       // 3 (for sorting)
    color: string?,       // "#FF0000"
    icon: string?         // "exclamation-mark"
  }

Task Structure:
  priority_id: string = "priority-2"  // References Priority entity

Example:
  Task {
    id: "task-001",
    title: "Buy milk",
    priority_id: "priority-2"  // Reference, not embedded
  }

Pros:
  + Extensible: add colors, icons, custom priorities
  + Separates concerns: Task doesn't own Priority definition
  + Allows filtering/sorting by priority properties

Cons:
  - Extra lookup/join needed to get priority details
  - More complex data structure
```

**Chosen for Phase 1**: Option A (Embedded Enum)
- Rationale: Simple, no overhead, sufficient for MVP
- Phase II Migration: If custom priorities needed, add Priority entity and change priority to priority_id reference
- No breaking change: existing tasks can get mapped to default priorities

### Step 5: Design Category/Tag Handling (Normalized)
Separate tags and categories from Task entity; use relationship-based design.

**Category/Tags Design (Phase II+, Not Phase 1)**:

```
PHASE 1 (Current):
  No categories or tags in Task entity
  Rationale: MVP doesn't need fine-grained categorization
  Storage: ~300 bytes per task (7 fields)

PHASE II (Web App):
  Add categorization support without bloating Task

Option A: Tags as separate Entity with Many-to-Many relationship
  Tag Entity:
    id: string           // "tag-1"
    name: string         // "shopping"
    color: string?       // "#FF5733"

  Task-Tag Relationship:
    task_id: string      // "task-001"
    tag_id: string       // "tag-1"

  Query: "Get all tasks with tag 'shopping'"
    SELECT tasks FROM task_tags WHERE tag_id="tag-1"

  Task Serialization (when needed):
    {
      id: "task-001",
      title: "Buy milk",
      tags: [
        { id: "tag-1", name: "shopping" },
        { id: "tag-2", name: "urgent" }
      ]
    }

Pros:
  + Tags shared across tasks (normalized)
  + Reduce redundancy (tag "shopping" stored once)
  + Efficient filtering (index on tag_id)

Cons:
  - Extra lookups/joins needed
  - More complex queries

Option B: Tags as embedded Array (Denormalized)
  Task Entity:
    id: string
    title: string
    tags: string[]       // ["shopping", "urgent"]

  Pros:
    + Simple, no extra queries
    + Task is self-contained
  Cons:
    - Tag "shopping" appears in every task (redundancy)
    - Renaming tag requires updating all tasks
    - Filtering requires scanning all tasks

Chosen for Phase II: Option A (Separate Entity)
  Rationale: Normalizes redundancy; better for multi-user web app
  Phase 1 Note: Not implemented; deferring to Phase II
```

### Step 6: Design Recurrence Handling (Normalized)
Create a recurrence rule structure that keeps Task simple while supporting recurring task patterns.

**Recurrence Design (Phase III+, Not Phase 1)**:

```
PHASE 1:
  No recurrence support
  Rationale: MVP tasks are one-time only
  Storage: Not applicable

PHASE III (Future):
  Add recurring task support (e.g., "Daily standup every weekday")

Recurrence Rule Structure:
  RecurrenceRule {
    pattern: enum           // DAILY, WEEKLY, MONTHLY, YEARLY
    interval: integer       // Every N days/weeks/months (e.g., 2 = every 2 weeks)
    days_of_week: string[]? // ["MON", "WED", "FRI"] for weekly pattern
    end_date: date?         // Recurring until this date (null = forever)
    occurrences: integer?   // Repeat N times (null = forever)
  }

Example Recurring Tasks:
  1. Daily standup:
     {
       pattern: "DAILY",
       interval: 1,         // Every day
       end_date: null       // Forever
     }

  2. Bi-weekly meeting (every other Wednesday):
     {
       pattern: "WEEKLY",
       interval: 2,         // Every 2 weeks
       days_of_week: ["WED"],
       end_date: "2026-12-31"
     }

  3. Monthly rent (1st of month, 12 times):
     {
       pattern: "MONTHLY",
       interval: 1,
       occurrences: 12
     }

Task Relationship to Recurrence:
  Option A: Task has recurrence_rule field (embedded)
    Task {
      id, title, ...,
      recurrence_rule: RecurrenceRule?
    }
    Pro: Simple, self-contained
    Con: Conflates recurring template with task instances

  Option B: Separate RecurringTask entity (normalized)
    RecurringTask {
      id: string,
      title: string,
      recurrence_rule: RecurrenceRule,
      generated_tasks: Task[]  // List of Task instances generated
    }
    Pro: Clean separation; Template vs. Instances
    Con: More complex data structure

  Option C: Hybrid (Chosen for Phase III)
    Task {
      id, title, ...,
      recurring_task_id: string?  // If part of recurring series
    }
    RecurringTask {
      id, title,
      recurrence_rule: RecurrenceRule,
      next_due_date: date        // When next task should be created
    }

    When recurring task "Daily standup" occurs:
    1. Create new Task with title "Daily standup"
    2. Set recurring_task_id reference
    3. Increment RecurringTask.next_due_date

    Pro: Tasks are still independent; can complete/edit without affecting pattern
    Con: Moderate complexity

Chosen for Phase III: Option C (Hybrid)
  Phase 1 Note: Not implemented; deferring to Phase III+ (AI-driven task creation)
```

### Step 7: Design Normalized Data Structure Summary
Create a comprehensive view of normalized data model across phases.

**Normalized Data Model Architecture**:

```
PHASE 1 (In-Memory, Current):
  Task
    ├── id: string
    ├── title: string
    ├── status: enum (pending, completed)
    ├── created_timestamp: datetime
    ├── completed_timestamp: datetime?
    ├── due_date: date?
    └── priority: enum (low, normal, high)

  Relationships: None (single-table design)
  Storage: ~300 bytes per task
  Query Complexity: O(n) scans for filtering
  Normalization: 1NF (flat structure, atomic values)

PHASE II (Web App + Database):
  Task
    ├── id: UUID
    ├── user_id: UUID (foreign key)
    ├── title: string
    ├── status: enum
    ├── created_timestamp: datetime
    ├── completed_timestamp: datetime?
    ├── due_date: date?
    ├── priority_id: UUID (foreign key, if custom priorities)
    └── [future: description, color, position]

  Category
    ├── id: UUID
    ├── user_id: UUID
    ├── name: string
    └── color: string?

  TaskCategory (Many-to-Many)
    ├── task_id: UUID
    └── category_id: UUID

  Tag
    ├── id: UUID
    ├── user_id: UUID
    ├── name: string
    └── color: string?

  TaskTag (Many-to-Many)
    ├── task_id: UUID
    └── tag_id: UUID

  Priority (Optional, if custom priorities)
    ├── id: UUID
    ├── user_id: UUID
    ├── name: string
    ├── level: integer
    ├── color: string?
    └── icon: string?

  Relationships:
    - Task belongs to User (1:N)
    - Task belongs to Category (M:N via TaskCategory)
    - Task has Tags (M:N via TaskTag)
    - Task references Priority (N:1, if custom priorities)

  Storage: ~500 bytes per task (plus foreign keys)
  Query Complexity: O(1) with indexes/joins
  Normalization: 3NF (normalized, no transitive dependencies)

PHASE III (AI Chatbot):
  [Phase II entities continue]

  RecurringTask
    ├── id: UUID
    ├── user_id: UUID
    ├── title: string
    ├── recurrence_rule: JSON (pattern, interval, days, end_date)
    ├── next_occurrence: date
    └── created_timestamp: datetime

  Task
    └── [Add field] recurring_task_id: UUID? (foreign key)

  Relationships:
    - RecurringTask belongs to User (1:N)
    - Task references RecurringTask (N:1, if recurring)
```

### Step 8: Design Serialization (JSON Output)
Define how normalized entities are serialized when returned to users.

**Serialization Examples**:

```
PHASE 1 Task Serialization (Simple):
  {
    "id": "task-001",
    "title": "Buy groceries",
    "status": "pending",
    "created_timestamp": "2025-12-30T10:30:45Z",
    "completed_timestamp": null,
    "due_date": "2026-01-15",
    "priority": "normal"
  }

PHASE II Task Serialization (Web API, with Categories):
  {
    "id": "abc-123-def",
    "user_id": "user-456",
    "title": "Buy groceries",
    "status": "pending",
    "created_timestamp": "2025-12-30T10:30:45Z",
    "completed_timestamp": null,
    "due_date": "2026-01-15",
    "priority": {
      "id": "priority-1",
      "name": "normal",
      "level": 2,
      "color": "#FFC107"
    },
    "categories": [
      { "id": "cat-1", "name": "shopping", "color": "#FF5733" }
    ],
    "tags": [
      { "id": "tag-1", "name": "grocery" },
      { "id": "tag-2", "name": "urgent" }
    ],
    "description": "Milk, bread, cheese, eggs"
  }

Serialization Strategy:
  - Core Task fields always included
  - Referenced entities (Priority, Category, Tag) can be:
    A) Included inline (convenience, but risks over-fetching)
    B) Returned as IDs only (lean, but requires extra queries)
    C) Configurable via ?expand=priority,categories query parameter (best practice)

Chosen for Phase II: Option C (Expandable fields)
  Example: GET /api/tasks/abc-123?expand=priority,categories
  Response includes full Priority and Category objects inline
  Without ?expand, response includes only IDs
```

### Step 9: Validate Normalization
Ensure the optimized model is properly normalized without premature optimization.

**Normalization Validation Checklist**:

```
Atomicity (1NF):
  ✅ Every field contains atomic value (not arrays/objects in Phase 1)
  ✅ No repeating groups (tags deferred to Phase II)
  ✅ Each row represents single task

Functional Dependency (2NF):
  ✅ All non-key attributes dependent on entire primary key (id)
  ✅ No partial dependencies (all fields depend on id)

Transitive Dependency (3NF):
  ⚠️ Phase 1: Not applicable (no foreign keys, single-table)
  ✅ Phase II: No non-key field depends on non-key field
    Example: Task.priority doesn't depend on Task.due_date

Redundancy:
  ✅ No duplicate data within Task (each field represents single concept)
  ✅ No derived fields (completed_timestamp is not derived from status)
  ✅ No calculated fields without explicit storage reason

BCNF (Boyce-Codd Normal Form):
  ⚠️ Phase 1: Not applicable (simple structure)
  ✅ Phase II: Every determinant is a candidate key
    Example: user_id determines which tasks user owns; user_id is foreign key

Denormalization Justified?
  ✅ Phase 1: No denormalization; all fields are atomic
  ✅ Phase II: Minimal denormalization
    - Task includes priority enum (could reference Priority entity)
    - Justification: Performance (avoid extra lookups for simple enum)
```

---

## Output

**Format**: Structured Markdown document with optimized data model design:

```markdown
# Data Model Optimization and Normalization

## Executive Summary
[One paragraph: what was optimized, how, and why]

## Redundancy Analysis
[What redundancy was identified and eliminated]

## Concern Separation
[How was the monolithic Task entity decomposed]

## Phase 1 Optimized Core Task Entity
[Lean Task design with minimal fields]

## Priority Handling (Normalized)
[How priority is designed and why]

## Category/Tag Design (Phase II+)
[How tags/categories are separated from Task]

## Recurrence Design (Phase III+)
[How recurring tasks are handled without bloating core Task]

## Normalization Validation
[Checklist confirming proper normalization]

## Design Trade-Offs and Rationale
[Decisions made and alternatives rejected]

## Data Model Across Phases
[How model evolves from Phase 1 to Phase V]

## Performance Considerations
[Storage, query complexity, indexing strategy]

## Success Criteria
[Checklist for validation]
```

---

## Failure Handling

### Scenario 1: Over-Normalization (Too Many Entities)
**Symptom**: Created separate Priority, Category, Tag entities for Phase 1 (premature)
**Resolution**:
- Revert to simple enums for Phase 1 (priority, status as enums)
- Document Plan to extract to entities in Phase II when complexity justifies it
- Keep Phase 1 implementation simple; avoid premature optimization
- Example: Priority as enum "normal", not separate Priority entity

### Scenario 2: Under-Normalization (Bloated Entity)
**Symptom**: Task entity has 20+ fields including future Phase II/III features
**Resolution**:
- Remove fields not used in Phase 1 (description, tags, recurrence_rule)
- Create forward-compatibility document: "Phase II will add these fields"
- Keep Phase 1 Task focused on current features only
- Example: Remove description field; add in Phase II when text editor UI ready

### Scenario 3: Redundant Data Storage
**Symptom**: Task stores both completed_timestamp AND has inferred from status field
**Resolution**:
- Document decision: completed_timestamp is NOT redundant (adds analytic value)
- Clarify: status=completed doesn't tell WHEN completion happened
- If truly redundant, remove one field and update spec
- Example: If only completion date matters (not time), use date field, not datetime

### Scenario 4: Conflated Concerns
**Symptom**: Task.priority mixes "importance level" (low/normal/high) with "urgency" (today/this week/later)
**Resolution**:
- Separate concepts: priority = importance, due_date = urgency
- Remove ambiguous fields
- Example: Use priority for importance ranking, due_date for urgency
- Update business logic to use both fields meaningfully

### Scenario 5: Phase II Incompatibility
**Symptom**: Optimized Phase 1 model cannot accommodate multi-user requirements
**Resolution**:
- Add user_id field to Task now (set to null/default in Phase 1)
- Plan migration: Phase 1 tasks get user_id="system" when upgraded
- Ensure Phase II can read Phase 1 tasks without breaking
- Test backward compatibility

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Data model refinement**: Apply same analysis to any domain entity
- **Feature expansion**: When adding new features, use concern separation pattern
- **Schema evolution**: When upgrading storage (memory → database), use normalized design
- **Performance tuning**: Use denormalization decisions to optimize critical queries
- **API design**: Use normalized entities to design clean API contracts
- **Database design**: Convert normalized model to SQL schema

---

## Success Metrics

- ✅ Core Task entity has ≤7 fields (lean, focused)
- ✅ All fields in Task are used by at least one Phase 1 feature
- ✅ No redundant or derived data in Phase 1 Task
- ✅ Priority handled as simple enum, not complex object (Phase 1)
- ✅ Tags/categories deferred to Phase II+ (not in Phase 1)
- ✅ Recurrence deferred to Phase III+ (not in Phase 1)
- ✅ Model is 1NF (Phase 1) and plans for 3NF (Phase II)
- ✅ Forward compatible: Phase II can add fields without breaking Phase 1
- ✅ Backward compatible: Phase II can read Phase 1 data
- ✅ Timestamps use ISO 8601 UTC (portable)
- ✅ No circular references or complex nesting

---

## Related Skills

- **Data Model Designer (DMD-001)**: Initial Task entity design
- **Functional Analysis (CLI-001)**: Specifies what data features need
- **Business Logic Engineer (BLE-001)**: Defines business rules that shape data model
- **Quality Assurance (QA-001)**: Tests that normalized model handles edge cases

---

## Example: Phase 1 Optimized Task Entity

### Current Task Entity (From DMD-001)

```python
@dataclass
class Task:
    id: str
    title: str
    status: TaskStatus = TaskStatus.PENDING
    created_timestamp: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    completed_timestamp: Optional[datetime] = None
```

### Analysis: Is This Already Optimized?

**Redundancy Check**:
- ✅ id: Essential (unique identifier)
- ✅ title: Essential (what is task?)
- ✅ status: Essential (pending or done?)
- ✅ created_timestamp: Essential (audit trail)
- ✅ completed_timestamp: NOT redundant (when was it completed?)
- ✅ due_date: Essential (when should it be done?)
- ✅ priority: Essential (how important?)

**Conclusion**: Current Task entity is already well-optimized for Phase 1.
- No redundant fields
- All 7 fields serve distinct purpose
- Simple, flat structure (1NF)
- Ready for implementation

### Optimization Decision: No Further Changes for Phase 1

**Rationale**:
- Task entity is already minimal and focused
- All fields are necessary for Phase 1 features
- Further optimization would premature (add complexity without benefit)
- Model is forward-compatible with Phase II additions

### Phase II Planned Extensions (NOT in Phase 1)

```python
# Phase II: Add these fields to support web app features
@dataclass
class Task:
    # ... Phase 1 fields ...

    # Phase II additions
    user_id: Optional[str] = None           # Multi-user support
    description: Optional[str] = None       # Extended task details
    category_ids: List[str] = field(default_factory=list)  # Categorization
    tag_ids: List[str] = field(default_factory=list)       # Tags/labels
    color: Optional[str] = None             # Visual customization
    position: Optional[int] = None          # Custom ordering
```

**Migration Strategy**:
- All new fields are optional
- Phase 1 tasks have new fields set to null/empty
- No breaking changes to Phase 1 data
- Phase II code handles null values gracefully

### Priority Handling: Why Enum is Optimal for Phase 1

**Chosen Design** (Embedded Enum):
```python
class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

@dataclass
class Task:
    priority: TaskPriority = TaskPriority.NORMAL
```

**Why This is Optimal**:
- ✅ Simple: No extra table or ID mapping
- ✅ Fast: No lookup required
- ✅ Clear: Meaning is immediate (no magic numbers)
- ✅ Extensible: Phase II can change to Priority entity if custom priorities needed

**Example Task**:
```json
{
  "id": "task-001",
  "title": "Buy groceries",
  "priority": "normal",
  "status": "pending",
  "due_date": "2026-01-15",
  "created_timestamp": "2025-12-30T10:30:45Z",
  "completed_timestamp": null
}
```

**Phase II Migration** (If custom priorities needed):
```python
# Phase II: Change priority to reference
@dataclass
class Task:
    priority_id: str = "priority-2"  # Reference to Priority entity

# New Phase II entity
@dataclass
class Priority:
    id: str
    name: str
    level: int
    color: str
    icon: str
```

No breaking change to Phase 1 data; just reinterpret priority field as priority_id.

### Category/Tags: Why Deferred to Phase II

**Phase 1 Decision**: No tags or categories in Task entity

**Rationale**:
- Not needed for Phase 1 MVP (Phase 1 focuses on basic CRUD)
- Categories require UI (select dropdowns, color pickers) not available in CLI
- Tags require tagging UI not available in console
- Storage overhead: each task would store category/tag IDs (bloats model)
- Query complexity: filtering by tag requires many-to-many relationship

**Phase II Implementation** (when web UI available):
```
New Entities:
  Category { id, user_id, name, color }
  Tag { id, user_id, name, color }
  TaskCategory { task_id, category_id }  [Many-to-Many]
  TaskTag { task_id, tag_id }             [Many-to-Many]

Task Addition:
  Task { ..., [no tags/categories field] }
  But can query: SELECT * FROM task_tags WHERE task_id = 'task-001'

Serialization (Phase II API):
  {
    "id": "task-001",
    "title": "Buy groceries",
    ...
    "categories": [
      { "id": "cat-1", "name": "shopping" }
    ],
    "tags": [
      { "id": "tag-1", "name": "urgent" },
      { "id": "tag-2", "name": "grocery" }
    ]
  }
```

### Recurrence: Why Deferred to Phase III

**Phase 1 Decision**: No recurrence support in Task entity

**Rationale**:
- Phase 1 is in-memory console app; no persistence across sessions
- Recurrence requires scheduling system (too complex for Phase 1)
- Users can manually recreate recurring tasks (workaround for MVP)
- Phase III will add AI-driven task generation (perfect for recurring tasks)

**Phase III Implementation** (with AI chatbot):
```
New Entity:
  RecurringTask {
    id, user_id, title,
    recurrence_rule: {
      pattern: "DAILY",
      interval: 1,
      end_date: null
    },
    next_occurrence: "2026-01-01",
    original_task: Task (template)
  }

Task Addition:
  Task { ..., recurring_task_id: "recurring-1" }

Behavior:
  1. RecurringTask "Daily standup" has next_occurrence = "2026-01-01"
  2. At 2026-01-01, system creates new Task with title "Daily standup"
  3. Sets new Task.recurring_task_id = "recurring-1" (links back to template)
  4. Updates RecurringTask.next_occurrence = "2026-01-02"
  5. Repeat daily until end_date or occurrences limit reached
```

### Normalization Summary

**Phase 1 Task Entity Normalization Status**:
- ✅ **1NF** (Atomic Values): All fields are atomic, no arrays/objects
- ✅ **2NF** (No Partial Dependencies): All non-key fields depend on id
- ✅ **3NF** (No Transitive Dependencies): No non-key field depends on non-key field
- ✅ **BCNF** (Simple Structure): Single table, no complex dependencies

**Design Decisions**:
1. **Priority as Enum**: Simple, fast, no overhead. Phase II can change if needed.
2. **Tags/Categories Deferred**: Unnecessary complexity for Phase 1 MVP.
3. **Recurrence Deferred**: Requires scheduling system (Phase III feature).
4. **No Description Field**: Phase II feature when UI for rich text editing available.
5. **All Required Fields**: Every field serves distinct purpose, no redundancy.

**Result**: Optimized Task entity is:
- ✅ Minimal (7 fields, all essential)
- ✅ Normalized (no redundancy, proper dependencies)
- ✅ Simple (no complex nesting, all atomic values)
- ✅ Extensible (forward-compatible with Phase II/III additions)
- ✅ Performant (O(1) memory per task, O(n) list operations acceptable for Phase 1)

---

## Performance Analysis

### Phase 1 (In-Memory)

**Storage Per Task**:
- id: 8 bytes (8 characters + length)
- title: ~30 bytes average (variable)
- status: 1 byte (enum)
- created_timestamp: 20 bytes (ISO string)
- completed_timestamp: 20 bytes (ISO string) or null
- due_date: 10 bytes (ISO date) or null
- priority: 1 byte (enum)

**Total Per Task**: ~90-100 bytes

**Collection of 1,000 Tasks**: ~100 KB (fits easily in memory)

**Query Performance**:
- Get task by ID: O(n) linear scan without index → acceptable for 1,000 items
- Optimization: Optional ID map → O(1) lookup
- Filter by status: O(n) scan → acceptable
- Sort by due_date: O(n log n) → acceptable
- Search by title: O(n) scan → acceptable

**Memory Scalability**:
- 1,000 tasks: ~100 KB
- 10,000 tasks: ~1 MB
- 100,000 tasks: ~10 MB (still fits in typical device memory)

### Phase II (Database)

**Storage Per Task** (PostgreSQL):
- id: UUID (16 bytes)
- user_id: UUID (16 bytes)
- title: VARCHAR(255) (variable)
- status: ENUM (1 byte)
- created_timestamp: TIMESTAMP (8 bytes)
- completed_timestamp: TIMESTAMP NULL (8 bytes)
- due_date: DATE NULL (4 bytes)
- priority: ENUM (1 byte)

**Total Per Task**: ~60 bytes fixed + variable title

**Query Performance** (with indexes):
- Get task by ID: O(1) B-tree index
- Get tasks by user_id: O(log n) + O(k) where k = user's tasks
- Filter by status: O(log n) + O(k) with index on (user_id, status)
- Filter by due_date: O(log n) + O(k) with index on (user_id, due_date)
- Sort by due_date: O(k log k) for user's tasks

**Database Scaling**:
- 1 million tasks: ~60 MB + indexes
- 100 million tasks: ~6 GB (still manageable with proper indexing)

---

## Conclusion

The Phase 1 Task entity is already optimized for the MVP. All 7 fields are essential, no redundancy exists, and the structure is properly normalized (1NF). The design is forward-compatible with Phase II web app additions and Phase III+ advanced features. Priority is handled efficiently as an embedded enum; tags/categories and recurrence are deferred to later phases when complexity justifies the added storage and query overhead.

The key optimization principle applied: **Simplicity for Phase 1, Extensibility for Phases II+**.

