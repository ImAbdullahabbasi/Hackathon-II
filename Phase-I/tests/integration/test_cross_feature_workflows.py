"""Integration tests for cross-feature workflows

Tests complex scenarios combining multiple features working together.
"""

import pytest
from datetime import datetime, date, timedelta
from src.services.task_service import TaskService
from src.services.filter_service import FilterService
from src.services.sort_service import SortService
from src.services.search_service import SearchService
from src.services.category_service import CategoryService
from src.services.priority_service import PriorityService


class TestWorkflowSearchAndFilter:
    """Test search combined with filtering"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_search_then_filter_by_priority(self, service):
        """Search for tasks, then filter results by priority"""
        # Create diverse tasks
        service.create_task("Urgent work report", priority="high", category="work")
        service.create_task("Regular work email", priority="medium", category="work")
        service.create_task("Work planning", priority="low", category="work")
        service.create_task("Personal project", priority="high", category="personal")

        # Search for "work"
        search_results = service.search_tasks("work")
        assert len(search_results) == 3

        # Filter search results by priority
        high_priority = [t for t in search_results if t.priority == "high"]
        assert len(high_priority) == 1
        assert high_priority[0].title == "Urgent work report"

    def test_filter_then_search_within_results(self, service):
        """Filter tasks, then search within filtered results"""
        # Create tasks
        service.create_task("Important work", priority="high", status="pending")
        service.create_task("Important personal", priority="high", status="completed")
        service.create_task("Regular work", priority="low", status="pending")

        # Filter by status=pending
        pending = service.filter_by_status("pending")
        assert len(pending) == 2

        # Search within pending for "work"
        work_pending = [t for t in pending if "work" in t.title.lower()]
        assert len(work_pending) == 2


class TestWorkflowSortAndFilter:
    """Test sort combined with filtering"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_filter_by_priority_then_sort_by_title(self, service):
        """Filter by priority, then sort results by title"""
        # Create tasks
        service.create_task("Zebra task", priority="high")
        service.create_task("Apple task", priority="high")
        service.create_task("Banana task", priority="low")

        # Filter by high priority
        high_priority = service.filter_by_priority("high")
        assert len(high_priority) == 2

        # Sort results by title
        sorted_results = SortService.sort_by_title(high_priority)
        assert sorted_results[0].title == "Apple task"
        assert sorted_results[1].title == "Zebra task"

    def test_filter_and_sort_with_status(self, service):
        """Filter by status and sort by priority"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Create mixed tasks
        service.create_task("High pending", priority="high", status="pending")
        service.create_task("Low pending", priority="low", status="pending", due_date=today)
        service.create_task("High completed", priority="high", status="completed", due_date=tomorrow)

        # Filter pending tasks
        pending = service.filter_by_status("pending")
        assert len(pending) == 2

        # Sort by priority
        sorted_pending = SortService.sort_by_priority(pending, descending=True)
        assert sorted_pending[0].priority == "high"
        assert sorted_pending[1].priority == "low"


class TestWorkflowComplexMultiStep:
    """Test complex multi-step workflows"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_workflow_organize_work_tasks(self, service):
        """Workflow: Organize all work tasks by priority"""
        # Create work tasks
        service.create_task("Meeting prep", category="work", priority="high")
        service.create_task("Email responses", category="work", priority="low")
        service.create_task("Report writing", category="work", priority="high")
        service.create_task("Documentation", category="work", priority="medium")
        service.create_task("Personal project", category="personal", priority="high")

        # Step 1: Filter to work category
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 4

        # Step 2: Sort by priority
        sorted_work = SortService.sort_by_priority(work_tasks, descending=True)
        assert sorted_work[0].priority == "high"
        assert sorted_work[1].priority == "high"
        assert sorted_work[2].priority == "medium"
        assert sorted_work[3].priority == "low"

        # Step 3: Mark high priority as complete
        service.mark_complete(sorted_work[0].id)
        service.mark_complete(sorted_work[1].id)

        # Step 4: Verify updated state
        remaining_work = service.filter_by_category("work")
        pending_work = [t for t in remaining_work if t.status == "pending"]
        assert len(pending_work) == 2

    def test_workflow_find_overdue_high_priority(self, service):
        """Workflow: Find overdue high priority tasks"""
        past = date.today() - timedelta(days=1)
        future = date.today() + timedelta(days=7)

        # Create tasks
        service.create_task("Overdue urgent", priority="high", due_date=past, status="pending")
        service.create_task("Completed urgent", priority="high", due_date=past, status="completed")
        service.create_task("Future urgent", priority="high", due_date=future)
        service.create_task("Overdue low", priority="low", due_date=past)

        # Step 1: Get overdue pending tasks
        overdue = service.get_overdue_tasks()
        assert len(overdue) == 2  # Includes both high and low

        # Step 2: Filter to high priority
        overdue_high = [t for t in overdue if t.priority == "high"]
        assert len(overdue_high) == 1
        assert overdue_high[0].title == "Overdue urgent"

    def test_workflow_search_categorize_and_prioritize(self, service):
        """Workflow: Search, then categorize and prioritize results"""
        # Create uncategorized, unprioritized tasks
        task1 = service.create_task("Bug fix needed")
        task2 = service.create_task("Bug in database")
        task3 = service.create_task("Feature development")

        # Step 1: Search for "bug"
        bug_tasks = service.search_tasks("bug")
        assert len(bug_tasks) == 2

        # Step 2: Categorize and prioritize results
        for task in bug_tasks:
            service.update_task(task.id, category="work", priority="high")

        # Step 3: Verify categorization
        work_tasks = service.filter_by_category("work")
        assert len(work_tasks) == 2
        assert all(t.priority == "high" for t in work_tasks)

    def test_workflow_multi_filter_and_sort(self, service):
        """Workflow: Apply multiple filters then sort"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Create diverse task set
        service.create_task("High work pending", priority="high", category="work", status="pending")
        service.create_task("Low work pending", priority="low", category="work", status="pending")
        service.create_task("High personal completed", priority="high", category="personal", status="completed")
        service.create_task("Medium work completed", priority="medium", category="work", status="completed", due_date=today)

        # Step 1: Multi-filter (work category AND pending status)
        filtered = FilterService.filter_tasks(
            service.get_all_tasks(),
            status="pending",
            category="work"
        )
        assert len(filtered) == 2

        # Step 2: Sort by priority
        sorted_results = SortService.sort_by_priority(filtered, descending=True)
        assert sorted_results[0].priority == "high"
        assert sorted_results[1].priority == "low"


class TestWorkflowTaskCompletion:
    """Test workflows around task completion"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_completion_workflow_with_stats(self, service):
        """Workflow: Create tasks, complete some, check stats"""
        # Create 5 tasks
        for i in range(5):
            service.create_task(f"Task {i+1}", priority="high" if i < 2 else "low")

        # Initial stats
        stats = service.get_completion_stats()
        assert stats["total"] == 5
        assert stats["pending"] == 5
        assert stats["completion_percentage"] == 0.0

        # Complete 2 high priority tasks
        all_tasks = service.get_all_tasks()
        service.mark_complete(all_tasks[0].id)
        service.mark_complete(all_tasks[1].id)

        # Updated stats
        stats = service.get_completion_stats()
        assert stats["total"] == 5
        assert stats["completed"] == 2
        assert stats["pending"] == 3
        assert stats["completion_percentage"] == 40.0

        # Verify high priority all completed
        high_priority = service.filter_by_priority("high")
        assert all(t.status == "completed" for t in high_priority)

    def test_recovery_workflow_mark_pending(self, service):
        """Workflow: Mark task complete, then revert to pending"""
        task = service.create_task("Important task", priority="high")
        task_id = task.id

        # Mark complete
        service.mark_complete(task_id)
        assert service.get_task(task_id).status == "completed"

        # Mark pending again
        service.mark_pending(task_id)
        assert service.get_task(task_id).status == "pending"


