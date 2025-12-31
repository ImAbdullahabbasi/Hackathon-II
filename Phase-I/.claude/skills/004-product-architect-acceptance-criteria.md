# Skill: Acceptance Criteria Definition and Validation

**Skill ID**: PA-001
**Agent Owner**: product-architect
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Define clear, measurable, and testable acceptance criteria using GIVEN/WHEN/THEN format for each Phase 1 feature. This skill ensures that acceptance criteria are unambiguous, comprehensive, and directly verifiable by QA engineers. Acceptance criteria serve as the contract between product requirements and development implementation, preventing scope creep and ensuring alignment on definition of "done."

---

## When to Use

- **Feature specification phase**: After user stories (RA-001) and functional analysis (CLI-001) are complete
- **Definition of Done**: Establishing what must be true for a feature to be considered complete
- **QA test case generation**: Converting criteria into executable test cases
- **Code review validation**: Verifying implementation matches acceptance criteria
- **Requirement handoff**: Communicating expectations to development team
- **Dispute resolution**: Settling disagreements about whether feature is truly complete

---

## Inputs

1. **User story** (text): Validated user story from requirements-analyst (RA-001)
2. **Functional specification** (document): Detailed specification from cli-ux-designer (CLI-001)
3. **Edge cases** (list): Edge cases identified by quality-assurance (QA-001)
4. **Business rules** (optional): Rules from business-logic-engineer (BLE-001)
5. **Success metrics** (optional): Quantifiable success measures from product spec

---

## Step-by-Step Process

### Step 1: Decompose Feature into Testable Scenarios
Break the feature into distinct scenarios that cover all important user journeys and error conditions.

**Scenario Categories**:
- **Happy Path**: User performs the action successfully with valid inputs
- **Alternate Success Path**: User reaches success via different route (optional inputs, shortcuts)
- **Error Scenarios**: User provides invalid input, system state prevents action
- **Boundary Scenarios**: Edge cases at limits of functionality
- **Rollback/Recovery**: What happens after partial failure or cancellation

**Example Decomposition for "Create Task"**:
- Scenario 1: Create task with title only (minimal required inputs)
- Scenario 2: Create task with title, due date, and priority (all optional inputs)
- Scenario 3: Create task with empty title (error case)
- Scenario 4: Create task with title exceeding max length (boundary case)
- Scenario 5: User cancels task creation mid-way (rollback case)

### Step 2: Define GIVEN Context (Initial State)
For each scenario, document the state of the system BEFORE the user action.

**GIVEN Statement Guidelines**:
- Be specific about system state, not generic
- Include data state (e.g., "task list contains 3 tasks")
- Include configuration state (e.g., "in-memory storage enabled")
- Include user state (e.g., "user is logged in", "user has opened the app")
- Use concrete values, not variables

**Anti-Pattern (Vague)**:
```
GIVEN the system is ready
```

**Pattern (Specific)**:
```
GIVEN the task list is empty
AND the user is in the main menu
AND the app is in command input mode
```

**More Examples**:
```
GIVEN the task list contains 5 existing tasks (task-001 through task-005)
AND the app is awaiting user input

GIVEN a task with ID task-001 exists and has status "pending"
AND the user has opened the task detail view

GIVEN the task list is at maximum capacity (1000 tasks)
AND the user is in the create task menu
```

### Step 3: Define WHEN Action (User Behavior)
Describe exactly what the user does or what event triggers the scenario.

**WHEN Statement Guidelines**:
- Be precise about command syntax and arguments
- Include exact input values from user
- Be specific about action (not "user interacts" but "user enters command")
- Use exact command/button/menu names as they appear to user
- Include timing if relevant (e.g., "user presses Escape immediately")

**Anti-Pattern (Vague)**:
```
WHEN the user creates a task
```

**Pattern (Specific)**:
```
WHEN the user enters the command "todo add 'Buy groceries' --due 2026-01-15 --priority high"
AND presses Enter
```

**More Examples**:
```
WHEN the user enters the command "todo add ''" (empty string title)
AND presses Enter

WHEN the user enters the command "todo delete task-001"
AND confirms the deletion prompt

WHEN the user enters the command "todo list --filter completed"
AND the task list contains 3 completed tasks
```

