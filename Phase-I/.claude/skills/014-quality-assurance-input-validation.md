# Skill: Input Validation Rules and Error Handling

**Skill ID**: QA-003
**Agent Owner**: quality-assurance
**Project**: Evolution of Todo Hackathon II – Phases 1-5
**Status**: Production

---

## Purpose

Define comprehensive input validation rules for all user inputs, specifying allowed formats, ranges, and constraints. This skill ensures invalid data never enters the system, prevents corruption, and guides users toward correct input with helpful error messages. Validation is the first line of defense against bugs, and well-defined validation rules make testing systematic and code review efficient.

---

## When to Use

- **Feature design phase**: After user input requirements are defined
- **Implementation planning**: Before coding input handlers
- **Test case generation**: Deriving valid/invalid test cases from validation rules
- **Code review**: Verifying all inputs are validated
- **Debugging**: Identifying where validation failed when bugs occur
- **Documentation**: Explaining to users what inputs are accepted

---

## Inputs

1. **Data model** (document): From DMD-001, field types and constraints
2. **Business rules** (document): From BLE-002, constraints and restrictions
3. **User stories** (list): From RA-001, what users expect to input
4. **Edge cases** (list): From QA-001, boundary conditions for inputs
5. **Command specifications** (document): From CLI-002, what inputs each command accepts

---

## Step-by-Step Process

### Step 1: Categorize All Inputs
Identify all places where user input enters the system.

**Input Categories**:

```
1. Command Inputs
   - Command name (todo add, todo list, etc.)
   - Command flags (--due, --priority, --filter)
   - Command arguments (task ID, search keyword)

2. Task Data Inputs (Create/Edit)
   - Task title (main input)
   - Due date (optional)
   - Priority (optional)
   - Description (Phase II+)
   - Category/Tags (Phase II+)

3. Filter/Search Inputs
   - Filter criteria (status, priority)
   - Sort field (created, due-date, priority)
   - Search keyword
   - Limit (max results)

4. User Confirmation Inputs
   - Yes/No confirmation prompts
   - Interactive mode responses

5. Configuration Inputs (Phase II+)
   - User preferences
   - Display settings
```

---

### Step 2: Define Validation Rules for Each Input
Create explicit validation rules for every input type.

**Task Title Validation**:

```
Field: task_title (required)
Type: string (text)
Source: User input (command argument or interactive prompt)

Constraints:
  - Required: YES (cannot be empty, null, or undefined)
  - Type: String (text characters only)
  - Length: Minimum 1 character, Maximum 255 characters
  - Characters: Any printable character allowed (no restrictions)
  - Whitespace: Leading/trailing whitespace TRIMMED (auto-correction)
  - Newlines: NOT ALLOWED (embedded line breaks forbidden)
  - Case: Any case accepted (no conversion applied)
  - Encoding: UTF-8 (supports unicode characters)

Validation Rules:
  1. Check if provided
     IF task_title is null OR undefined OR missing THEN
       error("Task title is required")

  2. Check if empty string
     IF task_title is empty string "" THEN
       error("Task title cannot be empty")

  3. Check if whitespace-only
     trimmed_title = task_title.trim()  # Remove leading/trailing spaces
     IF length(trimmed_title) == 0 THEN
       error("Task title cannot be only whitespace")

  4. Check length (after trimming)
     IF length(trimmed_title) < 1 THEN
       error("Task title must be at least 1 character")
     IF length(trimmed_title) > 255 THEN
       error("Task title too long ({actual} chars). Max: 255")

  5. Check for newlines
     IF contains(task_title, '\n') OR contains(task_title, '\r') THEN
       error("Task title cannot contain line breaks")

  6. Apply auto-corrections
     task_title = trimmed_title  # Use trimmed version

Error Messages:
  - "✗ Error: Task title is required. Provide a task title."
  - "✗ Error: Task title cannot be empty. Please provide a task title."
  - "✗ Error: Task title too long (300 chars). Max: 255 characters."
  - "✗ Error: Task title cannot contain line breaks."

Valid Examples:
  - "Buy groceries"
  - "Buy milk, bread, eggs"
  - "Send email to team@company.com"
  - "Fix bug #42: Username validation"
  - "🎯 Complete project"  (emoji allowed)
  - "Rencontrer à 10h30"  (accented characters allowed)

Invalid Examples:
  - ""  (empty)
  - "   "  (whitespace only)
  - "Buy\nmilk"  (contains newline)
  - None (null, not provided)
  - 123  (not a string)

Processing:
  Input: "  Buy groceries  " (with leading/trailing spaces)
  After trim: "Buy groceries"
  Stored: "Buy groceries" (trimmed, spaces removed)
```

