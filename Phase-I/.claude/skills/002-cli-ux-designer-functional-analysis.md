# Skill: CLI Functional Analysis and Decomposition

**Skill ID**: CLI-001
**Agent Owner**: cli-ux-designer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Perform functional analysis of CLI-based todo application features by decomposing each feature into inputs, processes, and outputs. This skill identifies dependencies between features and defines expected system behavior without prescribing implementation details or UI mechanics. The output is a structured breakdown that serves as the bridge between user stories (from requirements-analyst) and technical architecture (for data-model-designer and business-logic-engineer).

---

## When to Use

- **Feature decomposition**: Breaking down Phase 1 user stories (create task, list tasks, mark complete, delete task, filter/sort, search)
- **Dependency mapping**: Understanding which features must be implemented before others
- **CLI command design**: Designing command syntax and argument structures before implementation
- **Integration planning**: Identifying data flows and dependencies between subsystems
- **Acceptance testing**: Defining test scenarios based on functional inputs/outputs
- **Handoff to development**: Providing clear specification of what each feature must do

---

## Inputs

1. **User story** (text): A validated user story from requirements-analyst skill (e.g., "As a user, I want to create a task...")
2. **System context** (text, optional): Constraints or environment details (e.g., "in-memory storage", "console-only", "single-user")
3. **Related features** (list, optional): Names of other features this one may depend on or interact with
4. **Success criteria** (text, optional): Business requirements or acceptance criteria from spec

---

## Step-by-Step Process

### Step 1: Identify Feature Scope
- Define what constitutes a "feature" (should be atomic: one user story = one feature)
- Confirm feature is independent and testable in isolation
- Document any features it depends on (prerequisites)

**Example**:
- Feature: "Create Task"
- Depends on: None (foundational feature)
- Independent: Yes, can be tested without list/delete/complete

### Step 2: Extract and Document Inputs
Identify all information the system must accept from the user or external source.

**Input Categories**:
- **User-provided data**: Task title, due date, priority, description
- **System state**: Current list of tasks, app configuration
- **User commands**: Which command invokes this feature (e.g., `todo add`, `todo create`)

**Format**:
```
Input: <input_name>
  Type: <string/integer/date/enum/boolean>
  Source: <user_input/system_state/external>
  Constraints: <validation rules, ranges, required/optional>
  Example: <concrete example>
```

**Example for "Create Task"**:
```
Input: task_title
  Type: string
  Source: user_input
  Constraints: required, non-empty, max 255 characters, no leading/trailing whitespace
  Example: "Buy groceries"

Input: task_due_date (optional)
  Type: date (YYYY-MM-DD format)
  Source: user_input
  Constraints: optional, must be valid date, can be future or today
  Example: "2026-01-15"

Input: task_priority (optional)
  Type: enum {low, normal, high}
  Source: user_input
  Constraints: optional, defaults to "normal"
  Example: "high"
```

### Step 3: Define Processing Logic
Describe what the system does with the inputs to produce outputs. Focus on WHAT happens, not HOW (no code, no algorithms).

**Processing Components**:
- **Validation**: Check input constraints
- **Transformation**: Convert or normalize data
- **Storage/Retrieval**: Persist or fetch data
- **Business rules**: Apply rules defined by business-logic-engineer
- **State management**: Update system state

**Format**:
```
Process: <process_name>
  Input: <which inputs are used>
  Steps:
    1. [What happens first]
    2. [What happens next]
    3. [Conditional branching if applicable]
  Business Rules Applied: <references to business rules>
  Side Effects: <what state changes occur>
  Output: <what is produced>
```

