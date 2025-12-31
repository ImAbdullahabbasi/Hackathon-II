# Skill: Business Rules Definition and Conflict Resolution

**Skill ID**: BLE-002
**Agent Owner**: business-logic-engineer
**Project**: Evolution of Todo Hackathon II – Phases 1-5
**Status**: Production

---

## Purpose

Define clear, unambiguous business rules that govern system behavior and resolve conflicts between features. This skill ensures predictable behavior when rules interact, establishes rule priorities, and provides explicit guidance for edge cases. Business rules are the guardrails that prevent the system from entering invalid states and ensure consistency across all features. Well-defined rules reduce ambiguity, support user expectations, and guide implementation and testing.

---

## When to Use

- **Specification phase**: After features are defined, before implementation
- **Feature interaction analysis**: When new features may conflict with existing ones
- **Edge case resolution**: Deciding what happens in ambiguous scenarios
- **Rule priority assignment**: Establishing which rule wins when rules conflict
- **User expectation alignment**: Ensuring rules match what users expect
- **Test case design**: Using rules to derive comprehensive test coverage

---

## Inputs

1. **Feature specifications** (list): From Phase 1 features (create, list, delete, complete, filter, search)
2. **User stories** (list): From RA-001, what users expect
3. **Acceptance criteria** (document): From PA-001, what must work
4. **Edge cases** (list): From QA-001, boundary conditions
5. **Phase roadmap** (optional): How rules evolve across phases

---

## Step-by-Step Process

### Step 1: Identify Rule Categories
Categorize all rules by domain.

**Rule Categories**:

```
1. Data Integrity Rules
   Purpose: Ensure data is valid and consistent
   Examples:
     - Task title must be non-empty (1-255 chars)
     - Task ID must be unique
     - Created timestamp is immutable
     - Due date must be valid (not Feb 30)
     - Status must be one of: pending, completed

2. State Machine Rules
   Purpose: Define valid state transitions
   Examples:
     - New tasks start in "pending" state
     - Only pending tasks can be marked complete
     - Cannot mark a task complete and delete in same operation
     - Cannot delete a task that's already deleted

3. Constraint Rules
   Purpose: Enforce business constraints
   Examples:
     - Maximum 1000 tasks in Phase 1 (in-memory limit)
     - Task title limited to 255 characters
     - Priority must be: low, normal, high
     - Due date cannot be more than 100 years in future

4. Conflict Resolution Rules
   Purpose: Decide what happens when rules conflict
   Examples:
     - Priority determines display order (high before normal)
     - Due date is independent of priority (can have low-priority urgent task)
     - Completion timestamp is immutable (cannot undo completion timestamp)

5. Business Logic Rules
   Purpose: Define expected behavior for operations
   Examples:
     - Sorting by due date puts null due dates at end
     - Filtering is AND operation (status AND priority, not OR)
     - Search is case-insensitive by default
     - Delete requires confirmation (unless --force flag)

6. User Expectation Rules
   Purpose: Ensure system behaves as users expect
   Examples:
     - Confirmation prompts for destructive actions
     - Immediate feedback on task creation ("✓ Task created...")
     - Error messages are helpful (not just "Error occurred")
     - Commands are discoverable (help available everywhere)
```

---

### Step 2: Define Core Business Rules
Create explicit rules for each rule category.

**Data Integrity Rules**:

