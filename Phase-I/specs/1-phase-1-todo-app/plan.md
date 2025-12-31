# Implementation Plan: Phase 1 Todo App - Intermediate and Advanced Features

**Branch**: `1-phase-1-todo-app` | **Date**: 2025-12-30 | **Spec**: [specs/1-phase-1-todo-app/spec.md](spec.md)
**Input**: Feature specification from `/specs/1-phase-1-todo-app/spec.md`

---

## Summary

Implement intermediate and advanced features for CLI-based Python todo application:
- **Intermediate**: Priority/Category management, Search/Filter/Sort capabilities
- **Advanced**: Due date validation, Recurring task engine with auto-generation
- **Architecture**: Clean, testable, SOLID-compliant design with separation of concerns
- **Approach**: Incremental, spec-driven development with independent feature testability

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (Phase I constraint)
**Storage**: In-memory Python collections (list/dict, no database)
**Testing**: pytest (standard library + built-in test patterns)
**Target Platform**: CLI (cross-platform: Linux, macOS, Windows)
**Project Type**: Single CLI application (console-only)
**Performance Goals**:
- List/filter operations: <500ms for 100+ tasks
- Search operations: <100ms for 1000 items
- Multi-filter operations: <200ms
**Constraints**:
- No external database (in-memory only)
- No GUI (CLI-only)
- Backward compatible with Basic features
- Pure Python 3.13 (standard library)
**Scale/Scope**:
- Minimum 1000 tasks in-memory
- Multiple priority/category filtering
- 53 functional requirements
- 35 acceptance scenarios

---

## Constitution Check

**Status**: ✅ PASS - No violations detected

**Verification**:
- ✅ Spec-First Development: Specification completed before planning
- ✅ No Manual Coding: Plan-driven, no ad-hoc code generation
- ✅ Mandatory Tooling: Using Python 3.13+, UV (project setup)
- ✅ Clean Architecture: Service layer separation documented
- ✅ SOLID Principles: Single Responsibility, Open/Closed enforced in design
- ✅ Testable Design: Acceptance scenarios and edge cases defined
- ✅ In-Memory Storage: No external dependencies for Phase I
- ✅ Extensible Design: Contract-based interfaces allow future persistence layer

**Constitution Reference**: `.specify/memory/constitution.md`
- Phase I scope: ✅ Matches (in-memory Python console app)
- Technology stack: ✅ Compliant (Python 3.13+, standard library)
- Feature levels: ✅ Correct (Basic already exists, now Intermediate+Advanced)

---

## Project Structure

### Documentation (this feature)

```
specs/1-phase-1-todo-app/
├── spec.md                          # Feature specification (completed)
├── plan.md                          # This file (implementation plan)
├── research.md                      # Phase 0: Research findings (TBD)
├── data-model.md                    # Phase 1: Data entities and validation (TBD)
├── quickstart.md                    # Phase 1: Developer quickstart guide (TBD)
├── contracts/                       # Phase 1: API/Service contracts (TBD)
│   ├── data_model.md               # Task entity contract
│   ├── priority_service.md         # Priority operations contract
│   ├── category_service.md         # Category operations contract
│   ├── search_filter_service.md    # Search/filter/sort contract
│   ├── date_service.md             # Due date operations contract
│   └── recurrence_service.md       # Recurring task engine contract
├── checklists/
│   └── requirements.md              # Quality checklist (completed)
└── tasks.md                         # Phase 2: Actionable tasks (TBD, /sp.tasks)
```

### Source Code Structure (repository root)

