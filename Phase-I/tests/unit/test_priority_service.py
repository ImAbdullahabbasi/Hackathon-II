"""Unit tests for PriorityService"""

import pytest
from datetime import datetime, date
from src.models.task import Task
from src.services.priority_service import PriorityService


class TestPriorityServiceValidation:
    """Test priority validation in service"""

    def test_validate_priority_valid(self):
        """Test validating valid priorities"""
        assert PriorityService.validate_priority("high") is True
        assert PriorityService.validate_priority("medium") is True
        assert PriorityService.validate_priority("low") is True

    def test_validate_priority_invalid(self):
        """Test validating invalid priority"""
        with pytest.raises(ValueError):
            PriorityService.validate_priority("urgent")


class TestPriorityServiceFilter:
    """Test filtering tasks by priority"""

    def test_filter_by_priority_high(self):
        """Test filtering tasks with high priority"""
        tasks = [
            Task(
                id="task-001",
                title="High priority task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-002",
                title="Medium priority task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
            Task(
                id="task-003",
                title="Another high priority",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
        ]
        result = PriorityService.filter_by_priority(tasks, "high")
        assert len(result) == 2
        assert all(task.priority == "high" for task in result)

    def test_filter_by_priority_medium(self):
        """Test filtering tasks with medium priority"""
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
                title="Medium 1",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
            Task(
                id="task-003",
                title="Medium 2",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
            Task(
                id="task-004",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]
        result = PriorityService.filter_by_priority(tasks, "medium")
        assert len(result) == 2
        assert all(task.priority == "medium" for task in result)

    def test_filter_by_priority_empty_result(self):
        """Test filtering when no tasks match priority"""
        tasks = [
            Task(
                id="task-001",
                title="Low task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]
        result = PriorityService.filter_by_priority(tasks, "high")
        assert len(result) == 0

    def test_filter_by_priority_invalid_raises_error(self):
        """Test filtering with invalid priority raises error"""
        tasks = []
        with pytest.raises(ValueError):
            PriorityService.filter_by_priority(tasks, "urgent")


class TestPriorityServiceSort:
    """Test sorting tasks by priority"""

    def test_sort_by_priority_descending(self):
        """Test sorting tasks by priority descending (high to low)"""
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
        result = PriorityService.sort_by_priority(tasks, descending=True)
        assert result[0].priority == "high"
        assert result[1].priority == "medium"
        assert result[2].priority == "low"

    def test_sort_by_priority_ascending(self):
        """Test sorting tasks by priority ascending (low to high)"""
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
        result = PriorityService.sort_by_priority(tasks, descending=False)
        assert result[0].priority == "low"
        assert result[1].priority == "medium"
        assert result[2].priority == "high"

    def test_sort_by_priority_default_descending(self):
        """Test default sort order is descending"""
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
        result = PriorityService.sort_by_priority(tasks)
        assert result[0].priority == "high"
        assert result[1].priority == "low"

    def test_sort_by_priority_preserves_order_within_priority(self):
        """Test that tasks with same priority maintain original order"""
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
        result = PriorityService.sort_by_priority(tasks)
        assert result[0].id == "task-001"
        assert result[1].id == "task-002"


class TestPriorityServiceSummary:
    """Test priority summary generation"""

    def test_get_priority_summary_mixed(self):
        """Test summary with mixed priorities"""
        tasks = [
            Task(
                id="task-001",
                title="High 1",
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
                title="Medium",
                status="pending",
                created_timestamp=datetime.now(),
                priority="medium",
            ),
            Task(
                id="task-004",
                title="Low",
                status="pending",
                created_timestamp=datetime.now(),
                priority="low",
            ),
        ]
        result = PriorityService.get_priority_summary(tasks)
        assert result["high"] == 2
        assert result["medium"] == 1
        assert result["low"] == 1

    def test_get_priority_summary_empty_list(self):
        """Test summary with empty task list"""
        result = PriorityService.get_priority_summary([])
        assert result == {"high": 0, "medium": 0, "low": 0}

    def test_get_priority_summary_all_same_priority(self):
        """Test summary with all tasks same priority"""
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
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
            Task(
                id="task-003",
                title="Task 3",
                status="pending",
                created_timestamp=datetime.now(),
                priority="high",
            ),
        ]
        result = PriorityService.get_priority_summary(tasks)
        assert result == {"high": 3, "medium": 0, "low": 0}


class TestPriorityServiceSetPriority:
    """Test setting task priority"""

    def test_set_priority_valid(self):
        """Test setting valid priority"""
        task = Task(
            id="task-001",
            title="Test task",
            status="pending",
            created_timestamp=datetime.now(),
            priority="medium",
        )
        result = PriorityService.set_priority(task, "high")
        assert result.priority == "high"

    def test_set_priority_invalid(self):
        """Test setting invalid priority raises error"""
        task = Task(
            id="task-001",
            title="Test task",
            status="pending",
            created_timestamp=datetime.now(),
        )
        with pytest.raises(ValueError):
            PriorityService.set_priority(task, "urgent")

    def test_set_priority_preserves_other_fields(self):
        """Test that setting priority doesn't affect other fields"""
        now = datetime.now()
        task = Task(
            id="task-001",
            title="Test task",
            status="pending",
            created_timestamp=now,
            priority="low",
            category="work",
        )
        result = PriorityService.set_priority(task, "high")
        assert result.priority == "high"
        assert result.title == "Test task"
        assert result.category == "work"
        assert result.created_timestamp == now
