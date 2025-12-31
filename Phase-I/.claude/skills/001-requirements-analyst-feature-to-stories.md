# Skill: Feature to User Stories Conversion

**Skill ID**: RA-001
**Agent Owner**: requirements-analyst
**Project**: Evolution of Todo Hackathon II – Phase 1
**Status**: Production

---

## Purpose

Convert high-level feature descriptions into clear, testable user stories that communicate user intent and business value without prescribing technical implementation. This skill ensures requirements capture user needs in a way that is actionable, measurable, and independently implementable.

---

## When to Use

- **Feature specification phase**: When breaking down Phase 1 requirements (create task, list tasks, mark complete, delete task, filter/sort)
- **Sprint planning**: Before assigning work to development team
- **Acceptance testing**: To define test scenarios and acceptance criteria
- **Stakeholder communication**: To align on feature scope and user intent without getting lost in technical details
- **Requirement clarification**: When feature descriptions are vague or ambiguous

---

## Inputs

1. **Feature description** (text): High-level feature statement (e.g., "implement task creation", "add task filtering")
2. **User persona** (text, optional): Target user type (e.g., "individual productivity user", "team member")
3. **Business context** (text, optional): Why this feature matters (e.g., "Phase 1 MVP", "core user flow")
4. **Constraints** (text, optional): Limitations or requirements (e.g., "console-only", "in-memory storage")

---

## Step-by-Step Process

### Step 1: Identify the User Role
- Determine who will use this feature (e.g., "productivity-focused individual", "task organizer", "team collaborator")
- Avoid generic "user" if possible; be specific to actual usage pattern
- If multiple user roles benefit from feature, create separate stories for each role

**Example**:
- Feature: "task creation"
- User roles: individual user managing personal tasks, team member creating shared tasks

### Step 2: Extract Core User Intent
- What action does the user want to perform? (verb + object)
- What is the user trying to accomplish?
- Avoid technical terms (e.g., "persist data" → "save task for later", "filter results" → "see only important tasks")

**Example**:
- Intent: "User wants to save a new task quickly without leaving their workflow"

### Step 3: Identify Primary Benefit
- Why does the user want this feature?
- What problem does it solve or what outcome does it enable?
- Focus on user value, not technical advantage

**Example**:
- Benefit: "so I don't forget what I need to do"
- Benefit: "so I can organize my work and stay focused"

### Step 4: Formulate Story in Standard Format
- **Format**: "As a <user role>, I want <action/feature> so that <benefit>"
- Keep each clause concise (one sentence per clause)
- Ensure the story is independently testable (can be implemented and verified in isolation)

**Example**:
- "As an individual user, I want to create a new task with a title so that I can capture work I need to do"
- "As a user, I want to add a due date to a task so that I can prioritize by deadline"

### Step 5: Define Happy Path Scenario
- What is the successful outcome when the user interacts with this feature?
- Describe in plain language (Given-When-Then format)

**Example**:
- **Given** the user is in the task app
- **When** the user enters a task title and confirms
- **Then** the task appears in the task list immediately

### Step 6: Define Alternative Flows
- What happens if input is invalid? (e.g., empty title)
- What if the user cancels? (e.g., discard without saving)
- What edge cases exist? (e.g., very long titles, special characters)

**Example**:
- **When** the user tries to create a task with no title, **Then** show error message and don't save
- **When** the user presses Escape during creation, **Then** cancel and return to list without saving

### Step 7: Verify Testability
- Can a QA engineer test this story independently without other stories?
- Is the acceptance criteria clear and measurable?
- Does the story avoid "and" clauses that indicate multiple features?

**Red flags**:
- "User wants to create and delete tasks" → Split into two stories
- "System must persist data and validate input" → Technical concern, not user story

---

## Output

**Format**: Markdown list with the following structure:

```
### User Story: [Brief Title] (Priority: P1/P2/P3)

**Story**: "As a <user>, I want <feature> so that <benefit>"

**Happy Path**:
1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. (additional steps if multi-step workflow)

**Alternative Flows**:
1. **When** [error condition], **Then** [error handling]
2. **When** [user cancels], **Then** [cancellation behavior]

**Acceptance Criteria**:
- [ ] Task is created with title
- [ ] Task appears in list immediately
- [ ] Error shown if title is empty
- [ ] Can cancel without saving
```

---

## Failure Handling

### Scenario 1: Feature Description is Too Vague
**Symptom**: Cannot identify clear user intent or benefit
**Resolution**:
- Ask clarifying questions: "Who uses this? What problem does it solve?"
- Break feature into smaller, more specific features
- Example: "task management" → split into "create task", "view task", "update task", "delete task"

### Scenario 2: Feature Has Multiple User Roles
**Symptom**: One feature serves different user types with different benefits
**Resolution**:
- Create separate user story for each role
- Example: "As an individual user, I want to..." vs "As a team member, I want to..."

### Scenario 3: Story Contains Technical Implementation Details
**Symptom**: Story mentions database, API endpoints, UI frameworks, or data structures
**Resolution**:
- Rewrite from user perspective
- Bad: "As a user, I want data persisted to PostgreSQL so that it's durable"
- Good: "As a user, I want my tasks saved so that they're available when I open the app again"

### Scenario 4: Story is Too Large or Contains "And"
**Symptom**: Story requires multiple unrelated features or has "and" conjunctions
**Resolution**:
- Split into two or more independent stories
- Example: "As a user, I want to create tasks and assign them to others"
  - Story 1: "...I want to create tasks so that..."
  - Story 2: "...I want to assign tasks to others so that..."

### Scenario 5: Acceptance Criteria are Unclear
**Symptom**: Test scenarios or success conditions are ambiguous
**Resolution**:
- Add concrete examples
- Use specific values instead of variables
- Example: Bad: "Task should display correctly" → Good: "Task title (max 255 chars) displays on first line with ellipsis if truncated"

---

## Reusability Notes

This skill is **deterministic and reusable** across:
- **Any feature in Phase 1**: Task creation, listing, filtering, deletion, completion
- **Requirement clarification cycles**: Apply same process to refine vague requirements
- **Future phases**: User story format is consistent across Phase II–V
- **Handoff to development**: Stories output by this skill are directly usable in task.md generation

---

## Success Metrics

- ✅ Each user story is independently testable
- ✅ No technical implementation details in story text
- ✅ Clear happy path and alternative flows documented
- ✅ Acceptance criteria are measurable and concrete
- ✅ User intent and value are explicit (not implied)

---

## Related Skills

- **CLI-UX-Designer**: Designs command-line interface that implements these user stories
- **Business-Logic-Engineer**: Defines business rules that govern story execution (e.g., duplicate task handling, due date validation)
- **Data-Model-Designer**: Creates data structures to support these user stories

---

## Example: Phase 1 Core Stories (Generated Using This Skill)

### User Story: Create Task (Priority: P1)

**Story**: "As a productivity user, I want to create a new task with a title so that I can capture work I need to do"

**Happy Path**:
1. **Given** the user is in the task app, **When** the user enters command to create a new task, **Then** the app prompts for task title
2. **Given** the app is waiting for input, **When** the user enters a task title and confirms, **Then** the task is added to the list and confirmed with success message

**Alternative Flows**:
1. **When** the user submits an empty title, **Then** show error "Task title cannot be empty" and return to input prompt
2. **When** the user presses Escape or Ctrl+C, **Then** cancel task creation and return to main menu without saving

**Acceptance Criteria**:
- [ ] New task is created with non-empty title (max 255 characters)
- [ ] Task appears immediately in the task list
- [ ] Success confirmation displayed to user
- [ ] Empty title is rejected with clear error message
- [ ] Cancellation via Escape/Ctrl+C is supported without saving
