"""Unit tests for Task model"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.models.enums import Priority, Status, Recurrence


class TestTaskCreation:
    """Test Task creation and initialization"""

    def test_create_minimal_task(self):
        """Test creating task with only required fields"""
        task = Task(
            id="task-001",
            title="Buy groceries",
            status="pending",
            created_timestamp=datetime.now()
        )
        assert task.id == "task-001"
        assert task.title == "Buy groceries"
        assert task.status == "pending"
        assert task.priority == "medium"  # default
        assert task.category is None
        assert task.due_date is None
        assert task.recurrence is None

    def test_create_task_with_all_fields(self):
        """Test creating task with all fields"""
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        task = Task(
            id="task-002",
            title="Complete project",
            status="pending",
            created_timestamp=now,
            priority="high",
            category="work",
            due_date=tomorrow,
            recurrence="weekly"
        )
        assert task.priority == "high"
        assert task.category == "work"
        assert task.due_date == tomorrow
        assert task.recurrence == "weekly"

    def test_task_defaults(self):
        """Test task field defaults"""
        task = Task(
            id="task-003",
            title="Task",
            status="pending",
            created_timestamp=datetime.now()
        )
        assert task.priority == "medium"
        assert task.completed_timestamp is None
        assert task.category is None
        assert task.due_date is None
        assert task.recurrence is None
        assert task.parent_recurrence_id is None


class TestTaskValidation:
    """Test Task field validation"""

    def test_invalid_priority(self):
        """Test invalid priority raises error"""
        with pytest.raises(ValueError):
            Task(
                id="task-004",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                priority="urgent"  # invalid
            )

    def test_invalid_status(self):
        """Test invalid status raises error"""
        with pytest.raises(ValueError):
            Task(
                id="task-005",
                title="Task",
                status="in_progress",  # invalid
                created_timestamp=datetime.now()
            )

    def test_invalid_recurrence(self):
        """Test invalid recurrence raises error"""
        with pytest.raises(ValueError):
            Task(
                id="task-006",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                recurrence="biweekly"  # invalid
            )

    def test_category_too_long(self):
        """Test category exceeding 50 characters raises error"""
        long_category = "a" * 51
        with pytest.raises(ValueError):
            Task(
                id="task-007",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category=long_category
            )

    def test_title_too_short(self):
        """Test empty title raises error"""
        with pytest.raises(ValueError):
            Task(
                id="task-008",
                title="",
                status="pending",
                created_timestamp=datetime.now()
            )

    def test_title_too_long(self):
        """Test title exceeding 255 characters raises error"""
        long_title = "a" * 256
        with pytest.raises(ValueError):
            Task(
                id="task-009",
                title=long_title,
                status="pending",
                created_timestamp=datetime.now()
            )


class TestTaskProperties:
    """Test Task computed properties"""

    def test_is_overdue_past_date(self):
        """Test task is marked overdue for past due date"""
        past_date = date.today() - timedelta(days=1)
        task = Task(
            id="task-010",
            title="Overdue task",
            status="pending",
            created_timestamp=datetime.now(),
            due_date=past_date
        )
        assert task.is_overdue is True

    def test_is_overdue_future_date(self):
        """Test task not marked overdue for future due date"""
        future_date = date.today() + timedelta(days=1)
        task = Task(
            id="task-011",
            title="Future task",
            status="pending",
            created_timestamp=datetime.now(),
            due_date=future_date
        )
        assert task.is_overdue is False

    def test_is_overdue_no_due_date(self):
        """Test task without due date is not overdue"""
        task = Task(
            id="task-012",
            title="No due date",
            status="pending",
            created_timestamp=datetime.now()
        )
        assert task.is_overdue is False

    def test_next_recurrence_daily(self):
        """Test next recurrence date for daily pattern"""
        today = date.today()
        task = Task(
            id="task-013",
            title="Daily task",
            status="pending",
            created_timestamp=datetime.now(),
            due_date=today,
            recurrence="daily"
        )
        next_date = task.next_recurrence_date
        assert next_date == today + timedelta(days=1)

    def test_next_recurrence_weekly(self):
        """Test next recurrence date for weekly pattern"""
        today = date.today()
        task = Task(
            id="task-014",
            title="Weekly task",
            status="pending",
            created_timestamp=datetime.now(),
            due_date=today,
            recurrence="weekly"
        )
        next_date = task.next_recurrence_date
        assert next_date == today + timedelta(days=7)

    def test_next_recurrence_monthly(self):
        """Test next recurrence date for monthly pattern"""
        today = date.today()
        task = Task(
            id="task-015",
            title="Monthly task",
            status="pending",
            created_timestamp=datetime.now(),
            due_date=today,
            recurrence="monthly"
        )
        next_date = task.next_recurrence_date
        # Verify it's approximately 1 month later
        assert next_date > today
        assert (next_date - today).days >= 28

    def test_next_recurrence_none(self):
        """Test task without recurrence returns None"""
        task = Task(
            id="task-016",
            title="No recurrence",
            status="pending",
            created_timestamp=datetime.now()
        )
        assert task.next_recurrence_date is None


class TestTaskSerialization:
    """Test Task serialization and deserialization"""

    def test_to_dict(self):
        """Test converting task to dictionary"""
        now = datetime.now()
        tomorrow = date.today() + timedelta(days=1)
        task = Task(
            id="task-017",
            title="Serialized task",
            status="pending",
            created_timestamp=now,
            priority="high",
            category="work",
            due_date=tomorrow,
            recurrence="daily"
        )
        task_dict = task.to_dict()
        assert task_dict["id"] == "task-017"
        assert task_dict["title"] == "Serialized task"
        assert task_dict["status"] == "pending"
        assert task_dict["priority"] == "high"
        assert task_dict["category"] == "work"
        assert task_dict["recurrence"] == "daily"

    def test_from_dict(self):
        """Test creating task from dictionary"""
        task_dict = {
            "id": "task-018",
            "title": "From dict",
            "status": "pending",
            "created_timestamp": datetime.now().isoformat(),
            "priority": "medium",
            "category": "personal",
            "due_date": date.today().isoformat()
        }
        task = Task.from_dict(task_dict)
        assert task.id == "task-018"
        assert task.title == "From dict"
        assert task.category == "personal"

    def test_from_dict_with_defaults(self):
        """Test from_dict with missing optional fields"""
        task_dict = {
            "id": "task-019",
            "title": "Minimal",
            "status": "pending",
            "created_timestamp": datetime.now().isoformat()
        }
        task = Task.from_dict(task_dict)
        assert task.priority == "medium"  # default
        assert task.category is None
        assert task.due_date is None


class TestTaskCompletion:
    """Test task completion functionality"""

    def test_mark_complete(self):
        """Test marking task as completed"""
        task = Task(
            id="task-020",
            title="Complete me",
            status="pending",
            created_timestamp=datetime.now()
        )
        assert task.status == "pending"
        assert task.completed_timestamp is None

        # Mark complete
        task.status = "completed"
        assert task.status == "completed"
        assert task.completed_timestamp is not None
