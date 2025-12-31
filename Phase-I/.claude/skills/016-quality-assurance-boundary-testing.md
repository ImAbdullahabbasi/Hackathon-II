# Skill: Boundary Condition Analysis and Testing

**Skill ID**: QA-005
**Agent Owner**: quality-assurance
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Systematically identify and test boundary conditions for all constrained inputs. This skill ensures the system handles edge cases correctly at the exact limits of allowed values (minimum, maximum, just-before-limit, just-after-limit). Boundary testing catches off-by-one errors, prevents data truncation, and ensures predictable behavior at constraint boundaries. Well-designed boundary tests provide confidence that the system works correctly across its entire valid range and fails gracefully outside valid ranges.

---

## When to Use

- **Test design phase**: After constraints are defined (QA-003)
- **Edge case analysis**: Before implementation
- **Bug reproduction**: When users report issues at limits
- **Code review**: Verifying boundary checks are correct
- **Performance testing**: Identifying performance cliffs at high volumes
- **Data integrity**: Ensuring data isn't lost at boundaries

---

## Inputs

1. **Input constraints** (document): From QA-003, all field limits
2. **Data model** (document): From DMD-001, field types and sizes
3. **Business rules** (document): From BLE-002, operational limits
4. **Negative tests** (document): From QA-004, invalid inputs
5. **Acceptance criteria** (document): From PA-001, what must work

---

## Step-by-Step Process

### Step 1: Identify All Boundaries
Map all constraints that have minimum/maximum limits.

**Boundary Categories**:

```
1. String Length Boundaries
   - Minimum length (e.g., title must be ≥ 1 char)
   - Maximum length (e.g., title must be ≤ 255 chars)
   - Boundary values: 0, 1, 254, 255, 256

2. Numeric Boundaries
   - Minimum value (e.g., task ID ≥ 1)
   - Maximum value (e.g., tasks ≤ 1000 in Phase 1)
   - Boundary values: min-1, min, max, max+1

3. Date Boundaries
   - Earliest allowed (e.g., year 1900)
   - Latest allowed (e.g., year 2099)
   - Calendar edge cases (leap years, month boundaries)
   - Boundary values: day 0, day 1, day 28, day 29, day 30, day 31

4. Enum Boundaries
   - Minimum enum value (first in list)
   - Maximum enum value (last in list)
   - Value just outside enum (invalid)
   - Boundary values: one before, first, last, one after

5. Collection Boundaries
   - Empty collection (0 items)
   - Single item (1 item)
   - Near capacity (999 items when max is 1000)
   - At capacity (1000 items)
   - Over capacity (1001 items)

6. Time-Based Boundaries
   - Midnight (00:00:00) - Phase II+
   - End of day (23:59:59) - Phase II+
   - Leap second - unlikely in Phase 1
```

---

### Step 2: Define Test Cases for Each Boundary
Create specific test cases at and around each boundary.

**Boundary Test Case Template**:

```
Boundary: [Field Name - Minimum/Maximum]
Constraint: [Rule, e.g., "title length 1-255 chars"]
Boundary Value: [The limit, e.g., 255]

Test Cases (Critical Values):
  Case A (Below minimum):
    Input: [Value just below minimum]
    Expected: [Should fail]
    Reason: [Why this value is invalid]

  Case B (At minimum):
    Input: [Exact minimum value]
    Expected: [Should succeed]
    Reason: [Minimum is valid]

  Case C (Just above minimum):
    Input: [Slightly above minimum]
    Expected: [Should succeed]
    Reason: [Above minimum is valid]

  Case D (Just below maximum):
    Input: [Value just below maximum]
    Expected: [Should succeed]
    Reason: [Below maximum is valid]

  Case E (At maximum):
    Input: [Exact maximum value]
    Expected: [Should succeed]
    Reason: [Maximum is inclusive (boundary)]

  Case F (Just above maximum):
    Input: [Value just above maximum]
    Expected: [Should fail]
    Reason: [Exceeds maximum limit]

  Case G (Far above maximum):
    Input: [Value far above maximum]
    Expected: [Should fail with clear error]
    Reason: [Grossly exceeds limit; should show error]
```

---

### Step 3: Boundary Test Cases - String Length
Test title and other string fields at boundaries.