```
Rule DI-001: Task Title Must Be Non-Empty
  Definition: Every task MUST have a title containing at least 1 character
  Rationale: Tasks without titles are meaningless; prevents data garbage
  Enforcement: Validate on create, reject with error
  Error Message: "✗ Error: Task title cannot be empty"
  Phase: 1+ (all phases)
  Immutable: Yes (cannot be changed once set in Phase 1 MVP)

Rule DI-002: Task Title Maximum Length
  Definition: Task title MUST NOT exceed 255 characters
  Rationale: Prevents storage bloat, ensures consistent display
  Enforcement: Validate on create, reject if > 255
  Error Message: "✗ Error: Task title too long ({actual} chars). Max: 255"
  Phase: 1+ (all phases)
  Mutable in Phase II: Potentially increase to 512 chars

Rule DI-003: Task ID Must Be Unique
  Definition: Each task MUST have a unique ID within collection
  Rationale: ID is primary key; cannot have duplicates
  Enforcement: Check before create, reject if duplicate
  Error Message: "✗ Error: Task ID already exists (system error)"
  Phase: 1+ (all phases)
  Note: Should rarely occur unless multiple instances create simultaneously

Rule DI-004: Created Timestamp Is Immutable
  Definition: Once set, task.created_timestamp CANNOT be changed
  Rationale: Audit trail; prevents tampering with creation history
  Enforcement: Set once at creation, never update
  Phase: 1+ (all phases)
  Bypass: No (even admins cannot change)

Rule DI-005: Due Date Format Is ISO 8601
  Definition: Due date (if provided) MUST be in YYYY-MM-DD format
  Rationale: Standard format, unambiguous, sortable
  Enforcement: Validate on create, reject if wrong format
  Error Message: "✗ Error: Invalid date format '{provided}'. Expected YYYY-MM-DD (e.g., 2026-01-15)"
  Phase: 1+ (all phases)
  Supported Formats: Only YYYY-MM-DD (not DD/MM/YYYY, not MM/DD/YYYY)

Rule DI-006: Due Date Must Be Valid Calendar Date
  Definition: Due date (if provided) MUST represent actual calendar date
  Rationale: Prevents storing impossible dates (Feb 30)
  Enforcement: Validate on create, reject if invalid
  Error Message: "✗ Error: Invalid date '2026-02-30'. February has only 28 days."
  Phase: 1+ (all phases)
  Note: Both past and future dates allowed

Rule DI-007: Status Must Be Enum Value
  Definition: Task status MUST be one of: pending, completed
  Rationale: Ensures state machine is well-defined
  Enforcement: Validate on create/update, reject if unknown
  Error Message: "✗ Error: Invalid status '{value}'. Allowed: pending, completed"
  Phase: 1 (may expand in Phase III)
  Phase III Note: May add in_progress, blocked, archived

Rule DI-008: Priority Must Be Enum Value
  Definition: Task priority MUST be one of: low, normal, high
  Rationale: Prevents arbitrary priority values
  Enforcement: Validate on create, default to "normal"
  Error Message: "✗ Error: Invalid priority '{value}'. Allowed: low, normal, high"
  Phase: 1+ (all phases)

Rule DI-009: Completed Timestamp Set When Complete
  Definition: When status changes to "completed", completed_timestamp MUST be set
  Rationale: Records when task was completed (for analytics)
  Enforcement: Set automatically when status → completed
  Phase: 1+ (all phases)
  Immutability: Once set, never cleared (even if reverted to pending in Phase II)

Rule DI-010: Version Field Tracks Schema
  Definition: Each task MUST have version field matching data schema
  Rationale: Enables migrations across phase upgrades
  Enforcement: Set to "1.0.0" for Phase 1 tasks
  Phase: 1+ (all phases)
  Phase II: Updated to "2.0.0" during migration
```

**State Machine Rules**:

```
Rule SM-001: New Tasks Start Pending
  Definition: When task is created, status MUST be set to "pending"
  Rationale: New tasks are not done yet
  Enforcement: Automatic in create operation
  Phase: 1+ (all phases)
  Cannot Override: No way to create task in completed state

Rule SM-002: Only Pending Tasks Can Be Marked Complete
  Definition: Only tasks with status="pending" CAN be marked complete
  Rationale: Prevents completing already-completed tasks
  Enforcement: Check status before marking complete
  Error Message: "✗ Error: Task already completed: {id} '{title}'"
  Phase: 1+ (all phases)

Rule SM-003: Cannot Delete and Complete Simultaneously
  Definition: User CANNOT mark a task complete and delete in same command
  Rationale: Prevents ambiguous state (is it done or gone?)
  Enforcement: Reject if both operations requested
  Error Message: "✗ Error: Cannot both complete and delete. Choose one operation."
  Phase: 1 (may relax in Phase II)

Rule SM-004: Status Transitions Are One-Way in Phase 1
  Definition: In Phase 1, status: pending → completed → (stuck)
  Rationale: No "undo" feature in Phase 1 MVP
  Enforcement: Cannot revert completed task to pending
  Error Message: "Cannot revert task. Feature coming in Phase 2."
  Phase: 1 (Phase II will add revert)
  Phase II: Will allow pending ↔ completed transitions

Rule SM-005: Deleted Task Cannot Be Recovered in Phase 1
  Definition: Once deleted, task is gone permanently (no trash/archive)
  Rationale: Phase 1 simplicity; Phase II adds soft delete
  Enforcement: None (deletion is immediate and final)
  Warning: Show confirmation before delete
  Phase: 1 (Phase II+ will add trash/archive)

Rule SM-006: Cannot Transition to Unknown State
  Definition: Invalid state transitions are rejected
  Rationale: Prevents state machine corruption
  Enforcement: Validate all status changes
  Error Message: "✗ Error: Invalid state transition {current} → {requested}"
  Phase: 1+ (all phases)
```

**Constraint Rules**:

```
Rule CR-001: Maximum Task Limit (Phase 1)
  Definition: Cannot create more than 1000 tasks in Phase 1
  Rationale: In-memory storage limit for MVP
  Enforcement: Check task count before create
  Error Message: "✗ Error: Cannot create task (limit of 1000 tasks reached)"
  Phase: 1 only (removed in Phase II with database)
  Workaround: Delete unused tasks or upgrade to Phase II

Rule CR-002: Priority Must Be Standard Values Only
  Definition: Priority MUST be exactly: "low", "normal", or "high"
  Rationale: Prevents custom priorities without infrastructure
  Enforcement: Validate on create, reject if not in set
  Error Message: "✗ Error: Invalid priority '{value}'. Use: low, normal, high"
  Phase: 1 (Phase II may add custom priorities)
  Phase II: May allow custom priority definitions

Rule CR-003: Task ID Format Is Sequential
  Definition: Task IDs MUST follow format "task-NNN" (NNN = 3-digit number)
  Rationale: Human-readable, predictable, sortable
  Enforcement: Generate automatically, never accept user-provided IDs
  Format Pattern: task-001, task-002, ..., task-999, task-1000
  Phase: 1 (may change to UUID in Phase II)
  Phase II: May switch to UUID (a1b2c3d4...)

Rule CR-004: No Duplicate Task Titles Allowed
  Definition: Multiple tasks CAN have same title (duplicates allowed)
  Rationale: User might have multiple "Buy groceries" at different times
  Enforcement: No enforcement (allow duplicates)
  Phase: 1 (Phase II may add optional deduplication)
  Note: Unlike unique IDs, same title is intentional

Rule CR-005: Due Date Can Be Past or Future
  Definition: Due date CAN be in the past (before today)
  Rationale: Users track backlog items, historical tasks, etc.
  Enforcement: No restriction (accept any valid date)
  Warning: Optional warning "Task due date is in the past"
  Phase: 1+ (all phases)

Rule CR-006: No Multi-User Sharing in Phase 1
  Definition: All tasks are owned by "system" user (implicit)
  Rationale: Phase 1 is single-user console app
  Enforcement: No user field in Phase 1 data model
  Phase: 1 only (Phase II adds user_id)
  Phase II: user_id field tracks ownership
```

**Conflict Resolution Rules**:

```
Rule CFR-001: Priority vs Due Date
  Definition: When rules conflict, due date (deadline) takes precedence
  Example: Low-priority task due today is more urgent than high-priority task due next month
  Enforcement: In UI/sorting, show by due date first, then priority within same due date
  Sorting Order: Group by due date (today, overdue, this week, later), then by priority within group
  Phase: 1 (explicit in Phase II UI sorting)

Rule CFR-002: Completion Timestamp Is Immutable
  Definition: completed_timestamp, once set, CANNOT be cleared
  Rationale: Maintains audit trail even if task status reverted (Phase II feature)
  Example: Task completed 2026-01-15, reverted to pending 2026-01-20
    - status changes: pending → completed
    - completed_timestamp changes: null → 2026-01-15
    - Later, if status reverted: status pending, but completed_timestamp stays 2026-01-15
  Enforcement: completed_timestamp only set once, never cleared
  Phase: 1+ (all phases)

Rule CFR-003: Confirmation vs Speed
  Definition: Safety (confirmation) takes priority over speed (no confirmation)
  Example: Delete requires confirmation; marking complete does not
  Rationale: Destructive actions need confirmation, safe actions don't
  Enforcement: Confirmation required for: delete
                Confirmation skipped for: create, complete
  Phase: 1+ (all phases)

Rule CFR-004: Case Sensitivity in Search
  Definition: Search is case-insensitive by default
  Example: Search "grocery" matches "Grocery", "GROCERY", "GrOcery"
  Rationale: Users don't remember exact case
  Enforcement: Convert both query and text to lowercase for comparison
  Override: --case-sensitive flag enables case-sensitive
  Phase: 1+ (all phases)

Rule CFR-005: Filter Operators Are AND, Not OR
  Definition: Multiple filters combine with AND logic, not OR
  Example: --filter pending --priority high means (status=pending AND priority=high), not OR
  Rationale: More predictable; users expect narrower results with more filters
  Enforcement: Implement as nested conditions (all must match)
  Phase: 1+ (all phases)
  Future Note: Phase III may add OR/NOT logic with operators

Rule CFR-006: Sort Stability
  Definition: When primary sort key is equal, maintain insertion order (stable sort)
  Example: Two pending tasks with same priority → show in creation order
  Rationale: Predictable, reproducible results
  Enforcement: Use stable sort algorithm (not quicksort with random pivot)
  Phase: 1+ (all phases)
```

**Business Logic Rules**:

```
Rule BL-001: Sorting by Due Date Handles Nulls
  Definition: Tasks without due date appear AFTER tasks with due date
  Order: [tasks with due date sorted ascending] + [tasks without due date]
  Example: [2026-01-10, 2026-01-15, null, null]
  Rationale: Users expect to see deadline tasks first
  Enforcement: Separate null/non-null, sort non-null, concatenate
  Phase: 1+ (all phases)

Rule BL-002: Sorting by Priority (High First)
  Definition: Tasks sorted: high → normal → low
  Order: [high priority tasks] + [normal priority tasks] + [low priority tasks]
  Rationale: Important tasks shown first
  Enforcement: Define priority order {high:1, normal:2, low:3}, sort ascending
  Phase: 1+ (all phases)

Rule BL-003: Sorting by Created Date (Newest/Oldest First)
  Definition: Default sort is by created_timestamp, ascending (oldest first)
  Can be reversed: --reverse shows newest first
  Rationale: Chronological order is most natural default
  Enforcement: Sort by created_timestamp, allow --reverse flag
  Phase: 1+ (all phases)

Rule BL-004: List Returns Limited Results
  Definition: List command returns max 20 results by default (--limit 20)
  Rationale: Prevents overwhelming user with 1000+ line output
  Enforcement: Truncate results after 20 items, show info message
  Message: "Showing 20 of 100 tasks. Run 'todo list --limit 100' to see all."
  Phase: 1 (may adjust default in Phase II)
  Override: User can --limit 0 for all results or --limit N for custom

Rule BL-005: Search Is Substring Match
  Definition: Search finds keyword anywhere in task title
  Example: Search "grocery" matches "Buy groceries", "grocery store", "GROCERY LIST"
  Rationale: More flexible than exact match
  Enforcement: Check if keyword.lower() in title.lower()
  Phase: 1 (Phase II may add regex or full-text search)

Rule BL-006: Empty Results Are Valid, Not Errors
  Definition: When filter/search returns no tasks, show empty result with message (not error)
  Example: --filter pending when all tasks completed → show empty list, not error
  Rationale: No tasks matching criteria is valid state
  Enforcement: Return empty list with informative message
  Message: "No pending tasks. All tasks are completed!"
  Phase: 1+ (all phases)

Rule BL-007: Confirmation Prompts for Destructive Actions
  Definition: Delete requires user confirmation before executing
  Format: "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
  Rationale: Prevents accidental deletion
  Override: --force flag skips confirmation
  Enforcement: Show prompt unless --force flag
  Phase: 1+ (all phases)

Rule BL-008: Feedback on All Operations
  Definition: Every operation (create, delete, complete) shows result message
  Format: ✓ [success message] or ✗ [error message]
  Rationale: Users need confirmation that action worked
  Enforcement: Always output result message
  Phase: 1+ (all phases)
```

