# Skill: Data Model Versioning and Backward Compatibility Strategy

**Skill ID**: DMD-003
**Agent Owner**: data-model-designer
**Project**: Evolution of Todo Hackathon II – Phases 1-5
**Status**: Production

---

## Purpose

Design a versioning strategy for the Task entity and data model that ensures Phase 1 tasks continue to work seamlessly through Phase II (web app), Phase III (AI chatbot), Phase IV (Kubernetes), and Phase V (cloud deployment). This skill defines how new fields are introduced without breaking existing functionality, ensures backward compatibility across storage migrations (memory → database → cloud), and prevents version lock-in. The strategy allows the data model to evolve while protecting legacy data.

---

## When to Use

- **Between phase transitions**: When upgrading from Phase 1 to Phase II, II to III, etc.
- **Feature expansion planning**: Before adding new fields/entities to Task model
- **Storage migration**: When moving from in-memory to database, database to cloud
- **API versioning**: When Phase II web API must support both old and new task formats
- **Data migration planning**: When upgrading stored tasks to new schema
- **Rollback planning**: When a deployment fails and old version must be restored

---

## Inputs

1. **Current Task entity** (document): From DMD-001 and DMD-002, the optimized Phase 1 Task
2. **Phase II+ requirements** (list): New fields/features planned for future phases
3. **Storage platform timeline** (text): When storage changes (Phase 1 memory → Phase II DB → Phase V cloud)
4. **Breaking change tolerance** (text): How aggressive version upgrades can be
5. **Support duration** (text, optional): How long old versions must be supported

---

## Step-by-Step Process

### Step 1: Define Versioning Scheme
Choose a versioning scheme that clearly communicates breaking vs. non-breaking changes.

**Option A: Semantic Versioning (Recommended)**

```
Version Format: MAJOR.MINOR.PATCH
  MAJOR: Breaking changes (cannot auto-upgrade, migration required)
  MINOR: Backward-compatible additions (new optional fields, new entities)
  PATCH: Bug fixes and clarifications (no data changes)

Examples:
  1.0.0 = Phase 1 initial (4 required fields: id, title, status, created_timestamp)
  1.1.0 = Phase 1 enhancement (add due_date, priority optional fields)
  1.2.0 = Phase 1 bugfix (timestamp precision improvements)
  2.0.0 = Phase II breaking change (add required user_id field)
  2.1.0 = Phase II feature (add description field, categories)
  3.0.0 = Phase III breaking change (add recurrence_rule, change task state machine)
  4.0.0 = Phase IV breaking change (add cloud-specific fields)
  5.0.0 = Phase V breaking change (cloud deployment fields)

Backward Compatibility Rules:
  ✓ 1.0.0 → 1.1.0 = Backward compatible (old tasks work with new version)
  ✓ 1.1.0 → 1.2.0 = Backward compatible (same schema)
  ✗ 1.x.x → 2.0.0 = Breaking change (requires migration)
  ✗ 2.x.x → 3.0.0 = Breaking change (requires migration)
```

**Option B: Date-Based Versioning (Alternative)**

```
Version Format: YYYY-MM-DD
  Example: 2025-12-30 (Phase 1 initial release)
           2026-01-15 (Phase II release)
           2026-04-20 (Phase III release)

Pros: Clear timeline, easy to correlate with releases
Cons: Doesn't communicate breaking vs. non-breaking clearly

Not Recommended: Use semantic versioning instead for clarity
```

**Option C: Phase-Based Versioning (Not Recommended for Data)**

```
Version Format: Phase.Iteration
  Example: 1.0 (Phase 1 initial)
           1.1 (Phase 1 iteration 2)
           2.0 (Phase 2 initial)

Problem: Doesn't distinguish breaking from non-breaking changes
  Example: Phase 1.1 might add optional fields (backward compatible)
           or required fields (breaking change) — unclear from version alone

Conclusion: Not recommended; semantic versioning is clearer
```

**Chosen: Semantic Versioning (MAJOR.MINOR.PATCH)**
- Clear communication of compatibility
- Industry standard
- Tools support it (version comparison, ranges)

---

### Step 2: Define Breaking vs. Non-Breaking Changes
Classify all possible schema changes as breaking or non-breaking.

**Breaking Changes** (Require MAJOR version bump and migration):

```
1. Adding Required Field (no default value)
   Example: Phase II adds required user_id field
   Impact: Existing Phase 1 tasks have no user_id (invalid in Phase II)
   Migration: Must populate user_id for all Phase 1 tasks (default to "system" or prompt)
   Version: 1.x.x → 2.0.0

2. Removing Field
   Example: Phase III removes priority field (replaced with AI-calculated importance)
   Impact: Existing tasks with priority field are corrupted/ignored
   Migration: Must drop field or move to archive table
   Version: 2.x.x → 3.0.0

3. Changing Data Type
   Example: Phase II changes priority from enum string to numeric ID
   Impact: Existing "normal" value is no longer valid numeric ID
   Migration: Must convert all "low" → 1, "normal" → 2, "high" → 3 (or create Priority entity)
   Version: 1.x.x → 2.0.0

4. Changing Field Meaning
   Example: Phase III redefines status enum from (pending, completed) to (pending, in_progress, completed, cancelled)
   Impact: Existing tasks with status=pending work, but new system expects different values
   Migration: Must map old values to new state machine
   Version: 2.x.x → 3.0.0

5. Changing Constraint
   Example: Phase II makes title required (was optional), or reduces max length from 255 → 100
   Impact: Existing Phase 1 tasks may violate new constraint
   Migration: Must validate/update existing data
   Version: 1.x.x → 2.0.0

6. Restructuring Relationships
   Example: Phase II changes Task.priority from enum to Task.priority_id (reference to Priority entity)
   Impact: Existing embedded priority data is lost
   Migration: Must create Priority entity and relink tasks
   Version: 1.x.x → 2.0.0
```

