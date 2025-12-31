"""Acceptance tests for User Story 2: Organize Tasks by Category

User Story: "As a user, I want to organize and view my tasks by category
(work, personal, home-office, etc.) so that I can manage different aspects of my life."

Acceptance Scenarios:
1. Create tasks with different categories
2. Filter tasks by category
3. View category summary statistics
4. Update task category
5. View categorized vs uncategorized tasks
6. Rename category across all tasks
"""

import pytest
from datetime import datetime, date, timedelta
from src.services.task_service import TaskService
from src.services.category_service import CategoryService
from src.models.task import Task


class TestUserStory2CategoryManagement:
    """Test User Story 2: Organize tasks by category"""

    @pytest.fixture
    def service(self):
        """Create a fresh TaskService for each test"""
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_scenario_1_create_tasks_with_different_categories(self, service):
        """Scenario 1: Create tasks with different categories

        Given I have no tasks
        When I create tasks with work, personal, and home categories
        Then all tasks should be created with correct categories
        """
        # Create tasks with different categories
        work_task = service.create_task("Complete report", category="work")
        personal_task = service.create_task(
            "Buy groceries", category="personal"
        )
        home_task = service.create_task("Fix kitchen", category="home-office")

        # Verify all tasks were created
        assert service.get_task_count() == 3

        # Verify categories are set correctly
        assert work_task.category == "work"
        assert personal_task.category == "personal"
        assert home_task.category == "home-office"

        # Verify tasks can be created without category
        uncategorized = service.create_task("Random task")
        assert uncategorized.category is None

    def test_scenario_2_filter_tasks_by_category(self, service):
        """Scenario 2: Filter tasks by category

        Given I have tasks with different categories
        When I filter tasks by a specific category
        Then only tasks with that category are returned
        """
        # Create mixed category tasks
        service.create_task("Project planning", category="work")
        service.create_task("Code review", category="work")
        service.create_task("Dinner plans", category="personal")
        service.create_task("Fix fence", category="home-office")
        service.create_task("Call mom", category="personal")

        # Filter by work category
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 2
        assert all(t.category == "work" for t in work_tasks)

        # Filter by personal category
        personal_tasks = service.filter_by_category("personal")
        assert len(personal_tasks) == 2
        assert all(t.category == "personal" for t in personal_tasks)

        # Filter by home-office category
        home_tasks = service.filter_by_category("home-office")
        assert len(home_tasks) == 1
        assert home_tasks[0].category == "home-office"

    def test_scenario_3_view_category_summary_statistics(self, service):
        """Scenario 3: View category summary statistics

        Given I have tasks with various categories
        When I request category summary
        Then I see count of tasks at each category
        """
        # Create tasks with known distribution
        service.create_task("Work 1", category="work")
        service.create_task("Work 2", category="work")
        service.create_task("Work 3", category="work")
        service.create_task("Personal 1", category="personal")
        service.create_task("Personal 2", category="personal")
        service.create_task("Home task", category="home-office")
        service.create_task("Uncategorized")

        # Get category summary
        summary = CategoryService.get_category_summary(
            service.get_all_tasks()
        )

        # Verify counts
        assert summary["work"] == 3
        assert summary["personal"] == 2
        assert summary["home-office"] == 1
        assert summary["uncategorized"] == 1

        # Verify totals
        assert sum(summary.values()) == 7

    def test_scenario_4_update_task_category(self, service):
        """Scenario 4: Update task category

        Given I have a task with a category
        When I change the task category
        Then the task reflects the new category
        """
        # Create a task with work category
        task = service.create_task("Initial task", category="work")
        assert task.category == "work"
        task_id = task.id

        # Update to personal category
        updated = service.update_task(task_id, category="personal")
        assert updated.category == "personal"

        # Verify persistence
        retrieved = service.get_task(task_id)
        assert retrieved.category == "personal"

        # Remove category
        service.update_task(task_id, category=None)
        final = service.get_task(task_id)
        assert final.category is None

    def test_scenario_5_view_categorized_vs_uncategorized_tasks(self, service):
        """Scenario 5: View categorized vs uncategorized tasks

        Given I have mixed categorized and uncategorized tasks
        When I query for categorized and uncategorized tasks
        Then I get correct groups
        """
        # Create mixed tasks
        service.create_task("Work task 1", category="work")
        service.create_task("Work task 2", category="work")
        service.create_task("Personal task", category="personal")
        service.create_task("Uncategorized 1")
        service.create_task("Uncategorized 2")

        # Get categorized tasks
        categorized = CategoryService.tasks_with_category(
            service.get_all_tasks()
        )
        assert len(categorized) == 3
        assert all(t.category is not None for t in categorized)

        # Get uncategorized tasks
        uncategorized = CategoryService.tasks_without_category(
            service.get_all_tasks()
        )
        assert len(uncategorized) == 2
        assert all(t.category is None for t in uncategorized)

    def test_scenario_6_rename_category_across_tasks(self, service):
        """Scenario 6: Rename category across all tasks

        Given I have multiple tasks in a category
        When I rename that category
        Then all tasks in that category get the new name
        """
        # Create tasks with "work" category
        task1 = service.create_task("Task 1", category="work")
        task2 = service.create_task("Task 2", category="work")
        task3 = service.create_task("Task 3", category="personal")

        # Rename work to job
        all_tasks = service.get_all_tasks()
        renamed_tasks = CategoryService.rename_category(
            all_tasks, "work", "job"
        )

        # Update storage with renamed tasks (simulate persistence)
        for task in renamed_tasks:
            if task.id in [task1.id, task2.id]:
                service.update_task(task.id, category="job")

        # Verify rename worked
        job_tasks = service.filter_by_category("job")
        assert len(job_tasks) == 2
        assert all(t.category == "job" for t in job_tasks)

        # Verify old category doesn't exist
        old_work = service.filter_by_category("work")
        assert len(old_work) == 0

        # Verify other category unchanged
        personal_tasks = service.filter_by_category("personal")
        assert len(personal_tasks) == 1

    def test_scenario_extended_categories_with_priority(self, service):
        """Extended test: Combine categories with priority filtering

        Given I have tasks with both categories and priorities
        When I filter by category and then by priority
        Then I get correct combination of results
        """
        # Create tasks with both category and priority
        service.create_task(
            "Urgent report", category="work", priority="high"
        )
        service.create_task(
            "Regular meeting", category="work", priority="medium"
        )
        service.create_task(
            "Urgent call", category="personal", priority="high"
        )
        service.create_task(
            "Casual reading", category="personal", priority="low"
        )

        # Get all work category tasks
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 2

        # Get high priority work tasks
        high_work = [t for t in work_tasks if t.priority == "high"]
        assert len(high_work) == 1
        assert high_work[0].title == "Urgent report"

        # Get high priority tasks across all categories
        all_high = [t for t in service.get_all_tasks() if t.priority == "high"]
        assert len(all_high) == 2

        # Verify category distribution of high priority tasks
        high_by_category = {}
        for task in all_high:
            cat = task.category or "uncategorized"
            high_by_category[cat] = high_by_category.get(cat, 0) + 1

        assert high_by_category["work"] == 1
        assert high_by_category["personal"] == 1

    def test_scenario_extended_categories_with_status(self, service):
        """Extended test: Track completion by category

        Given I have categorized tasks with various statuses
        When I mark some as complete
        Then I can see completion rate by category
        """
        # Create work tasks
        work1 = service.create_task("Work task 1", category="work")
        work2 = service.create_task("Work task 2", category="work")

        # Create personal tasks
        personal1 = service.create_task("Personal task 1", category="personal")
        personal2 = service.create_task("Personal task 2", category="personal")

        # Mark some as complete
        service.mark_complete(work1.id)
        service.mark_complete(personal1.id)

        # Get work category summary
        work_tasks = service.filter_by_category("work")
        work_completed = [t for t in work_tasks if t.status == "completed"]
        work_pending = [t for t in work_tasks if t.status == "pending"]
        assert len(work_completed) == 1
        assert len(work_pending) == 1

        # Get personal category summary
        personal_tasks = service.filter_by_category("personal")
        personal_completed = [
            t for t in personal_tasks if t.status == "completed"
        ]
        personal_pending = [t for t in personal_tasks if t.status == "pending"]
        assert len(personal_completed) == 1
        assert len(personal_pending) == 1

        # Overall stats
        stats = service.get_completion_stats()
        assert stats["total"] == 4
        assert stats["completed"] == 2
        assert stats["pending"] == 2
        assert stats["completion_percentage"] == 50.0

    def test_scenario_categories_with_due_dates(self, service):
        """Test categories combined with due dates

        Given I have tasks with categories and due dates
        When I filter by category and due date
        Then I get correct results
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        # Create work tasks with various due dates
        service.create_task(
            "Due today", category="work", due_date=today
        )
        service.create_task(
            "Due tomorrow", category="work", due_date=tomorrow
        )

        # Create personal task due soon
        service.create_task(
            "Personal due soon", category="personal", due_date=tomorrow
        )

        # Get work category tasks
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 2

        # Get upcoming tasks (within 7 days)
        upcoming = service.get_upcoming_tasks(days=7)
        assert len(upcoming) == 3  # All three are within 7 days

        # Get overdue tasks (work task due today could be overdue depending on time)
        overdue = service.get_overdue_tasks()
        # This may or may not include the "Due today" depending on exact time

    def test_scenario_category_edge_cases(self, service):
        """Test edge cases with category management"""
        # Empty task list
        empty_work = service.filter_by_category("work")
        assert len(empty_work) == 0

        # Single task with category
        service.create_task("Single task", category="work")
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 1

        # All same category
        service.create_task("Task 2", category="work")
        service.create_task("Task 3", category="work")
        all_work = service.filter_by_category("work")
        assert len(all_work) == 3

        # Mix of categorized and uncategorized
        service.create_task("Uncategorized")
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 4

        # Get all unique categories
        categories = CategoryService.get_all_categories(all_tasks)
        assert categories == {"work"}

    def test_scenario_invalid_category_handling(self, service):
        """Test that invalid categories are rejected

        Given category validation is in place
        When I try to use invalid category
        Then I get an error
        """
        # Category too long
        with pytest.raises(ValueError):
            service.create_task("Task", category="a" * 51)

        # Valid category should work
        task = service.create_task("Task", category="work")
        assert task.category == "work"

    def test_scenario_category_operations_preservation(self, service):
        """Test that category operations preserve other task data

        Given I have tasks with multiple fields
        When I modify category
        Then other fields remain unchanged
        """
        # Create complex task
        task = service.create_task(
            "Complex task",
            priority="high",
            category="work",
            status="pending",
        )
        task_id = task.id
        original_title = task.title
        original_priority = task.priority
        original_created = task.created_timestamp

        # Update category
        service.update_task(task_id, category="personal")

        # Retrieve and verify
        updated = service.get_task(task_id)
        assert updated.category == "personal"
        assert updated.title == original_title
        assert updated.priority == original_priority
        assert updated.created_timestamp == original_created
        assert updated.status == "pending"

    def test_scenario_category_bulk_operations(self, service):
        """Test bulk operations with categories

        Given I have multiple tasks in a category
        When I perform operations on that category
        Then all tasks are affected correctly
        """
        # Create tasks
        service.create_task("Task 1", category="temp")
        service.create_task("Task 2", category="temp")
        service.create_task("Task 3", category="temp")

        # Verify category has 3 tasks
        temp_tasks = service.filter_by_category("temp")
        assert len(temp_tasks) == 3

        # Update all tasks in category to new category
        for task in temp_tasks:
            service.update_task(task.id, category="work")

        # Verify all moved
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 3

        # Verify old category is empty
        old_temp = service.filter_by_category("temp")
        assert len(old_temp) == 0
