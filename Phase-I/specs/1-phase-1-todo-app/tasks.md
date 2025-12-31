# Tasks: Phase 1 Todo App - Intermediate and Advanced Features

**Input**: Design documents from `/specs/1-phase-1-todo-app/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅
**Total Tasks**: 85+ across 10 phases
**User Stories**: 7 (P1: Stories 1-2, P2: Stories 3-5, P3: Stories 6-7)

**Organization**: Tasks organized by user story phase to enable independent implementation and testing of each story.

---

## Format: `[ID] [P] [StoryX] Description with file path`

- **[P]**: Task can run in parallel (different files, no task dependencies)
- **[StoryX]**: Which user story (US1, US2, US3, US4, US5, US6, US7)
- File paths are absolute and specific
- Each task is independently completable

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure
**Dependency**: None - can start immediately
**Acceptance**: Project structure created per plan.md, basic imports working

### Phase 1 Tasks

- [ ] T001 Create project directory structure per plan.md: `src/`, `src/models/`, `src/services/`, `src/cli/`, `src/cli/commands/`, `tests/`, `tests/unit/`, `tests/integration/`, `tests/acceptance/`
- [ ] T002 [P] Create `src/__init__.py` and `pyproject.toml` with Python 3.13+ specification and test framework configuration
- [ ] T003 [P] Create `src/models/__init__.py` for package initialization
- [ ] T004 [P] Create `src/services/__init__.py` for package initialization
- [ ] T005 [P] Create `src/cli/__init__.py` and `src/cli/commands/__init__.py` for package initialization
- [ ] T006 [P] Create `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`, `tests/acceptance/__init__.py`
- [ ] T007 Create `src/storage.py` module with TaskStorage interface (setup only, no implementation)
- [ ] T008 Create `README.md` with project overview and setup instructions

**Checkpoint**: Project structure in place, imports working

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented
**Dependency**: Depends on Phase 1 completion
**Acceptance**: All data models working, validation rules implemented, storage interface ready

### Enumerations & Basic Models

- [ ] T009 [P] Create enumerations module `src/models/enums.py` with Priority{HIGH, MEDIUM, LOW}, Status{PENDING, COMPLETED}, Recurrence{DAILY, WEEKLY, MONTHLY}
- [ ] T010 [P] Create validators module `src/models/validators.py` with functions: `validate_priority()`, `validate_category()`, `validate_due_date()`, `validate_recurrence()`, `validate_task_title()`
- [ ] T011 Create Task model class in `src/models/task.py` with all fields from data-model.md: id, title, status, created_timestamp, completed_timestamp, priority, category, due_date, recurrence, parent_recurrence_id

### Validation Integration

- [ ] T012 Add validation to Task model `__init__` method: call validators for each field before assignment
- [ ] T013 [P] Implement `is_overdue()` property in Task class to compute overdue status
- [ ] T014 [P] Implement `next_recurrence_date()` property in Task class to compute next recurrence
- [ ] T015 Add `__repr__` and `__str__` methods to Task for debugging and display

### In-Memory Storage

- [ ] T016 Implement TaskStorage class in `src/storage.py` with methods: `create()`, `read()`, `read_all()`, `update()`, `delete()`, `clear()`, `get_next_task_id()`
- [ ] T017 Implement task ID generation logic (format: task-NNN with auto-increment)
- [ ] T018 Implement validation in storage layer to ensure only valid tasks are stored
- [ ] T019 Create unit test file `tests/unit/test_task_model.py` for Task entity tests (creation, validation, defaults)
- [ ] T020 [P] Create unit test file `tests/unit/test_validators.py` for all validation functions
- [ ] T021 Create unit test file `tests/unit/test_storage.py` for storage CRUD operations

**Checkpoint**: Foundation ready - all data models validated, storage working. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Organize Tasks by Priority (Priority: P1) 🎯

**Goal**: Enable users to assign priority levels (high, medium, low) to tasks and filter by priority
**Independent Test**: Create 3 tasks with different priorities, filter by each priority, verify correct tasks returned
**User Story Acceptance**: All 5 acceptance scenarios from spec.md passing

### Data Model for User Story 1

- [ ] T022 [P] Unit test file `tests/unit/test_priority_service.py` with test cases for priority operations (create, read, filter, sort)
- [ ] T023 Add priority field validation in existing Task model (verify enum values)

### Implementation for User Story 1

- [ ] T024 [P] Create PriorityService class in `src/services/priority_service.py` with methods: `validate_priority()`, `filter_by_priority()`, `sort_by_priority()`
- [ ] T025 [P] Implement TaskService in `src/services/task_service.py` with CRUD operations that integrate with storage: `create_task()`, `update_task()`, `get_task()`, `get_all_tasks()`, `delete_task()`
- [ ] T026 Implement priority setting in TaskService: `set_task_priority(task_id, priority)`
- [ ] T027 Add priority display in CLI formatters module `src/cli/formatters.py` with function `format_task_for_display()` showing priority level

### CLI Implementation for User Story 1

- [ ] T028 Create `src/cli/commands/add.py` command handler with arguments: title (required), --priority {HIGH,MEDIUM,LOW} (optional), --category TEXT (optional)
- [ ] T029 Create `src/cli/commands/update.py` command handler with arguments: task_id (required), --priority {HIGH,MEDIUM,LOW}, --category TEXT, --title TEXT
- [ ] T030 Create `src/cli/commands/list.py` command handler with arguments: --filter-priority {HIGH,MEDIUM,LOW} (optional), --sort-by {PRIORITY,TITLE,DUE_DATE} (optional), --sort-order {ASC,DESC} (optional)
- [ ] T031 Add help text and examples for priority options in `src/cli/main.py` or command help strings

### Integration for User Story 1

- [ ] T032 [P] Integrate PriorityService into TaskService for filtering and sorting operations
- [ ] T033 Update `src/cli/commands/list.py` to call PriorityService.filter_by_priority() when --filter-priority is specified
- [ ] T034 Update `src/cli/commands/list.py` to call PriorityService.sort_by_priority() when --sort-by PRIORITY is specified
- [ ] T035 Test Task creation with priority (default to "medium", accept high/low/medium)
- [ ] T036 Test Task update with priority change
- [ ] T037 Acceptance test: Create 3 tasks with different priorities, list all, verify defaults and storage
- [ ] T038 Acceptance test: Filter tasks by high priority, verify only high-priority tasks shown
- [ ] T039 Acceptance test: Attempt to set invalid priority "urgent", verify error message matches spec

**Checkpoint**: User Story 1 fully functional and independently testable. All 5 acceptance scenarios passing.

---

## Phase 4: User Story 2 - Categorize Tasks with Tags (Priority: P1)

**Goal**: Enable users to assign categories/tags to tasks and filter by category
**Independent Test**: Create 4 tasks with different categories, filter by category, verify correct tasks returned
**User Story Acceptance**: All 6 acceptance scenarios from spec.md passing

### Data Model for User Story 2

- [ ] T040 [P] Unit test file `tests/unit/test_category_service.py` with test cases for category operations (validate, filter)
- [ ] T041 Add category field validation in existing Task model (string, max 50 chars, optional)

### Implementation for User Story 2

- [ ] T042 [P] Create CategoryService class in `src/services/category_service.py` with methods: `validate_category()`, `filter_by_category()`
- [ ] T043 [P] Extend TaskService with category operations: `set_task_category(task_id, category)`
- [ ] T044 Update CLI formatters to display category information in task display output

### CLI Implementation for User Story 2

- [ ] T045 Update `src/cli/commands/add.py` with --category flag (already added in Phase 3, T028)
- [ ] T046 Update `src/cli/commands/update.py` with --category flag (already added in Phase 3, T029)
- [ ] T047 Update `src/cli/commands/list.py` to support --filter-category TEXT
- [ ] T048 Add category help text and examples to CLI help text

### Integration for User Story 2

- [ ] T049 [P] Integrate CategoryService into TaskService for filtering operations
- [ ] T050 Update `src/cli/commands/list.py` to call CategoryService.filter_by_category() when --filter-category is specified
- [ ] T051 Test Task creation with category (optional, string, special chars allowed)
- [ ] T052 Test Task update with category change
- [ ] T053 Test empty string category (accept as optional empty)
- [ ] T054 Acceptance test: Create 4 tasks with different categories, filter by "work", verify correct tasks
- [ ] T055 Acceptance test: Create task without category, update to add category, verify change persisted
- [ ] T056 Acceptance test: Filter by category with special characters in category name, verify handling

**Checkpoint**: User Story 2 fully functional. All 6 acceptance scenarios passing. Users can now organize by priority AND category independently.

---

## Phase 5: User Story 3 - Search Tasks by Keyword (Priority: P2)

**Goal**: Enable users to search tasks by keyword in title
**Independent Test**: Create tasks with specific keywords, search for them, verify results
**User Story Acceptance**: All 5 acceptance scenarios from spec.md passing

### Data Model for User Story 3

- [ ] T057 [P] Unit test file `tests/unit/test_search_service.py` with test cases for search operations (case-insensitive, partial matching)

### Implementation for User Story 3

- [ ] T058 [P] Create SearchService class in `src/services/search_service.py` with methods: `search_tasks()` (case-insensitive partial match on title)
- [ ] T059 Extend TaskService with search integration: `search_tasks(keyword)`
- [ ] T060 Implement case-insensitive partial matching logic (title.lower().find(keyword.lower()) >= 0)

### CLI Implementation for User Story 3

- [ ] T061 Update `src/cli/commands/list.py` to support --search KEYWORD
- [ ] T062 Add search help text and examples to CLI

### Integration for User Story 3

- [ ] T063 [P] Integrate SearchService into TaskService for search operations
- [ ] T064 Update list command to call SearchService.search_tasks() when --search is specified
- [ ] T065 Test case-insensitive search ("BUY" matches "buy groceries")
- [ ] T066 Test partial matching (search "grocery" matches "Grocery list review" and "Buy groceries")
- [ ] T067 Test empty search results with appropriate message
- [ ] T068 Acceptance test: Search for "grocery" in list with 3 tasks, verify 2 matches returned
- [ ] T069 Acceptance test: Search case-insensitive, uppercase keyword matches lowercase title
- [ ] T070 Acceptance test: Search special characters, system handles gracefully

**Checkpoint**: User Story 3 fully functional. Users can now search for tasks independently.

---

## Phase 6: User Story 4 - Filter Tasks by Multiple Criteria (Priority: P2)

**Goal**: Enable users to combine multiple filters (status, priority, category)
**Independent Test**: Create diverse tasks, apply multiple filters, verify AND logic
**User Story Acceptance**: All 5 acceptance scenarios from spec.md passing

### Data Model for User Story 4

- [ ] T071 [P] Unit test file `tests/unit/test_filter_service.py` with test cases for multi-criteria filtering

### Implementation for User Story 4

- [ ] T072 [P] Create FilterService class in `src/services/filter_service.py` with method: `filter_tasks()` accepting multiple filter criteria with AND logic
- [ ] T073 Implement AND logic: task must match ALL specified filters to be returned
- [ ] T074 Extend TaskService with multi-filter integration: `filter_tasks(status=None, priority=None, category=None)`

### CLI Implementation for User Story 4

- [ ] T075 Update `src/cli/commands/list.py` to accept multiple --filter-* flags simultaneously
- [ ] T076 Add multi-filter examples to CLI help text

### Integration for User Story 4

- [ ] T077 [P] Integrate FilterService into TaskService for combined filtering
- [ ] T078 Update list command to apply all specified filters with AND logic
- [ ] T079 Test single filter (status, priority, or category) works independently
- [ ] T080 Test combining two filters (status AND priority)
- [ ] T081 Test combining three filters (status AND priority AND category)
- [ ] T082 Test empty results with appropriate message when no tasks match all filters
- [ ] T083 Acceptance test: Apply 3 filters, verify only tasks matching all criteria returned
- [ ] T084 Acceptance test: Clear one filter, verify results update to match remaining filters

**Checkpoint**: User Story 4 fully functional. Users can combine filters with AND logic.

---

## Phase 7: User Story 5 - Sort Tasks by Various Criteria (Priority: P2)

**Goal**: Enable users to sort tasks by priority, due date, or title
**Independent Test**: Create tasks with different values, sort by each criterion, verify order
**User Story Acceptance**: All 5 acceptance scenarios from spec.md passing

### Data Model for User Story 5

- [ ] T085 [P] Unit test file `tests/unit/test_sort_service.py` with test cases for sorting operations

### Implementation for User Story 5

- [ ] T086 [P] Create SortService class in `src/services/sort_service.py` with method: `sort_tasks()` supporting priority, due_date, title sorting with ASC/DESC
- [ ] T087 Implement priority sorting (high > medium > low)
- [ ] T088 Implement due_date sorting with null handling (null values at end)
- [ ] T089 Implement title sorting (alphabetical, case-insensitive)
- [ ] T090 Extend TaskService with sort integration: `sort_tasks(sort_by, sort_order='ASC')`

### CLI Implementation for User Story 5

- [ ] T091 Update `src/cli/commands/list.py` to support --sort-by {PRIORITY,DUE_DATE,TITLE} and --sort-order {ASC,DESC}
- [ ] T092 Add sort help text and examples to CLI

### Integration for User Story 5

- [ ] T093 [P] Integrate SortService into TaskService for sorting operations
- [ ] T094 Update list command to call SortService.sort_tasks() when --sort-by is specified
- [ ] T095 Test sort by priority (high, medium, low order)
- [ ] T096 Test sort by title (alphabetical order, case-insensitive)
- [ ] T097 Test sort by due_date with null dates at end
- [ ] T098 Test ASC and DESC ordering
- [ ] T099 Acceptance test: Sort by priority high-to-low, verify order high→medium→low
- [ ] T100 Acceptance test: Sort by title A-Z, verify alphabetical order

**Checkpoint**: User Story 5 fully functional. Users can sort by multiple criteria.

---

## Phase 8: User Story 6 - Set Due Dates with Validation (Priority: P3)

**Goal**: Enable users to assign optional due dates with validation and overdue detection
**Independent Test**: Create tasks with due dates, check overdue indicators, verify validation
**User Story Acceptance**: All 6 acceptance scenarios from spec.md passing

### Data Model for User Story 6

- [ ] T101 [P] Unit test file `tests/unit/test_date_service.py` with test cases for date validation and overdue detection

### Implementation for User Story 6

- [ ] T102 [P] Create DateService class in `src/services/date_service.py` with methods:
  - `validate_date_format()` - validate YYYY-MM-DD format
  - `validate_calendar_date()` - validate calendar date exists (handle leap years)
  - `check_overdue()` - return True if date < today
- [ ] T103 Add date parsing and validation to Task model
- [ ] T104 Implement `is_overdue` computed property in Task model
- [ ] T105 Extend TaskService with due date operations: `set_task_due_date(task_id, due_date_str)`
- [ ] T106 Update CLI formatters to display overdue indicator for overdue tasks

### CLI Implementation for User Story 6

- [ ] T107 Update `src/cli/commands/add.py` to support --due-date YYYY-MM-DD flag
- [ ] T108 Update `src/cli/commands/update.py` to support --due-date YYYY-MM-DD flag for modification/removal
- [ ] T109 Add date validation error messages to CLI output
- [ ] T110 Add due date help text and examples to CLI

### Integration for User Story 6

- [ ] T111 [P] Integrate DateService into TaskService for validation
- [ ] T112 Update list command to display overdue indicator in task display
- [ ] T113 Update sort command to support --sort-by DUE_DATE with proper null handling
- [ ] T114 Test date format validation (reject invalid formats with error message)
- [ ] T115 Test calendar date validation (reject Feb 30, etc.)
- [ ] T116 Test overdue detection (task with past due_date shows overdue indicator)
- [ ] T117 Test null due_date handling (optional field works)
- [ ] T118 Acceptance test: Create task with due date 2025-12-31, verify stored correctly
- [ ] T119 Acceptance test: Create task with due date in past, verify marked overdue
- [ ] T120 Acceptance test: Set invalid date, verify rejected with error message

**Checkpoint**: User Story 6 fully functional. Users can manage task due dates with validation.

---

## Phase 9: User Story 7 - Create Recurring Tasks (Priority: P3)

**Goal**: Enable users to create recurring tasks that auto-generate new instances on completion
**Independent Test**: Create daily recurring task, mark complete, verify new instance created
**User Story Acceptance**: All 8 acceptance scenarios from spec.md passing

### Data Model for User Story 7

- [ ] T121 [P] Unit test file `tests/unit/test_recurrence_service.py` with test cases for recurrence operations (validation, generation, month-end handling)

### Implementation for User Story 7

- [ ] T122 [P] Create RecurrenceService class in `src/services/recurrence_service.py` with methods:
  - `validate_recurrence()` - validate enum {daily, weekly, monthly}
  - `generate_next_instance()` - create new task with incremented due_date
  - `calculate_next_due_date()` - handle month-end edge cases
- [ ] T123 Add recurrence pattern support to Task model
- [ ] T124 Implement month-end edge case handling for monthly recurrence (Jan 31 + 1 month = Feb 28/29)
- [ ] T125 Implement parent_recurrence_id tracking in Task model
- [ ] T126 Extend TaskService with recurrence operations: `get_next_recurrence_date()`, `generate_next_recurring_instance()`

### CLI Implementation for User Story 7

- [ ] T127 Update `src/cli/commands/add.py` to support --recurrence {DAILY,WEEKLY,MONTHLY}
- [ ] T128 Update `src/cli/commands/complete.py` to trigger recurrence generation when completing recurring task
- [ ] T129 Update CLI formatters to display next recurrence date for recurring tasks
- [ ] T130 Add recurrence help text and examples to CLI

### Integration for User Story 7

- [ ] T131 [P] Integrate RecurrenceService into TaskService for recurrence operations
- [ ] T132 Update complete command to check if task has recurrence, generate next instance if needed
- [ ] T133 Update display/list to show next recurrence date and parent task reference
- [ ] T134 Test daily recurrence (create task, mark complete, verify next day's instance created)
- [ ] T135 Test weekly recurrence (+7 days)
- [ ] T136 Test monthly recurrence with month-end handling (Jan 31 → Feb 28/29)
- [ ] T137 Test leap year handling (Feb 29 exists in leap years)
- [ ] T138 Test recurrence with due_date (subsequent instances calculate new due dates)
- [ ] T139 Test recurrence with priority/category (inherited by new instances)
- [ ] T140 Acceptance test: Create daily standup, mark complete, verify new instance created for tomorrow
- [ ] T141 Acceptance test: Create monthly task on 31st, complete it, verify next instance on last day of next month
- [ ] T142 Acceptance test: Update recurring task title, verify new instances have new title but old instances unaffected

**Checkpoint**: User Story 7 fully functional. Users can create and manage recurring tasks. All 7 user stories now complete!

---

## Phase 10: Integration & Cross-Feature Testing

**Purpose**: Verify features work correctly in combination
**Dependency**: All user stories (Phases 3-9) complete
**Acceptance**: All integration scenarios pass, no feature conflicts

### Integration Tests

- [ ] T143 Create `tests/integration/test_task_workflows.py` with end-to-end task creation, update, filtering, deletion flows
- [ ] T144 Create `tests/integration/test_filtering_combinations.py` with multi-filter scenarios (priority + category + status, etc.)
- [ ] T145 Create `tests/integration/test_search_workflows.py` with search + filter + sort combinations
- [ ] T146 Create `tests/integration/test_recurring_workflows.py` with recurring task completion and generation
- [ ] T147 Create `tests/integration/test_date_workflows.py` with due date, overdue, and recurrence date combinations

### Acceptance Tests (User Story Scenarios)

- [ ] T148 [P] Create `tests/acceptance/test_user_story_1.py` with all 5 acceptance scenarios for priority
- [ ] T149 [P] Create `tests/acceptance/test_user_story_2.py` with all 6 acceptance scenarios for category
- [ ] T150 [P] Create `tests/acceptance/test_user_story_3.py` with all 5 acceptance scenarios for search
- [ ] T151 [P] Create `tests/acceptance/test_user_story_4.py` with all 5 acceptance scenarios for multi-filter
- [ ] T152 [P] Create `tests/acceptance/test_user_story_5.py` with all 5 acceptance scenarios for sort
- [ ] T153 [P] Create `tests/acceptance/test_user_story_6.py` with all 6 acceptance scenarios for due dates
- [ ] T154 [P] Create `tests/acceptance/test_user_story_7.py` with all 8 acceptance scenarios for recurring tasks

### Edge Case Tests

- [ ] T155 Create `tests/unit/test_edge_cases.py` with all 8 edge cases from spec:
  - Very long strings (255 char title, 50 char category)
  - Large task counts (1000+ items in memory)
  - Month-end dates (Jan 31, Feb 28/29, etc.)
  - Leap year handling
  - Null/empty value handling
  - Special characters
  - Concurrent operations (if applicable)
  - Filter combinations with no matches

### Performance Tests

- [ ] T156 Create `tests/unit/test_performance.py` with performance baselines:
  - List/filter 100 tasks: <500ms
  - Search 1000 items: <100ms
  - Multi-filter 3 criteria: <200ms
  - Sort 1000 items: <300ms

### Error Message & Help Text Validation

- [ ] T157 Validate all error messages match specification format (icon + what went wrong + how to fix)
- [ ] T158 Validate help text for all commands (`--help` output matches specification)
- [ ] T159 Validate all error paths (invalid input, missing args, invalid enum values)

### CLI Integration

- [ ] T160 Test full CLI workflow: add → list → filter → update → complete → delete
- [ ] T161 Test filter + sort combinations (filter priority + sort by due date)
- [ ] T162 Test search + filter + sort together
- [ ] T163 Test recurring task workflow: create → complete → verify new instance → complete again
- [ ] T164 Test backward compatibility with basic tasks (tasks created before intermediate features work correctly)

**Checkpoint**: All features integrated and tested. System ready for polish phase.

---

## Phase 11: Polish & Code Quality

**Purpose**: Code cleanup, documentation, quality improvements
**Dependency**: All integration tests passing
**Acceptance**: >90% code coverage, SOLID verified, documentation complete

### Code Quality

- [ ] T165 [P] Refactor duplicate code in services into shared utilities module `src/utils/`
- [ ] T166 [P] Add docstrings to all public methods and classes
- [ ] T167 [P] Review SOLID principle compliance in all services
- [ ] T168 Add type hints to all functions and methods (Python 3.13 features)
- [ ] T169 Run linting and formatting across all source files
- [ ] T170 Refactor error handling for consistency across all services

### Test Coverage

- [ ] T171 [P] Verify >90% code coverage for all services (pytest --cov)
- [ ] T172 [P] Add missing unit tests for edge cases and error paths
- [ ] T173 Remove redundant test cases if coverage >95%

### Documentation

- [ ] T174 Create `specs/1-phase-1-todo-app/quickstart.md` with setup instructions and first development task
- [ ] T175 Create `docs/API.md` documenting all service methods and contracts
- [ ] T176 Create `docs/ARCHITECTURE.md` explaining service layer design and SOLID principles
- [ ] T177 Create `docs/TESTING.md` with test strategy and how to run tests
- [ ] T178 Create `docs/TROUBLESHOOTING.md` with common issues and solutions
- [ ] T179 Update `README.md` with feature overview, setup, and usage examples

### Validation

- [ ] T180 Run full test suite and verify all tests passing
- [ ] T181 Verify all 35 acceptance scenarios passing via CLI
- [ ] T182 Run performance tests and verify all goals met (SC-001 through SC-010)
- [ ] T183 Verify backward compatibility (basic tasks work without modification)
- [ ] T184 Run quickstart.md validation to ensure setup instructions work
- [ ] T185 Validate all requirements (53 FR) implemented with green tests

**Checkpoint**: Code quality high, documentation complete, all tests passing. Ready for Phase II!

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all stories)
    ↓
┌───────────────────────────────────────┐
│ User Stories 1-7 (can run in parallel) │
├───────────────────────────────────────┤
│ Phase 3: US1 Priority                 │
│ Phase 4: US2 Category (P1)            │
│ Phase 5: US3 Search  (P2)             │
│ Phase 6: US4 Multi-Filter (P2)        │
│ Phase 7: US5 Sort    (P2)             │
│ Phase 8: US6 Due Dates (P3)           │
│ Phase 9: US7 Recurring (P3)           │
└───────────────────────────────────────┘
    ↓
Phase 10: Integration & Testing
    ↓
Phase 11: Polish & Quality
```

