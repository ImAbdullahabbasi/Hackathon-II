# Skill: CLI Command Design and Interface Consistency

**Skill ID**: CLI-002
**Agent Owner**: cli-ux-designer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Design clear, consistent, and intuitive CLI commands for the Phase 1 todo application that follow Unix conventions and best practices. This skill ensures all commands are predictable, easy to learn, and forgiving to user input. Command design directly impacts user experience; poor UX leads to user errors and frustration, while good design enables users to discover commands intuitively and complete tasks quickly.

---

## When to Use

- **Feature design phase**: After functional analysis (CLI-001) is complete; before implementation
- **Command syntax design**: Deciding how users invoke each feature (command name, flags, arguments)
- **Help text and documentation**: Writing --help output and user guides
- **Error message design**: Crafting user-friendly error messages for invalid commands
- **Consistency review**: Ensuring all commands follow same patterns (no surprises)
- **Onboarding**: Designing initial help menu to guide new users

---

## Inputs

1. **Functional specifications** (document): From CLI-001, describing inputs/outputs for each feature
2. **User stories** (list): From RA-001, describing user intent
3. **Phase 1 features** (list): Create, list, delete, mark complete, filter, search (in scope)
4. **Unix conventions guide** (reference): Standard CLI patterns (POSIX, GNU)

---

## Step-by-Step Process

### Step 1: Establish Command Design Principles
Define guiding principles for all Phase 1 commands.

**Core Principles**:

```
1. Discoverability
   Users should discover commands naturally without memorizing syntax
   Example: "todo" (no args) → shows help menu
   Example: "todo --help" → shows all commands
   Example: "todo add --help" → shows add command help

2. Consistency
   All commands follow same patterns (verb-noun, same flag names)
   Example: All destructive commands require confirmation (--force flag)
   Example: All filter commands use --filter or specific flags (--status, --priority)

3. Forgiveness
   System should be forgiving of user mistakes (trim whitespace, case-insensitive)
   Example: "todo add '  Buy milk  '" → trims and creates task
   Example: "todo get TASK-001" → finds task-001 (case-insensitive)

4. Brevity
   Commands should be short enough to type (max 80 chars on terminal)
   Example: "todo add 'task'" → good (short)
   Example: "todo add --title 'task' --due-date 2026-01-15 --priority high --no-description" → verbose

5. Clarity
   Command intent should be obvious from command name and flags
   Example: "todo delete" → clearly deletes (destructive)
   Example: "todo done" → ambiguous (complete? finished? mark done?)
   Better: "todo complete" or "todo mark-complete"

6. Standard Patterns
   Commands should follow Unix conventions (verbs first, flags with --, etc.)
   Example: "todo add 'task'" → follows Unix pattern (command, then arguments)
   Example: "todo --add 'task'" → violates pattern (flags before verbs)
```

---

### Step 2: Define Command Hierarchy and Naming
Organize commands into logical groups with consistent naming.

**Command Hierarchy**:

```
todo                          # Main entry point (shows help)
├── add                       # Create new task
├── list                      # Display all tasks (or filtered)
├── get                       # Show single task details
├── update                    # Modify existing task
├── delete                    # Remove task
├── complete                  # Mark task as done
├── mark                      # Mark task with status
├── search                    # Find tasks by keyword
├── filter                    # Display tasks matching criteria
├── help                      # Show help text
└── version                   # Show app version

Naming Conventions:
  - Use present-tense verbs (add, not adding)
  - Use singular nouns (task, not tasks)
  - Avoid abbreviations (list, not ls; delete, not del; unless standard Unix shorthand)
  - Keep names short (1-2 words max)
  - Use hyphens for multi-word commands (mark-complete, not markcomplete)

Examples (Good):
  todo add 'Buy milk'
  todo list
  todo complete task-001
  todo delete task-001
  todo filter --status pending
  todo search 'grocery'

Examples (Bad):
  todo addition 'Buy milk'           # Wrong tense
  todo listing                        # Unnecessary suffix
  todo rm task-001                    # Too abbreviated, non-standard
  todo do-task task-001               # Awkward verb
```

---

### Step 3: Design Command Syntax (Arguments and Flags)
Define how each command accepts input (positional args vs. flags).

**Argument vs. Flag Guidelines**:

