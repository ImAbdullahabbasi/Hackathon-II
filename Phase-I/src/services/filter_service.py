"""Filter service for combining multiple filter criteria"""

from typing import List, Optional
from datetime import date
from src.models.task import Task


class FilterService:
    """Service for filtering tasks by multiple criteria with AND logic"""

    @staticmethod
    def filter_tasks(
        tasks: List[Task],
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        is_overdue: Optional[bool] = None,
        has_due_date: Optional[bool] = None,
        is_recurring: Optional[bool] = None,
    ) -> List[Task]:
        """Filter tasks by multiple criteria with AND logic.

        All specified filters must match for a task to be included.

        Args:
            tasks: List of tasks to filter
            status: Optional status filter (pending, completed)
            priority: Optional priority filter (high, medium, low)
            category: Optional category filter
            is_overdue: Optional overdue filter (True for overdue only)
            has_due_date: Optional due date filter (True for tasks with due date)
            is_recurring: Optional recurring filter (True for recurring tasks only)

        Returns:
            List of tasks matching ALL specified filters
        """
        filtered_tasks = list(tasks)

        # Apply status filter
        if status is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if t.status == status
            ]

        # Apply priority filter
        if priority is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if t.priority == priority
            ]

        # Apply category filter
        if category is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if t.category == category
            ]

        # Apply overdue filter
        if is_overdue is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if t.is_overdue == is_overdue
            ]

        # Apply has due date filter
        if has_due_date is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if (t.due_date is not None) == has_due_date
            ]

        # Apply recurring filter
        if is_recurring is not None:
            filtered_tasks = [
                t for t in filtered_tasks
                if (t.recurrence is not None) == is_recurring
            ]

        return filtered_tasks

    @staticmethod
    def filter_by_status_and_priority(
        tasks: List[Task], status: str, priority: str
    ) -> List[Task]:
        """Filter by status AND priority.

        Args:
            tasks: List of tasks to filter
            status: Status to filter by
            priority: Priority to filter by

        Returns:
            Tasks matching both status and priority
        """
        return FilterService.filter_tasks(
            tasks, status=status, priority=priority
        )

    @staticmethod
    def filter_by_status_and_category(
        tasks: List[Task], status: str, category: str
    ) -> List[Task]:
        """Filter by status AND category.

        Args:
            tasks: List of tasks to filter
            status: Status to filter by
            category: Category to filter by

        Returns:
            Tasks matching both status and category
        """
        return FilterService.filter_tasks(
            tasks, status=status, category=category
        )

    @staticmethod
    def filter_by_priority_and_category(
        tasks: List[Task], priority: str, category: str
    ) -> List[Task]:
        """Filter by priority AND category.

        Args:
            tasks: List of tasks to filter
            priority: Priority to filter by
            category: Category to filter by

        Returns:
            Tasks matching both priority and category
        """
        return FilterService.filter_tasks(
            tasks, priority=priority, category=category
        )

    @staticmethod
    def filter_pending_high_priority(tasks: List[Task]) -> List[Task]:
        """Get pending high priority tasks.

        Args:
            tasks: List of tasks to filter

        Returns:
            Tasks that are pending AND high priority
        """
        return FilterService.filter_tasks(
            tasks, status="pending", priority="high"
        )

    @staticmethod
    def filter_pending_by_category(
        tasks: List[Task], category: str
    ) -> List[Task]:
        """Get pending tasks in a specific category.

        Args:
            tasks: List of tasks to filter
            category: Category to filter by

        Returns:
            Tasks that are pending AND in the category
        """
        return FilterService.filter_tasks(
            tasks, status="pending", category=category
        )

    @staticmethod
    def filter_completed_by_priority(
        tasks: List[Task], priority: str
    ) -> List[Task]:
        """Get completed tasks with a specific priority.

        Args:
            tasks: List of tasks to filter
            priority: Priority to filter by

        Returns:
            Tasks that are completed AND have the priority
        """
        return FilterService.filter_tasks(
            tasks, status="completed", priority=priority
        )

    @staticmethod
    def filter_overdue_pending(tasks: List[Task]) -> List[Task]:
        """Get overdue pending tasks.

        Args:
            tasks: List of tasks to filter

        Returns:
            Tasks that are overdue AND pending
        """
        return FilterService.filter_tasks(
            tasks, is_overdue=True, status="pending"
        )

    @staticmethod
    def filter_with_due_date_pending(tasks: List[Task]) -> List[Task]:
        """Get pending tasks that have a due date.

        Args:
            tasks: List of tasks to filter

        Returns:
            Tasks that are pending AND have a due date
        """
        return FilterService.filter_tasks(
            tasks, has_due_date=True, status="pending"
        )

    @staticmethod
    def filter_recurring_pending(tasks: List[Task]) -> List[Task]:
        """Get pending recurring tasks.

        Args:
            tasks: List of tasks to filter

        Returns:
            Tasks that are recurring AND pending
        """
        return FilterService.filter_tasks(
            tasks, is_recurring=True, status="pending"
        )

    @staticmethod
    def get_filter_options(tasks: List[Task]) -> dict:
        """Get available filter options from tasks.

        Useful for CLI or UI to show available filters.

        Args:
            tasks: List of tasks

        Returns:
            Dictionary with available filter options
        """
        statuses = set()
        priorities = set()
        categories = set()
        has_overdue = False
        has_due_date_tasks = False
        has_recurring = False

        for task in tasks:
            statuses.add(task.status)
            priorities.add(task.priority)
            if task.category:
                categories.add(task.category)
            if task.is_overdue:
                has_overdue = True
            if task.due_date:
                has_due_date_tasks = True
            if task.recurrence:
                has_recurring = True

        return {
            "statuses": sorted(list(statuses)),
            "priorities": sorted(list(priorities)),
            "categories": sorted(list(categories)),
            "has_overdue_tasks": has_overdue,
            "has_tasks_with_due_date": has_due_date_tasks,
            "has_recurring_tasks": has_recurring,
        }

    @staticmethod
    def count_by_filter(
        tasks: List[Task],
        filter_field: str
    ) -> dict:
        """Count tasks grouped by a filter field.

        Args:
            tasks: List of tasks
            filter_field: Field to group by (status, priority, category)

        Returns:
            Dictionary with counts for each value
        """
        counts = {}

        for task in tasks:
            if filter_field == "status":
                value = task.status
            elif filter_field == "priority":
                value = task.priority
            elif filter_field == "category":
                value = task.category or "uncategorized"
            else:
                continue

            counts[value] = counts.get(value, 0) + 1

        return counts

    @staticmethod
    def filter_and_count(
        tasks: List[Task],
        group_by: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
    ) -> dict:
        """Filter tasks and return counts grouped by a field.

        Args:
            tasks: List of tasks to filter
            group_by: Field to group results by (status, priority, category)
            status: Optional status filter
            priority: Optional priority filter
            category: Optional category filter

        Returns:
            Dictionary with counts grouped by the specified field
        """
        # First apply filters
        filtered = FilterService.filter_tasks(
            tasks,
            status=status,
            priority=priority,
            category=category
        )

        # Then count by group
        return FilterService.count_by_filter(filtered, group_by)