**Boundary: Task Title Length (1-255 characters)**:

```
Constraint: Task title MUST be 1-255 characters
Rationale: 1 char minimum = must have content; 255 char maximum = prevent bloat

Test Cases:

TC-1: Title with 0 characters (Empty)
  Input: todo add ''
  Expected: ✗ Error: Task title cannot be empty
  Pass Criteria:
    - [ ] Error message shown
    - [ ] No task created
    - [ ] Task list unchanged
  Justification: 0 < 1 (minimum), so invalid

TC-2: Title with 1 character (At Minimum)
  Input: todo add 'A'
  Expected: ✓ Task created: task-001 'A'
  Pass Criteria:
    - [ ] Task created successfully
    - [ ] Title stored exactly as 'A'
    - [ ] Task retrievable
  Justification: 1 = 1 (at minimum), so valid

TC-3: Title with 2 characters (Just Above Minimum)
  Input: todo add 'AB'
  Expected: ✓ Task created: task-001 'AB'
  Pass Criteria:
    - [ ] Task created successfully
    - [ ] Title stored exactly
  Justification: 2 > 1 (above minimum), so valid

TC-4: Title with 254 characters (Just Below Maximum)
  Input: todo add '[254-char string]'
  Expected: ✓ Task created: task-001 '[254-char title]'
  Pass Criteria:
    - [ ] Task created
    - [ ] Full 254 characters stored (no truncation)
    - [ ] Task searchable
  Justification: 254 < 255 (below maximum), so valid

TC-5: Title with 255 characters (At Maximum)
  Input: todo add '[255-char string]'
  Expected: ✓ Task created: task-001 '[255-char title]'
  Pass Criteria:
    - [ ] Task created
    - [ ] Full 255 characters stored (no truncation)
    - [ ] Boundary: inclusive, not exclusive
    - [ ] Task appears in list with full title
  Justification: 255 = 255 (at maximum), so valid
  Critical: This is the off-by-one boundary; must be inclusive

TC-6: Title with 256 characters (Just Above Maximum)
  Input: todo add '[256-char string]'
  Expected: ✗ Error: Task title too long (256 chars). Max: 255
  Pass Criteria:
    - [ ] Error message shown
    - [ ] Error shows actual count (256)
    - [ ] Error shows max allowed (255)
    - [ ] No task created
  Justification: 256 > 255 (exceeds maximum), so invalid

TC-7: Title with 500 characters (Far Above Maximum)
  Input: todo add '[500-char string]'
  Expected: ✗ Error: Task title too long (500 chars). Max: 255
  Pass Criteria:
    - [ ] Error shown with actual count
    - [ ] Clear message about exceeding limit
    - [ ] No task created
  Justification: 500 >> 255 (far exceeds maximum), so invalid

Boundary Summary:
  Valid Range: 1-255 (inclusive)
  Invalid Below: 0 or less
  Invalid Above: 256 or more
  Critical Test: Exactly 255 (boundary must be inclusive)
  Off-by-One Risk: Could reject valid 255-char title if coded as < 255 instead of ≤ 255
```

---

### Step 4: Boundary Test Cases - Numeric Limits
Test numeric constraints like task count limits.

**Boundary: Task Count (0-1000 tasks in Phase 1)**:

```
Constraint: Phase 1 in-memory storage limited to 1000 tasks
Rationale: In-memory list has practical limit; prevents memory exhaustion

Test Cases:

TC-8: Creating task with 0 existing (Empty list)
  Precondition: Task list is empty
  Input: todo add 'Task 1'
  Expected: ✓ Task created: task-001 'Task 1'
  Pass Criteria:
    - [ ] First task created successfully
    - [ ] Task ID is task-001 (sequential from 1)
    - [ ] List transitions from 0 to 1 item
  Justification: 1 ≤ 1000 (within limit), so valid

TC-9: Creating task with 1 existing (Just above minimum)
  Precondition: Task list has 1 task
  Input: todo add 'Task 2'
  Expected: ✓ Task created: task-002 'Task 2'
  Pass Criteria:
    - [ ] Task created
    - [ ] Task ID is task-002 (next sequential)
    - [ ] List now has 2 items
  Justification: 2 ≤ 1000 (within limit), so valid

TC-10: Creating task with 999 existing (Just Below Limit)
  Precondition: Task list has 999 tasks
  Input: todo add 'Task 1000'
  Expected: ✓ Task created: task-1000 'Task 1000'
  Pass Criteria:
    - [ ] Task created successfully
    - [ ] Task ID is task-1000
    - [ ] List now has 1000 items
  Justification: 1000 ≤ 1000 (at limit), so valid

TC-11: Creating task with 1000 existing (At Limit)
  Precondition: Task list has exactly 1000 tasks
  Input: todo add 'Task 1001'
  Expected: ✗ Error: Cannot create task (limit of 1000 tasks reached)
  Pass Criteria:
    - [ ] Error shown with limit mentioned
    - [ ] No task created
    - [ ] Task count remains 1000
    - [ ] Helpful suggestion: "Delete unused tasks or upgrade to Phase II"
  Justification: 1001 > 1000 (exceeds limit), so invalid
  Critical: Boundary behavior at exactly 1000

TC-12: Attempting to create with 1001 existing (Over limit)
  Precondition: Task list has 1001 tasks (shouldn't happen, but test recovery)
  Input: todo add 'Task 1002'
  Expected: ✗ Error: Cannot create task (limit of 1000 tasks reached)
  Pass Criteria:
    - [ ] Error shown even though already over limit
    - [ ] No additional task created
    - [ ] Task count doesn't increase
  Justification: System should prevent exceeding limit, even if already over

Boundary Summary:
  Valid Range: 1-1000 (inclusive)
  Invalid Below: 0 tasks (empty list is valid, but cannot create if list is over-limit)
  Invalid Above: 1001 or more
  Critical Test: Exactly 1000 (boundary must block at 1001)
  Off-by-One Risk: Could allow 1001 if coded as ≤ 1000 instead of < 1000
```

---

### Step 5: Boundary Test Cases - Date Boundaries
Test date field limits and calendar edge cases.

**Boundary: Due Date (Valid Calendar Dates)**:

```
Constraint: Due date must be valid calendar date in YYYY-MM-DD format
Rationale: Invalid dates corrupt data; prevent Feb 30, Apr 31, etc.

Test Cases:

TC-13: Minimum Year (Year 1900 - Far Past)
  Input: todo add 'Task' --due 1900-01-01
  Expected: ✓ Task created with due_date='1900-01-01'
  Pass Criteria:
    - [ ] Very old date accepted (no date range restriction in Phase 1)
    - [ ] Task created successfully
    - [ ] Date stored correctly
  Justification: Phase 1 allows past dates (for backlog items)
  Note: Could add warning "Task due date is far in the past" but not error

TC-14: Typical Date (Today or near future)
  Input: todo add 'Task' --due 2026-01-15
  Expected: ✓ Task created with due_date='2026-01-15'
  Pass Criteria:
    - [ ] Task created successfully
    - [ ] Date stored exactly as provided
  Justification: Typical valid date, should work

TC-15: Maximum Year (Year 2099 - Far Future)
  Input: todo add 'Task' --due 2099-12-31
  Expected: ✓ Task created with due_date='2099-12-31'
  Pass Criteria:
    - [ ] Future date accepted
    - [ ] Task created successfully
  Justification: Phase 1 allows future dates
  Note: Could add warning "Task due date is far in the future" but not error

TC-16: Invalid Date - February 29 in Non-Leap Year
  Input: todo add 'Task' --due 2025-02-29
  Expected: ✗ Error: Invalid date '2025-02-29'. February has 28 days in 2025.
  Pass Criteria:
    - [ ] Invalid date rejected
    - [ ] Error explains why (2025 not leap year)
    - [ ] No task created
  Justification: 2025 is not a leap year; Feb 29 doesn't exist

TC-17: Valid Date - February 29 in Leap Year
  Input: todo add 'Task' --due 2024-02-29
  Expected: ✓ Task created with due_date='2024-02-29'
  Pass Criteria:
    - [ ] Leap year date accepted
    - [ ] 2024 is leap year, so Feb 29 is valid
    - [ ] Task created successfully
  Justification: 2024 is a leap year; Feb 29 is valid

TC-18: Invalid Date - April 31 (April has 30 days)
  Input: todo add 'Task' --due 2026-04-31
  Expected: ✗ Error: Invalid date '2026-04-31'. April has only 30 days.
  Pass Criteria:
    - [ ] Invalid day-in-month rejected
    - [ ] Error explains why
    - [ ] No task created
  Justification: April has 30 days, not 31

TC-19: Invalid Date - Month 0 (No month 0)
  Input: todo add 'Task' --due 2026-00-15
  Expected: ✗ Error: Invalid date '2026-00-15'. Month must be 1-12.
  Pass Criteria:
    - [ ] Invalid month rejected
    - [ ] Error explains valid range
  Justification: Months are 1-12, not 0-11

TC-20: Invalid Date - Month 13 (No month 13)
  Input: todo add 'Task' --due 2026-13-01
  Expected: ✗ Error: Invalid date '2026-13-01'. Month must be 1-12.
  Pass Criteria:
    - [ ] Invalid month rejected
    - [ ] Error is clear
  Justification: Months are 1-12, not 0-13

TC-21: Invalid Date - Day 0 (No day 0)
  Input: todo add 'Task' --due 2026-01-00
  Expected: ✗ Error: Invalid date '2026-01-00'. Day must be 1-31.
  Pass Criteria:
    - [ ] Invalid day rejected
    - [ ] Error explains valid range (1-31)
  Justification: Days start at 1, not 0

TC-22: Invalid Date - Day 32 (No day 32)
  Input: todo add 'Task' --due 2026-01-32
  Expected: ✗ Error: Invalid date '2026-01-32'. Day must be 1-31.
  Pass Criteria:
    - [ ] Invalid day rejected
    - [ ] Error is clear
  Justification: January has 31 days, not 32

Boundary Summary:
  Valid Range: Any valid calendar date (year 1-9999, month 1-12, day 1-31)
  Invalid: Non-existent dates (Feb 30, Apr 31, etc.)
  Critical Tests: Leap year handling (Feb 29), month boundaries, day boundaries
  Off-by-One Risk: Could reject day 31 if coded as < 31 instead of ≤ 31
```

