"""Acceptance tests for User Story 3: Search Tasks

User Story: "As a user, I want to search for tasks by keyword
so that I can quickly find specific tasks without scrolling through my entire list."

Acceptance Scenarios:
1. Search for tasks by keyword in title
2. Case-insensitive search
3. Partial matching (substring search)
4. Search with no results
5. Search combined with other filters
"""

import pytest
from datetime import datetime, date, timedelta
from src.services.task_service import TaskService
from src.models.task import Task


class TestUserStory3SearchTasks:
    """Test User Story 3: Search tasks by keyword"""

    @pytest.fixture
    def service(self):
        """Create a fresh TaskService for each test"""
        service = TaskService()
        service.clear_all_tasks()
        return service

    def test_scenario_1_search_tasks_by_keyword(self, service):
        """Scenario 1: Search for tasks by keyword in title

        Given I have tasks with various titles
        When I search for a keyword
        Then all tasks with that keyword in title are returned
        """
        # Create tasks with various titles
        service.create_task("Buy groceries")
        service.create_task("Buy furniture")
        service.create_task("Cook dinner")
        service.create_task("Clean house")
        service.create_task("Buy supplies")

        # Search for "buy"
        results = service.search_tasks("buy")
        assert len(results) == 3
        assert all("buy" in t.title.lower() for t in results)

        # Search for "cook"
        results = service.search_tasks("cook")
        assert len(results) == 1
        assert results[0].title == "Cook dinner"

        # Search for "clean"
        results = service.search_tasks("clean")
        assert len(results) == 1
        assert results[0].title == "Clean house"

    def test_scenario_2_case_insensitive_search(self, service):
        """Scenario 2: Case-insensitive search

        Given I have tasks with various cases in titles
        When I search with different cases
        Then all case variations match
        """
        # Create tasks with mixed case
        service.create_task("BUY groceries")
        service.create_task("Buy Furniture")
        service.create_task("buy supplies")

        # Search with lowercase
        results = service.search_tasks("buy")
        assert len(results) == 3

        # Search with uppercase
        results = service.search_tasks("BUY")
        assert len(results) == 3

        # Search with mixed case
        results = service.search_tasks("Buy")
        assert len(results) == 3

    def test_scenario_3_partial_matching(self, service):
        """Scenario 3: Partial matching (substring search)

        Given I have tasks with various titles
        When I search for a partial keyword
        Then all tasks containing that substring are returned
        """
        # Create tasks where partial match is important
        service.create_task("Grocery list review")
        service.create_task("Buy groceries")
        service.create_task("Cooking instructions")
        service.create_task("Urgent review meeting")

        # Search for "review" matches two tasks
        results = service.search_tasks("review")
        assert len(results) == 2
        assert all("review" in t.title.lower() for t in results)

        # Search for "grocer" matches two tasks (substring)
        results = service.search_tasks("grocer")
        assert len(results) == 2
        assert any("grocery" in t.title.lower() for t in results)
        assert any("groceries" in t.title.lower() for t in results)

        # Search for "cook" matches one task
        results = service.search_tasks("cook")
        assert len(results) == 1

    def test_scenario_4_search_no_results(self, service):
        """Scenario 4: Search with no results

        Given I have tasks
        When I search for a keyword that doesn't exist
        Then I get empty results
        """
        # Create some tasks
        service.create_task("Buy groceries")
        service.create_task("Cook dinner")
        service.create_task("Clean house")

        # Search for non-existent keyword
        results = service.search_tasks("xyz")
        assert len(results) == 0

        # Search for empty list
        results = service.search_tasks("programming")
        assert len(results) == 0

    def test_scenario_5_search_with_filters(self, service):
        """Scenario 5: Search combined with other filters

        Given I have tasks with various attributes
        When I search with additional filters
        Then only tasks matching all criteria are returned
        """
        # Create diverse tasks
        service.create_task(
            "Urgent work report",
            priority="high",
            category="work",
            status="pending"
        )
        service.create_task(
            "Work meeting completed",
            priority="high",
            category="work",
            status="completed"
        )
        service.create_task(
            "Personal work task",
            priority="medium",
            category="personal",
            status="pending"
        )
        service.create_task(
            "Work on house",
            priority="low",
            category="home",
            status="pending"
        )

        # Search for "work" without filters (all matches)
        results = service.search_tasks("work")
        assert len(results) == 4

        # Search with status filter (pending only)
        results = service.search_tasks_with_filters(
            "work", status="pending"
        )
        assert len(results) == 3
        assert all(t.status == "pending" for t in results)

        # Search with priority filter (high priority only)
        results = service.search_tasks_with_filters(
            "work", priority="high"
        )
        assert len(results) == 2
        assert all(t.priority == "high" for t in results)

        # Search with category filter
        results = service.search_tasks_with_filters(
            "work", category="work"
        )
        assert len(results) == 2
        assert all(t.category == "work" for t in results)

        # Search with multiple filters
        results = service.search_tasks_with_filters(
            "work", status="pending", priority="high", category="work"
        )
        assert len(results) == 1
        assert results[0].title == "Urgent work report"

    def test_scenario_extended_search_with_special_chars(self, service):
        """Extended test: Search with special characters

        Given I have tasks with special characters in titles
        When I search for those characters
        Then matches work correctly
        """
        # Create tasks with special characters
        service.create_task("Task with (parentheses)")
        service.create_task("Task with 'quotes'")
        service.create_task("Task with #hashtag")
        service.create_task("Task with @mention")

        # Search for parts with special chars
        results = service.search_tasks("parentheses")
        assert len(results) == 1

        results = service.search_tasks("quotes")
        assert len(results) == 1

        results = service.search_tasks("hashtag")
        assert len(results) == 1

        results = service.search_tasks("mention")
        assert len(results) == 1

    def test_scenario_extended_search_empty_results_message(self, service):
        """Extended test: Handling search with no results

        Given I have a populated task list
        When I search for a keyword with no matches
        Then I get an empty list (appropriate response)
        """
        # Create tasks
        service.create_task("Task 1")
        service.create_task("Task 2")
        service.create_task("Task 3")

        # Search that yields no results
        results = service.search_tasks("nonexistent")

        # Should return empty list (not error)
        assert isinstance(results, list)
        assert len(results) == 0

        # Service should still work after search
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 3

    def test_scenario_search_error_on_empty_keyword(self, service):
        """Test that empty keyword raises error

        Given I have tasks
        When I try to search with empty keyword
        Then I get an error
        """
        service.create_task("Task 1")

        # Empty string should raise error
        with pytest.raises(ValueError):
            service.search_tasks("")

        # Whitespace only should raise error
        with pytest.raises(ValueError):
            service.search_tasks("   ")

    def test_scenario_search_preserves_task_data(self, service):
        """Test that search results preserve all task data

        Given I have tasks with multiple attributes
        When I search for them
        Then all task attributes are intact
        """
        # Create complex task
        tomorrow = date.today() + timedelta(days=1)
        original_task = service.create_task(
            "Search for this task",
            priority="high",
            category="work",
            due_date=tomorrow
        )

        # Search and retrieve
        results = service.search_tasks("search")
        assert len(results) == 1

        found_task = results[0]
        assert found_task.id == original_task.id
        assert found_task.title == original_task.title
        assert found_task.priority == original_task.priority
        assert found_task.category == original_task.category
        assert found_task.due_date == original_task.due_date
        assert found_task.status == original_task.status

    def test_scenario_search_across_all_task_fields_awareness(self, service):
        """Test user awareness that search only checks title

        Given tasks with keywords in different fields
        When I search
        Then only title matches are returned
        """
        # Create tasks where keyword exists in non-title fields
        service.create_task(
            "Regular task",
            category="work",
            priority="high"
        )
        service.create_task(
            "Another task",
            category="high-priority",
            priority="low"
        )
        service.create_task(
            "High priority task",
            category="personal",
            priority="low"
        )

        # Search for "high" - should match title only
        results = service.search_tasks("high")
        assert len(results) == 1
        assert results[0].title == "High priority task"

    def test_scenario_search_integration_with_completion(self, service):
        """Test search works with task completion status

        Given I have pending and completed tasks
        When I search
        Then both pending and completed matching tasks are returned
        """
        # Create and complete some tasks
        task1 = service.create_task("Work on report")
        task2 = service.create_task("Work on proposal")
        task3 = service.create_task("Work on presentation")

        # Complete one task
        service.mark_complete(task2.id)

        # Search for "work" gets all three
        results = service.search_tasks("work")
        assert len(results) == 3

        # Filter search results by status
        pending_results = [t for t in results if t.status == "pending"]
        completed_results = [t for t in results if t.status == "completed"]

        assert len(pending_results) == 2
        assert len(completed_results) == 1

    def test_scenario_search_with_many_tasks(self, service):
        """Test search performance with larger task list

        Given I have many tasks
        When I search
        Then search completes quickly with correct results
        """
        # Create many tasks
        for i in range(50):
            if i % 10 == 0:
                service.create_task(f"Important task {i}")
            elif i % 5 == 0:
                service.create_task(f"Regular task {i}")
            else:
                service.create_task(f"Task {i}")

        # Search for specific pattern
        results = service.search_tasks("Important")
        assert len(results) == 5  # 0, 10, 20, 30, 40

        # Search for another pattern (5, 15, 25, 35, 45 but 10, 20, 30, 40 are "Important")
        # Actually 5, 15, 25, 35, 45 - that's 5 total
        results = service.search_tasks("Regular")
        assert len(results) == 5  # 5, 15, 25, 35, 45

        # Search for generic "task" keyword
        results = service.search_tasks("task")
        assert len(results) == 50  # All tasks contain "task"

    def test_scenario_search_unicode_and_special_chars(self, service):
        """Test search with unicode and special characters

        Given I have tasks with unicode characters
        When I search
        Then unicode search works correctly
        """
        # Create tasks with unicode
        service.create_task("Task with emojis 🎉 🚀")
        service.create_task("Task with accents: café")
        service.create_task("Task with symbols: $100")

        # Search for emoji (if supported by Python string operations)
        results = service.search_tasks("emojis")
        assert len(results) == 1

        # Search for accented character
        results = service.search_tasks("caf")
        assert len(results) == 1

        # Search for symbol
        results = service.search_tasks("$")
        assert len(results) == 1
        assert "$100" in results[0].title
