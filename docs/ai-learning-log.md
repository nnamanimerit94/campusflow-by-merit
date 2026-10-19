# CampusFlow — AI Learning Log

## 1. Project Overview

CampusFlow is a Python command-line helpdesk management system designed to help campus staff create, prioritize, assign, and track support requests.

The project was developed as a team software engineering exercise.

AI was used as a learning and development assistant throughout the project.

Its role included helping us understand technical concepts, review implementation approaches, identify potential errors, and improve code quality.

## 2. How We Used AI

### Understanding the Project Requirements

AI helped us break down the project requirements into smaller, manageable tasks.

We identified the main components of CampusFlow:

- Input validation
- Priority calculation
- Ticket creation
- JSON storage
- Ticket workflow management
- Ticket queries and reporting
- Command-line integration
- Automated testing

This helped us organize the development process and divide responsibilities.

### Understanding Python Concepts

During development, AI helped explain Python concepts relevant to our implementation.

These included:

- Dictionaries and key-based lookups
- Functions and parameters
- Exception handling
- JSON serialization and deserialization
- File handling
- Python modules and imports
- Unit testing
- Git branches and pull requests

These explanations helped us understand why particular approaches were suitable for the project.

### Reviewing Code and Debugging

AI assisted with reviewing code, identifying possible errors, and suggesting corrections.

We used it to examine how different modules interacted and how to handle invalid inputs and unexpected failures.

AI suggestions were evaluated against the project's existing requirements and function contracts.

### CLI Integration

AI assisted with integrating the existing modules into `main.py`.

The CLI connects ticket creation, validation, assignment, status management, queries, reporting, and JSON persistence.

One important design correction involved ticket status management.

An earlier implementation introduced separate menu options for starting work and resolving tickets.

However, our existing function contract was:

`update_ticket_status(tickets, ticket_id, new_status)`

We corrected the CLI so administrators enter the desired status, while the existing workflow function determines whether the transition is valid.

This allowed us to reuse our existing business logic rather than introduce unnecessary duplication.

### Testing

AI assisted with preparing automated CLI tests using Python's built-in `unittest` framework.

The tests covered operations such as:

- Creating tickets
- Handling invalid input
- Assigning tickets
- Updating ticket statuses
- Reopening tickets
- Loading existing data
- Handling corrupted JSON
- Handling file-saving failures

The project had 96 existing tests before the CLI integration tests were added.

An additional 23 CLI tests were introduced, bringing the total to 119 automated tests.

The tests passed during the final Phase 7 verification.

## 3. Important Technical Decisions

### Using Dictionaries for Ticket Storage

We selected a dictionary to store tickets, using each ticket ID as its key.

This supports efficient ticket lookup without searching through a list of every ticket.

### Separating Validation from User Input

We implemented validation functions separately from the CLI.

This allows validation rules to be reused across the application.

The CLI collects input and displays errors, while the validation functions determine whether the supplied values are acceptable.

### Separating Business Logic into Modules

Instead of implementing all functionality in one file, we organized the application into modules.

Each module handles a specific responsibility.

This made it easier to develop, test, and integrate the different components.

### Using JSON Persistence

We used JSON because it is supported by Python's standard library and was suitable for the project's scope.

During integration, we improved the saving process by writing data to a temporary file before replacing the destination file.

This reduces the risk of damaging existing data if a write fails.

### Reusing Existing Functions

We decided that the CLI should call existing functions rather than recreate their logic.

For example, the CLI uses the workflow module to validate ticket status transitions.

This helps maintain consistent behavior across the application.

## 4. Challenges Encountered

### Integrating Team Members' Work

One challenge was bringing together code developed in separate Git branches.

We needed to ensure that modules used compatible function names, parameters, and data structures.

We addressed this by reviewing function contracts and testing the integrated application.

### Avoiding Duplicate Validation

During CLI development, we identified situations where validation rules were being repeated unnecessarily.

We corrected this by relying on the existing validation functions.

This reinforced the importance of separating responsibilities between modules.

### Handling Ticket Status Transitions

We needed to ensure that tickets followed the agreed workflow:

`open → in_progress → resolved`

Tickets must be assigned before work begins.

Resolved tickets must be explicitly reopened before they can move through the workflow again.

We used the existing workflow functions to enforce these rules.

### Preserving Ticket Data

An important challenge was ensuring that tickets remained available after the application closed.

We implemented JSON loading and saving and improved the saving process to reduce the risk of incomplete writes.

We also handled missing and malformed JSON files differently to avoid accidentally losing existing records.

### Managing Git Branches

The team worked with feature branches and merged completed work into the main branch.

This provided practical experience with version control, integration, and pull requests.

## 5. Lessons Learned

### AI Suggestions Must Be Reviewed

We learned that AI-generated suggestions should not automatically be accepted.

Some suggestions may introduce unnecessary complexity or differ from an existing design decision.

We therefore needed to compare proposed changes with our requirements and function contracts.

### Simplicity Matters

We learned that software does not need unnecessary abstractions to be well organized.

For CampusFlow, using straightforward functions and clearly separated modules helped keep the implementation understandable.

### Testing Helps Detect Problems Early

Automated testing helped us verify that individual modules behaved as expected.

After integrating the CLI, we ran the existing tests again to check that earlier functionality still worked.

We also added tests for the new CLI behavior.

### Function Contracts Improve Integration

Clearly defined function contracts helped us understand how modules should communicate.

They also made it easier to identify implementation decisions that did not match the agreed design.

### Error Handling Is Part of Application Design

We learned that handling invalid input, missing files, corrupted JSON, and saving failures is important for building a reliable application.

The application should explain expected errors clearly instead of terminating unexpectedly or silently discarding data.

## 6. Responsible Use of AI

Throughout the project, AI served as an assistant rather than the final authority on implementation decisions.

We used AI to:

- Explain unfamiliar concepts.
- Suggest possible implementation approaches.
- Review code and identify potential problems.
- Assist with debugging.
- Generate and improve automated tests.
- Support technical documentation.

We remained responsible for evaluating suggestions, making project decisions, running tests, and integrating the final implementation.

## 7. Final Project Outcome

CampusFlow was completed as a command-line minimum viable product.

The completed application supports:

- Ticket creation
- Automatic priority calculation
- Ticket assignment
- Ticket status management
- Ticket reopening
- Ticket listing and details
- Priority-based open work queues
- Ticket reports
- JSON persistence

The completed implementation was merged into the main Git branch.

The final test suite contained 119 automated tests.

## 8. Conclusion

Developing CampusFlow provided practical experience in modular Python programming, input validation, file handling, automated testing, Git collaboration, and application integration.

Using AI during development also reinforced the importance of understanding generated code, evaluating technical suggestions, and making deliberate engineering decisions.

The project demonstrated how separate software components can be combined into a functional command-line application.