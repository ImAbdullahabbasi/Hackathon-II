# Skill: Negative Test Scenarios and Robustness Testing

**Skill ID**: QA-004
**Agent Owner**: quality-assurance
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Design comprehensive negative test scenarios that assume users will misuse the system, provide invalid input, and attempt edge cases. This skill ensures the system never crashes, hangs, or enters undefined states regardless of user actions. Negative testing prevents bugs from reaching production and builds user confidence that the system is robust and predictable. The goal is to ensure graceful degradation and helpful error messages for all possible misuse scenarios.

---

## When to Use

- **Test planning phase**: After features are designed, before development
- **QA test case generation**: Creating comprehensive test suite
- **Robustness validation**: Before beta/production release
- **Debugging**: Reproducing issues from user reports
- **Security testing**: Identifying potential exploits or crashes
- **Documentation**: Explaining edge cases to support team

---

## Inputs

1. **Feature specifications** (list): From CLI-002, what each command does
2. **Validation rules** (document): From QA-003, what inputs are invalid
3. **Business rules** (document): From BLE-002, what operations are forbidden
4. **State machine** (document): From BLE-003, what transitions are invalid
5. **Edge cases** (list): From QA-001, boundary conditions

---

## Step-by-Step Process

### Step 1: Identify Misuse Categories
Categorize types of user misuse and system failures.

**Misuse Categories**:

```
1. Invalid Input Misuse
   - Empty/null inputs
   - Wrong data types
   - Out-of-range values
   - Invalid formats
   - Injection attempts (SQL, command)

2. Command Misuse
   - Wrong command syntax
   - Missing required arguments
   - Conflicting flags
   - Unknown commands
   - Repeated rapid commands (spam)

3. State Misuse
   - Invalid state transitions
   - Attempting forbidden operations
   - Deleting non-existent items
   - Completing already-completed tasks
   - Operating on corrupted state

4. Concurrency/Race Conditions (Phase II+)
   - Simultaneous operations
   - Delete while listing
   - Modify while filtering
   - (Not applicable to Phase 1 single-user in-memory)

5. System Resource Misuse
   - Creating 100,000 tasks (memory exhaustion)
   - Very large command input (buffer overflow)
   - Repeated operations without cleanup (memory leak)

6. Environmental Misuse (Phase II+)
   - Database connection lost
   - Disk space exhausted
   - File permissions denied
   - (Not applicable to Phase 1 in-memory)

7. User Interface Misuse
   - Entering random characters
   - Copy-paste errors (extra spaces, newlines)
   - Undo/redo attempts (not supported in Phase 1)
   - Keyboard shortcuts not implemented
```

---

### Step 2: Design Negative Test Cases
Create detailed test cases for each misuse scenario.

**Negative Test Case Format**:

```
Test Case: [Name]
Category: [Misuse Type]
Description: [What user does]
Precondition: [System state before]
Input: [Exact user input/command]
Expected System Response:
  - Output: [What user sees/hears]
  - State Change: [How system state changes]
  - Error: [Error message if applicable]
  - Crash: [Does it crash? Should be NO]
  - Side Effects: [Any unintended changes]
Acceptance Criteria:
  - [ ] System does not crash
  - [ ] Helpful error message shown
  - [ ] State unchanged (or appropriate change)
  - [ ] No data corruption
Verification Method: [How to test this]
```

---

### Step 3: Negative Test Cases - Invalid Input
Document tests for invalid input misuse.

**Test Cases: Task Title**:

```
TC-1: Empty Task Title

Category: Invalid Input
Description: User tries to create task with empty title
Precondition: User is in main menu
Input: todo add ''
Expected System Response:
  Output: ✗ Error: Task title cannot be empty. Please provide a task title.
  State Change: No task created
  Error: Clear error message
  Crash: NO
Acceptance Criteria:
  - [ ] System shows error (not crash)
  - [ ] Error message is specific (not "Invalid input")
  - [ ] No task created
  - [ ] User can retry with valid input
Verification: Run command, verify error shown

---

TC-2: Whitespace-Only Title

Category: Invalid Input
Description: User creates task with only spaces
Precondition: Task list is empty
Input: todo add '     '
Expected System Response:
  Output: ✗ Error: Task title cannot be empty.
  State Change: No task created
  Error: Whitespace-only treated as empty
  Crash: NO
Acceptance Criteria:
  - [ ] Whitespace trimmed before validation
  - [ ] Error shown after trimming detects empty
  - [ ] No task created
Verification: Run command with various whitespace

---

TC-3: Title Too Long (Exceeds 255 chars)

Category: Invalid Input / Boundary
Description: User provides 300-character title
Precondition: Task list has space
Input: todo add '[300-char string]'
Expected System Response:
  Output: ✗ Error: Task title too long (300 chars). Max: 255
  State Change: No task created
  Error: Shows actual and max lengths
  Crash: NO
Acceptance Criteria:
  - [ ] Error shows actual character count
  - [ ] Error shows max allowed
  - [ ] Suggests how many to remove
  - [ ] No task created
  - [ ] No data corruption
Verification: Test with 254, 255, 256 character strings

---

TC-4: Title with Newlines

Category: Invalid Input
Description: User pastes multiline text as title
Precondition: Task list is empty
Input: todo add 'Buy
groceries'
Expected System Response:
  Output: ✗ Error: Task title cannot contain line breaks.
  State Change: No task created
  Error: Newlines explicitly rejected
  Crash: NO
Acceptance Criteria:
  - [ ] Newlines detected and rejected
  - [ ] Error message clear
  - [ ] No partial task created
Verification: Paste text with newlines

---

TC-5: Title with Special Characters

Category: Valid (edge case, not misuse)
Description: User creates task with special chars
Precondition: Task list is empty
Input: todo add 'Buy milk & bread @store #urgent'
Expected System Response:
  Output: ✓ Task created: task-001 'Buy milk & bread @store #urgent'
  State Change: Task created exactly as typed
  Crash: NO
Acceptance Criteria:
  - [ ] Special characters accepted
  - [ ] Exact text stored (no sanitization)
  - [ ] Task retrievable with special chars
  - [ ] No injection vulnerabilities
Verification: Create task, verify exact storage, search for it

---

TC-6: Title is Null (Not Provided)

Category: Invalid Input
Description: User runs add command without title
Precondition: User is in main menu
Input: todo add
Expected System Response:
  Output: ✗ Error: Missing task title. Usage: todo add <TITLE>
  State Change: No task created
  Error: Explains required argument
  Crash: NO
Acceptance Criteria:
  - [ ] Error shows this is required
  - [ ] Usage help provided
  - [ ] Suggests correct syntax
Verification: Run without argument

---

TC-7: Non-String Title (Numeric)

Category: Invalid Input / Type Error
Description: User provides number instead of string
Precondition: Task list is empty
Input: todo add 123
Expected System Response:
  Output: ✓ Task created: task-001 '123'
  State Change: Task created (numbers are valid text)
  Crash: NO
  Note: 123 is valid as string "123"
Acceptance Criteria:
  - [ ] Numeric input treated as string
  - [ ] Stored as "123"
Verification: Create task with number, verify storage
```

**Test Cases: Due Date**:

```
TC-8: Invalid Date Format

Category: Invalid Input / Format Error
Description: User provides date in wrong format
Precondition: Task list is empty
Input: todo add 'Meeting' --due 01/15/2026
Expected System Response:
  Output: ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD (e.g., 2026-01-15)
  State Change: No task created
  Error: Shows expected format and example
  Crash: NO
Acceptance Criteria:
  - [ ] Error shows what was provided
  - [ ] Error shows expected format
  - [ ] Example provided
  - [ ] No task created
Verification: Test with MM/DD/YYYY, DD/MM/YYYY, other formats

---

TC-9: Non-Existent Date (Feb 30)

Category: Invalid Input / Constraint Error
Description: User provides calendar date that doesn't exist
Precondition: Task list is empty
Input: todo add 'Task' --due 2026-02-30
Expected System Response:
  Output: ✗ Error: Invalid date '2026-02-30'. February has only 28 days.
  State Change: No task created
  Error: Explains why date is invalid
  Crash: NO
Acceptance Criteria:
  - [ ] Invalid calendar dates rejected
  - [ ] Explanation of why invalid
  - [ ] No task created
  - [ ] Suggestion of valid alternative
Verification: Test Feb 29 (non-leap year), Feb 30, Apr 31, etc.

---

TC-10: Date String with Extra Characters

Category: Invalid Input
Description: User provides date with trailing/leading garbage
Precondition: Task list is empty
Input: todo add 'Task' --due '2026-01-15 extra'
Expected System Response:
  Output: ✗ Error: Invalid date format. Expected YYYY-MM-DD
  State Change: No task created
  Error: Does not parse extra characters
  Crash: NO
Acceptance Criteria:
  - [ ] Exact format required
  - [ ] Extra characters cause failure
  - [ ] No partial parsing
Verification: Test with trailing/leading spaces, text

---

TC-11: Empty Date Flag Value

Category: Invalid Input
Description: User provides --due flag without value
Precondition: Task list is empty
Input: todo add 'Task' --due
Expected System Response:
  Output: ✗ Error: --due flag requires a date value. Usage: --due YYYY-MM-DD
  State Change: No task created
  Error: Clear about missing flag value
  Crash: NO
Acceptance Criteria:
  - [ ] Flag without value detected
  - [ ] Error is clear
  - [ ] Shows expected usage
Verification: Provide flag without value
```

