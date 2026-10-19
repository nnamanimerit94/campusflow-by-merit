# Campusflow design decision 

## Decision 1: Ticket collection

For the ticket collection data structure, my member and i decided to use dictionary to store the tickets dictionary this is is as a result of the facf that dictionary users O(1)
 average-case time complexity for ticket lookup. while using list to search for a particular tickets which will require one to loop through all the tickets in that list but with dictionary using the key to fetch a ticket is quite easy. we decided to use strictly the id as the key.

## Decision 2: Input validation
we decided to create a function that specifically handles validating the input separated from the cli input handling first to ensure and have a clear separation of functions that handles it and also keeping the code free from unnecessary repetitive validation check

## Function Contracts

Purpose: to have a clear separated function that checks if value of affected_users is an int and the number is greated than or equal to 1 , else if valueerror or typeerror raises an exception 

Parameter: it receives the value of the affected_users

Accepted values: positive integers greater than or equal to one excluding booleans

Return value:first it checks if its a number and it returns the number back if positive

Errors: if theres an error it returns a the actual error raised 

Side effects: None. The function does not modify external data, print messages, or read user input.

## Validation Function Contracts

### validate_affected_users(value)
- Accepts: Positive integers only.
- Returns: The validated integer.
- Raises TypeError: When the input is not exactly an integer.
- Raises ValueError: When the integer is less than 1.
- Side effects: None.

### validate_urgency(value)
- Accepts: Strings representing low, medium, or high.
- Normalization: Removes surrounding whitespace and converts to lowercase.
- Returns: The normalized urgency string.
- Raises TypeError: When the input is not a string.
- Raises ValueError: When the urgency is invalid.
- Side effects: None.

### Title Validation

Function: validate_title(value)

Input: A string representing a ticket title.

Rules:
- Must be a string.
- Must not be empty or whitespace-only.
- Remove surrounding whitespace.
- Preserve capitalization.

Output: Cleaned title string.

Errors:
- TypeError for non-string inputs.
- ValueError for blank titles.

Side effects: None.

### Ticket ID Generation

Decision: Generate the next ticket ID using the highest existing ID + 1.

Rules:
- First ticket receives T001.
- IDs use the format T001, T002, T003, etc.
- Missing numbers are not reused while higher IDs exist.
- Ticket deletion is not supported in the MVP.

Trade-off:
This approach is simple but could reuse the highest ID if that
ticket were deleted. A persistent counter may be added later.

## Ticket Creation Contract

### Function
create_ticket(tickets, title, category, urgency, affected_users)

### Purpose
Create a new helpdesk ticket, validate its inputs, calculate
its priority, assign a unique ID, and store it in memory.

### Inputs
- tickets: Dictionary containing existing tickets.
- title: Non-empty string describing the issue.
- category: Network, Hardware, Software, or Other.
- urgency: low, medium, or high.
- affected_users: Positive integer greater than zero.
  Boolean values are not accepted.

### Validation
- Title is stripped of surrounding whitespace.
- Category is validated and normalized.
- Urgency is validated and converted to lowercase.
- Affected users must be a positive integer.
- Invalid inputs raise TypeError or ValueError.

### Generated Fields
- id: Generated using the highest existing ticket ID + 1.
- priority: Calculated from urgency and affected_users.
- status: Initially "open".
- assigned_to: Initially None.

### Output
Returns the newly created ticket as a dictionary.

### Side Effects
- Adds the new ticket to the supplied tickets dictionary.
- Does not modify existing tickets.
- Does not create a ticket if validation fails.

### ID Generation Decision
- First ticket ID is T001.
- Subsequent IDs increase sequentially.
- Missing numbers are not reused while higher IDs exist.
- Ticket deletion is not supported in the MVP.

### Limitations
- Tickets are currently stored in memory.
- Closing the application loses the tickets until JSON
  persistence is implemented.
- The ID generation approach assumes existing IDs are valid.
- Deleting the highest-numbered ticket could cause ID reuse.

## JSON Persistence Contract

