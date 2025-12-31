"""Beautiful interactive CLI for Todo application with colors and styling"""

import sys
from datetime import date
from src.services.task_service import TaskService


# Color codes for terminal
class Colors:
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

    # Text styling
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Reset
    RESET = '\033[0m'


def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text):
    """Print styled header"""
    width = 70
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'═' * width}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(width)}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'═' * width}{Colors.RESET}\n")


def print_subheader(text):
    """Print styled subheader"""
    print(f"\n{Colors.BRIGHT_CYAN}{Colors.BOLD}▶ {text}{Colors.RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}{Colors.BOLD}✓{Colors.RESET} {Colors.GREEN}{text}{Colors.RESET}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}{Colors.BOLD}✗{Colors.RESET} {Colors.RED}{text}{Colors.RESET}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}{Colors.BOLD}ℹ{Colors.RESET} {Colors.BLUE}{text}{Colors.RESET}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠{Colors.RESET} {Colors.YELLOW}{text}{Colors.RESET}")


def print_task(task, index=None):
    """Pretty print a task with colors"""
    # Status icon and color
    if task.status == "completed":
        status_icon = f"{Colors.GREEN}✓{Colors.RESET}"
        title_color = Colors.DIM
    else:
        status_icon = f"{Colors.YELLOW}○{Colors.RESET}"
        title_color = Colors.WHITE

    # Priority color
    if task.priority == "high":
        priority_color = Colors.RED
        priority_str = f"{priority_color}{Colors.BOLD}HIGH{Colors.RESET}"
    elif task.priority == "low":
        priority_color = Colors.GREEN
        priority_str = f"{priority_color}LOW{Colors.RESET}"
    else:
        priority_color = Colors.YELLOW
        priority_str = f"{priority_color}MED{Colors.RESET}"

    # Category
    category_str = ""
    if task.category:
        category_str = f" {Colors.MAGENTA}[{task.category.upper()}]{Colors.RESET}"

    # Overdue marker
    overdue_marker = ""
    if task.is_overdue:
        overdue_marker = f" {Colors.RED}{Colors.BOLD}[OVERDUE]{Colors.RESET}"

    # Index
    prefix = ""
    if index is not None:
        prefix = f"{Colors.CYAN}{index:2d}.{Colors.RESET} "

    # Task ID color
    task_id_color = Colors.BRIGHT_BLUE

    print(f"{prefix}{status_icon} {task_id_color}{task.id}{Colors.RESET} {title_color}│{Colors.RESET} {title_color}{task.title}{Colors.RESET}{category_str} {priority_str}{overdue_marker}")


def print_divider():
    """Print a divider line"""
    print(f"{Colors.BRIGHT_BLACK}{'─' * 70}{Colors.RESET}")


def input_colored(prompt, color=Colors.CYAN):
    """Get colored input"""
    return input(f"{color}{prompt}{Colors.RESET}")


def print_main_menu():
    """Print main menu with attractive layout"""
    clear_screen()
    print_header("✨ TODO APP - INTERACTIVE CLI ✨")

    menu_items = [
        ("1", "Create Task", "➕"),
        ("2", "Delete Task", "🗑️ "),
        ("3", "List All Tasks", "📋"),
        ("4", "Search Tasks", "🔍"),
        ("5", "Filter Tasks", "🔎"),
        ("6", "Mark Complete", "✅"),
        ("7", "Mark Pending", "🔄"),
        ("8", "Show Details", "📝"),
        ("9", "Statistics", "📊"),
        ("10", "Exit", "🚪"),
    ]

    for num, text, emoji in menu_items:
        print(f"  {Colors.CYAN}{Colors.BOLD}{num:2s}.{Colors.RESET} {emoji} {Colors.WHITE}{text:<25}{Colors.RESET}", end="")
        if num == "5" or num == "9":
            print()
        elif num != "10":
            print()
        else:
            print()

    print()