**Non-Breaking Changes** (Require MINOR version bump, no migration needed):

```
1. Adding Optional Field (with default)
   Example: Phase II adds description (string, max 2000, default null)
   Impact: Existing Phase 1 tasks have description=null (valid)
   Migration: None needed; old tasks work automatically
   Version: 1.1.0 (or 1.2.0, etc.)

   Prerequisite: Field must have default value that is valid in all contexts
   Unsafe: Adding optional field with no default (might null in unexpected places)
   Safe: Adding optional field with explicit default (null, empty string, default enum value)

2. Expanding Enum (adding values)
   Example: Phase II adds status value "archived" to existing (pending, completed)
   Impact: Existing tasks with status=pending or =completed still valid
   Migration: None needed; old tasks work automatically
   Version: 1.1.0

   Prerequisite: New enum value must not break existing code
   Example Safe: Add "archived" status (code can ignore it)
   Example Unsafe: Remove "pending" status (existing tasks become invalid)

3. Increasing Size Constraints
   Example: Phase II increases title max length from 255 → 512
   Impact: Existing tasks with <= 255 chars still valid
   Migration: None needed; old data still complies with new constraint
   Version: 1.1.0

   Prerequisite: All existing data must comply with new constraint
   Example: title max 255 → 512 (OK, all existing titles are ≤ 255)
   Example: title max 255 → 100 (BREAKING, some existing titles > 100)

4. Decreasing Size Constraints (if safe)
   Example: Phase II decreases title max length from 255 → 200 (only if no existing task > 200)
   Impact: If all existing tasks are ≤ 200 chars, non-breaking
   Migration: None needed (if constraint satisfied)
   Version: 1.1.0 (only if safe)

   Prerequisite: Must verify all existing data complies with new constraint
   If any existing data > 200 chars: This is BREAKING change
   Example: title max 255 → 200, but tasks "Buy a very long grocery list" exists (>200)
   Resolution: BREAKING change; requires migration

5. Adding New Entity
   Example: Phase II adds Category entity (new table)
   Impact: Existing tasks are unchanged; Category is optional
   Migration: None needed for Task; Category table starts empty
   Version: 1.1.0

   Prerequisite: Task does not reference new entity (or references as optional)
   Safe: Add Category entity, Task references category_id as optional (null by default)
   Unsafe: Add Category entity, make Task.category_id required (BREAKING)

6. Clarifications/Documentation Changes
   Example: Phase II clarifies that title cannot contain newlines (was ambiguous in Phase 1)
   Impact: Existing tasks are unchanged (no schema change)
   Migration: None needed (code already handles correctly)
   Version: 1.0.1 (PATCH version)
```

**Decision Matrix**:

| Change Type | Breaking? | Version Bump | Migration Needed? |
|-------------|-----------|--------------|-------------------|
| Add required field (no default) | ✗ YES | MAJOR | YES |
| Remove field | ✗ YES | MAJOR | YES |
| Change data type | ✗ YES | MAJOR | YES |
| Change field meaning | ✗ YES | MAJOR | YES |
| Change constraint (tighter) | ✗ YES (if data unsafe) | MAJOR | YES |
| Add optional field (with default) | ✓ NO | MINOR | NO |
| Expand enum (add values) | ✓ NO | MINOR | NO |
| Increase size constraint | ✓ NO | MINOR | NO |
| Decrease size constraint | ✓ NO (if safe) or ✗ YES | MINOR or MAJOR | NO or YES |
| Add new entity | ✓ NO | MINOR | NO |
| Documentation/clarification | ✓ NO | PATCH | NO |

---

### Step 3: Design Data Format with Version Field
Add version tracking to individual Task objects for safe schema evolution.

**Option A: No Version Field (Stateless)**

```
Current Task:
  {
    id: "task-001",
    title: "Buy groceries",
    status: "pending",
    created_timestamp: "2025-12-30T10:30:45Z",
    due_date: "2026-01-15",
    priority: "normal",
    completed_timestamp: null
  }

Problem: System cannot tell which version this task is
  - If code expects user_id field (Phase II), does this task have it?
  - If code reads priority, is it enum string or numeric ID?
  - No way to know without external metadata

Solution: Add version field to task
```

**Option B: Add Version Field (Stateful) — Recommended**