class TestWorkflowCategoryManagement:
    """Test workflows for category management"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_category_workflow_rename_and_verify(self, service):
        """Workflow: Rename category and verify all tasks updated"""
        # Create tasks in "old_category"
        service.create_task("Task 1", category="old_category")
        service.create_task("Task 2", category="old_category")
        service.create_task("Task 3", category="other_category")

        # Verify initial state
        old_cat_tasks = service.filter_by_category("old_category")
        assert len(old_cat_tasks) == 2

        # Rename category using CategoryService
        all_tasks = service.get_all_tasks()
        renamed = CategoryService.rename_category(all_tasks, "old_category", "new_category")

        # Update in service (simulate persistence)
        for task in renamed:
            if task.category == "new_category":
                service.update_task(task.id, category="new_category")

        # Verify rename worked
        new_cat_tasks = service.filter_by_category("new_category")
        assert len(new_cat_tasks) == 2

        # Verify old category is empty
        old_cat_tasks = service.filter_by_category("old_category")
        assert len(old_cat_tasks) == 0

    def test_category_workflow_summary_and_organize(self, service):
        """Workflow: Get category summary and organize by category"""
        # Create tasks in various categories
        for i in range(3):
            service.create_task(f"Work {i+1}", category="work")
        for i in range(2):
            service.create_task(f"Personal {i+1}", category="personal")
        service.create_task("No category")

        # Get summary
        summary = CategoryService.get_category_summary(service.get_all_tasks())
        assert summary["work"] == 3
        assert summary["personal"] == 2
        assert summary["uncategorized"] == 1

        # Organize: Get tasks by category
        for category in ["work", "personal"]:
            cat_tasks = service.filter_by_category(category)
            assert len(cat_tasks) > 0


class TestWorkflowSearchFiltering:
    """Test complex search and filtering workflows"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_search_workflow_refine_results(self, service):
        """Workflow: Search broad, then refine results"""
        # Create tasks
        service.create_task("Python project", category="work", priority="high")
        service.create_task("Python learning", category="personal", priority="medium")
        service.create_task("Java project", category="work", priority="low")
        service.create_task("Project management", category="work", priority="high")

        # Step 1: Broad search for "project"
        results = service.search_tasks("project")
        assert len(results) == 3  # Python project, Java project, Project management

        # Step 2: Refine to work category
        work_projects = [t for t in results if t.category == "work"]
        assert len(work_projects) == 3  # All 3 are in work category

        # Step 3: Further refine to high priority
        high_work_projects = [t for t in work_projects if t.priority == "high"]
        assert len(high_work_projects) == 2
        assert any(t.title == "Python project" for t in high_work_projects)

    def test_statistics_workflow_by_category_and_priority(self, service):
        """Workflow: Get statistics by category and priority"""
        # Create diverse tasks
        service.create_task("High work", category="work", priority="high")
        service.create_task("Medium work", category="work", priority="medium")
        service.create_task("High personal", category="personal", priority="high")
        service.create_task("Low personal", category="personal", priority="low")

        # Get work tasks
        work_tasks = service.filter_by_category("work")
        work_summary = FilterService.count_by_filter(work_tasks, "priority")
        assert work_summary["high"] == 1
        assert work_summary["medium"] == 1

        # Get personal tasks
        personal_tasks = service.filter_by_category("personal")
        personal_summary = FilterService.count_by_filter(personal_tasks, "priority")
        assert personal_summary["high"] == 1
        assert personal_summary["low"] == 1


class TestWorkflowErrorRecovery:
    """Test workflows with error handling"""

    @pytest.fixture
    def service(self):
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_search_with_invalid_keyword_handling(self, service):
        """Workflow: Handle invalid search gracefully"""
        service.create_task("Task 1")

        # Invalid empty search
        with pytest.raises(ValueError):
            service.search_tasks("")

        # Valid search still works
        results = service.search_tasks("Task")
        assert len(results) == 1

    def test_filter_with_no_matches(self, service):
        """Workflow: Handle filters that return no results"""
        service.create_task("Work task", category="work", priority="high")

        # Filter that matches nothing
        results = FilterService.filter_tasks(
            service.get_all_tasks(),
            status="pending",
            priority="low"
        )
        assert len(results) == 0

        # But service still works
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 1

    def test_sort_empty_list_handling(self, service):
        """Workflow: Sort empty result set"""
        # Empty search
        results = service.search_tasks("nonexistent")
        assert len(results) == 0

        # Sorting empty list should work
        sorted_results = SortService.sort_by_priority(results)
        assert len(sorted_results) == 0
