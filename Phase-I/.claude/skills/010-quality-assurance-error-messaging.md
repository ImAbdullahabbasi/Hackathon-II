# Skill: Human-Friendly Error Message Design

**Skill ID**: QA-002
**Agent Owner**: quality-assurance
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Design human-friendly error messages that convert technical failures into user-understandable explanations. This skill ensures error messages are clear, polite, actionable, and never expose technical implementation details. The goal is to help users understand what went wrong and how to fix it, rather than blaming them or showing stack traces. Good error messages reduce user frustration, support self-service problem-solving, and improve overall application experience.

---

## When to Use

- **Implementation phase**: When handling error conditions in code
- **Testing phase**: Validating error messages are helpful and accurate
- **User feedback analysis**: When users report confusion or frustration
- **Localization**: Before translating, ensure base messages are clear
- **Documentation**: Using error messages to guide users to solutions
- **Support training**: Teaching support staff how to explain errors to users

---

## Inputs

1. **Technical errors** (list): Error types from code (exceptions, validation failures, system errors)
2. **User scenarios** (list): When users encounter each error
3. **User personas** (optional): From CLI-003, non-technical to power users
4. **Phase 1 features** (list): Create, list, delete, complete, filter, search

---

## Step-by-Step Process

### Step 1: Categorize Errors
Group errors by type to ensure consistent handling.

**Error Categories**:

```
1. Input Validation Errors
   - Empty/missing required field
   - Invalid format (date, email, etc.)
   - Value out of range (too long, too short)
   - Invalid enum value (unknown priority)
   Example: User enters title as empty string

2. State Errors
   - Action invalid for current state (mark completed task as pending)
   - Resource already exists (create duplicate ID)
   - Resource doesn't exist (delete non-existent task)
   Example: User tries to delete task that doesn't exist

3. Resource Errors
   - Task not found
   - File not found
   - Storage full
   Example: User provides ID of task that was already deleted

4. System Errors
   - Out of memory
   - I/O failure
   - Network timeout
   Example: In-memory storage exhausted (rare for Phase 1)

5. User Errors
   - Unknown command
   - Invalid command syntax
   - Incorrect flag usage
   Example: User types "todo ad" instead of "todo add"

6. Conflict Errors
   - Conflicting options/flags
   - Circular dependencies
   Example: User tries to mark task complete and delete in same command

Error Distribution (Typical):
  Input validation: 60% (most common, user error)
  State errors: 20% (user misunderstanding)
  Resource errors: 15% (user forgot state)
  User errors: 5% (typos, syntax)
  System errors: <1% (rare)
  Conflict errors: <1% (rare)

Strategy:
  - Most effort on input validation (60%)
  - Moderate effort on state/resource (35%)
  - Minimal effort on system errors (requires rare scenarios)
```

---

### Step 2: Define Error Message Structure
Create a consistent template for all error messages.

**Error Message Template**:

```
✗ Error: <WHAT_WENT_WRONG>
  <EXPLANATION_IF_NEEDED>
  <SUGGESTION_HOW_TO_FIX>
```

**Components**:

```
1. Icon (✗ Error: or ⚠ Warning:)
   Purpose: Visual distinction from success (✓) or info (ℹ)
   Format: Symbol + "Error:" or "Warning:"
   Example: ✗ Error: Task title cannot be empty

2. Main Error Message (One Sentence)
   Purpose: Concise explanation of what went wrong
   Format: Clear, specific, past-tense or imperative
   Length: 1 sentence, < 100 characters if possible
   Tone: Polite, no blame ("cannot" not "invalid input you provided")
   Example: "Task title cannot be empty"
   Example: "Task not found: task-999"

3. Context/Explanation (Optional, If Ambiguous)
   Purpose: Additional detail if main message isn't sufficient
   Format: 1-2 sentences explaining why or what's possible
   When Use: Only if message alone wouldn't help
   Example: "Task title must contain at least one character."
   Example: "Expected format: YYYY-MM-DD (e.g., 2026-01-15)"

4. Actionable Fix Suggestion (Required)
   Purpose: How to resolve the error
   Format: Specific instruction or example
   When Use: Always, if possible
   Example: "Try: todo add 'Buy groceries'"
   Example: "Run 'todo list' to see all tasks"

5. Related Help (Optional, If Complex)
   Purpose: Link to documentation or related commands
   When Use: For errors with multiple possible causes
   Example: "For more info: todo delete --help"
   Example: "See: todo help filter"
```