**User Expectation Rules**:

```
Rule UE-001: Commands Are Discoverable
  Definition: User can type "todo" (no args) and see quick start guide
  Content: Lists main commands (add, list, complete, delete, help)
  Rationale: New users shouldn't need documentation
  Enforcement: Implement default help menu
  Phase: 1+ (all phases)

Rule UE-002: Help Is Always Available
  Definition: Every command supports --help flag
  Example: "todo add --help" shows add-command help
  Enforcement: --help recognized by all commands
  Phase: 1+ (all phases)

Rule UE-003: Error Messages Are Helpful
  Definition: Error messages explain what went wrong AND how to fix it
  Format: ✗ Error: [what went wrong]. [how to fix]. Example: [example]
  Rationale: Users should be able to self-serve
  Enforcement: No cryptic errors; all errors must be actionable
  Phase: 1+ (all phases)

Rule UE-004: Defaults Are Sensible
  Definition: Default values match what most users want most of the time
  Examples:
    - priority defaults to "normal" (not high/low)
    - due_date defaults to null (most tasks have no deadline)
    - status defaults to "pending" (new tasks not done)
    - sort defaults to "created" (chronological)
    - filter defaults to "all" (show everything)
  Rationale: Reduces user decisions, faster for common cases
  Enforcement: Use these defaults unless user overrides
  Phase: 1+ (all phases)

Rule UE-005: Immediate Feedback on Actions
  Definition: User sees result within 1 second of command execution
  Rationale: Confirms action worked
  Enforcement: No delays; all Phase 1 operations must be instant
  Performance: All operations < 1000ms (should be < 100ms)
  Phase: 1 (Phase II with database may need to relax this)

Rule UE-006: Commands Are Consistent
  Definition: All commands follow same patterns
  Pattern: [command] [argument] [--flags]
  Example: "todo add 'task'" vs "todo delete 'task-001'" vs "todo list --filter pending"
  Rationale: Users learn once, apply everywhere
  Enforcement: All commands follow verb-noun-arguments pattern
  Phase: 1+ (all phases)

Rule UE-007: Destructive Actions Show Confirmation
  Definition: Before delete, user sees what's being deleted
  Format: "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
  Rationale: User sees exactly what will be lost
  Enforcement: Show full task details in confirmation prompt
  Phase: 1+ (all phases)

Rule UE-008: No Silent Failures
  Definition: If operation fails, user sees clear error (not silent failure)
  Example: If storage fails, don't silently skip; show "✗ Error: Cannot save task"
  Rationale: Users need to know what failed
  Enforcement: Every code path that could fail must return error message
  Phase: 1+ (all phases)
```

---

### Step 3: Establish Rule Priority
Define which rule wins when rules conflict.

**Rule Priority Hierarchy**:

