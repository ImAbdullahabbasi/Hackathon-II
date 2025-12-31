# Skill: Task State Management and Transitions

**Skill ID**: BLE-003
**Agent Owner**: business-logic-engineer
**Project**: Evolution of Todo Hackathon II – Phases 1-5
**Status**: Production

---

## Purpose

Define all possible task states, document transitions between states, and enforce rules preventing invalid state changes. This skill ensures the task state machine is well-defined, predictable, and correct. A properly designed state machine prevents the system from reaching invalid or corrupted states, makes debugging easier, and enables users to understand task lifecycle. State management is critical for features like completion tracking, recurring tasks (Phase III), and collaborative workflows (Phase II+).

---

## When to Use

- **Feature design phase**: After rules (BLE-002) are defined
- **Implementation planning**: Before coding state transitions
- **Testing**: Defining test cases for valid/invalid transitions
- **Documentation**: Explaining task lifecycle to users
- **Phase transitions**: Planning how state machine evolves (Phase 1→5)
- **Debugging**: Identifying impossible states in bug reports

---

## Inputs

1. **Business rules** (document): From BLE-002, state machine rules (SM-*)
2. **User stories** (list): From RA-001, what users expect for task lifecycle
3. **Acceptance criteria** (document): From PA-001, what transitions must work
4. **Edge cases** (list): From QA-001, boundary conditions for states
5. **Phase roadmap** (optional): How state machine evolves across phases

---

## Step-by-Step Process

### Step 1: Define State Universe
Identify all possible states across all phases.

**State Universe by Phase**:

```
Phase 1 (In-Memory Console):
  States: pending, completed
  Count: 2 states
  Transitions: pending → completed (one-way in Phase 1)

Phase II (Web App):
  States: pending, in_progress, completed, (archived/trash for soft delete)
  Count: 3-4 states
  Transitions: pending ↔ in_progress ↔ completed (reversible)

Phase III (AI Chatbot):
  New State: regenerated (recurring task spawned new instance)
  States: pending, in_progress, completed, regenerated, archived
  Count: 5 states
  Transitions: Plus special handling for recurring tasks

Phase IV (Kubernetes):
  New State: synced (replicated to other regions)
  States: pending, in_progress, completed, regenerated, archived, synced
  Count: 6 states

Phase V (Cloud + Advanced):
  New States: delegated (assigned to team member), waiting_on_other (blocked)
  States: pending, in_progress, completed, delegated, waiting_on_other, archived, synced
  Count: 7-8 states

Phase 1 Focus: Only pending + completed
```

**State Definitions (Phase 1)**:

```
State: pending
  Definition: Task has not been completed yet
  Characteristics:
    - status = "pending"
    - completed_timestamp = null
    - User sees this in pending filters
    - Can be marked complete
    - Can be deleted
  Entry Point: Task creation (default)
  Exit Conditions: Mark complete, delete
  Duration: From creation until completion or deletion
  Example: "Buy groceries" just created, waiting to be done

State: completed
  Definition: Task has been finished/done
  Characteristics:
    - status = "completed"
    - completed_timestamp = set to when marked complete
    - User sees this in completed filters
    - Cannot be marked complete again (already done)
    - Can be deleted (in Phase 1; soft delete in Phase II)
  Entry Point: Mark pending task as complete
  Exit Conditions: Delete (in Phase 1; revert to pending in Phase II)
  Duration: From completion until deleted
  Example: "Buy groceries" marked complete on 2026-01-15
```

---

### Step 2: Design State Machine (Phase 1)
Create state diagram and transition rules for Phase 1.

**Phase 1 State Machine (Textual Diagram)**:

```
                    ┌──────────────┐
                    │              │
                    │   PENDING    │
                    │  (initial)   │
                    │              │
                    └──────────────┘
                         │    ▲
                         │    │
          Mark Complete  │    │ Revert (Phase II+)
                (Rule)   │    │
                         │    │
                         ▼    └────────────────┐
                    ┌──────────────┐           │
                    │              │           │
                    │  COMPLETED   │◄──────────┘
                    │              │
                    └──────────────┘

Transitions in Phase 1:
  pending → completed: ALLOWED (via "complete" command)
  completed → pending: NOT ALLOWED in Phase 1 (Phase II+ will allow)
  pending → pending: NOT ALLOWED (no-op)
  completed → completed: NOT ALLOWED (already done)

Invalid State:
  Any other state: FORBIDDEN (no corrupted states)

Delete Paths:
  pending → [deleted]: ALLOWED (delete task in pending state)
  completed → [deleted]: ALLOWED (delete task in completed state)
  Both visible until actually deleted
```

**Transition Table (Phase 1)**:

```
Current State │ Action          │ New State   │ Allowed │ Condition
──────────────┼─────────────────┼─────────────┼─────────┼──────────────────────────────
pending       │ Complete        │ completed   │ YES     │ Task must exist and be pending
pending       │ Delete          │ [deleted]   │ YES     │ User confirms deletion
pending       │ Create          │ (N/A)       │ NO      │ Already exists
completed     │ Complete Again  │ (unchanged) │ NO      │ Cannot complete twice
completed     │ Delete          │ [deleted]   │ YES     │ User confirms deletion
completed     │ Revert          │ pending     │ NO      │ Not in Phase 1 (Phase II+ allows)
any           │ Create New      │ pending     │ YES     │ Creates different task (OK)
any           │ Filter/Search   │ (unchanged) │ YES     │ State not changed by query
```

---

### Step 3: Define Transition Rules
Create explicit rules for each allowed transition.

**Transition: pending → completed**

```
Rule: Mark Task Complete
  Name: SM-002 (from BLE-002 Business Rules)
  Trigger: User runs "todo complete <TASK_ID>"
  Pre-Conditions:
    - Task with ID must exist
    - Task.status must be "pending" (not already completed)
    - Task.completed_timestamp must be null
  Actions:
    1. Set task.status = "completed"
    2. Set task.completed_timestamp = current_time_utc()
    3. Persist change (save to storage)
  Post-Conditions:
    - Task.status = "completed"
    - Task.completed_timestamp = set (immutable from now on)
    - Task no longer appears in pending filters
    - Task appears in completed filters
  Output:
    ✓ Task marked complete: task-001 'Buy groceries'
  Error Cases:
    - Task not found: ✗ Error: Task not found: task-001
    - Task already completed: ✗ Error: Task already completed: task-001
    - Task in unknown state: ✗ Error: Cannot complete task (invalid state)
  Rollback:
    - If save fails: Revert status to pending, completed_timestamp to null
    - Show error: ✗ Error: Cannot save task
  Reversibility:
    - Phase 1: NOT reversible (cannot undo completion)
    - Phase II+: REVERSIBLE via "todo mark task-001 pending"

Verification:
  ✓ Only tasks in pending state can be marked complete
  ✓ Completed timestamp is immutable (never cleared)
  ✓ Task no longer appears in pending filters
  ✓ Task appears in completed filters
```

**Transition: pending → deleted**

