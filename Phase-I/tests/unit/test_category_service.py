"""Unit tests for category management service"""

import pytest
from datetime import datetime
from src.models.task import Task
from src.services.category_service import CategoryService


class TestCategoryValidation:
    """Test category validation"""

    def test_validate_valid_category(self):
        """Test validating a valid category"""
        assert CategoryService.validate_category("work") is True
        assert CategoryService.validate_category("personal") is True
        assert CategoryService.validate_category("home-office") is True

    def test_validate_none_category(self):
        """Test validating None category (optional field)"""
        assert CategoryService.validate_category(None) is True

    def test_validate_empty_string_category(self):
        """Test validating empty string category (optional field)"""
        assert CategoryService.validate_category("") is True

    def test_validate_invalid_category_too_long(self):
        """Test validating category exceeding max length"""
        with pytest.raises(ValueError):
            CategoryService.validate_category("a" * 51)


class TestFilterByCategory:
    """Test filtering tasks by category"""

    def test_filter_single_category(self):
        """Test filtering tasks by a single category"""
        tasks = [
            Task(
                id="task-001",
                title="Work task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Personal task",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
            Task(
                id="task-003",
                title="Another work task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
        ]

        work_tasks = CategoryService.filter_by_category(tasks, "work")
        assert len(work_tasks) == 2
        assert all(t.category == "work" for t in work_tasks)

    def test_filter_no_matching_category(self):
        """Test filtering when no tasks match category"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        result = CategoryService.filter_by_category(tasks, "personal")
        assert len(result) == 0

    def test_filter_empty_task_list(self):
        """Test filtering empty task list"""
        result = CategoryService.filter_by_category([], "work")
        assert len(result) == 0

    def test_filter_invalid_category(self):
        """Test filtering with invalid category raises error"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
            )
        ]

        with pytest.raises(ValueError):
            CategoryService.filter_by_category(tasks, "a" * 51)


class TestFilterByMultipleCategories:
    """Test filtering by multiple categories"""

    def test_filter_multiple_categories_or_logic(self):
        """Test filtering tasks by multiple categories (OR operation)"""
        tasks = [
            Task(
                id="task-001",
                title="Work task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Personal task",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
            Task(
                id="task-003",
                title="Home task",
                status="pending",
                created_timestamp=datetime.now(),
                category="home",
            ),
        ]

        result = CategoryService.filter_by_categories(
            tasks, ["work", "personal"]
        )
        assert len(result) == 2
        assert all(t.category in ["work", "personal"] for t in result)

    def test_filter_no_matching_categories(self):
        """Test filtering when no tasks match any category"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        result = CategoryService.filter_by_categories(
            tasks, ["personal", "home"]
        )
        assert len(result) == 0


class TestGetAllCategories:
    """Test getting all unique categories"""

    def test_get_all_categories(self):
        """Test getting all unique categories from tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
            Task(
                id="task-003",
                title="Task 3",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
        ]

        categories = CategoryService.get_all_categories(tasks)
        assert categories == {"work", "personal"}

    def test_get_all_categories_with_uncategorized(self):
        """Test getting categories when some tasks have no category"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        categories = CategoryService.get_all_categories(tasks)
        assert categories == {"work"}

    def test_get_all_categories_empty_list(self):
        """Test getting categories from empty task list"""
        categories = CategoryService.get_all_categories([])
        assert categories == set()


class TestCategorySummary:
    """Test getting category summary"""

    def test_get_category_summary(self):
        """Test getting summary of task counts by category"""
        tasks = [
            Task(
                id="task-001",
                title="Work 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Work 2",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-003",
                title="Personal",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        summary = CategoryService.get_category_summary(tasks)
        assert summary == {"work": 2, "personal": 1}

    def test_get_category_summary_with_uncategorized(self):
        """Test category summary includes uncategorized count"""
        tasks = [
            Task(
                id="task-001",
                title="Work",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="No category",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        summary = CategoryService.get_category_summary(tasks)
        assert summary == {"work": 1, "uncategorized": 1}

    def test_get_category_summary_all_uncategorized(self):
        """Test category summary when all tasks are uncategorized"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        summary = CategoryService.get_category_summary(tasks)
        assert summary == {"uncategorized": 2}

    def test_get_category_summary_empty_list(self):
        """Test category summary on empty task list"""
        summary = CategoryService.get_category_summary([])
        assert summary == {}


class TestSetCategory:
    """Test setting task category"""

    def test_set_category_on_task(self):
        """Test setting category on a task"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
        )

        updated = CategoryService.set_category(task, "work")
        assert updated.category == "work"

    def test_set_category_overwrite_existing(self):
        """Test overwriting existing category"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
            category="personal",
        )

        updated = CategoryService.set_category(task, "work")
        assert updated.category == "work"

    def test_set_category_to_none(self):
        """Test setting category to None"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
            category="work",
        )

        updated = CategoryService.set_category(task, None)
        assert updated.category is None

    def test_set_invalid_category(self):
        """Test setting invalid category raises error"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
        )

        with pytest.raises(ValueError):
            CategoryService.set_category(task, "a" * 51)


