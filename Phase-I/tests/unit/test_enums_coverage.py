"""Tests for enum string representations (coverage gap filling)"""

import pytest
from src.models.enums import Priority, Status, Recurrence


class TestEnumStringRepresentations:
    """Test __str__ methods for all enums"""

    def test_priority_high_str(self):
        """Test Priority.HIGH string representation"""
        assert str(Priority.HIGH) == "High"

    def test_priority_medium_str(self):
        """Test Priority.MEDIUM string representation"""
        assert str(Priority.MEDIUM) == "Medium"

    def test_priority_low_str(self):
        """Test Priority.LOW string representation"""
        assert str(Priority.LOW) == "Low"

    def test_status_pending_str(self):
        """Test Status.PENDING string representation"""
        assert str(Status.PENDING) == "Pending"

    def test_status_completed_str(self):
        """Test Status.COMPLETED string representation"""
        assert str(Status.COMPLETED) == "Completed"

    def test_recurrence_daily_str(self):
        """Test Recurrence.DAILY string representation"""
        assert str(Recurrence.DAILY) == "Daily"

    def test_recurrence_weekly_str(self):
        """Test Recurrence.WEEKLY string representation"""
        assert str(Recurrence.WEEKLY) == "Weekly"

    def test_recurrence_monthly_str(self):
        """Test Recurrence.MONTHLY string representation"""
        assert str(Recurrence.MONTHLY) == "Monthly"
