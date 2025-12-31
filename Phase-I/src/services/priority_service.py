"""Priority management service for tasks"""

from typing import List, Optional
from src.models.task import Task
from src.models.validators import validate_priority


class PriorityService:
    """Service for managing task priorities"""

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate priority value.

        Args:
            priority: Priority string to validate

        Returns:
            True if valid

        Raises:
            ValueError: If priority is invalid
        """
        return validate_priority(priority)

    @staticmethod
    def filter_by_priority(tasks: List[Task], priority: str) -> List[Task]:
        """Filter tasks by priority level.

        Args:
            tasks: List of tasks to filter
            priority: Priority level to filter by (high, medium, low)

        Returns:
            List of tasks matching the priority

        Raises:
            ValueError: If priority is invalid
        """
        validate_priority(priority)
        return [task for task in tasks if task.priority == priority]

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
    def get_priority_summary(tasks: List[Task]) -> dict:
        """Get summary of task counts by priority.

        Args:
            tasks: List of tasks to analyze

        Returns:
            Dictionary with counts for each priority level
            Example: {"high": 2, "medium": 5, "low": 3}
        """
        summary = {"high": 0, "medium": 0, "low": 0}
        for task in tasks:
            if task.priority in summary:
                summary[task.priority] += 1
        return summary

    @staticmethod
    def set_priority(task: Task, priority: str) -> Task:
        """Set task priority.

        Args:
            task: Task to update
            priority: New priority value (high, medium, low)

        Returns:
            Updated task

        Raises:
            ValueError: If priority is invalid
        """
        validate_priority(priority)
        task.priority = priority
        return task
