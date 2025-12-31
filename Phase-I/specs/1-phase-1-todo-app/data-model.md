# Data Model: Phase 1 Todo App

**Date**: 2025-12-30
**Feature**: 1-phase-1-todo-app
**Purpose**: Define Task entity schema, validation rules, and storage contracts

---

## Task Entity

### Schema

```
Task
├── id: string (immutable)
│   ├── Format: "task-NNN" (task-001, task-042, etc.)
│   ├── Generated: Automatically on creation
│   └── Constraint: Unique within session
│
├── title: string (immutable after creation)
│   ├── Required: Yes
│   ├── Length: 1-255 characters
│   ├── Constraint: Non-empty, trimmed of whitespace
│   └── Type: UTF-8 encoded
│
├── status: enum (mutable)
│   ├── Values: "pending" | "completed"
│   ├── Default: "pending"
│   ├── Constraint: Valid enum values only
│   └── Transition: pending → completed (one-way in Phase I)
│
├── created_timestamp: datetime (immutable)
│   ├── Value: Set to current time on creation
│   ├── Format: ISO 8601 (datetime.datetime)
│   └── Constraint: Never modified
│
├── completed_timestamp: datetime | null (immutable after set)
│   ├── Value: Set when status changes to "completed"
│   ├── Default: None (null)
│   ├── Format: ISO 8601 (datetime.datetime)
│   └── Constraint: Set only once, never modified
│
├── priority: enum (mutable)
│   ├── Values: "high" | "medium" | "low"
│   ├── Default: "medium"
│   ├── Constraint: Valid enum values only, case-sensitive
│   └── Feature: Phase I (new)
│
├── category: string | null (mutable)
│   ├── Length: 0-50 characters (null if not set)
│   ├── Default: None (null)
│   ├── Constraint: Optional, non-empty string if provided
│   └── Feature: Phase I (new)
│
├── due_date: date | null (mutable)
│   ├── Format: YYYY-MM-DD (datetime.date)
│   ├── Default: None (null)
│   ├── Validation: Valid calendar date, any year
│   ├── Constraint: Past, present, future dates allowed
│   └── Feature: Phase I (new)
│
├── recurrence: enum | null (immutable after creation)
│   ├── Values: "daily" | "weekly" | "monthly" | null
│   ├── Default: None (null)
│   ├── Constraint: Valid enum values only
│   └── Feature: Phase I (new)
│
└── parent_recurrence_id: string | null (immutable)
    ├── Value: ID of original recurring task (if this is auto-generated instance)
    ├── Default: None (null)
    ├── Format: "task-NNN"
    ├── Constraint: Reference to valid task ID
    └── Feature: Phase I (new)
```

### Derived Properties (Computed, not stored)

```
is_overdue: boolean
├── Computation: due_date != null AND due_date < today
├── Used for: Display in CLI, filtering
└── Constraint: Read-only

next_recurrence_date: date | null
├── Computation: Based on recurrence pattern and due_date (if set)
├── Examples:
│   ├── Daily: due_date + 1 day
│   ├── Weekly: due_date + 7 days
│   └── Monthly: due_date + 1 month (month-end handling)
└── Used for: Display in CLI, for information only
```

---

## Enumerations

### Priority

```
enum Priority:
  HIGH = "high"
  MEDIUM = "medium"
  LOW = "low"

Default: MEDIUM
Case sensitivity: EXACT (lowercase in storage)
CLI representation: Uppercase (HIGH, MEDIUM, LOW)
```

### Status

```
enum Status:
  PENDING = "pending"
  COMPLETED = "completed"

Default: PENDING
Case sensitivity: EXACT (lowercase in storage)
CLI representation: Lowercase
```

### Recurrence

```
enum Recurrence:
  DAILY = "daily"
  WEEKLY = "weekly"
  MONTHLY = "monthly"

Default: None (no recurrence)
Case sensitivity: EXACT (lowercase in storage)
CLI representation: Uppercase (DAILY, WEEKLY, MONTHLY)
```

---

## Validation Rules

### Task ID (id)

**Rule**: Format must be "task-NNN" where NNN is zero-padded number
```
Pattern: ^task-\d{3,}$
Examples:
  ✅ task-001
  ✅ task-042
  ✅ task-999
  ✅ task-1000 (can exceed 999)
  ❌ task-01 (insufficient padding)
  ❌ task1 (missing dash)
  ❌ Task-001 (case sensitive)
```

