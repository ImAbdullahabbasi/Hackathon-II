"""In-memory task storage for Phase 1 Todo application"""

from typing import Optional, List, Any
from src.models.task import Task


# Module-level storage
_tasks: List[Task] = []
_task_counter: int = 0


class TaskStorage:
    """In-memory storage for Task entities with CRUD operations"""

    def __init__(self):
        """Initialize storage (uses module-level lists)"""
        global _tasks, _task_counter
        _tasks = []
        _task_counter = 0

    def create(self, task: Task) -> Task:
        """Create new task, assign ID, and store.

        Args:
            task: Task entity to store (id can be empty, will be assigned)

        Returns:
            Task with assigned ID

        Raises:
            ValueError: If task validation fails
        """
        global _task_counter
        _task_counter += 1
        task_id = f"task-{_task_counter:03d}"

        # Create new task with assigned ID
        new_task = Task(
            id=task_id,
            title=task.title,
            status=task.status,
            created_timestamp=task.created_timestamp,
            completed_timestamp=task.completed_timestamp,
            priority=task.priority,
            category=task.category,
            due_date=task.due_date,
            recurrence=task.recurrence,
            parent_recurrence_id=task.parent_recurrence_id,
        )

        _tasks.append(new_task)
        return new_task

    def read(self, task_id: str) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        for task in _tasks:
            if task.id == task_id:
                return task
        return None

    def read_all(self) -> List[Task]:
        """Get all tasks in creation order.

        Returns:
            List of all tasks
        """
        return list(_tasks)

    def update(self, task_id: str, **updates: Any) -> Task:
        """Update task fields.

        Args:
            task_id: ID of task to update
            **updates: Fields to update (title, status, priority, category, etc.)

        Returns:
            Updated task

        Raises:
            ValueError: If task not found or update invalid
        """
        task = self.read(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        # Immutable fields that cannot be updated
        immutable_fields = {"id", "created_timestamp"}

        # Apply updates
        for field, value in updates.items():
            if field in immutable_fields:
                continue  # Skip immutable fields
            if hasattr(task, field):
                setattr(task, field, value)

        return task

    def delete(self, task_id: str) -> bool:
        """Delete task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task was deleted, False if not found
        """
        global _tasks
        for i, task in enumerate(_tasks):
            if task.id == task_id:
                _tasks.pop(i)
                return True
        return False

    def clear(self) -> None:
        """Clear all tasks and reset counter (for testing)"""
        global _tasks, _task_counter
        _tasks = []
        _task_counter = 0

    def get_next_task_id(self) -> str:
        """Get the next task ID that would be assigned.

        Returns:
            Next task ID in format "task-NNN"
        """
        return f"task-{_task_counter + 1:03d}"
