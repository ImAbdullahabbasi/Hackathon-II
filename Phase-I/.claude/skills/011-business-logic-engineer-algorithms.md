# Skill: Business Logic and Algorithm Design

**Skill ID**: BLE-001
**Agent Owner**: business-logic-engineer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Define step-by-step business logic and algorithms for Phase 1 features (sorting, filtering, searching, task state transitions) in language-agnostic pseudocode. This skill focuses on correctness, clarity, and decision points without prescribing implementation language. The goal is to ensure all developers (Python, JavaScript, Go, etc.) implement the same logic consistently. Algorithms must be correct for edge cases, efficient for typical use (100-1000 tasks), and easy to verify against acceptance criteria.

---

## When to Use

- **Feature design phase**: After acceptance criteria (PA-001) are defined; before implementation
- **Code review**: Verifying implementation matches intended logic
- **Cross-platform implementation**: Ensuring Python, JavaScript, Go versions behave identically
- **Edge case analysis**: Identifying all decision points and branches
- **Performance analysis**: Determining algorithmic complexity and bottlenecks
- **Testing**: Deriving test cases from logical flow

---

## Inputs

1. **Acceptance criteria** (document): From PA-001, defining expected behavior
2. **Edge cases** (list): From QA-001, identifying corner cases
3. **Data model** (document): From DMD-001, structure of Task entity
4. **User stories** (list): From RA-001, describing what users expect

---

## Step-by-Step Process

### Step 1: Define Algorithm Structure
Create a consistent template for expressing algorithms.

**Algorithm Template**:

```
Algorithm: [NAME]
Purpose: [What this algorithm does in plain English]
Input: [What data is provided]
Output: [What result is produced]
Complexity: [Time and space complexity for Phase 1 scale]

Pre-Conditions:
  [What must be true before running]

Post-Conditions:
  [What must be true after running]

Steps:
  1. [Initial step]
  2. [Decision point: IF condition THEN ... ELSE ...]
  3. [Loop: FOR each item IN collection ...]
  4. [Comparison step]
  5. [Return result]

Special Cases:
  [Edge cases and how to handle]

Verification:
  [How to verify algorithm is correct]
```

---

### Step 2: Design Core Algorithms
Define algorithms for Phase 1 features.

**Algorithm 1: Create Task**

```
Algorithm: CreateTask
Purpose: Create a new task with given title and optional deadline/priority
Input:
  - task_title (string, required)
  - due_date (string in YYYY-MM-DD format, optional)
  - priority (enum: low/normal/high, optional, defaults to "normal")
Output:
  - new_task (Task object)
  - success_message (string confirmation)
Complexity:
  Time: O(1) constant time (single object creation)
  Space: O(1) constant space (one task object)

Pre-Conditions:
  - Application has initialized task list (empty or with existing tasks)
  - User has permission to create tasks

Post-Conditions:
  - New task added to task list
  - Task is retrievable by ID
  - New task appears in all list/filter operations

Steps:
  1. Validate Inputs
     a. IF task_title is empty OR null THEN
        RETURN error("Task title cannot be empty")
     b. Trim whitespace from task_title
     c. IF length(task_title) < 1 OR > 255 THEN
        RETURN error("Title must be 1-255 characters")
     d. IF due_date is provided THEN
        i. Parse due_date as YYYY-MM-DD
        ii. IF parse fails THEN
            RETURN error("Invalid date format. Expected YYYY-MM-DD")
        iii. Validate date exists (not Feb 30, etc.)
        iv. IF date invalid THEN
            RETURN error("Invalid date: <specific reason>")
     e. IF priority is provided AND priority NOT IN {low, normal, high} THEN
        RETURN error("Invalid priority. Allowed: low, normal, high")

  2. Generate Task ID
     a. existing_ids = get_all_task_ids()  # Get list of all current IDs
     b. max_id = find_maximum_numeric_id(existing_ids)
        # Extract numbers from IDs like "task-001", "task-025"
     c. new_id = format("task-{max_id + 1:03d}")  # Zero-padded to 3 digits
        # Example: task-001, task-002, ..., task-999
     d. IF new_id already exists (collision) THEN
        RETURN error("System error: ID generation failed")

  3. Create Task Object
     a. new_task = Task()
     b. new_task.id = new_id
     c. new_task.title = task_title (trimmed)
     d. new_task.status = "pending"  # Always start pending
     e. new_task.created_timestamp = current_time_utc()
     f. new_task.due_date = due_date OR null
     g. new_task.priority = priority OR "normal"
     h. new_task.completed_timestamp = null
     i. new_task.version = "1.0.0"

  4. Add to Task List
     a. task_list.append(new_task)
     b. IF append fails (storage error) THEN
        RETURN error("Cannot save task (storage error)")

  5. Return Success
     a. message = format("✓ Task created: {id} '{title}'")
        # If due_date or non-default priority, include them
        # Example: "✓ Task created: task-001 'Buy groceries' (due: 2026-01-15, priority: high)"
     b. RETURN (new_task, message)

Special Cases:
  - First task ever (empty list): Same logic, ID will be "task-001"
  - Task title with special characters: Allowed, stored as-is
  - Task title with newlines: Reject (invalid)
  - Due date in past: Allowed (for backlog items), optional warning
  - Due date far in future (2099+): Allowed, optional warning
  - Task title at exact boundary (255 chars): Allowed
  - Very large task list (1000+ tasks): Still O(1) creation, but O(n) ID search could be optimized

Verification:
  ✓ Created task has unique ID
  ✓ ID is sequential and doesn't skip numbers
  ✓ Task appears in list immediately
  ✓ All fields set correctly
  ✓ Invalid inputs are rejected with clear errors
  ✓ Edge cases (empty list, boundary values) work correctly
```