```
Level 1: Safety & Data Integrity (Highest Priority)
  - DI-* rules (data must be valid)
  - SM-* rules (state must be valid)
  - CFR-001 (completion timestamp immutable)
  Rationale: System must never enter invalid state
  Example: Even if user wants to create task with empty title, reject it

Level 2: Business Logic & Constraints (High Priority)
  - CR-* rules (limits and constraints)
  - BL-* rules (operations must follow defined logic)
  Rationale: System behavior must be predictable
  Example: Search results ordered by created date, not random

Level 3: User Experience & Expectations (Medium Priority)
  - UE-* rules (user sees expected behavior)
  - CFR-003 (confirmation before delete)
  Rationale: Users expect responsive, helpful system
  Example: Show error messages that help users self-serve

Level 4: Performance & Optimization (Lower Priority)
  - Speed of operations
  - Memory efficiency
  Rationale: Nice-to-have, but never sacrifice correctness
  Example: Don't use buggy fast algorithm; use correct slow algorithm

Conflict Resolution Example:

Scenario: User wants to save a task but storage is full (CR-001 violated)
  Conflicting Rules:
    - BR-002: User expects immediate feedback
    - CR-001: Can't create more than 1000 tasks
  Decision:
    - Level 1 wins: Cannot create task (data integrity)
    - Level 3 applies: But show helpful error message
  Result: "✗ Error: Cannot create task (limit of 1000 tasks reached). Delete unused tasks or upgrade to Phase II."
  This violates "immediate feedback" but protects data integrity
```

---

### Step 4: Define Phase-Specific Rules
Document how rules evolve across phases.

**Phase Rule Evolution**:

```
Phase 1 (In-Memory Console):
  Rule CR-001: 1000 task limit ACTIVE
  Rule SM-004: Cannot revert completed ACTIVE
  Rule SM-005: Cannot recover deleted ACTIVE
  Rule CR-003: Sequential ID format ACTIVE

Phase II (Web App + Database):
  Rule CR-001: 1000 task limit REMOVED (database has no limit)
  Rule SM-004: Cannot revert completed CHANGED → Can revert (add mark-pending)
  Rule SM-005: Cannot recover deleted CHANGED → Can recover (soft delete/trash)
  Rule CR-003: Sequential ID format UNCHANGED (keep for backward compat)
  New Rules:
    - User ownership (every task has user_id)
    - Task visibility (users only see their tasks)

Phase III (AI Chatbot):
  New Rules:
    - AI can generate recurring tasks
    - AI can suggest task improvements
    - Task completion frequency tracked (analytics)

Phase IV (Kubernetes):
  New Rules:
    - Tasks distributed across shards (regional)
    - Eventual consistency rules (replicated data)

Phase V (Cloud + Advanced):
  New Rules:
    - Real-time collaboration (lock/unlock)
    - Audit logging mandatory
    - Data retention policies (30-year archive)

Migration Rules:
  - Never remove Phase 1 rule data (backward compat)
  - Phase 1 tasks with ID="task-001" work in Phase V
  - No requirement to migrate data (users can use Phase 1 data in Phase II+)
```

---

### Step 5: Document Rule Dependencies
Map how rules relate to and support each other.

**Rule Dependency Map**:

```
Data Integrity Rules (DI-*)
  ↓ Supported by:
  - SM-* rules (ensure valid state transitions)
  - CR-* rules (constraints prevent invalid data)

State Machine Rules (SM-*)
  ↓ Supported by:
  - DI-* rules (no invalid data reaches state machine)
  - CFR-* rules (handle conflicts between states)

Conflict Resolution Rules (CFR-*)
  ↓ Supported by:
  - BL-* rules (algorithms implement conflict logic)
  - UE-* rules (users see expected behavior)

Business Logic Rules (BL-*)
  ↓ Supported by:
  - DI-* rules (input must be valid)
  - CFR-* rules (handle edge cases)

User Expectation Rules (UE-*)
  ↓ Supported by:
  - BL-* rules (correct behavior)
  - Error messaging guidelines (QA-002)

Example Dependency Chain:
  User creates task "Buy" with title length 3
    → UE-004 (sensible defaults applied)
    → DI-002 (title length 3 is within 1-255)
    → SM-001 (status set to pending)
    → DI-009 (completed_timestamp null)
    → BL-008 (feedback shown: "✓ Task created")
  Result: Valid task created successfully
```

---

### Step 6: Validate Rules for Completeness
Ensure rules cover all scenarios.

**Rule Validation Checklist**:

```
For Each Feature (Create, List, Delete, Complete, Search, Filter):

✅ Data Integrity
  [ ] All inputs are validated (DI-001 through DI-010)
  [ ] No data can be invalid in storage
  [ ] Immutable fields are protected
  [ ] Unique constraints enforced

✅ State Management
  [ ] Valid state transitions defined (SM-001 through SM-006)
  [ ] Invalid transitions rejected
  [ ] Cannot reach invalid state
  [ ] State is always consistent

✅ Constraints
  [ ] All limits documented (CR-001 through CR-006)
  [ ] Constraints enforced before operation
  [ ] Error message shown when limit reached
  [ ] Workarounds or alternatives suggested

✅ Conflict Resolution
  [ ] Rules for conflicting priorities exist (CFR-001 through CFR-006)
  [ ] Clear winner defined for each conflict
  [ ] User sees predictable behavior
  [ ] No ambiguous outcomes

✅ Business Logic
  [ ] Sorting rules clear (BL-001 through BL-003)
  [ ] Search/filter logic documented (BL-004 through BL-006)
  [ ] Operations have predictable results
  [ ] Edge cases handled (empty results, nulls, boundaries)

✅ User Expectations
  [ ] Help is discoverable (UE-001)
  [ ] Error messages are helpful (UE-003)
  [ ] Defaults are sensible (UE-004)
  [ ] Feedback is immediate (UE-005)
  [ ] Commands are consistent (UE-006)
  [ ] Destructive actions confirmed (UE-007)
  [ ] No silent failures (UE-008)
```

---

## Output

**Format**: Structured Markdown document with complete rule definitions:

```markdown
# Business Rules Definition and Conflict Resolution

## Rule Categories
[Data Integrity, State Machine, Constraints, Conflict Resolution, Business Logic, User Expectations]

## Complete Rule Definitions
[DI-001 through UE-008, each with definition, rationale, enforcement, phase]

## Rule Priority Hierarchy
[5 levels, from safety to performance]

## Rule Dependencies
[How rules support each other]

## Phase Evolution
[How rules change from Phase 1 to Phase V]

## Conflict Resolution Examples
[Specific scenarios showing which rules win]

## Validation Checklist
[Ensuring complete rule coverage]
```

---

## Failure Handling

### Scenario 1: Rule Conflict Not Resolved
**Symptom**: Two rules contradict (delete requires confirmation, but user expects instant)
**Resolution**:
- Document conflict explicitly: "Safety (confirmation) takes priority over speed"
- Establish clear winner: "Delete always requires confirmation (unless --force)"
- Explain rationale: "Destructive actions need safeguards"

### Scenario 2: Rule Changes Between Phases
**Symptom**: Phase 1 rule "cannot revert completed tasks" removed in Phase II
**Resolution**:
- Document rule evolution: "Phase 1: Rule active. Phase II: Rule removed"
- Plan migration: "Phase II adds mark-pending command"
- Ensure backward compatibility: "Phase 1 data works in Phase II, just can't revert"

### Scenario 3: Rule Violated in Implementation
**Symptom**: Code allows task title > 255 chars (violates DI-002)
**Resolution**:
- Code review catches violation: "Rule DI-002 requires max 255 chars"
- Fix code: Add validation before saving
- Test: Verify max length enforced

### Scenario 4: New Feature Violates Existing Rule
**Symptom**: New Phase II feature wants to share tasks (violates Phase 1 rule "no sharing")
**Resolution**:
- Phase II removes rule: "Phase 1 rule CR-006 'no sharing' is removed"
- Add new rules: "Phase II rule: Every task must have owner user_id"
- Plan migration: "Phase 1 tasks get default owner"

### Scenario 5: User Expectation Rule Conflicts with Business Rule
**Symptom**: User expects instant feedback (UE-005) but validating data takes time (BL-001)
**Resolution**:
- Document priority: "User experience is Level 3, Business logic is Level 2"
- Business logic wins: Validate data even if slightly slower
- Optimize: Make validation fast enough for < 1 second (still satisfies UE-005)

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Feature design**: Rules define expected behavior before coding
- **Test case generation**: Rules derive comprehensive test coverage
- **Code review**: Rules validate implementation matches intent
- **Phase transitions**: Rules show what changes between phases
- **Documentation**: Rules serve as executable spec
- **Support training**: Rules explain system behavior to support team