### Within Each User Story Phase

1. Data model (if new entity)
2. Service implementation
3. CLI implementation
4. Integration with existing features
5. Tests (if written)

### Parallel Opportunities

**Phase 1 (Setup)**:
- All T002-T006 marked [P] can run in parallel

**Phase 2 (Foundational)**:
- T009-T010 (enumerations, validators) marked [P]
- T013-T014 (Task properties) marked [P]
- T019-T021 (test files) marked [P]

**Phase 3-9 (User Stories)**:
- Once Phase 2 complete, all user stories can start in parallel
- Within each story, T0XX tasks marked [P] can run in parallel
- Example: T024, T025 (services) can run together
- Different team members can work on different stories

**Phase 10 (Integration)**:
- T143-T154 test files marked [P] can be written in parallel
- Each story's acceptance test file independent

**Example Parallel Execution**:
```
Developer A: Phase 3 (US1 Priority)
Developer B: Phase 4 (US2 Category)
Developer C: Phase 5 (US3 Search)
  + Phase 6 (US4 Filter) after US3 complete
Developer D: Phase 8 (US6 Due Dates)
All developers: Phase 10 (Integration)
Team lead: Phase 11 (Polish & Quality)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

Suggested approach for fastest MVP:

1. **Complete Phase 1**: Project setup (T001-T008) - ~1 hour
2. **Complete Phase 2**: Foundational infrastructure (T009-T021) - ~3 hours
3. **Complete Phase 3**: User Story 1 Priority (T022-T039) - ~4 hours
4. **Complete Phase 4**: User Story 2 Category (T040-T056) - ~3 hours
5. **STOP and VALIDATE**: Test independently via CLI - ~30 min
   - Users can organize tasks by priority and category
   - Ready to demo/deploy

**MVP Total**: ~12 hours for functional priority+category system

### Full Implementation (All 7 Stories)

1. Complete MVP (above)
2. Add Phase 5: User Story 3 Search - ~3 hours
3. Add Phase 6: User Story 4 Multi-Filter - ~2 hours
4. Add Phase 7: User Story 5 Sort - ~2 hours
5. Add Phase 8: User Story 6 Due Dates - ~4 hours
6. Add Phase 9: User Story 7 Recurring - ~5 hours
7. Phase 10: Integration & Testing - ~5 hours
8. Phase 11: Polish & Quality - ~3 hours

**Full Implementation Total**: ~36 hours

### Incremental Delivery Checklist

- [ ] **Milestone 1**: Phase 1 + 2 (Foundation ready)
- [ ] **Milestone 2**: +Phase 3-4 (Priority & Category MVP)
- [ ] **Milestone 3**: +Phase 5-7 (Search, Filter, Sort)
- [ ] **Milestone 4**: +Phase 8-9 (Due Dates & Recurring)
- [ ] **Milestone 5**: +Phase 10-11 (Integration & Polish)

---

## Task Checklist Notes

- [P] = parallelizable (can run concurrently with same-phase tasks)
- [StoryX] = belongs to specific user story (US1, US2, etc.)
- Each task has exact file path for clarity
- Tasks organized for independent testing at each checkpoint
- Acceptance tests verify user story acceptance scenarios
- Integration tests verify feature combinations work
- Polish phase ensures code quality and documentation

---

## Summary

**Total Tasks**: 185 tasks across 11 phases
**Setup Phase**: 8 tasks (Phase 1)
**Foundational Phase**: 13 tasks (Phase 2)
**User Story Phases**: 140+ tasks (Phases 3-9)
  - US1 Priority: 18 tasks
  - US2 Category: 17 tasks
  - US3 Search: 14 tasks
  - US4 Multi-Filter: 14 tasks
  - US5 Sort: 16 tasks
  - US6 Due Dates: 20 tasks
  - US7 Recurring: 22 tasks
**Integration Phase**: 22 tasks (Phase 10)
**Polish Phase**: 21 tasks (Phase 11)

**Parallel Opportunities**: 35+ tasks can run in parallel
**Independent Checkpoints**: 9 checkpoints (after each phase)
**Estimated Duration**: 12-36 hours depending on parallelization
**MVP Scope**: US1 + US2 (12 hours, ready to demo)