def option_1_create_task(service):
    """Option 1: Create a new task"""
    print_subheader("CREATE NEW TASK")

    try:
        title = input_colored("  📝 Task title: ")
        if not title:
            print_error("Title cannot be empty!")
            return

        print()
        print_info("Priority levels: high (🔴), medium (🟡), low (🟢)")
        priority = input_colored("  Priority [default: medium]: ").strip().lower() or "medium"

        print()
        category = input_colored("  Category [optional]: ").strip() or None

        print()
        due_date_str = input_colored("  Due date [YYYY-MM-DD]: ").strip()
        due_date = None
        if due_date_str:
            try:
                due_date = date.fromisoformat(due_date_str)
            except ValueError:
                print_error("Invalid date format! Use YYYY-MM-DD")
                return

        task = service.create_task(
            title,
            priority=priority,
            category=category,
            due_date=due_date
        )
        print()
        print_success(f"Task created successfully!")
        print_divider()
        print_task(task)
        print_divider()

    except Exception as e:
        print_error(f"Error creating task: {e}")


def option_2_delete_task(service):
    """Option 2: Delete a task"""
    print_subheader("DELETE TASK")

    tasks = service.get_all_tasks()
    if not tasks:
        print_warning("No tasks to delete.")
        return

    print(f"  Available tasks:\n")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_input = input_colored("  Enter task ID or number to delete: ")

    try:
        if task_input.isdigit():
            task_num = int(task_input) - 1
            if 0 <= task_num < len(tasks):
                task_id = tasks[task_num].id
            else:
                print_error("Invalid task number!")
                return
        else:
            task_id = task_input

        if service.delete_task(task_id):
            print()
            print_success(f"Task deleted: {task_id}")
        else:
            print_error(f"Task not found: {task_id}")

    except Exception as e:
        print_error(f"Error: {e}")


def option_3_list_all_tasks(service):
    """Option 3: List all tasks"""
    print_subheader("ALL TASKS")

    tasks = service.get_all_tasks()
    if not tasks:
        print_warning("No tasks found. Create one to get started!")
        return

    print()
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print_divider()
    stats = service.get_completion_stats()
    print(f"  {Colors.BRIGHT_CYAN}Total:{Colors.RESET} {Colors.CYAN}{stats['total']}{Colors.RESET} " +
          f"{Colors.BRIGHT_GREEN}✓ Completed:{Colors.RESET} {Colors.GREEN}{stats['completed']}{Colors.RESET} " +
          f"{Colors.BRIGHT_YELLOW}○ Pending:{Colors.RESET} {Colors.YELLOW}{stats['pending']}{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}Completion Rate:{Colors.RESET} {Colors.MAGENTA}{stats['completion_percentage']}%{Colors.RESET}")
    print_divider()


def option_4_search_tasks(service):
    """Option 4: Search tasks"""
    print_subheader("SEARCH TASKS")

    keyword = input_colored("  🔍 Enter search keyword: ")
    if not keyword:
        print_error("Keyword cannot be empty!")
        return

    results = service.search_tasks(keyword)

    if not results:
        print_warning(f"No tasks found matching '{keyword}'")
        return

    print(f"\n  {Colors.BRIGHT_GREEN}Search Results for '{keyword}' ({len(results)} found):{Colors.RESET}\n")
    for i, task in enumerate(results, 1):
        print_task(task, i)


