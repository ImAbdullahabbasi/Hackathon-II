"""Main task management service"""

from typing import List, Optional
from datetime import datetime, date
from src.models.task import Task
from src.storage import TaskStorage
from src.services.priority_service import PriorityService
from src.services.search_service import SearchService


class TaskService:
    """Service for managing tasks with CRUD and filtering operations"""

    def __init__(self, storage: Optional[TaskStorage] = None):
        """Initialize TaskService with storage.

        Args:
            storage: TaskStorage instance (creates new if not provided)
        """
        self.storage = storage or TaskStorage()

    def create_task(
        self,
        title: str,
        status: str = "pending",
        priority: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        recurrence: Optional[str] = None,
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title (required)
            status: Task status (default: pending)
            priority: Task priority - high, medium, low (default: medium)
            category: Task category (optional)
            due_date: Task due date (optional)
            recurrence: Task recurrence - daily, weekly, monthly (optional)

        Returns:
            Created task with assigned ID

        Raises:
            ValueError: If task validation fails
        """
        # Get next task ID from storage
        next_id = self.storage.get_next_task_id()
        task = Task(
            id=next_id,
            title=title,
            status=status,
            created_timestamp=datetime.now(),
            priority=priority or "medium",
            category=category,
            due_date=due_date,
            recurrence=recurrence,
        )
        return self.storage.create(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self.storage.read(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        return self.storage.read_all()

    def update_task(self, task_id: str, **updates) -> Task:
        """Update a task.

        Args:
            task_id: ID of task to update
            **updates: Fields to update

        Returns:
            Updated task

        Raises:
            ValueError: If task not found
        """
        return self.storage.update(task_id, **updates)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete(task_id)

    def list_all_tasks(self, sort_by: str = "created", reverse: bool = False) -> List[Task]:
        """List all tasks with optional sorting.

        Args:
            sort_by: Sort field - created, priority, due_date, status, title
            reverse: If True, reverse sort order

        Returns:
            List of sorted tasks
        """
        tasks = self.get_all_tasks()

        if sort_by == "priority":
            return PriorityService.sort_by_priority(tasks, descending=not reverse)
        elif sort_by == "due_date":
            tasks = sorted(
                tasks,
                key=lambda t: t.due_date or date.max,
                reverse=reverse
            )
        elif sort_by == "status":
            tasks = sorted(tasks, key=lambda t: t.status, reverse=reverse)
        elif sort_by == "title":
            tasks = sorted(tasks, key=lambda t: t.title, reverse=reverse)
        # Default: created (original order)

        return tasks

    def filter_by_status(self, status: str) -> List[Task]:
        """Filter tasks by status.

        Args:
            status: Status to filter by - pending or completed

        Returns:
            List of tasks with matching status
        """
        return [task for task in self.get_all_tasks() if task.status == status]

    def filter_by_priority(self, priority: str) -> List[Task]:
        """Filter tasks by priority.

        Args:
            priority: Priority to filter by - high, medium, low

        Returns:
            List of tasks with matching priority

        Raises:
            ValueError: If priority is invalid
        """
        return PriorityService.filter_by_priority(self.get_all_tasks(), priority)

    def filter_by_category(self, category: str) -> List[Task]:
        """Filter tasks by category.

        Args:
            category: Category to filter by

        Returns:
            List of tasks with matching category
        """
        return [task for task in self.get_all_tasks() if task.category == category]

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks.

        Returns:
            List of tasks that are overdue (due_date < today and not completed)
        """
        return [
            task for task in self.get_all_tasks()
            if task.is_overdue and task.status == "pending"
        ]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get upcoming tasks due within N days.

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            List of upcoming tasks
        """
        from datetime import timedelta
        cutoff_date = date.today() + timedelta(days=days)
        return [
            task for task in self.get_all_tasks()
            if task.due_date and date.today() <= task.due_date <= cutoff_date
            and task.status == "pending"
        ]

    def mark_complete(self, task_id: str) -> Task:
        """Mark a task as completed.

        Args:
            task_id: ID of task to mark complete

        Returns:
            Updated task

        Raises:
            ValueError: If task not found
        """
        return self.storage.update(
            task_id,
            status="completed",
            completed_timestamp=datetime.now()
        )

    def mark_pending(self, task_id: str) -> Task:
        """Mark a task as pending.

        Args:
            task_id: ID of task to mark pending

        Returns:
            Updated task

        Raises:
            ValueError: If task not found
        """
        return self.storage.update(
            task_id,
            status="pending",
            completed_timestamp=None
        )

    def get_task_count(self) -> int:
        """Get total number of tasks.

        Returns:
            Number of tasks
        """
        return len(self.get_all_tasks())

    def get_completion_stats(self) -> dict:
        """Get task completion statistics.

        Returns:
            Dictionary with completed and pending counts and completion percentage
        """
        tasks = self.get_all_tasks()
        completed = len([t for t in tasks if t.status == "completed"])
        pending = len([t for t in tasks if t.status == "pending"])
        total = len(tasks)
        percentage = (completed / total * 100) if total > 0 else 0

        return {
            "completed": completed,
            "pending": pending,
            "total": total,
            "completion_percentage": round(percentage, 2)
        }

    def clear_all_tasks(self) -> None:
        """Clear all tasks (for testing only)."""
        self.storage.clear()

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title.

        Args:
            keyword: Search keyword (case-insensitive partial match)

        Returns:
            List of tasks matching the keyword

        Raises:
            ValueError: If keyword is empty
        """
        return SearchService.search_tasks(self.get_all_tasks(), keyword)

    def search_tasks_with_filters(
        self,
        keyword: str,
        status: str = None,
        priority: str = None,
        category: str = None
    ) -> List[Task]:
        """Search tasks with additional filters.

        Args:
            keyword: Search keyword (case-insensitive)
            status: Optional status filter
            priority: Optional priority filter
            category: Optional category filter

        Returns:
            List of tasks matching keyword and filters

        Raises:
            ValueError: If keyword is empty
        """
        return SearchService.search_with_filters(
            self.get_all_tasks(),
            keyword,
            status=status,
            priority=priority,
            category=category
        )