```
Rule: Delete Task
  Name: SM-005 (related to BLE-002 Business Rules)
  Trigger: User runs "todo delete <TASK_ID>"
  Pre-Conditions:
    - Task with ID must exist
    - Task.status can be pending or completed (delete both)
    - User must confirm deletion (safety check)
  Actions:
    1. Find task in list
    2. Show confirmation prompt: "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
    3. Wait for user confirmation
    4. IF user confirms (y):
       - Remove task from list
       - Persist change (save updated list)
    5. ELSE (user says no):
       - Do nothing, return to main menu
  Post-Conditions:
    - Task removed from list
    - Task no longer retrievable by ID
    - Task does not appear in any filters
    - List is shorter by 1 task
  Output:
    ✓ Task deleted: task-001 'Buy groceries'
  Error Cases:
    - Task not found: ✗ Error: Task not found: task-001
    - Delete fails (storage error): ✗ Error: Cannot delete task
  Rollback:
    - Phase 1: NO ROLLBACK (deletion is permanent)
    - Phase II+: Can recover from trash/recycle bin
  Reversibility:
    - Phase 1: NOT reversible (permanently deleted)
    - Phase II+: Can restore from trash within 30 days

Confirmation Prompt:
  "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
  - Show full task ID and title (so user knows exactly what's being deleted)
  - Warn: "This cannot be undone" (emphasize permanence in Phase 1)
  - Allow abort: User can press Escape or type "n" to cancel

Verification:
  ✓ Confirmation shown before deletion
  ✓ Correct task deleted (not wrong task)
  ✓ Task no longer retrievable after deletion
  ✓ Delete can be aborted (user says no)
```

**Transition: completed → deleted**

```
Rule: Delete Completed Task
  Trigger: User runs "todo delete <TASK_ID>" on already-completed task
  Pre-Conditions:
    - Task with ID must exist
    - Task.status is "completed"
    - User must confirm deletion
  Actions:
    1. Show confirmation prompt including completed status
    2. Wait for user confirmation
    3. If confirmed: remove task, persist change
    4. If not confirmed: return to main menu
  Post-Conditions:
    - Task removed from list
    - No longer appears in completed filters
  Output:
    ✓ Task deleted: task-001 'Buy groceries' (was completed on 2026-01-15)
  Special Handling:
    - Show that task was completed (informational)
    - But still allow deletion (completed status doesn't prevent delete)

Verification:
  ✓ Can delete both pending and completed tasks
  ✓ No artificial restriction on deleting completed tasks
```

---

### Step 4: Document Forbidden Transitions
Explicitly define what CANNOT happen.

**Forbidden Transitions (Phase 1)**:

```
Transition: completed → pending
  Rule: Cannot revert completed task in Phase 1
  Reason: Phase 1 MVP simplicity; reverting is Phase II feature
  If Attempted: ✗ Error: Cannot revert task. Feature coming in Phase 2.
  Verification: Test that no mechanism allows this transition

Transition: pending → pending
  Rule: No-op transition; not allowed
  Reason: No meaningful action; pointless to "complete" pending task to pending
  If Attempted: Not applicable (no command does this)
  Verification: No command triggers this

Transition: completed → completed
  Rule: Cannot mark already-completed task as complete
  Reason: Task is already done; marking done again is error
  If Attempted: ✗ Error: Task already completed: task-001 'Buy groceries'
  Verification: Test that completing completed task shows error

Transition: [unknown] → any
  Rule: Corrupted state (task in invalid state)
  Reason: System should never reach invalid state
  If Attempted: ✗ Error: Cannot perform operation (task in invalid state)
  Verification: Test that invalid states cannot occur

Transition: any → [unknown_state]
  Rule: Cannot transition to undefined state
  Reason: Only pending and completed defined; no other states
  If Attempted: Prevented by code validation (state enum check)
  Verification: Test that setting status to undefined value is rejected

Parallel Transitions:
  Transition: pending → {completed, deleted} simultaneously
  Rule: Cannot complete and delete in same command
  Reason: Conflict; unclear final state
  If Attempted: ✗ Error: Cannot both complete and delete. Choose one.
  Verification: Test that mutually exclusive operations are prevented
```

---

### Step 5: Define State-Dependent Behavior
Show how system behaves differently in each state.

**State-Dependent Behavior**:

```
Feature: Filtering

Pending State:
  - Task appears in: "todo list --filter pending"
  - Task appears in: "todo list --filter all" (default)
  - Task does NOT appear in: "todo list --filter completed"
  - Behavior: Task is "active" and needs attention

Completed State:
  - Task appears in: "todo list --filter completed"
  - Task appears in: "todo list --filter all" (default)
  - Task does NOT appear in: "todo list --filter pending"
  - Behavior: Task is "done" and out of active list

---

Feature: Sorting

Pending State:
  - Included in sort operations (by due date, priority, created)
  - Sorted alongside other pending tasks
  - May be intermixed with completed tasks in "all" view (depends on filter)

Completed State:
  - Included in sort operations
  - Sorted alongside other completed tasks
  - May be intermixed with pending tasks in "all" view

---

Feature: Editing/Modification

Pending State:
  - Title: Cannot edit in Phase 1 (must delete and recreate)
  - Due Date: Cannot edit in Phase 1
  - Priority: Cannot edit in Phase 1
  - Status: Can change to completed
  - Delete: Allowed

Completed State:
  - Title: Cannot edit (not applicable, task is done)
  - Due Date: Cannot edit (due date no longer relevant)
  - Priority: Cannot edit (priority no longer relevant)
  - Status: Cannot change back to pending (Phase 1 restriction)
  - Delete: Allowed
  - Rationale: Phase 1 MVP doesn't support editing; Phase II will add edit capability

---

Feature: Listing

Pending State:
  - Shown by default when user runs "todo list"
  - Shown when user runs "todo list --filter pending"
  - Typically shown first (before completed in "all" view)

Completed State:
  - Not shown by default (must explicitly ask for completed)
  - Shown when user runs "todo list --filter completed"
  - Shown at end when user runs "todo list --filter all"

---

Feature: Search

Both States:
  - Search includes both pending and completed tasks (by default)
  - User can search only pending: "todo search 'keyword' --filter pending"
  - User can search only completed: "todo search 'keyword' --filter completed"
```

---

### Step 6: Plan State Machine Evolution
Document how state machine changes across phases.

**Phase Evolution of State Machine**:

```
Phase 1 (Current):
  States: pending, completed
  Transitions:
    pending → completed: YES (one-way)
    completed → pending: NO (forbidden)
  Delete: Permanent (no recovery)
  Reversibility: None (one-way streets)

Phase II (Web App):
  New States: in_progress (user can mark task as "working on it")
  New Transitions:
    pending ↔ in_progress: YES (bidirectional)
    in_progress ↔ completed: YES (bidirectional)
    pending ↔ completed: YES (can skip in_progress)
  Delete: Soft delete (moved to trash, recoverable for 30 days)
  Reversibility: Full (can undo any transition)

  Migration Strategy:
    - Phase 1 pending tasks → Phase II pending tasks (unchanged)
    - Phase 1 completed tasks → Phase II completed tasks (unchanged)
    - Add in_progress state for Phase II users (old tasks don't use it)

Phase III (AI Chatbot):
  New States: regenerated (recurring task spawned new instance)
  New Transitions:
    completed → regenerated: YES (recurring task auto-generates next instance)
  Workflow:
    - Recurring task template exists
    - When completed, triggers auto-generation
    - New task created in pending state
    - Template marked as regenerated (for tracking)

  State Details:
    regenerated:
      - Task was completed
      - Recurring template caused new instance to spawn
      - Original task status → completed, but marked as regenerated for UI
      - New task appears as pending task (user sees it as new work)

  Example:
    - "Daily standup" recurring task due 2026-01-10
    - User completes on 2026-01-10 → status = completed
    - Auto-generation triggers → creates new "Daily standup" task due 2026-01-11
    - Old task status = regenerated (for history/audit)
    - New task status = pending (user sees as new task)

Phase IV (Kubernetes):
  No major state changes
  New dimension: synced state (task replicated to other regions)
  Doesn't change local state machine, just adds metadata

Phase V (Cloud + Advanced):
  New States: delegated (assigned to teammate), waiting_on (blocked/depends on other task)
  Collaborative workflow:
    - pending → delegated: User assigns task to teammate
    - pending → waiting_on: User marks as blocked (waiting for dependency)
    - waiting_on → pending: Dependency resolved, task is unblocked
  Full Matrix Becomes Possible (via Phase V):
    Any State → Any State (if user explicitly moves it)

State Machine Stability:
  - Phase 1-5 always maintain pending and completed
  - Never remove these states (backward compatibility)
  - Only add new states in each phase
  - Old tasks still work in new phases (Phase 1 pending task works in Phase V)
```