**Template Examples**:

```
Simple (No Extra Context Needed):
  ✗ Error: Task title cannot be empty.
  Try: todo add 'Buy groceries'

With Context:
  ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD format.
  Try: todo add 'Meeting' --due 2026-01-15

With Suggestion + Help:
  ✗ Error: Task not found: task-999
  Run 'todo list' to see all existing tasks.
  Tip: Use the full task ID (e.g., task-001, task-002)

Complex Error with Multiple Causes:
  ✗ Error: Unknown command 'ad'. Did you mean 'add'?
  Available commands: add, list, get, complete, delete, search, filter, help
  Run 'todo help' for full command reference.
```

---

### Step 3: Map Technical Errors to User Messages
Create explicit mappings from code errors to user-friendly messages.

**Error Mapping Table**:

```
Technical Error         | User Message                      | Fix Suggestion
------------------------|-----------------------------------|-----------------
Empty string            | "Task title cannot be empty"      | "Try: todo add 'Buy milk'"
None/null input         | "Task title is required"          | "Provide a task title"
Length > 255            | "Title too long (300 chars)..."   | "Use 255 chars or less"
Length < 1              | "Title cannot be empty"           | "Provide a task title"
Invalid date format     | "Invalid date format..."          | "Use YYYY-MM-DD format"
Non-existent date       | "Invalid date '2026-02-30'..."    | "Did you mean 2026-02-28?"
Invalid enum value      | "Invalid priority 'urgent'..."    | "Use: low, normal, or high"
Resource not found      | "Task not found: task-999"        | "Run 'todo list' to see tasks"
Duplicate key           | "Task ID already exists"          | "System error; contact support"
Unknown command         | "Unknown command 'ad'..."         | "Did you mean 'add'? Run 'todo help'"
Invalid flag syntax     | "Invalid flag '--dur' for add"    | "Did you mean '--due'?"
Missing required arg    | "Missing task ID for delete"      | "Usage: todo delete <TASK_ID>"
Out of memory           | "Unable to create task (storage)" | "Delete unused tasks or restart"
File I/O error          | "Cannot read task data"           | "Check file permissions; restart"
Unexpected internal err | "An unexpected error occurred"    | "Please restart the application"
```

---

### Step 4: Design Category-Specific Error Messages
Create detailed messages for each error category.

**Input Validation Errors**:

```
Error Type: Empty Required Field

Technical Error Code:
  if not task_title:
    raise ValueError("Title is empty")

User Message:
  ✗ Error: Task title cannot be empty. Please provide a task title.
  Example: todo add 'Buy groceries'

Why This Works:
  - Uses "cannot" (polite) not "invalid input" (blaming)
  - Provides immediate example
  - Clear what action to take

---

Error Type: Invalid Format

Technical Error Code:
  if not date_matches_pattern(due_date, r'^\d{4}-\d{2}-\d{2}$'):
    raise ValueError("Invalid date format")

User Message (CURRENT):
  ✗ Error: Invalid date format

User Message (IMPROVED):
  ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD.
  Example: todo add 'Meeting' --due 2026-01-15

Why Better:
  - Shows what user provided ('01/15/2026')
  - Shows what was expected (YYYY-MM-DD)
  - Provides working example
  - User can immediately fix and retry

---

Error Type: Value Out of Range

Technical Error Code:
  if len(task_title) > 255:
    raise ValueError(f"Title too long: {len(task_title)}")

User Message (CURRENT):
  ✗ Error: Title too long

User Message (IMPROVED):
  ✗ Error: Task title too long (300 chars). Max allowed: 255 characters.
  Remove {300 - 255} = 45 characters to proceed.

Why Better:
  - Shows actual length (300)
  - Shows max allowed (255)
  - Tells user exactly how many to remove (45)
  - User knows exactly what to do

---

Error Type: Invalid Enum Value

Technical Error Code:
  valid_priorities = ['low', 'normal', 'high']
  if priority not in valid_priorities:
    raise ValueError(f"Invalid priority: {priority}")

User Message (CURRENT):
  ✗ Error: Invalid priority

User Message (IMPROVED):
  ✗ Error: Invalid priority 'urgent'. Allowed values: low, normal, high.
  Example: todo add 'Fix bug' --priority high

Why Better:
  - Shows what user provided ('urgent')
  - Lists all valid options
  - Provides working example
  - User knows exactly what to change
```