def option_5_filter_tasks(service):
    """Option 5: Filter tasks"""
    print_subheader("FILTER TASKS")

    print("  Filter by:")
    print(f"    {Colors.CYAN}1.{Colors.RESET} Priority")
    print(f"    {Colors.CYAN}2.{Colors.RESET} Category")
    print(f"    {Colors.CYAN}3.{Colors.RESET} Status")
    print(f"    {Colors.CYAN}4.{Colors.RESET} Multiple filters")

    choice = input_colored("\n  Select filter type (1-4): ")

    tasks = service.get_all_tasks()

    try:
        if choice == "1":
            print_info("Priorities: high, medium, low")
            priority = input_colored("  Priority: ").strip().lower()
            tasks = service.filter_by_priority(priority)

        elif choice == "2":
            category = input_colored("  Category: ").strip()
            tasks = [t for t in tasks if t.category == category]

        elif choice == "3":
            print_info("Statuses: pending, completed")
            status = input_colored("  Status: ").strip().lower()
            tasks = [t for t in tasks if t.status == status]

        elif choice == "4":
            print_info("Leave empty to skip")
            priority = input_colored("  Priority (high/medium/low): ").strip().lower() or None
            category = input_colored("  Category: ").strip() or None
            status = input_colored("  Status (pending/completed): ").strip().lower() or None

            if priority:
                tasks = service.filter_by_priority(priority)
            if category:
                tasks = [t for t in tasks if t.category == category]
            if status:
                tasks = [t for t in tasks if t.status == status]

        else:
            print_error("Invalid choice!")
            return

        if not tasks:
            print_warning("No tasks match the filter criteria.")
            return

        print(f"\n  {Colors.BRIGHT_GREEN}Filtered Results ({len(tasks)} found):{Colors.RESET}\n")
        for i, task in enumerate(tasks, 1):
            print_task(task, i)

    except Exception as e:
        print_error(f"Error: {e}")


def option_6_mark_complete(service):
    """Option 6: Mark task as complete"""
    print_subheader("MARK TASK COMPLETE")

    tasks = [t for t in service.get_all_tasks() if t.status == "pending"]
    if not tasks:
        print_warning("No pending tasks.")
        return

    print(f"  Pending tasks:\n")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_input = input_colored("  Enter task ID or number to complete: ")

    try:
        if task_input.isdigit():
            task_num = int(task_input) - 1
            if 0 <= task_num < len(tasks):
                task_id = tasks[task_num].id
            else:
                print_error("Invalid task number!")
                return
        else:
            task_id = task_input

        task = service.mark_complete(task_id)
        print()
        print_success("Task marked as complete!")
        print_divider()
        print_task(task)
        print_divider()

    except Exception as e:
        print_error(f"Error: {e}")


def option_7_mark_pending(service):
    """Option 7: Mark task as pending"""
    print_subheader("MARK TASK PENDING")

    tasks = [t for t in service.get_all_tasks() if t.status == "completed"]
    if not tasks:
        print_warning("No completed tasks.")
        return

    print(f"  Completed tasks:\n")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_input = input_colored("  Enter task ID or number to mark pending: ")

    try:
        if task_input.isdigit():
            task_num = int(task_input) - 1
            if 0 <= task_num < len(tasks):
                task_id = tasks[task_num].id
            else:
                print_error("Invalid task number!")
                return
        else:
            task_id = task_input

        task = service.mark_pending(task_id)
        print()
        print_success("Task marked as pending!")
        print_divider()
        print_task(task)
        print_divider()

    except Exception as e:
        print_error(f"Error: {e}")


def option_8_show_task_details(service):
    """Option 8: Show task details"""
    print_subheader("TASK DETAILS")

    tasks = service.get_all_tasks()
    if not tasks:
        print_warning("No tasks found.")
        return

    print(f"  Available tasks:\n")
    for i, task in enumerate(tasks, 1):
        print_task(task, i)

    print()
    task_input = input_colored("  Enter task ID or number to view: ")

    try:
        if task_input.isdigit():
            task_num = int(task_input) - 1
            if 0 <= task_num < len(tasks):
                task_id = tasks[task_num].id
            else:
                print_error("Invalid task number!")
                return
        else:
            task_id = task_input

        task = service.get_task(task_id)
        if not task:
            print_error(f"Task not found: {task_id}")
            return

        print_divider()
        print(f"  {Colors.BOLD}ID:{Colors.RESET}          {Colors.BRIGHT_BLUE}{task.id}{Colors.RESET}")
        print(f"  {Colors.BOLD}Title:{Colors.RESET}       {Colors.CYAN}{task.title}{Colors.RESET}")
        print(f"  {Colors.BOLD}Status:{Colors.RESET}      {'✅ ' if task.status == 'completed' else '⏳ '}{Colors.YELLOW}{task.status.upper()}{Colors.RESET}")

        # Priority color
        if task.priority == "high":
            priority_display = f"{Colors.RED}{Colors.BOLD}{task.priority.upper()}{Colors.RESET}"
        elif task.priority == "low":
            priority_display = f"{Colors.GREEN}{task.priority.upper()}{Colors.RESET}"
        else:
            priority_display = f"{Colors.YELLOW}{task.priority.upper()}{Colors.RESET}"

        print(f"  {Colors.BOLD}Priority:{Colors.RESET}    {priority_display}")
        print(f"  {Colors.BOLD}Category:{Colors.RESET}    {Colors.MAGENTA}{task.category or 'None'}{Colors.RESET}")
        print(f"  {Colors.BOLD}Due Date:{Colors.RESET}    {Colors.CYAN}{task.due_date or 'None'}{Colors.RESET}")
        print(f"  {Colors.BOLD}Recurrence:{Colors.RESET}  {Colors.BRIGHT_CYAN}{task.recurrence or 'None'}{Colors.RESET}")
        print(f"  {Colors.BOLD}Overdue:{Colors.RESET}     {'🔴 YES' if task.is_overdue else '🟢 NO'}")
        print(f"  {Colors.BOLD}Created:{Colors.RESET}     {Colors.BRIGHT_BLACK}{task.created_timestamp}{Colors.RESET}")
        if task.completed_timestamp:
            print(f"  {Colors.BOLD}Completed:{Colors.RESET}   {Colors.BRIGHT_BLACK}{task.completed_timestamp}{Colors.RESET}")
        print_divider()

    except Exception as e:
        print_error(f"Error: {e}")