**Test Cases: Priority**:

```
TC-12: Invalid Priority Value

Category: Invalid Input / Constraint Error
Description: User provides priority not in {low, normal, high}
Precondition: Task list is empty
Input: todo add 'Task' --priority urgent
Expected System Response:
  Output: ✗ Error: Invalid priority 'urgent'. Allowed: low, normal, high
  State Change: No task created
  Error: Lists valid values
  Crash: NO
Acceptance Criteria:
  - [ ] Invalid enum rejected
  - [ ] Valid options listed
  - [ ] No task created
Verification: Test with various invalid values (urgent, critical, 1, etc.)

---

TC-13: Priority with Wrong Case

Category: Invalid Input / Format Error
Description: User provides priority in uppercase
Precondition: Task list is empty
Input: todo add 'Task' --priority HIGH
Expected System Response:
  Output: ✗ Error: Invalid priority 'HIGH'. Use lowercase: high
  State Change: No task created
  Error: Explains case sensitivity
  Crash: NO
Acceptance Criteria:
  - [ ] Case sensitivity enforced
  - [ ] Error explains requirement
  - [ ] Correct case shown in error
Verification: Test HIGH, High, HiGh, etc.
```

---

### Step 4: Negative Test Cases - Command Misuse
Document tests for command misuse scenarios.

**Test Cases: Command Syntax**:

```
TC-14: Unknown Command

Category: Command Misuse
Description: User types command that doesn't exist
Precondition: User is in main menu
Input: todo ad 'Task'  (typo: "ad" instead of "add")
Expected System Response:
  Output: ✗ Error: Unknown command 'ad'. Did you mean 'add'?
  State Change: No operation performed
  Error: Suggests correct command
  Crash: NO
Acceptance Criteria:
  - [ ] Unknown command detected
  - [ ] Did-you-mean suggestion provided
  - [ ] List of available commands suggested
  - [ ] No crash
Verification: Test with various typos

---

TC-15: Unknown Flag

Category: Command Misuse
Description: User provides flag that doesn't exist for command
Precondition: Task list is empty
Input: todo add 'Task' --dur 2026-01-15  (typo: --dur instead of --due)
Expected System Response:
  Output: ✗ Error: Unknown flag '--dur' for 'add'. Did you mean '--due'?
  State Change: No task created
  Error: Suggests correct flag
  Crash: NO
Acceptance Criteria:
  - [ ] Unknown flag detected
  - [ ] Correct flag suggested
  - [ ] No task created
Verification: Test with various misspelled flags

---

TC-16: Conflicting Flags

Category: Command Misuse
Description: User provides conflicting options (hypothetical)
Precondition: Task list is empty
Input: todo add 'Task' --priority low --priority high  (duplicate flag)
Expected System Response:
  Output: ✗ Error: Priority specified twice. Use one value.
  State Change: No task created
  Error: Explains conflict
  Crash: NO
Acceptance Criteria:
  - [ ] Duplicate/conflicting flags detected
  - [ ] Error is clear
  - [ ] No task created
Verification: Provide same flag twice

---

TC-17: Missing Required Argument

Category: Command Misuse / Missing Input
Description: User runs command without required argument
Precondition: User is in main menu
Input: todo delete  (missing task ID)
Expected System Response:
  Output: ✗ Error: Missing task ID. Usage: todo delete <TASK_ID>
  State Change: No deletion
  Error: Shows required argument and usage
  Crash: NO
Acceptance Criteria:
  - [ ] Missing argument detected
  - [ ] Usage help provided
  - [ ] No operation performed
Verification: Run commands without required args
```