```
Enhanced Task with Version:
  {
    version: "1.0.0",                 // NEW: Schema version of this task
    id: "task-001",
    title: "Buy groceries",
    status: "pending",
    created_timestamp: "2025-12-30T10:30:45Z",
    due_date: "2026-01-15",
    priority: "normal",
    completed_timestamp: null
  }

Benefits:
  ✓ System knows exactly which schema this task uses
  ✓ Code can upgrade on read: if version < 2.0.0, apply migration
  ✓ Mixed versions in same collection: Phase 1 tasks (v1.0.0) and Phase II tasks (v2.0.0) coexist
  ✓ Handles partial upgrades: some tasks migrated, some not yet

Phase II Collection (mixed versions):
  [
    { version: "1.0.0", id: "task-001", ... },  // Phase 1 task (old format)
    { version: "2.0.0", id: "task-002", user_id: "user-123", ... },  // Phase II task (new format)
    { version: "1.0.0", id: "task-003", ... }   // Phase 1 task (old format)
  ]

When reading:
  FOR EACH task:
    IF task.version < current_schema_version:
      Apply migration: convert old format to new format
    USE upgraded task data

This allows:
  - Lazy migration (upgrade on read, not all at once)
  - Rollback (keep old version format, read with old code)
  - Hybrid operation (serve both old and new clients)
```

**Option C: Implicit Version (Code-Level, Not Data-Level)**

```
No version field in Task itself
Instead: Store migration metadata separately

MigrationRegistry:
  {
    "1.0.0": { added_fields: [], removed_fields: [], ...},
    "1.1.0": { added_fields: ["due_date", "priority"], ...},
    "2.0.0": { added_fields: ["user_id"], breaking_changes: true, ...}
  }

When reading Phase 1 task (no version field):
  1. Assume version 1.0.0 (oldest version)
  2. Apply migration chain: 1.0.0 → 1.1.0 → 2.0.0
  3. Return upgraded task

Problem:
  - Assumes oldest version for unversioned tasks (might be wrong)
  - All Phase II tasks must be explicitly migrated (cannot be lazy)
  - Cannot roll back without knowing old format
```

**Chosen: Option B (Version Field in Task)**
- Explicit, unambiguous version tracking
- Supports lazy migration (upgrade on read)
- Allows mixed versions in collection
- Clear rollback path

---

### Step 4: Define Migration Paths
Create explicit migration functions for each breaking change.

**Migration Framework**:

```python
from typing import Dict, Callable, Any

# Type for migration function
MigrationFunction = Callable[[Dict[str, Any]], Dict[str, Any]]

# Migration registry
migrations: Dict[str, MigrationFunction] = {}

# Migration 1.0.0 → 1.1.0 (Add optional fields due_date, priority)
def migrate_1_0_0_to_1_1_0(task: Dict) -> Dict:
    """
    Phase 1 enhancement: Add due_date and priority fields
    This is backward-compatible (new fields are optional)
    """
    # No actual migration needed (new fields have defaults)
    # But we update version explicitly
    task['version'] = '1.1.0'
    if 'due_date' not in task:
        task['due_date'] = None
    if 'priority' not in task:
        task['priority'] = 'normal'
    return task

migrations['1.0.0→1.1.0'] = migrate_1_0_0_to_1_1_0

# Migration 1.x.x → 2.0.0 (Add required user_id field)
def migrate_1_x_x_to_2_0_0(task: Dict, default_user_id: str = "system") -> Dict:
    """
    Phase II breaking change: Add required user_id field
    Migration strategy: Assign all Phase 1 tasks to "system" user (or configurable)
    """
    task['version'] = '2.0.0'
    task['user_id'] = task.get('user_id', default_user_id)
    return task

migrations['1.x.x→2.0.0'] = migrate_1_x_x_to_2_0_0

# Migration 2.x.x → 3.0.0 (Add recurrence_rule, change status enum)
def migrate_2_x_x_to_3_0_0(task: Dict) -> Dict:
    """
    Phase III breaking change: Add recurrence_rule, expand status enum
    """
    task['version'] = '3.0.0'

    # Add recurrence_rule (optional, defaults to none)
    if 'recurrence_rule' not in task:
        task['recurrence_rule'] = None

    # Expand status enum: pending + completed → pending + in_progress + completed + cancelled
    # Old tasks remain with original status (valid in new enum)
    # No conversion needed (pending and completed still exist in new enum)

    return task

migrations['2.x.x→3.0.0'] = migrate_2_x_x_to_3_0_0

# Upgrade function (apply chain of migrations)
def upgrade_task(task: Dict, target_version: str) -> Dict:
    """Upgrade task to target version by applying migrations in sequence"""
    current_version = task.get('version', '1.0.0')

    if current_version == target_version:
        return task  # Already current version

    # Define migration chain (in order)
    chain = [
        ('1.0.0', '1.1.0'),
        ('1.1.0', '2.0.0'),
        ('2.0.0', '3.0.0'),
        # ... add more migrations as phases progress
    ]

    # Apply migrations in sequence
    current = task
    for from_ver, to_ver in chain:
        if current.get('version', '1.0.0') < from_ver:
            continue  # Already past this migration
        if to_ver <= target_version:
            key = f'{from_ver}→{to_ver}'
            if key in migrations:
                current = migrations[key](current)

    return current

# Usage Example:
# Phase 1 task
old_task = {
    'version': '1.0.0',
    'id': 'task-001',
    'title': 'Buy groceries',
    'status': 'pending',
    'created_timestamp': '2025-12-30T10:30:45Z'
}

# Upgrade to Phase II (v2.0.0)
upgraded_task = upgrade_task(old_task, '2.0.0')
# Result:
# {
#   'version': '2.0.0',
#   'id': 'task-001',
#   'title': 'Buy groceries',
#   'status': 'pending',
#   'created_timestamp': '2025-12-30T10:30:45Z',
#   'user_id': 'system',
#   'due_date': None,
#   'priority': 'normal'
# }
```