### Functions
- save_tickets(tickets, file_path)
- load_tickets(file_path)

### Purpose
Persist tickets between application sessions using JSON files.

### Save Behavior
- Accepts a dictionary of tickets and a destination file path.
- Saves tickets as readable JSON with four-space indentation.
- Returns None on success.
- Allows file-writing and serialization errors to propagate.

### Load Behavior
- Returns saved tickets as a dictionary.
- Returns an empty dictionary if the file does not exist.
- Raises ValueError when the JSON is malformed.
- Does not modify the file during loading.

### Design Decision
Use Python's built-in json module to avoid external dependencies.

### Limitations
- Saving directly to a file can overwrite existing data.
- Atomic file replacement is not yet implemented.
- The current loader checks JSON syntax but does not fully validate
  the structure of saved ticket records.

  ## Ticket Workflow

### Functions
- find_ticket(tickets, ticket_id)
- assign_ticket(tickets, ticket_id, mentor)
- update_ticket_status(tickets, ticket_id, new_status)
- reopen_ticket(tickets, ticket_id)

### Business Rules
- Tickets begin with status `open`.
- Tickets must be assigned before moving to `in_progress`.
- Valid transitions are `open` → `in_progress` → `resolved`.
- Resolved tickets must be explicitly reopened before further changes.
- Reopening changes the status to `open` and preserves the assignment.
- Repeating the same status transition raises ValueError.
- Unknown ticket IDs raise KeyError.
- Assignment does not automatically change ticket status.

## Ticket Queries and Reporting

### Functions
- list_tickets(tickets)
- get_open_work_queue(tickets)
- get_ticket_report(tickets)

### Design Decisions
- Ticket listing uses ascending numeric ticket IDs.
- The open work queue excludes in-progress and resolved tickets.
- Open tickets are ordered by priority, highest first.
- Tickets with equal priority are ordered by ascending ticket ID.
- Reports count tickets by status and priority.
- Empty reports include all categories with zero counts.
- Query functions do not modify stored tickets.

## Phase 7: CLI Integration and JSON Persistence

### Overview

Phase 7 connects the existing CampusFlow modules into a working command-line application.

The CLI allows users to create, view, assign, resolve, and reopen tickets. It also provides an ordered work queue and ticket reports.

The implementation reuses existing validation, ticket creation, workflow, and query functions rather than duplicating business logic.

Ticket data is stored in `data/tickets.json` and loaded when the application starts.

---

## 1. Main Module (`main.py`)

### Responsibility

The `main.py` module is responsible for:

- Starting the CampusFlow application.
- Loading previously saved tickets.
- Displaying the application menu.
- Collecting user input.
- Calling existing business-logic functions.
- Handling expected errors without terminating the application.
- Saving changes after successful ticket operations.
- Displaying ticket information and reports.

Business validation and workflow rules remain in their existing modules.

### Function Contract: `display_menu()`

**Purpose:** Display the available CampusFlow menu options.

**Parameters:** None

**Returns:** `None`

**Behavior:**
- Displays menu options 1–9 and 0.
- Does not collect input.
- Does not modify ticket data.

**Side Effects:** Prints information to the terminal.

### Function Contract: `display_ticket(ticket)`

**Purpose:** Display the details of a single ticket.

**Parameters:**
- `ticket` (`dict`): A ticket containing all required ticket fields.

**Returns:** `None`

**Behavior:**
- Displays the ticket ID, title, category, urgency, affected users, priority, status, and assigned mentor.
- Displays `Unassigned` when no mentor is assigned.
- Does not modify the ticket.

**Exceptions:**
- `KeyError`: If a required ticket field is missing.

**Side Effects:** Prints ticket information to the terminal.

### Function Contract: `save_changes(tickets)`

**Purpose:** Save the current ticket collection and indicate whether saving succeeded.

**Parameters:**
- `tickets` (`dict`): Dictionary containing all current tickets.

**Returns:**
- `True`: If saving succeeds.
- `False`: If an operating-system error prevents saving.