---

### Step 5: Negative Test Cases - State Misuse
Document tests for invalid state transitions.

**Test Cases: State Violations**:

```
TC-18: Complete Already-Completed Task

Category: State Misuse / Invalid Transition
Description: User tries to mark completed task as complete again
Precondition: Task task-001 exists and is completed
Input: todo complete task-001
Expected System Response:
  Output: ✗ Error: Task already completed: task-001 'Buy groceries'
  State Change: No state change
  Error: Clear that task is already done
  Crash: NO
Acceptance Criteria:
  - [ ] Double-complete prevented
  - [ ] Error is specific
  - [ ] State unchanged
  - [ ] No side effects
Verification: Create task, complete it, try to complete again

---

TC-19: Delete Non-Existent Task

Category: State Misuse / Resource Not Found
Description: User tries to delete task that doesn't exist
Precondition: Task list is empty (or task-999 doesn't exist)
Input: todo delete task-999
Expected System Response:
  Output: ✗ Error: Task not found: task-999
  State Change: No deletion
  Error: Clear which task not found
  Crash: NO
Acceptance Criteria:
  - [ ] Non-existent task detected
  - [ ] Error shows task ID
  - [ ] Helpful suggestion (run todo list to see tasks)
  - [ ] No task deleted
Verification: Delete non-existent task IDs

---

TC-20: Operate on Recently Deleted Task

Category: State Misuse / Race Condition (Phase 1 single-user, shouldn't happen)
Description: User deletes task, then tries to complete it
Precondition: Task task-001 exists
Input: todo delete task-001 (confirm yes)
        todo complete task-001  (immediate)
Expected System Response:
  Step 1: ✓ Task deleted: task-001 'Buy groceries'
  Step 2: ✗ Error: Task not found: task-001
  State Change: Task deleted, no completion
  Crash: NO
Acceptance Criteria:
  - [ ] First operation succeeds
  - [ ] Second operation fails gracefully
  - [ ] Clear error message
  - [ ] No crash
Verification: Delete task, immediately try to operate on it

---

TC-21: Invalid Task ID Format

Category: Invalid Input / Format Error
Description: User provides task ID in wrong format
Precondition: Task list contains some tasks
Input: todo complete 001  (missing "task-" prefix)
Expected System Response:
  Output: ✗ Error: Invalid task ID format '001'. Expected: task-NNN (e.g., task-001)
  State Change: No completion
  Error: Explains correct format
  Crash: NO
Acceptance Criteria:
  - [ ] Format validation works
  - [ ] Error shows expected format
  - [ ] Example provided
Verification: Test with various invalid formats
```

---

### Step 6: Negative Test Cases - Resource/Performance
Document tests for system resource misuse.

**Test Cases: System Limits**:

```
TC-22: Create Tasks Near Limit (1000 tasks in Phase 1)

Category: System Resource / Constraint
Description: User creates many tasks, approaching 1000-task limit
Precondition: Task list has 998 tasks
Input: todo add 'Task 999'
       todo add 'Task 1000'
       todo add 'Task 1001'  (exceeds limit)
Expected System Response:
  Task 999: ✓ Task created: task-999 'Task 999'
  Task 1000: ✓ Task created: task-1000 'Task 1000'
  Task 1001: ✗ Error: Cannot create task (limit of 1000 tasks reached)
  State Change: 1000 tasks total, no more created
  Crash: NO
Acceptance Criteria:
  - [ ] Tasks created up to limit
  - [ ] Limit enforced at 1000
  - [ ] Clear error at limit
  - [ ] No crash
  - [ ] Helpful suggestion (delete unused tasks)
Verification: Create tasks in batches, test at boundary

---

TC-23: Very Long Title Near Boundary

Category: Boundary Test
Description: User creates task with title at exact boundary (255 chars)
Precondition: Task list is empty
Input: todo add '[255-character string exactly]'
Expected System Response:
  Output: ✓ Task created: task-001 '[255-char title]'
  State Change: Task created with full 255 chars
  Crash: NO
Acceptance Criteria:
  - [ ] 255-char title accepted
  - [ ] Title stored in full (no truncation)
  - [ ] Task retrievable and searchable
Verification: Test with 254, 255, 256 character strings

---

TC-24: Very Large Input (Buffer Overflow Risk)

Category: System Resource / Security
Description: User provides extremely long input
Precondition: Task list is empty
Input: todo add '[10,000-character string]'
Expected System Response:
  Output: ✗ Error: Task title too long (10000 chars). Max: 255
  State Change: No task created
  Error: Shows length constraint
  Crash: NO
Acceptance Criteria:
  - [ ] Large input not causing buffer overflow
  - [ ] Handled gracefully
  - [ ] Error message clear
  - [ ] No crash or memory issues
Verification: Test with increasingly large inputs
```

