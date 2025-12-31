"""Task entity for the todo application.

This module contains the Task class representing a single task in the todo system,
with support for priorities, categories, due dates, and recurring tasks.
"""

from datetime import datetime, date, timedelta
from typing import Optional
from src.models.enums import Priority, Status, Recurrence


class Task:
    """Represents a single task in the todo application.

    A Task encapsulates all information about a todo item, including its
    basic properties (id, title, status), timestamps, and advanced features
    (priority, category, due date, recurrence).

    Attributes:
        id: Unique task identifier in format "task-NNN"
        title: Task title (1-255 characters, immutable)
        status: Task completion status (pending or completed)
        created_timestamp: When task was created (immutable)
        completed_timestamp: When task was completed (None if pending)
        priority: Priority level (high, medium, low; defaults to medium)
        category: Optional category/tag (max 50 characters)
        due_date: Optional due date in YYYY-MM-DD format
        recurrence: Optional recurrence pattern (daily, weekly, monthly)
        parent_recurrence_id: ID of parent if this is auto-generated instance
    """

    def __init__(
        self,
        id: str,
        title: str,
        status: str = "pending",
        created_timestamp: Optional[datetime] = None,
        completed_timestamp: Optional[datetime] = None,
        priority: str = "medium",
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        recurrence: Optional[str] = None,
        parent_recurrence_id: Optional[str] = None,
    ) -> None:
        """Initialize a Task instance with validation.

        Args:
            id: Task identifier (format: task-NNN)
            title: Task title (required, 1-255 chars)
            status: Task status, defaults to "pending"
            created_timestamp: Creation timestamp, defaults to now if not provided
            completed_timestamp: Completion timestamp (None if pending)
            priority: Priority level (high, medium, low), defaults to "medium"
            category: Optional category string (max 50 chars)
            due_date: Optional due date
            recurrence: Optional recurrence pattern (daily, weekly, monthly)
            parent_recurrence_id: Optional parent task ID for recurrence

        Raises:
            ValueError: If title is empty/invalid or other validation fails
            TypeError: If arguments are wrong type
        """
        # Validate and set id
        self._validate_id(id)
        self.id: str = id

        # Validate and set title
        self._validate_title(title)
        self._title: str = title

        # Validate and set status
        self._validate_status(status)
        self._status: str = status

        # Set timestamps
        self.created_timestamp: datetime = (
            created_timestamp if created_timestamp is not None else datetime.now()
        )
        self.completed_timestamp: Optional[datetime] = completed_timestamp

        # Validate and set priority
        self._validate_priority(priority)
        self.priority: str = priority

        # Validate and set category
        self._validate_category(category)
        self.category: Optional[str] = category if category else None

        # Validate and set due_date
        self._validate_due_date(due_date)
        self.due_date: Optional[date] = due_date

        # Validate and set recurrence
        self._validate_recurrence(recurrence)
        self.recurrence: Optional[str] = recurrence

        # Set parent_recurrence_id
        self.parent_recurrence_id: Optional[str] = parent_recurrence_id

    @staticmethod
    def _validate_id(id_value: str) -> None:
        """Validate task ID format.

        Args:
            id_value: The ID to validate

        Raises:
            ValueError: If ID doesn't match format task-NNN
        """
        if not isinstance(id_value, str):
            raise TypeError("ID must be a string")
        if not id_value.startswith("task-"):
            raise ValueError("ID must start with 'task-'")
        parts = id_value.split("-")
        if len(parts) != 2 or not parts[1].isdigit():
            raise ValueError("ID format must be 'task-NNN' where NNN is a number")

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate task title.

        Args:
            title: The title to validate

        Raises:
            ValueError: If title is empty or exceeds length limits
            TypeError: If title is not a string
        """
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        trimmed = title.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty")
        if len(trimmed) > 255:
            raise ValueError("Title must be 255 characters or less")

    @staticmethod
    def _validate_status(status: str) -> None:
        """Validate task status.

        Args:
            status: The status to validate

        Raises:
            ValueError: If status is not pending or completed
        """
        if not isinstance(status, str):
            raise TypeError("Status must be a string")
        if status not in {"pending", "completed"}:
            raise ValueError("Status must be 'pending' or 'completed'")

    @staticmethod
    def _validate_priority(priority: str) -> None:
        """Validate task priority.

        Args:
            priority: The priority to validate

        Raises:
            ValueError: If priority is not high, medium, or low
        """
        if not isinstance(priority, str):
            raise TypeError("Priority must be a string")
        if priority not in {"high", "medium", "low"}:
            raise ValueError("Invalid priority. Must be 'high', 'medium', or 'low'.")

    @staticmethod
    def _validate_category(category: Optional[str]) -> None:
        """Validate task category.

        Args:
            category: The category to validate (can be None)

        Raises:
            ValueError: If category exceeds length limit
        """
        if category is None or category == "":
            return
        if not isinstance(category, str):
            raise TypeError("Category must be a string or None")
        if len(category) > 50:
            raise ValueError(
                f"Category must be 50 characters or less (received {len(category)} characters)."
            )

    @staticmethod
    def _validate_due_date(due_date: Optional[date]) -> None:
        """Validate task due date.

        Args:
            due_date: The due date to validate (can be None)

        Raises:
            ValueError: If date format or value is invalid
        """
        if due_date is None:
            return
        if not isinstance(due_date, date):
            raise TypeError("Due date must be a datetime.date or None")

    @staticmethod
    def _validate_recurrence(recurrence: Optional[str]) -> None:
        """Validate task recurrence pattern.

        Args:
            recurrence: The recurrence pattern to validate (can be None)

        Raises:
            ValueError: If recurrence is not daily, weekly, monthly, or None
        """
        if recurrence is None:
            return
        if not isinstance(recurrence, str):
            raise TypeError("Recurrence must be a string or None")
        if recurrence not in {"daily", "weekly", "monthly"}:
            raise ValueError(
                "Invalid recurrence. Must be 'daily', 'weekly', or 'monthly'."
            )

    @property
    def title(self) -> str:
        """Get task title (read-only, immutable)."""
        return self._title

    @property
    def status(self) -> str:
        """Get task status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set task status with validation.

        Args:
            value: The new status value

        Raises:
            ValueError: If status value is invalid
        """
        self._validate_status(value)
        self._status = value
        # Set completed_timestamp when task is marked complete
        if value == "completed" and self.completed_timestamp is None:
            self.completed_timestamp = datetime.now()

    @property
    def is_overdue(self) -> bool:
        """Determine if task is overdue.

        A task is overdue if it has a due date and that date is in the past
        (current date > due date, not >=).

        Returns:
            True if task is overdue, False otherwise
        """
        if self.due_date is None:
            return False
        return date.today() > self.due_date

    @property
    def next_recurrence_date(self) -> Optional[date]:
        """Calculate the next recurrence date for this task.

        Based on the recurrence pattern and due date, computes when the
        next instance should occur. Only valid for recurring tasks with a due date.

        Returns:
            The next recurrence date, or None if task is not recurring or has no due date

        Raises:
            ValueError: If recurrence pattern is invalid
        """
        if self.recurrence is None or self.due_date is None:
            return None

        if self.recurrence == "daily":
            return self.due_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            return self.due_date + timedelta(weeks=1)
        elif self.recurrence == "monthly":
            return self._add_months(self.due_date, 1)
        else:
            raise ValueError(f"Unknown recurrence pattern: {self.recurrence}")

    @staticmethod
    def _add_months(target_date: date, months: int) -> date:
        """Add months to a date, handling month-end edge cases.

        Handles edge cases like Jan 31 + 1 month = Feb 28/29.

        Args:
            target_date: The starting date
            months: Number of months to add

        Returns:
            The new date after adding months
        """
        month = target_date.month - 1 + months
        year = target_date.year + month // 12
        month = month % 12 + 1
        day = min(target_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date(year, month, day)

    def __repr__(self) -> str:
        """Return detailed string representation for debugging.

        Returns:
            String representation with all fields
        """
        return (
            f"Task(id={self.id!r}, title={self.title!r}, status={self.status!r}, "
            f"priority={self.priority!r}, category={self.category!r}, "
            f"due_date={self.due_date!r}, recurrence={self.recurrence!r}, "
            f"is_overdue={self.is_overdue})"
        )

    def __str__(self) -> str:
        """Return user-friendly string representation.

        Returns:
            Formatted string showing title, status, and overdue indicator
        """
        status_indicator = "✓" if self.status == "completed" else "○"
        overdue_indicator = " [OVERDUE]" if self.is_overdue else ""
        return f"{status_indicator} [{self.id}] {self.title}{overdue_indicator}"

    def to_dict(self) -> dict:
        """Serialize task to dictionary.

        Converts all fields to dictionary format suitable for storage or JSON serialization.
        Timestamps and dates are converted to ISO format strings.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_timestamp": self.created_timestamp.isoformat(),
            "completed_timestamp": (
                self.completed_timestamp.isoformat()
                if self.completed_timestamp
                else None
            ),
            "priority": self.priority,
            "category": self.category,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "recurrence": self.recurrence,
            "parent_recurrence_id": self.parent_recurrence_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary.

        Handles deserialization from stored format, including date/datetime
        string parsing. Supports backward compatibility with older tasks
        that may be missing new fields.

        Args:
            data: Dictionary containing task data

        Returns:
            New Task instance

        Raises:
            ValueError: If required fields are missing or invalid
            TypeError: If data types are incorrect
        """
        # Parse timestamps
        created_timestamp = None
        if "created_timestamp" in data and data["created_timestamp"]:
            if isinstance(data["created_timestamp"], str):
                created_timestamp = datetime.fromisoformat(data["created_timestamp"])
            else:
                created_timestamp = data["created_timestamp"]

        completed_timestamp = None
        if "completed_timestamp" in data and data["completed_timestamp"]:
            if isinstance(data["completed_timestamp"], str):
                completed_timestamp = datetime.fromisoformat(
                    data["completed_timestamp"]
                )
            else:
                completed_timestamp = data["completed_timestamp"]

        # Parse due_date
        due_date = None
        if "due_date" in data and data["due_date"]:
            if isinstance(data["due_date"], str):
                due_date = date.fromisoformat(data["due_date"])
            else:
                due_date = data["due_date"]

        # Extract fields with defaults for backward compatibility
        return cls(
            id=data["id"],
            title=data["title"],
            status=data.get("status", "pending"),
            created_timestamp=created_timestamp,
            completed_timestamp=completed_timestamp,
            priority=data.get("priority", "medium"),
            category=data.get("category"),
            due_date=due_date,
            recurrence=data.get("recurrence"),
            parent_recurrence_id=data.get("parent_recurrence_id"),
        )
