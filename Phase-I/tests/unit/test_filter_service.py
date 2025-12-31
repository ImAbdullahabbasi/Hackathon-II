"""Unit tests for filter service"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.services.filter_service import FilterService


class TestMultiCriteriaFilter:
    """Test filtering by multiple criteria with AND logic"""

    def test_filter_by_status_and_priority(self):
        """Test filtering by status AND priority"""
        tasks = [
            Task(
                id="task-001",
                title="High pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="High completed",
                status="completed",
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

        # Filter: pending AND high priority
        result = FilterService.filter_tasks(
            tasks, status="pending", priority="high"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Filter: completed AND high priority
        result = FilterService.filter_tasks(
            tasks, status="completed", priority="high"
        )
        assert len(result) == 1
        assert result[0].id == "task-002"

        # Filter: pending AND low priority
        result = FilterService.filter_tasks(
            tasks, status="pending", priority="low"
        )
        assert len(result) == 1
        assert result[0].id == "task-003"

    def test_filter_by_status_and_category(self):
        """Test filtering by status AND category"""
        tasks = [
            Task(
                id="task-001",
                title="Work pending",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Work completed",
                status="completed",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-003",
                title="Personal pending",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        # Filter: pending AND work
        result = FilterService.filter_tasks(
            tasks, status="pending", category="work"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Filter: completed AND work
        result = FilterService.filter_tasks(
            tasks, status="completed", category="work"
        )
        assert len(result) == 1
        assert result[0].id == "task-002"

    def test_filter_by_priority_and_category(self):
        """Test filtering by priority AND category"""
        tasks = [
            Task(
                id="task-001",
                title="High work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="High personal",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="personal",
            ),
            Task(
                id="task-003",
                title="Low work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
                category="work",
            ),
        ]

        # Filter: high AND work
        result = FilterService.filter_tasks(
            tasks, priority="high", category="work"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

        # Filter: high AND personal
        result = FilterService.filter_tasks(
            tasks, priority="high", category="personal"
        )
        assert len(result) == 1
        assert result[0].id == "task-002"

    def test_filter_all_three_criteria(self):
        """Test filtering by status, priority, and category"""
        tasks = [
            Task(
                id="task-001",
                title="Match all",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Different status",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-003",
                title="Different priority",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
                category="work",
            ),
            Task(
                id="task-004",
                title="Different category",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="personal",
            ),
        ]

        # Filter: pending AND high AND work
        result = FilterService.filter_tasks(
            tasks, status="pending", priority="high", category="work"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"

    def test_filter_with_none_values_includes_all(self):
        """Test that None filter values are ignored"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="completed",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]

        # Filter with None values should include all
        result = FilterService.filter_tasks(tasks, status=None, priority=None)
        assert len(result) == 2