**Example for "Create Task"**:
```
Process: Validate Task Input
  Input: task_title, task_due_date (optional), task_priority (optional)
  Steps:
    1. Check if task_title is provided (non-empty string)
    2. If not provided, stop and return error
    3. If provided, trim whitespace and check length (max 255 chars)
    4. If due_date is provided, parse and validate date format (YYYY-MM-DD)
    5. If date is invalid, return error with suggestion
    6. If priority is provided, validate it's in {low, normal, high}
  Business Rules Applied: BR-VALIDATE-TITLE, BR-VALIDATE-DATE
  Side Effects: None (validation only)
  Output: Validated input object OR error message

Process: Create New Task Object
  Input: validated task_title, validated task_due_date, validated task_priority
  Steps:
    1. Generate unique task ID
    2. Set creation timestamp to current time
    3. Set task status to "pending" (default state)
    4. Assemble task object with all attributes
  Business Rules Applied: BR-TASK-ID-UNIQUENESS, BR-DEFAULT-STATUS
  Side Effects: None (data not yet persisted)
  Output: Task object ready for storage

Process: Store Task
  Input: Task object
  Steps:
    1. Add task to in-memory task list
    2. Return success confirmation
  Business Rules Applied: None
  Side Effects: In-memory task list is updated; task is now retrievable
  Output: Confirmation message with task details (ID, title, created timestamp)
```

### Step 4: Define Outputs
Specify what information the system returns to the user or to other features.

**Output Types**:
- **Success output**: What the user sees when feature executes successfully
- **Error output**: What the user sees when something fails
- **System state output**: How the system's internal state changes

**Format**:
```
Output: <output_name>
  Type: <message/data_object/status_code>
  Recipient: <user_console/other_feature/system_state>
  Content: <what information is included>
  Format: <how is it formatted for display>
  Example: <concrete example>
```

**Example for "Create Task"**:
```
Output: Success Message
  Type: message
  Recipient: user_console
  Content: Task ID, title, creation timestamp, optional due date
  Format: Human-readable text, e.g., "✓ Task created: [ID] 'Buy groceries' (due: 2026-01-15)"
  Example: "✓ Task created: task-001 'Buy groceries' (due: 2026-01-15)"

Output: Error Message (Title Empty)
  Type: message
  Recipient: user_console
  Content: Error description and guidance
  Format: "✗ Error: Task title cannot be empty. Please provide a task title."
  Example: "✗ Error: Task title cannot be empty. Please provide a task title."

Output: Error Message (Invalid Date)
  Type: message
  Recipient: user_console
  Content: Error description, provided value, expected format
  Format: "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"
  Example: "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"

Output: Updated Task List (Internal State)
  Type: data_object
  Recipient: system_state (used by list, filter, delete features)
  Content: In-memory list of all tasks including newly created task
  Format: List of task objects
  Example: [task-001, task-002, task-003 (new)]
```

### Step 5: Identify Feature Dependencies
Map which features must exist or run before this feature can function.

**Dependency Types**:
- **Data dependencies**: Feature A needs data produced by Feature B
- **Prerequisite dependencies**: Feature B must be implemented before Feature A
- **Optional dependencies**: Feature A works independently but has enhanced behavior if Feature B exists

**Format**:
```
Dependencies:
  Hard Dependencies (must exist):
    - <feature_name>: <reason/what data or state is required>
  Soft Dependencies (optional):
    - <feature_name>: <what enhanced behavior is provided>
```

**Example for "Create Task"**:
```
Dependencies:
  Hard Dependencies (must exist):
    - None (foundational feature)
  Soft Dependencies (optional):
    - List Tasks: If list feature exists, user can verify new task was created
    - Search Tasks: If search exists, user can find newly created task by title
```

**Example for "Delete Task"**:
```
Dependencies:
  Hard Dependencies (must exist):
    - Create Task: Need existing tasks to delete
    - List Tasks: User must be able to identify which task to delete
  Soft Dependencies (optional):
    - Search Tasks: User can search before deleting
    - Mark Complete: User might want to complete before deleting
```

### Step 6: Define System Behavior Specifications
Document how the system behaves across different scenarios (happy path, error conditions, edge cases).