---

### Step 7: Negative Test Cases - Concurrency (Phase II+, Document for Future)
Plan for future negative tests.

**Test Cases: Concurrency (Phase II+)**:

```
TC-25: Simultaneous Modifications (Phase II, Multi-User)

Category: Concurrency / Race Condition
Description: Two users modify same task simultaneously
Precondition: Task task-001 exists
Input User A: todo complete task-001
      User B: todo delete task-001  (same time)
Expected System Response (Phase II+):
  One operation succeeds, one fails with conflict error
  ✗ Error: Task was modified by another user. Refresh and try again.
  Crash: NO
  State: Consistent (either completed or deleted, not both)
Acceptance Criteria:
  - [ ] No crash
  - [ ] Clear conflict message
  - [ ] System state consistent
  - [ ] No data corruption
Note: Phase 1 doesn't apply (single-user, in-memory)
      Plan for Phase II+ with database
```

---

### Step 8: Validation Checklist for Negative Tests
Ensure comprehensive negative test coverage.

**Negative Test Coverage Checklist**:

```
✅ Invalid Input
  [ ] Empty/null required fields
  [ ] Wrong data types (number instead of string)
  [ ] Out-of-range values (title > 255 chars)
  [ ] Invalid formats (date format violations)
  [ ] Boundary violations (at exact limit)
  [ ] Special characters (handled correctly)
  [ ] Very large input (buffer overflow protection)

✅ Command Misuse
  [ ] Unknown commands
  [ ] Misspelled flags
  [ ] Missing required arguments
  [ ] Wrong argument types
  [ ] Conflicting flags

✅ State Violations
  [ ] Invalid state transitions (complete completed task)
  [ ] Operating on non-existent resources (delete non-existent)
  [ ] Operating on deleted resources (immediate reuse)
  [ ] Corrupted state recovery

✅ System Resilience
  [ ] Resource limit reached (1000 tasks)
  [ ] Memory exhaustion scenarios
  [ ] Rapid repeated commands (spam)
  [ ] Cleanup after failed operations

✅ Error Handling
  [ ] All errors have messages (no silent failures)
  [ ] Messages are specific (not generic)
  [ ] Messages are actionable (how to fix)
  [ ] No stack traces or technical jargon

✅ No Crashes
  [ ] Test doesn't cause crash/hang/freeze
  [ ] System recovers gracefully
  [ ] State consistent after error
  [ ] No data corruption
```

---

## Output

**Format**: Structured Markdown document with negative test catalog:

```markdown
# Negative Test Scenarios and Robustness Testing

## Misuse Categories
[Invalid input, command misuse, state violations, etc.]

## Negative Test Cases
[25+ detailed test cases with expected responses]

## System Response Guarantees
[What happens for every possible misuse]

## Error Message Catalog (from Negative Tests)
[All error messages expected from misuse scenarios]

## Robustness Checklist
[Ensuring no crashes or undefined behavior]

## Phase II+ Future Tests
[Tests planned for later phases with concurrency]
```

---

## Failure Handling

### Scenario 1: Test Crashes System
**Symptom**: Test case causes crash instead of error
**Resolution**:
- This IS a failure (system should not crash)
- Add crash recovery: Wrap operation in try-catch
- Add input validation: Validate before operation
- Fix code, add test to regression suite

