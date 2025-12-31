"""Unit tests for TaskService"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.storage import TaskStorage
from src.services.task_service import TaskService


class TestTaskServiceCreate:
    """Test creating tasks via TaskService"""

    def test_create_task_minimal(self):
        """Test creating task with minimal fields"""
        service = TaskService()
        task = service.create_task("Buy groceries")
        assert task.title == "Buy groceries"
        assert task.status == "pending"
        assert task.priority == "medium"
        assert task.id == "task-001"

    def test_create_task_with_all_fields(self):
        """Test creating task with all fields"""
        service = TaskService()
        tomorrow = date.today() + timedelta(days=1)
        task = service.create_task(
            title="Complete project",
            status="pending",
            priority="high",
            category="work",
            due_date=tomorrow,
            recurrence="weekly"
        )
        assert task.title == "Complete project"
        assert task.priority == "high"
        assert task.category == "work"
        assert task.due_date == tomorrow
        assert task.recurrence == "weekly"

    def test_create_multiple_tasks_increments_id(self):
        """Test that multiple creates increment task IDs"""
        service = TaskService()
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        assert task1.id == "task-001"
        assert task2.id == "task-002"


class TestTaskServiceRead:
    """Test reading tasks via TaskService"""

    def test_get_task_existing(self):
        """Test getting an existing task"""
        service = TaskService()
        created = service.create_task("Test task")
        retrieved = service.get_task("task-001")
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_task_nonexistent(self):
        """Test getting nonexistent task returns None"""
        service = TaskService()
        retrieved = service.get_task("task-999")
        assert retrieved is None

    def test_get_all_tasks(self):
        """Test getting all tasks"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 3
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"
        assert all_tasks[2].title == "Task 3"


class TestTaskServiceUpdate:
    """Test updating tasks via TaskService"""

    def test_update_task_fields(self):
        """Test updating task fields"""
        service = TaskService()
        service.create_task("Original title")
        updated = service.update_task("task-001", priority="high", status="completed")
        assert updated.title == "Original title"  # title is immutable
        assert updated.priority == "high"
        assert updated.status == "completed"

    def test_update_nonexistent_task_raises_error(self):
        """Test updating nonexistent task raises error"""
        service = TaskService()
        with pytest.raises(ValueError):
            service.update_task("task-999", title="Update")


class TestTaskServiceDelete:
    """Test deleting tasks via TaskService"""

    def test_delete_task(self):
        """Test deleting a task"""
        service = TaskService()
        service.create_task("Task to delete")
        result = service.delete_task("task-001")
        assert result is True
        assert service.get_task("task-001") is None

    def test_delete_nonexistent_task(self):
        """Test deleting nonexistent task returns False"""
        service = TaskService()
        result = service.delete_task("task-999")
        assert result is False