**State Errors**:

```
Error Type: Resource Not Found

Technical Error Code:
  task = find_task_by_id(task_id)
  if not task:
    raise TaskNotFoundError(f"Task {task_id} not found")

User Message (CURRENT):
  ✗ Error: Task not found

User Message (IMPROVED):
  ✗ Error: Task not found: task-999
  Run 'todo list' to see all existing tasks.
  Tip: Task IDs are shown in the list output (e.g., task-001, task-002)

Why Better:
  - Shows which task user tried to access (task-999)
  - Provides immediate way to see valid tasks (todo list)
  - Educates user about task ID format
  - User can recover by listing and trying again

---

Error Type: Action Invalid for State

Technical Error Code:
  if task.status == 'completed':
    raise InvalidStateError("Cannot mark completed task as pending")

User Message (CURRENT):
  ✗ Error: Invalid operation

User Message (IMPROVED):
  ✗ Error: Task is already completed. Mark it as pending instead?
  To undo completion: todo mark task-001 pending
  (Note: This feature may be added in Phase 2)

Why Better:
  - Explains current state (already completed)
  - Suggests what to do instead (mark as pending)
  - Shows how to do it if feature exists
  - Clear, helpful tone (not blaming)

---

Error Type: Conflicting Operations

Technical Error Code:
  if delete_requested and mark_complete_requested:
    raise ConflictError("Cannot delete and complete simultaneously")

User Message (CURRENT):
  ✗ Error: Conflicting options

User Message (IMPROVED):
  ✗ Error: Cannot both delete and complete a task simultaneously.
  Choose one:
    1. Mark complete: todo complete task-001
    2. Delete: todo delete task-001

Why Better:
  - Explains conflict clearly
  - Provides both options
  - User can choose which action to perform
```

**User Input Errors**:

```
Error Type: Unknown Command

Technical Error Code:
  command = parse_command(user_input)
  if command not in VALID_COMMANDS:
    raise UnknownCommandError(f"Unknown command: {command}")

User Message (CURRENT):
  ✗ Error: Unknown command

User Message (IMPROVED):
  ✗ Error: Unknown command 'ad'. Did you mean 'add'?
  Run 'todo help' to see all available commands.

Why Better:
  - Shows exactly what user typed ('ad')
  - Suggests did-you-mean correction
  - Provides way to discover all commands
  - Helpful, not blaming

Implementation of Did-You-Mean:
  Use Levenshtein distance (string similarity)
  If typed command is 1-2 chars different from valid command:
    → Suggest it
  Example:
    User types: "ad" (2 chars different from "add")
    Suggest: "Did you mean 'add'?"

    User types: "complete_task" (too different from "complete")
    Don't suggest (too many differences)

---

Error Type: Invalid Flag

Technical Error Code:
  if flag not in VALID_FLAGS:
    raise InvalidFlagError(f"Unknown flag: {flag}")

User Message (CURRENT):
  ✗ Error: Invalid flag

User Message (IMPROVED):
  ✗ Error: Unknown flag '--dur' for 'add' command. Did you mean '--due'?
  Valid flags: --due, --priority, --help
  Run 'todo add --help' for more information.

Why Better:
  - Shows what user typed (--dur)
  - Shows what was likely meant (--due)
  - Lists valid flags
  - Links to command help
  - User can correct and retry

---

Error Type: Missing Required Argument

Technical Error Code:
  if not task_id_provided:
    raise MissingArgumentError("Missing required argument: <TASK_ID>")

User Message (CURRENT):
  ✗ Error: Missing argument

User Message (IMPROVED):
  ✗ Error: Missing task ID. This command requires a task ID.
  Usage: todo delete <TASK_ID>
  Example: todo delete task-001
  Run 'todo list' to see all task IDs.

Why Better:
  - Explains what's missing (task ID)
  - Shows usage syntax
  - Provides concrete example
  - Tells user how to find valid IDs
  - User knows exactly what to do
```