### Scenario 2: Error Message Missing
**Symptom**: Invalid input causes no output (silent failure)
**Resolution**:
- This IS a failure (users should see error)
- Add error handling: "if invalid then error(...)"
- Show helpful message: Not generic "error occurred"
- Test: Verify error message shown

### Scenario 3: State Gets Corrupted
**Symptom**: After invalid operation, task list is corrupted
**Resolution**:
- This IS critical failure
- Add transaction semantics: "all-or-nothing" operations
- Test: Verify state unchanged on error
- Add rollback: "if error then undo changes"

### Scenario 4: Test Doesn't Cover Edge Case
**Symptom**: Bug found in production not in test suite
**Resolution**:
- Add new negative test for this case
- Ensure test fails with old code, passes with fix
- Document: "This case was missing"
- Prevent regression: Keep test in suite

### Scenario 5: Over-Defensive Code
**Symptom**: Test expects error, but code auto-corrects
**Resolution**:
- Sometimes auto-correction is good (trim whitespace)
- Document: "Whitespace auto-trimmed, not error"
- Test: Verify auto-correction works
- Boundary: Only auto-correct where safe

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Test suite generation**: Negative tests become regression suite
- **Bug reproduction**: Use these tests to reproduce reported issues
- **Code review**: Review error handling against these tests
- **Phase evolution**: Negative tests carry forward to Phase II+
- **Security testing**: Tests verify system not exploitable
- **Documentation**: Tests show system constraints to users

---

## Success Metrics

- ✅ No test case causes system crash
- ✅ All misuse scenarios have clear error message
- ✅ Error messages are specific (not generic)
- ✅ Error messages are helpful (show how to fix)
- ✅ System state unchanged when error occurs
- ✅ No silent failures (all errors reported)
- ✅ Resource limits enforced gracefully
- ✅ Invalid state transitions prevented
- ✅ 25+ negative test cases documented
- ✅ All test cases have clear pass/fail criteria

---

## Related Skills

- **Input Validation (QA-003)**: Prevents invalid input from reaching system
- **Error Messaging (QA-002)**: Provides helpful error messages for misuse
- **Business Rules (BLE-002)**: Prevent invalid operations
- **State Management (BLE-003)**: Prevent invalid state transitions
- **Edge Cases (QA-001)**: Boundary condition testing

---

## Example: Complete Negative Test Scenario

### Scenario: User Spams Create Command Rapidly

**Test**: Rapid task creation
```
Precondition: Task list is empty
Action 1: todo add 'Task 1'
Action 2: todo add 'Task 2'  (immediately after 1)
Action 3: todo add 'Task 3'  (immediately after 2)

Expected System Response:
  Action 1: ✓ Task created: task-001 'Task 1'
  Action 2: ✓ Task created: task-002 'Task 2'
  Action 3: ✓ Task created: task-003 'Task 3'

System Behavior:
  - All tasks created successfully
  - No crash or slowdown
  - Each task gets unique sequential ID
  - No tasks lost
  - No data corruption

Verification:
  - Run: todo list
  - Verify: 3 tasks shown
  - Verify: IDs are task-001, task-002, task-003
  - Verify: Titles match what was entered
  - Verify: Created timestamps are all valid
```

### Scenario: User Provides Injection Attempt

**Test**: SQL/Command injection attempt (security test)
```
Precondition: Task list is empty
Input: todo add 'Task'; DROP TABLE tasks; --'

Expected System Response:
  - Task created with exact title: 'Task'; DROP TABLE tasks; --'
  - No SQL execution
  - No command interpretation
  - No special meaning to semicolon, quotes, etc.

System Behavior:
  - Title stored as literal string
  - No interpretation of special syntax
  - No code injection possible
  - Task appears in list with exact title shown

Verification:
  - Run: todo list
  - Verify: Task shown with full title including semicolons
  - Run: todo search 'DROP'
  - Verify: Task found (search is literal)
  - Verify: No tables dropped
  - Verify: System still functional
```

---

## Conclusion

Phase 1 negative testing ensures the system is robust, predictable, and never crashes. Every misuse scenario has a clear, helpful error response. The system gracefully degrades and helps users correct their mistakes.

Negative tests are the safety net that catches bugs before they reach users.

