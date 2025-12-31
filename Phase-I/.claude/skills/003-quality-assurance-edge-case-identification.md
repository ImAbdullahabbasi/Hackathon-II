# Skill: Edge Case Identification and Analysis

**Skill ID**: QA-001
**Agent Owner**: quality-assurance
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Systematically identify and document edge cases, boundary conditions, and error scenarios for each CLI todo feature. This skill ensures comprehensive test coverage by examining invalid inputs, missing data, conflicting states, and real user mistakes that could cause unexpected behavior. Edge case analysis prevents bugs from reaching production and informs error handling design decisions.

---

## When to Use

- **Specification refinement**: After functional analysis (CLI-001) is complete, before implementation
- **Test case generation**: Creating comprehensive QA test plans and test scenarios
- **Error handling design**: Informing what error messages and recovery mechanisms are needed
- **Robustness validation**: Ensuring system gracefully handles unexpected inputs and states
- **User experience improvement**: Identifying where better guidance or validation is needed
- **Requirement completeness**: Finding gaps in functional specifications

---

## Inputs

1. **Feature functional specification** (document): Output from CLI-UX-Designer (CLI-001) with inputs, processes, outputs
2. **User story** (text): Original user story from requirements-analyst (RA-001)
3. **Business rules** (list, optional): Rules from business-logic-engineer that constrain behavior
4. **Current implementation constraints** (text, optional): Known limitations (e.g., "in-memory only", "single-user")

---

## Step-by-Step Process

### Step 1: Extract Input Constraints
Review the functional specification to identify all inputs and their documented constraints.

**For Each Input**:
- What type is it? (string, integer, date, enum, boolean)
- What are the valid constraints? (required/optional, min/max, allowed values, format)
- What validation rules apply?

**Example Input Analysis**:
```
Input: task_title
  Type: string
  Valid constraints: required, non-empty, max 255 characters, no leading/trailing whitespace
  Validation rules: Must be between 1-255 chars, trimmed
```

### Step 2: Identify Invalid Input Cases
For each input, systematically generate invalid cases that violate constraints.

**Categories of Invalid Input**:

#### A. Missing/Empty Input
- Required input not provided at all
- Input provided as empty string, zero, null, undefined
- Input provided as whitespace-only

**Example Edge Cases**:
- User enters "todo add" with no title argument
- User enters "todo add ''" (empty string)
- User enters "todo add '    '" (whitespace only)

#### B. Format Violations
- Wrong data type provided (text instead of number, string instead of date)
- Invalid format for structured inputs (dates, URLs, patterns)
- Encoding issues (special characters, unicode, line breaks)

**Example Edge Cases**:
- User enters "todo add 123" for date (number instead of YYYY-MM-DD string)
- User enters "todo add 'Title' --due 01/15/2026" (MM/DD/YYYY instead of YYYY-MM-DD)
- User enters "todo add 'Title\nMultiline'" (title with newline)
- User enters "todo add 'Title' --priority urgent" (unknown priority value)

#### C. Boundary Value Violations
- Minimum boundary: input below minimum allowed (negative, less than 1)
- Maximum boundary: input exceeds maximum allowed (string too long, number too large)
- Off-by-one errors: exactly at boundary (e.g., 255 chars vs. 256 chars)

**Example Edge Cases**:
- User enters "todo add '[256-character string]'" (exceeds max 255)
- User enters "todo add '[255-character string]'" (exactly at boundary, should succeed)
- User enters "todo add '[0-character string]'" (empty, should fail)

#### D. Special/Reserved Characters
- Characters that might be interpreted specially by shell or system
- Quotes, backslashes, wildcards, control characters
- HTML/SQL injection attempts (defensive design)

**Example Edge Cases**:
- User enters "todo add 'Title with \"quotes\"'" (escaped quotes in title)
- User enters "todo add 'Title; rm -rf /'" (command injection attempt)
- User enters "todo add 'Title' OR 1=1; --'" (SQL injection attempt)
- User enters "todo add 'Title\x00Binary'" (null byte)

