"""CLI entry point for Todo application"""

import sys
from datetime import date
from src.services.task_service import TaskService


def print_task(task, index=None):
    """Pretty print a task"""
    prefix = f"{index}. " if index is not None else ""
    status_icon = "✓" if task.status == "completed" else "○"
    overdue_marker = " [OVERDUE]" if task.is_overdue else ""
    category_str = f" [{task.category}]" if task.category else ""
    priority_str = f" ({task.priority})" if task.priority != "medium" else ""

    print(f"{prefix}{status_icon} {task.id} | {task.title}{category_str}{priority_str}{overdue_marker}")


def main():
    """Main CLI entry point"""
    service = TaskService()

    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "list" or command == "ls":
        # List all tasks
        tasks = service.list_all_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print(f"\n{'Tasks:':^60}")
        print("=" * 60)
        for i, task in enumerate(tasks, 1):
            print_task(task, i)
        print("=" * 60)

        # Print summary
        stats = service.get_completion_stats()
        print(f"\nTotal: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}")
        print(f"Completion: {stats['completion_percentage']}%")

    elif command == "add":
        # Add a new task
        if len(sys.argv) < 3:
            print("Usage: add <title> [--priority PRIORITY] [--category CATEGORY] [--due-date DATE]")
            return

        title = sys.argv[2]
        priority = None
        category = None
        due_date = None

        # Parse optional arguments
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--due-date" and i + 1 < len(sys.argv):
                due_date = date.fromisoformat(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        task = service.create_task(title, priority=priority, category=category, due_date=due_date)
        print(f"✓ Task created: {task.id}")
        print_task(task)

    elif command == "search":
        # Search tasks
        if len(sys.argv) < 3:
            print("Usage: search <keyword>")
            return

        keyword = sys.argv[2]
        results = service.search_tasks(keyword)

        if not results:
            print(f"No tasks found matching '{keyword}'")
            return

        print(f"\nSearch Results for '{keyword}':")
        print("=" * 60)
        for i, task in enumerate(results, 1):
            print_task(task, i)
        print("=" * 60)

    elif command == "filter":
        # Filter tasks
        if len(sys.argv) < 3:
            print("Usage: filter [--priority PRIORITY] [--category CATEGORY] [--status STATUS]")
            return

        priority = None
        category = None
        status = None

        # Parse optional arguments
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            else:
                i += 1

        # Apply filters
        tasks = service.get_all_tasks()
        if priority:
            tasks = service.filter_by_priority(priority)
        if category:
            tasks = [t for t in tasks if t.category == category]
        if status:
            tasks = [t for t in tasks if t.status == status]

        if not tasks:
            print("No tasks match the filter criteria.")
            return

        print(f"\nFiltered Results:")
        print("=" * 60)
        for i, task in enumerate(tasks, 1):
            print_task(task, i)
        print("=" * 60)

    elif command == "complete":
        # Mark task as complete
        if len(sys.argv) < 3:
            print("Usage: complete <task-id>")
            return

        task_id = sys.argv[2]
        task = service.mark_complete(task_id)
        print(f"✓ Task marked as complete: {task_id}")
        print_task(task)

    elif command == "pending":
        # Mark task as pending
        if len(sys.argv) < 3:
            print("Usage: pending <task-id>")
            return

        task_id = sys.argv[2]
        task = service.mark_pending(task_id)
        print(f"○ Task marked as pending: {task_id}")
        print_task(task)

    elif command == "delete":
        # Delete a task
        if len(sys.argv) < 3:
            print("Usage: delete <task-id>")
            return

        task_id = sys.argv[2]
        if service.delete_task(task_id):
            print(f"✓ Task deleted: {task_id}")
        else:
            print(f"✗ Task not found: {task_id}")

    elif command == "show":
        # Show task details
        if len(sys.argv) < 3:
            print("Usage: show <task-id>")
            return

        task_id = sys.argv[2]
        task = service.get_task(task_id)
        if not task:
            print(f"✗ Task not found: {task_id}")
            return

        print(f"\nTask Details:")
        print("=" * 60)
        print(f"ID:        {task.id}")
        print(f"Title:     {task.title}")
        print(f"Status:    {task.status}")
        print(f"Priority:  {task.priority}")
        print(f"Category:  {task.category or 'None'}")
        print(f"Due Date:  {task.due_date or 'None'}")
        print(f"Recurrence: {task.recurrence or 'None'}")
        print(f"Overdue:   {task.is_overdue}")
        print("=" * 60)

    elif command == "stats":
        # Show statistics
        stats = service.get_completion_stats()
        overdue = service.get_overdue_tasks()

        print(f"\nTask Statistics:")
        print("=" * 60)
        print(f"Total Tasks:      {stats['total']}")
        print(f"Completed:        {stats['completed']}")
        print(f"Pending:          {stats['pending']}")
        print(f"Completion:       {stats['completion_percentage']}%")
        print(f"Overdue:          {len(overdue)}")
        print("=" * 60)

    elif command == "help" or command == "-h" or command == "--help":
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


def print_help():
    """Print help message"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                      Todo App - CLI Help                       ║
╚════════════════════════════════════════════════════════════════╝

COMMANDS:

  list                              List all tasks
                                    Usage: list

  add <title>                       Create a new task
                                    Usage: add "Buy groceries" --priority high --category personal

  search <keyword>                  Search tasks by keyword
                                    Usage: search grocery

  filter                            Filter tasks by criteria
                                    Usage: filter --priority high --category work --status pending

  complete <task-id>                Mark task as complete
                                    Usage: complete task-001

  pending <task-id>                 Mark task as pending
                                    Usage: pending task-001

  delete <task-id>                  Delete a task
                                    Usage: delete task-001

  show <task-id>                    Show task details
                                    Usage: show task-001

  stats                             Show statistics
                                    Usage: stats

  help                              Show this help message
                                    Usage: help

OPTIONS:

  --priority <PRIORITY>             Task priority: high, medium, low
  --category <CATEGORY>             Task category
  --due-date <DATE>                 Due date in YYYY-MM-DD format
  --status <STATUS>                 Task status: pending, completed

EXAMPLES:

  python -m src list
  python -m src add "Buy groceries" --priority high --category personal
  python -m src search "grocery"
  python -m src filter --priority high --status pending
  python -m src complete task-001
  python -m src stats

""")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