---

### Step 5: Define Backward Compatibility Rules
Establish clear rules for what versions code must support.

**Backward Compatibility Policy**:

```
Rule 1: Current Version Support (Mandatory)
  Code MUST support reading/writing current schema version
  Example: Phase II code MUST support v2.0.0 format
  Duration: Always (current version forever supported)

Rule 2: Previous Major Version Support (Recommended)
  Code SHOULD support reading previous MAJOR version (one release back)
  Example: Phase II code SHOULD support v1.x.x reading (via migration)
  Duration: Until next MAJOR version released

  Rationale:
    - Users may not upgrade immediately
    - Gradual rollout possible (some users on Phase 1, some on Phase 2)
    - Rollback possible if Phase 2 has issues

Rule 3: Pre-Previous Major Version Support (Optional)
  Code MAY support reading older MAJOR versions (optional)
  Example: Phase III code MAY support v1.x.x, but not required
  Duration: Until dropped explicitly

  Decision per phase:
    Phase I→II: MUST support v1.x.x reads
    Phase II→III: SHOULD support v2.x.x reads
    Phase III→IV: MAY support v2.x.x reads (optional)
    Phase IV→V: OPTIONAL (v3.x.x support can be dropped)

Rule 4: Older Versions Can Be Dropped
  Code MUST announce deprecation before dropping support
  Example: Phase IV announces "Phase I v1.x.x support will be dropped in Phase V"
  Duration: At least one phase before dropping

Deprecation Policy:
  Year 1 (Phase I + II + III):
    - All versions from Phase I (v1.x.x) are supported
  Year 2 (Phase IV):
    - Phase I (v1.x.x) support announced as deprecated
    - Phase II-III (v2.x.x, v3.x.x) fully supported
  Year 3 (Phase V+):
    - Phase I (v1.x.x) support can be dropped
    - Phase II+ (v2.x.x+) fully supported
```

**Backward Compatibility Guarantees**:

```
API Guarantee (What Developers Expect):
  ✓ I can read/parse a Phase 1 task in Phase II code
  ✓ I can write a Phase II task; it's valid in Phase III
  ✓ I can migrate a Phase 1 collection to Phase II schema
  ✗ I do NOT have to support reading Phase 3 format in Phase 2 code

Client/Server Compatibility:
  ✓ Old CLI client (Phase 1) CAN connect to new API (Phase II) if API supports v1.x.x reads
  ✗ Old CLI client cannot understand new API response fields it doesn't know about
  → Solution: API SHOULD be additive (add fields, don't remove) for old clients

Migration Guarantee:
  ✓ I CAN upgrade all Phase 1 tasks to Phase II schema automatically
  ✓ I CAN migrate in batches (some Phase 1 tasks, then more later)
  ✓ I CAN rollback: restore Phase 1 tasks from backup
  ✗ I CANNOT downgrade: I can restore v1.0.0 from backup, but cannot revert v2.0.0 to v1.0.0 automatically
```

---

### Step 6: Plan Storage Migration (Memory → Database → Cloud)
Define how versioning works across different storage platforms.

**Phase 1: In-Memory Storage**

```
Format: Python dataclass / JSON in memory
Version Tracking: version field in Task object
Serialization: JSON (to disk as backup, optional)

Example In-Memory Task:
  {
    version: "1.0.0",
    id: "task-001",
    title: "Buy groceries",
    status: "pending",
    created_timestamp: "2025-12-30T10:30:45Z",
    due_date: "2026-01-15",
    priority: "normal",
    completed_timestamp: null
  }

Upgrade Strategy:
  When Phase II code loads Phase 1 in-memory data:
    1. Read all tasks from memory
    2. Check each task.version
    3. If version < 2.0.0, apply migration_1_x_x_to_2_0_0()
    4. Update task.version = "2.0.0"
    5. Store back in memory (new format)

Backup Strategy:
  Save to JSON file: `tasks-backup-v1.0.0.json`
  {
    "version": "1.0.0",
    "tasks": [
      { "version": "1.0.0", ... },
      ...
    ]
  }
  If Phase II fails, restore from backup and stay on Phase 1
```

**Phase II: PostgreSQL Database**

