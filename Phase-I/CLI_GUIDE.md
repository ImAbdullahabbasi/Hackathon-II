# Todo App - CLI Guide

## 🚀 Quick Start Commands

### Run the Beautiful Interactive CLI (Recommended)
```bash
python -m src.cli_beautiful
```

Or with uv:
```bash
uv run python -m src.cli_beautiful
```

### Run the Simple Interactive CLI
```bash
python -m src.cli_interactive
```

### Run Command-Line Interface
```bash
python -m src
```

---

## 🎨 Beautiful Interactive CLI Features

The beautiful CLI comes with:
- ✨ Colorful, attractive interface
- 🎯 Color-coded priorities (🔴 High, 🟡 Medium, 🟢 Low)
- 📊 Visual task indicators (✓ Complete, ○ Pending)
- 🌈 Category highlighting
- ⚠️ Overdue task warnings
- 📈 Statistics with breakdowns

### Menu Options (Beautiful CLI)

```
1.  Create Task        ➕ Add a new task with details
2.  Delete Task        🗑️  Remove a task
3.  List All Tasks     📋 View all tasks with stats
4.  Search Tasks       🔍 Find tasks by keyword
5.  Filter Tasks       🔎 Filter by priority/category/status
6.  Mark Complete      ✅ Mark pending tasks as done
7.  Mark Pending       🔄 Mark completed tasks back to pending
8.  Show Details       📝 View detailed task information
9.  Statistics         📊 View task statistics & breakdown
10. Exit               🚪 Exit the application
```

---

## 📝 How to Use Each Option

### Option 1: Create Task
```
Enter task title: Buy groceries
Priority [default: medium]: high
Category [optional]: personal
Due date [YYYY-MM-DD]: 2024-01-15
```
Creates a new task with the specified details.

### Option 2: Delete Task
Shows all tasks with numbers. Select by:
- Task number: `1` (for first task)
- Or task ID: `task-001`

### Option 3: List All Tasks
Displays all tasks with:
- Status indicator (✓ or ○)
- Task ID
- Title
- Category (if set)
- Priority
- Overdue warning (if applicable)

Shows completion stats:
- Total tasks
- Completed count
- Pending count
- Completion percentage

### Option 4: Search Tasks
```
Enter search keyword: grocery
```
Finds tasks containing the keyword (case-insensitive).

### Option 5: Filter Tasks
Filter by:
1. **Priority** - high, medium, low
2. **Category** - specific category name
3. **Status** - pending or completed
4. **Multiple filters** - Combine priority, category, and status

### Option 6: Mark Complete
Shows pending tasks. Select one to mark as complete.
Updates task status and shows completion timestamp.

### Option 7: Mark Pending
Shows completed tasks. Select one to revert to pending.
Clears the completion timestamp.

### Option 8: Show Details
Shows complete task information:
- Task ID
- Title
- Status
- Priority
- Category
- Due date
- Recurrence
- Overdue status
- Creation timestamp
- Completion timestamp (if completed)

### Option 9: Statistics
Displays:
- **Task Summary**: Total, Completed, Pending, Completion %
- **Overdue Count**: Number of overdue tasks
- **Priority Breakdown**: Count by High/Medium/Low
- **Category Breakdown**: Count by category

### Option 10: Exit
Saves all tasks and exits the application.

---

## 💻 Command-Line Interface Examples

### List Tasks
```bash
python -m src list
```

### Add Task
```bash
python -m src add "Buy groceries"
python -m src add "Buy groceries" --priority high --category personal
python -m src add "Pay bills" --due-date 2024-01-15 --priority high
```

### Search Tasks
```bash
python -m src search "grocery"
python -m src search "work"
```

### Filter Tasks
```bash
python -m src filter --priority high --status pending
python -m src filter --category work
python -m src filter --status completed
```

### Mark Complete
```bash
python -m src complete task-001
```

### Mark Pending
```bash
python -m src pending task-001
```

### Delete Task
```bash
python -m src delete task-001
```

### Show Task Details
```bash
python -m src show task-001
```

### View Statistics
```bash
python -m src stats
```

### Get Help
```bash
python -m src help
```

---

## 🎯 Priority Levels

| Priority | Color | Indicator |
|----------|-------|-----------|
| High | 🔴 Red | Most urgent |
| Medium | 🟡 Yellow | Standard (default) |
| Low | 🟢 Green | Less urgent |

---

## 📅 Date Format

All dates must be in **YYYY-MM-DD** format:
- ✅ Valid: `2024-01-15`, `2024-12-31`, `2025-06-20`
- ❌ Invalid: `01/15/2024`, `15-01-2024`, `Jan 15, 2024`

---

## 🔄 Task Status

| Status | Indicator | Meaning |
|--------|-----------|---------|
| Pending | ○ | Not yet completed |
| Completed | ✓ | Task is done |

---

## 💡 Tips & Tricks

1. **Quick Selection**: In most menus, you can select tasks by number (1, 2, 3...) instead of entering the full task ID.

2. **Search Keywords**: Search is case-insensitive and matches partial text:
   - Search: `grocery` matches "Buy groceries", "grocery list", etc.

3. **Filter Combinations**: Use multiple filters together:
   - Filter by high priority + work category = only high priority work tasks

4. **Overdue Tasks**: Tasks with due dates in the past are marked as OVERDUE.

5. **Statistics**: Check stats regularly to see your progress and priorities.

---

## 🐛 Troubleshooting

### "Task not found"
- Make sure you entered the correct task ID or number
- Use option 3 (List All Tasks) to see all available tasks

### "Invalid date format"
- Use YYYY-MM-DD format (e.g., 2024-01-15)
- Don't use slashes or dashes in the year-month separator

### "Invalid priority"
- Use only: `high`, `medium`, or `low`
- Priority names are case-insensitive

### Colors not showing (Windows)
- Some Windows terminals don't support colors by default
- Try running in Windows PowerShell or Windows Terminal instead of CMD

---

## 📊 File Locations

- **Main CLI (Beautiful)**: `src/cli_beautiful.py`
- **Simple CLI**: `src/cli_interactive.py`
- **Command-line CLI**: `src/__main__.py`
- **Core Services**: `src/services/`
- **Data Models**: `src/models/`

---

## 🎓 About This Todo App

**Features Implemented:**
- ✅ Create, read, update, delete tasks
- ✅ Priority management (high/medium/low)
- ✅ Category organization
- ✅ Search functionality
- ✅ Advanced filtering
- ✅ Sorting capabilities
- ✅ Task completion tracking
- ✅ Overdue detection
- ✅ Statistics dashboard

**Test Coverage:** 99.04% (326 tests passing)

**Tech Stack:**
- Python 3.13+
- No external dependencies
- Pure Python stdlib

---

## 📞 Need Help?

Run the help command in the CLI:
```bash
python -m src help
```

Or select option 10 in the beautiful CLI for more information.

---

**Enjoy your Todo App! 🚀✨**