### Step 4: Define THEN Outcomes (Expected Results)
Specify what the system should do and what the user should see.

**THEN Statement Guidelines**:
- Be specific about observable outcomes (console output, system state change)
- Include success message content or error message text
- Specify data changes (what is added/updated/deleted)
- Specify UI state (what menu/screen user sees after)
- Make outcomes measurable and verifiable
- Separate multiple outcomes with AND

**Anti-Pattern (Vague)**:
```
THEN the task is created
```

**Pattern (Specific)**:
```
THEN a new task is created with:
  - ID: task-006 (next sequential ID)
  - Title: "Buy groceries"
  - Due Date: 2026-01-15
  - Priority: high
  - Status: pending
  - Created Timestamp: current date/time
AND the console displays: "✓ Task created: task-006 'Buy groceries' (due: 2026-01-15, priority: high)"
AND the task appears in the task list immediately
AND the user is returned to the main menu
```

**More Examples**:
```
THEN the console displays the error message: "✗ Error: Task title cannot be empty"
AND no task is created
AND the user is returned to the input prompt
AND the task list remains unchanged

THEN the console displays: "✓ Task deleted: task-001 'Buy groceries'"
AND task-001 is removed from the task list
AND the task list now contains 4 tasks
AND the user is returned to the main menu
```

### Step 5: Add Verification Steps (How QA Verifies)
Append concrete verification instructions so QA knows exactly how to test.

**Verification Step Format**:
```
**Verification Steps**:
1. [Action] - [What to check/observe]
2. [Action] - [What to check/observe]
3. [Action] - [Expected result]
```

**Example**:
```
**Verification Steps**:
1. Run "todo add 'Buy groceries' --due 2026-01-15 --priority high"
   - Check console output contains: "✓ Task created: task-006"
2. Run "todo list"
   - Check output includes the new task with correct ID, title, due date, priority
3. Restart the app (to verify in-memory state is preserved)
   - Check task-006 is still in the list (or confirm it's lost, if that's expected behavior)
4. Run "todo list --filter pending"
   - Check task-006 appears in filtered results
```

### Step 6: Identify Acceptance Thresholds (Pass/Fail Criteria)
Define what constitutes "pass" vs. "fail" for each criterion.

**Pass/Fail Format**:
```
**PASS Criteria**:
- [ ] Task created with exact ID, title, due date, priority as provided
- [ ] Success message displayed with correct task details
- [ ] Task immediately appears in task list
- [ ] Task is retrievable by ID or in filtered lists

**FAIL Criteria**:
- [ ] Task created with different/missing attributes
- [ ] Task ID is wrong or not sequential
- [ ] Success message is missing or incorrect
- [ ] Task does not appear in task list
- [ ] Error message is unclear or contradicts action
```

### Step 7: Account for Boundary and Error Cases
Ensure acceptance criteria cover not just happy path but error scenarios and edge cases.

**Error Acceptance Criteria Examples**:

```
Scenario: Create Task - Empty Title
GIVEN the task list is empty
AND the user is in the main menu

WHEN the user enters "todo add ''" (empty title)

THEN the console displays: "✗ Error: Task title cannot be empty. Please provide a task title."
AND no task is created
AND the task list remains empty
AND the user is returned to the input prompt
AND the app does not crash or hang

PASS Criteria:
- [ ] Exact error message displayed
- [ ] No task created (list size unchanged)
- [ ] User can retry with valid input
```

```
Scenario: Create Task - Invalid Date Format
GIVEN the user is in the create task menu

WHEN the user enters "todo add 'Meeting' --due 01/15/2026" (MM/DD/YYYY instead of YYYY-MM-DD)

THEN the console displays: "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"
AND no task is created
AND the user is prompted to retry with correct format

PASS Criteria:
- [ ] Error message clearly states expected format
- [ ] Error message echoes back the incorrect input user provided
- [ ] No task created with invalid date
```

### Step 8: Validate Acceptance Criteria Completeness
Ensure criteria are comprehensive, measurable, and free of ambiguity.