```
Positional Arguments (required, positional):
  - Use for main object of command (the thing being acted on)
  - Example: "todo delete <task_id>" → task_id is positional
  - Example: "todo add <title>" → title is positional

Named Flags (optional, --flag-name):
  - Use for options that modify behavior
  - Example: "todo add 'Task' --due 2026-01-15" → --due is flag
  - Example: "todo list --filter pending" → --filter is flag

Short Flags (single letter, -f):
  - Use for common flags only (help: -h, version: -v, force: -f)
  - Example: "todo -h" (short for --help)
  - Example: "todo list -s" (short for --status)

Boolean Flags (no value needed):
  - Use for true/false options
  - Example: "todo add 'Task' --no-notify" (disable notifications)
  - Example: "todo list --completed" (show only completed)

Value Flags (requires value):
  - Use for options that specify a value
  - Example: "todo add 'Task' --priority high"
  - Example: "todo list --sort due-date"
```

---

### Step 4: Design Individual Commands
Define syntax, flags, and behavior for each Phase 1 command.

**Command: todo add**

```
Purpose: Create a new task

Syntax:
  todo add <title> [OPTIONS]

Arguments:
  <title>
    Required: YES
    Type: string
    Description: Task title (what needs to be done)
    Constraints: 1-255 characters, non-empty
    Example: "Buy groceries"

Options:
  --due <DATE>, -d <DATE>
    Required: NO
    Type: date (YYYY-MM-DD)
    Description: Task deadline
    Default: null (no deadline)
    Example: --due 2026-01-15

  --priority <LEVEL>, -p <LEVEL>
    Required: NO
    Type: enum (low, normal, high)
    Description: Task importance level
    Default: normal
    Example: --priority high

  --no-confirm
    Required: NO
    Type: boolean flag
    Description: Skip confirmation prompt (create immediately)
    Default: false (show confirmation)

  --help, -h
    Required: NO
    Type: boolean flag
    Description: Show command help
    Default: false

Examples:
  Basic: todo add 'Buy milk'
  With deadline: todo add 'Submit report' --due 2026-01-15
  With priority: todo add 'Fix critical bug' --priority high --due 2026-01-10
  Multiple options: todo add 'Meeting' --priority high --due 2026-01-20 --no-confirm

Output on Success:
  ✓ Task created: task-001 'Buy milk'

Output on Error:
  ✗ Error: Task title cannot be empty
  ✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'
  ✗ Error: Invalid priority. Allowed: low, normal, high

Help Text:
  USAGE:
    todo add <TITLE> [OPTIONS]

  DESCRIPTION:
    Create a new task with the given title and optional deadline/priority

  ARGUMENTS:
    <TITLE>              Task title (required, 1-255 characters)

  OPTIONS:
    -d, --due <DATE>     Deadline (YYYY-MM-DD format)
    -p, --priority       Priority level (low, normal, high; default: normal)
    --no-confirm         Create without confirmation
    -h, --help           Show this help message

  EXAMPLES:
    todo add 'Buy groceries'
    todo add 'Fix bug' --priority high --due 2026-01-15
```

**Command: todo list**

```
Purpose: Display all tasks or filtered subset

Syntax:
  todo list [OPTIONS]

Options:
  --filter <STATUS>, -f <STATUS>
    Required: NO
    Type: enum (pending, completed, all)
    Description: Show only tasks with this status
    Default: all (show both pending and completed)
    Example: --filter pending

  --sort <FIELD>, -s <FIELD>
    Required: NO
    Type: enum (created, due-date, priority)
    Description: Sort by this field
    Default: created (sort by creation time, oldest first)
    Example: --sort priority

  --reverse, -r
    Required: NO
    Type: boolean flag
    Description: Reverse sort order
    Default: false (ascending order)

  --limit <N>
    Required: NO
    Type: integer
    Description: Show only first N tasks
    Default: all (no limit)

  --format <FORMAT>
    Required: NO
    Type: enum (table, json, simple)
    Description: Output format
    Default: table (human-readable table)
    Example: --format json

  --help, -h
    Required: NO
    Type: boolean flag
    Description: Show command help

Examples:
  All tasks: todo list
  Pending only: todo list --filter pending
  Completed only: todo list --filter completed
  Sorted by due date: todo list --sort due-date
  Latest first: todo list --reverse
  First 5: todo list --limit 5
  JSON output: todo list --format json

Output Format (Table, Default):
  ID        TITLE              STATUS    DUE DATE      PRIORITY
  --------  -----------------  --------  -----------   --------
  task-001  Buy groceries      pending   2026-01-15    normal
  task-002  Submit report      completed 2026-01-10    high
  task-003  Fix critical bug   pending   (no due date) high
  task-004  Plan next sprint   pending   (no due date) normal

Output Format (JSON):
  {
    "tasks": [
      {
        "id": "task-001",
        "title": "Buy groceries",
        "status": "pending",
        "due_date": "2026-01-15",
        "priority": "normal",
        "created_timestamp": "2025-12-30T10:30:45Z"
      },
      ...
    ],
    "total": 4,
    "filtered": true
  }

Output Format (Simple, Minimal):
  task-001: Buy groceries (pending, due: 2026-01-15)
  task-002: Submit report (completed)
  task-003: Fix critical bug (pending, priority: high)
  ...
```

