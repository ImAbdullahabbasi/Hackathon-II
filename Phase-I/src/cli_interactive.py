"""Interactive menu-driven CLI for Todo application"""

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


def print_main_menu():
    """Print main menu options"""
    print("\n" + "=" * 60)
    print("                    TODO APP - MAIN MENU")
    print("=" * 60)
    print("1.  Create Task")
    print("2.  Delete Task")
    print("3.  List All Tasks")
    print("4.  Search Tasks")
    print("5.  Filter Tasks")
    print("6.  Mark Task Complete")
    print("7.  Mark Task Pending")
    print("8.  Show Task Details")
    print("9.  View Statistics")
    print("10. Exit")
    print("=" * 60)


def option_1_create_task(service):
    """Option 1: Create a new task"""
    print("\n--- CREATE NEW TASK ---\n")

    title = input("Enter task title: ").strip()
    if not title:
        print("✗ Title cannot be empty!")
        return

    print("\nPriority (high/medium/low) [default: medium]:")
    priority = input("Enter priority: ").strip().lower() or "medium"

    print("\nCategory [optional]:")
    category = input("Enter category: ").strip() or None

    print("\nDue date [optional, format: YYYY-MM-DD]:")
    due_date_str = input("Enter due date: ").strip()
    due_date = None
    if due_date_str:
        try:
            due_date = date.fromisoformat(due_date_str)
        except ValueError:
            print("✗ Invalid date format!")
            return

    try:
        task = service.create_task(
            title,
            priority=priority,
            category=category,
            due_date=due_date
        )
        print(f"\n✓ Task created successfully!")
        print_task(task)
    except Exception as e:
        print(f"✗ Error creating task: {e}")


def option_2_delete_task(service):
    """Option 2: Delete a task"""
    print("\n--- DELETE TASK ---\n")

    # Show all tasks
    tasks = service.get_all_tasks()
    if not tasks:
        print("No tasks to delete.")
        return

    print("Available tasks:")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_id = input("Enter task ID to delete (or task number): ").strip()

    # If user entered a number, convert it to task ID
    if task_id.isdigit():
        task_num = int(task_id) - 1
        if 0 <= task_num < len(tasks):
            task_id = tasks[task_num].id
        else:
            print("✗ Invalid task number!")
            return

    if service.delete_task(task_id):
        print(f"\n✓ Task deleted: {task_id}")
    else:
        print(f"\n✗ Task not found: {task_id}")


def option_3_list_all_tasks(service):
    """Option 3: List all tasks"""
    print("\n--- ALL TASKS ---\n")

    tasks = service.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    # Print summary
    stats = service.get_completion_stats()
    print("\n" + "-" * 60)
    print(f"Total: {stats['total']} | Completed: {stats['completed']} | Pending: {stats['pending']}")
    print(f"Completion: {stats['completion_percentage']}%")
    print("-" * 60)


def option_4_search_tasks(service):
    """Option 4: Search tasks"""
    print("\n--- SEARCH TASKS ---\n")

    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print("✗ Keyword cannot be empty!")
        return

    results = service.search_tasks(keyword)

    if not results:
        print(f"\nNo tasks found matching '{keyword}'")
        return

    print(f"\nSearch Results for '{keyword}' ({len(results)} found):\n")
    for i, task in enumerate(results, 1):
        print_task(task, i)


def option_5_filter_tasks(service):
    """Option 5: Filter tasks"""
    print("\n--- FILTER TASKS ---\n")

    print("Filter Options:")
    print("1. By Priority")
    print("2. By Category")
    print("3. By Status")
    print("4. Multiple filters")

    choice = input("\nSelect filter type (1-4): ").strip()

    tasks = service.get_all_tasks()

    if choice == "1":
        print("\nAvailable priorities: high, medium, low")
        priority = input("Enter priority: ").strip().lower()
        tasks = service.filter_by_priority(priority)

    elif choice == "2":
        category = input("Enter category: ").strip()
        tasks = [t for t in tasks if t.category == category]

    elif choice == "3":
        print("Available statuses: pending, completed")
        status = input("Enter status: ").strip().lower()
        tasks = [t for t in tasks if t.status == status]

    elif choice == "4":
        print("\nEnter filters (leave empty to skip):")
        priority = input("Priority (high/medium/low): ").strip().lower() or None
        category = input("Category: ").strip() or None
        status = input("Status (pending/completed): ").strip().lower() or None

        if priority:
            tasks = service.filter_by_priority(priority)
        if category:
            tasks = [t for t in tasks if t.category == category]
        if status:
            tasks = [t for t in tasks if t.status == status]

    else:
        print("✗ Invalid choice!")
        return

    if not tasks:
        print("\nNo tasks match the filter criteria.")
        return

    print(f"\nFiltered Results ({len(tasks)} found):\n")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)