**Validation Checklist**:
- ✅ Every criterion uses GIVEN/WHEN/THEN format
- ✅ GIVEN specifies concrete initial state (not vague)
- ✅ WHEN describes specific user action (not generic)
- ✅ THEN lists observable outcomes (not assumptions)
- ✅ At least 3 scenarios per feature (happy path + 2 error cases minimum)
- ✅ All edge cases from QA-001 have corresponding criteria
- ✅ All error messages are documented word-for-word
- ✅ All data state changes are explicit (e.g., "task list now contains 6 tasks")
- ✅ Verification steps are concrete and executable
- ✅ Pass/Fail criteria are unambiguous (no "should", "may", "might")
- ✅ Measurable: Could an automated test verify this? Yes → good criteria

**Red Flags (Signs of Poor Criteria)**:
- "User sees the task" (ambiguous — where? how? what format?)
- "System handles the request" (vague — handles how?)
- "Error is displayed" (what error message exactly?)
- "Task is created correctly" (what does "correctly" mean?)
- Use of modal verbs: "should", "may", "might", "could"

---

## Output

**Format**: Structured Markdown document organized by feature, with acceptance criteria grouped by scenario:

```markdown
# Acceptance Criteria: [Feature Name]

## Scenario 1: [Happy Path Title]

**GIVEN**: [Initial system state and user context]

**WHEN**: [User action or event]

**THEN**: [Observable outcomes]

**Verification Steps**:
1. [How to test]
2. [What to verify]

**PASS Criteria**:
- [ ] [Specific verifiable criterion]
- [ ] [Specific verifiable criterion]

**FAIL Criteria**:
- [ ] [Specific failure condition]

---

## Scenario 2: [Error Case Title]

[Same structure as Scenario 1]

---

## Summary
- Total scenarios: [N]
- Happy path scenarios: [N]
- Error scenarios: [N]
- Boundary scenarios: [N]
```

---

## Failure Handling

### Scenario 1: Criteria Too Vague to Test
**Symptom**: Criteria says "Task is created" without specifying what "created" means (ID? Title? Timestamp?)
**Resolution**:
- Add specific attributes: "Task created with ID task-006, title 'Buy groceries', status 'pending', timestamp 2025-12-30T10:30:00"
- Add exact observable output: "Console displays: '✓ Task created: task-006 'Buy groceries''"
- Add verification method: "User can retrieve task by running 'todo get task-006'"

### Scenario 2: Criteria Missing Error Cases
**Symptom**: Acceptance criteria only cover happy path; no validation error scenarios
**Resolution**:
- Add scenarios for each invalid input from functional spec (CLI-001)
- Add scenarios for each error case from edge case analysis (QA-001)
- Ensure error message text is documented exactly
- Include "no data changed" verification for error cases

### Scenario 3: Criteria References Non-Existent Feature State
**Symptom**: Criteria says "user is on the task detail page" but detail view doesn't exist in Phase 1
**Resolution**:
- Verify feature scope against spec; if feature doesn't exist in Phase 1, remove criterion
- If criterion implies missing feature, escalate to requirements-analyst or product-architect
- Mark as "Phase II feature" if applicable

### Scenario 4: Circular Dependencies in Criteria
**Symptom**: "Feature A acceptance depends on Feature B" but Feature B acceptance depends on Feature A
**Resolution**:
- Identify which feature is foundational (can be tested independently)
- Separate into two acceptance criteria sets
- Example: "List Tasks" should work even if "Create Task" feature isn't tested; create both independently

### Scenario 5: Acceptance Criteria Conflict with Business Rules
**Symptom**: Criteria allows behavior (e.g., "create task with past due date") but business rules forbid it
**Resolution**:
- Escalate to business-logic-engineer for clarification
- Update business rules or acceptance criteria (not both)
- Document rationale for decision
- Example: "Business decision: Allow past due dates (phase II will add warnings)"