#### E. Locale/Encoding Issues
- Non-ASCII characters (emojis, accented characters, CJK)
- Right-to-left text
- Case sensitivity

**Example Edge Cases**:
- User enters "todo add '買い物リスト'" (Japanese title)
- User enters "todo add 'Café'" (accented characters)
- User enters "todo add '🎯 Buy milk'" (emoji in title)

### Step 3: Identify Missing Data Cases
Analyze scenarios where expected data is unavailable or incomplete.

**Missing Data Scenarios**:
- Feature requires data from another feature that hasn't been used yet
- System state is incomplete (e.g., trying to delete task when no tasks exist)
- Optional inputs not provided (should have sensible defaults)
- Data becomes stale or inconsistent

**Example Edge Cases for "Delete Task"**:
- User tries to delete from empty task list
- User provides task ID that doesn't exist
- User deletes a task, then tries to delete the same ID again
- User provides ID from a previous session (after app restart)

**Example Edge Cases for "Mark Complete"**:
- User tries to mark task as complete when no tasks exist
- User provides non-existent task ID
- Task list was modified by another instance (concurrent modification)

### Step 4: Identify Conflicting States
Analyze scenarios where system state creates impossible or contradictory situations.

**State Conflict Scenarios**:
- Attempting to transition to invalid state (already in that state)
- Attempting operation that contradicts current state
- Race conditions or timing issues (in future phases with concurrency)
- Data inconsistencies

**Example Edge Cases**:
- User tries to mark a task as complete that's already complete
- User tries to mark a deleted task as complete
- User creates task with due date in the past (already "overdue")
- User lists tasks, deletes one, tries to filter by that task's ID
- User tries to update a task title to same value (no-op)

### Step 5: Identify Boundary Conditions
Analyze system behavior at critical thresholds.

**Boundary Condition Categories**:
- List boundaries: empty list, single item, large number of items
- Time boundaries: current time, far future, past dates, leap year dates
- Size boundaries: minimum task title, maximum task title, very long descriptions
- Numeric boundaries: zero, negative numbers (if applicable), maximum integer values
- Collection boundaries: adding first item, removing last item

**Example Edge Cases**:
- User creates first task (empty list → one item)
- User deletes last task (one item → empty list)
- User creates 1,000 tasks (memory/performance boundary)
- User tries to create task with due date "2099-12-31" (far future)
- User tries to create task with due date "1900-01-01" (far past)
- User tries to create task with due date "2026-02-29" (leap year boundary, but 2026 is not leap year)
- User searches through list with exactly 100 tasks (boundary threshold)

### Step 6: Identify Real User Mistakes
Analyze mistakes actual users commonly make, based on UX research and user behavior.

**Common User Mistakes**:
- Typos and misspellings
- Copy-paste errors (extra spaces, newlines)
- Accidental double-submission (clicking button twice)
- Confusion between features (trying to use delete syntax for complete)
- Forgetting required fields
- Using inconsistent formats (sometimes YYYY-MM-DD, sometimes MM/DD/YYYY)
- Misunderstanding error messages and retrying wrong action

**Example Edge Cases**:
- User enters "todo add 'Buy milk  '" (trailing spaces; should be trimmed)
- User pastes title from email with newlines: "Buy milk\nBread\nEggs" (should be rejected or newlines stripped)
- User enters "todo add 'Buy milk'" twice in quick succession (double submission)
- User enters "todo delete 5" when command is actually "todo remove 5" (command format confusion)
- User enters date as "2026-1-5" instead of "2026-01-05" (zero-padding inconsistency)
- User copy-pastes task ID from output but includes trailing whitespace: "task-001 " (should be trimmed)

### Step 7: Create Edge Case Catalog
Document all identified edge cases in structured format with explanation.

