# Phase 0 Research Findings: Phase 1 Todo App

**Date**: 2025-12-30
**Feature**: 1-phase-1-todo-app
**Purpose**: Document technical decisions and research findings for implementation

---

## Research Topics

### 1. Python DateTime Handling for Due Dates

**Decision**: Use `datetime.date` for due dates (no time component in Phase I)

**Rationale**:
- Feature spec specifies "optional due date" without time requirement
- `datetime.date` simpler than `datetime.datetime` for Phase I
- Adequate for daily/weekly/monthly recurrence patterns
- Format validation straightforward (YYYY-MM-DD)

**Implementation Approach**:
- Validate format with regex: `^\d{4}-\d{2}-\d{2}$`
- Parse with `datetime.strptime(date_str, "%Y-%m-%d").date()`
- Compare with `datetime.date.today()` for overdue detection
- No timezone handling needed (local calendar date sufficient)

**Edge Cases Documented**:
- Leap years: Use `calendar.monthrange()` for day validation
- Month-end: Handle in recurrence service
- Past dates: Allowed and stored normally

**Alternatives Rejected**:
- `datetime.datetime`: Unnecessary complexity for Phase I
- String storage: Harder to validate and compare

---

### 2. In-Memory Storage Patterns for Filtering/Sorting

**Decision**: Use Python `list` with filter/sort applied in-memory

**Rationale**:
- Simple, testable, no external dependencies
- Performance adequate for Phase I scope (<1000 tasks)
- Can be replaced with database in Phase II (interface-based)

**Implementation Approach**:
- Store tasks in module-level list or Storage class
- Filter: Use list comprehension with predicates
- Sort: Use `sorted()` with custom key functions
- Index/find: Linear search acceptable for scope