### Scenario 6: Acceptance Criteria Too Strict (Over-specification)
**Symptom**: Criteria specifies implementation details (e.g., "Task ID must be generated using UUID v4")
**Resolution**:
- Remove implementation details; focus on observable behavior
- Bad: "Task ID generated using UUID v4"
- Good: "Task ID is unique and never duplicates existing tasks"
- Keep criteria at functional level, not technical level

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **All Phase 1 features**: Create, list, delete, mark complete, filter, search, edit
- **Phase II web app features**: Same GIVEN/WHEN/THEN format applies to web UI
- **Requirement refinement**: Acceptance criteria reveal ambiguities in specs; help tighten requirements
- **Regression testing**: Criteria become the regression test suite across phases
- **QA handoff**: Output directly drives QA test case creation
- **Code review**: Developers verify their implementation matches acceptance criteria

---

## Success Metrics

- ✅ Every feature has at least 3 acceptance scenarios (happy path + 2 error cases minimum)
- ✅ Every scenario uses GIVEN/WHEN/THEN format explicitly
- ✅ Every criterion is measurable and testable (no vague language)
- ✅ Error scenarios include exact error message text (word-for-word)
- ✅ Data state changes are explicit (e.g., "task list contains 6 tasks" not "task list updated")
- ✅ Verification steps are concrete and executable (QA can follow and verify)
- ✅ Pass/Fail criteria unambiguous (testable by automated or manual QA)
- ✅ Scenarios cover happy path, error cases, boundary conditions, and user mistakes
- ✅ No implementation details (no mention of code, algorithms, frameworks)
- ✅ No circular dependencies (criteria can be tested independently)

---

## Related Skills

- **Requirements-Analyst (RA-001)**: Produces user stories that acceptance criteria implement
- **CLI-UX-Designer (CLI-001)**: Provides functional specification; criteria validate implementation
- **Quality-Assurance (QA-001)**: Identifies edge cases; each edge case gets acceptance criterion
- **Business-Logic-Engineer (BLE-001)**: Defines business rules that acceptance criteria enforce

---

## Example: Phase 1 Feature Acceptance Criteria

### Feature: Create Task

#### Scenario 1: Create Task - Happy Path (Title Only)

**GIVEN**:
- The task list is empty
- The user is in the main menu
- The app is in command input mode

**WHEN**:
- The user enters the command: `todo add 'Buy groceries'`
- The user presses Enter

**THEN**:
- A new task is created with the following attributes:
  - ID: `task-001` (first task, next sequential ID)
  - Title: `Buy groceries` (exactly as provided, trimmed)
  - Status: `pending` (default status)
  - Created Timestamp: current date and time (system time)
  - Due Date: none (optional, not provided)
  - Priority: `normal` (default priority)
- The console displays: `✓ Task created: task-001 'Buy groceries'`
- The task list now contains 1 task (previously empty, now contains new task)
- The user is returned to the main menu
- The app remains in command input mode

**Verification Steps**:
1. Start the app with empty task list
2. Run: `todo add 'Buy groceries'`
3. Verify console output contains: `✓ Task created: task-001 'Buy groceries'`
4. Run: `todo list`
5. Verify output includes task with ID `task-001`, title `Buy groceries`, status `pending`
6. Verify task count is 1
7. Verify no error messages appear
8. Verify app is ready for next command

**PASS Criteria**:
- [ ] New task created with sequential ID (task-001)
- [ ] Task title exactly matches user input (trimmed)
- [ ] Task status defaults to "pending"
- [ ] Success message displayed with correct task ID and title
- [ ] Task appears immediately in task list
- [ ] Task list count increases from 0 to 1
- [ ] No error message displayed
- [ ] User returned to main menu

**FAIL Criteria**:
- [ ] Task ID is not sequential (e.g., task-999)
- [ ] Task title is modified, truncated, or missing
- [ ] Task status is not "pending"
- [ ] Success message is missing or incorrect
- [ ] Task does not appear in task list
- [ ] Error message is displayed
- [ ] App crashes or hangs
- [ ] Task is created but not retrievable by ID

---

#### Scenario 2: Create Task - All Optional Inputs (Title + Due Date + Priority)

**GIVEN**:
- The task list contains 1 existing task (task-001)
- The user is in the main menu
- The system time is 2025-12-30 10:00:00 UTC

**WHEN**:
- The user enters the command: `todo add 'Submit report' --due 2026-01-15 --priority high`
- The user presses Enter

