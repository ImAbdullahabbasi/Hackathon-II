"""Unit tests for sort service"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.services.sort_service import SortService


class TestSortByPriority:
    """Test sorting by priority"""

    def test_sort_by_priority_descending(self):
        """Test sorting by priority high to low"""
        tasks = [
            Task(
                id="task-001",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
            Task(
                id="task-002",
                title="High",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Medium",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
        ]

        result = SortService.sort_by_priority(tasks, descending=True)
        assert result[0].priority == "high"
        assert result[1].priority == "medium"
        assert result[2].priority == "low"

    def test_sort_by_priority_ascending(self):
        """Test sorting by priority low to high"""
        tasks = [
            Task(
                id="task-001",
                title="High",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
            Task(
                id="task-003",
                title="Medium",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
        ]

        result = SortService.sort_by_priority(tasks, descending=False)
        assert result[0].priority == "low"
        assert result[1].priority == "medium"
        assert result[2].priority == "high"


class TestSortByStatus:
    """Test sorting by status"""

    def test_sort_by_status_pending_first(self):
        """Test sorting with pending first"""
        tasks = [
            Task(
                id="task-001",
                title="Completed",
                status="completed",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Pending",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Another completed",
                status="completed",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_status(tasks, pending_first=True)
        assert result[0].status == "pending"
        assert result[1].status == "completed"
        assert result[2].status == "completed"

    def test_sort_by_status_completed_first(self):
        """Test sorting with completed first"""
        tasks = [
            Task(
                id="task-001",
                title="Pending",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Completed",
                status="completed",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_status(tasks, pending_first=False)
        assert result[0].status == "completed"
        assert result[1].status == "pending"


class TestSortByTitle:
    """Test sorting by title"""

    def test_sort_by_title_ascending(self):
        """Test sorting by title A to Z"""
        tasks = [
            Task(
                id="task-001",
                title="Zebra",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Apple",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Banana",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_title(tasks, reverse=False)
        assert result[0].title == "Apple"
        assert result[1].title == "Banana"
        assert result[2].title == "Zebra"

    def test_sort_by_title_descending(self):
        """Test sorting by title Z to A"""
        tasks = [
            Task(
                id="task-001",
                title="Apple",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Zebra",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Banana",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_title(tasks, reverse=True)
        assert result[0].title == "Zebra"
        assert result[1].title == "Banana"
        assert result[2].title == "Apple"

    def test_sort_by_title_case_insensitive(self):
        """Test sorting by title is case-insensitive"""
        tasks = [
            Task(
                id="task-001",
                title="apple",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="ZEBRA",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Banana",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_title(tasks, reverse=False)
        assert result[0].title == "apple"
        assert result[1].title == "Banana"
        assert result[2].title == "ZEBRA"


class TestSortByDueDate:
    """Test sorting by due date"""

    def test_sort_by_due_date_ascending(self):
        """Test sorting by due date earliest first"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        tasks = [
            Task(
                id="task-001",
                title="Next week",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=next_week,
            ),
            Task(
                id="task-002",
                title="Tomorrow",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=tomorrow,
            ),
            Task(
                id="task-003",
                title="Today",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=today,
            ),
        ]

        result = SortService.sort_by_due_date(tasks, ascending=True)
        assert result[0].due_date == today
        assert result[1].due_date == tomorrow
        assert result[2].due_date == next_week

    def test_sort_by_due_date_with_no_due_date(self):
        """Test sorting by due date when some tasks have no due date"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        tasks = [
            Task(
                id="task-001",
                title="No due date 1",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Tomorrow",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=tomorrow,
            ),
            Task(
                id="task-003",
                title="Today",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=today,
            ),
            Task(
                id="task-004",
                title="No due date 2",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_by_due_date(tasks, ascending=True)
        # Tasks with due dates should come first
        assert result[0].due_date == today
        assert result[1].due_date == tomorrow
        # Tasks without due dates at the end
        assert result[2].due_date is None
        assert result[3].due_date is None


class TestSortByCreatedDate:
    """Test sorting by creation date"""

    def test_sort_by_created_date_ascending(self):
        """Test sorting by created date oldest first"""
        now = datetime.now()
        earlier = datetime(now.year, now.month, max(1, now.day - 1))

        tasks = [
            Task(
                id="task-001",
                title="Recent",
                status="pending",
                created_timestamp=now,
            ),
            Task(
                id="task-002",
                title="Old",
                status="pending",
                created_timestamp=earlier,
            ),
        ]

        result = SortService.sort_by_created_date(tasks, ascending=True)
        assert result[0].created_timestamp == earlier
        assert result[1].created_timestamp == now


class TestSortByCategory:
    """Test sorting by category"""

    def test_sort_by_category_ascending(self):
        """Test sorting by category A to Z"""
        tasks = [
            Task(
                id="task-001",
                title="Work",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Personal",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
            Task(
                id="task-003",
                title="Home",
                status="pending",
                created_timestamp=datetime.now(),
                category="home",
            ),
        ]

        result = SortService.sort_by_category(tasks, reverse=False)
        assert result[0].category == "home"
        assert result[1].category == "personal"
        assert result[2].category == "work"

    def test_sort_by_category_with_uncategorized(self):
        """Test sorting by category with some uncategorized tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Work",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Uncategorized",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Home",
                status="pending",
                created_timestamp=datetime.now(),
                category="home",
            ),
        ]

        result = SortService.sort_by_category(tasks, reverse=False)
        # Categorized tasks first, uncategorized last
        assert result[0].category == "home"
        assert result[1].category == "work"
        assert result[2].category is None