class TestTaskServiceFilterByStatus:
    """Test filtering tasks by status"""

    def test_filter_by_status_pending(self):
        """Test filtering pending tasks"""
        service = TaskService()
        service.create_task("Pending 1")
        service.create_task("Pending 2")
        service.create_task("Completed")
        service.mark_complete("task-003")

        pending = service.filter_by_status("pending")
        assert len(pending) == 2
        assert all(t.status == "pending" for t in pending)

    def test_filter_by_status_completed(self):
        """Test filtering completed tasks"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.mark_complete("task-001")

        completed = service.filter_by_status("completed")
        assert len(completed) == 1
        assert completed[0].status == "completed"


class TestTaskServiceFilterByPriority:
    """Test filtering tasks by priority"""

    def test_filter_by_priority_high(self):
        """Test filtering high priority tasks"""
        service = TaskService()
        service.create_task("Task 1", priority="high")
        service.create_task("Task 2", priority="medium")
        service.create_task("Task 3", priority="high")

        high_priority = service.filter_by_priority("high")
        assert len(high_priority) == 2
        assert all(t.priority == "high" for t in high_priority)

    def test_filter_by_priority_invalid_raises_error(self):
        """Test filtering with invalid priority raises error"""
        service = TaskService()
        with pytest.raises(ValueError):
            service.filter_by_priority("urgent")


class TestTaskServiceFilterByCategory:
    """Test filtering tasks by category"""

    def test_filter_by_category(self):
        """Test filtering tasks by category"""
        service = TaskService()
        service.create_task("Work task", category="work")
        service.create_task("Personal task", category="personal")
        service.create_task("Another work task", category="work")

        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 2
        assert all(t.category == "work" for t in work_tasks)

    def test_filter_by_category_none_found(self):
        """Test filtering by category with no matches"""
        service = TaskService()
        service.create_task("Task", category="work")

        personal = service.filter_by_category("personal")
        assert len(personal) == 0


class TestTaskServiceOverdueTasks:
    """Test getting overdue tasks"""

    def test_get_overdue_tasks(self):
        """Test getting overdue tasks"""
        service = TaskService()
        past_date = date.today() - timedelta(days=1)
        future_date = date.today() + timedelta(days=1)

        service.create_task("Overdue task", due_date=past_date)
        service.create_task("Future task", due_date=future_date)
        service.create_task("No due date")

        overdue = service.get_overdue_tasks()
        assert len(overdue) == 1
        assert overdue[0].title == "Overdue task"

    def test_get_overdue_tasks_excludes_completed(self):
        """Test that completed tasks are excluded from overdue"""
        service = TaskService()
        past_date = date.today() - timedelta(days=1)
        service.create_task("Overdue task", due_date=past_date)
        service.mark_complete("task-001")

        overdue = service.get_overdue_tasks()
        assert len(overdue) == 0


class TestTaskServiceUpcomingTasks:
    """Test getting upcoming tasks"""

    def test_get_upcoming_tasks(self):
        """Test getting upcoming tasks within 7 days"""
        service = TaskService()
        today = date.today()

        service.create_task("Overdue", due_date=today - timedelta(days=1))
        service.create_task("Today", due_date=today)
        service.create_task("Tomorrow", due_date=today + timedelta(days=1))
        service.create_task("In 3 days", due_date=today + timedelta(days=3))
        service.create_task("In 10 days", due_date=today + timedelta(days=10))
        service.create_task("No due date")

        upcoming = service.get_upcoming_tasks(days=7)
        assert len(upcoming) == 3  # Today, Tomorrow, In 3 days
        assert all(t.status == "pending" for t in upcoming)

    def test_get_upcoming_tasks_custom_days(self):
        """Test getting upcoming tasks with custom day range"""
        service = TaskService()
        today = date.today()

        service.create_task("In 1 day", due_date=today + timedelta(days=1))
        service.create_task("In 5 days", due_date=today + timedelta(days=5))

        upcoming = service.get_upcoming_tasks(days=3)
        assert len(upcoming) == 1  # Only 1 day
        assert upcoming[0].title == "In 1 day"


class TestTaskServiceCompletion:
    """Test marking tasks complete/pending"""

    def test_mark_complete(self):
        """Test marking task as completed"""
        service = TaskService()
        service.create_task("Task")
        completed = service.mark_complete("task-001")
        assert completed.status == "completed"
        assert completed.completed_timestamp is not None

    def test_mark_pending(self):
        """Test marking task as pending"""
        service = TaskService()
        service.create_task("Task")
        service.mark_complete("task-001")
        pending = service.mark_pending("task-001")
        assert pending.status == "pending"
        assert pending.completed_timestamp is None

    def test_mark_complete_nonexistent_raises_error(self):
        """Test marking nonexistent task complete raises error"""
        service = TaskService()
        with pytest.raises(ValueError):
            service.mark_complete("task-999")


class TestTaskServiceListAll:
    """Test listing all tasks with sorting"""

    def test_list_all_default_sort(self):
        """Test listing all tasks with default sort (created)"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")

        tasks = service.list_all_tasks()
        assert [t.title for t in tasks] == ["Task 1", "Task 2", "Task 3"]

    def test_list_all_sort_by_priority(self):
        """Test listing tasks sorted by priority"""
        service = TaskService()
        service.create_task("Low", priority="low")
        service.create_task("High", priority="high")
        service.create_task("Medium", priority="medium")

        tasks = service.list_all_tasks(sort_by="priority")
        assert [t.priority for t in tasks] == ["high", "medium", "low"]

    def test_list_all_sort_by_title(self):
        """Test listing tasks sorted by title"""
        service = TaskService()
        service.create_task("Zebra")
        service.create_task("Apple")
        service.create_task("Banana")

        tasks = service.list_all_tasks(sort_by="title")
        assert [t.title for t in tasks] == ["Apple", "Banana", "Zebra"]

    def test_list_all_sort_reverse(self):
        """Test listing tasks with reverse sort"""
        service = TaskService()
        service.create_task("High", priority="high")
        service.create_task("Low", priority="low")

        tasks = service.list_all_tasks(sort_by="priority", reverse=True)
        assert [t.priority for t in tasks] == ["low", "high"]


class TestTaskServiceStats:
    """Test task statistics"""

    def test_get_task_count(self):
        """Test getting task count"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")

        assert service.get_task_count() == 3

    def test_get_completion_stats(self):
        """Test getting completion statistics"""
        service = TaskService()
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")
        service.mark_complete("task-001")
        service.mark_complete("task-002")

        stats = service.get_completion_stats()
        assert stats["completed"] == 2
        assert stats["pending"] == 1
        assert stats["total"] == 3
        assert stats["completion_percentage"] == 66.67

    def test_get_completion_stats_empty(self):
        """Test completion stats with no tasks"""
        service = TaskService()

        stats = service.get_completion_stats()
        assert stats["completed"] == 0
        assert stats["pending"] == 0
        assert stats["total"] == 0
        assert stats["completion_percentage"] == 0


class TestTaskServiceIntegration:
    """Test TaskService with custom storage"""

    def test_custom_storage(self):
        """Test TaskService with custom storage instance"""
        storage = TaskStorage()
        service = TaskService(storage=storage)

        task = service.create_task("Test task")
        assert task.id == "task-001"

        # Verify it's in the provided storage
        assert storage.read("task-001") is not None

    def test_multiple_service_instances_share_storage(self):
        """Test multiple services with same storage share data"""
        storage = TaskStorage()
        service1 = TaskService(storage=storage)
        service2 = TaskService(storage=storage)

        task = service1.create_task("Task from service 1")
        retrieved = service2.get_task("task-001")
        assert retrieved is not None
        assert retrieved.title == "Task from service 1"