```
src/
├── models/
│   ├── task.py                     # Task entity with validation
│   ├── enums.py                    # Priority, Status, Recurrence enums
│   └── validators.py               # Validation logic
│
├── services/
│   ├── task_service.py             # Core task operations
│   ├── priority_service.py         # Priority management logic
│   ├── category_service.py         # Category management logic
│   ├── search_service.py           # Search implementation
│   ├── filter_service.py           # Filter implementation
│   ├── sort_service.py             # Sort implementation
│   ├── date_service.py             # Due date validation and utilities
│   ├── recurrence_service.py       # Recurring task engine
│   └── storage.py                  # In-memory task storage
│
├── cli/
│   ├── main.py                     # CLI entry point
│   ├── commands/
│   │   ├── add.py                  # Create task command
│   │   ├── update.py               # Update task command
│   │   ├── delete.py               # Delete task command
│   │   ├── view.py                 # View tasks command
│   │   ├── list.py                 # List with filters/sort command
│   │   ├── complete.py             # Mark complete command
│   │   └── search.py               # Search tasks command
│   └── formatters.py               # Output formatting

tests/
├── unit/
│   ├── test_task_model.py          # Task entity tests
│   ├── test_validators.py          # Validation tests
│   ├── test_priority_service.py    # Priority logic tests
│   ├── test_category_service.py    # Category logic tests
│   ├── test_search_service.py      # Search tests
│   ├── test_filter_service.py      # Filter tests
│   ├── test_sort_service.py        # Sort tests
│   ├── test_date_service.py        # Date validation tests
│   ├── test_recurrence_service.py  # Recurring task tests
│   └── test_storage.py             # Storage tests
│
├── integration/
│   ├── test_task_workflows.py      # End-to-end task flows
│   ├── test_filtering_combinations.py # Multi-filter scenarios
│   ├── test_search_workflows.py    # Search+filter combinations
│   ├── test_recurring_workflows.py # Recurring task flows
│   └── test_date_workflows.py      # Date-based workflows
│
└── acceptance/
    ├── test_user_story_1.py        # Priority management scenarios
    ├── test_user_story_2.py        # Category management scenarios
    ├── test_user_story_3.py        # Search scenarios
    ├── test_user_story_4.py        # Multi-filter scenarios
    ├── test_user_story_5.py        # Sorting scenarios
    ├── test_user_story_6.py        # Due date scenarios
    └── test_user_story_7.py        # Recurring task scenarios
```

**Structure Decision**: Single CLI project with clean separation between models (data), services (business logic), and CLI (user interface). Tests organized by type (unit, integration, acceptance) to support independent feature validation.

---

## Implementation Phases

### Phase 0: Research & Clarifications *(Parallel with Phase 1)*

**Objective**: Resolve any technical uncertainties before beginning implementation

**Research Tasks**:
1. **Python datetime handling**: Best practices for date validation and comparison
2. **In-memory data structure patterns**: Optimal collections for task storage with filtering/sorting
3. **CLI patterns**: Standard argument parsing and error handling conventions
4. **Recurrence calculation**: Edge cases for monthly recurrence (month-end handling)
5. **SOLID principles**: Concrete patterns for service layer design in Python

**Responsibilities**:
- Identify optimal Python patterns for in-memory filtering/sorting
- Validate month-end edge case handling strategy (Jan 31 + 1 month = Feb 28/29)
- Confirm CLI argument parsing approach (argparse vs custom)

**Inputs**:
- Feature specification
- Constitution requirements (Python 3.13+, standard library)

**Outputs**:
- `research.md` with decisions and rationale
- Confirmed design patterns for each service
- Resolved edge case handling strategies

**Risks**:
- Month-end recurrence logic complexity higher than estimated
- Performance impact of filtering/sorting on large in-memory collections

**Completion Criteria**:
- All research tasks completed and documented
- No "NEEDS CLARIFICATION" markers remain
- Design patterns confirmed with rationale

---

### Phase 1: Data Model & Service Contracts *(Foundation)*

**Objective**: Define the data model, service contracts, and architectural boundaries

**Phase 1.1: Data Model**

**Responsibilities**:
- Extend Task entity with new fields: priority, category, due_date, recurrence
- Define validation rules for each field
- Define enums for priority, status, recurrence
- Plan backward compatibility strategy

**Inputs**:
- Feature specification (Task entity definition)
- Acceptance scenarios (validation requirements)
- Research findings

**Outputs**:
- `data-model.md` with Task entity schema
- Validation rules document
- Enum definitions
- `models/task.py` structure plan

**Acceptance Criteria**:
- Task entity includes all 6 new fields with proper types
- Validation rules for each field documented
- Backward compatibility plan for Basic feature tasks documented
- Default values specified (priority="medium", category=null, etc.)

---

**Phase 1.2: Service Contracts**

**Responsibilities**:
- Define service layer boundaries (TaskService, PriorityService, etc.)
- Specify service method signatures and responsibilities
- Define error handling contracts
- Plan data flow between services

**Inputs**:
- Functional requirements (FR-001 through FR-053)
- Feature specification
- Data model from Phase 1.1