**Algorithm 2: List Tasks with Filtering and Sorting**

```
Algorithm: ListTasks
Purpose: Return all tasks optionally filtered by status/priority and sorted
Input:
  - filter_status (enum: pending/completed/all, default: "all")
  - sort_by (enum: created/due-date/priority, default: "created")
  - sort_order (enum: ascending/descending, default: "ascending")
  - limit (integer max results, default: 20, 0 = all)
Output:
  - filtered_sorted_tasks (list of Task objects)
  - metadata (total count, shown count, info message)
Complexity:
  Time: O(n) where n = number of tasks (filter) + O(n log n) for sort = O(n log n)
  Space: O(n) for result list

Pre-Conditions:
  - Task list may be empty or have tasks
  - Filter and sort parameters are valid

Post-Conditions:
  - Returned tasks match filter criteria
  - Returned tasks are sorted by specified field
  - Number of results ≤ limit
  - Metadata shows true counts

Steps:
  1. Initialize
     a. all_tasks = get_all_tasks()
     b. IF all_tasks is empty THEN
        RETURN (empty_list, message="No tasks yet. Create one: todo add 'task'")

  2. Filter Tasks by Status
     a. filtered_tasks = empty list
     b. FOR each task IN all_tasks
        i. IF filter_status == "all" THEN
           append task to filtered_tasks
        ii. ELSE IF filter_status == "pending" AND task.status == "pending" THEN
           append task to filtered_tasks
        iii. ELSE IF filter_status == "completed" AND task.status == "completed" THEN
           append task to filtered_tasks
        iv. ELSE skip task (doesn't match filter)

  3. Sort Tasks
     a. IF sort_by == "created" THEN
        sort filtered_tasks by created_timestamp
     b. ELSE IF sort_by == "due-date" THEN
        i. Create two lists: tasks_with_due_date, tasks_without_due_date
        ii. FOR each task IN filtered_tasks
            - IF task.due_date is not null THEN add to tasks_with_due_date
            - ELSE add to tasks_without_due_date
        iii. Sort tasks_with_due_date by due_date (ascending: earliest first)
        iv. Concatenate: sorted = tasks_with_due_date + tasks_without_due_date
            (tasks without due dates appear last)
     c. ELSE IF sort_by == "priority" THEN
        i. Define priority order: high (1) > normal (2) > low (3)
        ii. Sort filtered_tasks by priority (high first, low last)
        iii. For tasks with same priority, maintain created timestamp order (stable sort)

  4. Apply Reverse Order (if requested)
     a. IF sort_order == "descending" THEN
        reverse(filtered_tasks)

  5. Apply Limit
     a. IF limit == 0 THEN
        results = filtered_tasks  (return all)
     b. ELSE
        results = filtered_tasks[0:limit]  (return first limit items)

  6. Prepare Metadata
     a. total_count = length(all_tasks)
     b. filtered_count = length(filtered_tasks)
     c. shown_count = length(results)
     d. IF shown_count < filtered_count THEN
        message = format("Showing {shown} of {filtered} tasks. Run 'todo list --limit {filtered}' to see all")
     e. ELSE
        message = format("Showing all {total} tasks")

  7. Return Results
     a. RETURN (results, metadata={total: total_count, filtered: filtered_count, shown: shown_count, message: message})

Special Cases:
  - Empty task list: Return empty list with helpful message
  - No tasks match filter: Return empty list with message
  - All tasks have no due date: Sort by due_date puts all at end
  - limit=0: Return all tasks (no truncation)
  - limit > total: Return all tasks (no error)
  - limit=1: Return single task
  - Stable sort: If two tasks have same priority, maintain creation order

Verification:
  ✓ Filtering works correctly (pending, completed, all)
  ✓ Sorting works correctly (by created, due_date, priority)
  ✓ Reverse order reverses results
  ✓ Limit truncates results correctly
  ✓ Metadata counts are accurate
  ✓ Edge cases (empty list, no matches) handled
  ✓ Tasks without due dates appear correctly
  ✓ Stable sort maintains original order for ties
```