**THEN**:
- A new task is created with the following attributes:
  - ID: `task-002` (next sequential ID)
  - Title: `Submit report`
  - Status: `pending`
  - Created Timestamp: 2025-12-30 10:00:00 UTC (system time)
  - Due Date: `2026-01-15` (as provided)
  - Priority: `high` (as provided)
- The console displays: `✓ Task created: task-002 'Submit report' (due: 2026-01-15, priority: high)`
- The task list now contains 2 tasks
- The user is returned to the main menu

**Verification Steps**:
1. Verify task list contains 1 task (task-001)
2. Run: `todo add 'Submit report' --due 2026-01-15 --priority high`
3. Verify console output: `✓ Task created: task-002 'Submit report' (due: 2026-01-15, priority: high)`
4. Run: `todo list`
5. Verify output shows:
   - task-001 (first task)
   - task-002 (new task) with due date 2026-01-15 and priority high
6. Run: `todo get task-002`
7. Verify task details show all attributes correctly
8. Run: `todo list --filter high-priority`
9. Verify task-002 appears in high-priority filtered list
10. Run: `todo list --filter due-after 2026-01-10`
11. Verify task-002 appears in results (due date matches filter)

**PASS Criteria**:
- [ ] Task ID is sequential (task-002)
- [ ] Title is exactly "Submit report"
- [ ] Due date is stored as 2026-01-15
- [ ] Priority is stored as "high"
- [ ] Status defaults to "pending"
- [ ] Success message includes due date and priority
- [ ] Task appears in task list with all attributes
- [ ] Task is retrievable by ID with all details
- [ ] Task is filterable by priority and due date
- [ ] Task list count is now 2

**FAIL Criteria**:
- [ ] Task ID is not sequential
- [ ] Due date is not stored or is stored incorrectly
- [ ] Priority is not stored or is stored as default
- [ ] Success message is missing optional attributes
- [ ] Task is not filterable by the provided attributes
- [ ] Task count is not 2

---

#### Scenario 3: Create Task - Empty Title (Error Case)

**GIVEN**:
- The task list is empty
- The user is in the main menu
- The app is in command input mode

**WHEN**:
- The user enters the command: `todo add ''` (empty string title)
- The user presses Enter

**THEN**:
- No task is created
- The task list remains empty
- The console displays the error message: `✗ Error: Task title cannot be empty. Please provide a task title.`
- The user is returned to the input prompt (can retry)
- The app does not crash or hang
- The app is ready for next command

**Verification Steps**:
1. Start app with empty task list
2. Run: `todo add ''`
3. Verify console displays: `✗ Error: Task title cannot be empty. Please provide a task title.`
4. Run: `todo list`
5. Verify task list is still empty (no task created)
6. Verify task count is 0
7. Run: `todo add 'Valid task'` (retry with valid input)
8. Verify retry succeeds

**PASS Criteria**:
- [ ] Exact error message displayed
- [ ] No task created
- [ ] Task list count remains 0
- [ ] User can retry with valid input
- [ ] No app crash or hang

**FAIL Criteria**:
- [ ] No error message displayed
- [ ] Task created with empty title
- [ ] Error message is vague or unhelpful
- [ ] User cannot retry
- [ ] App crashes

---

#### Scenario 4: Create Task - Whitespace-Only Title (Error Case)

**GIVEN**:
- The task list is empty
- The user is in the main menu

**WHEN**:
- The user enters the command: `todo add '    '` (spaces only)
- The user presses Enter

**THEN**:
- The app detects that title is whitespace-only
- After trimming whitespace, title is empty
- The console displays: `✗ Error: Task title cannot be empty. Please provide a task title.`
- No task is created
- The task list remains empty
- The user can retry with valid input

**Verification Steps**:
1. Run: `todo add '    '`
2. Verify error message is displayed
3. Verify no task is created
4. Verify task list is empty

**PASS Criteria**:
- [ ] Whitespace-only input is rejected
- [ ] Error message is clear
- [ ] No task created

**FAIL Criteria**:
- [ ] Task created with whitespace-only title
- [ ] No error message displayed

---

