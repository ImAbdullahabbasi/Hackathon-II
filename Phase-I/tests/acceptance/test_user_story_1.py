"""Acceptance tests for User Story 1: Organize Tasks by Priority

User Story: "As a user, I want to organize and view my tasks by priority level
(high, medium, low) so that I can focus on what's most important."

Acceptance Scenarios:
1. Create tasks with different priorities
2. Filter tasks by priority level
3. Sort tasks by priority level
4. View priority summary statistics
5. Update task priority
"""

import pytest
from datetime import datetime, date, timedelta
from src.services.task_service import TaskService
from src.models.task import Task


class TestUserStory1PriorityManagement:
    """Test User Story 1: Organize tasks by priority"""

    @pytest.fixture
    def service(self):
        """Create a fresh TaskService for each test"""
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_scenario_1_create_tasks_with_different_priorities(self, service):
        """Scenario 1: Create tasks with different priorities

        Given I have no tasks
        When I create tasks with high, medium, and low priorities
        Then all tasks should be created with correct priority levels
        """
        # Create tasks with different priorities
        high_task = service.create_task("Urgent report", priority="high")
        medium_task = service.create_task("Weekly meeting", priority="medium")
        low_task = service.create_task("Read documentation", priority="low")

        # Verify all tasks were created
        assert service.get_task_count() == 3

        # Verify priorities are set correctly
        assert high_task.priority == "high"
        assert medium_task.priority == "medium"
        assert low_task.priority == "low"

        # Verify default priority is medium
        default_task = service.create_task("Regular task")
        assert default_task.priority == "medium"

    def test_scenario_2_filter_tasks_by_priority_level(self, service):
        """Scenario 2: Filter tasks by priority level

        Given I have tasks with different priorities
        When I filter tasks by a specific priority
        Then only tasks with that priority are returned
        """
        # Create mixed priority tasks
        service.create_task("Emergency fix", priority="high")
        service.create_task("Code review", priority="high")
        service.create_task("Team meeting", priority="medium")
        service.create_task("Documentation", priority="low")
        service.create_task("Research", priority="low")

        # Filter by high priority
        high_priority_tasks = service.filter_by_priority("high")
        assert len(high_priority_tasks) == 2
        assert all(t.priority == "high" for t in high_priority_tasks)

        # Filter by medium priority
        medium_priority_tasks = service.filter_by_priority("medium")
        assert len(medium_priority_tasks) == 1
        assert medium_priority_tasks[0].priority == "medium"

        # Filter by low priority
        low_priority_tasks = service.filter_by_priority("low")
        assert len(low_priority_tasks) == 2
        assert all(t.priority == "low" for t in low_priority_tasks)

    def test_scenario_3_sort_tasks_by_priority_level(self, service):
        """Scenario 3: Sort tasks by priority level

        Given I have tasks with mixed priorities
        When I sort tasks by priority (high to low)
        Then tasks appear in correct priority order
        """
        # Create tasks in mixed order
        service.create_task("Low priority task", priority="low")
        service.create_task("High priority task", priority="high")
        service.create_task("Medium priority task", priority="medium")
        service.create_task("Another high task", priority="high")

        # Sort by priority descending (high to low)
        sorted_tasks = service.list_all_tasks(sort_by="priority")

        # Verify order: high, high, medium, low
        assert len(sorted_tasks) == 4
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "high"
        assert sorted_tasks[2].priority == "medium"
        assert sorted_tasks[3].priority == "low"

        # Sort ascending (low to high)
        sorted_asc = service.list_all_tasks(sort_by="priority", reverse=True)
        assert sorted_asc[0].priority == "low"
        assert sorted_asc[1].priority == "medium"
        assert sorted_asc[2].priority == "high"
        assert sorted_asc[3].priority == "high"

    def test_scenario_4_view_priority_summary_statistics(self, service):
        """Scenario 4: View priority summary statistics

        Given I have tasks with various priorities
        When I request priority summary
        Then I see count of tasks at each priority level
        """
        # Create tasks with known distribution
        service.create_task("Urgent 1", priority="high")
        service.create_task("Urgent 2", priority="high")
        service.create_task("Urgent 3", priority="high")
        service.create_task("Normal 1", priority="medium")
        service.create_task("Normal 2", priority="medium")
        service.create_task("Low 1", priority="low")

        # Get priority summary
        from src.services.priority_service import PriorityService
        summary = PriorityService.get_priority_summary(service.get_all_tasks())

        # Verify counts
        assert summary["high"] == 3
        assert summary["medium"] == 2
        assert summary["low"] == 1

        # Verify totals
        assert sum(summary.values()) == 6

    def test_scenario_5_update_task_priority(self, service):
        """Scenario 5: Update task priority

        Given I have a task with a priority
        When I change the task priority
        Then the task reflects the new priority
        """
        # Create a task with low priority
        task = service.create_task("Initial task", priority="low")
        assert task.priority == "low"
        task_id = task.id

        # Update to high priority
        updated = service.update_task(task_id, priority="high")
        assert updated.priority == "high"

        # Verify persistence
        retrieved = service.get_task(task_id)
        assert retrieved.priority == "high"

        # Update to medium priority
        service.update_task(task_id, priority="medium")
        final = service.get_task(task_id)
        assert final.priority == "medium"

    def test_scenario_extended_priority_with_other_filters(self, service):
        """Extended test: Combine priority with status filtering

        Given I have tasks with various priorities and statuses
        When I filter by both priority and status
        Then I get correct combination of results
        """
        # Create diverse task set
        service.create_task("High urgent", priority="high", category="work")
        service.create_task("High done", priority="high", category="work")
        service.create_task("Medium urgent", priority="medium", category="personal")
        service.create_task("Medium done", priority="medium", category="personal")
        service.create_task("Low urgent", priority="low")
        service.create_task("Low done", priority="low")

        # Mark some as completed
        service.mark_complete("task-002")  # High done
        service.mark_complete("task-004")  # Medium done
        service.mark_complete("task-006")  # Low done

        # Get pending high priority tasks
        high_pending = [t for t in service.filter_by_priority("high") if t.status == "pending"]
        assert len(high_pending) == 1
        assert high_pending[0].title == "High urgent"

        # Get completed tasks sorted by priority
        completed_tasks = service.filter_by_status("completed")
        assert len(completed_tasks) == 3

        # Verify we can still sort them by priority
        sorted_completed = service.list_all_tasks(sort_by="priority")
        completed_sorted = [t for t in sorted_completed if t.status == "completed"]
        assert len(completed_sorted) == 3
        # First completed should be high priority
        assert completed_sorted[0].priority == "high"

    def test_scenario_priority_edge_cases(self, service):
        """Test edge cases with priority management"""
        # Empty task list
        empty_high = service.filter_by_priority("high")
        assert len(empty_high) == 0

        # Single task
        service.create_task("Single task", priority="medium")
        all_medium = service.filter_by_priority("medium")
        assert len(all_medium) == 1

        # All same priority
        service.create_task("Task 2", priority="medium")
        service.create_task("Task 3", priority="medium")
        all_medium = service.filter_by_priority("medium")
        assert len(all_medium) == 3

        # Verify invalid priority raises error
        with pytest.raises(ValueError):
            service.filter_by_priority("critical")

    def test_scenario_priority_with_due_dates(self, service):
        """Test priority functionality combined with due dates"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        # Create high priority task due soon
        service.create_task(
            "Urgent: Due tomorrow",
            priority="high",
            due_date=tomorrow
        )

        # Create low priority task due later
        service.create_task(
            "Low priority: Due next week",
            priority="low",
            due_date=next_week
        )

        # Create high priority task with no due date
        service.create_task(
            "High priority: No deadline",
            priority="high"
        )

        # Verify we can filter high priority
        high_tasks = service.filter_by_priority("high")
        assert len(high_tasks) == 2

        # Verify we can get upcoming tasks within 7 days (both tomorrow and next week)
        upcoming = service.get_upcoming_tasks(days=7)
        assert len(upcoming) == 2  # Both tomorrow and next week are within 7 days
        # First should be high priority (due sooner)
        high_priority_upcoming = [t for t in upcoming if t.priority == "high"]
        assert len(high_priority_upcoming) == 1

    def test_scenario_priority_completion_stats(self, service):
        """Test tracking completion with priority levels"""
        # Create tasks with mixed priorities
        service.create_task("High task 1", priority="high")
        service.create_task("High task 2", priority="high")
        service.create_task("Medium task", priority="medium")
        service.create_task("Low task", priority="low")

        # Complete some tasks
        service.mark_complete("task-001")  # First high task
        service.mark_complete("task-003")  # Medium task

        # Get stats
        stats = service.get_completion_stats()
        assert stats["total"] == 4
        assert stats["completed"] == 2
        assert stats["pending"] == 2
        assert stats["completion_percentage"] == 50.0

        # Verify high priority tasks
        high_tasks = service.filter_by_priority("high")
        assert len(high_tasks) == 2
        completed_high = [t for t in high_tasks if t.status == "completed"]
        pending_high = [t for t in high_tasks if t.status == "pending"]
        assert len(completed_high) == 1
        assert len(pending_high) == 1