**Algorithm 3: Complete Task (Mark as Done)**

```
Algorithm: CompleteTask
Purpose: Mark a task as completed and record completion time
Input:
  - task_id (string, e.g., "task-001")
Output:
  - updated_task (Task object)
  - success_message (string confirmation)
Complexity:
  Time: O(n) where n = number of tasks (find task) + O(1) for update = O(n)
  Space: O(1) constant space

Pre-Conditions:
  - Task with task_id exists in task list
  - Task is currently in "pending" status

Post-Conditions:
  - Task status changed to "completed"
  - Task.completed_timestamp set to current time
  - Task is no longer returned by "pending" filters
  - Task is returned by "completed" filters

Steps:
  1. Find Task
     a. task = find_task_by_id(task_id)
     b. IF task == null THEN
        RETURN error("Task not found: {task_id}")

  2. Check State
     a. IF task.status == "completed" THEN
        RETURN error("Task already completed: {task_id} '{title}'")
     b. IF task.status != "pending" THEN
        RETURN error("Cannot complete task in '{status}' state")

  3. Update Task
     a. task.status = "completed"
     b. task.completed_timestamp = current_time_utc()
     c. IF update fails THEN
        RETURN error("Cannot save task (update failed)")

  4. Return Success
     a. message = format("✓ Task marked complete: {id} '{title}'")
        # Optional: Add time-to-completion info
        # Example: "✓ Task marked complete: task-001 'Buy groceries' (completed in 3 days)"
     b. RETURN (task, message)

Special Cases:
  - Task already completed: Error (cannot complete twice)
  - Task in unknown state: Error (shouldn't happen)
  - Task ID not found: Error with helpful message
  - First task ever completed: Same logic, just update single task

Verification:
  ✓ Task status changes from pending to completed
  ✓ Completion timestamp is set
  ✓ Task no longer appears in pending filters
  ✓ Task appears in completed filters
  ✓ Error if already completed
  ✓ Error if task not found
```

**Algorithm 4: Delete Task**