---

### Step 5: Design Tone and Language
Establish consistent, friendly tone for all messages.

**Tone Principles**:

```
1. Be Polite, Not Blaming

Bad (Blaming):
  ✗ Error: Invalid input provided by user
  ✗ Error: You entered wrong data
  ✗ Error: Invalid argument (user error)

Good (Neutral/Polite):
  ✗ Error: Task title cannot be empty
  ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD.
  ✗ Error: Unknown command 'ad'. Did you mean 'add'?

Why?
  Users are frustrated when they make mistakes.
  Blaming them makes it worse.
  Neutral tone helps them focus on fixing it.

2. Use Simple, Clear Language

Bad (Jargon-Heavy):
  ✗ Error: TaskValidationException - required field missing
  ✗ Error: NullPointerException in parseDateString()
  ✗ Error: Serialization failed due to invalid JSON structure

Good (Clear):
  ✗ Error: Task title is required
  ✗ Error: Invalid date format
  ✗ Error: Cannot save task (unexpected error occurred)

Why?
  Non-technical users don't understand jargon.
  Simple language works for all users.
  Focus on what happened, not technical details.

3. Give Actionable Guidance

Bad (No Help):
  ✗ Error: Invalid input
  ✗ Error: Operation failed
  ✗ Error: Unexpected error

Good (Actionable):
  ✗ Error: Task title cannot be empty. Try: todo add 'Buy milk'
  ✗ Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-15)
  ✗ Error: Unable to complete task. Please restart the application.

Why?
  Users need to know how to fix it.
  Guidance reduces support tickets.
  Empowers users to self-serve.

4. Use Specific, Not Generic, Messages

Bad (Generic):
  ✗ Error: Invalid input
  ✗ Error: Operation failed
  ✗ Error: Something went wrong

Good (Specific):
  ✗ Error: Task title cannot be empty
  ✗ Error: Task not found: task-999
  ✗ Error: Storage full (no space for new tasks)

Why?
  Generic messages don't help.
  Specific messages explain actual problem.
  Users can understand and act on specifics.

5. Offer Options When Ambiguous

Bad (Single Path):
  ✗ Error: Invalid command

Good (Multiple Paths):
  ✗ Error: Unknown command 'mark'. Did you mean one of:
    - todo complete <TASK_ID> (mark as done)
    - todo mark <TASK_ID> <STATUS> (set custom status)
  Run 'todo help' to see all commands.

Why?
  Some errors have multiple causes.
  Offering options helps user find right path.
  Reduces guessing and retries.

Language Examples (Good Practices):

Use This:                      | Avoid This:
-------------------------------|-----------------------------------
"cannot" (user can try again) | "invalid" (blaming)
"required" (necessary)         | "missing" (blaming)
"expected" (what we need)      | "got" (what you provided, blaming)
"try" (suggestion)             | "must" (command)
"example" (show how)           | "usage" (abstract syntax)
"did you mean?" (helpful)      | "wrong" (blaming)
"run X to fix" (actionable)    | "error occurred" (helpless)
```

---

### Step 6: Design Context-Aware Messages
Tailor messages based on user level and context.

**Context-Aware Messaging**:

```
Same Error, Different Messages (Based on User Level):

Error: Invalid date format

For Beginner (First Time User):
  ✗ Error: Invalid date format '01/15/2026'.
  Expected format: YYYY-MM-DD (for example: 2026-01-15)
  Example: todo add 'Meeting' --due 2026-01-15

For Intermediate (Knows Basics):
  ✗ Error: Invalid date format. Use YYYY-MM-DD.
  Example: todo add 'Meeting' --due 2026-01-15

For Power User (Knows the App):
  ✗ Error: Invalid date '01/15/2026' (expected YYYY-MM-DD)

Detection Method:
  - First-time user: Show detailed explanation + example
  - Returning user: Show brief message + example
  - Power user: Show minimal message (assume knowledge)

Implementation:
  Keep basic message the same.
  Append additional detail based on user history/flags.
  Example:
    if is_first_time_user():
      append_tutorial_details()
    if is_power_user():
      use_brief_format()

---

Context: User Approaching Limit

Error: Cannot create more tasks (storage limit)

Message (Normal State):
  ✗ Error: Unable to create task. Phase 1 supports up to 1,000 tasks.
  You currently have 1,000 tasks.
  Delete unused tasks or upgrade to Phase 2.

Why Different?
  Normal: Storage is unlimited (unlikely to hit limit)
  Limit: User is at/near limit
    - Explain current situation (you have 1,000)
    - Explain limit (max 1,000)
    - Suggest solution (delete old tasks)

---

Context: Repeated Same Error

Error: Empty task title (user tried 3 times with same mistake)

First Attempt:
  ✗ Error: Task title cannot be empty.
  Try: todo add 'Buy groceries'

Second Attempt (User Still Doesn't Understand):
  ✗ Error: Task title cannot be empty.
  Please provide text for the task (what needs to be done?).
  Example: todo add 'Buy milk'
  (More explanation added)

Third Attempt (Obvious User Doesn't Understand Concept):
  ✗ Error: I need you to tell me what task to create.
  What is the task? (For example: 'Buy groceries', 'Call Mom', 'Fix the bug')
  Try: todo add 'YOUR TASK HERE'
  (Even simpler, more guidance)

Implementation:
  Track error count per session/user.
  Progressively add more explanation.
  Eventually suggest contacting support.
```

---

### Step 7: Handle System/Unexpected Errors
Design messages for errors beyond user control.

**System Error Messages**:

```
Category: Rare System Errors (Out of User Control)

Error: Out of Memory

User Message:
  ✗ Error: Cannot save task (memory limit reached).
  Try deleting unused tasks or restarting the application.

Why This Works:
  - Explains what happened (memory limit)
  - Is polite (not blaming)
  - Gives recovery steps (delete tasks, restart)
  - Doesn't show technical details

---

Error: File I/O Failure

User Message:
  ✗ Error: Cannot read task data (file access error).
  Check file permissions and ensure storage is accessible.
  If problem persists, contact support.

Why This Works:
  - Explains broad issue (file access)
  - Suggests what might help (check permissions)
  - Provides escalation path (contact support)
  - Doesn't show stack trace

---

Error: Unexpected Internal Error

User Message:
  ✗ Error: An unexpected error occurred.
  Please restart the application.
  If the problem continues, contact support with this info: [error-code]

Why This Works:
  - Honest that we don't know what happened
  - Provides immediate recovery step (restart)
  - Gives escalation path (support)
  - Provides error code for debugging (helps support team)

Never Show:
  - Stack traces
  - Internal function names
  - Line numbers
  - Variable values
  - Technical jargon

These Are For:
  - Logs (hidden from user)
  - Support engineers (when users contact support)
  - Developers (when debugging)
```

---

### Step 8: Validate Error Messages
Ensure messages meet quality standards.

**Error Message Validation Checklist**:

```
✅ Clarity
  [ ] Message is one sentence (if possible)
  [ ] No jargon or technical terms
  [ ] Explains what went wrong in plain English
  [ ] Readable by 10-year-old (comprehension test)

✅ Actionability
  [ ] Message suggests how to fix
  [ ] Suggestion is concrete (example, not vague)
  [ ] User can act on suggestion immediately
  [ ] No "good luck figuring it out" messages

✅ Tone
  [ ] Polite, not blaming
  [ ] Doesn't say "invalid input" (says "cannot be empty")
  [ ] Doesn't say "you did wrong" (says "expected X, got Y")
  [ ] Reassuring, not scary

✅ Completeness
  [ ] Shows what user provided (if applicable)
  [ ] Shows what was expected
  [ ] Shows how to fix it
  [ ] Suggests next steps (if needed)

✅ No Technical Leakage
  [ ] No stack traces
  [ ] No function names
  [ ] No line numbers
  [ ] No variable names/values (unless user-visible)
  [ ] No framework/library names

✅ Consistency
  [ ] Similar errors use similar phrasing
  [ ] Same terminology used throughout
  [ ] Format consistent (icon + message + suggestion)
  [ ] Capitalization consistent (start with capital)

✅ Brevity
  [ ] Main message < 100 characters (fits one line)
  [ ] Explanation < 3 additional lines if needed
  [ ] No redundancy (doesn't repeat itself)
  [ ] No unnecessary detail

Example Validation:

Bad Message:
  ✗ "ValueError in date_validator at line 42: date_str is None"
  Problems:
    [ ] Shows stack trace (bad)
    [ ] Shows function name (bad)
    [ ] Shows line number (bad)
    [ ] Doesn't say what to do (bad)
    [ ] Technical jargon (bad)

Good Message:
  ✗ Error: Task date is required. Use format YYYY-MM-DD.
  Example: todo add 'Meeting' --due 2026-01-15
  Checks:
    [✓] Clarity (one sentence, plain English)
    [✓] Actionability (shows format and example)
    [✓] Tone (polite, not blaming)
    [✓] Completeness (what went wrong, how to fix)
    [✓] No technical leakage (no jargon)
    [✓] Consistency (follows pattern)
    [✓] Brevity (concise)
```