---

### Step 7: Validate State Machine
Ensure state machine is correct and complete.

**State Machine Validation Checklist**:

```
✅ State Definition
  [ ] Every state has clear definition (what it means)
  [ ] Every state has entry condition (how to reach it)
  [ ] Every state has exit conditions (how to leave it)
  [ ] Every state has duration (roughly how long task stays)

✅ Transitions
  [ ] All allowed transitions documented
  [ ] All forbidden transitions documented
  [ ] Each transition has trigger (what causes it)
  [ ] Each transition has preconditions (what must be true)
  [ ] Each transition has postconditions (what becomes true)

✅ Completeness
  [ ] Every state reachable from initial state
  [ ] Every state has exit path (can delete from any state)
  [ ] No dead-end states (except delete, which is final)
  [ ] No unreachable states (all states useful)

✅ Consistency
  [ ] Transitions match business rules (SM-* rules enforced)
  [ ] Error messages for forbidden transitions documented
  [ ] No conflicting transitions defined
  [ ] Symmetry correct (if A→B defined, is B←A forbidden correctly?)

✅ Correctness
  [ ] Task cannot reach invalid state
  [ ] State transitions are deterministic (same input = same output)
  [ ] Immutable fields respected (created_timestamp, completed_timestamp)
  [ ] Delete path works from all states

✅ User Understanding
  [ ] State names are understandable (not technical jargon)
  [ ] Transitions match user expectations
  [ ] Error messages explain why transition forbidden
  [ ] Help text describes state machine

✅ Edge Cases
  [ ] First task (creation works)
  [ ] Last task (deletion works)
  [ ] Rapid state changes (can user spam complete button?)
  [ ] Delete immediately after create (works)
  [ ] Complete immediately after create (works)

✅ Phase Transitions
  [ ] Phase 1 tasks work in Phase 2
  [ ] No data loss during phase migration
  [ ] New states don't break old code
  [ ] Reversibility plan clear for each phase
```

---

## Output

**Format**: Structured Markdown document with state machine specification:

```markdown
# Task State Management and Transitions

## State Universe
[All possible states per phase]

## Phase 1 State Machine
[States, transitions, initial state]

## State Definitions
[Detailed definition for each state]

## Transition Rules
[What happens during each transition]

## Forbidden Transitions
[What cannot happen and why]

## State-Dependent Behavior
[How features behave differently in each state]

## State Machine Evolution
[How states change across phases 1-5]

## Validation Checklist
[Ensuring correct, complete state machine]
```

---

## Failure Handling

### Scenario 1: Task Reaches Invalid State
**Symptom**: Task has status="unknown" (not pending or completed)
**Resolution**:
- Prevent by validating all state assignments: "status MUST be in {pending, completed}"
- Code review catches: "Assigning status without checking enum"
- Fix: Add validation before any state change

### Scenario 2: Transition Happens Without Permission
**Symptom**: User completes a task that's already completed
**Resolution**:
- Precondition check catches: "IF status ≠ pending THEN error"
- Error shown: "✗ Error: Task already completed"
- Prevention: Every transition checks preconditions

### Scenario 3: Completed Timestamp Gets Cleared
**Symptom**: Task marked complete, then timestamp cleared
**Resolution**:
- completed_timestamp is immutable: "Once set, never cleared"
- Code review enforces: "completed_timestamp can only be set once"
- Test verifies: "Reverting task to pending doesn't clear timestamp"

### Scenario 4: Phase II Reversal Not Planned
**Symptom**: Phase II added "revert to pending" but no state for intermediate state
**Resolution**:
- Plan ahead: Document completed → pending transition in Phase 2 design
- Ensure state machine supports it: "Phase II adds pending ↔ in_progress transitions"
- Migration: Phase 1 completed tasks stay completed until user explicitly reverts