---

### Step 6: Boundary Test Cases - Enum Boundaries
Test enum values at boundaries.

**Boundary: Priority Enum (low, normal, high)**:

```
Constraint: Priority MUST be one of: low, normal, high
Rationale: Ensures consistent priority values for filtering and sorting

Test Cases:

TC-23: First Enum Value
  Input: todo add 'Task' --priority low
  Expected: ✓ Task created with priority='low'
  Pass Criteria:
    - [ ] Task created with first enum value
    - [ ] Appears in low-priority filters
  Justification: "low" is first value in enum; should be accepted

TC-24: Middle Enum Value
  Input: todo add 'Task' --priority normal
  Expected: ✓ Task created with priority='normal'
  Pass Criteria:
    - [ ] Task created with middle enum value
    - [ ] Default when not specified
  Justification: "normal" is middle value; standard case

TC-25: Last Enum Value
  Input: todo add 'Task' --priority high
  Expected: ✓ Task created with priority='high'
  Pass Criteria:
    - [ ] Task created with last enum value
    - [ ] Appears in high-priority filters
  Justification: "high" is last value in enum; should be accepted

TC-26: Value Before First Enum
  Input: todo add 'Task' --priority critical
  Expected: ✗ Error: Invalid priority 'critical'. Allowed: low, normal, high
  Pass Criteria:
    - [ ] Value not in enum rejected
    - [ ] Error lists valid values
  Justification: "critical" is before "low" alphabetically; not in enum

TC-27: Value After Last Enum
  Input: todo add 'Task' --priority urgent
  Expected: ✗ Error: Invalid priority 'urgent'. Allowed: low, normal, high
  Pass Criteria:
    - [ ] Value not in enum rejected
    - [ ] Error lists valid values
  Justification: "urgent" is after "low" but not in enum

Boundary Summary:
  Valid Values: {low, normal, high} only
  Invalid: Any value outside this set
  Critical Test: Ensure no values accepted outside enum
  Off-by-One Risk: Could accidentally accept 4th value if enum boundary not enforced
```

---