**Edge Case Documentation Format**:
```
## Edge Case: [Brief Title]

**Category**: [Invalid Input / Missing Data / Conflicting State / Boundary Condition / User Mistake]

**Scenario**: [What user does or what situation occurs]

**Expected Input/State**: [What should happen]

**Actual Behavior (Without Handling)**: [What could go wrong]

**Why It Matters**: [Impact on user, data integrity, system stability]

**Severity**: [Critical / High / Medium / Low]
  - Critical: Data corruption, data loss, security vulnerability
  - High: Feature fails, user cannot complete task, unexpected crash
  - Medium: Confusing error message, poor user experience, workaround exists
  - Low: Minor UX issue, rare edge case, cosmetic problem

**Recommended Handling**: [How system should respond]

**Test Case**: [How QA should verify this is handled correctly]
```

### Step 8: Validate Edge Case Completeness
Ensure edge case analysis is thorough and covers all important scenarios.

**Validation Checklist**:
- ✅ All input types have invalid cases documented
- ✅ All constraints have boundary cases documented
- ✅ State transitions have conflict cases documented
- ✅ At least 3 real user mistake scenarios documented per feature
- ✅ Edge cases span all severity levels (not just "nice to have")
- ✅ Critical and high-severity cases have recommended handling
- ✅ Each edge case explains WHY it matters (impact, not just description)
- ✅ Test cases are concrete and verifiable (not vague)

---

## Output

**Format**: Structured Markdown document organized by feature, with edge cases grouped by category:

```markdown
# Edge Case Analysis: [Feature Name]

## Invalid Input Cases
- **Case 1**: [Scenario] → [Why it matters]
- **Case 2**: [Scenario] → [Why it matters]

## Missing Data Cases
- **Case 1**: [Scenario] → [Why it matters]
- **Case 2**: [Scenario] → [Why it matters]

## Conflicting State Cases
- **Case 1**: [Scenario] → [Why it matters]
- **Case 2**: [Scenario] → [Why it matters]

## Boundary Condition Cases
- **Case 1**: [Scenario] → [Why it matters]
- **Case 2**: [Scenario] → [Why it matters]

## Real User Mistake Cases
- **Case 1**: [Scenario] → [Why it matters]
- **Case 2**: [Scenario] → [Why it matters]

## Summary
- Total edge cases identified: [N]
- Critical severity: [N]
- High severity: [N]
- Medium severity: [N]
- Low severity: [N]
```

---

## Failure Handling

### Scenario 1: Feature Specification is Incomplete
**Symptom**: Functional specification doesn't list all inputs or constraints
**Resolution**:
- Request complete specification from cli-ux-designer
- If needed, identify missing inputs and infer likely constraints
- Document assumptions clearly
- Mark as "pending specification update"

### Scenario 2: Edge Case Identified But No Clear Handling Strategy
**Symptom**: Found edge case (e.g., duplicate task creation) but unclear how to handle it
**Resolution**:
- Mark as "requires design decision"
- Escalate to business-logic-engineer for rule definition
- Propose options: reject, allow with warning, auto-deduplicate, etc.
- Don't leave unresolved

### Scenario 3: Too Many Edge Cases (Analysis Paralysis)
**Symptom**: Hundreds of edge cases identified; cannot prioritize
**Resolution**:
- Focus on severity: critical and high first
- Group related cases (e.g., all date format variants into one category)
- Document low-severity cases as "nice to have" for future phases
- Recommend MVP edge cases and Phase II enhancements

### Scenario 4: Edge Cases Contradict Functional Spec
**Symptom**: Functional spec allows behavior, but edge case analysis says it should be blocked
**Resolution**:
- This indicates a spec gap or ambiguity
- Raise for clarification with requirements-analyst or business-logic-engineer
- Example: "Spec allows empty priority field, but is NULL acceptable?"
- Update spec and edge case analysis together

