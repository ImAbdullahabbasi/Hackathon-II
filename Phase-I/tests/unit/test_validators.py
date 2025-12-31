"""Unit tests for field validators"""

import pytest
from datetime import date
from src.models.validators import (
    validate_priority,
    validate_category,
    validate_due_date,
    validate_recurrence,
    validate_task_title,
)


class TestPriorityValidation:
    """Test priority field validation"""

    def test_valid_priorities(self):
        """Test all valid priority values"""
        assert validate_priority("high") is True
        assert validate_priority("medium") is True
        assert validate_priority("low") is True

    def test_invalid_priority(self):
        """Test invalid priority values"""
        with pytest.raises(ValueError):
            validate_priority("urgent")

    def test_priority_case_sensitive(self):
        """Test priority validation is case-sensitive"""
        with pytest.raises(ValueError):
            validate_priority("HIGH")
        with pytest.raises(ValueError):
            validate_priority("Medium")


class TestCategoryValidation:
    """Test category field validation"""

    def test_valid_categories(self):
        """Test valid category values"""
        assert validate_category("work") is True
        assert validate_category("personal") is True
        assert validate_category("home-office") is True

    def test_category_none(self):
        """Test None category is valid (optional field)"""
        assert validate_category(None) is True

    def test_category_empty_string(self):
        """Test empty string category is valid (optional field)"""
        assert validate_category("") is True

    def test_category_max_length(self):
        """Test category at max length (50 chars)"""
        assert validate_category("a" * 50) is True

    def test_category_exceeds_max_length(self):
        """Test category exceeding max length"""
        with pytest.raises(ValueError):
            validate_category("a" * 51)

    def test_category_special_characters(self):
        """Test category with special characters"""
        assert validate_category("Work @2025 (important!)") is True


class TestDueDateValidation:
    """Test due date field validation"""

    def test_valid_date(self):
        """Test valid date format"""
        result = validate_due_date("2025-12-31")
        assert result == date(2025, 12, 31)

    def test_date_none(self):
        """Test None date is valid (optional field)"""
        assert validate_due_date(None) is None

    def test_date_empty_string(self):
        """Test empty string date is valid (optional field)"""
        assert validate_due_date("") is None

    def test_invalid_date_format(self):
        """Test invalid date format"""
        with pytest.raises(ValueError):
            validate_due_date("2025/12/31")
        with pytest.raises(ValueError):
            validate_due_date("12-31-2025")

    def test_invalid_month(self):
        """Test invalid month"""
        with pytest.raises(ValueError):
            validate_due_date("2025-13-01")

    def test_invalid_day(self):
        """Test invalid day"""
        with pytest.raises(ValueError):
            validate_due_date("2025-12-32")

    def test_february_non_leap_year(self):
        """Test February 29 in non-leap year"""
        with pytest.raises(ValueError):
            validate_due_date("2025-02-29")

    def test_february_leap_year(self):
        """Test February 29 in leap year"""
        result = validate_due_date("2024-02-29")
        assert result == date(2024, 2, 29)

    def test_past_date(self):
        """Test past date is allowed"""
        result = validate_due_date("2020-01-01")
        assert result == date(2020, 1, 1)

    def test_invalid_calendar_dates(self):
        """Test invalid calendar dates (line 73 - Feb 30, Apr 31, etc)"""
        # Note: strptime catches these errors before reaching the monthrange check
        # but the code path still exists for completeness
        invalid_dates = [
            "2025-02-30",  # February 30 doesn't exist
            "2025-04-31",  # April has 30 days
            "2025-06-31",  # June has 30 days
            "2025-09-31",  # September has 30 days
            "2025-11-31",  # November has 30 days
        ]
        for invalid_date in invalid_dates:
            with pytest.raises(ValueError):
                validate_due_date(invalid_date)


class TestRecurrenceValidation:
    """Test recurrence field validation"""

    def test_valid_recurrences(self):
        """Test all valid recurrence values"""
        assert validate_recurrence("daily") is True
        assert validate_recurrence("weekly") is True
        assert validate_recurrence("monthly") is True

    def test_recurrence_none(self):
        """Test None recurrence is valid (optional field)"""
        assert validate_recurrence(None) is True

    def test_recurrence_empty_string(self):
        """Test empty string recurrence is valid (optional field)"""
        assert validate_recurrence("") is True

    def test_invalid_recurrence(self):
        """Test invalid recurrence values"""
        with pytest.raises(ValueError):
            validate_recurrence("biweekly")
        with pytest.raises(ValueError):
            validate_recurrence("yearly")

    def test_recurrence_case_sensitive(self):
        """Test recurrence validation is case-sensitive"""
        with pytest.raises(ValueError):
            validate_recurrence("DAILY")


class TestTaskTitleValidation:
    """Test task title field validation"""

    def test_valid_title(self):
        """Test valid task titles"""
        assert validate_task_title("Buy groceries") is True
        assert validate_task_title("Complete project") is True

    def test_title_min_length(self):
        """Test title at minimum length (1 char)"""
        assert validate_task_title("A") is True

    def test_title_max_length(self):
        """Test title at maximum length (255 chars)"""
        assert validate_task_title("a" * 255) is True

    def test_title_empty_string(self):
        """Test empty title is invalid"""
        with pytest.raises(ValueError):
            validate_task_title("")

    def test_title_whitespace_only(self):
        """Test whitespace-only title is invalid"""
        with pytest.raises(ValueError):
            validate_task_title("   ")
        with pytest.raises(ValueError):
            validate_task_title("\t\n")

    def test_title_exceeds_max_length(self):
        """Test title exceeding max length"""
        with pytest.raises(ValueError):
            validate_task_title("a" * 256)

    def test_title_special_characters(self):
        """Test title with special characters"""
        assert validate_task_title("Task with émojis 🎉") is True

    def test_title_with_quotes(self):
        """Test title with quotes"""
        assert validate_task_title('Complete "important" task') is True
