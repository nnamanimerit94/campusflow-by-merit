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