```
Algorithm: DeleteTask
Purpose: Permanently remove a task from the task list
Input:
  - task_id (string, e.g., "task-001")
  - confirm (boolean, whether confirmation was given)
Output:
  - success_message (string confirmation)
  - deleted_task (Task object, for logging)
Complexity:
  Time: O(n) where n = number of tasks (find + remove)
  Space: O(1) constant space

Pre-Conditions:
  - Task with task_id exists (or error shown)
  - confirm flag is true (confirmation given)

Post-Conditions:
  - Task removed from task list
  - Task no longer appears in any list/filter operations
  - Task cannot be retrieved by ID

Steps:
  1. Find Task
     a. task = find_task_by_id(task_id)
     b. IF task == null THEN
        RETURN error("Task not found: {task_id}")

  2. Get Task Details (for confirmation message)
     a. task_title = task.title
     b. saved_task = copy(task)  # Save for return value

  3. Delete from List
     a. task_list.remove(task)
     b. IF remove fails THEN
        RETURN error("Cannot delete task (storage error)")

  4. Verify Deletion
     a. IF find_task_by_id(task_id) != null THEN
        RETURN error("Delete failed: task still exists")

  5. Return Success
     a. message = format("✓ Task deleted: {id} '{title}'")
     b. RETURN (message, deleted_task=saved_task)

Special Cases:
  - Task doesn't exist: Error
  - Delete last remaining task: Same logic, list becomes empty
  - Delete task by ID that partially matches: No (must be exact match)

Verification:
  ✓ Task is removed from list
  ✓ Task cannot be found by ID after deletion
  ✓ Other tasks are unaffected
  ✓ Error if task doesn't exist
```

**Algorithm 5: Search Tasks**

```
Algorithm: SearchTasks
Purpose: Find tasks matching a keyword in title
Input:
  - keyword (string to search for)
  - case_sensitive (boolean, default: false)
  - filter_status (enum: pending/completed/all, default: "all")
Output:
  - matching_tasks (list of Task objects)
  - metadata (count, search term)
Complexity:
  Time: O(n) where n = number of tasks (scan all, check each)
  Space: O(m) where m = number of matches

Pre-Conditions:
  - Task list may be empty or have tasks
  - keyword is non-empty string

Post-Conditions:
  - Returned tasks contain keyword in title
  - Results match filter_status if provided
  - Search is case-insensitive by default

Steps:
  1. Validate Input
     a. IF keyword is empty THEN
        RETURN error("Search keyword cannot be empty")
     b. search_term = keyword

  2. Initialize Search
     a. matches = empty list
     b. all_tasks = get_all_tasks()
     c. IF all_tasks is empty THEN
        RETURN (empty_list, message="No tasks to search")

  3. Search Tasks
     a. FOR each task IN all_tasks
        i. IF filter_status != "all" AND task.status != filter_status THEN
           skip (doesn't match status filter)
        ii. IF case_sensitive == true THEN
           contains = search_term in task.title
        iii. ELSE (case-insensitive, default)
           contains = search_term.lower() in task.title.lower()
        iv. IF contains == true THEN
           append task to matches

  4. Prepare Results
     a. count = length(matches)
     b. IF count == 0 THEN
        message = format("No tasks found matching '{keyword}'")
     c. ELSE IF count == 1 THEN
        message = format("Found 1 task matching '{keyword}'")
     d. ELSE
        message = format("Found {count} tasks matching '{keyword}'")

  5. Return Results
     a. RETURN (matches, metadata={count: count, message: message})

Special Cases:
  - Keyword not found: Return empty list with message
  - Case-sensitive search: Exact case match only
  - Partial match: "milk" matches "Buy groceries and milk"
  - Special characters in keyword: Treated as literal (not regex)

Verification:
  ✓ All matching tasks returned
  ✓ No non-matching tasks included
  ✓ Case-insensitivity works correctly
  ✓ Status filter applied correctly
  ✓ Empty keyword rejected
  ✓ No tasks found returns appropriate message
```

---

### Step 3: Define Decision Points and Branches
Identify all decision points in algorithms.

**Decision Point Analysis (Example: CreateTask)**:

```
Decision 1: Task Title Validation
  Condition: task_title is empty or null
  IF true: Reject with error "Task title cannot be empty"
  IF false: Continue

Decision 2: Task Title Length
  Condition: length(task_title) outside 1-255 range
  IF true: Reject with error showing actual length
  IF false: Continue

Decision 3: Date Format Validation
  Condition: due_date provided AND format is not YYYY-MM-DD
  IF true: Reject with error showing expected format
  IF false: Continue or skip (no due_date)

Decision 4: Date Validity
  Condition: due_date provided AND date doesn't exist (e.g., Feb 30)
  IF true: Reject with error explaining why
  IF false: Continue

Decision 5: Priority Validation
  Condition: priority provided AND not in {low, normal, high}
  IF true: Reject with error listing valid values
  IF false: Continue or skip (use default "normal")

Decision 6: Task ID Collision
  Condition: Generated ID already exists in list
  IF true: Reject with system error (very rare)
  IF false: Proceed with creation

All Decisions Must Result In:
  - Clear error message to user (if reject)
  - Proceed with next step (if accept)
  - No silent failures or undefined behavior
```

---

### Step 4: Handle Edge Cases
Explicitly define behavior for edge cases.

**Edge Case Examples**:

```
Edge Case: First Task Creation (Empty List)
  - Max ID calculation returns 0
  - New ID becomes "task-001"
  - Task is first in list
  - List transitions from empty to non-empty
  Logic: Same as normal creation, just starting from task-001

Edge Case: Task Title with Special Characters
  - Title: "Buy milk & bread @store #urgent"
  - Special chars are stored as-is (no escaping)
  - No interpretation of special meaning
  - Allows user to write naturally
  Logic: Store raw string, no sanitization

Edge Case: Boundary Date (Leap Year)
  - Date: "2026-02-29" (not leap year, invalid)
  - Should reject: "Invalid date '2026-02-29'. Feb 29 only in leap years."
  - Alternative valid: "2026-02-28"
  Logic: Validate full date existence, not just format

Edge Case: Very Long Task List (1000+ Tasks)
  - CreateTask: Still O(1) if using next sequential ID
  - ListTasks: O(n log n) acceptable for 1000 items
  - Search: O(n) acceptable for 1000 items
  - Optimization: If scales beyond 1000, consider:
    - Caching max ID instead of scanning all
    - Indexing by status/priority
    - Database in Phase II
  Logic: Phase 1 doesn't optimize beyond O(n); Phase II uses database

Edge Case: Task Completed and Reverted
  - Complete task: status = "completed", completed_timestamp = 2026-01-15T10:00:00Z
  - Revert (Phase II feature): status = "pending", completed_timestamp stays (historical record)
  - Not in Phase 1 MVP, but design for Phase II:
    - Don't clear completed_timestamp
    - Keep for analytics (time-to-completion)
  Logic: Immutable history, reversible status

Edge Case: Filtering With No Matches
  - Filter by "pending" when all tasks completed
  - Return empty list with message: "No pending tasks"
  - Don't error, just empty result
  Logic: Empty result set is valid, not an error

Edge Case: Sorting Stable Order
  - Two tasks have same priority (both "normal")
  - Order by creation time (original creation sequence)
  - Don't randomize or shuffle
  Logic: Use stable sort to maintain insertion order for ties
```

---

### Step 5: Define Algorithm Correctness Criteria
Establish verification standards.

**Correctness Verification**:

```
For Each Algorithm, Verify:

1. Input Validation
   ✓ All required inputs are checked
   ✓ Invalid inputs are rejected with clear errors
   ✓ Edge case inputs (empty, null, boundary) handled
   ✓ No assumption about input validity

2. Decision Points
   ✓ All branches defined (if-then-else complete)
   ✓ No undefined states (else clause always present)
   ✓ Error paths clearly identified
   ✓ Success paths clearly identified

3. Output
   ✓ Output format is consistent
   ✓ Output includes all necessary data
   ✓ Error messages are actionable
   ✓ Success messages confirm action

4. State Changes
   ✓ All state modifications documented
   ✓ State consistency maintained (no corrupted state)
   ✓ Side effects explicitly listed
   ✓ Rollback/recovery defined if needed

5. Edge Cases
   ✓ First operation (empty state)
   ✓ Last operation (full/limit reached)
   ✓ Duplicate/conflicting operations
   ✓ Boundary values (max length, max count)
   ✓ Missing/null data

6. Complexity
   ✓ Time complexity documented
   ✓ Acceptable for Phase 1 scale (100-1000 items)
   ✓ No hidden expensive operations
   ✓ Optimization path identified for Phase II

7. Consistency
   ✓ Algorithm matches acceptance criteria
   ✓ Algorithm matches user expectations
   ✓ Same logic in all languages (Python, JS, etc.)
   ✓ Deterministic (same input → same output)
```