**Command: todo get**

```
Purpose: Show details of a single task

Syntax:
  todo get <TASK_ID> [OPTIONS]

Arguments:
  <TASK_ID>
    Required: YES
    Type: string
    Description: Task identifier (e.g., task-001)
    Example: task-001

Options:
  --format <FORMAT>
    Type: enum (detailed, json, simple)
    Default: detailed (show all fields with formatting)
    Example: --format json

  --help, -h
    Type: boolean flag
    Description: Show command help

Examples:
  Basic: todo get task-001
  JSON: todo get task-001 --format json

Output (Detailed, Default):
  TASK ID:           task-001
  TITLE:             Buy groceries
  STATUS:            pending
  PRIORITY:          normal
  DUE DATE:          2026-01-15
  CREATED:           2025-12-30 10:30:45 UTC
  COMPLETED:         (not completed)

Output (JSON):
  {
    "id": "task-001",
    "title": "Buy groceries",
    "status": "pending",
    "priority": "normal",
    "due_date": "2026-01-15",
    "created_timestamp": "2025-12-30T10:30:45Z",
    "completed_timestamp": null
  }

Error Cases:
  ✗ Error: Task not found: task-999
```

**Command: todo complete** (Mark task as done)

```
Purpose: Mark a task as completed

Syntax:
  todo complete <TASK_ID> [OPTIONS]

Arguments:
  <TASK_ID>
    Required: YES
    Type: string
    Description: Task identifier
    Example: task-001

Options:
  --force, -f
    Type: boolean flag
    Description: Mark complete without confirmation
    Default: false (show confirmation)

  --help, -h
    Type: boolean flag

Examples:
  With confirmation: todo complete task-001
  Without confirmation: todo complete task-001 --force

Output on Success:
  ✓ Task marked complete: task-001 'Buy groceries'

Output (Confirmation Prompt):
  Mark task-001 'Buy groceries' as complete? (y/n) >

Error Cases:
  ✗ Error: Task not found: task-001
  ✗ Error: Task already completed: task-001
```

**Command: todo delete**

```
Purpose: Remove a task permanently

Syntax:
  todo delete <TASK_ID> [OPTIONS]

Arguments:
  <TASK_ID>
    Required: YES
    Type: string
    Description: Task identifier
    Example: task-001

Options:
  --force, -f
    Type: boolean flag
    Description: Delete without confirmation (dangerous!)
    Default: false (show confirmation)

  --help, -h
    Type: boolean flag

Examples:
  With confirmation: todo delete task-001
  Without confirmation: todo delete task-001 --force

Output (Confirmation Prompt):
  Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >

Output on Success:
  ✓ Task deleted: task-001 'Buy groceries'

Error Cases:
  ✗ Error: Task not found: task-001
```

**Command: todo search**

```
Purpose: Find tasks by title or keyword

Syntax:
  todo search <KEYWORD> [OPTIONS]

Arguments:
  <KEYWORD>
    Required: YES
    Type: string
    Description: Search term (searched in task titles)
    Example: "grocery"

Options:
  --case-sensitive
    Type: boolean flag
    Description: Case-sensitive search (default: case-insensitive)
    Default: false

  --status <STATUS>, -s <STATUS>
    Type: enum (pending, completed, all)
    Description: Search only within this status
    Default: all

  --limit <N>
    Type: integer
    Description: Maximum results to return
    Default: all

  --help, -h
    Type: boolean flag

Examples:
  Basic search: todo search 'grocery'
  Case-sensitive: todo search 'Grocery' --case-sensitive
  Pending only: todo search 'fix' --status pending

Output:
  Found 3 matches:
    task-001: Buy groceries (pending)
    task-003: Grocery shopping (pending)
    task-005: Need groceries (completed)

Output (No Matches):
  No tasks found matching 'nonexistent'
```