### Scenario 5: Overlap Between Edge Cases
**Symptom**: Multiple edge cases describe same scenario with different wording
**Resolution**:
- Consolidate into single documented edge case
- Note all variations in "Scenario" description
- Avoid duplicate test cases

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **All Phase 1 features**: Create, list, delete, mark complete, filter, search, edit
- **Input validation**: Edge cases inform input validation rules used across features
- **Error message design**: Edge cases identify what error messages are needed
- **QA test plan generation**: Output directly feeds into comprehensive test case suite
- **Future phases**: Same edge case categories (invalid input, missing data, state conflicts) apply to web app and cloud phases
- **Requirement refinement**: Edge cases reveal ambiguities in specs; help tighten requirements

---

## Success Metrics

- ✅ At least 5 edge cases identified per feature
- ✅ All input types have both valid and invalid cases
- ✅ Edge cases span all 5 categories (invalid input, missing data, conflict, boundary, user mistake)
- ✅ Each case explains WHY it matters (impact, not just description)
- ✅ Severity levels assigned (critical, high, medium, low)
- ✅ Recommended handling defined for critical/high cases
- ✅ Test cases are concrete and verifiable
- ✅ No vague language ("may", "might", "could") — use definitive language

---

## Related Skills

- **CLI-UX-Designer (CLI-001)**: Provides functional specification with input constraints
- **Business-Logic-Engineer (BLE-001)**: Defines business rules that govern edge case handling
- **Requirements-Analyst (RA-001)**: Clarifies user intent when edge cases reveal ambiguity
- **Data-Model-Designer**: Identifies state conflicts based on data structure design

---

## Example: Phase 1 Feature Edge Cases

### Feature: Create Task

#### Invalid Input Cases

**Case 1: Empty Task Title**
- **Scenario**: User enters "todo add" with no title or "todo add ''"
- **Expected**: System rejects with error message
- **Why It Matters**: Task title is required; empty tasks are useless and waste storage. Foundation of data quality.
- **Severity**: Critical
- **Handling**: Display error "✗ Error: Task title cannot be empty. Please provide a task title."
- **Test**: `todo add ''` → should show error, no task created

**Case 2: Whitespace-Only Title**
- **Scenario**: User enters "todo add '    '" (spaces, tabs, newlines only)
- **Expected**: System trims whitespace and rejects if result is empty
- **Why It Matters**: Whitespace-only titles appear empty to user; confusing and poor data quality
- **Severity**: High
- **Handling**: Trim whitespace; if empty after trimming, reject as Case 1
- **Test**: `todo add '   '` → should show error, no task created

**Case 3: Title Exceeds Max Length**
- **Scenario**: User enters title of 300 characters (spec max is 255)
- **Expected**: System rejects with error and provides character count
- **Why It Matters**: Prevents data bloat; ensures consistent display across interfaces
- **Severity**: High
- **Handling**: Display error "✗ Error: Task title too long (300 chars). Max allowed: 255"
- **Test**: `todo add '[300-char string]'` → should show error

**Case 4: Title at Exact Boundary**
- **Scenario**: User enters title of exactly 255 characters
- **Expected**: System accepts (boundary case, should succeed)
- **Why It Matters**: Off-by-one errors in length checking; common implementation bug
- **Severity**: High
- **Handling**: Accept as valid (255 is inclusive max)
- **Test**: `todo add '[255-char string]'` → should create successfully

**Case 5: Invalid Date Format**
- **Scenario**: User enters "todo add 'Title' --due 01/15/2026" (MM/DD/YYYY instead of YYYY-MM-DD)
- **Expected**: System rejects with error showing expected format
- **Why It Matters**: Date format ambiguity is major source of errors (US vs. international). Prevents silent data corruption.
- **Severity**: Critical
- **Handling**: Display error "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"
- **Test**: `todo add 'Title' --due 01/15/2026` → should show error with expected format