**Generation**: Auto-increment counter
- Start: task-001
- Increment: +1 per new task
- Uniqueness: Guaranteed within session
- Persistence: Counter preserved across task deletions (IDs don't reuse)

---

### Title (title)

**Rule**: Non-empty string, 1-255 characters, UTF-8
```
Validation Steps:
1. Non-null check ✓
2. Length check: 1 ≤ len(title) ≤ 255 ✓
3. Trim leading/trailing whitespace
4. Check not empty after trim
5. Encode as UTF-8 (implicit in Python 3)

Examples:
  ✅ "Buy groceries"
  ✅ "Task with émojis 🎉"
  ✅ "A" (1 char minimum)
  ✅ "Long title..." (255 chars)
  ❌ "" (empty)
  ❌ "   " (whitespace only)
  ❌ Title with 256+ characters
```

**Immutability**: Title cannot be changed after creation

---

### Status (status)

**Rule**: Valid enum value only
```
Validation Steps:
1. Check value in {"pending", "completed"}
2. Case-sensitive comparison

Examples:
  ✅ "pending"
  ✅ "completed"
  ❌ "Pending" (wrong case)
  ❌ "complete" (wrong value)
  ❌ "done"

Transition Rules:
  pending → completed ✅ allowed
  completed → pending ❌ not allowed (Phase I)
  completed → completed ✅ allowed (no-op)
  pending → pending ✅ allowed (no-op)
```

---

### Created Timestamp (created_timestamp)

**Rule**: Set to current datetime on task creation, never modified
```
Format: datetime.datetime (ISO 8601 when serialized)
Example: 2025-12-30 14:30:45.123456

Constraints:
  - Automatic on creation
  - Immutable
  - Always recorded (no null)
  - Used for sorting "created first"
```

---

### Completed Timestamp (completed_timestamp)

**Rule**: Set only when status changes to "completed", never modified
```
Format: datetime.datetime | null (ISO 8601 when serialized)
Example: 2025-12-30 15:45:30.654321

Constraints:
  - Default: None (null)
  - Set only when: status = "completed" AND previously = "pending"
  - Immutable once set
  - Clear on status change back to "pending"? (Not allowed Phase I)

Null Handling:
  ✅ Task with status="pending" has completed_timestamp=None
  ✅ Task with status="completed" has completed_timestamp set
```

---

### Priority (priority)

**Rule**: Valid enum value, defaults to "medium"
```
Validation Steps:
1. If null/not provided: Use default "medium"
2. If provided: Check value in {"high", "medium", "low"}
3. Case-sensitive comparison

Examples:
  ✅ "high"
  ✅ "medium"
  ✅ "low"
  ✅ Not provided (defaults to "medium")
  ❌ "High" (wrong case)
  ❌ "urgent" (not in enum)
  ❌ 1 (wrong type)

CLI Input → Storage Mapping:
  HIGH → "high"
  MEDIUM → "medium"
  LOW → "low"
```

---

### Category (category)

**Rule**: Optional string, max 50 characters, no validation of content
```
Validation Steps:
1. If null/not provided: Store as None
2. If empty string: Accept (equivalent to null)
3. If provided: Check length ≤ 50
4. Allow any characters (including special chars)

Examples:
  ✅ "work"
  ✅ "personal"
  ✅ "home-office"
  ✅ "Project @2025 (urgent!)" (special chars allowed)
  ✅ null / not provided
  ✅ "" (empty string, treated as null)
  ❌ "This category has more than 50 characters and should be rejected now"

Storage:
  - Python: None for null/empty
  - Serialized: null for null, string for values
```

---

### Due Date (due_date)

**Rule**: Optional date in YYYY-MM-DD format, must be valid calendar date
```
Validation Steps:
1. If null/not provided: Store as None
2. If provided: Parse format YYYY-MM-DD
3. Validate calendar date exists (e.g., reject Feb 30)
4. Allow past, present, future dates

Format Validation:
  Pattern: ^\d{4}-\d{2}-\d{2}$
  Examples:
    ✅ "2025-12-31"
    ✅ "2020-01-01" (past)
    ❌ "2025-13-45" (invalid month/day)
    ❌ "2025-02-30" (Feb never has 30 days)
    ❌ "25-12-31" (year must be 4 digits)
    ❌ "2025-1-1" (month/day must be zero-padded)

Calendar Validation:
  Use: datetime.date.fromisoformat() or strptime()
  Examples:
    ✅ "2025-12-31" (Dec has 31 days)
    ✅ "2024-02-29" (2024 is leap year)
    ❌ "2025-02-29" (2025 is not leap year)
    ❌ "2025-04-31" (Apr has 30 days)

Date Range:
  Minimum: Any year (even 1900)
  Maximum: Any year (even 2099)
  No validation against current date (past dates allowed)
```

**Overdue Calculation**:
```
is_overdue = (due_date != null) AND (due_date < today)

Examples (assuming today = 2025-12-30):
  ✅ Due 2025-12-29: OVERDUE
  ❌ Due 2025-12-30: NOT overdue (due today, not yet past)
  ❌ Due 2025-12-31: NOT overdue (due tomorrow)
  ❌ No due date: NOT overdue (null)
```

---

### Recurrence (recurrence)

**Rule**: Optional enum value, immutable after creation
```
Validation Steps:
1. If null/not provided: Store as None
2. If provided: Check value in {"daily", "weekly", "monthly"}
3. Case-sensitive comparison

Examples:
  ✅ "daily"
  ✅ "weekly"
  ✅ "monthly"
  ✅ null / not provided
  ❌ "Daily" (wrong case)
  ❌ "biweekly" (not supported Phase I)
  ❌ "yearly"

Immutability:
  - Set on task creation
  - Cannot be changed after creation
  - To change recurrence, delete and recreate task

CLI Input → Storage Mapping:
  DAILY → "daily"
  WEEKLY → "weekly"
  MONTHLY → "monthly"
```

---

### Parent Recurrence ID (parent_recurrence_id)

**Rule**: Optional reference to parent task, only set for auto-generated instances
```
Format: "task-NNN" (same format as id)
Examples:
  ✅ "task-001" (parent is task-001)
  ✅ null (original task, not auto-generated)

Constraint:
  - Set only for auto-generated instances
  - References valid task ID in storage
  - Immutable
  - No validation loop (no task should reference itself)

Usage:
  - Identify tasks created by recurrence
  - Link instances to original recurring task
  - Preserve history (original task still exists)
```

---

## Backward Compatibility Rules

### Loading Old Tasks (Basic Features Only)

When loading/creating tasks from Basic feature (before intermediate/advanced):

```python
task = Task(
    id="task-001",
    title="Task from basic feature",
    status="pending",
    created_timestamp=datetime.now(),
    completed_timestamp=None,
    # NEW FIELDS - apply defaults
    priority="medium",  # DEFAULT
    category=None,      # DEFAULT
    due_date=None,      # DEFAULT
    recurrence=None,    # DEFAULT
    parent_recurrence_id=None  # DEFAULT
)
```

### Serialization/Deserialization

```python
# When saving to storage:
task_dict = {
    "id": task.id,
    "title": task.title,
    "status": task.status,
    "created_timestamp": task.created_timestamp.isoformat(),
    "completed_timestamp": task.completed_timestamp.isoformat() if task.completed_timestamp else None,
    "priority": task.priority,
    "category": task.category,
    "due_date": task.due_date.isoformat() if task.due_date else None,
    "recurrence": task.recurrence,
    "parent_recurrence_id": task.parent_recurrence_id
}

# When loading from storage:
# All fields present in dict (new tasks) or missing (old tasks)
# Use .get() with defaults for optional fields
priority = data.get("priority", "medium")
category = data.get("category", None)
due_date = data.get("due_date", None)
# etc.
```

---

## Validation Error Messages

### Priority Validation

```
Input: "urgent"
Error: "Invalid priority. Must be 'high', 'medium', or 'low'."

Input: None (required in some contexts)
Error: "Priority must be specified."
```

### Category Validation

```
Input: "This category is way too long and exceeds the 50 character limit we have"
Error: "Category must be 50 characters or less (received 76 characters)."

Input: ""
Info: "Category is optional. Leave empty to skip."
```

### Due Date Validation

```
Input: "2025-13-45"
Error: "Invalid date format. Use YYYY-MM-DD."

Input: "2025-02-30"
Error: "Invalid date. February does not have 30 days."

Input: "25-12-31"
Error: "Invalid date format. Year must be 4 digits. Use YYYY-MM-DD."
```

### Recurrence Validation

```
Input: "biweekly"
Error: "Invalid recurrence. Must be 'daily', 'weekly', or 'monthly'."

Input: "DAILY"
Error: "Invalid recurrence. Must be 'daily', 'weekly', or 'monthly'."
```

---

## Storage Contract

### In-Memory Storage Interface

```python
class TaskStorage:
    """In-memory task storage."""

    def create(self, task: Task) -> Task:
        """Create new task, assign ID, return created task."""
        # Auto-generate ID
        # Validate task data
        # Store in list
        # Return task with ID set

    def read(self, task_id: str) -> Optional[Task]:
        """Get task by ID, return None if not found."""

    def read_all(self) -> List[Task]:
        """Get all tasks in creation order."""

    def update(self, task_id: str, updates: dict) -> Task:
        """Update task fields, return updated task."""
        # Validate updates
        # Merge with existing task
        # Preserve immutable fields

    def delete(self, task_id: str) -> bool:
        """Delete task, return True if deleted."""

    def clear(self) -> None:
        """Clear all tasks (for testing)."""
```

### Storage Guarantees

- **Atomicity**: Single operation (no partial updates)
- **Consistency**: Validation before storage
- **Isolation**: Single-threaded (Phase I)
- **Durability**: None (in-memory, lost on exit)
- **Query Performance**: Filtering/sorting <500ms for 1000 tasks

---

## Examples

### Example 1: Simple Task (Basic Feature)

```json
{
  "id": "task-001",
  "title": "Buy groceries",
  "status": "pending",
  "created_timestamp": "2025-12-30T10:00:00",
  "completed_timestamp": null,
  "priority": "medium",
  "category": null,
  "due_date": null,
  "recurrence": null,
  "parent_recurrence_id": null
}
```

### Example 2: Task with Priority & Category

```json
{
  "id": "task-002",
  "title": "Prepare Q1 presentation",
  "status": "pending",
  "created_timestamp": "2025-12-30T11:30:00",
  "completed_timestamp": null,
  "priority": "high",
  "category": "work",
  "due_date": null,
  "recurrence": null,
  "parent_recurrence_id": null
}
```

### Example 3: Task with Due Date

```json
{
  "id": "task-003",
  "title": "Pay utilities bill",
  "status": "pending",
  "created_timestamp": "2025-12-25T09:00:00",
  "completed_timestamp": null,
  "priority": "high",
  "category": "personal",
  "due_date": "2025-12-31",
  "recurrence": null,
  "parent_recurrence_id": null
}
```

### Example 4: Recurring Task

```json
{
  "id": "task-004",
  "title": "Daily standup",
  "status": "pending",
  "created_timestamp": "2025-12-30T08:00:00",
  "completed_timestamp": null,
  "priority": "medium",
  "category": "work",
  "due_date": "2025-12-31",
  "recurrence": "daily",
  "parent_recurrence_id": null
}
```

### Example 5: Auto-Generated Recurring Task

```json
{
  "id": "task-005",
  "title": "Daily standup",
  "status": "pending",
  "created_timestamp": "2025-12-31T08:00:00",
  "completed_timestamp": null,
  "priority": "medium",
  "category": "work",
  "due_date": "2026-01-01",
  "recurrence": "daily",
  "parent_recurrence_id": "task-004"
}
```

---

## Testing Strategy

### Unit Tests for Data Model

1. **Task Creation**: Valid/invalid inputs, defaults applied
2. **Validation**: Priority, category, due_date, recurrence rules
3. **Immutability**: title, id, created_timestamp cannot change
4. **Enum Handling**: Case sensitivity, valid values
5. **Date Handling**: Format validation, calendar validation, leap years
6. **Backward Compat**: Old tasks get defaults applied
7. **Derived Properties**: is_overdue, next_recurrence_date computed correctly

### Edge Cases

- Very long strings (near 255 char limit)
- Special characters in category
- Dates at boundaries (year 1900, 2099)
- Leap year handling (Feb 29)
- Month-end dates (Jan 31, March 31, etc.)
- Null/empty value handling