**Behavior Specification Format**:
```
Scenario: <scenario_name>
  Context: <what state the system is in>
  User Action: <what the user does>
  System Behavior: <what the system does>
  Output: <what the user sees>
  Post-Condition: <what state the system is in after>
```

**Example for "Create Task"**:
```
Scenario: Create Task - Happy Path
  Context: User is in main menu, no existing tasks
  User Action: Enter "add" command and provide title "Buy milk"
  System Behavior:
    1. Validates title (non-empty, valid length)
    2. Creates new task with ID task-001
    3. Sets status to pending
    4. Stores in task list
    5. Displays success confirmation
  Output: "✓ Task created: task-001 'Buy milk'"
  Post-Condition: Task is now retrievable via list command

Scenario: Create Task - Empty Title
  Context: User is in main menu
  User Action: Enter "add" command with no title or empty string ""
  System Behavior:
    1. Detects empty/missing title
    2. Rejects input
    3. Displays error message
    4. Returns to input prompt
  Output: "✗ Error: Task title cannot be empty"
  Post-Condition: No task is created; system state unchanged

Scenario: Create Task - Title Too Long
  Context: User is in main menu
  User Action: Enter "add" command with title of 300 characters
  System Behavior:
    1. Validates title length (max 255)
    2. Rejects input exceeding limit
    3. Displays error with character count
  Output: "✗ Error: Task title too long (300 chars). Max allowed: 255"
  Post-Condition: No task is created; system state unchanged

Scenario: Create Task - With Optional Due Date
  Context: User is in main menu
  User Action: Enter "add" command with title "Submit report" and due date "2026-01-10"
  System Behavior:
    1. Validates title
    2. Parses and validates date format
    3. Creates task with title and due_date
    4. Stores in task list
  Output: "✓ Task created: task-003 'Submit report' (due: 2026-01-10)"
  Post-Condition: Task stored with due date; retrievable via list
```

### Step 7: Validate Functional Completeness
Ensure the functional analysis covers all aspects without implementation assumptions.

**Validation Checklist**:
- ✅ All inputs documented with type, source, constraints
- ✅ All processing steps describe WHAT, not HOW
- ✅ All outputs documented with type, recipient, format
- ✅ Dependencies clearly identified (hard vs. soft)
- ✅ At least 3 behavior scenarios defined (happy path, error, edge case)
- ✅ No technical implementation details (no code, no algorithm names, no data structure specifics)
- ✅ No UI assumptions beyond "CLI input/output"
- ✅ Testable: Could QA write test cases from this spec? Yes → complete

---

## Output

**Format**: Structured Markdown document with sections per feature:

```markdown
# Feature: <Feature Name>

## Overview
<One sentence: what does this feature do from user perspective>

## Inputs
<List of all inputs with type, source, constraints, examples>

## Processing
<Sequence of processing steps for each process>

## Outputs
<Success, error, and state outputs>

## Dependencies
<Hard and soft dependencies on other features>

## Behavior Specifications
<Scenarios: happy path, error conditions, edge cases>

## Related Features
<List of features that interact with or depend on this one>
```

---

## Failure Handling

### Scenario 1: Feature Description Lacks Detail
**Symptom**: User story is vague (e.g., "manage tasks")
**Resolution**:
- Ask clarifying questions: "Which specific action? Create? Update? Delete?"
- Request the original user story from requirements-analyst
- Break vague feature into smaller, testable features

### Scenario 2: Functional Analysis Contains Implementation Details
**Symptom**: Inputs mention "database", outputs mention "API response", processes mention "hashing"
**Resolution**:
- Rewrite from functional perspective (ignore HOW)
- Example: "Store in database" → "Task is now retrievable by ID"
- Example: "Return JSON API response" → "System confirms task creation with task details"
- Remove technical terminology; use business/user language

