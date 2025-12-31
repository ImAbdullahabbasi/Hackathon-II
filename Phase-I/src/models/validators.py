"""Validation functions for Task entity fields"""

from datetime import datetime, date
from typing import Optional
import calendar


def validate_priority(priority: str) -> bool:
    """Validate priority is one of: high, medium, low.

    Args:
        priority: Priority string to validate

    Returns:
        True if valid

    Raises:
        ValueError: If priority is invalid
    """
    valid_priorities = {"high", "medium", "low"}
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority. Must be high, medium, or low (got '{priority}')")
    return True


def validate_category(category: Optional[str]) -> bool:
    """Validate category is optional string with max 50 characters.

    Args:
        category: Category string to validate (can be None or empty)

    Returns:
        True if valid

    Raises:
        ValueError: If category exceeds 50 characters
    """
    if category is None or category == "":
        return True

    if len(category) > 50:
        raise ValueError(f"Category must be 50 characters or less (got {len(category)} characters)")
    return True


def validate_due_date(due_date_str: Optional[str]) -> Optional[date]:
    """Validate due date format YYYY-MM-DD and that it's a valid calendar date.

    Args:
        due_date_str: Due date string in YYYY-MM-DD format (can be None)

    Returns:
        datetime.date object if valid, None if input is None

    Raises:
        ValueError: If date format is invalid or calendar date doesn't exist
    """
    if due_date_str is None or due_date_str == "":
        return None

    # Validate format
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError(f"Invalid date format. Use YYYY-MM-DD (got '{due_date_str}')")
        raise ValueError(f"Invalid date. {str(e)}")

    # Validate calendar date exists (catches Feb 30, Apr 31, etc.)
    year, month, day = due_date.year, due_date.month, due_date.day
    max_day = calendar.monthrange(year, month)[1]
    if day > max_day:
        raise ValueError(f"Invalid date. {month}/{day}/{year} does not exist")

    return due_date


def validate_recurrence(recurrence: Optional[str]) -> bool:
    """Validate recurrence is one of: daily, weekly, monthly (or None for no recurrence).

    Args:
        recurrence: Recurrence string to validate (can be None)

    Returns:
        True if valid

    Raises:
        ValueError: If recurrence is invalid
    """
    if recurrence is None or recurrence == "":
        return True

    valid_recurrences = {"daily", "weekly", "monthly"}
    if recurrence not in valid_recurrences:
        raise ValueError(f"Invalid recurrence. Must be daily, weekly, or monthly (got '{recurrence}')")
    return True


def validate_task_title(title: str) -> bool:
    """Validate task title is 1-255 characters and not whitespace-only.

    Args:
        title: Task title to validate

    Returns:
        True if valid

    Raises:
        ValueError: If title is invalid
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")

    # Check length
    if len(title) < 1 or len(title) > 255:
        raise ValueError(f"Title must be 1-255 characters (got {len(title)})")

    # Check not whitespace only
    if not title.strip():
        raise ValueError("Title cannot be whitespace only")

    return True