**Command: todo filter**

```
Purpose: Display tasks matching multiple criteria (alternative to list with filters)

Syntax:
  todo filter [OPTIONS]

Options:
  --status <STATUS>
    Type: enum (pending, completed)
    Description: Filter by status

  --priority <LEVEL>
    Type: enum (low, normal, high)
    Description: Filter by priority

  --due-after <DATE>
    Type: date (YYYY-MM-DD)
    Description: Show tasks due after this date

  --due-before <DATE>
    Type: date (YYYY-MM-DD)
    Description: Show tasks due before this date

  --due-today
    Type: boolean flag
    Description: Show tasks due today

  --overdue
    Type: boolean flag
    Description: Show overdue tasks (due date < today)

  --help, -h
    Type: boolean flag

Examples:
  High priority pending: todo filter --status pending --priority high
  Overdue: todo filter --overdue
  Due this week: todo filter --due-before 2026-01-10 --due-after 2026-01-05
  Today: todo filter --due-today

Output:
  (Same table format as "todo list")
```

**Command: todo help**

```
Purpose: Show help and command reference

Syntax:
  todo help [COMMAND]

Arguments:
  [COMMAND]
    Required: NO
    Type: string
    Description: Show help for specific command (if not provided, show all commands)
    Example: add

Examples:
  All commands: todo help
  Specific command: todo help add
  Same as: todo add --help

Output (All Commands):
  TODO - A simple task management CLI

  USAGE:
    todo <COMMAND> [ARGUMENTS] [OPTIONS]

  COMMANDS:
    add <TITLE>      Create a new task
    list [OPTIONS]   Display tasks
    get <ID>         Show task details
    complete <ID>    Mark task as done
    delete <ID>      Remove a task
    search <KEYWORD> Find tasks by keyword
    filter [OPTIONS] Find tasks by criteria
    help [COMMAND]   Show this help text
    version          Show version information

  OPTIONS (global):
    -h, --help       Show help
    -v, --version    Show version

  Get help on a specific command:
    todo help add
    todo add --help
```

**Command: todo version**

```
Purpose: Display application version

Syntax:
  todo version

Output:
  todo version 1.0.0
  (or: Evolution of Todo Phase 1, v1.0.0)
```

**Command: Main Entry Point (no command)**

```
Purpose: Show help when user runs "todo" with no arguments

Syntax:
  todo

Output (Default, Show Quick Help):
  TODO - A simple task management CLI v1.0.0

  QUICK START:
    Create task:   todo add 'Task title'
    List tasks:    todo list
    Complete:      todo complete task-001
    Delete:        todo delete task-001
    Search:        todo search 'keyword'
    Help:          todo help

  Run "todo help" for full command reference
  Run "todo <command> --help" for command-specific help
```

---

### Step 5: Define Error Handling and Messages
Design error messages that are helpful and unambiguous.

**Error Message Principles**:

```
1. Be Specific
   Bad: "Error: Something went wrong"
   Good: "✗ Error: Task title cannot be empty"
   Better: "✗ Error: Task title cannot be empty. Please provide a task title."

2. Show What User Did
   Bad: "Invalid input"
   Good: "✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'"

3. Suggest How to Fix
   Bad: "Date error"
   Good: "✗ Error: Invalid date '2026-02-30'. February has only 28 days in 2026."
   Better: "✗ Error: Invalid date '2026-02-30'. Did you mean 2026-02-28?"

4. Use Consistent Format
   Error: "✗ Error: <description>"
   Warning: "⚠ Warning: <description>"
   Success: "✓ <description>"
   Info: "ℹ <description>"

5. Avoid Jargon
   Bad: "NullPointerException in parseDate()"
   Good: "Task title cannot be empty"

Example Error Messages:

Empty Title:
  ✗ Error: Task title cannot be empty. Please provide a task title.

Title Too Long:
  ✗ Error: Task title too long (300 chars). Max allowed: 255

Invalid Date:
  ✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'

Non-Existent Task:
  ✗ Error: Task not found: task-999

Invalid Priority:
  ✗ Error: Invalid priority 'urgent'. Allowed values: low, normal, high

Unknown Command:
  ✗ Error: Unknown command 'add-new'
  Did you mean: 'add'?

Missing Required Argument:
  ✗ Error: Missing required argument <TASK_ID>
  Usage: todo delete <TASK_ID> [OPTIONS]
  Run 'todo delete --help' for more information
```