**Behavior:**
1. Calls `save_tickets(tickets, FILE_PATH)`.
2. Returns `True` if saving completes successfully.
3. Catches `OSError` if saving fails.
4. Displays the error and returns `False`.

**Side Effects:** Writes ticket data to the configured JSON file.

**Dependencies:** `save_tickets()` from `campusflow.storage`.

### Function Contract: `main()`

**Purpose:** Control the CampusFlow application and coordinate all user operations.

**Parameters:** None

**Returns:** `None`

**Preconditions:**
- Required CampusFlow modules are available.
- The `data/` directory exists.
- The application has appropriate filesystem permissions.
- Existing ticket data, if present, is valid JSON.

**Behavior:**

1. Loads existing tickets using `load_tickets()`.
2. Starts with an empty dictionary if the JSON file does not exist.
3. Stops startup if the JSON file is corrupted or cannot be read.
4. Displays the menu repeatedly until the user exits.
5. Processes the selected menu operation.
6. Handles expected validation and workflow errors.
7. Saves successful ticket mutations.
8. Exits when the user selects option `0` or interrupts terminal input.

**Supported Operations:**

| Option | Operation | Functions Used |
|---|---|---|
| 1 | Create Ticket | Validation functions, `create_ticket()`, `save_changes()` |
| 2 | View All Tickets | `list_tickets()`, `display_ticket()` |
| 3 | Assign Ticket | `find_ticket()`, `assign_ticket()`, `save_changes()` |
| 4 | View Ticket Details | `find_ticket()`, `display_ticket()` |
| 5 | Start Working | `find_ticket()`, `update_ticket_status()`, `save_changes()` |
| 6 | Resolve Ticket | `find_ticket()`, `update_ticket_status()`, `save_changes()` |
| 7 | Reopen Ticket | `find_ticket()`, `reopen_ticket()`, `save_changes()` |
| 8 | View Open Work Queue | `get_open_work_queue()` |
| 9 | View Reports | `get_ticket_report()` |
| 0 | Exit | Ends the application loop |

**Error Handling:**

- Invalid ticket input: Display the error and request correction of the affected field.
- Invalid menu selection: Display an error and show the menu again.
- Missing ticket: Display the error without terminating the application.
- Invalid workflow transition: Display the error without modifying the ticket.
- Corrupted JSON during startup: Display an error and stop the application.
- File-saving failure: Display an error and do not report the operation as successful.
- `KeyboardInterrupt` or `EOFError`: Exit the application gracefully.

**Postconditions:**
- Successful ticket mutations are persisted to JSON.
- Invalid operations do not intentionally modify ticket data.
- Previously saved tickets remain available after restarting the application.

---

## 2. Storage Module (`campusflow/storage.py`)

### Responsibility

The storage module manages reading and writing ticket data using JSON files.

It provides two functions:

1. `load_tickets()`
2. `save_tickets()`

The module uses Python's standard library and does not require an external database.

### Function Contract: `load_tickets(file_path)`

**Purpose:** Load previously saved ticket data from a JSON file.

**Parameters:**
- `file_path` (`str` or path-like object): Location of the JSON file.

**Returns:**
- Parsed JSON data, expected to be a dictionary of tickets.
- An empty dictionary `{}` if the file does not exist.

**Behavior:**
1. Opens the specified file in read mode.
2. Uses `json.load()` to deserialize its contents.
3. Returns the loaded data.
4. Returns `{}` if the file does not exist.
5. Raises an error if the file contains malformed JSON.

**Exceptions:**
- `ValueError`: If the JSON file contains invalid JSON.
- `OSError`: If another filesystem error prevents reading.

**Side Effects:** Reads from the filesystem without modifying the file.

**Constraints:**
- Corrupted JSON must not be silently replaced with an empty dictionary.
- The function does not validate individual ticket fields.
- The current implementation does not verify that valid JSON contains a dictionary.

### Function Contract: `save_tickets(tickets, file_path)`

**Purpose:** Save the complete ticket collection to a JSON file using temporary-file replacement.