class TestRemoveCategory:
    """Test removing category from task"""

    def test_remove_category(self):
        """Test removing category from task"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
            category="work",
        )

        updated = CategoryService.remove_category(task)
        assert updated.category is None

    def test_remove_category_already_none(self):
        """Test removing category when already None"""
        task = Task(
            id="task-001",
            title="Task",
            status="pending",
            created_timestamp=datetime.now(),
        )

        updated = CategoryService.remove_category(task)
        assert updated.category is None


class TestRenameCategory:
    """Test renaming category across tasks"""

    def test_rename_category(self):
        """Test renaming a category across all tasks"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="old_name",
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="pending",
                created_timestamp=datetime.now(),
                category="other",
            ),
            Task(
                id="task-003",
                title="Task 3",
                status="pending",
                created_timestamp=datetime.now(),
                category="old_name",
            ),
        ]

        renamed = CategoryService.rename_category(tasks, "old_name", "new_name")
        assert len(renamed) == 3
        assert renamed[0].category == "new_name"
        assert renamed[1].category == "other"
        assert renamed[2].category == "new_name"

    def test_rename_category_no_matches(self):
        """Test renaming category when no tasks match"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        renamed = CategoryService.rename_category(tasks, "personal", "home")
        assert renamed[0].category == "work"

    def test_rename_invalid_old_category(self):
        """Test renaming with invalid old category"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        with pytest.raises(ValueError):
            CategoryService.rename_category(tasks, "a" * 51, "work")

    def test_rename_invalid_new_category(self):
        """Test renaming with invalid new category"""
        tasks = [
            Task(
                id="task-001",
                title="Task",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        with pytest.raises(ValueError):
            CategoryService.rename_category(tasks, "work", "a" * 51)


class TestTasksWithCategory:
    """Test getting tasks with/without categories"""

    def test_tasks_with_category(self):
        """Test getting all tasks that have a category"""
        tasks = [
            Task(
                id="task-001",
                title="With category",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="No category",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Also with category",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        result = CategoryService.tasks_with_category(tasks)
        assert len(result) == 2
        assert all(t.category is not None for t in result)

    def test_tasks_without_category(self):
        """Test getting all tasks without category"""
        tasks = [
            Task(
                id="task-001",
                title="With category",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="No category",
                status="pending",
                created_timestamp=datetime.now(),
            ),
            Task(
                id="task-003",
                title="Also no category",
                status="pending",
                created_timestamp=datetime.now(),
            ),
        ]

        result = CategoryService.tasks_without_category(tasks)
        assert len(result) == 2
        assert all(t.category is None for t in result)

    def test_tasks_with_category_all_categorized(self):
        """Test getting tasks when all have categories"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            ),
            Task(
                id="task-002",
                title="Task 2",
                status="pending",
                created_timestamp=datetime.now(),
                category="personal",
            ),
        ]

        result = CategoryService.tasks_with_category(tasks)
        assert len(result) == 2

    def test_tasks_without_category_none_uncategorized(self):
        """Test getting uncategorized tasks when all have categories"""
        tasks = [
            Task(
                id="task-001",
                title="Task 1",
                status="pending",
                created_timestamp=datetime.now(),
                category="work",
            )
        ]

        result = CategoryService.tasks_without_category(tasks)
        assert len(result) == 0