**Outputs**:
- `contracts/task_service.md`: Core task CRUD operations
- `contracts/priority_service.md`: Priority management
- `contracts/category_service.md`: Category management
- `contracts/search_filter_service.md`: Search/filter/sort logic
- `contracts/date_service.md`: Date validation and utilities
- `contracts/recurrence_service.md`: Recurring task engine

**Acceptance Criteria**:
- Each contract specifies input/output types (no implementation)
- Error cases defined (validation errors, edge cases)
- Service responsibilities clearly separated
- Testable method signatures defined

---

**Phase 1.3: CLI Command Contracts**

**Responsibilities**:
- Define new CLI flags and command structures
- Specify input validation at CLI boundary
- Plan output formatting for new features
- Document help text and examples

**Inputs**:
- Functional requirements (FR-042 through FR-053)
- CLI command specification from spec.md
- User stories (for UX guidance)

**Outputs**:
- `contracts/cli_commands.md` with all flag definitions
- Example command usage for each feature
- Output format specifications

**Acceptance Criteria**:
- All new flags documented (--priority, --category, --search, etc.)
- Input validation rules specified
- Output examples for each feature provided
- Help text templates included

---

**Phase 1.4: Quickstart & Architecture Guide**

**Responsibilities**:
- Document development setup instructions
- Explain architecture and design decisions
- Provide implementation guidance for each service

**Inputs**:
- All Phase 1 outputs above
- Constitution guidelines
- Spec-driven development principles

**Outputs**:
- `quickstart.md` with setup and first development step
- `architecture.md` explaining service layer design
- Debugging and testing guidance

**Acceptance Criteria**:
- New developer can understand architecture in <15 minutes
- Setup instructions clear and reproducible
- Each service's responsibility clearly explained
- References to specific contracts provided

---

### Phase 2: Priority & Category Features *(P1 - Foundation)*

**Objective**: Implement task prioritization and categorization (foundation for other features)

**Phase 2.1: Data Model Implementation**

**Responsibilities**:
- Implement Task class with priority and category fields
- Implement validation for priority enum {high, medium, low}
- Implement validation for category string (max 50 chars, optional)
- Implement default value for priority (medium)

**Inputs**:
- Task entity schema from Phase 1
- Validation rules from Phase 1
- User Story 1 and 2 acceptance scenarios

**Outputs**:
- `src/models/task.py` with Task class
- `src/models/enums.py` with Priority, Status, Recurrence enums
- `src/models/validators.py` with validation functions

**Risks**:
- Task serialization/deserialization complexity
- Backward compatibility with existing Basic tasks

**Completion Criteria**:
- Task entity passes all User Story 1 & 2 acceptance scenarios
- Validation rejects invalid priority values
- Category validation enforces length constraints
- Default priority applied correctly
- Unit tests for all validations passing (100% coverage)

---

**Phase 2.2: Priority Service Implementation**

**Responsibilities**:
- Implement priority-related operations (set, get, filter)
- Implement priority-based sorting
- Implement validation integration

**Inputs**:
- Priority service contract from Phase 1
- Task model from Phase 2.1
- Acceptance scenarios

**Outputs**:
- `src/services/priority_service.py`
- Unit tests in `tests/unit/test_priority_service.py`

**Completion Criteria**:
- All priority-related FR requirements implemented (FR-001-007)
- Filtering by priority returns correct subset
- Sorting by priority orders correctly (high → medium → low)
- Error cases handled with appropriate messages

---

**Phase 2.3: Category Service Implementation**

**Responsibilities**:
- Implement category operations (set, get, filter)
- Implement category filtering
- Handle special characters and edge cases

**Inputs**:
- Category service contract from Phase 1
- Task model from Phase 2.1
- Acceptance scenarios

**Outputs**:
- `src/services/category_service.py`
- Unit tests in `tests/unit/test_category_service.py`

**Completion Criteria**:
- All category-related FR requirements implemented (FR-002, FR-004, FR-005, FR-007)
- Filtering by category returns correct subset
- Special characters handled gracefully
- Optional category handling works correctly

---

**Phase 2.4: CLI Command Updates for Priority & Category**

**Responsibilities**:
- Add --priority flag to add/update commands
- Add --category flag to add/update commands
- Implement input validation at CLI boundary
- Update help text and examples

**Inputs**:
- CLI contracts from Phase 1
- Priority and Category services from Phase 2.2-2.3
- Feature specification

