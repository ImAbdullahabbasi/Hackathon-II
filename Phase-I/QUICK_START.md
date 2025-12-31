# 🚀 Todo App - Quick Start

## ⚡ Fastest Way to Start

```bash
python -m src.cli_beautiful
```

That's it! You'll see a beautiful interactive menu. 🎨

---

## 📋 What You Can Do

### In the Beautiful CLI:

```
1. ➕ Create Task
   - Add new tasks with priority, category, due date

2. 🗑️  Delete Task
   - Remove tasks you don't need

3. 📋 List All Tasks
   - See all your tasks with stats

4. 🔍 Search Tasks
   - Find tasks by keyword

5. 🔎 Filter Tasks
   - Filter by priority, category, or status

6. ✅ Mark Complete
   - Mark tasks as done

7. 🔄 Mark Pending
   - Undo completion

8. 📝 Show Details
   - View full task information

9. 📊 Statistics
   - See your progress

10. 🚪 Exit
    - Save and exit
```

---

## 🎯 Priority Levels

- 🔴 **HIGH** - Most urgent
- 🟡 **MEDIUM** - Standard (default)
- 🟢 **LOW** - Less urgent

---

## 📅 Date Format

Use `YYYY-MM-DD` format:
- ✅ 2024-01-15
- ❌ 01/15/2024

---

## 💡 Pro Tips

1. **Quick selection** - Type task number (1, 2, 3...) not just ID
2. **Search anywhere** - Partial text works (search "grocery" finds "Buy groceries")
3. **Combine filters** - Filter by multiple criteria at once
4. **Check stats** - See your progress anytime

---

## 🐛 Common Commands

### Command-Line (without menu):

```bash
# List all tasks
python -m src list

# Add task
python -m src add "Task title" --priority high --category work

# Search
python -m src search "keyword"

# Mark complete
python -m src complete task-001

# View stats
python -m src stats
```

---

## 📖 Full Documentation

See `CLI_GUIDE.md` for complete documentation.

---

**Ready to go? Run:**
```bash
python -m src.cli_beautiful
```

Enjoy! 🎉