class TestConvenientFilterMethods:
    """Test convenient filter method shortcuts"""

    def test_filter_pending_high_priority(self):
        """Test convenient method for pending high priority tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Pending high",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Completed high",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Pending low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]

        result = FilterService.filter_pending_high_priority(tasks)
        assert len(result) == 1
        assert result[0].id == "task-001"

    def test_filter_pending_by_category(self):
        """Test convenient method for pending tasks in category"""
        tasks = [
            Task(
                id="task-001",
                title="Pending work",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Completed work",
                status="completed",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-003",
                title="Pending personal",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        result = FilterService.filter_pending_by_category(tasks, "work")
        assert len(result) == 1
        assert result[0].id == "task-001"

    def test_filter_overdue_pending(self):
        """Test convenient method for overdue pending tasks"""
        past_date = date.today() - timedelta(days=1)
        future_date = date.today() + timedelta(days=1)

        tasks = [
            Task(
                id="task-001",
                title="Overdue pending",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=past_date,
            ),
            Task(
                id="task-002",
                title="Overdue completed",
                status="completed",
                created_timestamp=datetime.now(),
                due_date=past_date,
            ),
            Task(
                id="task-003",
                title="Not overdue pending",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=future_date,
            ),
        ]

        result = FilterService.filter_overdue_pending(tasks)
        assert len(result) == 1
        assert result[0].id == "task-001"


class TestFilterOptions:
    """Test getting available filter options"""

    def test_get_filter_options(self):
        """Test getting available filter options from tasks"""
        past_date = date.today() - timedelta(days=1)

        tasks = [
            Task(
                id="task-001",
                title="Work",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Personal",
                status="completed",
                created_timestamp=datetime.now(),
                priority="low",
                category="personal",
                due_date=past_date,
            ),
            Task(
                id="task-003",
                title="Recurring",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
                recurrence="daily",
            ),
        ]

        options = FilterService.get_filter_options(tasks)

        assert set(options["statuses"]) == {"pending", "completed"}
        assert set(options["priorities"]) == {"high", "medium", "low"}
        assert set(options["categories"]) == {"work", "personal"}
        assert options["has_overdue_tasks"] is True
        assert options["has_tasks_with_due_date"] is True
        assert options["has_recurring_tasks"] is True

    def test_get_filter_options_empty_list(self):
        """Test getting filter options from empty list"""
        options = FilterService.get_filter_options([])

        assert options["statuses"] == []
        assert options["priorities"] == []
        assert options["categories"] == []
        assert options["has_overdue_tasks"] is False


class TestCountByFilter:
    """Test counting tasks grouped by filter field"""

    def test_count_by_status(self):
        """Test counting tasks by status"""
        tasks = [
            Task(
                id="task-001",
                title="Pending 1",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Pending 2",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Completed",
                status="completed",
                created_timestamp=datetime.now(),
            ),
        ]

        counts = FilterService.count_by_filter(tasks, "status")
        assert counts["pending"] == 2
        assert counts["completed"] == 1

    def test_count_by_priority(self):
        """Test counting tasks by priority"""
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
                title="High 2",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]

        counts = FilterService.count_by_filter(tasks, "priority")
        assert counts["high"] == 2
        assert counts["low"] == 1

    def test_count_by_category(self):
        """Test counting tasks by category"""
        tasks = [
            Task(
                id="task-001",
                title="Work 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Work 2",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-003",
                title="No category",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        counts = FilterService.count_by_filter(tasks, "category")
        assert counts["work"] == 2
        assert counts["uncategorized"] == 1


class TestFilterAndCount:
    """Test filtering and counting in one operation"""

    def test_filter_and_count_status(self):
        """Test filtering and counting by status"""
        tasks = [
            Task(
                id="task-001",
                title="Work pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Work completed",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-003",
                title="Personal pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
                category="personal",
            ),
        ]

        # Count by status when filtering by category=work
        counts = FilterService.filter_and_count(
            tasks, group_by="status", category="work"
        )

        assert counts["pending"] == 1
        assert counts["completed"] == 1

    def test_filter_and_count_multiple_filters(self):
        """Test filtering and counting with multiple filters"""
        tasks = [
            Task(
                id="task-001",
                title="Work high pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
                category="work",
            ),
            Task(
                id="task-002",
                title="Work low pending",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
                category="work",
            ),
            Task(
                id="task-003",
                title="Personal high completed",
                status="completed",
                created_timestamp=datetime.now(),
                priority="high",
                category="personal",
            ),
        ]

        # Count by priority when status=pending and category=work
        counts = FilterService.filter_and_count(
            tasks,
            group_by="priority",
            status="pending",
            category="work"
        )

        assert counts["high"] == 1
        assert counts["low"] == 1
        assert "medium" not in counts


class TestComplexFilterScenarios:
    """Test complex filtering scenarios"""

    def test_filter_no_results(self):
        """Test filtering that returns no results"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
        ]

        # Filter for status completed AND priority high (no matches)
        result = FilterService.filter_tasks(
            tasks, status="completed", priority="high"
        )
        assert len(result) == 0

    def test_filter_with_overdue_and_due_date(self):
        """Test filtering with overdue and has_due_date filters"""
        past_date = date.today() - timedelta(days=1)
        future_date = date.today() + timedelta(days=1)

        tasks = [
            Task(
                id="task-001",
                title="Overdue",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=past_date,
            ),
            Task(
                id="task-002",
                title="Future",
                status="pending",
                created_timestamp=datetime.now(),
                due_date=future_date,
            ),
            Task(
                id="task-003",
                title="No due date",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        # Filter: has_due_date=True
        result = FilterService.filter_tasks(tasks, has_due_date=True)
        assert len(result) == 2

        # Filter: is_overdue=True
        result = FilterService.filter_tasks(tasks, is_overdue=True)
        assert len(result) == 1
        assert result[0].id == "task-001"

    def test_filter_with_recurring(self):
        """Test filtering recurring tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Daily",
                status="pending",
                created_timestamp=datetime.now(),
                recurrence="daily",
            ),
            Task(
                id="task-002",
                title="No recurrence",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Weekly",
                status="completed",
                created_timestamp=datetime.now(),
                recurrence="weekly",
            ),
        ]

        # Filter: is_recurring=True
        result = FilterService.filter_tasks(tasks, is_recurring=True)
        assert len(result) == 2

        # Filter: is_recurring=True AND status=pending
        result = FilterService.filter_tasks(
            tasks, is_recurring=True, status="pending"
        )
        assert len(result) == 1
        assert result[0].id == "task-001"