**Case 6: Invalid Date - Non-Existent Date**
- **Scenario**: User enters "todo add 'Title' --due 2026-02-30" (February 30th doesn't exist)
- **Expected**: System detects invalid date and rejects
- **Why It Matters**: Prevents storing impossible dates; data integrity
- **Severity**: High
- **Handling**: Display error "✗ Error: Invalid date. February has only 28 days in 2026."
- **Test**: `todo add 'Title' --due 2026-02-30` → should show error

**Case 7: Invalid Priority Value**
- **Scenario**: User enters "todo add 'Title' --priority urgent" (allowed: low, normal, high)
- **Expected**: System rejects with list of allowed values
- **Why It Matters**: Invalid enum values corrupt data; prevents consistent filtering/sorting
- **Severity**: High
- **Handling**: Display error "✗ Error: Invalid priority. Allowed: low, normal, high"
- **Test**: `todo add 'Title' --priority urgent` → should show error

**Case 8: Title with Special Characters**
- **Scenario**: User enters "todo add 'Buy \"milk\" & bread'" (quotes, ampersand)
- **Expected**: System accepts and preserves special characters
- **Why It Matters**: Users need to create tasks with real-world text; special characters are common
- **Severity**: Medium (failure here is poor UX but not data loss)
- **Handling**: Accept and store exactly as provided (no interpretation)
- **Test**: `todo add 'Buy "milk" & bread'` → should create task with exact title

**Case 9: Title with Emoji**
- **Scenario**: User enters "todo add '🎯 Complete project'" (emoji in title)
- **Expected**: System accepts (modern CLIs support UTF-8)
- **Why It Matters**: Users increasingly use emoji; rejecting them is frustrating
- **Severity**: Low
- **Handling**: Accept UTF-8 encoded emoji
- **Test**: `todo add '🎯 Complete project'` → should create with emoji preserved

**Case 10: Title with Newlines (Multiline)**
- **Scenario**: User pastes title from email: "Buy milk\nBread\nEggs"
- **Expected**: System rejects or strips newlines (depending on design)
- **Why It Matters**: Multiline titles break list display and cause confusion
- **Severity**: High
- **Handling**: Recommended: Reject with error "Task title cannot contain line breaks"
- **Test**: Attempt paste with newline → should reject

#### Missing Data Cases

**Case 11: No Tasks Exist But User Creates One**
- **Scenario**: User creates first task on fresh app start
- **Expected**: System creates successfully; app transitions from empty state
- **Why It Matters**: Boundary between empty and non-empty state; different code paths
- **Severity**: High
- **Handling**: Handle gracefully; create task and initialize task list
- **Test**: Fresh app → `todo add 'First task'` → verify task-001 created and retrievable

**Case 12: Required Input Not Provided (No Title Argument)**
- **Scenario**: User enters "todo add" with no title argument or flag
- **Expected**: System prompts for title or shows usage error
- **Why It Matters**: User intent unclear; should not silently create empty task
- **Severity**: Critical
- **Handling**: Display error "✗ Error: Please provide a task title. Usage: todo add 'task title'"
- **Test**: `todo add` → should show usage error

#### Conflicting State Cases

**Case 13: Create Task with Past Due Date**
- **Scenario**: User enters "todo add 'Old task' --due 2020-01-01" (due date is in past)
- **Expected**: System accepts (not all past dates are errors; could be backlog item)
- **Why It Matters**: Past due dates are valid; task might already be overdue. Design choice.
- **Severity**: Low
- **Handling**: Accept but display warning "⚠ Warning: Task due date is in the past"
- **Test**: `todo add 'Task' --due 2020-01-01` → should create with warning

**Case 14: Create Task with Far Future Due Date**
- **Scenario**: User enters "todo add 'Long project' --due 2099-12-31" (99 years in future)
- **Expected**: System accepts (unusual but not invalid)
- **Why It Matters**: Catch potential typos or misunderstandings (year 2099 vs. 2029)
- **Severity**: Low
- **Handling**: Accept but optionally display warning "⚠ Warning: Task due date is far in the future (73 years)"
- **Test**: `todo add 'Task' --due 2099-12-31` → should create (optionally with warning)

#### Boundary Condition Cases

**Case 15: Create First Task (Empty List Boundary)**
- **Scenario**: User creates task when task list is empty
- **Expected**: Task created, list transitions to non-empty
- **Why It Matters**: Empty list is distinct state; ensures initialization is correct
- **Severity**: High
- **Handling**: Handle gracefully; task is task-001, list is now retrievable
- **Test**: Fresh app → create task → verify list contains one task

**Case 16: Create 1,000th Task (Large Collection Boundary)**
- **Scenario**: User creates many tasks (stress test); list contains 1,000 items
- **Expected**: Task created successfully; no performance degradation
- **Why It Matters**: Phase 1 is in-memory; very large lists may cause issues
- **Severity**: Medium
- **Handling**: Create successfully; performance acceptable for 1,000 items
- **Test**: Create 1,000 tasks in loop → each should succeed, memory usage reasonable

#### Real User Mistake Cases

**Case 17: Trailing Spaces in Title**
- **Scenario**: User copy-pastes title from document: "Buy milk " (trailing space)
- **Expected**: System trims whitespace
- **Why It Matters**: Common copy-paste error; title with trailing space looks identical to user
- **Severity**: Medium
- **Handling**: Automatically trim leading/trailing whitespace from title
- **Test**: `todo add ' Buy milk '` → should create as "Buy milk"

**Case 18: Double Submission (Rapid Repeat)**
- **Scenario**: User enters "todo add 'Task'" then immediately enters same command again
- **Expected**: System creates two separate tasks (not deduplicated in Phase 1 MVP)
- **Why It Matters**: User may click multiple times thinking first didn't work
- **Severity**: Low
- **Handling**: Phase 1 allows duplicates (no uniqueness constraint). Phase II could add deduplication.
- **Test**: `todo add 'Task'` twice → should create two identical tasks

**Case 19: Date Format Inconsistency**
- **Scenario**: User creates task with "2026-01-15", next task with "2026-1-15" (missing zero padding)
- **Expected**: System should accept both formats (parse flexibly) or reject second (enforce strict format)
- **Why It Matters**: Users naturally use different formats; inconsistency in acceptance causes confusion
- **Severity**: Medium
- **Handling**: Recommended: Accept and normalize to YYYY-MM-DD format; or reject second as invalid
- **Test**: `todo add 'A' --due 2026-01-15` then `todo add 'B' --due 2026-1-15` → consistent handling

**Case 20: Command Syntax Confusion**
- **Scenario**: User enters "add 'Title'" instead of "todo add 'Title'" (missing "todo" command)
- **Expected**: System shows error or help message
- **Why It Matters**: New users may not remember exact command syntax; good error message helps
- **Severity**: Low
- **Handling**: Display error "✗ Command not found: 'add'. Did you mean 'todo add'?"
- **Test**: `add 'Task'` → should show helpful error

#### Summary

**Total edge cases identified**: 20
- **Critical severity**: 3 (empty title, invalid date, required input missing)
- **High severity**: 9 (whitespace title, exceeds length, boundary, invalid date, priority, multiline, first task, large collection)
- **Medium severity**: 5 (special chars, trailing spaces, date inconsistency, past date, double submission)
- **Low severity**: 3 (emoji, far future date, command syntax)

**Recommended MVP Coverage** (Phase 1):
- All Critical cases MUST be handled
- All High cases SHOULD be handled
- Medium cases CAN be handled (prioritize trailing spaces, date consistency)
- Low cases are nice-to-have for Phase II

---

### Feature: Delete Task

#### Invalid Input Cases

**Case 1: Delete Non-Existent Task ID**
- **Scenario**: User enters "todo delete task-999" when only task-001 and task-002 exist
- **Expected**: System displays error "Task not found"
- **Why It Matters**: Prevents silent failures; user should know deletion failed
- **Severity**: High
- **Handling**: Display error "✗ Error: Task not found: task-999"
- **Test**: `todo delete task-999` → should show error

**Case 2: Delete with Invalid Task ID Format**
- **Scenario**: User enters "todo delete 12345" (numeric ID instead of "task-001" format)
- **Expected**: System rejects or attempts to parse; unclear what user means
- **Why It Matters**: Task ID format matters; ambiguous input should not be accepted
- **Severity**: Medium
- **Handling**: Display error "✗ Error: Invalid task ID format. Expected 'task-NNN'"
- **Test**: `todo delete 12345` → should show error

**Case 3: Delete with No Task ID**
- **Scenario**: User enters "todo delete" with no task ID argument
- **Expected**: System shows usage error
- **Why It Matters**: Required argument missing; user intent unclear
- **Severity**: High
- **Handling**: Display error "✗ Error: Please provide a task ID. Usage: todo delete 'task-001'"
- **Test**: `todo delete` → should show usage error

#### Missing Data Cases

**Case 4: Delete from Empty Task List**
- **Scenario**: User tries to delete task when list is empty (app just started)
- **Expected**: System displays "No tasks to delete" or "Task not found"
- **Why It Matters**: Empty list is distinct state; prevent errors
- **Severity**: Medium
- **Handling**: Display error "✗ Error: No tasks exist. Task not found: task-001"
- **Test**: Fresh app → `todo delete task-001` → should show error

#### Conflicting State Cases

**Case 5: Delete Already-Deleted Task**
- **Scenario**: User deletes task-001, then tries to delete task-001 again
- **Expected**: System shows error (task no longer exists)
- **Why It Matters**: Prevents double-delete bugs; idempotency not guaranteed in Phase 1
- **Severity**: Medium
- **Handling**: Display error "✗ Error: Task not found: task-001"
- **Test**: Delete task → delete same ID again → should show error on second delete

**Case 6: Delete Task While Listing**
- **Scenario**: User lists tasks, then before list is displayed, deletes a task
- **Expected**: Behavior depends on implementation; list should reflect current state
- **Why It Matters**: In future phases with concurrency, race conditions are possible
- **Severity**: Low (not applicable to in-memory single-user Phase 1)
- **Handling**: In Phase 1, sequential operations only; no race conditions possible
- **Test**: Delete then list → deleted task should not appear

#### Boundary Condition Cases

**Case 7: Delete Last Remaining Task**
- **Scenario**: User has one task, deletes it; list becomes empty
- **Expected**: Task deleted, list is empty
- **Why It Matters**: Boundary between non-empty and empty state
- **Severity**: High
- **Handling**: Handle gracefully; return to empty state
- **Test**: Create one task → delete it → list should be empty

**Case 8: Delete from Large Task List**
- **Scenario**: User has 1,000 tasks, deletes one
- **Expected**: Deletion is fast; list updates correctly
- **Why It Matters**: Performance check for large collections
- **Severity**: Medium
- **Handling**: Deletion should be O(n) at worst; acceptable for 1,000 items
- **Test**: Create 1,000 tasks → delete middle task → verify performance

#### Real User Mistake Cases

**Case 9: Task ID with Whitespace**
- **Scenario**: User enters "todo delete ' task-001 '" (spaces around ID)
- **Expected**: System trims whitespace or rejects
- **Why It Matters**: Copy-paste errors often include whitespace
- **Severity**: Medium
- **Handling**: Trim leading/trailing whitespace from task ID before lookup
- **Test**: `todo delete ' task-001 '` → should find and delete task-001

**Case 10: Task ID Case Sensitivity**
- **Scenario**: User enters "todo delete TASK-001" or "todo delete Task-001" (wrong case)
- **Expected**: System should handle case-insensitively or reject clearly
- **Why It Matters**: Users may remember ID incorrectly; inconsistent case is common mistake
- **Severity**: Low
- **Handling**: Case-insensitive lookup recommended
- **Test**: `todo delete task-001` and `todo delete TASK-001` → both should delete same task

#### Summary

**Total edge cases identified**: 10
- **Critical severity**: 1 (delete non-existent task)
- **High severity**: 4 (invalid ID format, no ID, delete last task, from empty list)
- **Medium severity**: 4 (delete already-deleted, large collection, ID whitespace, case sensitivity)
- **Low severity**: 1 (concurrent delete in future phases)