```
Schema Versioning:
  Table: task_schema_version
    {
      id: INT PRIMARY KEY,
      version: VARCHAR(10),        // "2.0.0"
      migrated_at: TIMESTAMP,
      migration_status: ENUM(pending, in_progress, completed, rolled_back)
    }

Task Table v1.0.0:
  CREATE TABLE tasks_v1 (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20),            // ENUM
    created_timestamp TIMESTAMP,
    due_date DATE,
    priority VARCHAR(20),          // ENUM
    completed_timestamp TIMESTAMP
  );

Task Table v2.0.0 (after migration):
  CREATE TABLE tasks_v2 (
    id VARCHAR(20) PRIMARY KEY,
    user_id UUID NOT NULL,         // NEW required field
    title VARCHAR(255) NOT NULL,
    status VARCHAR(20),
    created_timestamp TIMESTAMP,
    due_date DATE,
    priority VARCHAR(20),
    completed_timestamp TIMESTAMP,
    version VARCHAR(10)            // NEW version field
  );

Migration Strategy (v1 → v2):
  1. Create new tasks_v2 table (with new schema)
  2. BEGIN TRANSACTION
  3. Copy from tasks_v1 to tasks_v2:
     INSERT INTO tasks_v2 SELECT
       id, 'system' as user_id,     // Assign default user_id
       title, status, created_timestamp, due_date, priority, completed_timestamp,
       '2.0.0' as version
     FROM tasks_v1
  4. UPDATE task_schema_version SET version='2.0.0', migration_status='completed'
  5. COMMIT
  6. (Optional) DROP tasks_v1 or RENAME to tasks_v1_archive
  7. RENAME tasks_v2 to tasks

Zero-Downtime Upgrade (Blue-Green Deployment):
  1. Keep v1 database running (blue)
  2. Create v2 database (green) with new schema
  3. Migrate data in background
  4. Redirect reads to v2 (after migration completes)
  5. Redirect writes to v2 (dual-write briefly)
  6. Monitor v2 stability
  7. Keep v1 as rollback (for 24 hours or agreed time)
  8. Decommission v1 when v2 stable

Rollback Strategy:
  If Phase II database fails:
    1. Stop serving from v2
    2. Clear v2 database
    3. Restore from backup (if needed)
    4. Resume serving from v1
    5. Investigate failure (schema issue? data loss?)
    6. Retry migration after fix
```

**Phase V: Cloud (DOKS/GKE/AKS)**

```
Version Tracking in Cloud:
  ConfigMap: task-schema-config
    {
      currentVersion: "5.0.0",
      supportedVersions: ["5.0.0", "4.x.x"]  // What versions this deployment reads
    }

Migration in Kubernetes:
  Pod: migration-job
    - Reads all tasks from database
    - For each task < 5.0.0, apply migration
    - Updates database (batched, no downtime)
    - Reports status (N tasks migrated, Y failed)

Canary Deployment (Gradual Rollout):
  1. Deploy Phase V code to 10% of pods
  2. Route 10% of reads to new pods
  3. Monitor for errors (schema mismatches?)
  4. If OK, increase to 25%, 50%, 100%
  5. If error, rollback 10% pods to Phase IV

Version Compatibility:
  Phase V code MUST handle:
    ✓ Phase V (5.0.0) tasks (primary)
    ✓ Phase IV (4.x.x) tasks (via migration on read)
    ? Phase III (3.x.x) tasks (optional, can drop)

Gradual Migration Strategy:
  Day 1: Deploy Phase V code, serve Phase IV data (auto-migrate on read)
  Day 2-3: Background job migrates Phase IV → Phase V (reduces read-time migration)
  Day 4: Verify all tasks are Phase V format
  Week 2: Drop support for Phase IV format (if confident)
```

---

### Step 7: Document Version Compatibility Matrix
Create a clear matrix showing which code versions can read which data versions.

**Compatibility Matrix**:

```
                  | Can Read v1.x.x | Can Read v2.x.x | Can Read v3.x.x | Can Read v4.x.x | Can Read v5.x.x
Phase I (v1.x.x)  | ✓ YES           | ✗ NO            | ✗ NO            | ✗ NO            | ✗ NO
Phase II (v2.x.x) | ✓ YES (via migr)| ✓ YES           | ✗ NO            | ✗ NO            | ✗ NO
Phase III (v3.x.x)| ✓ YES (via migr)| ✓ YES (via migr)| ✓ YES           | ✗ NO            | ✗ NO
Phase IV (v4.x.x) | ✓ OPTIONAL      | ✓ YES (via migr)| ✓ YES (via migr)| ✓ YES           | ✗ NO
Phase V (v5.x.x)  | ✗ NO (dropped)  | ✓ OPTIONAL      | ✓ OPTIONAL      | ✓ OPTIONAL      | ✓ YES

Legend:
  ✓ YES         = Full support (code understands data format)
  ✓ YES (via migr) = Support with automatic migration on read
  ✓ OPTIONAL    = May drop support (deprecation announced)
  ✗ NO          = No support (requires external migration tool or backup restore)

Example Reading Scenarios:

Scenario 1: Phase II code reading Phase 1 data (v1.0.0)
  Code: Phase II (v2.x.x)
  Data: Phase I task { version: "1.0.0", ... }

  Execution:
    1. Code loads task, checks version: "1.0.0"
    2. Code < 2.0.0, so migrate: apply migrate_1_x_x_to_2_0_0()
    3. Task now has { version: "2.0.0", user_id: "system", ... }
    4. Code can now read/process task normally

  Result: ✓ Works

Scenario 2: Phase IV code reading Phase I data (v1.0.0)
  Code: Phase IV (v4.x.x)
  Data: Phase I task { version: "1.0.0", ... }

  Decision: Phase IV announced v1.x.x support is OPTIONAL

  Option A (Maintain Compatibility):
    Apply migration chain: 1.0.0 → 1.1.0 → 2.0.0 → 3.0.0 → 4.0.0
    Result: ✓ Works (but slower due to long chain)

  Option B (Drop Support):
    Code throws error: "Unsupported task version: 1.0.0"
    Admin must use migration tool to upgrade data before using Phase IV
    Result: ✓ Works after migration, but requires external tool

Scenario 3: Phase I code reading Phase II data (v2.0.0)
  Code: Phase I (v1.x.x)
  Data: Phase II task { version: "2.0.0", user_id: "system", ... }

  Execution:
    Phase I code doesn't know about version field or user_id
    Tries to read task, encounters unknown fields
    Behavior depends on implementation:
      Option A (Strict): Throw error "Unknown fields in task"
      Option B (Lenient): Ignore unknown fields, use known fields

  Result: ✗ Fails (Phase I cannot understand Phase II format)

  Note: This is expected; old clients cannot understand new data
  Solution: Must use old Phase I version if needing to read Phase II data
            OR run compatible adapter that strips v2-only fields
```