---

## Output

**Format**: Structured Markdown document with error message catalog and mapping:

```markdown
# Human-Friendly Error Message Design

## Error Categories and Examples
[Input validation, state, resource, system, user input errors]

## Error Message Template
[Consistent structure: icon, what went wrong, how to fix]

## Error Message Catalog (Phase 1)
[Complete list of all errors with user messages]

## Error → Message Mapping
[Technical error to user message mapping table]

## Tone and Language Guidelines
[Principles for friendly, helpful messaging]

## Context-Aware Messaging
[Adapting messages by user level and context]

## System/Unexpected Errors
[Handling rare errors gracefully]

## Validation Checklist
[Quality standards for error messages]
```

---

## Failure Handling

### Scenario 1: Generic Error Message Used
**Symptom**: User sees "Error: Invalid input" (too vague)
**Resolution**:
- Replace with specific message: "Task title cannot be empty"
- Show what was expected: "Task title must be 1-255 characters"
- Provide example: "Try: todo add 'Buy groceries'"

### Scenario 2: Error Message Blames User
**Symptom**: "Error: You provided invalid date"
**Resolution**:
- Change tone: "Invalid date format provided" → "Invalid date format"
- Better: "Date must be in YYYY-MM-DD format (e.g., 2026-01-15)"
- Focus on what to do, not what they did wrong

### Scenario 3: Technical Details Leak
**Symptom**: User sees "TypeError: 'NoneType' object has no attribute 'title'"
**Resolution**:
- Never show stack traces to users
- Log technical error for debugging
- Show user: "Unable to save task (unexpected error occurred)"
- Provide: Error code for support ("Error code: #5042")

### Scenario 4: Error Message Is Too Long
**Symptom**: Error takes 5 lines and user doesn't read it all
**Resolution**:
- Main message: 1 sentence, < 100 characters
- Additional context: Only if essential
- Move advanced tips to "--help" output
- Example: Brief error, point to help: "Run 'todo add --help' for examples"

### Scenario 5: Error Repeats (User Doesn't Understand)
**Symptom**: User gets same error 3 times running same command
**Resolution**:
- First error: Concise explanation + example
- Second error: More detailed explanation
- Third error: Even simpler explanation + offer support
- Track repeated errors and escalate/expand help

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Phase II web app**: Same error messages on API responses and UI
- **API errors**: HTTP status codes + user-friendly message body
- **Chat/voice interfaces**: Same messages adapted for spoken language
- **Mobile apps**: Same messages adapted for mobile context
- **Localization**: Error messages are first to localize (high impact)
- **Support documentation**: Error messages serve as documentation
- **User education**: Messages teach users about system constraints

---

## Success Metrics

- ✅ No error message contains stack trace or technical jargon
- ✅ Every error message suggests how to fix it
- ✅ Error messages are polite (no blame)
- ✅ Error messages are specific (not generic "Error occurred")
- ✅ Main error message is < 100 characters (one line)
- ✅ Examples provided for format-specific errors
- ✅ Did-you-mean suggestions for typos/unknowns
- ✅ Consistent format (icon + message + suggestion)
- ✅ Messages use consistent terminology
- ✅ No user blame language ("invalid input you provided" → "cannot be empty")

---

## Related Skills

- **User Experience Design (CLI-003)**: Error messages are critical to UX
- **Command Design (CLI-002)**: Help text complements error messages
- **Edge Case Identification (QA-001)**: Tests identify all error scenarios
- **Acceptance Criteria (PA-001)**: Tests verify error messages are helpful