### Step 7: Validation Checklist for Boundary Testing
Ensure comprehensive boundary coverage.

**Boundary Test Coverage Checklist**:

```
✅ String Length Boundaries
  [ ] Test minimum-1 (reject)
  [ ] Test minimum (accept)
  [ ] Test minimum+1 (accept)
  [ ] Test maximum-1 (accept)
  [ ] Test maximum (accept)
  [ ] Test maximum+1 (reject)
  [ ] Test far beyond maximum (reject with clear error)

✅ Numeric Boundaries
  [ ] Test 0 items (empty)
  [ ] Test 1 item (minimum)
  [ ] Test near max (n-1)
  [ ] Test at max (exactly at limit)
  [ ] Test over max (reject)
  [ ] Test far over (reject with clear error)

✅ Date Boundaries
  [ ] Test year 0, 1, 1900 (past)
  [ ] Test current year
  [ ] Test year 2099, 9999 (future)
  [ ] Test month 0, 1, 12, 13 (boundaries)
  [ ] Test day 0, 1, 28, 29, 30, 31, 32 (all boundaries)
  [ ] Test leap year Feb 29 (valid in leap year, invalid otherwise)
  [ ] Test month-specific day boundaries (Apr 31 invalid, etc.)

✅ Enum Boundaries
  [ ] Test first enum value (accept)
  [ ] Test last enum value (accept)
  [ ] Test value before first (reject)
  [ ] Test value after last (reject)

✅ Boundary Behavior
  [ ] All boundary tests have clear pass/fail
  [ ] Error messages specific for boundary violations
  [ ] No off-by-one errors
  [ ] No data truncation at boundaries
  [ ] No silent failures at limits

✅ Documentation
  [ ] Each boundary documented with justification
  [ ] Critical boundaries (like length limits) clearly marked
  [ ] Off-by-one risks identified
  [ ] Migration path clear for Phase II if limits change
```

---

## Output

**Format**: Structured Markdown document with boundary test catalog:

```markdown
# Boundary Condition Analysis and Testing

## Boundary Categories
[String length, numeric limits, dates, enums, collections]

## Complete Boundary Test Cases
[22+ detailed test cases with justification]

## Boundary Specification
[For each boundary: minimum, maximum, inclusive/exclusive]

## Off-By-One Risk Analysis
[Common coding errors and how to prevent]

## Test Coverage Matrix
[Which boundaries are tested, coverage percentage]
```

---

## Failure Handling

### Scenario 1: Off-By-One Error in Code
**Symptom**: Code rejects valid 255-char title (boundary should be ≤ 255)
**Resolution**:
- Test explicitly catches this: "255-char title should be accepted"
- Code review: Look for < 255 (should be ≤ 255)
- Fix: Change to ≤ 255
- Regression test: Add test that fails with old code, passes with fix

### Scenario 2: Data Truncation at Boundary
**Symptom**: 255-char title stored as 254 chars (truncation at boundary)
**Resolution**:
- Test verifies: Full 255 chars stored, no truncation
- Code review: Check storage mechanism doesn't truncate
- Fix: Ensure storage allocates full size
- Verify: Read back task, confirm full title present

### Scenario 3: Silent Failure at Limit
**Symptom**: User creates 1001st task, silently ignored (no error)
**Resolution**:
- Test expects error: "Cannot create task (limit of 1000)"
- Code must reject: Check count before creation
- Fix: Add validation before operation
- Verify: Error shown, task not created

### Scenario 4: Boundary Test Misses Edge Case
**Symptom**: Bug found at boundary not in test suite
**Resolution**:
- Add new boundary test for this case
- Ensure test fails with old code, passes with fix
- Document: "This edge case was missing"
- Prevent regression: Keep test in suite forever

### Scenario 5: Leap Year Handling Broken
**Symptom**: Feb 29, 2024 rejected (should be valid in leap year)
**Resolution**:
- Test explicitly includes leap year handling
- Code review: Verify leap year calculation correct
- Fix: Ensure leap year detection is correct (year % 4 == 0, except centuries)
- Test: Verify Feb 29 accepted in leap years, rejected otherwise

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **All constrained fields**: Apply same boundary analysis to new fields in Phase II+
- **Regression testing**: Boundary tests remain valid across phases
- **Performance testing**: Identify performance cliffs at high volumes
- **Data validation**: Boundary tests verify data quality
- **Documentation**: Tests explain limits to users
- **Future phases**: Scale boundaries (e.g., 1000 → 10,000 tasks) and re-test