**Outputs**:
- Updated `src/cli/commands/add.py` (with --priority, --category)
- Updated `src/cli/commands/update.py` (with --priority, --category)
- Updated help text and examples

**Completion Criteria**:
- `todo add "Task" --priority HIGH --category work` works
- `todo update task-001 --priority MEDIUM` works
- Invalid priority rejected with clear error message
- Category length validation enforced at CLI

---

### Phase 3: Search, Filter, and Sort Features *(P2 - Discovery)*

**Objective**: Enable efficient task discovery through search, filtering, and sorting

**Phase 3.1: Search Service Implementation**

**Responsibilities**:
- Implement keyword search (case-insensitive)
- Implement partial matching
- Implement search across title and description
- Handle special characters gracefully

**Inputs**:
- Search service contract from Phase 1
- Task model with fields
- User Story 3 acceptance scenarios

**Outputs**:
- `src/services/search_service.py`
- Unit tests in `tests/unit/test_search_service.py`

**Completion Criteria**:
- Case-insensitive search implemented
- Partial matching works ("grocery" matches "Grocery list")
- Special character handling graceful
- Performance <100ms for 1000-item list

---

**Phase 3.2: Filter Service Implementation**

**Responsibilities**:
- Implement status filtering (complete/incomplete)
- Implement priority filtering
- Implement category filtering
- Implement AND logic for combined filters

**Inputs**:
- Filter service contract from Phase 1
- Task model with all fields
- User Story 4 acceptance scenarios

**Outputs**:
- `src/services/filter_service.py`
- Unit tests in `tests/unit/test_filter_service.py`

**Completion Criteria**:
- Single and combined filters work correctly
- AND logic enforced (all criteria must match)
- Empty results handled gracefully
- Performance <200ms for 3+ combined filters

---

**Phase 3.3: Sort Service Implementation**

**Responsibilities**:
- Implement priority-based sorting
- Implement due-date sorting (with null handling)
- Implement title alphabetic sorting
- Implement ASC/DESC order

**Inputs**:
- Sort service contract from Phase 1
- Task model with all fields
- User Story 5 acceptance scenarios

**Outputs**:
- `src/services/sort_service.py`
- Unit tests in `tests/unit/test_sort_service.py`

**Completion Criteria**:
- Sorting by priority orders high → medium → low
- Null due dates placed at end
- Alphabetic sorting works (case-insensitive)
- ASC/DESC ordering works correctly

---

**Phase 3.4: CLI Updates for Search, Filter, Sort**

**Responsibilities**:
- Add --search flag to list command
- Add --filter-status, --filter-priority, --filter-category flags
- Add --sort-by and --sort-order flags
- Implement composable flag handling

**Inputs**:
- CLI contracts from Phase 1
- Search, Filter, Sort services from Phase 3.1-3.3
- Feature specification

**Outputs**:
- Updated `src/cli/commands/list.py`
- Help text with examples for all new flags

**Completion Criteria**:
- `todo list --search keyword` returns matching tasks
- `todo list --filter-priority HIGH --filter-category work` works
- `todo list --sort-by DUE_DATE --sort-order ASC` works
- Combining flags works (search + multiple filters + sort)

---

### Phase 4: Due Dates & Recurring Tasks *(P3 - Advanced)*

**Objective**: Implement time-based task management with automation

**Phase 4.1: Date Service Implementation**

**Responsibilities**:
- Implement date format validation (YYYY-MM-DD)
- Implement calendar date validation
- Implement overdue detection
- Implement timezone handling (local timezone)

**Inputs**:
- Date service contract from Phase 1
- User Story 6 acceptance scenarios
- Research findings on date handling

**Outputs**:
- `src/services/date_service.py`
- Unit tests in `tests/unit/test_date_service.py`

**Risks**:
- Timezone edge cases
- Leap year handling

**Completion Criteria**:
- Date format validation catches invalid formats
- Calendar validation rejects invalid dates (e.g., 2025-02-30)
- Overdue detection works correctly (current_date > due_date)
- All date-related FR requirements implemented (FR-021-027)
- Edge cases pass (leap years, month boundaries)

---

**Phase 4.2: Recurrence Service Implementation**

**Responsibilities**:
- Implement recurrence pattern validation (daily, weekly, monthly)
- Implement new instance generation on completion
- Implement due date calculation for next instance
- Implement month-end edge case handling
- Implement independent instance tracking