def option_6_mark_complete(service):
    """Option 6: Mark task as complete"""
    print("\n--- MARK TASK COMPLETE ---\n")

    # Show pending tasks
    tasks = [t for t in service.get_all_tasks() if t.status == "pending"]
    if not tasks:
        print("No pending tasks.")
        return

    print("Pending tasks:")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_id = input("Enter task ID to complete (or task number): ").strip()

    # If user entered a number, convert it to task ID
    if task_id.isdigit():
        task_num = int(task_id) - 1
        if 0 <= task_num < len(tasks):
            task_id = tasks[task_num].id
        else:
            print("✗ Invalid task number!")
            return

    try:
        task = service.mark_complete(task_id)
        print(f"\n✓ Task marked as complete!")
        print_task(task)
    except Exception as e:
        print(f"\n✗ Error: {e}")


def option_7_mark_pending(service):
    """Option 7: Mark task as pending"""
    print("\n--- MARK TASK PENDING ---\n")

    # Show completed tasks
    tasks = [t for t in service.get_all_tasks() if t.status == "completed"]
    if not tasks:
        print("No completed tasks.")
        return

    print("Completed tasks:")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_id = input("Enter task ID to mark pending (or task number): ").strip()

    # If user entered a number, convert it to task ID
    if task_id.isdigit():
        task_num = int(task_id) - 1
        if 0 <= task_num < len(tasks):
            task_id = tasks[task_num].id
        else:
            print("✗ Invalid task number!")
            return

    try:
        task = service.mark_pending(task_id)
        print(f"\n✓ Task marked as pending!")
        print_task(task)
    except Exception as e:
        print(f"\n✗ Error: {e}")


def option_8_show_task_details(service):
    """Option 8: Show task details"""
    print("\n--- TASK DETAILS ---\n")

    # Show all tasks
    tasks = service.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("Available tasks:")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_id = input("Enter task ID to view (or task number): ").strip()

    # If user entered a number, convert it to task ID
    if task_id.isdigit():
        task_num = int(task_id) - 1
        if 0 <= task_num < len(tasks):
            task_id = tasks[task_num].id
        else:
            print("✗ Invalid task number!")
            return

    task = service.get_task(task_id)
    if not task:
        print(f"✗ Task not found: {task_id}")
        return

    print(f"\nTask Details:")
    print("=" * 60)
    print(f"ID:          {task.id}")
    print(f"Title:       {task.title}")
    print(f"Status:      {task.status}")
    print(f"Priority:    {task.priority}")
    print(f"Category:    {task.category or 'None'}")
    print(f"Due Date:    {task.due_date or 'None'}")
    print(f"Recurrence:  {task.recurrence or 'None'}")
    print(f"Overdue:     {'Yes' if task.is_overdue else 'No'}")
    print(f"Created:     {task.created_timestamp}")
    if task.completed_timestamp:
        print(f"Completed:   {task.completed_timestamp}")
    print("=" * 60)


def option_9_view_statistics(service):
    """Option 9: View statistics"""
    print("\n--- STATISTICS ---\n")

    stats = service.get_completion_stats()
    overdue = service.get_overdue_tasks()
    all_tasks = service.get_all_tasks()

    # Count by priority
    high_priority = len([t for t in all_tasks if t.priority == "high"])
    medium_priority = len([t for t in all_tasks if t.priority == "medium"])
    low_priority = len([t for t in all_tasks if t.priority == "low"])

    # Count by category
    categories = {}
    for task in all_tasks:
        cat = task.category or "Uncategorized"
        categories[cat] = categories.get(cat, 0) + 1

    print("=" * 60)
    print("TASK STATISTICS")
    print("=" * 60)
    print(f"Total Tasks:        {stats['total']}")
    print(f"Completed:          {stats['completed']}")
    print(f"Pending:            {stats['pending']}")
    print(f"Completion Rate:    {stats['completion_percentage']}%")
    print(f"Overdue Tasks:      {len(overdue)}")
    print("\nPriority Breakdown:")
    print(f"  High:             {high_priority}")
    print(f"  Medium:           {medium_priority}")
    print(f"  Low:              {low_priority}")
    print("\nCategory Breakdown:")
    for category, count in sorted(categories.items()):
        print(f"  {category}:       {count}")
    print("=" * 60)


def main():
    """Main interactive CLI"""
    service = TaskService()

    print("\n" + "=" * 60)
    print("          Welcome to Todo App")
    print("=" * 60)

    while True:
        print_main_menu()
        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            option_1_create_task(service)
        elif choice == "2":
            option_2_delete_task(service)
        elif choice == "3":
            option_3_list_all_tasks(service)
        elif choice == "4":
            option_4_search_tasks(service)
        elif choice == "5":
            option_5_filter_tasks(service)
        elif choice == "6":
            option_6_mark_complete(service)
        elif choice == "7":
            option_7_mark_pending(service)
        elif choice == "8":
            option_8_show_task_details(service)
        elif choice == "9":
            option_9_view_statistics(service)
        elif choice == "10":
            print("\n✓ Goodbye! Your tasks have been saved.")
            break
        else:
            print("✗ Invalid choice! Please select 1-10.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Goodbye,Thanks for using TODO APP! Your tasks have been saved.")
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