**Performance Analysis**:
- Filter 1000 tasks by priority: ~5ms (list comprehension + if check)
- Sort 1000 tasks by due date: ~15ms (Python's Timsort)
- Combined filter+sort: ~20ms (within <500ms goal)
- Multi-criteria filter: ~10-20ms per criteria

**Optimization Strategies** (if needed in Phase 5):
1. Lazy filtering: Filter only when list is displayed
2. Indexed storage: Use dict by ID for O(1) lookups
3. Sorted containers: Maintain pre-sorted views (Python `sortedcontainers`)
4. Caching: Cache filter results for repeated queries

**Alternatives Rejected**:
- Dictionary keyed by ID: Loses insertion order, complicates iteration
- Separate indices: Over-engineered for <1000 items
- Database: Violates Phase I constraint

---

### 3. CLI Argument Parsing Patterns

**Decision**: Use Python's `argparse` module (standard library)

**Rationale**:
- Standard library (no external dependencies)
- Well-documented and battle-tested
- Supports subcommands, flags, positional args
- Built-in help generation

**Implementation Approach**:
- Use ArgumentParser with subparsers for commands (add, update, list, etc.)
- Each command has dedicated parser with flags
- Priority: `--priority {HIGH,MEDIUM,LOW}` (choices for validation)
- Category: `--category TEXT` (string)
- Due date: `--due-date DATE` (format validated separately)
- Search: `--search KEYWORD`
- Filters: `--filter-status`, `--filter-priority`, `--filter-category`
- Sort: `--sort-by {PRIORITY,DUE_DATE,TITLE}` with `--sort-order {ASC,DESC}`

**Example Structure**:
```
add --priority HIGH --category work "Task title" --due-date 2025-12-31
update task-001 --priority MEDIUM --category personal
list --filter-priority HIGH --filter-category work --sort-by DUE_DATE --sort-order ASC
search "keyword"
```

**Error Handling**:
- Invalid enum values rejected by argparse
- Missing required args caught by argparse
- Custom validation for date format in service layer

**Alternatives Rejected**:
- Click framework: External dependency
- Custom parsing: Error-prone, worse UX
- Interactive prompts: Not spec'd, not typical for CLI tools

---

### 4. Month-End Recurrence Calculation

**Decision**: Use calendar arithmetic with month-end handling

**Rationale**:
- Spec requirement: "handle month-end edge cases for monthly recurrence"
- Jan 31 + 1 month should become Feb 28 or Feb 29 (leap year)
- User expectation: Task recurring on "31st" becomes available on last day of next month

**Implementation Approach**:
```
For monthly recurrence:
1. Original due date: Day D, Month M, Year Y
2. Next due date:
   - Target month: M+1
   - Target day: min(D, calendar.monthrange(Y, M+1)[1])
   - Handle year rollover when M = 12
```

**Examples**:
- Jan 31, 2025 → Feb 28, 2025 (Feb has 28 days)
- Feb 28, 2025 → Mar 28, 2025 (Mar has 31 days, use original day)
- Jan 31, 2026 → Feb 28, 2026 (Feb has 28 days)
- Jan 31, 2024 → Feb 29, 2024 (leap year, Feb has 29 days)

**Edge Cases**:
- Monthly recurrence without due date: Use creation date
- Monthly recurrence with due date before creation: Use due date
- Feb 29 leap year: Handled by `monthrange()` returning correct day count

**Testing Strategy**:
- Test all month combinations (28, 29, 30, 31 day months)
- Test leap year handling
- Test year boundary (Dec 31 + 1 month = Jan 31)

**Alternatives Rejected**:
- dateutil library: External dependency (Phase I constraint)
- Simple +30 days: Doesn't match user expectation ("recurring on 31st")
- User-configurable handling: Adds complexity not in spec

---

### 5. SOLID Principles in Python Services

**Decision**: Apply SOLID through service layer architecture

**Rationale**:
- Spec requirement: "SOLID principles"
- Single Responsibility: Each service handles one concern
- Open/Closed: Services extend through composition, not modification
- Liskov: Interface-based services (contract documents)
- Interface Segregation: Small, focused service contracts
- Dependency Inversion: Services depend on abstractions (Task model), not implementations

**Implementation Approach**:

**Single Responsibility**:
- PriorityService: Only priority-related operations
- CategoryService: Only category-related operations
- SearchService: Only search logic
- DateService: Only date validation and utilities
- RecurrenceService: Only recurrence pattern handling

**Open/Closed**:
- Services defined as classes (open for extension via inheritance)
- New filter types added without modifying existing filters
- New sort criteria added without modifying existing sorts

**Dependency Inversion**:
- Services accept Task objects (not raw data)
- Task model defines validation rules
- CLI layer depends on service contracts, not implementations

**Example Service Structure**:
```python
class PriorityService:
    """Handles priority-related operations."""

    def validate_priority(self, priority: str) -> bool:
        """Validate priority is valid enum."""
        pass

    def filter_by_priority(self, tasks: List[Task], priority: str) -> List[Task]:
        """Return tasks matching priority."""
        pass

    def sort_by_priority(self, tasks: List[Task], reverse: bool = False) -> List[Task]:
        """Return tasks sorted by priority."""
        pass
```

**Code Organization**:
- `models/`: Data entities (Task, Enums)
- `services/`: Business logic (PriorityService, etc.)
- `cli/`: User interface (commands, formatters)
- `tests/`: Test layer per category

**Alternatives Rejected**:
- Monolithic TaskService: Violates Single Responsibility
- Functional programming: Doesn't fit team familiarity (assuming OOP background)
- Domain-driven design: Over-engineered for Phase I scope

---

### 6. Testing Strategy

**Decision**: Multi-layer testing (unit, integration, acceptance)

**Rationale**:
- Spec requirement: "Testable design"
- Independent feature testing: Each service tested in isolation
- Cross-feature validation: Integration tests verify interactions
- User-centric testing: Acceptance tests via CLI

**Testing Layer Structure**:

**Unit Tests** (>95% coverage per service):
- Test each service method with valid/invalid inputs
- Mock dependencies (e.g., Storage)
- Test error paths and edge cases
- Example: `test_priority_service.py` tests validate_priority(), filter_by_priority(), sort_by_priority()

**Integration Tests** (40+ scenarios):
- Test feature combinations (priority + filter, search + sort)
- Test multi-filter scenarios
- Test recurring task with priority/category/due date
- Test complete workflows

**Acceptance Tests** (35 user story scenarios):
- Test each acceptance scenario via CLI
- No mocking, full end-to-end
- Verify error messages match spec
- One test file per user story

**Edge Case Tests**:
- Boundary conditions (very long strings, large counts)
- Month-end dates, leap years
- Null/empty values
- Special characters

**Test Tools**:
- Framework: pytest (standard library compatible)
- Mocking: unittest.mock (standard library)
- Fixtures: pytest fixtures for test data
- Parameterization: pytest.mark.parametrize for edge cases

**Coverage Goals**:
- Phase 2: >95% coverage for priority/category services
- Phase 3: >95% coverage for search/filter/sort services
- Phase 4: >95% coverage for date/recurrence services
- Overall: >90% code coverage

**Alternatives Rejected**:
- unittest: pytest cleaner and more powerful
- No testing: Violates spec requirement
- Only acceptance tests: Misses edge cases and unit logic errors

---

### 7. Backward Compatibility with Basic Features

**Decision**: New fields optional in Task model with sensible defaults

**Rationale**:
- Spec requirement: "maintain backward compatibility with existing Basic feature tasks"
- Basic features: Add, Delete, Update, View, Mark Complete
- Phase I may have existing tasks created without priority/category/due_date

**Implementation Approach**:

**Task Model Evolution**:
```python
class Task:
    id: str
    title: str
    status: str  # existing
    created_timestamp: datetime  # existing
    completed_timestamp: Optional[datetime]  # existing

    # NEW fields (optional, with defaults)
    priority: str = "medium"  # NEW: default to medium
    category: Optional[str] = None  # NEW: optional
    due_date: Optional[date] = None  # NEW: optional
    recurrence: Optional[str] = None  # NEW: optional
```

**Serialization**:
- When loading existing tasks: Set priority="medium", others=None
- When saving: Include all fields (optional fields stored as null)
- Migration: Not needed (fields created with defaults)

**CLI Behavior**:
- Display priority even if "medium" (default)
- Display category only if set (not empty)
- Display due date only if set
- Display recurrence only if set

**Services**:
- Handle null/empty values gracefully
- Filter by priority includes all tasks (medium is default)
- Don't crash if null values present

**Testing**:
- Create tasks without new fields, verify defaults applied
- Update basic task to add priority, verify not lost
- Filter includes old tasks with defaults

**Alternatives Rejected**:
- Database migration: Not applicable (in-memory)
- Version tracking: Unnecessary for Phase I (simple defaults work)
- Separate "legacy" task type: Over-engineered

---

## Key Decisions Summary

| Topic | Decision | Why | Risk Level |
|-------|----------|-----|------------|
| Date handling | Use `datetime.date` | Simple, adequate for spec | Low |
| Storage | In-memory list | No dependencies, adequate performance | Low |
| CLI parsing | Use `argparse` | Standard library, battle-tested | Low |
| Month-end math | Calendar arithmetic | Matches user expectations | Medium |
| SOLID design | Service layer architecture | Testable, maintainable, extensible | Low |
| Testing | Multi-layer (unit/integration/acceptance) | Comprehensive coverage | Low |
| Backward compat | Optional fields with defaults | Simple, no migration needed | Low |

---

## Implementation Guidance

### For Phase 2 (Priority & Category)
- Start with Task model (add priority, category fields)
- Implement validators for each field
- Create PriorityService and CategoryService
- Update CLI add/update commands
- Write unit tests

### For Phase 3 (Search, Filter, Sort)
- Create SearchService (case-insensitive partial match)
- Create FilterService (AND logic for combined filters)
- Create SortService (stable sort, null handling)
- Update CLI list command
- Parallel development with Phase 2 possible

### For Phase 4 (Due Dates, Recurring)
- Create DateService (validation, overdue detection)
- Create RecurrenceService (pattern validation, instance generation)
- Update Task model to track parent_recurrence_id
- Update CLI complete command to trigger recurrence generation
- Extensive edge case testing for dates

### For Phase 5+ (Testing, Refactoring)
- Achieve >90% coverage
- Extract common patterns
- Document all contracts
- Performance profiling and optimization if needed

---

## References & Resources

- Python `datetime` docs: https://docs.python.org/3/library/datetime.html
- Python `argparse` docs: https://docs.python.org/3/library/argparse.html
- Python `calendar` docs: https://docs.python.org/3/library/calendar.html
- pytest documentation: https://docs.pytest.org/
- SOLID principles: https://en.wikipedia.org/wiki/SOLID
- Feature specification: [spec.md](spec.md)