### Scenario 3: Circular Dependencies Detected
**Symptom**: Feature A depends on B, B depends on A
**Resolution**:
- This indicates a design issue or missing feature
- Suggest decomposing features differently
- Example: Instead of "Create and immediately delete task", split into separate features
- Ask: "Which feature is truly foundational?"

### Scenario 4: Missing Error Scenarios
**Symptom**: Behavior specs only cover happy path
**Resolution**:
- Identify common failure modes:
  - Invalid input (empty, format, constraints)
  - Resource exhaustion (too many tasks)
  - State conflicts (delete already-deleted task)
  - User cancellation
- Add at least one error scenario for each input type

### Scenario 5: Outputs are Too Technical
**Symptom**: Outputs mention "status codes", "JSON", "database records"
**Resolution**:
- Translate to user-visible outputs
- Example: "HTTP 201 Created" → "✓ Task created successfully"
- Example: "Database record inserted" → "Task is now in the task list"
- Focus on what user sees and can act on

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **All Phase 1 features**: Create, list, delete, mark complete, filter, search, edit
- **Dependency mapping**: Apply same process to identify feature ordering
- **Requirement validation**: Can be re-applied when requirements change
- **Handoff to architects**: Functional specs output by this skill drive data model design and business logic definition
- **Test case generation**: QA can derive test scenarios directly from behavior specifications

---

## Success Metrics

- ✅ All inputs fully documented (type, source, constraints, examples)
- ✅ All processing steps are functional (WHAT), not technical (HOW)
- ✅ All outputs are user-visible or system-state changes
- ✅ Dependencies clearly mapped (hard vs. soft)
- ✅ At least 3 behavior scenarios documented per feature
- ✅ No implementation details (code, algorithms, frameworks)
- ✅ No UI assumptions beyond "CLI input/output"
- ✅ Testable: Could a QA engineer write test cases? Yes

---

## Related Skills

- **Requirements-Analyst (RA-001)**: Produces user stories that feed into this skill
- **Business-Logic-Engineer**: Defines business rules referenced in processing steps
- **Data-Model-Designer**: Uses functional analysis to design data structures
- **CLI-UX-Designer (other skills)**: Uses this analysis to design command syntax and help text

---

## Example: Phase 1 Feature Analysis

### Feature: Create Task

#### Overview
User can create a new task by providing a title and optional due date and priority level.

#### Inputs

```
Input: task_title
  Type: string
  Source: user_input (command argument or interactive prompt)
  Constraints: required, non-empty, max 255 characters, no leading/trailing whitespace
  Example: "Buy groceries"

Input: task_due_date
  Type: date
  Source: user_input (optional flag or interactive prompt)
  Constraints: optional, format YYYY-MM-DD, must be a valid date (not past)
  Example: "2026-01-15"

Input: task_priority
  Type: enum
  Source: user_input (optional flag)
  Constraints: optional, values: {low, normal, high}, defaults to "normal"
  Example: "high"
```

#### Processing

```
Process: Validate Inputs
  Input: task_title, task_due_date (optional), task_priority (optional)
  Steps:
    1. Check task_title is provided
    2. If missing, return error "Task title is required"
    3. Strip leading/trailing whitespace from title
    4. Check length is between 1 and 255 characters
    5. If too long, return error with character count
    6. If task_due_date provided, parse and validate YYYY-MM-DD format
    7. If invalid, return error "Invalid date format"
    8. If task_priority provided, validate against {low, normal, high}
    9. If invalid, return error "Invalid priority"
  Business Rules Applied: BR-TITLE-REQUIRED, BR-TITLE-LENGTH, BR-DATE-FORMAT
  Side Effects: None
  Output: Validation result (pass/fail with error details)

Process: Generate Task
  Input: validated task_title, validated task_due_date, validated task_priority
  Steps:
    1. Generate unique task ID (e.g., task-001, task-002)
    2. Set creation_timestamp to current date/time
    3. Set status to "pending"
    4. Assemble task object
  Business Rules Applied: BR-UNIQUE-ID, BR-DEFAULT-STATUS
  Side Effects: None (in-memory only, not yet persisted)
  Output: Task object

Process: Store Task
  Input: Task object
  Steps:
    1. Add to in-memory task list
    2. Return success
  Side Effects: Task list updated
  Output: Stored task with all details

Process: Notify User
  Input: Stored task object
  Steps:
    1. Format task details for display
    2. Send success message to console
  Output: Confirmation message
```

