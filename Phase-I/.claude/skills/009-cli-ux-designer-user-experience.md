# Skill: CLI User Experience Design (Non-Technical User Focus)

**Skill ID**: CLI-003
**Agent Owner**: cli-ux-designer
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Design a CLI todo application that feels natural and intuitive to non-technical users. This skill applies user experience principles to CLI design, focusing on reducing cognitive load, providing sensible defaults, minimizing required inputs, and offering helpful guidance at every step. The goal is to make the Phase 1 todo app approachable for users without terminal experience while remaining efficient for power users.

---

## When to Use

- **CLI design phase**: After command syntax (CLI-002) is established; before implementation
- **User testing**: Validating command intuitiveness with actual users
- **Onboarding design**: Creating getting-started guides and initial prompts
- **Error recovery**: Designing helpful error messages and recovery paths
- **Feature simplification**: Deciding which options are essential vs. nice-to-have
- **Accessibility improvement**: Making CLI approachable to diverse user backgrounds

---

## Inputs

1. **Command specifications** (document): From CLI-002, defining command syntax and flags
2. **User stories** (list): From RA-001, describing user intent and context
3. **Acceptance criteria** (document): From PA-001, defining success conditions
4. **Target user personas** (optional): Non-technical users, power users, mixed audience

---

## Step-by-Step Process

### Step 1: Define Target User Personas
Create profiles of users the CLI must serve.

**Non-Technical User Persona**:

```
Profile: Alex, Project Manager
- Age: 35, non-technical background
- Uses computer for email, spreadsheets, documents
- Minimal command-line experience (never opened terminal)
- Learns by trying things and reading error messages
- Expects software to be forgiving and easy to undo

Goals:
- Create tasks quickly
- See all tasks at a glance
- Mark tasks complete
- Find specific tasks when needed

Pain Points:
- Confused by flag syntax (--due vs. -d)
- Forgets exact command names
- Nervous about making mistakes
- Needs confirmation before destructive actions
- Wants to see results of actions immediately

What Makes Them Happy:
- Software that anticipates their needs
- Clear, jargon-free instructions
- Ability to discover features without documentation
- Reassurance that "undo" is possible
- Simple, predictable behavior
```

**Power User Persona**:

```
Profile: Jordan, Software Developer
- Age: 28, technical background
- Uses terminal daily
- Values efficiency and keyboard shortcuts
- Likes flexibility and customization
- Comfortable with piping output and scripting

Goals:
- Manage tasks at high speed
- Integrate with other tools (export JSON, pipe to grep)
- Automate task creation via scripts
- Batch operations (mark all as complete)

Pain Points:
- Annoyed by confirmation prompts (can disable with --force)
- Wants short flags and aliases
- Needs JSON output for scripting
- Wants programmable/scriptable interface

What Makes Them Happy:
- Powerful, composable commands
- Good shell completion
- JSON output option
- Aliases for common workflows
- Piping support
```

**Mixed Audience Strategy**:

```
Design for non-technical first, add power features second:
  1. Core commands are simple and discoverable (non-tech friendly)
  2. Advanced flags (--json, --force) hidden by default (power user friendly)
  3. Defaults are sensible for non-tech users
  4. Aliases exist for power users (--help / -h)
  5. Multiple ways to do common tasks (CLI, interactive mode, scripting)

Example: "todo add" command
  For non-tech:
    todo add 'Buy milk'                           (simplest)
    todo add 'Buy milk' --due 2026-01-15         (add deadline)

  For power users:
    todo add 'Buy milk' -d 2026-01-15 -p high --json  (flags, JSON output)
    todo add 'Buy milk' --due 2026-01-15 --force      (skip confirmation)
```

---

### Step 2: Apply Cognitive Load Reduction
Minimize the amount of thinking required to use commands.

**Cognitive Load Reduction Principles**:

```
1. Recognize Patterns (Don't Make Users Memorize)

Problem: Users must memorize "todo add", "todo delete", "todo complete"
Solution: Use familiar verbs from English
  - "todo add" (like adding to list)
  - "todo delete" (like deleting from email)
  - "todo done" or "todo complete" (like marking email as read)

Problem: Users don't know if command exists
Solution: Use "did you mean" for typos
  User types: "todo ad 'task'"
  System: "✗ Unknown command 'ad'. Did you mean 'add'?"

2. Chunk Information (Present in Digestible Pieces)

Problem: User sees "task-001", "task-002", ... — meaningless IDs
Solution: Show IDs with context
  Bad:  task-001
  Good: task-001: Buy groceries (pending, due: 2026-01-15)

Problem: Long task list (50+ items) overwhelming
Solution: Paginate or limit results
  Show: "Showing 10 of 50 tasks. Run 'todo list --limit 50' to see all"

3. Use Constraints (Limit Choices)

Problem: User can set priority to any value (unlimited options)
Solution: Offer limited, named choices
  Good: "What priority? (low/normal/high)" [radio buttons / multiple choice]
  Bad: "Enter priority level" [free text, can be anything]

Problem: User unsure what date format to use
Solution: Show example/constraint
  Good: "Enter due date (YYYY-MM-DD, e.g., 2026-01-15):"
  Bad: "Enter due date:"

4. Rely on Defaults (Minimize Decisions)

Problem: User must decide every option (priority, due date, confirmation)
Solution: Use sensible defaults
  Good: Priority defaults to "normal" (80% of tasks)
  Good: Due date defaults to none (optional)
  Good: Confirmation defaults to "yes" (safer for non-tech users)

Example: "todo add" with defaults
  User input: todo add 'Buy milk'
  System applies defaults:
    - priority: normal (default)
    - due_date: none (default)
    - confirmation: shown (default)
  Result: Safe, predictable behavior

5. Provide Validation (Tell Users They're Right)

Problem: User unsure if command worked
Solution: Provide immediate, clear feedback
  Good: "✓ Task created: task-001 'Buy groceries'"
  Bad: (silence, no feedback)

Problem: User enters invalid data
Solution: Validate early and suggest fixes
  Good: "✗ Error: Invalid date '01/15/2026'. Expected YYYY-MM-DD. Try: 2026-01-15"
  Bad: "✗ Date parse error"

6. Reduce Working Memory (Show Context)

Problem: User must remember task ID from list to complete it
Solution: Show IDs in list output
  Good: Show full task in output: "task-001: Buy groceries (pending)"
  Bad: Just show ID: "task-001"

Problem: User deletes task but not sure if it worked
Solution: Echo the action back
  Good: "✓ Task deleted: task-001 'Buy groceries'"
  Bad: "✓ Deleted" (which task?)
```

---

### Step 3: Design Sensible Defaults
Establish default values that work for the most common scenarios.

**Default Value Strategy**:

```
Task Creation Defaults:
  - status: "pending" (new tasks start undone)
  - priority: "normal" (most tasks are normal priority)
  - due_date: null (most tasks have no deadline)
  - completed_timestamp: null (not done yet)

List Defaults:
  - filter: "all" (show both pending and completed)
  - sort: "created" (show newest first)
  - limit: 20 (show first 20 tasks)
  - format: "table" (human-readable, not JSON)

Confirmation Defaults:
  - delete: "ask" (confirm before deletion, safer)
  - complete: "no confirmation" (safe action, quick)
  - add: "no confirmation" (safe action, quick)

Priority Defaults by User Type:
  Non-tech user: "What priority?" → defaults to "normal"
  Power user: todo add 'Task' → assumes "normal" without asking

Due Date Defaults:
  Optional: Leave null if not provided (most tasks have no deadline)
  Smart: If --due is provided, validate format (YYYY-MM-DD only)
```

**Why These Defaults**:

```
priority: "normal" (default)
  Rationale: Most tasks are neither urgent nor trivial
  Data: In typical todo lists, 70-80% of tasks are "normal" priority
  Implication: Users rarely need to specify priority
  Alternative: Could default to "high" (would be wrong for most users)

due_date: null (default)
  Rationale: Most tasks have no specific deadline
  Data: In typical todo lists, 40-50% of tasks have no due date
  Implication: Users don't have to specify --due every time
  Alternative: Could default to "today" (would be wrong for most users)

status: "pending" (default)
  Rationale: New tasks are not done yet
  Data: 100% of new tasks should start pending
  Implication: No choice; always pending

confirmation for delete: "ask"
  Rationale: Deletion is irreversible; safer to confirm
  Data: Users sometimes regret deleting
  Implication: Adds one prompt (acceptable trade-off for safety)

confirmation for complete: "none" (no prompt)
  Rationale: Completion is reversible (can mark pending again)
  Data: Users frequently complete and uncomplete tasks
  Implication: Fast, non-annoying behavior
```

---

### Step 4: Design Minimal Input Interface
Reduce what users must type or decide.

**Minimal Input Principles**:

```
1. Make Common Tasks One Command

Very Good (Minimal):
  $ todo add 'Buy milk'
  $ todo list
  $ todo complete task-001

Good (Requires One Flag):
  $ todo add 'Buy milk' --due 2026-01-15
  $ todo list --filter pending

Acceptable (Requires Multiple Flags):
  $ todo add 'Buy milk' --due 2026-01-15 --priority high

Bad (Too Many Options):
  $ todo add --title 'Buy milk' --due 2026-01-15 --priority high --description 'at store' --category shopping

2. Make Rare Tasks Easy to Skip

Rare operations should not clutter common operations:
  - Advanced filters (--due-between X Y) hidden behind help
  - JSON output (--format json) available but optional
  - Batch operations (--all) documented but not forced

3. Provide Interactive Mode (Optional)

For non-tech users who are uncomfortable with flags:

Option A: Interactive Prompts
  $ todo add
  Task title: Buy milk
  Due date (optional, YYYY-MM-DD): 2026-01-15
  Priority (low/normal/high) [normal]: high

  ✓ Task created: task-001 'Buy milk' (due: 2026-01-15, priority: high)

Option B: Command-Line with Defaults
  $ todo add 'Buy milk'
  ✓ Task created: task-001 'Buy milk'

Both work; command-line is faster for experienced users, interactive is friendlier for beginners.

Implementation: Detect if input is provided
  If "todo add" (no title):
    → Show interactive prompts
  If "todo add 'title'":
    → Create immediately (use defaults for unspecified options)

4. Make Editing Optional (CRUD without Update)

Phase 1 simplification: Provide Create, Read, Delete, but no Update
  - If user makes mistake, delete and recreate
  - Fewer commands to learn
  - Simpler implementation

Rationale: Non-tech users rarely need to edit
  - Scenario: "I set due date to Jan 15, but it should be Jan 20"
  - Option 1: "todo update task-001 --due 2026-01-20" (requires update command)
  - Option 2: "todo delete task-001" + "todo add 'task' --due 2026-01-20" (two commands, but simple)

For Phase 2+: Add update when justified
```

---

### Step 5: Design Helpful Messages and Guidance
Provide context-sensitive help and error recovery.

**Message Types and Examples**:

```
1. Success Messages (Give Positive Feedback)

Task Created:
  Good: ✓ Task created: task-001 'Buy milk'
  Better: ✓ Task created: task-001 'Buy milk' (due: 2026-01-15, priority: high)
  Too Minimal: ✓ Created

Why? User wants to verify what was created; seeing the full task confirms it's correct.

Task Completed:
  Good: ✓ Task marked complete: task-001 'Buy milk'
  Better: ✓ Task marked complete: task-001 'Buy milk' (completed in 5 days)
  Why? Time-to-completion is motivating for users.

2. Error Messages (Help User Fix It)

Missing Required Input:
  Bad: ✗ Error: Title required
  Good: ✗ Error: Task title cannot be empty. Please provide a task title.
  Better: ✗ Error: Task title cannot be empty.
          Usage: todo add <TITLE>
          Example: todo add 'Buy groceries'

Invalid Input:
  Bad: ✗ Error: Invalid date
  Good: ✗ Error: Invalid date format. Expected YYYY-MM-DD, got '01/15/2026'
  Better: ✗ Error: Invalid date format '01/15/2026'. Expected YYYY-MM-DD.
          Did you mean: 2026-01-15?

Unknown Command:
  Bad: ✗ Error: Unknown command
  Good: ✗ Error: Unknown command 'ad'. Did you mean 'add'?

Task Not Found:
  Bad: ✗ Error: Not found
  Good: ✗ Error: Task not found: task-999
  Better: ✗ Error: Task not found: task-999
          Run 'todo list' to see all tasks.

3. Contextual Help (Guidance When Stuck)

When User Needs Help:
  $ todo
  → Shows quick help menu (not too much, not too little)

  Output:
    TODO - Task Management CLI

    QUICK START:
      Create task:   todo add 'Task title'
      List tasks:    todo list
      Complete:      todo complete task-001
      Delete:        todo delete task-001
      Help:          todo help

    Run "todo help" for full command reference

When User Types Invalid Command:
  $ todo ad 'task'
  ✗ Error: Unknown command 'ad'. Did you mean 'add'?

When User Needs Command Syntax:
  $ todo add --help
  → Shows full command reference with examples

When User Forgets Task ID:
  $ todo list
  → Shows all tasks with IDs they can reference

4. Warnings (Alert User to Potential Problems)

Delete Confirmation:
  $ todo delete task-001
  Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >

Past Due Date Warning:
  $ todo add 'Old task' --due 2020-01-01
  ⚠ Warning: Task due date is in the past. Is this correct? (y/n) >

5. Info Messages (Context Without Alarm)

List Count:
  $ todo list
  (table of tasks)
  ℹ Showing 10 of 50 tasks. Run 'todo list --limit 50' to see all.

Completion Motivation:
  $ todo complete task-001
  ✓ Task marked complete: task-001 'Buy groceries'
  ℹ You've completed 5 tasks this week. Great progress!
```

---

### Step 6: Design for Discoverability
Enable users to discover commands without reading documentation.

**Discoverability Strategy**:

```
1. Progressive Disclosure (Reveal Complexity Gradually)

Level 1: Entry Point (No Args)
  $ todo
  → Quick start guide (most important commands)
  → Mention "todo help" for more

Level 2: Command Help
  $ todo add --help
  → Full syntax, options, examples
  → Mention related commands (todo complete, todo list)

Level 3: Full Reference
  $ todo help
  → All commands, all options
  → Organized by category (create, view, modify, delete)

Philosophy: User only sees as much as they need, when they need it.
Non-tech users stay on Level 1 and 2.
Power users can access Level 3 for advanced features.

2. Consistent Help Format (Same Pattern Everywhere)

Every command help follows same structure:
  USAGE: <command syntax>
  DESCRIPTION: <one sentence>
  EXAMPLES: <2-3 common examples>
  OPTIONS: <flags, alphabetically>
  SEE ALSO: <related commands>

This consistency helps users learn once, apply everywhere.

3. Command Suggestions (Anticipate Typos)

User types: "todo creat 'task'"
System: ✗ Error: Unknown command 'creat'. Did you mean 'add'?

User types: "todo complete-task task-001"
System: ✗ Error: Unknown command 'complete-task'. Did you mean 'complete'?

Implementation: Levenshtein distance (fuzzy matching)
  - If user input is close to valid command (1-2 characters off), suggest it

4. Related Commands (Cross-Link Help)

When showing help for "add":
  SEE ALSO:
    todo list    - Show all tasks
    todo complete - Mark task as done
    todo delete   - Remove task

This helps users understand the ecosystem of commands.

5. Examples First (Show, Don't Tell)

Help for non-technical user:
  Good approach: Show 3-4 examples, then explain
    Example 1: todo add 'Buy milk'
    Example 2: todo add 'Submit report' --due 2026-01-15
    Example 3: todo add 'Fix bug' --priority high
    (Then explain --due and --priority flags)

  Bad approach: Explain flags, then examples
    Flags: --due accepts dates in YYYY-MM-DD format...
    (User's eyes glaze over before seeing an example)
```