---

## Output

**Format**: Structured Markdown document with complete algorithms:

```markdown
# Business Logic and Algorithm Design

## Algorithm Template
[Standard format for expressing algorithms]

## Core Algorithms (Phase 1)
[CreateTask, ListTasks, CompleteTask, DeleteTask, SearchTasks]

## Algorithm Specifications
[Detailed pseudocode for each]

## Decision Points and Branches
[All conditional logic documented]

## Edge Case Handling
[How boundary conditions are handled]

## Correctness Criteria
[Verification checklist for algorithms]

## Examples and Walkthroughs
[Step-by-step execution examples]
```

---

## Failure Handling

### Scenario 1: Algorithm Ambiguity in Language
**Symptom**: Python dev interprets "sort by due date" differently than JS dev
**Resolution**:
- Document sort order explicitly: "ascending = earliest due date first"
- Document nulls/empty: "Tasks without due dates appear last"
- Include example: "Due dates [2026-01-15, null, 2026-01-10] → [2026-01-10, 2026-01-15, null]"
- Cross-language tests verify same behavior

### Scenario 2: Edge Case Not Documented
**Symptom**: What happens if user completes already-completed task?
**Resolution**:
- Document explicitly in algorithm: "IF task.status == 'completed' THEN RETURN error"
- Test verifies: completing completed task shows error
- Error message consistent across all languages

### Scenario 3: Algorithm Has Hidden Assumption
**Symptom**: "Find max ID" assumes IDs are numeric and formatted "task-001"
**Resolution**:
- Document assumption: "Task IDs are formatted as 'task-NNN' where NNN is 3-digit number"
- Document extraction logic: "Parse numeric part using regex: task-(\d+)"
- Test verifies: Works with "task-001" through "task-999"

### Scenario 4: Performance Not Considered
**Symptom**: Linear search for every list operation becomes slow with 10K tasks
**Resolution**:
- Document complexity: "O(n) time for searching all tasks"
- State acceptable for Phase 1: "Acceptable for Phase 1 (max ~1000 tasks)"
- Plan Phase II optimization: "Phase II will use database indexes for O(1) lookup"
- Don't over-engineer Phase 1; document phase-out plan

### Scenario 5: Determinism Not Guaranteed
**Symptom**: Sorting tasks returns different order in different runs
**Resolution**:
- Ensure stable sort: "For tasks with equal priority, maintain creation order"
- Document randomness: "No randomization in any algorithm"
- Test: Run same algorithm 10x, verify same output each time

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Cross-language implementation**: Pseudocode serves as spec for Python, JS, Go, etc.
- **Code review**: Reference spec when reviewing implementation
- **Test case generation**: Algorithms define expected behavior for tests
- **Phase evolution**: Algorithms can be enhanced in Phase II without breaking Phase 1
- **Bug fixes**: If behavior is wrong, update algorithm first, then code
- **Documentation**: Algorithms serve as executable documentation

---

## Success Metrics

- ✅ All algorithms expressed in language-agnostic pseudocode
- ✅ All decision points and branches explicitly documented
- ✅ All edge cases handled (empty, boundary, null)
- ✅ Time/space complexity documented and acceptable for Phase 1
- ✅ Pre-conditions and post-conditions clearly defined
- ✅ Error cases return actionable error messages
- ✅ Special cases documented (first operation, no matches, etc.)
- ✅ Algorithms match acceptance criteria
- ✅ Same algorithm produces same output in any language
- ✅ No undefined behavior or implicit assumptions

---

## Related Skills

- **Acceptance Criteria (PA-001)**: Algorithms implement these criteria
- **Edge Case Identification (QA-001)**: Tests verify edge case handling
- **Data Model (DMD-001)**: Algorithms operate on Task entity
- **Error Messaging (QA-002)**: Algorithms produce these error messages

---

## Example: Complete Algorithm Walkthrough

