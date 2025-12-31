"""Search service for finding tasks by keyword"""

from typing import List
from src.models.task import Task


class SearchService:
    """Service for searching tasks by keyword"""

    @staticmethod
    def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
        """Search tasks by keyword with case-insensitive partial matching.

        Searches task titles for the keyword using case-insensitive matching.
        A match occurs when the keyword appears anywhere in the title.

        Args:
            tasks: List of tasks to search
            keyword: Search keyword (case-insensitive)

        Returns:
            List of tasks where keyword matches (case-insensitive) any part of the title

        Raises:
            ValueError: If keyword is empty or None
        """
        if not keyword or (isinstance(keyword, str) and not keyword.strip()):
            raise ValueError("Search keyword cannot be empty")

        keyword_lower = keyword.lower()
        matching_tasks = [
            task for task in tasks
            if keyword_lower in task.title.lower()
        ]
        return matching_tasks

    @staticmethod
    def search_by_title(tasks: List[Task], keyword: str) -> List[Task]:
        """Search tasks by title keyword (alias for search_tasks).

        Args:
            tasks: List of tasks to search
            keyword: Search keyword for title (case-insensitive)

        Returns:
            List of tasks matching the keyword

        Raises:
            ValueError: If keyword is empty
        """
        return SearchService.search_tasks(tasks, keyword)

    @staticmethod
    def search_by_title_exact(tasks: List[Task], title: str) -> List[Task]:
        """Search tasks by exact title match (case-insensitive).

        Args:
            tasks: List of tasks to search
            title: Exact title to match (case-insensitive)

        Returns:
            List of tasks with exact title match

        Raises:
            ValueError: If title is empty
        """
        if not title or (isinstance(title, str) and not title.strip()):
            raise ValueError("Title cannot be empty")

        title_lower = title.lower()
        matching_tasks = [
            task for task in tasks
            if task.title.lower() == title_lower
        ]
        return matching_tasks

    @staticmethod
    def search_by_category_and_keyword(
        tasks: List[Task], category: str, keyword: str
    ) -> List[Task]:
        """Search tasks by category and keyword.

        Filters by category first, then searches within those tasks by keyword.

        Args:
            tasks: List of tasks to search
            category: Category to filter by
            keyword: Keyword to search in title (case-insensitive)

        Returns:
            List of tasks in the category matching the keyword

        Raises:
            ValueError: If keyword is empty
        """
        # First filter by category
        category_tasks = [task for task in tasks if task.category == category]

        # Then search within those tasks
        return SearchService.search_tasks(category_tasks, keyword)

    @staticmethod
    def search_by_priority_and_keyword(
        tasks: List[Task], priority: str, keyword: str
    ) -> List[Task]:
        """Search tasks by priority and keyword.

        Filters by priority first, then searches within those tasks by keyword.

        Args:
            tasks: List of tasks to search
            priority: Priority to filter by (high, medium, low)
            keyword: Keyword to search in title (case-insensitive)

        Returns:
            List of tasks with the priority matching the keyword

        Raises:
            ValueError: If keyword is empty
        """
        # First filter by priority
        priority_tasks = [task for task in tasks if task.priority == priority]

        # Then search within those tasks
        return SearchService.search_tasks(priority_tasks, keyword)

    @staticmethod
    def search_and_sort(
        tasks: List[Task], keyword: str, sort_by: str = "created"
    ) -> List[Task]:
        """Search tasks and return sorted results.

        Args:
            tasks: List of tasks to search
            keyword: Search keyword (case-insensitive)
            sort_by: Sort field - created (default), priority, status, title, due_date

        Returns:
            List of matching tasks, sorted by specified field

        Raises:
            ValueError: If keyword is empty
        """
        matching_tasks = SearchService.search_tasks(tasks, keyword)

        # Sort by specified field
        if sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            matching_tasks = sorted(
                matching_tasks,
                key=lambda t: priority_order.get(t.priority, 1)
            )
        elif sort_by == "status":
            # Pending first, then completed
            status_order = {"pending": 0, "completed": 1}
            matching_tasks = sorted(
                matching_tasks,
                key=lambda t: status_order.get(t.status, 1)
            )
        elif sort_by == "title":
            matching_tasks = sorted(matching_tasks, key=lambda t: t.title)
        elif sort_by == "due_date":
            from datetime import date
            matching_tasks = sorted(
                matching_tasks,
                key=lambda t: t.due_date or date.max
            )
        # Default: created (original order)

        return matching_tasks

    @staticmethod
    def get_search_stats(tasks: List[Task], keyword: str) -> dict:
        """Get statistics about search results.

        Args:
            tasks: List of tasks to search
            keyword: Search keyword (case-insensitive)

        Returns:
            Dictionary with search statistics including:
            - total_matches: Number of matching tasks
            - by_status: Count of matches by status
            - by_priority: Count of matches by priority
            - by_category: Count of matches by category

        Raises:
            ValueError: If keyword is empty
        """
        matching_tasks = SearchService.search_tasks(tasks, keyword)

        stats = {
            "total_matches": len(matching_tasks),
            "by_status": {},
            "by_priority": {},
            "by_category": {}
        }

        # Count by status
        for task in matching_tasks:
            status = task.status
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            priority = task.priority
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

            category = task.category or "uncategorized"
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        return stats

    @staticmethod
    def search_with_filters(
        tasks: List[Task],
        keyword: str,
        status: str = None,
        priority: str = None,
        category: str = None
    ) -> List[Task]:
        """Search tasks with multiple filters.

        Args:
            tasks: List of tasks to search
            keyword: Search keyword (case-insensitive)
            status: Optional status filter (pending, completed)
            priority: Optional priority filter (high, medium, low)
            category: Optional category filter

        Returns:
            List of tasks matching keyword and all provided filters

        Raises:
            ValueError: If keyword is empty
        """
        # Start with keyword search
        matching_tasks = SearchService.search_tasks(tasks, keyword)

        # Apply status filter if provided
        if status:
            matching_tasks = [t for t in matching_tasks if t.status == status]

        # Apply priority filter if provided
        if priority:
            matching_tasks = [t for t in matching_tasks if t.priority == priority]

        # Apply category filter if provided
        if category:
            matching_tasks = [t for t in matching_tasks if t.category == category]

        return matching_tasks