---

### Step 7: Design Error Recovery
Make it easy for users to recover from mistakes.

**Error Recovery Principles**:

```
1. Confirmation Before Destructive Actions

Deletion (Irreversible):
  $ todo delete task-001
  Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >

Completion (Reversible):
  $ todo complete task-001
  (No confirmation; completion can be easily undone)

Rationale: Non-tech users are nervous about mistakes.
Confirmation adds one prompt for rare operations (acceptable).

2. Undo Capability (Where Practical)

Completed Task:
  $ todo complete task-001
  ✓ Task marked complete

  If user makes mistake:
  $ todo mark task-001 pending
  (Revert completion easily)

Deleted Task:
  Phase 1: Deleted permanently (no undo)
  Phase 2+: Implement trash/archive before permanent delete

Rationale: Reversible actions don't need confirmation.
Irreversible actions need careful handling.

3. Clear Consequences (Tell User What Happens)

Before delete: "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
(Tells user deletion is permanent)

Before export: "Export will create file 'tasks.json' (overwrite if exists). Continue? (y/n) >"
(Tells user side effects)

Before reset: "Reset will delete ALL tasks permanently. This cannot be undone. Type 'yes' to confirm >"
(Requires explicit user input for dangerous operations)

4. Exit Routes (Easy Way Out)

User starts destructive operation, changes mind:
  $ todo delete task-001
  Delete task-001 'Buy groceries'? This cannot be undone. (y/n) > n
  (Aborted. No action taken.)

User in interactive mode, doesn't want to continue:
  Task title: Buy milk
  Due date (optional): (Ctrl+C or type 'cancel')
  (Allows user to exit)

5. Recovery Path (Help User Fix It)

User deletes task by mistake (Phase 1, no undo):
  ✗ "Oops! I accidentally deleted a task. Can I get it back?"
  System: "Deleted tasks cannot be recovered in Phase 1. Start again: todo add 'task'"

  (Clear explanation, path to move forward)

User enters wrong priority:
  $ todo add 'task' --priority super-high
  ✗ Error: Invalid priority 'super-high'. Allowed: low, normal, high.
  $ todo add 'task' --priority high
  (Easy to retry)
```

---

### Step 8: Design for Multiple User Levels
Support both non-tech and power users.

**Multi-Level Design**:

```
Level 1: Absolute Beginner (Never Used Terminal)

What They Know:
  - How to open terminal/command prompt
  - How to type
  - That some commands might break things (nervously)

What They Need:
  - Simple, predictable commands
  - Confirmation before anything scary
  - Clear error messages explaining what went wrong
  - Immediate feedback that action worked

Recommended Approach:
  - Interactive mode: "todo" (no args) shows prompts
  - Sensible defaults: Don't force them to choose priority, due date
  - Confirmations: Show confirmation for delete
  - Guidance: "todo help" is always available

Example Session:
  $ todo
  What would you like to do? (add/list/complete/delete/search) > add
  Task title: Buy groceries
  Due date (optional, YYYY-MM-DD):
  Priority (low/normal/high) [normal]:
  ✓ Task created: task-001 'Buy groceries'

Level 2: Basic User (Comfortable with Typing)

What They Know:
  - How to use command line (familiar with cd, ls, etc.)
  - Understands arguments and flags
  - Knows how to read error messages

What They Need:
  - Efficient commands (short, no unnecessary prompts)
  - Some flexibility (flags for common options)
  - Good error messages
  - Quick feedback

Recommended Approach:
  - Direct command syntax: "todo add 'task'" (no prompts)
  - Flags for options: "--due", "--priority" (optional)
  - Sensible defaults: Assume defaults unless overridden
  - Help available: "--help" flag

Example Session:
  $ todo add 'Buy groceries' --due 2026-01-15 --priority normal
  ✓ Task created: task-001 'Buy groceries'

  $ todo list --filter pending
  (table of pending tasks)

  $ todo complete task-001
  ✓ Task marked complete: task-001 'Buy groceries'

Level 3: Power User (Developer, Advanced User)

What They Know:
  - Terminal is their home
  - Likes piping and scripting
  - Values efficiency above all

What They Need:
  - Short flags and aliases
  - JSON output for scripting
  - No confirmation prompts (--force flag)
  - Ability to batch operate (--all)

Recommended Approach:
  - Short aliases: "-a" for add, "-d" for delete, "-c" for complete
  - JSON output: "--format json" for scripting
  - Force flag: "--force" to skip confirmations
  - Composability: Output can pipe to other tools
  - Automation: Support bulk operations

Example Session:
  $ todo add 'Buy groceries' -d 2026-01-15 -p normal -f  # Force, no confirmation
  $ todo list --filter pending --format json | jq '.[] | select(.priority=="high")'
  (Pipes JSON to jq for advanced filtering)

Design Pattern: One Codebase, Multiple Interfaces

Implementation:
  - Core logic is mode-agnostic (works same regardless of interface)
  - Interface layer detects user type:
    IF (no args provided) AND (terminal is interactive):
      → Use interactive mode (Level 1)
    ELSE IF (using direct command syntax):
      → Use command-line mode (Level 2)
    ELSE IF (using flags like --force, --format json):
      → Use power-user mode (Level 3)

Result: Same application serves all user levels without separate codebases.
```

---

### Step 9: Validate UX Design
Ensure design meets non-technical user needs.

**UX Validation Checklist**:

```
✅ Cognitive Load
  [ ] All commands use familiar English verbs
  [ ] Users don't need to memorize task IDs (shown in output)
  [ ] Defaults are sensible (don't ask users to choose)
  [ ] Error messages explain what went wrong and how to fix
  [ ] Related commands are cross-linked in help

✅ Minimal Input
  [ ] Most common task (create task) takes 1 command
  [ ] Optional features don't clutter the main interface
  [ ] Non-tech users can complete workflows without flags
  [ ] Power users can use flags for efficiency

✅ Helpful Messages
  [ ] Success messages confirm what was created/modified
  [ ] Error messages are specific (not generic "error")
  [ ] Error messages suggest how to fix (not just what's wrong)
  [ ] "Did you mean?" suggestions for typos
  [ ] Confirmations shown before destructive actions

✅ Discoverability
  [ ] "todo" (no args) shows quick start guide
  [ ] "todo help" shows all commands
  [ ] "todo <command> --help" shows command details
  [ ] Examples shown for every command
  [ ] Related commands mentioned in help

✅ Error Recovery
  [ ] Confirmations before delete/dangerous operations
  [ ] Clear consequences explained (e.g., "cannot be undone")
  [ ] Easy way to cancel/abort operations
  [ ] Recovery path suggested (e.g., how to recreate deleted task)

✅ Multi-Level Support
  [ ] Interactive mode available for beginners (no flags)
  [ ] Command-line mode works for basic users
  [ ] Power-user features available (--force, --json, aliases)
  [ ] Same commands work across all user levels

✅ Accessibility
  [ ] Output is readable in standard terminal
  [ ] Colors used but not required (colorblind friendly)
  [ ] Long lists paginated or truncated
  [ ] Text is plain English (no jargon, no abbreviations)

✅ Performance
  [ ] Commands complete quickly (< 1 second feedback)
  [ ] No unnecessary prompts slowing down common tasks
  [ ] Visible progress for long operations
```

---

## Output

**Format**: Structured Markdown document with UX recommendations and improvements:

```markdown
# CLI User Experience Design (Non-Technical User Focus)

## Target User Personas
[Profiles of non-tech, basic, and power users]

## Cognitive Load Reduction
[Principles to minimize thinking required]

## Sensible Defaults
[Default values for common decisions]

## Minimal Input Interface
[How to reduce what users must type]

## Helpful Messages and Guidance
[Error messages, help text, suggestions]

## Discoverability Design
[How users discover commands naturally]

## Error Recovery
[How to help users recover from mistakes]

## Multi-Level Design
[Supporting different user sophistication levels]

## UX Validation Checklist
[Verifying design meets user needs]

## Usage Improvements
[Recommended changes to commands]
```

---

## Failure Handling

### Scenario 1: Defaults Conflict with User Expectations
**Symptom**: New user creates task, expects it to default to "high" priority (thinks all tasks are urgent)
**Resolution**:
- Keep default as "normal" (statistically correct for most users)
- Show feedback message: "✓ Task created with normal priority"
- Allow user to change: "To set priority, run: todo add 'task' --priority high"
- This educates user without overriding their initial action

### Scenario 2: Non-Tech User Overwhelmed by Power-User Features
**Symptom**: "todo help" shows 50+ flags; user confused
**Resolution**:
- Separate help levels: "todo" (quick), "todo help" (full), "todo <cmd> --help" (detailed)
- Quick help shows only essential commands
- Full help shows power-user features but marks them as "advanced"
- Progressive disclosure prevents information overload

### Scenario 3: Error Messages Too Technical
**Symptom**: "TypeError: NoneType object has no attribute 'upper()'"
**Resolution**:
- Never show internal errors to users
- Translate to user-friendly message: "✗ Error: Task title is missing"
- Log technical errors for debugging (separate system)
- All user-facing messages should be plain English

### Scenario 4: Users Accidentally Delete Tasks
**Symptom**: User deletes task without realizing it can't be undone
**Resolution**:
- Show clear confirmation: "Delete task-001 'Buy groceries'? This cannot be undone. (y/n) >"
- Use strong language ("cannot be undone") not weak ("are you sure?")
- Consider soft delete for Phase 2 (trash/archive before permanent)
- Document how to manually restore from backup if disaster happens

### Scenario 5: Help Text Too Long
**Symptom**: User runs "todo --help", sees 40-line document, scrolls away
**Resolution**:
- Keep quick help under 10 lines
- Show most common examples (2-3 best)
- Link to detailed help: "Run 'todo help' for more examples"
- Help text should answer 80% of questions, defer edge cases

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Phase II web UI**: Same UX principles apply (sensible defaults, minimal inputs, helpful feedback)
- **API design**: Error messages should follow same clarity standards
- **Chatbot interface**: Same cognitive load reduction principles
- **Mobile apps**: Progressive disclosure works on all platforms
- **Other CLI tools**: Non-tech user focus applies universally

---

## Success Metrics

- ✅ Non-technical users can use core features without documentation
- ✅ Common tasks (create, complete, list) require minimal commands
- ✅ Error messages are specific, helpful, and actionable
- ✅ Users can discover commands via help (no memorization needed)
- ✅ Destructive actions require confirmation
- ✅ All messages are plain English (no jargon)
- ✅ Defaults are sensible (reduce user decisions)
- ✅ Power users can use advanced features (flags, JSON, aliases)
- ✅ Multi-level support (interactive mode for beginners, flags for advanced)
- ✅ Recovery path clear after any error

---

## Related Skills

- **Command Design (CLI-002)**: Defines syntax and structure
- **Functional Analysis (CLI-001)**: Defines what commands do
- **Acceptance Criteria (PA-001)**: Tests that UX meets requirements
- **Quality Assurance (QA-001)**: Tests edge cases and error recovery

---

## Example: Phase 1 UX Improvements

### Current vs. Improved

**Task Creation (Current)**:
```
$ todo add 'Buy milk' --due 2026-01-15 --priority normal
✓ Created
```

**Task Creation (Improved)**:
```
$ todo add 'Buy milk'
✓ Task created: task-001 'Buy milk'
(Defaults applied: priority=normal, no due date, status=pending)

$ todo add 'Buy milk' --due 2026-01-15
✓ Task created: task-001 'Buy milk' (due: 2026-01-15, priority: normal)
```