---

### Step 8: Design Rollback Strategy
Plan how to recover if a phase upgrade fails.

**Rollback Procedures**:

```
Phase 1 → Phase 2 Rollback

Scenario: Phase 2 database migration fails partway
  - 50% of Phase 1 tasks migrated to v2 schema
  - 50% still in v1 schema
  - Phase 2 code cannot start (mixed schemas)

Rollback Steps:
  1. Stop Phase 2 servers (prevent further writes)
  2. Restore Phase 1 database from pre-migration backup
     Command: restore-db --from backup-2026-01-14-phase1.sql
  3. Verify all tasks are v1.0.0 format
     Query: SELECT COUNT(*) FROM tasks WHERE version NOT LIKE '1.%'
     Expected: 0 rows
  4. Restart Phase 1 servers
  5. Investigate failure cause
  6. Fix and retry migration after root cause identified

Recovery Time: 1-5 minutes (depending on database size)

Prerequisite: Must have taken backup BEFORE migration
  Backup command: mysqldump tasks > backup-2026-01-14-phase1.sql
  Backup size: ~1 MB per 10,000 tasks
  Storage: Keep backup for 1 week after successful upgrade

Phase 2 → Phase 3 Rollback

Scenario: Phase 3 code incompatible with Phase 2 data (bug in migration)
  - Phase 3 code expects recurrence_rule field
  - Phase 2 data doesn't have this field
  - Phase 3 code crashes

Rollback Steps:
  1. Stop Phase 3 servers
  2. Scale down Phase 3 pods to 0
  3. Scale up Phase 2 pods (restore from previous deployment)
  4. Redirect traffic to Phase 2 pods
  5. Database stays Phase 2 schema (don't revert data, it's too risky)
  6. Investigate code bug
  7. Fix code, test, then retry Phase 3 deployment

Recovery Time: 2-10 minutes (Kubernetes rolling back deployment)

Note: Database rollback NOT recommended here
  Reason: If Phase 3 writes data, reverting database loses those writes
  Safer: Just revert code, keep Phase 2 data, then redeploy Phase 3 after fix
```

---

### Step 9: Validate Versioning Strategy
Ensure strategy covers all phases and edge cases.

**Validation Checklist**:

```
✅ Version Format
  [ ] Chosen semantic versioning (MAJOR.MINOR.PATCH)
  [ ] Each phase has defined version (e.g., Phase II = 2.0.0)
  [ ] Increment rules documented (when bump MAJOR vs. MINOR vs. PATCH)

✅ Breaking Changes
  [ ] All breaking changes identified per phase
  [ ] Each breaking change triggers MAJOR version bump
  [ ] Non-breaking changes trigger MINOR version bump
  [ ] Migration functions exist for each breaking change

✅ Data Versioning
  [ ] Task objects have version field
  [ ] Upgrade functions chain migrations (1.0.0 → 2.0.0 → 3.0.0 → ...)
  [ ] Lazy migration strategy documented (upgrade on read, not all-at-once)
  [ ] Mixed-version collections supported (Phase 1 + Phase 2 data in same collection)

✅ Backward Compatibility
  [ ] Current version support guaranteed (mandatory)
  [ ] Previous MAJOR version support guaranteed (at least one phase back)
  [ ] Older versions have deprecation policy (announced before dropped)
  [ ] API changes are additive (new fields added, not removed)

✅ Storage Migration
  [ ] Phase 1 (memory) → Phase 2 (database) migration planned
  [ ] Phase 2 (database) → Phase 5 (cloud) migration planned
  [ ] Version tracking works across storage platforms
  [ ] Backup/restore procedures documented

✅ Rollback Strategy
  [ ] Rollback procedures for each phase transition
  [ ] Backup requirements defined (what to backup, how long to keep)
  [ ] Recovery time estimates provided
  [ ] Root cause investigation process defined

✅ Testing
  [ ] Upgrade path tested: v1.0.0 → 2.0.0 → 3.0.0 → ...
  [ ] Rollback path tested: v3.0.0 → v2.0.0 (via restore)
  [ ] Mixed-version data tested (old and new tasks in same collection)
  [ ] Backward compatibility tested (old code reading new fields = ignored)

✅ Documentation
  [ ] Compatibility matrix documented
  [ ] Migration paths documented with examples
  [ ] Rollback procedures documented step-by-step
  [ ] Version upgrade checklist provided for operators
```