---

### Step 6: Design Help and Documentation
Create consistent help text and documentation.

**Help Text Structure**:

```
<COMMAND DESCRIPTION>

USAGE:
  <command syntax>

DESCRIPTION:
  <what the command does, 1-2 sentences>

ARGUMENTS:
  <arg-name>    Description of argument

OPTIONS:
  -s, --short   Description of option
  -l, --long    Description with more detail

EXAMPLES:
  $ example command 1
  $ example command 2

SEE ALSO:
  <related commands>
```

**Example Help Text (todo add)**:

```
USAGE:
  todo add <TITLE> [OPTIONS]

DESCRIPTION:
  Create a new task with the given title. Optionally set a deadline and
  priority level.

ARGUMENTS:
  <TITLE>              Task title (required, 1-255 characters)

OPTIONS:
  -d, --due <DATE>     Deadline in YYYY-MM-DD format
  -p, --priority LEVEL Priority level: low, normal, or high (default: normal)
  --no-confirm         Create task without confirmation prompt
  -h, --help           Show this help message

EXAMPLES:
  Create a task with title only:
    $ todo add 'Buy groceries'

  Create a task with deadline and priority:
    $ todo add 'Fix critical bug' --priority high --due 2026-01-15

  Create without confirmation:
    $ todo add 'Quick task' --no-confirm

SEE ALSO:
  todo list, todo get, todo delete, todo help
```

---

### Step 7: Validate Command Design
Ensure all commands are consistent and user-friendly.

**Command Design Validation Checklist**:

```
✅ Consistency
  [ ] All commands use present-tense verbs
  [ ] All commands use singular nouns
  [ ] All commands follow same argument order (command, then args, then flags)
  [ ] All destructive commands have confirmation prompts (unless --force)
  [ ] All filter commands use same --filter/--sort/--limit naming

✅ Clarity
  [ ] Command names clearly indicate what they do
  [ ] No ambiguous names (done vs. complete, rm vs. delete)
  [ ] Flag names are unambiguous (not "s" for both sort and status)
  [ ] Help text is clear and concise

✅ Usability
  [ ] Common commands are short (add, list, get, delete)
  [ ] Long commands have short equivalents (-h for --help, -d for --due)
  [ ] Defaults are sensible (priority defaults to "normal", status to "all")
  [ ] Commands are forgiving (trim whitespace, case-insensitive where sensible)

✅ Discoverability
  [ ] "todo" with no args shows quick help
  [ ] "todo help" shows all commands
  [ ] "todo <command> --help" shows command-specific help
  [ ] Related commands mentioned in help text

✅ Error Handling
  [ ] Error messages are specific (not generic "error")
  [ ] Error messages suggest how to fix
  [ ] Unknown commands suggest did-you-mean
  [ ] Required arguments show usage on error

✅ Output Consistency
  [ ] Success messages start with ✓
  [ ] Error messages start with ✗
  [ ] Warning messages start with ⚠
  [ ] All messages end with period (if complete sentence)
```

---

## Output

**Format**: Structured Markdown document with command reference and design guidelines:

```markdown
# CLI Command Design Reference

## Design Principles
[Core principles for all commands]

## Command Hierarchy
[Tree of all commands]

## Individual Commands
[Detailed specification for each command]

## Error Messages
[Error message examples and guidelines]

## Help Text Format
[Template for help text]

## Validation Checklist
[Checklist confirming all commands follow design]

## Unix Conventions Reference
[Brief reference to relevant Unix standards]
```

---

## Failure Handling

### Scenario 1: Command Names Conflict with System Commands
**Symptom**: User runs "todo add" but system has other "add" commands (file manager, etc.)
**Resolution**:
- Keep "todo" as the main command (adds namespace)
- Example: "todo add", not just "add"
- This prevents conflicts with system utilities