Why Better?
- Immediate feedback shows what was created
- Includes task ID for future reference
- Shows applied defaults (educates user)
- Works with or without optional flags

**Error Message (Current)**:
```
$ todo add ''
✗ Error: Empty string invalid
```

**Error Message (Improved)**:
```
$ todo add ''
✗ Error: Task title cannot be empty. Please provide a task title.

Examples:
  todo add 'Buy groceries'
  todo add 'Submit report' --due 2026-01-15
```

Why Better?
- Explains what went wrong in plain English
- Suggests how to fix
- Shows examples of correct usage

**List Output (Current)**:
```
$ todo list
task-001
task-002
task-003
(20 more tasks...)
```

**List Output (Improved)**:
```
$ todo list
ID        TITLE              STATUS     DUE DATE      PRIORITY
--------  -----------------  ---------  -----------   --------
task-001  Buy groceries      pending    2026-01-15    normal
task-002  Submit report      completed  2026-01-10    high
task-003  Fix critical bug   pending    (no due date) high
(showing 5 of 23 tasks; run 'todo list --limit 23' to see all)
```

Why Better?
- Shows full context (title, status, due date) with task ID
- Format is human-readable (table)
- Tells user there are more tasks available
- Helps non-tech user understand their tasks at a glance

**Help Text (Current)**:
```
$ todo add --help
-t, --title STR     Task title
-d, --due DATE      Due date (YYYY-MM-DD)
-p, --priority LV   Priority (low/normal/high)
-c, --confirm       Confirm before creating
```

**Help Text (Improved)**:
```
$ todo add --help
USAGE:
  todo add <TITLE> [OPTIONS]

DESCRIPTION:
  Create a new task with optional deadline and priority.

ARGUMENTS:
  <TITLE>              Task title (required, 1-255 characters)

OPTIONS:
  -d, --due <DATE>     Deadline (YYYY-MM-DD format, optional)
  -p, --priority LEVEL Priority level: low, normal, high (default: normal)
  -f, --force          Create without confirmation

EXAMPLES:
  Create a simple task:
    $ todo add 'Buy groceries'

  Add a deadline:
    $ todo add 'Submit report' --due 2026-01-15

  Set priority:
    $ todo add 'Fix critical bug' --priority high

SEE ALSO:
  todo list, todo complete, todo delete, todo help
```

Why Better?
- Structure is consistent and easy to scan
- Examples come before detailed explanations
- Shows related commands (cross-linking)
- Explains defaults (priority defaults to "normal")
- Real-world examples, not abstract explanations

### Interactive Mode Example

For non-technical users who don't like flags:

```
$ todo
TODO - Task Management

What would you like to do?
  1. Add a new task
  2. View all tasks
  3. Mark task complete
  4. Delete a task
  5. Search tasks
  6. Get help

Choice (1-6) > 1

Task title (required): Buy groceries
Due date (optional, YYYY-MM-DD): 2026-01-15
Priority (optional: low/normal/high) [normal]:
Confirm? (yes/no) [yes]:

✓ Task created: task-001 'Buy groceries' (due: 2026-01-15, priority: normal)

What's next? (add another/view all/main menu) > main menu
```

Benefits:
- No flags to remember
- Prompts guide user through options
- Sensible defaults shown in brackets
- User always knows what to do next

---

## Conclusion

Phase 1 CLI user experience is designed for non-technical users while remaining efficient for power users. Key principles are:

1. **Reduce Cognitive Load**: Familiar verbs, sensible defaults, clear feedback
2. **Minimal Input**: Core tasks need only command and argument, no flags required
3. **Helpful Guidance**: Error messages explain what went wrong and how to fix
4. **Discoverability**: Help available at every level (quick, command, detailed)
5. **Safe Operations**: Confirmation before destructive actions, clear recovery path
6. **Multi-Level Support**: Interactive mode for beginners, flags for power users

The result is a tool that feels natural to non-technical users while offering power and flexibility to advanced users.