---

## Output

**Format**: Structured Markdown document with versioning strategy:

```markdown
# Data Model Versioning and Backward Compatibility Strategy

## Executive Summary
[Brief overview of versioning approach and backward compatibility guarantees]

## Versioning Scheme
[MAJOR.MINOR.PATCH explanation and version roadmap]

## Breaking vs. Non-Breaking Changes
[Decision matrix and classification rules]

## Data Format Versioning
[Version field design and migration framework]

## Migration Paths
[Code examples for each phase transition]

## Backward Compatibility Policy
[Support duration and deprecation rules]

## Storage Migration
[Versioning across Phase 1→2→5]

## Rollback Strategy
[Recovery procedures and prerequisites]

## Version Compatibility Matrix
[Chart showing what code can read what data]

## Testing and Validation
[Test scenarios for upgrade and rollback paths]

## Summary and Checklist
[Validation that strategy covers all phases]
```

---

## Failure Handling

### Scenario 1: Breaking Change Not Identified
**Symptom**: Phase 2 adds required field without migration path; Phase 1 tasks fail
**Resolution**:
- This is a breaking change; must bump MAJOR version
- Add migration function that populates field with default for old tasks
- Example: user_id field → default to "system" for Phase 1 tasks
- Document in version release notes

### Scenario 2: Migration Function Loses Data
**Symptom**: Migration strips description field but Phase 2+ needs it
**Resolution**:
- Never remove data; move to archive table if needed
- Example: Phase 2 removes description? Move to description_archive table first
- Keep version field to track what was migrated
- Document data retention policy per field

### Scenario 3: Rollback Fails (No Backup)
**Symptom**: Phase 2 migration corrupts database; backup not available
**Resolution**:
- This is critical; prevent by making backups mandatory
- Procedure: Backup BEFORE migration, verify backup reads correctly
- If backup missing: Cannot recover automatically; must restore from disaster recovery
- Post-incident: Implement backup verification before all future migrations

### Scenario 4: Mixed Versions in Production
**Symptom**: Phase 2 pods serving Phase 2 data, Phase 1 pods still running on old version
**Resolution**:
- This is expected during rolling deployment
- Ensure Phase 2 code can read Phase 1 data (backward compatible)
- Ensure Phase 1 code doesn't need to read Phase 2 data (traffic routed correctly)
- Use compatibility matrix to verify this scenario is supported

### Scenario 5: Version Field Missing in Old Data
**Symptom**: Phase 1 backup has tasks without version field; cannot determine schema
**Resolution**:
- Assume oldest version (1.0.0) for unversioned tasks
- Add migration: "If no version field, assume v1.0.0, then upgrade"
- Example: `task_version = task.get('version', '1.0.0')`
- Document assumption clearly in migration code

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Data model versioning**: Apply same strategy to any evolving data model
- **API versioning**: HTTP API versions can use same MAJOR.MINOR.PATCH scheme
- **Database schema versioning**: SQL migrations can follow same patterns
- **Multi-product environments**: If managing multiple products, each gets version scheme
- **Microservices**: Each service has independent version (coordinated at deployment)

---

## Success Metrics

- ✅ Versioning scheme (semantic) clearly documented and understood
- ✅ All breaking changes identified and assigned MAJOR version bumps
- ✅ Migration functions exist and tested for each breaking change
- ✅ Data format includes version field for tracking
- ✅ Backward compatibility policy defined (current + 1 previous MAJOR version supported)
- ✅ Compatibility matrix shows what code/data combinations work
- ✅ Storage migration (Phase 1→2→5) has documented versioning
- ✅ Rollback procedures documented with recovery time estimates
- ✅ Backup requirements defined and enforced
- ✅ Test plan covers upgrade and rollback scenarios

---

## Related Skills

- **Data Model Designer (DMD-001)**: Initial Task entity design
- **Data Model Optimization (DMD-002)**: Refinements that may trigger version bumps
- **Functional Analysis (CLI-001)**: Specifies what data features need (informs breaking changes)
- **Quality Assurance (QA-001)**: Tests upgrade/rollback scenarios

---

## Example: Complete Versioning Roadmap

### Phase 1 (v1.0.0 - v1.1.0)

**v1.0.0 (Initial Phase 1)**
```
Required Fields:
  - id, title, status, created_timestamp

Optional Fields:
  - None yet
```

**v1.1.0 (Phase 1 Enhancement)**
```
Breaking Changes: None
New Optional Fields:
  - due_date (date, defaults to null)
  - priority (enum low/normal/high, defaults to "normal")
  - completed_timestamp (datetime, defaults to null)

Migration: None needed (all new fields optional)
Version Bump: MINOR (from 1.0.0 to 1.1.0)
```

### Phase 2 (v2.0.0 - v2.2.0)

**v2.0.0 (Phase 2 Major - Multi-User)**
```
Breaking Change: Add required user_id field
  Reason: Phase II is web app with multi-user support
  Impact: Phase 1 tasks don't have user_id
  Migration:
    FOR EACH task IN phase1_data:
      task['user_id'] = 'system'  # Default user
      task['version'] = '2.0.0'

Version Bump: MAJOR (1.x.x → 2.0.0)
Backup Required: YES (before migration)

Migration Function:
  def migrate_1_x_x_to_2_0_0(task):
      task['version'] = '2.0.0'
      task['user_id'] = task.get('user_id', 'system')
      return task
```