---

## Example: Phase 1 Complete Error Message Catalog

### Input Validation Errors

**Error #1: Empty Task Title**

```
Trigger: User runs: todo add ''
Technical Error: ValueError("Title is empty or None")

User Message:
  ✗ Error: Task title cannot be empty. Please provide a task title.
  Example: todo add 'Buy groceries'
```

**Error #2: Task Title Too Long**

```
Trigger: User runs: todo add '[300 character string]'
Technical Error: ValueError(f"Title exceeds max length: {len(title)}")

User Message:
  ✗ Error: Task title too long (300 chars). Max allowed: 255 characters.
  Your title needs to be {300-255} characters shorter.
```

**Error #3: Invalid Date Format**

```
Trigger: User runs: todo add 'Task' --due 01/15/2026
Technical Error: ValueError("Date format is not YYYY-MM-DD")

User Message:
  ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD.
  Example: todo add 'Meeting' --due 2026-01-15
```

**Error #4: Non-Existent Date**

```
Trigger: User runs: todo add 'Task' --due 2026-02-30
Technical Error: ValueError("Feb 30 does not exist")

User Message:
  ✗ Error: Invalid date '2026-02-30'. February has only 28 days.
  Did you mean 2026-02-28?
```

**Error #5: Invalid Priority Value**

```
Trigger: User runs: todo add 'Task' --priority urgent
Technical Error: ValueError("Priority must be low, normal, or high")

User Message:
  ✗ Error: Invalid priority 'urgent'. Allowed values: low, normal, high.
  Example: todo add 'Fix bug' --priority high
```

### State Errors

**Error #6: Task Not Found**

```
Trigger: User runs: todo delete task-999
Technical Error: TaskNotFoundError("Task task-999 does not exist")

User Message:
  ✗ Error: Task not found: task-999
  Run 'todo list' to see all existing tasks.
```

**Error #7: Task Already Completed**

```
Trigger: User runs: todo complete task-001 (already completed)
Technical Error: InvalidStateError("Task is already completed")

User Message:
  ✗ Error: Task is already completed: task-001 'Buy groceries'
  To undo: todo mark task-001 pending (feature coming in Phase 2)
```

### User Input Errors

**Error #8: Unknown Command**

```
Trigger: User runs: todo ad 'Buy milk'
Technical Error: UnknownCommandError("Unknown command: ad")

User Message:
  ✗ Error: Unknown command 'ad'. Did you mean 'add'?
  Run 'todo help' to see all available commands.
```

**Error #9: Invalid Flag**

```
Trigger: User runs: todo add 'Task' --dur 2026-01-15
Technical Error: UnknownFlagError("Unknown flag: --dur for add")

User Message:
  ✗ Error: Unknown flag '--dur' for 'add' command. Did you mean '--due'?
  Valid flags: --due, --priority, --no-confirm, --help
```

**Error #10: Missing Required Argument**

```
Trigger: User runs: todo delete (no task ID)
Technical Error: MissingArgumentError("Missing required argument: TASK_ID")

User Message:
  ✗ Error: Missing task ID. This command requires a task ID.
  Usage: todo delete <TASK_ID>
  Example: todo delete task-001
```

### System Errors

**Error #11: Out of Memory**

```
Trigger: Rare - user creates 10,000+ tasks
Technical Error: MemoryError("Out of memory")

User Message:
  ✗ Error: Cannot save task (memory limit reached).
  Try deleting unused tasks or restarting the application.
  Phase 2 will support database storage for unlimited tasks.
```

**Error #12: Unexpected Error**

```
Trigger: Unforeseen internal error
Technical Error: Exception("Internal error - see logs")

User Message:
  ✗ Error: An unexpected error occurred.
  Please restart the application.
  If the problem persists, contact support [error code: #5042].
```

---

## Conclusion

Phase 1 error messages are designed to be helpful, honest, and actionable. Key principles are:

1. **Clear**: Plain English, no jargon
2. **Specific**: Not generic "Error occurred"
3. **Polite**: No blame ("cannot be empty" not "invalid input")
4. **Actionable**: How to fix, not just what's wrong
5. **Complete**: What happened, why, and what to do

Error messages are the first line of support; good messages reduce support burden and improve user experience.

