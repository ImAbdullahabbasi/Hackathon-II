"""Unit tests for in-memory task storage"""

import pytest
from datetime import datetime
from src.models.task import Task
from src.storage import TaskStorage


class TestStorageCreate:
    """Test creating tasks in storage"""

    def test_create_task(self):
        """Test creating a task assigns ID and stores it"""
        storage = TaskStorage()
        next_id = storage.get_next_task_id()
        task = Task(
            id=next_id,
            title="New task",
            status="pending",
            created_timestamp=datetime.now()
        )
        created_task = storage.create(task)
        assert created_task.id == "task-001"
        assert created_task.title == "New task"

    def test_create_multiple_tasks_increments_id(self):
        """Test multiple creates increment task ID"""
        storage = TaskStorage()
        task1 = storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        task2 = storage.create(Task(
            id=storage.get_next_task_id(), title="Task 2", status="pending", created_timestamp=datetime.now()
        ))
        assert task1.id == "task-001"
        assert task2.id == "task-002"

    def test_create_doesnt_reuse_deleted_ids(self):
        """Test that deleted task IDs are not reused"""
        storage = TaskStorage()
        task1 = storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        task2 = storage.create(Task(
            id=storage.get_next_task_id(), title="Task 2", status="pending", created_timestamp=datetime.now()
        ))
        storage.delete("task-001")
        task3 = storage.create(Task(
            id=storage.get_next_task_id(), title="Task 3", status="pending", created_timestamp=datetime.now()
        ))
        assert task3.id == "task-003"


class TestStorageRead:
    """Test reading tasks from storage"""

    def test_read_existing_task(self):
        """Test reading a task that exists"""
        storage = TaskStorage()
        created = storage.create(Task(
            id=storage.get_next_task_id(), title="Test task", status="pending", created_timestamp=datetime.now()
        ))
        read = storage.read("task-001")
        assert read is not None
        assert read.id == created.id
        assert read.title == created.title

    def test_read_nonexistent_task(self):
        """Test reading a task that doesn't exist"""
        storage = TaskStorage()
        result = storage.read("task-999")
        assert result is None

    def test_read_all(self):
        """Test reading all tasks"""
        storage = TaskStorage()
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 2", status="pending", created_timestamp=datetime.now()
        ))
        all_tasks = storage.read_all()
        assert len(all_tasks) == 2
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"

    def test_read_all_empty(self):
        """Test read_all on empty storage"""
        storage = TaskStorage()
        all_tasks = storage.read_all()
        assert len(all_tasks) == 0


class TestStorageUpdate:
    """Test updating tasks in storage"""

    def test_update_task_fields(self):
        """Test updating task fields"""
        storage = TaskStorage()
        task = storage.create(Task(
            id=storage.get_next_task_id(), title="Original", status="pending", created_timestamp=datetime.now()
        ))
        updated = storage.update("task-001", status="completed", priority="high")
        assert updated.title == "Original"  # title is immutable
        assert updated.priority == "high"
        assert updated.status == "completed"

    def test_update_nonexistent_task_raises_error(self):
        """Test updating nonexistent task raises error"""
        storage = TaskStorage()
        with pytest.raises(ValueError):
            storage.update("task-999", status="completed")

    def test_update_preserves_immutable_fields(self):
        """Test that immutable fields cannot be updated"""
        storage = TaskStorage()
        original_created = datetime.now()
        task = storage.create(Task(
            id=storage.get_next_task_id(), title="Task", status="pending", created_timestamp=original_created
        ))
        # Attempt to update immutable field
        updated = storage.update("task-001", created_timestamp=datetime.now())
        assert updated.created_timestamp == original_created


class TestStorageDelete:
    """Test deleting tasks from storage"""

    def test_delete_existing_task(self):
        """Test deleting a task that exists"""
        storage = TaskStorage()
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task to delete", status="pending", created_timestamp=datetime.now()
        ))
        result = storage.delete("task-001")
        assert result is True
        assert storage.read("task-001") is None

    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist"""
        storage = TaskStorage()
        result = storage.delete("task-999")
        assert result is False

    def test_delete_removes_from_read_all(self):
        """Test deleted task doesn't appear in read_all"""
        storage = TaskStorage()
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 2", status="pending", created_timestamp=datetime.now()
        ))
        storage.delete("task-001")
        all_tasks = storage.read_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == "task-002"


class TestStorageClear:
    """Test clearing storage"""

    def test_clear_removes_all_tasks(self):
        """Test clear removes all tasks"""
        storage = TaskStorage()
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 2", status="pending", created_timestamp=datetime.now()
        ))
        storage.clear()
        assert len(storage.read_all()) == 0

    def test_clear_resets_id_counter(self):
        """Test clear resets task ID counter"""
        storage = TaskStorage()
        storage.create(Task(
            id=storage.get_next_task_id(), title="Task 1", status="pending", created_timestamp=datetime.now()
        ))
        storage.clear()
        new_task = storage.create(Task(
            id=storage.get_next_task_id(), title="New task", status="pending", created_timestamp=datetime.now()
        ))
        assert new_task.id == "task-001"


class TestStorageIntegration:
    """Test storage operations together"""

    def test_create_read_update_delete_cycle(self):
        """Test full CRUD cycle"""
        storage = TaskStorage()

        # Create
        created = storage.create(Task(
            id=storage.get_next_task_id(), title="CRUD test", status="pending", created_timestamp=datetime.now()
        ))
        assert created.id == "task-001"

        # Read
        read = storage.read("task-001")
        assert read.title == "CRUD test"

        # Update
        updated = storage.update("task-001", status="completed", priority="high")
        assert updated.title == "CRUD test"  # immutable
        assert updated.priority == "high"
        assert updated.status == "completed"

        # Verify update
        verified = storage.read("task-001")
        assert verified.status == "completed"

        # Delete
        deleted = storage.delete("task-001")
        assert deleted is True
        assert storage.read("task-001") is None

    def test_storage_roundtrip_with_modifications(self):
        """Test complete storage workflow with modifications"""
        storage = TaskStorage()

        # Create a task
        task1 = storage.create(Task(
            id=storage.get_next_task_id(), title="Original task", status="pending", created_timestamp=datetime.now()
        ))
        assert task1.id == "task-001"

        # Verify we can read it back
        retrieved = storage.read("task-001")
        assert retrieved.title == "Original task"

        # Modify it
        storage.update("task-001", status="completed", priority="high")
        modified = storage.read("task-001")
        assert modified.status == "completed"
        assert modified.priority == "high"
