"""Category management service for tasks"""

from typing import List, Optional, Set
from src.models.task import Task
from src.models.validators import validate_category


class CategoryService:
    """Service for managing task categories"""

    @staticmethod
    def validate_category(category: Optional[str]) -> bool:
        """Validate category value.

        Args:
            category: Category string to validate (optional)

        Returns:
            True if valid

        Raises:
            ValueError: If category is invalid
        """
        return validate_category(category)

    @staticmethod
    def filter_by_category(tasks: List[Task], category: str) -> List[Task]:
        """Filter tasks by category.

        Args:
            tasks: List of tasks to filter
            category: Category to filter by

        Returns:
            List of tasks matching the category

        Raises:
            ValueError: If category is invalid
        """
        validate_category(category)
        return [task for task in tasks if task.category == category]

    @staticmethod
    def filter_by_categories(
        tasks: List[Task], categories: List[str]
    ) -> List[Task]:
        """Filter tasks by multiple categories (OR operation).

        Args:
            tasks: List of tasks to filter
            categories: List of categories to filter by

        Returns:
            List of tasks matching any of the categories

        Raises:
            ValueError: If any category is invalid
        """
        for category in categories:
            validate_category(category)

        return [task for task in tasks if task.category in categories]

    @staticmethod
    def get_all_categories(tasks: List[Task]) -> Set[str]:
        """Get all unique categories used in tasks.

        Args:
            tasks: List of tasks to analyze

        Returns:
            Set of all unique category values (excluding None)
        """
        categories = {task.category for task in tasks if task.category is not None}
        return categories

    @staticmethod
    def get_category_summary(tasks: List[Task]) -> dict:
        """Get summary of task counts by category.

        Args:
            tasks: List of tasks to analyze

        Returns:
            Dictionary with counts for each category
            Example: {"work": 3, "personal": 2, "uncategorized": 1}
        """
        summary: dict = {}
        uncategorized_count = 0

        for task in tasks:
            if task.category:
                summary[task.category] = summary.get(task.category, 0) + 1
            else:
                uncategorized_count += 1

        if uncategorized_count > 0:
            summary["uncategorized"] = uncategorized_count

        return summary

    @staticmethod
    def set_category(task: Task, category: Optional[str]) -> Task:
        """Set task category.

        Args:
            task: Task to update
            category: New category value (or None to unset)

        Returns:
            Updated task

        Raises:
            ValueError: If category is invalid
        """
        validate_category(category)
        task.category = category
        return task

    @staticmethod
    def remove_category(task: Task) -> Task:
        """Remove category from task (set to None).

        Args:
            task: Task to update

        Returns:
            Updated task with category set to None
        """
        task.category = None
        return task

    @staticmethod
    def rename_category(
        tasks: List[Task], old_category: str, new_category: str
    ) -> List[Task]:
        """Rename a category across all tasks.

        Args:
            tasks: List of tasks to update
            old_category: Current category name to replace
            new_category: New category name

        Returns:
            List of updated tasks

        Raises:
            ValueError: If new_category is invalid
        """
        validate_category(old_category)
        validate_category(new_category)

        updated_tasks = []
        for task in tasks:
            if task.category == old_category:
                task.category = new_category
            updated_tasks.append(task)

        return updated_tasks

    @staticmethod
    def tasks_with_category(tasks: List[Task]) -> List[Task]:
        """Get all tasks that have a category assigned.

        Args:
            tasks: List of tasks to filter

        Returns:
            List of tasks with non-None category
        """
        return [task for task in tasks if task.category is not None]

    @staticmethod
    def tasks_without_category(tasks: List[Task]) -> List[Task]:
        """Get all tasks that don't have a category assigned.

        Args:
            tasks: List of tasks to filter

        Returns:
            List of tasks with None category
        """
        return [task for task in tasks if task.category is None]