---

## Success Metrics

- ✅ All constraints have identified boundaries
- ✅ Test cases cover: minimum-1, minimum, maximum, maximum+1
- ✅ Boundary tests explicit (not accidental coverage)
- ✅ Each boundary test has clear justification
- ✅ Off-by-one errors identified and tested
- ✅ Data not truncated at boundaries
- ✅ Error messages specific for boundary violations
- ✅ All boundary tests have clear pass/fail
- ✅ 22+ comprehensive boundary test cases
- ✅ Calendar edge cases covered (leap years, month boundaries)

---

## Related Skills

- **Input Validation (QA-003)**: Prevents inputs outside boundaries
- **Negative Testing (QA-004)**: Tests invalid inputs beyond boundaries
- **Edge Cases (QA-001)**: Identifies boundary conditions
- **Acceptance Criteria (PA-001)**: Tests verify acceptance criteria at boundaries

---

## Example: Complete Boundary Scenario

### Scenario: User Creates Task with 255-Character Title (At Boundary)

**Test Setup**:
```
Task: Create task with exactly 255-character title
Precondition: Task list is empty
Boundary: Task title max = 255 characters (inclusive)
Critical: Off-by-one error could reject valid 255-char title
```

**Test Execution**:
```
Step 1: Generate 255-character title
  title = "A" * 255  # Exactly 255 'A's

Step 2: Create task
  Input: todo add '[255-char string]'

Step 3: Verify creation
  Expected Output: ✓ Task created: task-001 '[255-char title]'

Step 4: Verify storage
  Run: todo get task-001
  Expected: Task retrieved with full 255-character title

Step 5: Verify searchability
  Run: todo search 'A'  (search for the character)
  Expected: Task-001 found in results

Step 6: Verify no truncation
  Run: todo list
  Expected: Task shown with full title (no truncation)
```

**Boundary Validation**:
```
✓ PASS: 255-char title accepted (at boundary)
✓ PASS: Title stored in full (no truncation)
✓ PASS: Title retrievable (not corrupted)

Off-By-One Risk: If code had used < 255 instead of ≤ 255:
  ✗ FAIL: 255-char title would be rejected
  This test explicitly catches that bug
```

---

### Scenario: User Creates Task with 1000th Task (At Limit)

**Test Setup**:
```
Task: Create task when list has exactly 999 tasks
Boundary: Task count limit = 1000 (inclusive)
Critical: Off-by-one error could allow 1001 or block valid 1000
```

**Test Execution**:
```
Step 1: Setup: Create 999 tasks
  For i = 1 to 999:
    todo add 'Task {i}'
  Result: Task list has 999 tasks

Step 2: Create 1000th task
  Input: todo add 'Task 1000'
  Expected Output: ✓ Task created: task-1000 'Task 1000'

Step 3: Verify count
  Run: todo list
  Verify: Exactly 1000 tasks shown

Step 4: Attempt to create 1001st task
  Input: todo add 'Task 1001'
  Expected Output: ✗ Error: Cannot create task (limit of 1000 tasks reached)

Step 5: Verify limit enforced
  Run: todo list
  Verify: Still exactly 1000 tasks (none added)
```

**Boundary Validation**:
```
✓ PASS: 999 tasks created successfully
✓ PASS: 1000th task created (at boundary)
✓ PASS: 1001st task rejected with clear error
✓ PASS: Boundary is inclusive at 1000, blocks at 1001

Off-By-One Risk: If code had used ≤ 1000 instead of < 1000 for checking:
  ✗ FAIL: Would allow 1001st task
  This test explicitly catches that bug
```

---

## Conclusion

Phase 1 boundary testing ensures the system works correctly across its entire valid range and fails gracefully at boundaries. Every constraint has explicit boundary tests that catch off-by-one errors, data truncation, and boundary violations. Boundary tests are the most effective way to find subtle bugs that only appear at the edges of valid input ranges.

Boundary tests are where the most hidden bugs live—find them proactively, not reactively.