def option_9_view_statistics(service):
    """Option 9: View statistics"""
    print_subheader("STATISTICS")

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

    print_divider()
    print(f"  {Colors.BOLD}{Colors.BRIGHT_CYAN}📊 TASK STATISTICS{Colors.RESET}")
    print_divider()

    print(f"  {Colors.BRIGHT_BLUE}Total Tasks:{Colors.RESET}        {Colors.CYAN}{stats['total']}{Colors.RESET}")
    print(f"  {Colors.BRIGHT_GREEN}✅ Completed:{Colors.RESET}       {Colors.GREEN}{stats['completed']}{Colors.RESET}")
    print(f"  {Colors.BRIGHT_YELLOW}○ Pending:{Colors.RESET}          {Colors.YELLOW}{stats['pending']}{Colors.RESET}")
    print(f"  {Colors.BRIGHT_MAGENTA}Completion Rate:{Colors.RESET}   {Colors.MAGENTA}{stats['completion_percentage']}%{Colors.RESET}")
    print(f"  {Colors.BRIGHT_RED}🔴 Overdue Tasks:{Colors.RESET}     {Colors.RED}{len(overdue)}{Colors.RESET}")

    print(f"\n  {Colors.BOLD}{Colors.BRIGHT_CYAN}Priority Breakdown:{Colors.RESET}")
    print(f"    {Colors.RED}🔴 High:{Colors.RESET}     {Colors.RED}{high_priority}{Colors.RESET}")
    print(f"    {Colors.YELLOW}🟡 Medium:{Colors.RESET}   {Colors.YELLOW}{medium_priority}{Colors.RESET}")
    print(f"    {Colors.GREEN}🟢 Low:{Colors.RESET}      {Colors.GREEN}{low_priority}{Colors.RESET}")

    if categories:
        print(f"\n  {Colors.BOLD}{Colors.BRIGHT_CYAN}Category Breakdown:{Colors.RESET}")
        for category, count in sorted(categories.items()):
            print(f"    {Colors.MAGENTA}{category}:{Colors.RESET} {Colors.MAGENTA}{count}{Colors.RESET}")

    print_divider()


def main():
    """Main interactive CLI"""
    service = TaskService()

    while True:
        print_main_menu()
        choice = input_colored("  Choose an option (1-10): ")

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
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Goodbye! Your tasks have been saved.{Colors.RESET}\n")
            break
        else:
            print_error("Invalid choice! Please select 1-10.")

        input_colored(f"\n  Press {Colors.BOLD}Enter{Colors.RESET} to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}{Colors.BOLD}✓ Goodbye! Your tasks have been saved.{Colors.RESET}\n")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
