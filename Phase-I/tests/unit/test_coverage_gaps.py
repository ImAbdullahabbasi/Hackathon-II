"""Tests to fill coverage gaps in various modules"""

import pytest
from datetime import datetime, date, timedelta
from src.models.task import Task
from src.services.sort_service import SortService
from src.services.filter_service import FilterService
from src.services.search_service import SearchService
from src.services.task_service import TaskService


class TestSortServiceCoverageFill:
    """Test sort service edge cases for coverage"""

    def test_sort_by_created_date_descending(self):
        """Test sorting by created date in reverse order"""
        now = datetime.now()
        earlier = datetime(now.year, now.month, max(1, now.day - 1))
        later = datetime.now()

        tasks = [
            Task(id="task-1", title="Earlier", status="pending", created_timestamp=earlier),
            Task(id="task-2", title="Later", status="pending", created_timestamp=later),
        ]

        # Descending (newest first)
        result = SortService.sort_by_created_date(tasks, ascending=False)
        assert result[0].created_timestamp >= result[1].created_timestamp

    def test_sort_by_category_descending(self):
        """Test sorting by category in reverse order"""
        tasks = [
            Task(id="task-1", title="Work", status="pending", created_timestamp=datetime.now(), category="work"),
            Task(id="task-2", title="Personal", status="pending", created_timestamp=datetime.now(), category="personal"),
        ]

        result = SortService.sort_by_category(tasks, reverse=True)
        assert result[0].category == "work"
        assert result[1].category == "personal"

    def test_sort_by_due_date_descending(self):
        """Test sorting by due date in descending order"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        tasks = [
            Task(id="task-1", title="Today", status="pending", created_timestamp=datetime.now(), due_date=today),
            Task(id="task-2", title="Tomorrow", status="pending", created_timestamp=datetime.now(), due_date=tomorrow),
        ]

        result = SortService.sort_by_due_date(tasks, ascending=False)
        assert result[0].due_date > result[1].due_date


class TestFilterServiceCoverageFill:
    """Test filter service edge cases for coverage"""

    def test_filter_by_status_and_priority(self):
        """Test convenient filter method"""
        tasks = [
            Task(id="task-1", title="High pending", status="pending", priority="high", created_timestamp=datetime.now()),
            Task(id="task-2", title="Low completed", status="completed", priority="low", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_by_status_and_priority(tasks, "pending", "high")
        assert len(result) == 1
        assert result[0].priority == "high"

    def test_filter_by_status_and_category(self):
        """Test filter by status and category"""
        tasks = [
            Task(id="task-1", title="Work pending", status="pending", category="work", created_timestamp=datetime.now()),
            Task(id="task-2", title="Work completed", status="completed", category="work", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_by_status_and_category(tasks, "pending", "work")
        assert len(result) == 1

    def test_filter_by_priority_and_category(self):
        """Test filter by priority and category"""
        tasks = [
            Task(id="task-1", title="High work", status="pending", priority="high", category="work", created_timestamp=datetime.now()),
            Task(id="task-2", title="Low work", status="pending", priority="low", category="work", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_by_priority_and_category(tasks, "high", "work")
        assert len(result) == 1

    def test_filter_completed_by_priority(self):
        """Test convenient method for completed tasks by priority"""
        tasks = [
            Task(id="task-1", title="High completed", status="completed", priority="high", created_timestamp=datetime.now()),
            Task(id="task-2", title="Low pending", status="pending", priority="low", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_completed_by_priority(tasks, "high")
        assert len(result) == 1
        assert result[0].status == "completed"

    def test_filter_with_due_date_pending(self):
        """Test convenient method for pending tasks with due date"""
        today = date.today()
        tasks = [
            Task(id="task-1", title="With due date", status="pending", created_timestamp=datetime.now(), due_date=today),
            Task(id="task-2", title="No due date", status="pending", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_with_due_date_pending(tasks)
        assert len(result) == 1
        assert result[0].due_date is not None

    def test_filter_recurring_pending(self):
        """Test convenient method for recurring pending tasks"""
        tasks = [
            Task(id="task-1", title="Daily task", status="pending", recurrence="daily", created_timestamp=datetime.now()),
            Task(id="task-2", title="No recurrence", status="pending", created_timestamp=datetime.now()),
        ]

        result = FilterService.filter_recurring_pending(tasks)
        assert len(result) == 1
        assert result[0].recurrence is not None


class TestSearchServiceCoverageFill:
    """Test search service edge cases for coverage"""

    def test_search_by_title_exact_method(self):
        """Test alias method search_by_title"""
        tasks = [
            Task(id="task-1", title="Buy groceries", status="pending", created_timestamp=datetime.now()),
            Task(id="task-2", title="Sell items", status="pending", created_timestamp=datetime.now()),
        ]

        result = SearchService.search_by_title(tasks, "buy")
        assert len(result) == 1


class TestTaskServiceCoverageFill:
    """Test task service edge cases for coverage"""

    def test_search_and_filter_method(self):
        """Test search_tasks_with_filters method"""
        service = TaskService()
        service.clear_all_tasks()

        service.create_task("Work report", priority="high", category="work", status="pending")
        service.create_task("Work email", priority="low", category="work", status="completed")
        service.create_task("Personal project", priority="high", category="personal", status="pending")

        # Search with filters
        result = service.search_tasks_with_filters("work", status="pending", priority="high")
        assert len(result) == 1
        assert result[0].title == "Work report"

    def test_search_method_on_service(self):
        """Test search_tasks method on service"""
        service = TaskService()
        service.clear_all_tasks()

        service.create_task("Python development")
        service.create_task("Python learning")
        service.create_task("Java project")

        result = service.search_tasks("python")
        assert len(result) == 2

    def test_sort_by_due_date_on_service(self):
        """Test list_all_tasks with due_date parameter (lines 121-125)"""
        service = TaskService()
        service.clear_all_tasks()

        today = date.today()
        tomorrow = today + timedelta(days=1)

        task1 = service.create_task("Tomorrow task")
        task2 = service.create_task("Today task")

        # Update due dates
        service.update_task(task2.id, due_date=today)
        service.update_task(task1.id, due_date=tomorrow)

        result = service.list_all_tasks(sort_by="due_date")
        assert result[0].due_date == today

    def test_sort_by_status_on_service(self):
        """Test list_all_tasks with status parameter (line 127)"""
        service = TaskService()
        service.clear_all_tasks()

        service.create_task("First pending")
        task2 = service.create_task("Completed task")
        service.mark_complete(task2.id)

        result = service.list_all_tasks(sort_by="status")
        assert result[0].status == "completed"


class TestFilterServiceCountingEdgeCases:
    """Test filter service counting with edge cases"""

    def test_count_by_filter_with_invalid_field(self):
        """Test count_by_filter with invalid field - triggers line 291 continue"""
        tasks = [
            Task(id="task-1", title="Task 1", status="pending", priority="high", created_timestamp=datetime.now()),
            Task(id="task-2", title="Task 2", status="completed", priority="low", created_timestamp=datetime.now()),
        ]

        # Pass invalid filter field - should return empty dict due to continue
        result = FilterService.count_by_filter(tasks, "invalid_field")
        assert result == {}

    def test_count_by_filter_by_status(self):
        """Test count_by_filter with valid status field"""
        tasks = [
            Task(id="task-1", title="Task 1", status="pending", created_timestamp=datetime.now()),
            Task(id="task-2", title="Task 2", status="pending", created_timestamp=datetime.now()),
            Task(id="task-3", title="Task 3", status="completed", created_timestamp=datetime.now()),
        ]

        result = FilterService.count_by_filter(tasks, "status")
        assert result.get("pending") == 2
        assert result.get("completed") == 1


class TestSearchServiceValidationEdgeCases:
    """Test search service validation edge cases"""

    def test_search_tasks_with_empty_keyword_raises_error(self):
        """Test that empty keyword raises ValueError"""
        tasks = [Task(id="task-1", title="Test", status="pending", created_timestamp=datetime.now())]

        with pytest.raises(ValueError, match="Search keyword cannot be empty"):
            SearchService.search_tasks(tasks, "")

    def test_search_by_title_exact_with_empty_raises_error(self):
        """Test that search_by_title_exact with empty title raises ValueError (line 68)"""
        tasks = [Task(id="task-1", title="Test", status="pending", created_timestamp=datetime.now())]

        with pytest.raises(ValueError, match="Title cannot be empty"):
            SearchService.search_by_title_exact(tasks, "")


class TestSortServiceComplexScenarios:
    """Test sort service complex sorting scenarios"""

    def test_sort_by_recurrence_with_options(self):
        """Test sort_by_recurrence method"""
        tasks = [
            Task(id="task-1", title="No recurrence", status="pending", created_timestamp=datetime.now()),
            Task(id="task-2", title="Daily", status="pending", recurrence="daily", created_timestamp=datetime.now()),
        ]

        # recurring_first=True
        result = SortService.sort_by_recurrence(tasks, recurring_first=True)
        assert result[0].recurrence == "daily"

        # recurring_first=False
        result = SortService.sort_by_recurrence(tasks, recurring_first=False)
        assert result[0].recurrence is None

    def test_sort_by_completion_status_method(self):
        """Test sort_by_completion_status convenience method"""
        task1 = Task(id="task-1", title="Pending", status="pending", created_timestamp=datetime.now())
        task2 = Task(id="task-2", title="Completed", status="completed", created_timestamp=datetime.now())
        tasks = [task1, task2]

        # completed_first=False (default - pending first)
        result = SortService.sort_by_completion_status(tasks, completed_first=False)
        assert result[0].status == "pending"

        # completed_first=True
        result = SortService.sort_by_completion_status(tasks, completed_first=True)
        assert result[0].status == "completed"

    def test_sort_by_field_helper_covers_all_cases(self):
        """Test _sort_by_field helper method covers edge cases"""
        task1 = Task(id="task-1", title="A", status="pending", priority="high", created_timestamp=datetime.now())
        task2 = Task(id="task-2", title="B", status="pending", priority="low", created_timestamp=datetime.now())
        tasks = [task1, task2]

        # Test sorting with different field types
        for field in ["priority", "status", "title", "created", "category", "due_date"]:
            result = SortService.multi_sort(tasks, primary_field=field)
            assert len(result) == 2

    def test_multi_sort_with_tertiary_and_secondary_fields(self):
        """Test multi_sort with tertiary field (line 216)"""
        today = date.today()
        task1 = Task(id="task-1", title="Z", status="pending", priority="high", category="work",
                     created_timestamp=datetime.now(), due_date=today)
        task2 = Task(id="task-2", title="A", status="pending", priority="low", category="personal",
                     created_timestamp=datetime.now(), due_date=today)
        task3 = Task(id="task-3", title="M", status="pending", priority="high", category="work",
                     created_timestamp=datetime.now(), due_date=today)
        tasks = [task1, task2, task3]

        # Use multi_sort with tertiary field to trigger line 216
        result = SortService.multi_sort(
            tasks,
            primary_field="priority",
            secondary_field="category",
            tertiary_field="title"
        )
        assert len(result) == 3

    def test_multi_sort_with_due_date_and_category_fields(self):
        """Test multi_sort with due_date and category fields (lines 248, 251-254)"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        task1 = Task(id="task-1", title="Task 1", status="pending", priority="medium", category="work",
                     created_timestamp=datetime.now(), due_date=tomorrow)
        task2 = Task(id="task-2", title="Task 2", status="pending", priority="medium", category="personal",
                     created_timestamp=datetime.now(), due_date=today)
        tasks = [task1, task2]

        # Primary: category, Secondary: due_date
        result = SortService.multi_sort(tasks, primary_field="category", secondary_field="due_date")
        assert len(result) == 2

    def test_sort_by_invalid_field_returns_unchanged(self):
        """Test _sort_by_field with invalid field (line 254 else)"""
        task1 = Task(id="task-1", title="Task 1", status="pending", created_timestamp=datetime.now())
        task2 = Task(id="task-2", title="Task 2", status="pending", created_timestamp=datetime.now())
        tasks = [task1, task2]

        # multi_sort with invalid field should return unchanged
        result = SortService.multi_sort(tasks, primary_field="invalid_field")
        assert result == tasks