### Scenario: User Lists Tasks with Filter

**Command**: `todo list --filter pending --sort due-date`

**Walkthrough**:

```
Input:
  filter_status = "pending"
  sort_by = "due-date"
  sort_order = "ascending"
  limit = 20 (default)

Execution:

Step 1: Initialize
  all_tasks = [
    { id: "task-001", title: "Buy groceries", status: "pending", due_date: "2026-01-15", priority: "normal" },
    { id: "task-002", title: "Submit report", status: "completed", due_date: "2026-01-10", priority: "high" },
    { id: "task-003", title: "Fix bug", status: "pending", due_date: null, priority: "high" },
    { id: "task-004", title: "Plan meeting", status: "pending", due_date: "2026-01-20", priority: "normal" }
  ]
  total_count = 4

Step 2: Filter by Status ("pending")
  FOR each task in all_tasks:
    task-001: status = "pending" → INCLUDE
    task-002: status = "completed" → SKIP
    task-003: status = "pending" → INCLUDE
    task-004: status = "pending" → INCLUDE

  filtered_tasks = [
    { id: "task-001", due_date: "2026-01-15", ... },
    { id: "task-003", due_date: null, ... },
    { id: "task-004", due_date: "2026-01-20", ... }
  ]
  filtered_count = 3

Step 3: Sort by Due Date
  Separate into two groups:
    with_due_date = [task-001 (2026-01-15), task-004 (2026-01-20)]
    without_due_date = [task-003 (null)]

  Sort with_due_date by date (ascending, earliest first):
    task-001 (2026-01-15)
    task-004 (2026-01-20)

  Concatenate:
    sorted_tasks = [task-001, task-004, task-003]

Step 4: Apply Reverse (not requested, skip)

Step 5: Apply Limit (20, no truncation needed)
  results = [task-001, task-004, task-003]  (all 3 items)
  shown_count = 3

Step 6: Prepare Metadata
  total_count = 4
  filtered_count = 3
  shown_count = 3
  message = "Showing all 3 pending tasks"

Output:
  Results:
    ┌─────────┬──────────────────┬──────────┬────────────┬──────────┐
    │ ID      │ TITLE            │ STATUS   │ DUE DATE   │ PRIORITY │
    ├─────────┼──────────────────┼──────────┼────────────┼──────────┤
    │ task-001│ Buy groceries    │ pending  │ 2026-01-15 │ normal   │
    │ task-004│ Plan meeting     │ pending  │ 2026-01-20 │ normal   │
    │ task-003│ Fix bug          │ pending  │ (none)     │ high     │
    └─────────┴──────────────────┴──────────┴────────────┴──────────┘

  Message: "Showing all 3 pending tasks"

Correctness Verification:
  ✓ Filter applied correctly (only "pending" tasks)
  ✓ Sort by due date (earliest first: 2026-01-15, then 2026-01-20, then null)
  ✓ Tasks without due date appear last
  ✓ Counts are accurate (3 pending out of 4 total)
  ✓ All results returned (shown = 3, filtered = 3)
```

---

### Scenario: User Tries to Complete Already-Completed Task

**Command**: `todo complete task-002` (task-002 is already completed)

**Walkthrough**:

```
Input:
  task_id = "task-002"

Execution:

Step 1: Find Task
  task = find_task_by_id("task-002")
  result: { id: "task-002", title: "Submit report", status: "completed", ... }
  found = true

Step 2: Check State
  IF task.status == "completed" THEN
    RETURN error("Task already completed: task-002 'Submit report'")

Output:
  Error Message: "✗ Error: Task already completed: task-002 'Submit report'"
  Action: None (task state unchanged)

Correctness Verification:
  ✓ Error returned (cannot complete twice)
  ✓ Error message shows task ID and title
  ✓ Task state unchanged
  ✓ No side effects
```

---

## Conclusion

Phase 1 algorithms are simple, correct, and language-agnostic. All logic is documented in pseudocode, all decision points are explicit, and all edge cases are handled. This ensures consistent behavior across all implementations (Python, JavaScript, Go, etc.) and makes testing straightforward.