**Due Date Validation**:

```
Field: due_date (optional)
Type: string (date)
Source: User input via --due flag

Constraints:
  - Required: NO (optional, defaults to null)
  - Type: String in YYYY-MM-DD format
  - Format: Exactly YYYY-MM-DD (4-digit year, 2-digit month, 2-digit day)
  - Date Range: Any valid calendar date (past, present, or future allowed)
  - Leap Year: Properly handle leap years (2024 is leap, 2025 is not)
  - Timezone: No timezone info (dates are assumed in user's local timezone)

Validation Rules:
  1. Check if provided
     IF due_date is not provided THEN
       due_date = null  (optional, skip validation)
       return  (no error)

  2. Check if not null
     IF due_date is null THEN
       return  (valid, no due date)

  3. Check format
     pattern = "^\d{4}-\d{2}-\d{2}$"  (regex pattern)
     IF due_date does not match pattern THEN
       error("Invalid date format '{due_date}'. Expected YYYY-MM-DD.")

  4. Parse date
     year, month, day = parse_date(due_date)
     IF parse fails THEN
       error("Invalid date '{due_date}'")

  5. Validate calendar date
     IF not is_valid_date(year, month, day) THEN
       IF month == 2 AND day == 30 THEN
         error("Invalid date '2026-02-30'. February has 28 days in 2026.")
       ELSE
         error("Invalid date '{due_date}'")

  6. Check date range (Phase 1)
     No restriction on past/future dates
     (Users can set task due in past for backlog items)

Error Messages:
  - "✗ Error: Invalid date format 'DDMMYYYY'. Expected YYYY-MM-DD (e.g., 2026-01-15)"
  - "✗ Error: Invalid date '2026-02-30'. February has only 28 days in 2026."
  - "✗ Error: Invalid date '2025-13-01'. Month must be 1-12."
  - "✗ Error: Invalid date '2026-01-32'. Day must be 1-31."

Valid Examples:
  - "2026-01-15"  (future date)
  - "2025-12-31"  (current year)
  - "2020-01-01"  (past date)
  - "2024-02-29"  (leap year date)
  - "2000-01-01"  (year 2000)

Invalid Examples:
  - "01/15/2026"  (MM/DD/YYYY format, wrong)
  - "2026-1-15"  (missing zero padding, wrong)
  - "15-01-2026"  (DD-MM-YYYY format, wrong)
  - "2026/01/15"  (slashes, wrong)
  - "2026-02-30"  (invalid calendar date)
  - "2026-13-01"  (month 13 doesn't exist)
  - "2026-01-32"  (day 32 doesn't exist)

Processing:
  Input: "2026-01-15"
  Check format: ✓ Matches YYYY-MM-DD
  Parse: year=2026, month=1, day=15
  Validate date: ✓ Valid calendar date
  Stored: "2026-01-15"

  Input: "2026-1-15"
  Check format: ✗ Does not match pattern (missing zero padding)
  Error: "Invalid date format '2026-1-15'. Expected YYYY-MM-DD (e.g., 2026-01-15)"
```

**Priority Validation**:

```
Field: priority (optional)
Type: enum
Source: User input via --priority flag

Constraints:
  - Required: NO (optional, defaults to "normal")
  - Type: Enum (one of: low, normal, high)
  - Case: Lowercase only (case-sensitive, "high" not "High")
  - Values: Exactly three choices: low, normal, high
  - No custom values allowed in Phase 1

Validation Rules:
  1. Check if provided
     IF priority is not provided THEN
       priority = "normal"  (default)
       return  (no error)

  2. Check if null
     IF priority is null THEN
       priority = "normal"  (default)
       return

  3. Check if valid enum value
     valid_values = {"low", "normal", "high"}
     IF priority NOT IN valid_values THEN
       error("Invalid priority '{priority}'. Allowed: low, normal, high")

  4. Case sensitivity
     IF priority is "High" OR "HIGH" OR "HIGH" (wrong case) THEN
       error("Invalid priority '{priority}'. Use lowercase: high")

Error Messages:
  - "✗ Error: Invalid priority 'urgent'. Allowed: low, normal, high"
  - "✗ Error: Invalid priority 'High'. Use lowercase: high"
  - "✗ Error: Invalid priority '1'. Use: low, normal, or high"

Valid Examples:
  - "low"  (valid)
  - "normal"  (valid)
  - "high"  (valid)
  - (not provided, defaults to "normal")

Invalid Examples:
  - "High"  (wrong case)
  - "urgent"  (not in enum)
  - "1"  (not text)
  - "critical"  (not in enum)

Processing:
  Input: --priority high
  Check: "high" in {low, normal, high}? ✓ YES
  Stored: priority="high"

  Input: --priority URGENT
  Check: "URGENT" in {low, normal, high}? ✗ NO
  Error: "Invalid priority 'URGENT'. Allowed: low, normal, high"
```

**Task ID Validation**:

```
Field: task_id (required for operations)
Type: string
Source: User input (command argument for delete, complete, get)

Constraints:
  - Format: "task-NNN" where NNN is 1-4 digits
  - Examples: "task-1", "task-001", "task-123", "task-9999"
  - Case: Lowercase "task" prefix (case-insensitive lookup acceptable)
  - Length: 5-9 characters total
  - Pattern: Exactly matches ^task-\d+$

Validation Rules:
  1. Check if provided
     IF task_id is not provided OR empty THEN
       error("Task ID is required")

  2. Check format
     pattern = "^task-\d+$"
     IF task_id does not match pattern THEN
       error("Invalid task ID format '{task_id}'. Expected: task-NNN (e.g., task-001)")

  3. Extract numeric part
     numbers = extract_digits(task_id)
     IF not valid integer THEN
       error("Invalid task ID")

  4. Check if task exists
     IF find_task_by_id(task_id) == null THEN
       error("Task not found: {task_id}")
       (separate error from format error)

  5. Case handling
     Internally: Convert to lowercase for lookup
     "TASK-001" → "task-001" (lookup works, case-insensitive)
     "Task-001" → "task-001" (lookup works, case-insensitive)

Error Messages:
  - "✗ Error: Task ID is required. Usage: todo delete <TASK_ID>"
  - "✗ Error: Invalid task ID format 'task-abc'. Expected: task-NNN (e.g., task-001)"
  - "✗ Error: Task not found: task-999"

Valid Examples:
  - "task-001"  (zero-padded)
  - "task-1"  (no padding)
  - "task-123"  (3 digits)
  - "TASK-001"  (case-insensitive, converted to lowercase)

Invalid Examples:
  - "task-abc"  (non-numeric)
  - "001"  (missing task prefix)
  - "task 001"  (space instead of dash)
  - "task-"  (no number)
  - "todo-001"  (wrong prefix)

Processing:
  Input: task-001
  Check format: ✓ Matches task-NNN
  Check exists: ✓ Task found in list
  Stored: task-001

  Input: task-999
  Check format: ✓ Matches task-NNN
  Check exists: ✗ Task not found
  Error: "Task not found: task-999"
```

**Search Keyword Validation**:

```
Field: keyword (required for search)
Type: string
Source: User input for "todo search" command

Constraints:
  - Required: YES (cannot search for empty keyword)
  - Type: String
  - Length: Minimum 1 character
  - Case: Case-insensitive by default
  - Characters: Any printable characters allowed
  - Wildcards: NOT supported in Phase 1 (literal string match)

Validation Rules:
  1. Check if provided
     IF keyword is not provided OR empty THEN
       error("Search keyword cannot be empty")

  2. Check if null
     IF keyword is null THEN
       error("Please provide a search term")

  3. Check minimum length
     IF length(keyword) < 1 THEN
       error("Search keyword must be at least 1 character")

  4. Trim whitespace
     keyword = keyword.trim()

  5. Check after trimming
     IF length(keyword) < 1 THEN
       error("Search keyword cannot be only whitespace")

Error Messages:
  - "✗ Error: Search keyword cannot be empty"
  - "✗ Error: Search keyword must be at least 1 character"

Valid Examples:
  - "grocery"  (simple word)
  - "buy milk"  (phrase with space)
  - "bug #42"  (special characters)

Invalid Examples:
  - ""  (empty)
  - "   "  (whitespace only)
  - (not provided)

Processing:
  Input: "grocery"
  Check: length > 0? ✓ YES
  Stored: keyword="grocery"
  Search: Find all tasks containing "grocery" (case-insensitive)

  Input: ""
  Check: length > 0? ✗ NO
  Error: "Search keyword cannot be empty"
```

**Filter Status Validation**:

```
Field: status (filter)
Type: enum
Source: User input via --filter flag

Constraints:
  - Type: Enum (pending, completed, all)
  - Default: "all" (if not provided)
  - Case: Lowercase
  - Values: Exactly three: pending, completed, all

Validation Rules:
  1. Check if provided
     IF status is not provided THEN
       status = "all"  (default)
       return

  2. Check if null
     IF status is null THEN
       status = "all"

  3. Check if valid value
     valid_values = {"pending", "completed", "all"}
     IF status NOT IN valid_values THEN
       error("Invalid filter '{status}'. Allowed: pending, completed, all")

Error Messages:
  - "✗ Error: Invalid filter 'done'. Allowed: pending, completed, all"

Valid Examples:
  - "pending"  (show only pending tasks)
  - "completed"  (show only completed)
  - "all"  (show both)
  - (not provided, defaults to "all")

Invalid Examples:
  - "active"  (not in enum)
  - "done"  (not in enum)
  - "Pending"  (wrong case)
```

---

### Step 3: Define Validation Strategies
Establish how and where validation happens.

**Validation Strategy**:

```
Validation Layers:

1. Input Reception Layer
   Where: CLI argument parser
   When: Immediately after user input received
   Action: Reject invalid format before processing
   Example: "--due INVALID" → reject before creating task

2. Type Conversion Layer
   Where: During data parsing
   When: Converting string to expected type
   Action: Validate type matches, convert if possible
   Example: "--priority high" → convert to enum value

3. Constraint Validation Layer
   Where: Before business logic
   When: Checking business constraints
   Action: Validate against rules (length, range, enum values)
   Example: title.length > 255 → reject

4. Business Logic Layer
   Where: During operation execution
   When: Before database/storage write
   Action: Final consistency check
   Example: Ensure due_date is not invalid for this user

5. Post-Validation Layer
   Where: After successful operation
   When: Confirm write succeeded
   Action: Verify data was stored correctly
   Example: Read back created task, confirm fields match

Timing:
  - Early validation is better (reject ASAP)
  - Fail fast principle: First error stops processing
  - Don't validate what doesn't need validating
```

---

### Step 4: Document Error Handling
Specify how to handle validation failures.

**Error Handling**:

```
For Each Validation Failure:

1. Detect Error (Constraint violated)
2. Halt Operation (Don't proceed with invalid data)
3. Prepare Error Message (Specific, helpful, actionable)
4. Show Error (Display to user)
5. Recover (Return to input prompt, allow retry)

Error Message Structure:
  ✗ Error: [WHAT_WENT_WRONG]
  [WHY_IT_MATTERS]
  [HOW_TO_FIX]

Example: Invalid date
  ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD.
  Example: todo add 'Meeting' --due 2026-01-15

Error Response Code (for API Phase II+):
  - 400 Bad Request (invalid input format)
  - 422 Unprocessable Entity (invalid business logic)
  - 404 Not Found (resource doesn't exist)

No Silent Failures:
  - Never ignore validation errors
  - Never truncate/modify invalid input to make it valid
    (Exception: trimming whitespace is acceptable auto-correction)
  - Always inform user what went wrong

Retry Path:
  - User sees error and tries again
  - Can correct error and resubmit
  - Should be obvious how to fix

No Generic Errors:
  Bad:   "✗ Error: Invalid input"
  Good:  "✗ Error: Task title too long (300 chars). Max: 255"
  Better: "✗ Error: Task title too long (300 chars). Max: 255.
           Remove at least 45 characters to proceed."
```