**v2.1.0 (Phase 2 Enhancement)**
```
Breaking Changes: None
New Optional Fields:
  - description (string, max 2000, defaults to null)
  - category_id (reference to Category entity, defaults to null)
  - color (string hex, defaults to null)

Migration: None needed (all new fields optional)
Version Bump: MINOR (2.0.0 to 2.1.0)
```

**v2.2.0 (Phase 2 Patch)**
```
Breaking Changes: None
Changes:
  - Clarified title cannot contain newlines (code already enforces)
  - Added indexes to improved query performance (no data change)
  - Fixed timestamp precision (microseconds now included)

Migration: None needed (code handles microseconds transparently)
Version Bump: PATCH (2.1.0 to 2.2.0)
```

### Phase 3 (v3.0.0)

**v3.0.0 (Phase 3 Major - AI Features)**
```
Breaking Changes:
  1. Add recurrence_rule field (optional, but complex structure)
  2. Expand status enum: (pending, completed) → (pending, in_progress, completed, cancelled, archived)

Migration:
  def migrate_2_x_x_to_3_0_0(task):
      task['version'] = '3.0.0'
      # New field, no conversion needed (all tasks get null by default)
      if 'recurrence_rule' not in task:
          task['recurrence_rule'] = None
      # Status enum expansion: old values still valid in new enum
      # No conversion needed
      return task

Version Bump: MAJOR (2.x.x → 3.0.0)
Backward Compatibility: Phase 2 code can still read Phase 3 data
  (Phase 3 tasks have status="pending" or "completed", understood by Phase 2)
Forward Compatibility: Phase 3 code can read Phase 2 data
  (Phase 2 tasks missing recurrence_rule; Phase 3 handles as null)
```

### Phase 4 (v4.0.0)

**v4.0.0 (Phase 4 Major - Kubernetes)**
```
Breaking Changes:
  1. Add cloud_backup_id field (optional, reference to backup service)
  2. Add last_synced_timestamp (optional, for cloud sync tracking)

Migration:
  def migrate_3_x_x_to_4_0_0(task):
      task['version'] = '4.0.0'
      task['cloud_backup_id'] = None
      task['last_synced_timestamp'] = datetime.utcnow()
      return task

Version Bump: MAJOR (3.x.x → 4.0.0)
Note: This is MAJOR only because it signals deployment to Kubernetes
      Actually non-breaking (all new fields optional), but MAJOR indicates
      infrastructure change (local → containerized)
```

### Phase 5 (v5.0.0)

**v5.0.0 (Phase 5 Major - Cloud Deployment)**
```
Breaking Changes:
  1. Add region field (string, required for cloud distribution)
  2. Add shard_id (required for distributed storage)
  3. Remove cloud_backup_id (replaced with native cloud backup)

Migration:
  def migrate_4_x_x_to_5_0_0(task, region='us-east-1'):
      task['version'] = '5.0.0'
      task['region'] = task.get('region', region)  # Default region for migrated tasks
      task['shard_id'] = task.get('shard_id', compute_shard(task['user_id'], region))
      # cloud_backup_id is removed (archived, not deleted)
      task.pop('cloud_backup_id', None)
      return task

Version Bump: MAJOR (4.x.x → 5.0.0)
Backup Required: YES (removing field is risky)

Deprecation: Phase 4 support can be announced as deprecated
  "Phase 4 (Kubernetes) code will not be supported after Phase 6"
  Allows operators 1 phase to prepare for migration
```

### Version Support Timeline

```
Timeline:
  2025-12: Phase 1 (v1.0.0 released)
  2026-01: Phase 2 (v2.0.0 released, v1.x.x support continues)
  2026-04: Phase 3 (v3.0.0 released, v2.x.x support continues)
  2026-07: Phase 4 (v4.0.0 released, v3.x.x support continues)
  2026-08: Phase 1 (v1.x.x) support announced as deprecated
  2027-01: Phase 5 (v5.0.0 released, v4.x.x support continues)
  2027-02: Phase 4 (v4.x.x) support announced as deprecated
  2027-08: Phase 1 (v1.x.x) support DROPPED
  2028-02: Phase 4 (v4.x.x) support DROPPED

Support Policy:
  Each MAJOR version supported for:
    - Minimum 6-12 months
    - At least through next MAJOR release + 6 months
    - Longer for critical versions (v2.0.0 = 18+ months)
```

---

## Conclusion

This versioning strategy ensures:

1. **Backward Compatibility**: Phase 1 tasks work in Phase 2, Phase 2 in Phase 3, etc.
2. **Clear Breaking Changes**: MAJOR version bumps signal required migrations
3. **Data Safety**: Migrations tested, backups taken, rollbacks available
4. **Gradual Adoption**: Old code can read new data (if backward compatible)
5. **Clear Deprecation**: Old versions announced for removal in advance
6. **Audit Trail**: Version field in each task tracks schema evolution

The strategy prioritizes **stability** and **safety** over agility, with explicit migration paths for each phase transition.