### Scenario 2: Too Many Flags (Command Too Verbose)
**Symptom**: "todo add 'Task' --due 2026-01-15 --priority high --no-confirm --format json --dry-run"
**Resolution**:
- Limit flags to 3-5 per command (more = harder to use)
- Move advanced options to separate commands or phases
- Example: Phase 1 keeps only --due, --priority, --no-confirm
- Example: Phase II adds --format, --description, etc.

### Scenario 3: Inconsistent Flag Names Across Commands
**Symptom**: "todo list --status pending" vs. "todo filter --filter completed"
**Resolution**:
- Standardize flag names (--status for all status filters)
- Use same names across commands
- Document standard flags: --status, --priority, --sort, --limit

### Scenario 4: Help Text Is Too Long
**Symptom**: "todo add --help" shows 50 lines of documentation
**Resolution**:
- Keep help text concise (max 20 lines)
- Show basic examples (2-3 most common)
- Link to detailed docs for advanced usage
- Example: "Run 'todo help add' for more examples"

### Scenario 5: Ambiguous Command Names
**Symptom**: Is "todo mark" marking as complete, or marking for deletion?
**Resolution**:
- Use specific verb-noun pairs
- "todo complete" (not mark, done, finish)
- "todo delete" (not remove, rm, trash)
- "todo update" (not edit, modify, change)

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Phase II web UI**: API commands can mirror CLI command structure
- **Phase III chatbot**: Natural language commands map to CLI commands
- **API design**: REST endpoints can follow same naming conventions
- **Other CLI tools**: Same principles apply to other projects

---

## Success Metrics

- ✅ All commands follow consistent verb-noun pattern
- ✅ All destructive commands require confirmation (unless --force)
- ✅ All commands have --help flag
- ✅ Help text is clear and includes examples
- ✅ Error messages are specific and suggest fixes
- ✅ No command exceeds 80 characters on typical terminal
- ✅ Common operations are reachable in 1-2 commands
- ✅ All flag names are unambiguous and consistent
- ✅ Defaults are sensible (users rarely need flags)
- ✅ Commands follow Unix conventions (verbs first, flags at end)

---

## Related Skills

- **Functional Analysis (CLI-001)**: Defines what each command does (inputs/outputs)
- **Acceptance Criteria (PA-001)**: Tests verify commands work as specified
- **Quality Assurance (QA-001)**: Tests error cases and edge cases

---

## Example: Complete Phase 1 Command Reference

### Quick Reference

```
Create task:         todo add 'Task title'
List tasks:          todo list
Show task details:   todo get task-001
Complete task:       todo complete task-001
Delete task:         todo delete task-001
Search tasks:        todo search 'keyword'
Find tasks:          todo filter --status pending
Show help:           todo help
Show version:        todo version
```

### Detailed Commands

(See Step 4 above for full command specifications)

### Common Workflows

**Workflow 1: Create and Complete Task**
```bash
$ todo add 'Buy groceries'
✓ Task created: task-001 'Buy groceries'

$ todo list
ID        TITLE              STATUS    DUE DATE      PRIORITY
--------  -----------------  --------  -----------   --------
task-001  Buy groceries      pending   (no due date) normal

$ todo complete task-001
Mark task-001 'Buy groceries' as complete? (y/n) > y
✓ Task marked complete: task-001 'Buy groceries'

$ todo list --filter pending
(no tasks shown)
```

**Workflow 2: Create Deadline Task, Filter by Due Date**
```bash
$ todo add 'Submit report' --due 2026-01-15 --priority high
✓ Task created: task-002 'Submit report'

$ todo filter --due-before 2026-01-20
ID        TITLE           STATUS    DUE DATE      PRIORITY
--------  ---------------  --------  -----------   --------
task-002  Submit report    pending   2026-01-15    high

$ todo complete task-002
✓ Task marked complete: task-002 'Submit report'
```

**Workflow 3: Search and Delete**
```bash
$ todo search 'old'
Found 2 matches:
  task-003: Old grocery list (completed)
  task-004: Old project (pending)

$ todo delete task-003
Delete task-003 'Old grocery list'? This cannot be undone. (y/n) > y
✓ Task deleted: task-003 'Old grocery list'
```

---

## Conclusion

Phase 1 CLI commands are designed to be simple, consistent, and forgiving. Users can discover commands naturally via help menus, error messages provide clear guidance, and command syntax follows Unix conventions. The design prioritizes **usability** and **discoverability** over advanced features, keeping the MVP focused and approachable.

