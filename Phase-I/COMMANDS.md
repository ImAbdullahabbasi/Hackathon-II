# 📋 Todo App - All Commands Reference

## 🎨 Run the Beautiful Interactive CLI

```bash
python -m src.cli_beautiful
```

This is the main interface with colors, emojis, and beautiful formatting.

---

## 🎯 Interactive Menu Commands

Once you run the CLI, you'll see this menu:

```
1.  Create Task
2.  Delete Task
3.  List All Tasks
4.  Search Tasks
5.  Filter Tasks
6.  Mark Complete
7.  Mark Pending
8.  Show Details
9.  Statistics
10. Exit
```

Just enter the number (1-10) to perform the action.

---

## 💻 Command-Line Interface Commands

### Basic Commands

```bash
# Show help
python -m src help

# List all tasks
python -m src list
python -m src ls

# View statistics
python -m src stats
```

### Create Tasks

```bash
# Simple task
python -m src add "Task title"

# With priority
python -m src add "Task title" --priority high
python -m src add "Task title" --priority medium
python -m src add "Task title" --priority low

# With category
python -m src add "Task title" --category work
python -m src add "Task title" --category personal

# With due date
python -m src add "Task title" --due-date 2024-01-15

# All options combined
python -m src add "Buy groceries" --priority high --category personal --due-date 2024-01-15
```

### Search & Filter

```bash
# Search by keyword
python -m src search "grocery"
python -m src search "work"

# Filter by priority
python -m src filter --priority high
python -m src filter --priority medium
python -m src filter --priority low

# Filter by category
python -m src filter --category work
python -m src filter --category personal

# Filter by status
python -m src filter --status pending
python -m src filter --status completed

# Multiple filters (AND logic)
python -m src filter --priority high --status pending
python -m src filter --category work --priority high --status pending
```

### Mark Tasks

```bash
# Mark task as complete
python -m src complete task-001
python -m src complete task-002

# Mark task as pending
python -m src pending task-001
python -m src pending task-002
```

### Delete & View

```bash
# Delete a task
python -m src delete task-001

# Show task details
python -m src show task-001
```

---

## 🎨 Alternative CLI Options

### Simple Interactive CLI
```bash
python -m src.cli_interactive
```
Same as beautiful CLI but without colors.

### Command Mode Only
```bash
python -m src [command] [options]
```
Use command-line arguments only, no menu.

---

## 📝 Interactive Menu - Detailed Steps

### Option 1: Create Task
```
1. Enter task title
2. Enter priority (high/medium/low) [optional]
3. Enter category [optional]
4. Enter due date (YYYY-MM-DD) [optional]
```

### Option 2: Delete Task
```
1. View available tasks
2. Enter task number or ID
3. Task is deleted
```

### Option 3: List All Tasks
```
Shows:
- All tasks with status, priority, category
- Total count
- Completed count
- Pending count
- Completion percentage
```

### Option 4: Search Tasks
```
1. Enter search keyword
2. Results displayed with matches highlighted
3. Case-insensitive search
```

### Option 5: Filter Tasks
```
Choose filter type:
1. By Priority (high/medium/low)
2. By Category
3. By Status (pending/completed)
4. Multiple filters
```

### Option 6: Mark Complete
```
1. View pending tasks
2. Select task number or ID
3. Task marked as complete ✓
```

### Option 7: Mark Pending
```
1. View completed tasks
2. Select task number or ID
3. Task marked as pending ○
```

### Option 8: Show Details
```
1. View available tasks
2. Select task number or ID
3. Full task information displayed
```

### Option 9: Statistics
```
Shows:
- Total, completed, pending counts
- Completion percentage
- Overdue count
- Priority breakdown
- Category breakdown
```

### Option 10: Exit
```
- Saves all tasks
- Closes the application
```

---

## 🎯 Priority Reference

| Priority | Level | Color | Usage |
|----------|-------|-------|-------|
| high | 1 | 🔴 Red | Urgent tasks |
| medium | 2 | 🟡 Yellow | Standard tasks |
| low | 3 | 🟢 Green | Less urgent |

**Default:** `medium`

---

## 📅 Date Format

All dates use ISO 8601 format: **YYYY-MM-DD**

Examples:
- `2024-01-15` ✅ January 15, 2024
- `2024-12-31` ✅ December 31, 2024
- `2025-06-20` ✅ June 20, 2025

❌ Don't use:
- `01/15/2024`
- `15-01-2024`
- `Jan 15, 2024`

---

## 🎨 Visual Indicators

### Status
- `✓` - Task completed
- `○` - Task pending

### Priority
- `🔴` - High priority
- `🟡` - Medium priority
- `🟢` - Low priority

### Special
- `[OVERDUE]` - Task is overdue (red)
- `[CATEGORY]` - Task category (magenta)

---

## 🔍 Search & Filter Features

### Search
- Case-insensitive
- Partial text matching
- Searches in task title
- Example: `"grocery"` finds `"Buy groceries"`

### Filter
- By priority: `high`, `medium`, `low`
- By category: Any category name
- By status: `pending`, `completed`
- Multiple filters: Combine with AND logic

---

## 📊 Example Workflows

### Create and Complete a Task

```bash
# 1. Create task
python -m src add "Buy groceries" --priority high --category personal --due-date 2024-01-15

# 2. List tasks to see it
python -m src list

# 3. Mark as complete
python -m src complete task-001

# 4. View statistics
python -m src stats
```

### Search and Filter

```bash
# 1. Search for work tasks
python -m src search "work"

# 2. Filter high priority pending tasks
python -m src filter --priority high --status pending

# 3. View details of a specific task
python -m src show task-001
```

### Manage Tasks

```bash
# Create multiple tasks
python -m src add "Task 1" --priority high --category work
python -m src add "Task 2" --priority medium --category personal
python -m src add "Task 3" --priority low --category work

# Filter by category
python -m src filter --category work

# Complete tasks
python -m src complete task-001
python -m src complete task-003

# View stats
python -m src stats
```

---

## ✨ Best Practices

1. **Use the Beautiful CLI** - Most user-friendly
2. **Set priorities** - Helps with focus
3. **Categorize tasks** - Easier to organize
4. **Set due dates** - Tracks deadlines
5. **Check statistics** - Monitor progress
6. **Search regularly** - Find tasks quickly
7. **Mark complete** - Feel accomplished!

---

## 📞 Getting Help

```bash
# In command-line mode
python -m src help

# In interactive menu
Select option 10 and look at the help section
```

---

**Ready to start?**
```bash
python -m src.cli_beautiful
```

Enjoy managing your tasks! 🚀✨