---

### Step 5: Validation Testing Strategy
Define how to test validation comprehensively.

**Test Coverage for Validation**:

```
For Each Input Field:

1. Valid Cases
   - Minimum valid value (e.g., title with 1 char)
   - Maximum valid value (e.g., title with 255 chars)
   - Typical valid value (e.g., "Buy groceries")
   - Edge cases within valid range

2. Invalid Cases
   - Empty/null (required fields)
   - Below minimum (too short)
   - Above maximum (too long)
   - Wrong type (string instead of number)
   - Wrong format (DDMMYYYY instead of YYYY-MM-DD)
   - Invalid enum value
   - Special characters/newlines
   - Whitespace-only
   - Boundary violations

3. Error Message Tests
   - Error message displayed? YES
   - Error message specific? (Not generic "error")
   - Error message actionable? (How to fix?)
   - Error message shows actual input? (What user typed)

Example Test Cases for due_date:
  ✓ Valid: "2026-01-15"
  ✓ Valid: "2000-01-01"
  ✗ Invalid: ""  (empty)
  ✗ Invalid: "01/15/2026"  (wrong format)
  ✗ Invalid: "2026-1-15"  (missing zero padding)
  ✗ Invalid: "2026-02-30"  (invalid date)
  ✗ Invalid: "2026-13-01"  (month 13)
  → Test each with specific error message
```

---

## Output

**Format**: Structured Markdown document with validation rules catalog:

```markdown
# Input Validation Rules and Error Handling

## Input Categories
[All places where user input enters system]

## Validation Rules by Input Type
[Detailed rules for task_title, due_date, priority, task_id, etc.]

## Validation Strategy
[When and how validation occurs]

## Error Handling
[How to respond to validation failures]

## Testing Strategy
[How to verify validation works correctly]

## Error Message Catalog
[All error messages for all validation failures]

## Phase Evolution
[How validation changes across phases]
```

---

## Failure Handling

### Scenario 1: Validation Rule Missing
**Symptom**: User enters text in priority field, system accepts it
**Resolution**:
- Add validation: "priority MUST be in {low, normal, high}"
- Code review catches: "No validation for priority enum"
- Test: Verify invalid priority rejected with error

### Scenario 2: Error Message Not Helpful
**Symptom**: User sees "Invalid input" for task title
**Resolution**:
- Make specific: "Task title too long (300 chars). Max: 255"
- Show what went wrong AND how to fix
- Test: Verify error message is actionable

### Scenario 3: No Auto-Correction Applied
**Symptom**: User enters "  Buy groceries  " (with spaces), rejected
**Resolution**:
- Apply auto-correction: Trim leading/trailing whitespace
- Acceptable auto-corrections: Whitespace trimming, lowercasing enums
- Don't auto-correct: Date format (keep exact), title case (keep original)

### Scenario 4: Validation Too Strict
**Symptom**: User cannot search for "&" character (special char)
**Resolution**:
- Allow special characters in most fields (title, search keyword)
- Only restrict where necessary (date format, enum values)
- Test: Verify special chars accepted where appropriate

### Scenario 5: Validation Order Wrong
**Symptom**: User sees format error for invalid due date, but it's actually year 9999 (edge case)
**Resolution**:
- Order validation: Format first, then validity
- Format check: "Is YYYY-MM-DD?"
- Validity check: "Is valid calendar date?"
- Clear error messages for each level

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Implementation**: Code validates per these rules
- **Test generation**: Rules become test cases
- **Documentation**: Validation rules serve as user guide
- **API design**: Phase II API uses same validation rules
- **Localization**: Error messages can be translated
- **Future phases**: Validation rules stay consistent across phases

---

## Success Metrics