**Inputs**:
- Recurrence service contract from Phase 1
- User Story 7 acceptance scenarios
- Research findings on month-end edge cases

**Outputs**:
- `src/services/recurrence_service.py`
- Unit tests in `tests/unit/test_recurrence_service.py`

**Risks**:
- Month-end calculation complexity (Jan 31 + 1 month)
- Large volume recurrence performance (100+ daily tasks)

**Completion Criteria**:
- Daily recurrence generates next task for tomorrow
- Weekly recurrence generates next task +7 days
- Monthly recurrence handles month-end (Jan 31 → Feb 28/29)
- New instances created immediately on completion
- All recurrence FR requirements implemented (FR-028-037)
- Performance acceptable for 100+ recurring tasks

---

**Phase 4.3: CLI Updates for Due Dates & Recurrence**

**Responsibilities**:
- Add --due-date flag to add/update commands
- Add --recurrence flag to add command
- Display overdue indicator in list output
- Display next recurrence date in task details

**Inputs**:
- Date and Recurrence services from Phase 4.1-4.2
- CLI contracts from Phase 1
- Feature specification

**Outputs**:
- Updated `src/cli/commands/add.py` (with --due-date, --recurrence)
- Updated `src/cli/commands/update.py` (with --due-date)
- Updated `src/cli/formatters.py` (overdue indicator, next recurrence display)
- Updated `src/cli/commands/complete.py` (trigger recurrence generation)

**Completion Criteria**:
- `todo add "Task" --due-date 2025-12-31` works
- `todo add "Daily standup" --recurrence DAILY` works
- Overdue tasks display with clear indicator
- Next recurrence date displayed for recurring tasks
- Completing recurring task auto-generates next instance

---

### Phase 5: Integration & Cross-Feature Testing *(Validation)*

**Objective**: Verify all features work correctly individually and in combination

**Phase 5.1: Integration Test Suite**

**Responsibilities**:
- Test feature interactions (priority + due date, filter + sort, etc.)
- Test multi-filter scenarios
- Test search + filter + sort combinations
- Test recurring task with priority/category/due date

**Inputs**:
- All service implementations from Phases 2-4
- Feature specification acceptance scenarios
- Edge case definitions

**Outputs**:
- `tests/integration/` test suite (40+ integration tests)
- Integration test report

**Completion Criteria**:
- All feature combinations tested
- No conflicts between features
- Performance remains <200ms for complex operations
- All edge cases pass

---

**Phase 5.2: Acceptance Test Suite**

**Responsibilities**:
- Test each user story scenario end-to-end via CLI
- Validate all 35 acceptance scenarios
- Test error paths and error messages
- Validate help text and examples

**Inputs**:
- All user stories (1-7) from specification
- Acceptance scenarios (35 total)
- CLI implementation

**Outputs**:
- `tests/acceptance/` test suite (one test file per user story)
- Acceptance test report (35/35 scenarios passing)

**Completion Criteria**:
- All 35 acceptance scenarios passing via CLI
- Error messages match specification
- No manual intervention required to run tests
- Documentation accurate and examples work

---

**Phase 5.3: Edge Case & Boundary Testing**

**Responsibilities**:
- Test boundary conditions (very long strings, large counts, etc.)
- Test edge cases (month-end recurrence, leap years, etc.)
- Test null/empty value handling
- Test concurrent operations (if applicable)

**Inputs**:
- Edge case definitions from specification (8 cases)
- Boundary condition requirements (SC-005)
- Error handling specifications

**Outputs**:
- `tests/unit/test_edge_cases.py` (comprehensive edge case coverage)
- Edge case test report

**Completion Criteria**:
- All 8 identified edge cases tested and passing
- Boundary conditions validated
- System behavior consistent for all null/empty cases

---

**Phase 5.4: Performance Validation**

**Responsibilities**:
- Verify performance goals met (SC-001, SC-002, SC-003)
- Profile filtering/sorting operations
- Test with 1000+ tasks
- Document performance baseline

**Inputs**:
- Performance goals from specification
- All service implementations
- Integration tests

**Outputs**:
- Performance test results
- Baseline metrics document
- Optimization recommendations if needed

**Completion Criteria**:
- List/filter <500ms for 100+ tasks ✅
- Search <100ms for 1000 items ✅
- Multi-filter <200ms ✅
- No significant regressions from basic features

---

### Phase 6: Refactoring & Clean Architecture *(Polish)*