**Parameters:**
- `tickets` (`dict`): Complete collection of tickets to save.
- `file_path` (`str` or path-like object): Destination JSON file.

**Returns:** `None`

**Preconditions:**
- Ticket data is JSON-serializable.
- The destination directory exists.
- The application has permission to write to the directory.

**Behavior:**
1. Determines the destination directory.
2. Creates a temporary file in the same directory.
3. Serializes the ticket dictionary using `json.dump()`.
4. Flushes the temporary file.
5. Synchronizes the temporary file's contents using `os.fsync()`.
6. Replaces the destination file using `os.replace()`.
7. Removes any remaining temporary file during cleanup.

**Exceptions:**
- `OSError`: If a filesystem operation fails.
- `TypeError`: If the supplied data cannot be serialized to JSON.

**Side Effects:**
- Creates a temporary JSON file.
- Replaces the destination JSON file after writing succeeds.
- Removes temporary files during cleanup.

**Postconditions:**
- On success, the destination contains the complete supplied ticket collection.
- On failure before replacement, the original destination file remains unchanged.
- The function does not modify the in-memory ticket dictionary.

**Constraints:**
- Saving replaces the destination file's contents with the supplied dictionary.
- The function does not automatically merge old and new tickets.
- Existing tickets must be loaded before new tickets are added.
- The application assumes a single process modifies the JSON file at a time.
- Atomic replacement reduces the risk of partial writes but does not guarantee protection against every hardware or filesystem failure.

---

## 3. Data Flow

CampusFlow follows this sequence:

```text
Application starts
        |
        v
load_tickets()
        |
        v
Load existing tickets into memory
        |
        v
Display menu
        |
        v
User selects an operation
        |
        v
Collect and validate input
        |
        v
Call existing business-logic function
        |
        v
Update in-memory ticket dictionary
        |
        v
save_changes()
        |
        v
save_tickets()
        |
        v
Write temporary JSON file
        |
        v
Replace original JSON file
        |
        v
Display success or failure
        |
        v
Return to menu
```

Read-only operations, such as viewing tickets and reports, do not require saving.

---

## 4. Design Decisions

| Decision | Reason |
|---|---|
| Keep CLI logic in `main.py` | Maintain a simple structure appropriate for the project |
| Reuse existing validation functions | Avoid duplicating business rules |
| Use `try/except` | Handle expected errors without crashing |
| Retry invalid fields individually | Allow users to correct mistakes without restarting ticket creation |
| Load JSON at startup | Preserve previously saved tickets |
| Save after ticket mutations | Keep stored data updated |
| Use JSON storage | Meet project requirements without external dependencies |
| Use temporary-file replacement | Reduce the risk of damaging existing data during saving |
| Stop startup when JSON is corrupted | Prevent accidental overwriting of potentially recoverable records |
| Keep storage separate from business logic | Improve organization and testability |

---

## 5. Known Limitations

1. The application is designed for one running instance at a time.
2. Concurrent modifications to the same JSON file are not supported.
3. JSON structure validation is not performed during loading.
4. The CLI handles expected user and filesystem errors but does not suppress unexpected programming errors.
5. Temporary-file replacement improves persistence safety but does not guarantee protection against every possible system failure.

---

## 6. Testing Requirements

The following behaviors must be verified before Phase 7 is considered complete:

- Existing tickets load correctly at startup.
- Missing JSON files result in an empty ticket collection.
- Corrupted JSON prevents unsafe startup.
- Invalid input does not terminate the application.
- Users can retry only the field they entered incorrectly.
- Tickets can be created, viewed, and assigned.
- Ticket status transitions follow existing workflow rules.
- Resolved tickets can be reopened.
- The work queue contains only open tickets in the correct order.
- Reports display accurate ticket counts.
- Saved tickets remain available after restarting the application.
- File-saving failures do not produce false success messages.
- Existing unit tests continue to pass.
- CLI integration tests cover the complete user workflow.

**Phase 7 completion criteria:** All menu operations work correctly, persistence is verified, expected errors are handled, and automated tests pass.