---

## Success Metrics

- ✅ All rules are explicit and documented (not implicit)
- ✅ All conflicts have clear resolution (no ambiguity)
- ✅ Rules are prioritized (Level 1-5 hierarchy)
- ✅ Rules are phase-specific (show evolution)
- ✅ Rules cover all features (create, list, delete, complete, filter, search)
- ✅ Rules cover edge cases (empty list, no matches, boundary values)
- ✅ Rules include error messages (specific, not generic)
- ✅ Rules are testable (every rule can be verified)
- ✅ Rules are enforceable (code can implement them)
- ✅ User expectations documented (rules match what users expect)

---

## Related Skills

- **Algorithms (BLE-001)**: Implement these rules
- **Acceptance Criteria (PA-001)**: Tests verify rules are followed
- **Edge Case Identification (QA-001)**: Tests verify edge cases per rules
- **Error Messaging (QA-002)**: Error messages explain rule violations

---

## Example: Complete Rule Scenario

### Scenario: User Creates Task with Invalid Due Date

**Command**: `todo add 'Meeting' --due 2026-02-30`

**Rule Chain**:

```
Step 1: User Input
  - User provides due date: "2026-02-30"
  - Rule UE-004 applies: Expect helpful error (not crash)

Step 2: Format Validation
  - Rule DI-005 checks: "Is format YYYY-MM-DD?" → YES
  - Proceed to next step

Step 3: Date Validity
  - Rule DI-006 checks: "Is 2026-02-30 a valid calendar date?" → NO
    (February has 28 days in 2026, not a leap year)
  - Apply CFR-002: Immutable rule wins (can't ignore validation)
  - Rule Level 1 (Data Integrity) > Rule Level 3 (UX)
  - Decision: REJECT

Step 4: Error Message
  - Rule UE-003 applies: Error must be helpful
  - Message: "✗ Error: Invalid date '2026-02-30'. February has 28 days in 2026."
  - Add suggestion: "Did you mean 2026-02-28?"

Step 5: User Recourse
  - Rule UE-001 applies: Help is available
  - Suggest: "Run 'todo add --help' for date format examples"

Result:
  ✗ Error: Invalid date '2026-02-30'. February has 28 days in 2026.
  Did you mean 2026-02-28?
  Run 'todo add --help' for date format examples.

Rule Validation:
  ✓ DI-006 (date validity) enforced
  ✓ CFR-001 (conflict resolved in favor of data integrity)
  ✓ UE-003 (helpful error message)
  ✓ UE-001 (help available)
  ✓ User expectation met (understood what went wrong, how to fix)
```

---

### Scenario: User Tries to Delete and Complete Same Task

**Command**: `todo delete task-001 --also-complete` (hypothetical)

**Rule Chain**:

```
Step 1: User Input
  - User requests: delete AND complete
  - Rule SM-003 checks: "Can task have two simultaneous status changes?" → NO
  - Decision: REJECT

Step 2: Error Resolution
  - Rule CFR-003 applies: "Confirmation takes priority"
  - Decision: Show error, require choosing one action

Step 3: Error Message
  - Rule UE-003: Error must be helpful
  - Show both options:
    "✗ Error: Cannot both complete and delete. Choose one:
      1. Mark complete: todo complete task-001
      2. Delete: todo delete task-001"

Step 4: User Recourse
  - User chooses one command and reruns

Result: User understands conflict and knows how to proceed

Rule Validation:
  ✓ SM-003 (mutually exclusive operations) enforced
  ✓ CFR-003 (safety priority) applied
  ✓ UE-003 (helpful error) provided
  ✓ User not forced to pick; given clear options
```

---

## Conclusion

Phase 1 business rules are explicit, complete, and prioritized. Rules ensure:

1. **Data Integrity**: System never enters invalid state
2. **Predictability**: Users know what will happen
3. **Safety**: Destructive actions guarded with confirmation
4. **Clarity**: Conflicts have clear resolution
5. **Helpfulness**: Error messages guide users to fix

Rules are the contract between users and system; clear rules build trust.