**Objective**: Ensure code maintainability, consistency, and adherence to SOLID principles

**Phase 6.1: Service Layer Refinement**

**Responsibilities**:
- Extract common patterns into shared utilities
- Implement consistent error handling across services
- Apply Dependency Injection pattern for testability
- Document service contracts in code comments

**Inputs**:
- All service implementations from Phases 2-4
- Architecture guide from Phase 1

**Outputs**:
- Refactored services with consistent patterns
- Utility module for common logic
- Updated service docstrings

**Completion Criteria**:
- Services follow Single Responsibility Principle
- Error handling consistent across all services
- Dependencies explicitly defined
- Code comments document contracts

---

**Phase 6.2: Test Coverage & Mocking**

**Responsibilities**:
- Achieve >90% code coverage
- Implement proper mocking for dependencies
- Add test helper utilities
- Document testing approach

**Inputs**:
- All test files from Phases 2-5
- Services to be tested

**Outputs**:
- Coverage report (>90%)
- Test utilities module
- Testing documentation

**Completion Criteria**:
- Code coverage >90% for all services
- No untested error paths
- Mocking used appropriately (not over-mocked)

---

**Phase 6.3: Documentation & Examples**

**Responsibilities**:
- Complete API documentation
- Provide usage examples for each service
- Document testing approach
- Create developer guide

**Inputs**:
- All service implementations
- Test suites
- Architecture decisions

**Outputs**:
- Complete API documentation
- Usage examples for developers
- Testing guide
- Troubleshooting guide

**Completion Criteria**:
- New developer can understand codebase in <1 hour
- All public methods documented
- Examples cover common use cases
- Debugging guidance provided

---

## Key Design Decisions

### 1. Service Layer Architecture
**Decision**: Implement discrete services (PriorityService, CategoryService, SearchService, etc.) rather than monolithic TaskService

**Rationale**:
- Enables independent testing of each feature
- Follows Single Responsibility Principle
- Allows parallel development of features
- Easier to maintain and extend

**Alternatives Considered**:
- Monolithic TaskService: Would violate SRP and make testing harder
- Domain-driven design: Overkill for Phase I scope

### 2. In-Memory Storage Implementation
**Decision**: Use Python list for task storage with filtering applied in-memory

**Rationale**:
- Meets Phase I constraint (no external database)
- Performance acceptable for <1000 tasks
- Simple and testable
- Can be replaced with database in Phase II without API changes

**Alternatives Considered**:
- Dictionary lookup: Requires synchronization between storage methods
- Sorted containers: Adds complexity without significant benefit for Phase I

### 3. Validation Layer
**Decision**: Implement validators module with reusable validation functions

**Rationale**:
- Validation logic testable independently
- Reusable across CLI and service layers
- Clear error messages from validation failures
- Maintains SOLID principles

**Alternatives Considered**:
- Dataclass validators: Less flexible, couples validation to model
- String validation at CLI: Allows invalid data in service layer

### 4. CLI Command Design
**Decision**: Extend existing commands with new flags rather than create new commands

**Rationale**:
- Maintains consistency with existing CLI
- Reduces command count
- Familiar to existing users
- Easier to document

**Alternatives Considered**:
- Separate command for filtering: Would require users to learn multiple commands
- Interactive mode: Out of scope for Phase I

### 5. Recurrence Implementation
**Decision**: Create new task instance on completion rather than modify existing task