- ✅ All inputs have explicit validation rules
- ✅ All constraints documented (format, range, type)
- ✅ All error messages are specific and helpful
- ✅ No silent failures (all errors shown)
- ✅ Auto-corrections minimal and safe (whitespace only)
- ✅ Validation happens early (reject invalid input ASAP)
- ✅ Error messages show what went wrong AND how to fix
- ✅ All edge cases covered (empty, null, boundary)
- ✅ Validation testable (test cases derived from rules)
- ✅ Consistent validation across all commands

---

## Related Skills

- **Business Rules (BLE-002)**: Constraints inform validation
- **Algorithms (BLE-001)**: Validation logic implemented
- **Error Messaging (QA-002)**: Error messages for validation failures
- **Acceptance Criteria (PA-001)**: Tests verify validation works
- **Edge Cases (QA-001)**: Tests verify edge cases handled

---

## Example: Complete Validation Scenario

### Scenario: User Creates Task with All Inputs

**Command**: `todo add 'Buy groceries' --due 2026-01-15 --priority high`

**Validation Chain**:

```
Input Received:
  - command: "add"
  - title_arg: 'Buy groceries'
  - flag_due: '2026-01-15'
  - flag_priority: 'high'

Step 1: Validate Command
  Command "add" in {add, list, delete, complete, search, filter, help}? ✓ YES
  Proceed

Step 2: Validate Task Title
  Check: title_arg provided? ✓ YES
  Check: not null? ✓ YES
  Trim: "Buy groceries" (already trimmed)
  Check: length > 0? ✓ YES (13 characters)
  Check: length ≤ 255? ✓ YES
  Check: no newlines? ✓ YES
  ✓ VALID: task_title = "Buy groceries"

Step 3: Validate Due Date
  Check: due_date provided? ✓ YES ('2026-01-15')
  Check: not null? ✓ YES
  Check: format matches YYYY-MM-DD? ✓ YES
  Parse: year=2026, month=1, day=15
  Check: valid calendar date? ✓ YES
  ✓ VALID: due_date = "2026-01-15"

Step 4: Validate Priority
  Check: priority provided? ✓ YES ('high')
  Check: in {low, normal, high}? ✓ YES
  Check: lowercase? ✓ YES
  ✓ VALID: priority = "high"

All Inputs Valid: ✓ YES
  Proceed to create task

Output:
  ✓ Task created: task-001 'Buy groceries' (due: 2026-01-15, priority: high)

Stored Task:
  {
    id: "task-001",
    title: "Buy groceries",
    status: "pending",
    created_timestamp: "2025-12-30T10:30:45Z",
    due_date: "2026-01-15",
    priority: "high",
    completed_timestamp: null
  }
```

### Scenario: User Creates Task with Invalid Inputs

**Command**: `todo add '  ' --due 01/15/2026 --priority urgent`

**Validation Chain**:

```
Input Received:
  - command: "add"
  - title_arg: '  '  (whitespace only)
  - flag_due: '01/15/2026'  (wrong format)
  - flag_priority: 'urgent'  (invalid value)

Step 1: Validate Command
  Command "add" valid? ✓ YES
  Proceed

Step 2: Validate Task Title
  Check: title_arg provided? ✓ YES
  Trim: "" (becomes empty after trim)
  Check: length > 0 after trim? ✗ NO
  ✗ INVALID: Task title cannot be empty

STOP HERE: First validation error found
  Don't proceed with other fields
  Show error and return to prompt

Output:
  ✗ Error: Task title cannot be empty. Please provide a task title.
  Example: todo add 'Buy groceries'

No Task Created: Operation halted at first error

Note: Other errors (invalid date, priority) not shown yet
  They would be shown if title validation passed
  Principle: Fail fast, fix one error at a time
```

---

## Conclusion

Phase 1 input validation is comprehensive, early, and helpful. Validation rules ensure:

1. **Data Integrity**: Only valid data enters system
2. **Predictability**: Users know what inputs work
3. **Helpfulness**: Error messages guide users to correct input
4. **Testability**: Validation rules become test cases
5. **Consistency**: Same validation across all commands

Input validation is the guardian against corrupted data.

