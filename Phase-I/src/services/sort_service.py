"""Sort service for ordering tasks by various criteria"""

from typing import List, Optional
from datetime import date
from src.models.task import Task


class SortService:
    """Service for sorting tasks by various criteria"""

    @staticmethod
    def sort_by_priority(
        tasks: List[Task], descending: bool = True
    ) -> List[Task]:
        """Sort tasks by priority level.

        Args:
            tasks: List of tasks to sort
            descending: If True, sort high to low (default). If False, sort low to high.

        Returns:
            New list of tasks sorted by priority

        Note:
            Priority order: high (0) > medium (1) > low (2)
            When descending=True: high first, then medium, then low
            When descending=False: low first, then medium, then high
        """
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            tasks,
            key=lambda task: priority_order.get(task.priority, 1),
            reverse=not descending,
        )
        return sorted_tasks

    @staticmethod
    def sort_by_status(
        tasks: List[Task], pending_first: bool = True
    ) -> List[Task]:
        """Sort tasks by status.

        Args:
            tasks: List of tasks to sort
            pending_first: If True, pending tasks first (default). If False, completed first.

        Returns:
            New list of tasks sorted by status
        """
        status_order = {"pending": 0, "completed": 1}
        reverse = not pending_first
        sorted_tasks = sorted(
            tasks,
            key=lambda task: status_order.get(task.status, 1),
            reverse=reverse,
        )
        return sorted_tasks

    @staticmethod
    def sort_by_title(
        tasks: List[Task], reverse: bool = False
    ) -> List[Task]:
        """Sort tasks by title alphabetically.

        Args:
            tasks: List of tasks to sort
            reverse: If True, sort Z to A. If False (default), sort A to Z.

        Returns:
            New list of tasks sorted by title
        """
        sorted_tasks = sorted(tasks, key=lambda task: task.title.lower(), reverse=reverse)
        return sorted_tasks

    @staticmethod
    def sort_by_due_date(
        tasks: List[Task], ascending: bool = True
    ) -> List[Task]:
        """Sort tasks by due date.

        Tasks without due dates are placed at the end (or beginning if descending).

        Args:
            tasks: List of tasks to sort
            ascending: If True (default), earliest dates first. If False, latest first.

        Returns:
            New list of tasks sorted by due date
        """
        # Separate tasks with and without due dates
        with_due_date = [t for t in tasks if t.due_date is not None]
        without_due_date = [t for t in tasks if t.due_date is None]

        # Sort tasks with due dates
        sorted_with = sorted(
            with_due_date,
            key=lambda task: task.due_date,
            reverse=not ascending
        )

        # Combine: with due dates first (or last if descending)
        if ascending:
            return sorted_with + without_due_date
        else:
            return without_due_date + sorted_with

    @staticmethod
    def sort_by_created_date(
        tasks: List[Task], ascending: bool = True
    ) -> List[Task]:
        """Sort tasks by creation date.

        Args:
            tasks: List of tasks to sort
            ascending: If True (default), oldest first. If False, newest first.

        Returns:
            New list of tasks sorted by creation date
        """
        sorted_tasks = sorted(
            tasks,
            key=lambda task: task.created_timestamp,
            reverse=not ascending
        )
        return sorted_tasks

    @staticmethod
    def sort_by_category(
        tasks: List[Task], reverse: bool = False
    ) -> List[Task]:
        """Sort tasks by category alphabetically.

        Tasks without categories are placed at the end.

        Args:
            tasks: List of tasks to sort
            reverse: If True, sort Z to A. If False (default), sort A to Z.

        Returns:
            New list of tasks sorted by category
        """
        # Separate tasks with and without category
        with_category = [t for t in tasks if t.category is not None]
        without_category = [t for t in tasks if t.category is None]

        # Sort tasks with category
        sorted_with = sorted(
            with_category,
            key=lambda task: task.category.lower(),
            reverse=reverse
        )

        # Combine: with category first
        return sorted_with + without_category

    @staticmethod
    def sort_by_recurrence(
        tasks: List[Task], recurring_first: bool = True
    ) -> List[Task]:
        """Sort tasks by recurrence pattern.

        Args:
            tasks: List of tasks to sort
            recurring_first: If True, recurring tasks first (default). If False, non-recurring first.

        Returns:
            New list of tasks sorted by recurrence
        """
        recurring = [t for t in tasks if t.recurrence is not None]
        non_recurring = [t for t in tasks if t.recurrence is None]

        if recurring_first:
            return recurring + non_recurring
        else:
            return non_recurring + recurring

    @staticmethod
    def sort_by_completion_status(
        tasks: List[Task], completed_first: bool = False
    ) -> List[Task]:
        """Sort tasks by completion status with secondary sort.

        Args:
            tasks: List of tasks to sort
            completed_first: If True, completed first. If False (default), pending first.

        Returns:
            New list of tasks sorted by completion status
        """
        return SortService.sort_by_status(
            tasks, pending_first=not completed_first
        )

    @staticmethod
    def multi_sort(
        tasks: List[Task],
        primary_field: str = "priority",
        secondary_field: Optional[str] = None,
        tertiary_field: Optional[str] = None,
        ascending: bool = True,
    ) -> List[Task]:
        """Sort tasks by multiple fields with priority ordering.

        Args:
            tasks: List of tasks to sort
            primary_field: Primary sort field (priority, status, title, due_date, created, category)
            secondary_field: Optional secondary sort field
            tertiary_field: Optional tertiary sort field
            ascending: If True, ascending order for all fields. If False, descending.

        Returns:
            New list of tasks sorted by specified fields
        """
        # First apply tertiary sort if specified
        if tertiary_field:
            tasks = SortService._sort_by_field(tasks, tertiary_field, ascending)

        # Then apply secondary sort if specified
        if secondary_field:
            tasks = SortService._sort_by_field(tasks, secondary_field, ascending)

        # Finally apply primary sort
        tasks = SortService._sort_by_field(tasks, primary_field, ascending)

        return tasks

    @staticmethod
    def _sort_by_field(
        tasks: List[Task], field: str, ascending: bool = True
    ) -> List[Task]:
        """Internal method to sort by a single field.

        Args:
            tasks: List of tasks to sort
            field: Field to sort by
            ascending: Sort direction

        Returns:
            Sorted list of tasks
        """
        if field == "priority":
            return SortService.sort_by_priority(tasks, descending=not ascending)
        elif field == "status":
            return SortService.sort_by_status(tasks, pending_first=ascending)
        elif field == "title":
            return SortService.sort_by_title(tasks, reverse=not ascending)
        elif field == "due_date":
            return SortService.sort_by_due_date(tasks, ascending=ascending)
        elif field == "created":
            return SortService.sort_by_created_date(tasks, ascending=ascending)
        elif field == "category":
            return SortService.sort_by_category(tasks, reverse=not ascending)
        else:
            return tasks

    @staticmethod
    def sort_overdue_first(tasks: List[Task]) -> List[Task]:
        """Sort tasks with overdue tasks first.

        Args:
            tasks: List of tasks to sort

        Returns:
            List of tasks with overdue tasks at the beginning
        """
        overdue = [t for t in tasks if t.is_overdue]
        not_overdue = [t for t in tasks if not t.is_overdue]
        return overdue + not_overdue

    @staticmethod
    def sort_high_priority_first(tasks: List[Task]) -> List[Task]:
        """Sort tasks with high priority first.

        Args:
            tasks: List of tasks to sort

        Returns:
            List of tasks with high priority first
        """
        return SortService.sort_by_priority(tasks, descending=True)

    @staticmethod
    def sort_pending_first(tasks: List[Task]) -> List[Task]:
        """Sort tasks with pending first.

        Args:
            tasks: List of tasks to sort

        Returns:
            List of tasks with pending first
        """
        return SortService.sort_by_status(tasks, pending_first=True)