**Rationale**:
- Preserves completion history
- Independent instances (update one, doesn't affect others)
- Matches user expectation (original task marked complete)
- Simplifies deletion logic

**Alternatives Considered**:
- Modify task with recurrence tracking: Couples completion with recurrence
- Queue-based generation: Over-engineered for Phase I

### 6. Error Handling Strategy
**Decision**: Validate at boundaries (CLI, service entry points), pass clean data through system

**Rationale**:
- Clear responsibility for error handling
- User-friendly error messages at CLI
- Internal APIs work with valid data only
- Testable error paths

**Alternatives Considered**:
- Defensive programming everywhere: Overly verbose
- Exceptions throughout: Hard to test, inconsistent handling

---

## Acceptance Criteria by Phase

### Phase 0: Research Complete
- [ ] research.md created with all findings
- [ ] No "NEEDS CLARIFICATION" markers remain
- [ ] Design patterns confirmed
- [ ] Edge case strategies validated

### Phase 1: Design Complete
- [ ] data-model.md documents Task entity
- [ ] contracts/ documents all service boundaries
- [ ] quickstart.md guides developers
- [ ] architecture.md explains design decisions

### Phase 2: Priority & Category Features Complete
- [ ] User Story 1 (Priority) 5/5 acceptance scenarios passing
- [ ] User Story 2 (Category) 6/6 acceptance scenarios passing
- [ ] FR-001 through FR-007 implemented
- [ ] CLI commands for priority/category working
- [ ] Unit tests >95% coverage for Phase 2 services

### Phase 3: Search, Filter, Sort Features Complete
- [ ] User Story 3 (Search) 5/5 acceptance scenarios passing
- [ ] User Story 4 (Filter) 5/5 acceptance scenarios passing
- [ ] User Story 5 (Sort) 5/5 acceptance scenarios passing
- [ ] FR-008 through FR-020 implemented
- [ ] CLI flags working for search/filter/sort
- [ ] Performance goals met (SC-002, SC-003)
- [ ] Unit tests >95% coverage for Phase 3 services

### Phase 4: Due Dates & Recurring Tasks Complete
- [ ] User Story 6 (Due Dates) 6/6 acceptance scenarios passing
- [ ] User Story 7 (Recurring Tasks) 8/8 acceptance scenarios passing
- [ ] FR-021 through FR-053 implemented
- [ ] Recurring task auto-generation working
- [ ] Month-end edge cases handled correctly
- [ ] Performance goals met (SC-004, SC-005)
- [ ] Unit tests >95% coverage for Phase 4 services

### Phase 5: Integration & Acceptance Testing Complete
- [ ] All 35 acceptance scenarios passing via CLI
- [ ] Integration tests (40+) passing
- [ ] Edge cases (8) tested and passing
- [ ] Performance baseline documented (SC-001 through SC-010)
- [ ] No conflicts between features
- [ ] Help text accurate and examples working

### Phase 6: Code Quality & Documentation Complete
- [ ] Code coverage >90% overall
- [ ] All services follow SOLID principles
- [ ] Error handling consistent
- [ ] API documentation complete
- [ ] Developer guide complete
- [ ] Ready for Phase II implementation

---

## Timeline & Dependencies

### Critical Path
1. Phase 0 (Research) - Parallel with Phase 1
2. Phase 1 (Design) - Foundation, unblocks all development
3. Phases 2 & 3 - Can be parallel (P1 features independent from P2)
4. Phase 4 - Depends on Phases 2 & 3 complete
5. Phases 5 & 6 - Final validation and polish

### Parallel Development Opportunities
- Phase 2 (Priority/Category) and Phase 3 (Search/Filter/Sort) can be developed in parallel
- Phase 5 (Integration testing) and Phase 6 (Refactoring) can overlap
- CLI updates for each phase can be done independently

---

## Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|-----------|
| Month-end recurrence calculation error | High | Medium | Implement and test extensively in Phase 4.2; document edge cases |
| Performance degradation with 1000+ tasks | Medium | Low | Profile in Phase 5.4; optimize if needed; in-memory acceptable for scope |
| Feature interactions causing bugs | High | Low | Comprehensive integration tests in Phase 5.1 |
| CLI interface conflicts | Medium | Low | Contract-based CLI design from Phase 1; validate in Phase 5.2 |
| Test coverage gaps | Medium | Medium | Enforce >90% coverage in Phase 6.2; track coverage throughout |

---

## Success Metrics

✅ **Feature Completeness**: All 53 functional requirements implemented
✅ **User Story Completeness**: All 7 user stories (35 scenarios) passing
✅ **Quality**: >90% code coverage, <3 bugs found in acceptance testing
✅ **Performance**: All SC goals met (SC-001 through SC-010)
✅ **Backward Compatibility**: Existing Basic features unaffected
✅ **Code Quality**: SOLID principles followed, architecture reviewed
✅ **Documentation**: Developer can understand and extend codebase

---

## Deliverables Checklist

- [ ] research.md
- [ ] data-model.md
- [ ] contracts/ (6 contract documents)
- [ ] quickstart.md
- [ ] architecture.md
- [ ] src/ (complete implementation)
- [ ] tests/ (unit, integration, acceptance)
- [ ] README.md with setup instructions
- [ ] API documentation
- [ ] Developer guide
- [ ] Performance baseline report