class TestSortByRecurrence:
    """Test sorting by recurrence"""

    def test_sort_by_recurrence_recurring_first(self):
        """Test sorting with recurring tasks first"""
        tasks = [
            Task(
                id="task-001",
                title="No recurrence",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Daily",
                status="pending",
                created_timestamp=datetime.now(),
                recurrence="daily",
            ),
            Task(
                id="task-003",
                title="Weekly",
                status="pending",
                created_timestamp=datetime.now(),
                recurrence="weekly",
            ),
        ]

        result = SortService.sort_by_recurrence(tasks, recurring_first=True)
        assert result[0].recurrence == "daily"
        assert result[1].recurrence == "weekly"
        assert result[2].recurrence is None


class TestMultiSort:
    """Test multi-field sorting"""

    def test_multi_sort_priority_then_status(self):
        """Test sorting by priority, then status"""
        tasks = [
            Task(
                id="task-001",
                title="High completed",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="High pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Low pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]

        # ascending=True for priority means low to high, descending means high to low
        # Using ascending=False to get high priority first
        result = SortService.multi_sort(
            tasks,
            primary_field="priority",
            secondary_field="status",
            ascending=False
        )

        # High priority should be first (descending), then sorted by status within priority
        assert result[0].priority == "high"
        assert result[1].priority == "high"
        assert result[2].priority == "low"


class TestConvenientSortMethods:
    """Test convenient sort method shortcuts"""

    def test_sort_overdue_first(self):
        """Test convenient method to sort overdue first"""
        past = date.today() - timedelta(days=1)
        future = date.today() + timedelta(days=1)

        tasks = [
            Task(
                id="task-001",
                title="Not overdue",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=future,
            ),
            Task(
                id="task-002",
                title="Overdue",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=past,
            ),
        ]

        result = SortService.sort_overdue_first(tasks)
        assert result[0].is_overdue is True
        assert result[1].is_overdue is False

    def test_sort_high_priority_first(self):
        """Test convenient method to sort high priority first"""
        tasks = [
            Task(
                id="task-001",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
            Task(
                id="task-002",
                title="High",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
        ]

        result = SortService.sort_high_priority_first(tasks)
        assert result[0].priority == "high"
        assert result[1].priority == "low"

    def test_sort_pending_first(self):
        """Test convenient method to sort pending first"""
        tasks = [
            Task(
                id="task-001",
                title="Completed",
                status="completed",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Pending",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = SortService.sort_pending_first(tasks)
        assert result[0].status == "pending"
        assert result[1].status == "completed"


class TestSortEdgeCases:
    """Test edge cases in sorting"""

    def test_sort_empty_list(self):
        """Test sorting an empty list"""
        result = SortService.sort_by_priority([])
        assert result == []

    def test_sort_single_task(self):
        """Test sorting a single task"""
        tasks = [
            Task(
                id="task-001",
                title="Only task",
                status="pending",
                created_timestamp=datetime.now(),
            )
        ]

        result = SortService.sort_by_priority(tasks)
        assert len(result) == 1
        assert result[0].id == "task-001"

    def test_sort_same_priority_maintains_order(self):
        """Test that sorting maintains relative order for equal values"""
        tasks = [
            Task(
                id="task-001",
                title="First high",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Second high",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
        ]

        result = SortService.sort_by_priority(tasks)
        # Both are high, should maintain original order (stable sort)
        assert result[0].id == "task-001"
        assert result[1].id == "task-002"