### Scenario 5: Delete Path Missing from State
**Symptom**: Completed task cannot be deleted (delete only works in pending)
**Resolution**:
- Ensure delete path from all states: "Delete allowed from any state"
- Test: "Can delete pending task AND completed task"
- No state is trapped (all states have exit path)

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Implementation**: Code validates all state transitions
- **Testing**: Test cases verify valid/invalid transitions
- **Documentation**: State machine serves as spec
- **Phase evolution**: Shows how states change between phases
- **Debugging**: State machine helps identify impossible states
- **Collaboration**: Team understands consistent state model

---

## Success Metrics

- ✅ All states defined and named clearly
- ✅ All allowed transitions documented with preconditions/postconditions
- ✅ All forbidden transitions documented with reason
- ✅ Initial state defined (pending for new tasks)
- ✅ Exit paths defined for all states (delete from any)
- ✅ No dead-end states (except delete, which is final)
- ✅ Error messages for forbidden transitions clear
- ✅ State-dependent behavior documented per feature
- ✅ Phase evolution planned (states in 1-5)
- ✅ Immutable fields (created_timestamp, completed_timestamp) protected

---

## Related Skills

- **Business Rules (BLE-002)**: State machine rules (SM-*) define transitions
- **Algorithms (BLE-001)**: Algorithms implement transitions
- **Edge Cases (QA-001)**: Tests verify all transition cases
- **Acceptance Criteria (PA-001)**: Tests verify state machine works

---

## Example: Complete State Scenario

### Scenario: Complete Task, Then Try to Complete Again

**Initial State**: Task task-001 is pending

**Step 1: Complete Task (First Time)**
```
Command: todo complete task-001

Check Preconditions:
  - Task exists? YES
  - Task.status = pending? YES
  ✓ Preconditions met → proceed

Transition:
  status: pending → completed
  completed_timestamp: null → 2026-01-15T10:30:00Z

Output:
  ✓ Task marked complete: task-001 'Buy groceries'

Post-Conditions:
  - Task.status = completed
  - Task.completed_timestamp = 2026-01-15T10:30:00Z (immutable)
  - Task no longer appears in pending filters
  - Task appears in completed filters
```

**Step 2: Complete Task (Second Time)**
```
Command: todo complete task-001 (same task)

Check Preconditions:
  - Task exists? YES
  - Task.status = pending? NO (it's completed)
  ✗ Preconditions NOT met → reject

Output:
  ✗ Error: Task already completed: task-001 'Buy groceries'

Post-Conditions:
  - Task state UNCHANGED (still completed)
  - completed_timestamp UNCHANGED (remains immutable)
  - Error displayed, no operation performed

User Experience:
  User understands: Cannot complete task twice
  Clear error message: Knows exact problem and affected task
```

---

### Scenario: Delete Completed Task

**Initial State**: Task task-002 is completed (from previous completion)

**Step 1: Delete Completed Task**
```
Command: todo delete task-002

Check Preconditions:
  - Task exists? YES
  - Task can be deleted? YES (can delete any state)
  ✓ Preconditions met → proceed

Show Confirmation:
  "Delete task-002 'Submit report' (completed on 2026-01-10)? This cannot be undone. (y/n) >"

User confirms: y

Transition:
  Task removed from list

Output:
  ✓ Task deleted: task-002 'Submit report' (was completed)

Post-Conditions:
  - Task removed from list
  - No longer retrievable by ID
  - Does not appear in any filters
  - Permanent (Phase 1 has no undo)
```

---

## Conclusion

Phase 1 task state machine is simple but correct:
- Two states: pending, completed
- One-way transition: pending → completed
- No reversibility (Phase II adds this)
- Delete path from any state
- All invalid transitions prevented with clear errors
- Immutable audit trail (created_timestamp, completed_timestamp)

State machine is the foundation for all task operations and ensures consistency.

