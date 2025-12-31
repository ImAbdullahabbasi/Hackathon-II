"""Acceptance tests for User Story 5: Sort Tasks

User Story: "As a user, I want to sort my tasks by various criteria
(priority, status, title, due date, etc.) so that I can organize my view
and focus on what matters most."

Acceptance Scenarios:
1. Sort tasks by priority level
2. Sort tasks by status (pending/completed)
3. Sort tasks by title alphabetically
4. Sort tasks by due date
5. Sort by multiple criteria
"""

import pytest
from datetime import datetime, date, timedelta
from src.services.task_service import TaskService
from src.services.sort_service import SortService
from src.models.task import Task


class TestUserStory5SortTasks:
    """Test User Story 5: Sort tasks by various criteria"""

    @pytest.fixture
    def service(self):
        """Create a fresh TaskService for each test"""
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_scenario_1_sort_by_priority(self, service):
        """Scenario 1: Sort tasks by priority level

        Given I have tasks with different priorities
        When I sort by priority high to low
        Then high priority tasks appear first
        """
        # Create tasks with mixed priorities
        service.create_task("Report", priority="low")
        service.create_task("Meeting", priority="high")
        service.create_task("Email", priority="medium")
        service.create_task("Urgent fix", priority="high")

        # Sort by priority
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_priority(all_tasks, descending=True)

        # Verify order: high, high, medium, low
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "high"
        assert sorted_tasks[2].priority == "medium"
        assert sorted_tasks[3].priority == "low"

    def test_scenario_2_sort_by_status(self, service):
        """Scenario 2: Sort tasks by status

        Given I have pending and completed tasks
        When I sort by status with pending first
        Then pending tasks appear before completed tasks
        """
        # Create mixed status tasks
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2", status="pending")
        task3 = service.create_task("Task 3")

        # Mark some as completed
        service.mark_complete(task1.id)
        service.mark_complete(task3.id)

        # Sort by status (pending first)
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_status(all_tasks, pending_first=True)

        # Verify: pending first, then completed
        assert sorted_tasks[0].status == "pending"
        assert sorted_tasks[1].status == "completed"
        assert sorted_tasks[2].status == "completed"

    def test_scenario_3_sort_by_title(self, service):
        """Scenario 3: Sort tasks by title alphabetically

        Given I have tasks with various titles
        When I sort by title alphabetically
        Then tasks appear in A-Z order
        """
        # Create tasks with unsorted titles
        service.create_task("Zebra task")
        service.create_task("Apple task")
        service.create_task("Mango task")
        service.create_task("Banana task")

        # Sort by title
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_title(all_tasks, reverse=False)

        # Verify alphabetical order
        assert sorted_tasks[0].title == "Apple task"
        assert sorted_tasks[1].title == "Banana task"
        assert sorted_tasks[2].title == "Mango task"
        assert sorted_tasks[3].title == "Zebra task"

    def test_scenario_4_sort_by_due_date(self, service):
        """Scenario 4: Sort tasks by due date

        Given I have tasks with different due dates
        When I sort by due date earliest first
        Then tasks appear in chronological order
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        yesterday = today - timedelta(days=1)

        # Create tasks with various due dates
        service.create_task("Next week task", due_date=next_week)
        service.create_task("Today task", due_date=today)
        service.create_task("Tomorrow task", due_date=tomorrow)
        service.create_task("Yesterday task", due_date=yesterday)

        # Sort by due date
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_due_date(all_tasks, ascending=True)

        # Verify chronological order
        assert sorted_tasks[0].due_date == yesterday
        assert sorted_tasks[1].due_date == today
        assert sorted_tasks[2].due_date == tomorrow
        assert sorted_tasks[3].due_date == next_week

    def test_scenario_5_multi_criteria_sort(self, service):
        """Scenario 5: Sort by multiple criteria

        Given I have tasks with various attributes
        When I sort by multiple criteria
        Then tasks are ordered by primary, then secondary criteria
        """
        # Create tasks with mixed attributes
        service.create_task(
            "High pending",
            priority="high",
            status="pending",
        )
        service.create_task(
            "High completed",
            priority="high",
            status="completed",
        )
        service.create_task(
            "Low pending",
            priority="low",
            status="pending",
        )

        # Mark one as completed
        all_tasks = service.get_all_tasks()
        service.mark_complete(all_tasks[1].id)

        # Multi-sort: priority first (high to low), then status (pending first)
        sorted_tasks = SortService.multi_sort(
            service.get_all_tasks(),
            primary_field="priority",
            secondary_field="status",
            ascending=False
        )

        # High priority tasks should come first
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "high"
        assert sorted_tasks[2].priority == "low"

    def test_scenario_extended_sort_with_categories(self, service):
        """Extended test: Sort by category

        Given I have categorized tasks
        When I sort by category
        Then tasks are grouped by category alphabetically
        """
        # Create categorized tasks
        service.create_task("Work report", category="work")
        service.create_task("Personal note", category="personal")
        service.create_task("Home repair", category="home")
        service.create_task("Work meeting", category="work")
        service.create_task("No category task")

        # Sort by category
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_category(all_tasks, reverse=False)

        # Categories should be alphabetically ordered, uncategorized last
        assert sorted_tasks[0].category == "home"
        assert sorted_tasks[1].category == "personal"
        assert sorted_tasks[2].category == "work"
        assert sorted_tasks[3].category == "work"
        assert sorted_tasks[4].category is None

    def test_scenario_extended_sort_with_recurrence(self, service):
        """Extended test: Sort by recurrence

        Given I have recurring and non-recurring tasks
        When I sort by recurrence
        Then recurring tasks appear first
        """
        # Create recurring and non-recurring tasks
        service.create_task("Daily standup", recurrence="daily")
        service.create_task("One-time task")
        service.create_task("Weekly review", recurrence="weekly")
        service.create_task("Another one-time")

        # Sort with recurring first
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_recurrence(all_tasks, recurring_first=True)

        # Recurring tasks should come first
        assert sorted_tasks[0].recurrence is not None
        assert sorted_tasks[1].recurrence is not None
        assert sorted_tasks[2].recurrence is None
        assert sorted_tasks[3].recurrence is None

    def test_scenario_sort_overdue_first(self, service):
        """Test convenient method: sort overdue first

        Given I have overdue and non-overdue tasks
        When I use the overdue first shortcut
        Then overdue tasks appear first
        """
        past_date = date.today() - timedelta(days=1)
        future_date = date.today() + timedelta(days=7)

        # Create tasks with different due dates
        service.create_task("Future task", due_date=future_date)
        service.create_task("Overdue task", due_date=past_date)
        service.create_task("Another future", due_date=future_date)

        # Sort overdue first
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_overdue_first(all_tasks)

        # Overdue should be first
        assert sorted_tasks[0].is_overdue is True
        assert sorted_tasks[1].is_overdue is False
        assert sorted_tasks[2].is_overdue is False

    def test_scenario_sort_high_priority_first(self, service):
        """Test convenient method: high priority first

        Given I have mixed priority tasks
        When I use the high priority first shortcut
        Then high priority tasks appear first
        """
        # Create mixed priority tasks
        service.create_task("Low", priority="low")
        service.create_task("High", priority="high")
        service.create_task("Medium", priority="medium")

        # Sort high priority first
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_high_priority_first(all_tasks)

        # High should be first
        assert sorted_tasks[0].priority == "high"

    def test_scenario_case_insensitive_title_sort(self, service):
        """Test that title sorting is case-insensitive

        Given I have tasks with various cases
        When I sort by title
        Then sorting ignores case
        """
        # Create tasks with mixed cases
        service.create_task("apple task")
        service.create_task("ZEBRA task")
        service.create_task("Banana task")

        # Sort by title
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_title(all_tasks)

        # Verify case-insensitive order
        assert "apple" in sorted_tasks[0].title.lower()
        assert "banana" in sorted_tasks[1].title.lower()
        assert "zebra" in sorted_tasks[2].title.lower()

    def test_scenario_sort_preserves_relative_order(self, service):
        """Test that sorting is stable

        Given I have tasks with same priority
        When I sort by priority
        Then tasks with same priority maintain original order
        """
        # Create tasks with same priority
        service.create_task("First high", priority="high")
        service.create_task("Second high", priority="high")
        service.create_task("Third high", priority="high")

        # Sort by priority
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_priority(all_tasks)

        # All should have high priority and maintain order
        assert all(t.priority == "high" for t in sorted_tasks)
        assert sorted_tasks[0].title == "First high"
        assert sorted_tasks[1].title == "Second high"
        assert sorted_tasks[2].title == "Third high"

    def test_scenario_sort_integration_with_service(self, service):
        """Test sorting integrated with TaskService

        Given I have tasks in the service
        When I retrieve all tasks and sort them
        Then sorting works with service data
        """
        # Create complex tasks
        today = date.today()
        tomorrow = today + timedelta(days=1)

        service.create_task(
            "Urgent work",
            priority="high",
            category="work",
            status="pending",
            due_date=tomorrow
        )
        service.create_task(
            "Low priority personal",
            priority="low",
            category="personal",
            status="completed"
        )
        service.create_task(
            "Medium priority home",
            priority="medium",
            category="home",
            due_date=today
        )

        # Get all and sort by priority
        all_tasks = service.get_all_tasks()
        sorted_by_priority = SortService.sort_by_priority(all_tasks, descending=True)

        # Verify sorting worked on service data
        assert sorted_by_priority[0].priority == "high"
        assert sorted_by_priority[1].priority == "medium"
        assert sorted_by_priority[2].priority == "low"

    def test_scenario_sort_handles_null_values(self, service):
        """Test sorting with null/missing values

        Given I have tasks without due dates or categories
        When I sort by those fields
        Then tasks without values are placed appropriately
        """
        # Create tasks with and without due dates
        service.create_task("No due date")
        service.create_task("Has due date", due_date=date.today())

        # Sort by due date
        all_tasks = service.get_all_tasks()
        sorted_tasks = SortService.sort_by_due_date(all_tasks, ascending=True)

        # Task with due date should come first
        assert sorted_tasks[0].due_date is not None
        assert sorted_tasks[1].due_date is None

    def test_scenario_sort_reverse_order(self, service):
        """Test reverse sorting

        Given I have tasks
        When I sort in reverse
        Then tasks appear in opposite order
        """
        # Create alphabetically ordered tasks
        service.create_task("Apple")
        service.create_task("Banana")
        service.create_task("Cherry")

        # Sort forward
        all_tasks = service.get_all_tasks()
        forward = SortService.sort_by_title(all_tasks, reverse=False)

        # Sort reverse
        reverse = SortService.sort_by_title(all_tasks, reverse=True)

        # Verify reverse order
        assert forward[0].title == reverse[2].title
        assert forward[1].title == reverse[1].title
        assert forward[2].title == reverse[0].title

    def test_scenario_sort_empty_and_single_task(self, service):
        """Test edge cases: empty list and single task

        Given I have an empty or single-task list
        When I sort
        Then sorting handles these gracefully
        """
        # Empty list
        sorted_empty = SortService.sort_by_priority([])
        assert len(sorted_empty) == 0

        # Single task
        service.create_task("Only task", priority="high")
        all_tasks = service.get_all_tasks()
        sorted_single = SortService.sort_by_priority(all_tasks)
        assert len(sorted_single) == 1
        assert sorted_single[0].title == "Only task"