#### Outputs

```
Output: Task Creation Success
  Type: confirmation message
  Recipient: user console
  Content: Task ID, title, due date (if set), priority (if non-default)
  Format: "✓ Task created: [ID] '[TITLE]'" with optional details
  Example: "✓ Task created: task-001 'Buy groceries' (due: 2026-01-15, priority: high)"

Output: Validation Error - Empty Title
  Type: error message
  Recipient: user console
  Format: "✗ Error: Task title cannot be empty"

Output: Validation Error - Title Too Long
  Type: error message
  Recipient: user console
  Format: "✗ Error: Task title too long (chars). Max: 255"

Output: Validation Error - Invalid Date
  Type: error message
  Recipient: user console
  Format: "✗ Error: Invalid date format. Expected YYYY-MM-DD"

Output: Updated Task State
  Type: system state
  Recipient: internal (list, search, filter, delete features)
  Content: In-memory list of all tasks (including new task)
  Format: Task list data structure
```

#### Dependencies

```
Hard Dependencies:
  - None (foundational feature)

Soft Dependencies:
  - List Tasks: User can verify new task was created
  - Search Tasks: User can find task by title
  - View Task Details: User can see full task information
```

#### Behavior Specifications

```
Scenario: Create Task - Happy Path
  Context: App is running, task list is empty
  User Action: Enter "todo add 'Buy milk'"
  System Behavior:
    1. Parse command and extract title
    2. Validate title (non-empty, valid length)
    3. Create task object with ID task-001, status pending
    4. Store in task list
    5. Display success confirmation
  Output: "✓ Task created: task-001 'Buy milk'"
  Post-Condition: Task-001 is in task list and retrievable

Scenario: Create Task - With Due Date
  Context: App is running
  User Action: Enter "todo add 'Submit report' --due 2026-01-10"
  System Behavior:
    1. Parse command, extract title and due date
    2. Validate title
    3. Parse and validate date (2026-01-10)
    4. Create task with due date
    5. Store and confirm
  Output: "✓ Task created: task-002 'Submit report' (due: 2026-01-10)"
  Post-Condition: Task stored with due date

Scenario: Create Task - Empty Title Error
  Context: App is running
  User Action: Enter "todo add ''"
  System Behavior:
    1. Parse command
    2. Detect empty title
    3. Return error
    4. Prompt for input again
  Output: "✗ Error: Task title cannot be empty"
  Post-Condition: No task created; user can retry

Scenario: Create Task - Title Too Long
  Context: App is running
  User Action: Enter "todo add '[300-character string]'"
  System Behavior:
    1. Parse command
    2. Check length (300 chars > 255 max)
    3. Return error with count
  Output: "✗ Error: Task title too long (300 chars). Max: 255"
  Post-Condition: No task created

Scenario: Create Task - Invalid Date Format
  Context: App is running
  User Action: Enter "todo add 'Meeting' --due 01/10/2026"
  System Behavior:
    1. Parse command
    2. Try to parse due date
    3. Detect invalid format (MM/DD/YYYY instead of YYYY-MM-DD)
    4. Return error
  Output: "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/10/2026'"
  Post-Condition: No task created
```

#### Related Features
- List Tasks (user verifies creation)
- Search Tasks (user finds new task)
- Mark Complete (user completes task)
- Delete Task (user removes task)
- Filter Tasks (user organizes tasks)
