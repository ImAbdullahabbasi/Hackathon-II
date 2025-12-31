"""Unit tests for search service"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.services.search_service import SearchService


class TestSearchByKeyword:
    """Test basic keyword search"""

    def test_search_case_insensitive_match(self):
        """Test case-insensitive keyword matching"""
        tasks = [
            Task(
                id="task-001",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Buy furniture",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Sell old items",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Search with lowercase
        result = SearchService.search_tasks(tasks, "buy")
        assert len(result) == 2
        assert all("buy" in t.title.lower() for t in result)

        # Search with uppercase
        result = SearchService.search_tasks(tasks, "BUY")
        assert len(result) == 2

        # Search with mixed case (searches for "buy" substring)
        result = SearchService.search_tasks(tasks, "Buy")
        assert len(result) == 2

    def test_search_partial_matching(self):
        """Test partial string matching"""
        tasks = [
            Task(
                id="task-001",
                title="Grocery list review",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Cooking instructions",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Search "grocer" matches both (substring in both)
        result = SearchService.search_tasks(tasks, "grocer")
        assert len(result) == 2

        # Search "list" matches first one
        result = SearchService.search_tasks(tasks, "list")
        assert len(result) == 1

    def test_search_no_matches(self):
        """Test search with no matching results"""
        tasks = [
            Task(
                id="task-001",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Clean house",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SearchService.search_tasks(tasks, "xyz")
        assert len(result) == 0

    def test_search_empty_keyword_raises_error(self):
        """Test that empty keyword raises error"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
            )
        ]

        with pytest.raises(ValueError):
            SearchService.search_tasks(tasks, "")

        with pytest.raises(ValueError):
            SearchService.search_tasks(tasks, "   ")

        with pytest.raises(ValueError):
            SearchService.search_tasks(tasks, None)

    def test_search_special_characters(self):
        """Test search with special characters in title"""
        tasks = [
            Task(
                id="task-001",
                title="Task with (parentheses)",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Task with 'quotes'",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Task with #hashtag",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Search for word with special chars
        result = SearchService.search_tasks(tasks, "parentheses")
        assert len(result) == 1

        result = SearchService.search_tasks(tasks, "quotes")
        assert len(result) == 1

        result = SearchService.search_tasks(tasks, "hashtag")
        assert len(result) == 1

    def test_search_empty_task_list(self):
        """Test search on empty task list"""
        result = SearchService.search_tasks([], "keyword")
        assert len(result) == 0


class TestSearchByTitle:
    """Test title-specific search operations"""

    def test_search_exact_title_match(self):
        """Test exact title matching"""
        tasks = [
            Task(
                id="task-001",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Buy groceries list",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Sell items",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Exact match (case-insensitive)
        result = SearchService.search_by_title_exact(tasks, "Buy groceries")
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Exact match with different case
        result = SearchService.search_by_title_exact(tasks, "buy groceries")
        assert len(result) == 1

    def test_search_exact_title_no_match(self):
        """Test exact title match with no results"""
        tasks = [
            Task(
                id="task-001",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            )
        ]

        result = SearchService.search_by_title_exact(tasks, "Buy groceries list")
        assert len(result) == 0

    def test_search_title_alias(self):
        """Test that search_by_title is alias for search_tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Buy groceries",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Buy furniture",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Both should return same results
        result1 = SearchService.search_tasks(tasks, "buy")
        result2 = SearchService.search_by_title(tasks, "buy")

        assert len(result1) == len(result2)
        assert result1 == result2


class TestSearchWithFilters:
    """Test search combined with other filters"""

    def test_search_by_category_and_keyword(self):
        """Test search within a specific category"""
        tasks = [
            Task(
                id="task-001",
                title="Work on report",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Work on house",
                status="pending",
                created_timestamp=datetime.now(),
                category="home",
            ),
            Task(
                id="task-003",
                title="Personal work",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        # Search "work" in work category
        result = SearchService.search_by_category_and_keyword(
            tasks, "work", "work"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Search "work" in home category
        result = SearchService.search_by_category_and_keyword(
            tasks, "home", "work"
        )
        assert len(result) == 1
        assert result[0].id == "task-002"

    def test_search_by_priority_and_keyword(self):
        """Test search within a specific priority level"""
        tasks = [
            Task(
                id="task-001",
                title="Urgent report",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Urgent meeting",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Urgent review",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
        ]

        # Search "urgent" in high priority
        result = SearchService.search_by_priority_and_keyword(
            tasks, "high", "urgent"
        )
        assert len(result) == 2

        # Search "urgent" in medium priority
        result = SearchService.search_by_priority_and_keyword(
            tasks, "medium", "urgent"
        )
        assert len(result) == 1
        assert result[0].id == "task-003"

    def test_search_with_multiple_filters(self):
        """Test search with multiple filters applied"""
        tasks = [
            Task(
                id="task-001",
                title="Urgent work report",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Urgent work meeting",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-003",
                title="Regular work task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
                category="work",
            ),
        ]

        # Search with all filters
        result = SearchService.search_with_filters(
            tasks,
            keyword="work",
            status="pending",
            priority="high",
            category="work"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Search with partial filters
        result = SearchService.search_with_filters(
            tasks, keyword="work", status="pending"
        )
        assert len(result) == 2

        # Search with only keyword
        result = SearchService.search_with_filters(tasks, keyword="work")
        assert len(result) == 3


class TestSearchAndSort:
    """Test search results with sorting"""

    def test_search_and_sort_by_priority(self):
        """Test search results sorted by priority"""
        tasks = [
            Task(
                id="task-001",
                title="Important work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
            Task(
                id="task-002",
                title="Critical work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Normal work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
        ]

        result = SearchService.search_and_sort(tasks, "work", sort_by="priority")
        assert len(result) == 3
        assert result[0].priority == "high"
        assert result[1].priority == "medium"
        assert result[2].priority == "low"

    def test_search_and_sort_by_status(self):
        """Test search results sorted by status"""
        tasks = [
            Task(
                id="task-001",
                title="Completed work",
                status="completed",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Pending work",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Another work",
                status="completed",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SearchService.search_and_sort(tasks, "work", sort_by="status")
        assert result[0].status == "pending"
        assert result[1].status == "completed"
        assert result[2].status == "completed"

    def test_search_and_sort_by_title(self):
        """Test search results sorted by title"""
        tasks = [
            Task(
                id="task-001",
                title="Zebra work",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Apple work",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Banana work",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SearchService.search_and_sort(tasks, "work", sort_by="title")
        assert result[0].title == "Apple work"
        assert result[1].title == "Banana work"
        assert result[2].title == "Zebra work"

    def test_search_and_sort_by_due_date(self):
        """Test search results sorted by due date"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        tasks = [
            Task(
                id="task-001",
                title="Future work",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=next_week,
            ),
            Task(
                id="task-002",
                title="Soon work",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=tomorrow,
            ),
            Task(
                id="task-003",
                title="Today work",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=today,
            ),
        ]

        result = SearchService.search_and_sort(tasks, "work", sort_by="due_date")
        assert result[0].due_date == today
        assert result[1].due_date == tomorrow
        assert result[2].due_date == next_week

    def test_search_and_sort_default_order(self):
        """Test search results in default order (creation)"""
        tasks = [
            Task(
                id="task-001",
                title="First work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
            Task(
                id="task-002",
                title="Second work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Third work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
        ]

        # Default sort should maintain original order
        result = SearchService.search_and_sort(tasks, "work")
        assert result[0].id == "task-001"
        assert result[1].id == "task-002"
        assert result[2].id == "task-003"


class TestSearchStats:
    """Test search statistics"""

    def test_get_search_stats(self):
        """Test getting statistics about search results"""
        tasks = [
            Task(
                id="task-001",
                title="Work report",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Work meeting",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-003",
                title="Work task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
                category="work",
            ),
            Task(
                id="task-004",
                title="Personal task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]

        # Search for "work"
        stats = SearchService.get_search_stats(tasks, "work")

        # Verify overall count
        assert stats["total_matches"] == 3

        # Verify status breakdown
        assert stats["by_status"]["pending"] == 2
        assert stats["by_status"]["completed"] == 1

        # Verify priority breakdown
        assert stats["by_priority"]["high"] == 2
        assert stats["by_priority"]["medium"] == 1

        # Verify category breakdown
        assert stats["by_category"]["work"] == 3

    def test_get_search_stats_uncategorized(self):
        """Test search stats with uncategorized tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Work task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Work task uncategorized",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        stats = SearchService.get_search_stats(tasks, "work")
        assert stats["by_category"]["work"] == 1
        assert stats["by_category"]["uncategorized"] == 1

    def test_get_search_stats_no_results(self):
        """Test search stats with no matches"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
            )
        ]

        stats = SearchService.get_search_stats(tasks, "xyz")
        assert stats["total_matches"] == 0
        assert stats["by_status"] == {}
        assert stats["by_priority"] == {}
        assert stats["by_category"] == {}