#### Scenario 5: Create Task - Title Exceeds Max Length (Error Case)

**GIVEN**:
- The task list is empty
- The user is in the main menu
- Task title max length is 255 characters

**WHEN**:
- The user enters a command with a title of 300 characters: `todo add '[300-character string]'`
- The user presses Enter

**THEN**:
- The app detects that title exceeds 255 characters
- The console displays: `✗ Error: Task title too long (300 chars). Max allowed: 255`
- No task is created
- The task list remains empty
- The user can retry with shorter title

**Verification Steps**:
1. Generate 300-character string
2. Run: `todo add '[300-char string]'`
3. Verify error message includes character count (300 chars, max 255)
4. Verify no task is created

**PASS Criteria**:
- [ ] Error message displays actual and max character counts
- [ ] Title exceeding 255 chars is rejected
- [ ] Task count remains 0

**FAIL Criteria**:
- [ ] Task created with oversized title
- [ ] Error message does not include character count
- [ ] User cannot determine how many chars are too many

---

#### Scenario 6: Create Task - Invalid Date Format (Error Case)

**GIVEN**:
- The user is in the main menu
- Expected date format is YYYY-MM-DD

**WHEN**:
- The user enters: `todo add 'Meeting' --due 01/15/2026` (MM/DD/YYYY format instead of YYYY-MM-DD)
- The user presses Enter

**THEN**:
- The app attempts to parse the date
- The app detects that the format is invalid (01/15/2026 does not match YYYY-MM-DD)
- The console displays: `✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'`
- No task is created
- The user can retry with correct format

**Verification Steps**:
1. Run: `todo add 'Meeting' --due 01/15/2026`
2. Verify error message shows expected format (YYYY-MM-DD) and actual input (01/15/2026)
3. Verify no task created
4. Run: `todo add 'Meeting' --due 2026-01-15`
5. Verify retry succeeds with correct format

**PASS Criteria**:
- [ ] Error message clearly states expected format (YYYY-MM-DD)
- [ ] Error message echoes the incorrect input user provided
- [ ] No task created with invalid date
- [ ] User can retry with correct format
- [ ] Correct format is accepted

**FAIL Criteria**:
- [ ] Error message does not show expected format
- [ ] Task created with unparseable date
- [ ] No guidance on correct format

---

#### Scenario 7: Create Task - Title at Exact Boundary (255 Characters)

**GIVEN**:
- The task list is empty
- Task title max length is 255 characters

**WHEN**:
- The user enters a command with a title of exactly 255 characters: `todo add '[255-character string]'`
- The user presses Enter

**THEN**:
- The app validates title length (255 characters is at the maximum, allowed)
- Task is created successfully with all 255 characters
- The console displays: `✓ Task created: task-001 '[255-char title]'`
- The task list now contains the task
- The task title is stored and retrievable in full (no truncation)

**Verification Steps**:
1. Generate exactly 255-character string
2. Run: `todo add '[255-char string]'`
3. Verify success message displayed
4. Run: `todo get task-001`
5. Verify task title is exactly 255 characters (no truncation)

**PASS Criteria**:
- [ ] 255-character title is accepted
- [ ] Task created successfully
- [ ] Title is stored without truncation
- [ ] Title is fully retrievable

**FAIL Criteria**:
- [ ] 255-character title rejected as too long
- [ ] Title truncated to less than 255 chars
- [ ] Off-by-one error (reject at 255, allow at 256)

---

### Feature: Delete Task

#### Scenario 1: Delete Task - Happy Path

**GIVEN**:
- The task list contains 3 tasks:
  - task-001: 'Buy groceries' (pending)
  - task-002: 'Submit report' (pending)
  - task-003: 'Fix bug' (pending)
- The user is in the main menu

**WHEN**:
- The user enters the command: `todo delete task-002`
- The user presses Enter

**THEN**:
- Task task-002 is found in the task list
- Task task-002 is deleted from the task list
- The console displays: `✓ Task deleted: task-002 'Submit report'`
- The task list now contains 2 tasks (task-001 and task-003)
- task-002 is no longer retrievable
- The user is returned to the main menu