class TestTaskEdgeCases:
    """Test task model edge cases"""

    def test_task_with_all_optional_fields(self):
        """Test task with all optional fields set"""
        now = datetime.now()
        today = date.today()
        task = Task(
            id="task-1",
            title="Complete task",
            status="pending",
            created_timestamp=now,
            priority="high",
            category="work",
            due_date=today,
            recurrence="daily",
            completed_timestamp=None,
            parent_recurrence_id=None
        )
        assert task.priority == "high"
        assert task.category == "work"
        assert task.due_date == today
        assert task.recurrence == "daily"

    def test_task_is_overdue_property(self):
        """Test is_overdue computed property"""
        now = datetime.now()
        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        overdue_task = Task(id="task-1", title="Overdue", status="pending", created_timestamp=now, due_date=yesterday)
        assert overdue_task.is_overdue

        upcoming_task = Task(id="task-2", title="Upcoming", status="pending", created_timestamp=now, due_date=tomorrow)
        assert not upcoming_task.is_overdue

    def test_task_status_with_none_category(self):
        """Test task fields with None values"""
        now = datetime.now()
        task = Task(
            id="task-1",
            title="Task",
            status="pending",
            created_timestamp=now,
            category=None,
            due_date=None,
            recurrence=None
        )
        assert task.category is None
        assert task.due_date is None
        assert task.recurrence is None

    def test_task_invalid_id_format(self):
        """Test task validation with invalid ID formats (lines 111, 113, 116)"""
        now = datetime.now()

        # Non-string ID
        with pytest.raises(TypeError, match="ID must be a string"):
            Task(id=123, title="Task", status="pending", created_timestamp=now)

        # ID without task- prefix
        with pytest.raises(ValueError, match="ID must start with"):
            Task(id="not-task-1", title="Task", status="pending", created_timestamp=now)

        # ID with wrong format
        with pytest.raises(ValueError, match="ID format must be"):
            Task(id="task-abc", title="Task", status="pending", created_timestamp=now)

    def test_task_invalid_title_format(self):
        """Test task validation with invalid title formats (lines 130, 133, 135)"""
        now = datetime.now()

        # Non-string title
        with pytest.raises(TypeError, match="Title must be a string"):
            Task(id="task-1", title=123, status="pending", created_timestamp=now)

        # Empty title
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id="task-1", title="", status="pending", created_timestamp=now)

        # Title too long
        with pytest.raises(ValueError, match="255 characters"):
            Task(id="task-1", title="x" * 256, status="pending", created_timestamp=now)

    def test_task_invalid_status(self):
        """Test task validation with invalid status (line 148)"""
        now = datetime.now()

        with pytest.raises(ValueError, match="Status must be"):
            Task(id="task-1", title="Task", status="invalid", created_timestamp=now)

    def test_task_invalid_priority(self):
        """Test task validation with invalid priority (line 163)"""
        now = datetime.now()

        with pytest.raises(ValueError, match="Invalid priority"):
            Task(id="task-1", title="Task", status="pending", priority="urgent", created_timestamp=now)

    def test_task_invalid_due_date(self):
        """Test task validation with invalid due date (line 180)"""
        now = datetime.now()

        with pytest.raises(TypeError, match="Due date must be"):
            Task(id="task-1", title="Task", status="pending", created_timestamp=now, due_date="invalid")

    def test_task_invalid_recurrence(self):
        """Test task validation with invalid recurrence (line 199)"""
        now = datetime.now()

        with pytest.raises(ValueError, match="Invalid recurrence"):
            Task(id="task-1", title="Task", status="pending", created_timestamp=now, recurrence="yearly")

    def test_task_invalid_category_length(self):
        """Test task validation with category too long (line 214)"""
        now = datetime.now()

        with pytest.raises(ValueError, match="Category"):
            Task(id="task-1", title="Task", status="pending", created_timestamp=now, category="x" * 101)

    def test_task_repr_method(self):
        """Test task __repr__ method (line 311)"""
        now = datetime.now()
        task = Task(id="task-1", title="Test Task", status="pending", created_timestamp=now)
        repr_str = repr(task)
        assert "Task(" in repr_str
        assert "id='task-1'" in repr_str
        assert "title='Test Task'" in repr_str

    def test_task_str_method_pending(self):
        """Test task __str__ method for pending task (lines 324-326)"""
        now = datetime.now()
        task = Task(id="task-1", title="Test Task", status="pending", created_timestamp=now)
        str_repr = str(task)
        assert "○" in str_repr  # pending indicator
        assert "[task-1]" in str_repr
        assert "Test Task" in str_repr

    def test_task_str_method_completed(self):
        """Test task __str__ method for completed task (line 324)"""
        now = datetime.now()
        task = Task(id="task-2", title="Completed Task", status="completed", created_timestamp=now)
        str_repr = str(task)
        assert "✓" in str_repr  # completed indicator
        assert "[task-2]" in str_repr

    def test_task_str_method_overdue(self):
        """Test task __str__ method for overdue task (line 325)"""
        now = datetime.now()
        yesterday = date.today() - timedelta(days=1)
        task = Task(id="task-3", title="Overdue Task", status="pending", created_timestamp=now, due_date=yesterday)
        str_repr = str(task)
        assert "[OVERDUE]" in str_repr

    def test_task_next_recurrence_date_with_valid_recurrence(self):
        """Test next_recurrence_date property with valid recurrence patterns"""
        now = datetime.now()
        today = date.today()

        # Daily recurrence
        daily_task = Task(id="task-1", title="Task", status="pending", created_timestamp=now,
                         due_date=today, recurrence="daily")
        assert daily_task.next_recurrence_date == today + timedelta(days=1)

        # Weekly recurrence
        weekly_task = Task(id="task-2", title="Task", status="pending", created_timestamp=now,
                          due_date=today, recurrence="weekly")
        assert weekly_task.next_recurrence_date == today + timedelta(weeks=1)

        # Monthly recurrence
        monthly_task = Task(id="task-3", title="Task", status="pending", created_timestamp=now,
                           due_date=today, recurrence="monthly")
        next_month = monthly_task.next_recurrence_date
        assert next_month is not None

    def test_task_next_recurrence_date_none_returns_none(self):
        """Test next_recurrence_date returns None when recurrence or due_date is None"""
        now = datetime.now()
        today = date.today()

        # No recurrence
        task_no_recurrence = Task(id="task-1", title="Task", status="pending", created_timestamp=now,
                                 due_date=today)
        assert task_no_recurrence.next_recurrence_date is None

        # No due_date
        task_no_due_date = Task(id="task-2", title="Task", status="pending", created_timestamp=now,
                               recurrence="daily")
        assert task_no_due_date.next_recurrence_date is None

    def test_task_to_dict_and_from_dict_roundtrip(self):
        """Test task serialization and deserialization roundtrip"""
        now = datetime.now()
        today = date.today()
        task = Task(
            id="task-1",
            title="Test Task",
            status="pending",
            created_timestamp=now,
            completed_timestamp=None,
            priority="high",
            category="work",
            due_date=today,
            recurrence="daily"
        )

        # Serialize to dict
        task_dict = task.to_dict()
        assert isinstance(task_dict, dict)
        assert task_dict["id"] == "task-1"

        # Deserialize from dict (with datetime objects, not strings)
        reconstructed = Task.from_dict(task_dict)
        assert reconstructed.id == task.id
        assert reconstructed.title == task.title
        assert reconstructed.priority == task.priority

    def test_task_from_dict_with_datetime_objects(self):
        """Test from_dict with datetime/date objects instead of strings (lines 378, 382-387, 395)"""
        now = datetime.now()
        today = date.today()
        completed = datetime.now()

        # Create dict with actual datetime/date objects
        task_dict = {
            "id": "task-1",
            "title": "Test Task",
            "status": "completed",
            "created_timestamp": now,  # datetime object, not string
            "completed_timestamp": completed,  # datetime object, not string
            "priority": "high",
            "category": "work",
            "due_date": today,  # date object, not string
            "recurrence": "daily"
        }

        # Should handle datetime/date objects correctly
        task = Task.from_dict(task_dict)
        assert task.created_timestamp == now
        assert task.completed_timestamp == completed
        assert task.due_date == today

    def test_task_from_dict_with_string_timestamps(self):
        """Test from_dict with ISO format string timestamps (line 383)"""
        now = datetime.now()
        today = date.today()
        completed = datetime.now()

        # Create dict with ISO format strings
        task_dict = {
            "id": "task-1",
            "title": "Test Task",
            "status": "completed",
            "created_timestamp": now.isoformat(),  # string
            "completed_timestamp": completed.isoformat(),  # string
            "priority": "high",
            "category": "work",
            "due_date": today.isoformat(),  # string
            "recurrence": "daily"
        }

        # Should parse ISO format strings correctly
        task = Task.from_dict(task_dict)
        assert task.id == "task-1"
        assert task.title == "Test Task"
        assert task.status == "completed"
