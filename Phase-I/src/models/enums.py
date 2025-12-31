"""Enumerations for the todo application.

This module contains enumeration classes used throughout the application
to represent different states and configurations for todos.
"""

from enum import Enum


class Priority(Enum):
    """Priority levels for todo items.

    Attributes:
        HIGH: High priority tasks that require immediate attention.
        MEDIUM: Medium priority tasks with standard importance.
        LOW: Low priority tasks that can be deferred.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __str__(self) -> str:
        """Return user-friendly string representation of priority level."""
        return self.value.capitalize()


class Status(Enum):
    """Status states for todo items.

    Attributes:
        PENDING: Task has not been completed yet.
        COMPLETED: Task has been successfully completed.
    """

    PENDING = "pending"
    COMPLETED = "completed"

    def __str__(self) -> str:
        """Return user-friendly string representation of status."""
        return self.value.capitalize()


class Recurrence(Enum):
    """Recurrence patterns for recurring todo items.

    Attributes:
        DAILY: Task repeats every day.
        WEEKLY: Task repeats every week.
        MONTHLY: Task repeats every month.
    """

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    def __str__(self) -> str:
        """Return user-friendly string representation of recurrence pattern."""
        return self.value.capitalize()