**Verification Steps**:
1. Verify task list contains 3 tasks
2. Run: `todo delete task-002`
3. Verify console displays: `✓ Task deleted: task-002 'Submit report'`
4. Run: `todo list`
5. Verify output shows only 2 tasks (task-001, task-003)
6. Verify task-002 does not appear
7. Run: `todo get task-002`
8. Verify error: task not found

**PASS Criteria**:
- [ ] Task is deleted by ID
- [ ] Deletion message includes task ID and title
- [ ] Task count decreases from 3 to 2
- [ ] Deleted task is not retrievable
- [ ] Other tasks remain unchanged

**FAIL Criteria**:
- [ ] Wrong task deleted
- [ ] No confirmation message
- [ ] Task count not updated
- [ ] Deleted task still appears in list

---

#### Scenario 2: Delete Task - Non-Existent Task ID (Error Case)

**GIVEN**:
- The task list contains 3 tasks (task-001, task-002, task-003)
- The user is in the main menu

**WHEN**:
- The user enters the command: `todo delete task-999`
- The user presses Enter

**THEN**:
- The app searches for task-999 in the task list
- The app does not find task-999 (does not exist)
- The console displays: `✗ Error: Task not found: task-999`
- The task list remains unchanged (all 3 tasks still present)
- The user is returned to the input prompt

**Verification Steps**:
1. Verify task list contains 3 tasks
2. Run: `todo delete task-999`
3. Verify error message: `✗ Error: Task not found: task-999`
4. Run: `todo list`
5. Verify task count still 3 (no deletion occurred)

**PASS Criteria**:
- [ ] Error message clearly states task was not found
- [ ] Error message includes the task ID that was not found
- [ ] No task deleted
- [ ] Task list count unchanged

**FAIL Criteria**:
- [ ] No error message displayed
- [ ] Task deleted anyway (wrong task)
- [ ] Task count changed

---

#### Scenario 3: Delete Task - Empty Task List (Error Case)

**GIVEN**:
- The task list is empty (no tasks)
- The user is in the main menu

**WHEN**:
- The user enters the command: `todo delete task-001`
- The user presses Enter

**THEN**:
- The app searches for task-001
- The app finds no tasks in the list
- The console displays: `✗ Error: Task not found: task-001` (or "No tasks exist")
- No deletion occurs
- The task list remains empty
- The user is returned to the input prompt

**Verification Steps**:
1. Verify task list is empty (0 tasks)
2. Run: `todo delete task-001`
3. Verify error message
4. Run: `todo list`
5. Verify task list still empty

**PASS Criteria**:
- [ ] Error message displayed when list is empty
- [ ] No task deleted
- [ ] Task count remains 0

**FAIL Criteria**:
- [ ] No error message
- [ ] App crashes when deleting from empty list

---

#### Scenario 4: Delete Task - Last Remaining Task

**GIVEN**:
- The task list contains 1 task (task-001)
- The user is in the main menu

**WHEN**:
- The user enters the command: `todo delete task-001`
- The user presses Enter

**THEN**:
- Task task-001 is deleted
- The console displays: `✓ Task deleted: task-001 '[title]'`
- The task list becomes empty
- Task count is now 0
- The user is returned to the main menu

**Verification Steps**:
1. Create 1 task, verify list contains 1
2. Run: `todo delete task-001`
3. Verify success message
4. Run: `todo list`
5. Verify output shows empty list (0 tasks)
6. Verify appropriate "no tasks" message or empty output

**PASS Criteria**:
- [ ] Task is deleted successfully
- [ ] Task list becomes empty after deletion
- [ ] Success message displayed
- [ ] App handles empty state correctly

**FAIL Criteria**:
- [ ] Task not deleted
- [ ] App crashes when list becomes empty
- [ ] Cannot create new task after list is empty

---

## Summary for All Features

**Total acceptance criteria scenarios**: 10 (7 for Create Task, 3 for Delete Task)
- **Happy path scenarios**: 2
- **Error scenarios**: 6
- **Boundary scenarios**: 2

**All scenarios follow GIVEN/WHEN/THEN format**
**All verification steps are concrete and executable**
**All PASS/FAIL criteria are measurable and unambiguous**

